from celery import shared_task
from apps.core.db import increment_solution_views
 
 
@shared_task(bind=True, max_retries=3)
def increment_solution_views_task(self, solution_id: int):
    try:
        increment_solution_views(solution_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)