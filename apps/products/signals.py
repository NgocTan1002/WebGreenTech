from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def sync_stock_status(sender, instance, **kwargs):
    threshold = instance.category.low_stock_threshold

    if instance.stock_quantity <= 0:
        new_status = Product.STOCK_OUT
    elif instance.stock_quantity <= threshold:
        new_status = Product.STOCK_LOW
    else:
        new_status = Product.STOCK_IN

    if instance.stock_status != new_status:
        Product.objects.filter(pk=instance.pk).update(
            stock_status=new_status
        )
        instance.stock_status = new_status