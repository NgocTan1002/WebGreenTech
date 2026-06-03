from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms

from .models import Customer
class CustomerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu *'}),
        label='Mật khẩu',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nhập lại mật khẩu *'}),
        label='Xác nhận mật khẩu',
    )

    class Meta:
        model = Customer
        fields = [
            'email', 'first_name', 'last_name',
            'phone', 'company_name', 'company_type', 'job_title',
        ]

    def clean(self):
        cd = super().clean()
        if cd.get('password1') != cd.get('password2'):
            self.add_error('password2', 'Mật khẩu không khớp.')
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class RegisterView(CreateView):
    model = Customer
    form_class = CustomerRegistrationForm
    template_name = 'customers/register.html'
    success_url = reverse_lazy('customers:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(
            self.request,
            self.object,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = [
        'first_name', 'last_name', 'phone',
        'company_name', 'company_type', 'job_title', 'industry',
    ]
    template_name = 'customers/profile.html'
    success_url = reverse_lazy('customers:profile')

    def get_object(self, queryset=None):
        return self.request.user


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        from apps.orders.models import Order, QuoteRequest
        context['recent_orders'] = (
            Order.objects
            .filter(customer=user)
            .order_by('-created_at')
            .select_related()
            [:5]
        )
        context['recent_quotes'] = (
            QuoteRequest.objects
            .filter(email=user.email)
            .order_by('-created_at')
            [:5]
        )
        return context