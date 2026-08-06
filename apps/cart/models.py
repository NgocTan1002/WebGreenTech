import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel  # ← fix: import đúng nguồn
from apps.products.models import Product


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='carts',
    )
    is_active = models.BooleanField(default=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'
        indexes = [
            models.Index(fields=['session_key', 'is_active']),
            models.Index(fields=['customer', 'is_active']),
        ]

    def __str__(self):
        return f'Cart {self.id}'

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        subtotal = Decimal('0')
        for item in self.items.all():
            line_total = item.line_total
            if line_total is not None:
                subtotal += line_total
        return subtotal

    @property
    def has_pending_quote(self):
        return any(item.price_pending for item in self.items.all())

    def merge_with(self, other_cart):
        """Gộp giỏ hàng session vào giỏ hàng tài khoản khi đăng nhập."""
        for item in other_cart.items.all():
            existing = self.items.filter(product=item.product).first()
            if existing:
                existing.quantity += item.quantity
                existing.save()
            else:
                item.cart = self
                item.save()
        other_cart.is_active = False
        other_cart.save()


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    pricing_type = models.CharField(
        max_length=20,
        choices=Product.PRICING_CHOICES,
        default=Product.PRICING_FIXED,
        verbose_name='Loại giá tại thời điểm thêm',
    )
    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name='Đơn giá tạm tính',
    )

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Sản phẩm trong giỏ hàng'
        verbose_name_plural = 'Sản phẩm trong giỏ hàng'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def line_total(self):
        if self.price_pending:
            return None
        return Decimal(str(self.unit_price)) * self.quantity

    @property
    def price_pending(self):
        return self.pricing_type != Product.PRICING_FIXED or self.unit_price is None

    def save(self, *args, **kwargs):
        if self.product_id:
            self.pricing_type = (
                Product.PRICING_QUOTE
                if self.product.requires_quote
                else self.product.pricing_type
            )
            if self.pricing_type != Product.PRICING_FIXED:
                self.unit_price = None
            elif self.unit_price is None:
                self.unit_price = self.product.display_price
        super().save(*args, **kwargs)
