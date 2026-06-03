"""Internal staff dashboard views."""
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta


# ---------------------------------------------------------------------------
# Base — apply staff_member_required once, inherit everywhere
# ---------------------------------------------------------------------------

@method_decorator(staff_member_required, name='dispatch')
class StaffRequiredMixin(TemplateView):
    """
    Base view that gates all dashboard views behind staff_member_required.
    Inherit instead of repeating @method_decorator on every subclass.
    """
    pass


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

class DashboardHomeView(StaffRequiredMixin):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.orders.models import Order, QuoteRequest
        from apps.contacts.models import ContactInquiry
        from apps.products.models import Product

        week_ago = timezone.now() - timedelta(days=7)

        context.update({
            # Counts — cheap, index-only scans
            'total_orders':      Order.objects.count(),
            'orders_this_week':  Order.objects.filter(created_at__gte=week_ago).count(),
            'pending_quotes':    QuoteRequest.objects.filter(status='new').count(),
            'new_contacts':      ContactInquiry.objects.filter(status='new').count(),
            'total_products':    Product.objects.filter(status='published').count(),
            'low_stock_products': Product.objects.filter(stock_status='low_stock').count(),

            # Recent rows — select_related avoids N+1 in templates
            'recent_orders': (
                Order.objects
                .select_related('customer')
                .order_by('-created_at')
                [:10]
            ),
            'recent_quotes': (
                QuoteRequest.objects
                .order_by('-created_at')
                [:10]
            ),
        })
        return context


class DashboardProductsView(StaffRequiredMixin):
    template_name = 'dashboard/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.products.models import Product

        base_qs = Product.objects.select_related('category', 'brand')

        context['top_viewed'] = (
            base_qs
            .filter(status='published')
            .order_by('-view_count')
            [:20]
        )
        context['low_stock'] = (
            base_qs
            .filter(stock_status__in=['low_stock', 'out_of_stock'])
            .order_by('stock_status', 'stock_quantity')
            [:20]
        )
        return context


class DashboardOrdersView(StaffRequiredMixin):
    template_name = 'dashboard/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.orders.models import Order

        context['orders'] = (
            Order.objects
            .select_related('customer')
            .prefetch_related('items')
            .order_by('-created_at')
            [:50]
        )
        return context


class DashboardQuotesView(StaffRequiredMixin):
    template_name = 'dashboard/quotes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.orders.models import QuoteRequest

        context['quotes'] = (
            QuoteRequest.objects
            .select_related('solution', 'assigned_to', 'converted_to_order')
            .prefetch_related('items')
            .order_by('-created_at')
            [:50]
        )
        return context


class DashboardContactsView(StaffRequiredMixin):
    template_name = 'dashboard/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.contacts.models import ContactInquiry

        context['contacts'] = (
            ContactInquiry.objects
            .order_by('-created_at')
            [:50]
        )
        return context


class DashboardAnalyticsView(StaffRequiredMixin):
    template_name = 'dashboard/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.products.models import Product
        from apps.orders.models import Order, QuoteRequest
        from apps.blog.models import Post
        from django.db.models import Count, Sum

        # ── Date ranges ───────────────────────────────────────────────────
        now      = timezone.now()
        day_30   = now - timedelta(days=30)
        day_7    = now - timedelta(days=7)

        # ── Orders revenue (last 30 days) ─────────────────────────────────
        revenue_30d = (
            Order.objects
            .filter(created_at__gte=day_30)
            .aggregate(total=Sum('total'))['total'] or 0
        )

        # ── Top 10 products by view count ─────────────────────────────────
        top_products = (
            Product.objects
            .filter(status='published')
            .order_by('-view_count')
            .values('name', 'slug', 'sku', 'view_count', 'stock_status')
            [:10]
        )

        # ── Orders by status ──────────────────────────────────────────────
        orders_by_status = (
            Order.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )

        # ── Quote funnel (last 30 days) ────────────────────────────────────
        quote_funnel = (
            QuoteRequest.objects
            .filter(created_at__gte=day_30)
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )

        # ── Top blog posts by view count ──────────────────────────────────
        top_posts = (
            Post.objects
            .filter(status='published')
            .order_by('-view_count')
            .values('title', 'slug', 'view_count', 'post_type')
            [:10]
        )

        context.update({
            'revenue_30d':      revenue_30d,
            'top_products':     top_products,
            'orders_by_status': orders_by_status,
            'quote_funnel':     quote_funnel,
            'top_posts':        top_posts,
            'period_start':     day_30.date(),
            'period_end':       now.date(),
        })
        return context
