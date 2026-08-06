from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id: str):
    try:
        from apps.orders.models import Order
        order = Order.objects.prefetch_related('items__product').get(id=order_id)
        is_quote_request = (
            order.order_type == Order.ORDER_TYPE_QUOTE
            or order.has_pending_quote
        )

        ctx = {
            'order':        order,
            'items':        order.items.all(),
            'is_quote_request': is_quote_request,
            'SITE_URL':     settings.SITE_URL,
            'COMPANY_NAME': settings.COMPANY_NAME,
            'COMPANY_EMAIL': settings.COMPANY_EMAIL,
            'COMPANY_PHONE': settings.COMPANY_PHONE,
            'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        }
        html_body = render_to_string('emails/order_confirmation.html', ctx)
        text_body = render_to_string('emails/order_confirmation.txt', ctx)

        msg = EmailMultiAlternatives(
            subject=(
                f'Đã tiếp nhận yêu cầu báo giá #{order.order_number} | {settings.COMPANY_NAME}'
                if is_quote_request
                else f'Xác nhận đơn hàng #{order.order_number} | {settings.COMPANY_NAME}'
            ),
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        # Admin notification
        recipient = getattr(settings, 'COMPANY_EMAIL', '') or settings.DEFAULT_FROM_EMAIL
        request_label = 'Yêu cầu báo giá mới' if is_quote_request else 'Đơn hàng mới'
        total_label = 'Chờ báo giá' if is_quote_request else f'{int(order.total):,} ₫'
        send_mail(
            subject=f'[{request_label}] #{order.order_number} — {order.company_name or order.email}',
            message=(
                f'{request_label} vừa được tạo.\n'
                f'Mã đơn : #{order.order_number}\n'
                f'Khách  : {order.email}\n'
                f'Công ty: {order.company_name or "—"}\n'
                f'Tổng   : {total_label}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as exc:
        logger.error('send_order_confirmation_email failed for order_id=%s: %s', order_id, exc)
        raise self.retry(exc=exc, countdown=60)
    
@shared_task(bind=True, max_retries=3)
def send_quote_notification_email(self, quote_id: int):
    try:
        from apps.orders.models import QuoteRequest
        quote = QuoteRequest.objects.select_related('solution').get(pk=quote_id)

        ctx = {
            'quote':        quote,
            'SITE_URL':     settings.SITE_URL,
            'COMPANY_NAME': settings.COMPANY_NAME,
        }
        html_body = render_to_string('emails/quote_received.html', ctx)
        text_body = render_to_string('emails/quote_received.txt', ctx)

        msg = EmailMultiAlternatives(
            subject=f'[Báo giá] {quote.reference} đã được tiếp nhận | {settings.COMPANY_NAME}',
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[quote.email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        recipient = getattr(settings, 'COMPANY_EMAIL', '') or settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject=f'[RFQ mới] {quote.reference} — {quote.company or quote.name}',
            message=(
                f'Yêu cầu báo giá mới.\n'
                f'Mã tham chiếu: {quote.reference}\n'
                f'Người gửi    : {quote.name}\n'
                f'Email        : {quote.email}\n'
                f'Công ty      : {quote.company or "—"}\n'
                f'Giải pháp   : {quote.solution.title if quote.solution else "—"}\n'
                f'Ứng dụng     : {quote.application or "—"}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

    except Exception as exc:
        logger.error('send_quote_notification_email failed for quote_id=%s: %s', quote_id, exc)
        raise self.retry(exc=exc, countdown=60)
