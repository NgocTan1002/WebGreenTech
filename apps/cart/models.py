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
        return sum(item.line_total for item in self.items.all())

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
    unit_price = models.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def line_total(self):
        return Decimal(str(self.unit_price)) * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price or 0
        super().save(*args, **kwargs)