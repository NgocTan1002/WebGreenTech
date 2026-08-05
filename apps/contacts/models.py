from django.db import models
from apps.core.models import TimeStampedModel

class ContactInquiry(TimeStampedModel):
    INQUIRY_GENERAL = "general"
    INQUIRY_TECHNICAL = "technical"
    INQUIRY_SALES = "sales"
    INQUIRY_SUPPORT = "support"
    INQUIRY_PARTNERSHIP = "partnership"
    INQUIRY_TYPE_CHOICES = [
        (INQUIRY_GENERAL, "Tư vấn chung"),
        (INQUIRY_TECHNICAL, "Hỗ trợ kỹ thuật"),
        (INQUIRY_SALES, "Kinh doanh / Báo giá"),
        (INQUIRY_SUPPORT, "Hỗ trợ sau bán hàng"),
        (INQUIRY_PARTNERSHIP, "Hợp tác"),
    ]

    STATUS_NEW = "new"
    STATUS_READ = "read"
    STATUS_REPLIED = "replied"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_NEW, "Mới"),
        (STATUS_READ, "Đã đọc"),
        (STATUS_REPLIED, "Đã trả lời"),
        (STATUS_CLOSED, "Đã đóng"),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default=INQUIRY_GENERAL)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(blank=True)
    source_url = models.URLField(blank=True)
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Yêu cầu liên hệ'
        verbose_name_plural = 'Yêu cầu liên hệ'

    def __str__(self):
        return f'{self.name} - {self.subject}'
    
class DemoRequest(TimeStampedModel):
    STATUS_NEW       = 'new'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW,       'Mới'),
        (STATUS_SCHEDULED, 'Đã lên lịch'),
        (STATUS_COMPLETED, 'Hoàn thành'),
        (STATUS_CANCELLED, 'Đã hủy'),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    solution = models.ForeignKey(
        'solutions.Solution', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='demo_requests')
    
    preferred_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Yêu cầu đăng ký demo'
        verbose_name_plural = 'Yêu cầu đăng ký demo'
    
    def __str__(self):
        return f'Demo: {self.name} ({self.company})'
