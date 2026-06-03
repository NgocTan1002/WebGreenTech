from django.db import models
from apps.core.models import TimeStampedModel

class ContactInquiry(TimeStampedModel):
    INQUIRY_GENERAL = "general"
    INQUIRY_TECHNICAL = "technical"
    INQUIRY_SALES = "sales"
    INQUIRY_SUPPORT = "support"
    INQUIRY_PARTNERSHIP = "partnership"
    INQUIRY_TYPE_CHOICES = [
        (INQUIRY_GENERAL, "General Inquiry"),
        (INQUIRY_TECHNICAL, "Technical Support"),
        (INQUIRY_SALES, "Sales / Pricing"),
        (INQUIRY_SUPPORT, "After-Sales Support"),
        (INQUIRY_PARTNERSHIP, "Partnership"),
    ]

    STATUS_NEW = "new"
    STATUS_READ = "read"
    STATUS_REPLIED = "replied"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_READ, "Read"),
        (STATUS_REPLIED, "Replied"),
        (STATUS_CLOSED, "Closed"),
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
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        return f'{self.name} - {self.subject}'
    
class DemoRequest(TimeStampedModel):
    STATUS_NEW       = 'new'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW,       'New'),
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
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
    
    def __str__(self):
        return f'Demo: {self.name} ({self.company})'