from decimal import Decimal

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def vnd(value):
    """
    Format a number as VND with dot thousand separators.
    """
    if value is None or value == "":
        return "Liên hệ"

    try:
        amount = int(Decimal(str(value)))
    except (ValueError, TypeError):
        return "Liên hệ"

    if amount == 0:
        return "Miễn phí"

    formatted = f"{amount:,}".replace(",", ".")
    return f"{formatted} ₫"


@register.filter
def media_url(value):
    """
    Convert a relative media path into a full media URL.

    Stored functions return ImageField values as plain strings such as
    "blog/thumbnails/image.jpg"; templates need "/media/..." to load them.
    """
    if not value:
        return ""

    value = str(value)
    if value.startswith(("http://", "https://", "/media/", "/static/")):
        return value

    return f"{settings.MEDIA_URL}{value}"
