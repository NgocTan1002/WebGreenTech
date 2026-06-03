from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_contact_notification(self, inquiry_id: int):
    from apps.contacts.models import ContactInquiry
    try:
        inquiry = ContactInquiry.objects.get(pk=inquiry_id)
        subject = f'[Liên hệ mới] {inquiry.subject} — {inquiry.name}'
        body = (
            f'Người gửi : {inquiry.name}\n'
            f'Email     : {inquiry.email}\n'
            f'Điện thoại: {inquiry.phone or "—"}\n'
            f'Công ty   : {inquiry.company or "—"}\n'
            f'Loại      : {inquiry.get_inquiry_type_display()}\n'
            f'Tiêu đề   : {inquiry.subject}\n\n'
            f'Nội dung:\n{inquiry.message}\n\n'
            f'---\nIP: {inquiry.ip_address} | URL: {inquiry.source_url}'
        )

        recipient = getattr(settings, 'COMPANY_EMAIL', '') or settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@shared_task(bind=True, max_retries=3)
def send_demo_request_notification(self, demo_id: int):
    try:
        from apps.contacts.models import DemoRequest
        demo = DemoRequest.objects.select_related('solution').get(pk=demo_id)

        solution_title = demo.solution.title if demo.solution else '-'
        subject = f'[Demo mới] {demo.name} — {demo.company or demo.email}'
        body = (
            f'Người đăng ký: {demo.name}\n'
            f'Email        : {demo.email}\n'
            f'Điện thoại   : {demo.phone or "—"}\n'
            f'Công ty      : {demo.company or "—"}\n'
            f'Chức danh    : {demo.job_title or "—"}\n'
            f'Giải pháp    : {solution_title}\n'
            f'Ngày mong muốn: {demo.preferred_date or "—"}\n\n'
            f'Ghi chú:\n{demo.message or "—"}'
        )
        
        recipient = getattr(settings, 'COMPANY_EMAIL', '') or settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )

    except Exception as exc:
        raise  self.retry(exc=exc, countdown=60)