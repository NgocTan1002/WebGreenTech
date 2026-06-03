from celery import shared_task
from apps.core.db import increment_post_views
 
 
@shared_task(bind=True, max_retries=3)
def increment_post_views_task(self, post_id: int):
    try:
        increment_post_views(post_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)