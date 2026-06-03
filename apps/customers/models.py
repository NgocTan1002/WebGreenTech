import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
from apps.core.models import TimeStampedModel


class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Cần có email để tạo tài khoản')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom user model cho B2B platform.
    Đăng nhập bằng email thay vì username.
    """
    # ─── Thông tin cơ bản ─────────────────────────────────────────────────────
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)

    # ─── Thông tin công ty (B2B) ──────────────────────────────────────────────
    company_name = models.CharField(max_length=255, blank=True)
    company_type = models.CharField(
        max_length=50,
        choices=[
            ('manufacturer',  'Nhà sản xuất'),
            ('integrator',    'System Integrator'),
            ('distributor',   'Nhà phân phối'),
            ('end_user',      'End User'),
            ('other',         'Khác'),
        ],
        blank=True,
    )
    job_title = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=200, blank=True)

    # ─── Trạng thái ───────────────────────────────────────────────────────────
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)

    # ─── Tùy chỉnh ────────────────────────────────────────────────────────────
    newsletter_subscribed = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('customers:profile')


class CustomerAddress(TimeStampedModel):
    """Sổ địa chỉ giao hàng / thanh toán cho khách hàng B2B."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=100, default='Văn phòng', help_text='Ví dụ: "Văn phòng", "Kho hàng"')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company = models.CharField(max_length=255, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Việt Nam')
    phone = models.CharField(max_length=30, blank=True)
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Customer Address'
        verbose_name_plural = 'Customer Addresses'

    def __str__(self):
        return f'{self.customer.email} — {self.label}'

    @property
    def full_address(self):
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.extend([self.city, self.state, self.postal_code, self.country])
        return ', '.join(filter(None, parts))