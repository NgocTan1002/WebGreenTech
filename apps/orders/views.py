from django.views.generic import TemplateView, DetailView, CreateView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q

from .models import Order, OrderItem, QuoteRequest
from .forms import CheckoutForm, QuoteRequestForm
from apps.cart.services import CartService
from apps.products.models import Product
from apps.contacts.tasks import send_contact_notification
from apps.orders.tasks import (
    send_order_confirmation_email,
    send_quote_notification_email,
)
from apps.core.db import get_cart_detail, get_cart_summary


class CheckoutView(TemplateView):
    """Multi-step checkout: cart review → contact → confirmation."""
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartService.get_or_create_cart(self.request)
        cart_items = get_cart_detail(str(cart.id))
        summary = get_cart_summary(str(cart.id))
        context['cart'] = cart
        context['cart_items'] = cart_items
        context['subtotal'] = summary['subtotal']
        context['has_pending_quote'] = any(
            item.get('price_pending') for item in cart_items
        )

        user = self.request.user
        context['form'] = CheckoutForm(
            initial={
                'email':        user.email        if user.is_authenticated else '',
                'first_name':   user.first_name   if user.is_authenticated else '',
                'last_name':    user.last_name    if user.is_authenticated else '',
                'company_name': user.company_name if user.is_authenticated else '',
                'phone':        user.phone        if user.is_authenticated else '',
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        cart = CartService.get_or_create_cart(request)

        if not cart.items.exists():
            messages.error(request, 'Giỏ hàng của bạn đang trống.')
            return redirect('cart:detail')

        if form.is_valid():
            has_pending_quote = cart.items.filter(
                ~Q(pricing_type=Product.PRICING_FIXED) | Q(unit_price__isnull=True)
            ).exists()
            order_type = (
                Order.ORDER_TYPE_QUOTE
                if has_pending_quote
                else Order.ORDER_TYPE_PURCHASE
            )
            order = Order.objects.create(
                order_type=order_type,
                customer=request.user if request.user.is_authenticated else None,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                company_name=form.cleaned_data.get('company_name', ''),
                phone=form.cleaned_data.get('phone', ''),
                shipping_address=form.cleaned_data.get('shipping_address', {}),
                billing_address=form.cleaned_data.get('billing_address', {}),
                customer_notes=form.cleaned_data.get('notes', ''),
            )

            for item in cart.items.select_related('product').all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_sku=item.product.sku,
                    quantity=item.quantity,
                    pricing_type=item.pricing_type,
                    unit_price=item.unit_price,
                )
            order.calculate_totals()  # fix: method đúng tên
            transaction.on_commit(
                lambda order_id=str(order.id):
                send_order_confirmation_email.delay(order_id)
            )

            cart.is_active = False
            cart.save(update_fields=['is_active'])
            request.session.pop('cart_session_key', None)  # fix: dùng pop tránh KeyError

            if has_pending_quote:
                messages.success(
                    request,
                    f'Yêu cầu báo giá {order.order_number} đã được tiếp nhận.',
                )
                return redirect('orders:quote_success')

            messages.success(
                request,
                f'Đơn hàng {order.order_number} đã được tiếp nhận.',
            )
            return redirect(
                'orders:confirmation',
                order_number=order.order_number,
            )

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class OrderConfirmationView(TemplateView):
    template_name = 'orders/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, order_number=kwargs['order_number'])
        context['order'] = order
        context['order_items'] = order.items.select_related('product').all()
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'

    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).prefetch_related('items__product')


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).order_by('-created_at')


class QuoteRequestView(CreateView):
    """Standalone quote request form (not from cart)."""
    model = QuoteRequest
    form_class = QuoteRequestForm
    template_name = 'orders/quote_request.html'
    success_url = reverse_lazy('orders:quote_success')

    def get_initial(self):
        initial = super().get_initial()

        product_slug = self.request.GET.get('product')
        if product_slug:
            try:
                product = Product.objects.get(slug=product_slug, status='published')
                initial['message'] = (
                    f'Tôi quan tâm đến sản phẩm {product.name} (SKU: {product.sku}). '
                    f'Vui lòng cung cấp báo giá và tình trạng hàng.'
                )
            except Product.DoesNotExist:
                pass

        solution_slug = self.request.GET.get('solution')
        if solution_slug:
            from apps.solutions.models import Solution
            try:
                solution = Solution.objects.get(slug=solution_slug, status='published')
                initial['solution'] = solution
                initial['message'] = (
                    f'Tôi muốn tìm hiểu thêm về giải pháp "{solution.title}".'
                )
            except Solution.DoesNotExist:
                pass

        if self.request.user.is_authenticated:
            user = self.request.user
            initial.update({
                'name':    user.get_full_name(),
                'email':   user.email,
                'phone':   user.phone,
                'company': user.company_name,
            })
        return initial

    def form_valid(self, form):
        quote = form.save()
        from apps.contacts.tasks import send_contact_notification
        # Reuse contact notification hoặc tạo task riêng sau
        send_quote_notification_email.delay(quote.pk)
        messages.success(
            self.request,
            f'Yêu cầu báo giá #{quote.reference} đã được gửi. Chúng tôi sẽ liên hệ sớm nhất!'
        )
        return redirect(self.success_url)


class QuoteSuccessView(TemplateView):
    template_name = 'orders/quote_success.html'
