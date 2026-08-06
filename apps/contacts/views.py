from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import ContactInquiry, DemoRequest
from .forms import ContactForm, DemoRequestForm

class ContactView(CreateView):
    model = ContactInquiry
    form_class = ContactForm
    template_name = 'contacts/contact.html'
    success_url = reverse_lazy('contacts:success')

    def get_initial(self):
        initial = super().get_initial()
        product_slug = self.request.GET.get('product')
        if product_slug:
            from apps.products.models import Product
            try:
                product = Product.objects.get(slug=product_slug, status='published')
                initial.update({
                    'inquiry_type': ContactInquiry.INQUIRY_SALES,
                    'subject': f'Tư vấn sản phẩm {product.name}',
                    'message': (
                        f'Tôi quan tâm đến sản phẩm {product.name} '
                        f'(SKU: {product.sku}). Vui lòng liên hệ tư vấn thêm.'
                    ),
                })
            except Product.DoesNotExist:
                pass
        return initial

    def form_valid(self, form): 
        inquiry = form.save(commit=False)
        inquiry.ip_address = self.request.META.get('REMOTE_ADDR')
        inquiry.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        inquiry.source_url = self.request.META.get('HTTP_REFERER', '')
        inquiry.save()
        from .tasks import send_contact_notification
        send_contact_notification.delay(inquiry.pk)
        return redirect(self.success_url)
    
class ContactSuccessView(TemplateView):
    template_name = 'contacts/success.html'

class DemoRequestView(CreateView):
    model = DemoRequest
    form_class = DemoRequestForm
    template_name = 'contacts/demo_request.html'
    success_url = reverse_lazy('contacts:demo_success')
 
    def get_initial(self):
        initial = super().get_initial()
        solution_slug = self.request.GET.get('solution')
        if solution_slug:
            from apps.solutions.models import Solution
            try:
                sol = Solution.objects.get(slug=solution_slug)
                initial['solution'] = sol
            except Solution.DoesNotExist:
                pass
        return initial
 
    def form_valid(self, form):
        demo = form.save()
        from .tasks import send_demo_request_notification
        send_demo_request_notification.delay(demo.pk)
        return redirect(self.success_url)
 
 
class DemoSuccessView(TemplateView):
    template_name = 'contacts/demo_success.html'
