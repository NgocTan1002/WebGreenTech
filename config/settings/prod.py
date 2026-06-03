"""
Production settings — ghi đè base.py.
Tất cả secrets PHẢI có trong .env trên server.
"""

from .base import *  # noqa: F401, F403
from decouple import config, Csv

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# ---------------------------------------------------------------------------
# HTTPS / Security headers
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT              = True
SECURE_HSTS_SECONDS              = 31_536_000   # 1 năm
SECURE_HSTS_INCLUDE_SUBDOMAINS   = True
SECURE_HSTS_PRELOAD              = True
SECURE_CONTENT_TYPE_NOSNIFF      = True
SESSION_COOKIE_SECURE            = True
CSRF_COOKIE_SECURE               = True

# ---------------------------------------------------------------------------
# Email — SMTP thật trong prod
# ---------------------------------------------------------------------------
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# ---------------------------------------------------------------------------
# Logging — structured JSON (cài ở phase sau + Sentry)
# ---------------------------------------------------------------------------
SENTRY_DSN = config("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.2,
        send_default_pii=False,
    )

# ---------------------------------------------------------------------------
# Static files — Whitenoise (cài ở phase sau)
# ---------------------------------------------------------------------------
# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------------
# S3 file storage (cài ở phase sau)
# ---------------------------------------------------------------------------
USE_S3 = config("USE_S3", default=False, cast=bool)
if USE_S3:
    AWS_ACCESS_KEY_ID        = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY    = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME  = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME       = config("AWS_S3_REGION_NAME", default="ap-southeast-1")
    AWS_S3_CUSTOM_DOMAIN     = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    DEFAULT_FILE_STORAGE     = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE      = "storages.backends.s3boto3.S3StaticStorage"
    MEDIA_URL                = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    STATIC_URL               = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"