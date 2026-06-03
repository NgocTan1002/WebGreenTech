import random
import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.products.models import Product


class Order(TimeStampedModel):
    """
    Đơn hàng — hỗ trợ cả Purchase Order (PO) và Quotation Request (QT).
    B2B: không có shipping_cost / tax / discount tại tầng model,
    những khoản đó được thương lượng riêng qua QuoteRequest.
    """
    ORDER_TYPE_PURCHASE = 'purchase'
    ORDER_TYPE_QUOTE    = 'quote'
    ORDER_TYPE_CHOICES  = [
        (ORDER_TYPE_PURCHASE, 'Đơn mua hàng'),
        (ORDER_TYPE_QUOTE,    'Yêu cầu báo giá'),
    ]

    STATUS_PENDING    = 'pending'
    STATUS_CONFIRMED  = 'confirmed'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED    = 'shipped'
    STATUS_DELIVERED  = 'delivered'
    STATUS_CANCELLED  = 'cancelled'
    STATUS_REFUNDED   = 'refunded'
    STATUS_CHOICES    = [
        (STATUS_PENDING,    'Chờ xử lý'),
        (STATUS_CONFIRMED,  'Đã xác nhận'),
        (STATUS_PROCESSING, 'Đang xử lý'),
        (STATUS_SHIPPED,    'Đã giao vận'),
        (STATUS_DELIVERED,  'Đã giao hàng'),
        (STATUS_CANCELLED,  'Đã huỷ'),
        (STATUS_REFUNDED,   'Đã hoàn tiền'),
    ]

    # ─── Identity ─────────────────────────────────────────────────────────────
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=30, unique=True, db_index=True)
    order_type   = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default=ORDER_TYPE_PURCHASE)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)

    # ─── Khách hàng ───────────────────────────────────────────────────────────
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders',
    )
    # Snapshot thông tin liên hệ (hỗ trợ cả guest checkout)
    email        = models.EmailField(db_index=True)
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    phone        = models.CharField(max_length=20, blank=True)

    # ─── Địa chỉ (JSON snapshot tại thời điểm đặt hàng) ──────────────────────
    shipping_address = models.JSONField(default=dict)
    billing_address  = models.JSONField(default=dict)

    # ─── Tài chính ────────────────────────────────────────────────────────────
    subtotal = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    total    = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    # ─── Ghi chú ──────────────────────────────────────────────────────────────
    customer_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    po_number      = models.CharField(max_length=100, blank=True,
                                      help_text='Mã PO của khách hàng (nếu có)')

    # ─── Vận chuyển (dùng sau) ────────────────────────────────────────────────
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at      = models.DateTimeField(null=True, blank=True)
    delivered_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['email']),
            models.Index(fields=['order_number']),
        ]

    def __str__(self):
        return f'Order {self.order_number}'

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'order_number': self.order_number})

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def _generate_order_number(self):
        prefix = 'QT' if self.order_type == self.ORDER_TYPE_QUOTE else 'PO'
        return f"{prefix}-{timezone.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"

    def calculate_totals(self):
        """Tính lại subtotal và total từ các OrderItem."""
        self.subtotal = sum(item.line_total for item in self.items.all())
        self.total    = self.subtotal
        self.save(update_fields=['subtotal', 'total'])


class OrderItem(models.Model):
    """
    Dòng sản phẩm trong đơn hàng.
    Lưu snapshot tên + SKU tại thời điểm đặt hàng để bảo toàn lịch sử.
    """
    order        = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')

    # Snapshot — giữ nguyên dù product sau này bị đổi tên hoặc xóa
    product_name = models.CharField(max_length=255)
    product_sku  = models.CharField(max_length=100)
    quantity     = models.PositiveIntegerField()
    unit_price   = models.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        verbose_name = 'Dòng đơn hàng'
        verbose_name_plural = 'Dòng đơn hàng'

    def __str__(self):
        return f'{self.quantity} × {self.product_sku}'

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class QuoteRequest(TimeStampedModel):
    """
    Yêu cầu báo giá (RFQ) — luồng chính của B2B platform.
    Workflow: new → in_review → quoted → accepted / declined
    """
    STATUS_NEW       = 'new'
    STATUS_IN_REVIEW = 'in_review'
    STATUS_QUOTED    = 'quoted'
    STATUS_ACCEPTED  = 'accepted'
    STATUS_DECLINED  = 'declined'
    STATUS_CHOICES   = [
        (STATUS_NEW,       'Mới'),
        (STATUS_IN_REVIEW, 'Đang xem xét'),
        (STATUS_QUOTED,    'Đã báo giá'),
        (STATUS_ACCEPTED,  'Đã chấp nhận'),
        (STATUS_DECLINED,  'Từ chối'),
    ]

    # ─── Identity ─────────────────────────────────────────────────────────────
    reference = models.CharField(max_length=30, unique=True)
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True)

    # ─── Thông tin liên hệ ────────────────────────────────────────────────────
    name    = models.CharField(max_length=100)
    email   = models.EmailField(db_index=True)
    phone   = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)

    # ─── Chi tiết yêu cầu ─────────────────────────────────────────────────────
    message     = models.TextField()
    products    = models.ManyToManyField(Product, through='QuoteRequestItem', blank=True)
    solution    = models.ForeignKey(
        'solutions.Solution',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='quote_requests',
    )
    application = models.CharField(max_length=200, blank=True,
                                   help_text='Ứng dụng / ngành hàng cụ thể')

    # ─── Xử lý nội bộ ─────────────────────────────────────────────────────────
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_quotes',
        limit_choices_to={'is_staff': True},
    )
    internal_notes    = models.TextField(blank=True)
    converted_to_order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='from_quote',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Yêu cầu báo giá'
        verbose_name_plural = 'Yêu cầu báo giá'

    def __str__(self):
        return f'RFQ {self.reference} — {self.company or self.name}'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = (
                f'RFQ-{timezone.now().strftime("%Y%m")}-{random.randint(10000, 99999)}'
            )
        super().save(*args, **kwargs)


class QuoteRequestItem(models.Model):
    """Through model cho QuoteRequest ↔ Product."""
    quote    = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    # Snapshot
    product_name = models.CharField(max_length=255)
    product_sku  = models.CharField(max_length=100)
    quantity     = models.PositiveIntegerField(default=1)
    notes        = models.TextField(blank=True)

    class Meta:
        unique_together = ('quote', 'product')
        verbose_name = 'Dòng báo giá'
        verbose_name_plural = 'Dòng báo giá'

    def __str__(self):
        return f'{self.quantity} × {self.product_sku}'

    def save(self, *args, **kwargs):
        if self.product and not self.product_name:
            self.product_name = self.product.name
            self.product_sku  = self.product.sku
        super().save(*args, **kwargs)