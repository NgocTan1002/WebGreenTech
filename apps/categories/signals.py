from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Brand


HOME_PAGE_CACHE_KEY = "home_page_context"
GLOBAL_CONTEXT_CACHE_KEY = "global_context_data"


def clear_home_page_cache():
    cache.delete(HOME_PAGE_CACHE_KEY)
    cache.delete(GLOBAL_CONTEXT_CACHE_KEY)


@receiver(post_save, sender=Brand)
def clear_home_cache_on_brand_save(sender, instance, **kwargs):
    clear_home_page_cache()


@receiver(post_delete, sender=Brand)
def clear_home_cache_on_brand_delete(sender, instance, **kwargs):
    clear_home_page_cache()
