"""
Django base settings for ProjectQ.
Tất cả secrets được đọc từ .env qua python-decouple.
Không hardcode bất kỳ giá trị nhạy cảm nào ở đây.
"""

from pathlib import Path
from decouple import config, Csv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /projectq root


# ---------------------------------------------------------------------------
# Security — tất cả đọc từ .env
# ---------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())


# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "apps.customers",

    "mptt",
    "apps.core.taggit_config.VietnameseTaggitAppConfig",
    "imagekit",
    "ckeditor",

    "apps.core",
    "apps.categories",
    "apps.dashboard",
    "apps.products",
    "apps.solutions",
    "apps.cart",
    "apps.orders",
    "apps.contacts",
    "apps.blog",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    'django.contrib.humanize',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Replaces the old `company` processor.
                # Injects: COMPANY_*, SITE_URL, GA_TRACKING_ID,
                # nav_solutions, solution_categories, nav_categories.
                "apps.core.context_processors.global_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE":   config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME":     config("DB_NAME",   default="projectq_db"),
        "USER":     config("DB_USER",   default="postgres"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST":     config("DB_HOST",   default="localhost"),
        "PORT":     config("DB_PORT",   default="5432"),
    }
}

AUTH_USER_MODEL = 'customers.Customer'
LOGIN_URL = 'customers:login'
LOGIN_REDIRECT_URL = 'customers:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# ---------------------------------------------------------------------------
# Cache — Redis qua django-redis
# ---------------------------------------------------------------------------
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
# Khi cài django-redis, thay bằng:
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,
#         "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
#     }
# }


# ---------------------------------------------------------------------------
# Celery
# ---------------------------------------------------------------------------
CELERY_BROKER_URL        = config("CELERY_BROKER_URL",     default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND    = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/1")
CELERY_ACCEPT_CONTENT    = ["json"]
CELERY_TASK_SERIALIZER   = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE          = "Asia/Ho_Chi_Minh"


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_BACKEND       = config("EMAIL_BACKEND",      default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST          = config("EMAIL_HOST",          default="smtp.gmail.com")
EMAIL_PORT          = config("EMAIL_PORT",          default=587, cast=int)
EMAIL_USE_TLS       = config("EMAIL_USE_TLS",       default=True, cast=bool)
EMAIL_HOST_USER     = config("EMAIL_HOST_USER",     default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL  = config("DEFAULT_FROM_EMAIL",  default="noreply@projectq.vn")


# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "vi"
TIME_ZONE     = "Asia/Ho_Chi_Minh"
USE_I18N      = True
USE_TZ        = True


# ---------------------------------------------------------------------------
# Static & Media files
# ---------------------------------------------------------------------------
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------------
# CKEditor
# ---------------------------------------------------------------------------
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "ProductContent",
        "toolbar_ProductContent": [
            ["Format", "Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList", "Outdent", "Indent"],
            ["Link", "Unlink", "Table"],
            ["RemoveFormat", "Source"],
        ],
        "format_tags": "p;h2;h3;h4",
        "height": 360,
        "width": "100%",
        "removePlugins": "elementspath",
        "resize_enabled": True,
        "extraAllowedContent": "h2 h3 h4 p ul ol li strong em u table thead tbody tr th td a[href,target,rel]",
    }
}


# ---------------------------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# Site & Company info
# Đọc từ .env; dùng trong global_context processor và JSON-LD schema.
# ---------------------------------------------------------------------------
SITE_URL        = config("SITE_URL",        default="http://localhost:8000")
COMPANY_NAME    = config("COMPANY_NAME",    default="IoTech")
COMPANY_ADDRESS = config("COMPANY_ADDRESS", default="")
COMPANY_PHONE   = config("COMPANY_PHONE",   default="")
COMPANY_EMAIL   = config("COMPANY_EMAIL",   default="")
MESSENGER_URL   = config(
    "MESSENGER_URL",
    default="https://m.me/1165618003296928",
)

# ---------------------------------------------------------------------------
# Analytics (optional)
# ---------------------------------------------------------------------------
GA_TRACKING_ID = config("GA_TRACKING_ID", default="")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # ── Project middleware ─────────────────────────────────────────────────
    "apps.core.middleware.SEOMiddleware",
    "apps.core.middleware.CartMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsPagination',
    'PAGE_SIZE': 24,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
