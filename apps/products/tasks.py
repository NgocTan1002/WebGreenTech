from celery import shared_task
from apps.core.db import increment_product_views
 
 
@shared_task(bind=True, max_retries=3)
def increment_product_views_task(self, product_id: int):
    try:
        increment_product_views(product_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)