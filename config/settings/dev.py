"""
Development settings — ghi đè base.py.
File này an toàn để commit, không chứa secrets.
"""

from .base import *  # noqa: F401, F403
from decouple import config

DEBUG = True

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Django Debug Toolbar (cài ở phase sau)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
# INTERNAL_IPS = ["127.0.0.1"]

# Email đọc từ .env (base.py) nên không hardcode console ở đây nữa
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# # Ép Celery chạy task đồng bộ, không cần đẩy vào Broker (Redis)
CELERY_TASK_ALWAYS_EAGER = True

CSRF_TRUSTED_ORIGINS = [
    "https://www.higtc.com",
    "https://higtc.com",
]