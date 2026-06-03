"""
Core abstract base models for IoT Platform.
All domain models inherit from these for consistency.
"""
import uuid
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base with UUID primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Abstract base with SEO fields."""
    meta_title = models.CharField(max_length=70, blank=True, help_text='SEO title (max 70 chars)')
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description (max 160 chars)')
    meta_keywords = models.CharField(max_length=255, blank=True)
    canonical_url = models.URLField(blank=True, help_text='Override canonical URL if needed')
    og_image = models.ImageField(upload_to='seo/og/', blank=True, null=True, help_text='OpenGraph image (1200x630px)')

    class Meta:
        abstract = True

    def get_meta_title(self):
        return self.meta_title or getattr(self, 'name', None) or getattr(self, 'title', '')

    def get_meta_description(self):
        return self.meta_description or getattr(self, 'short_description', '')[:160]


class PublishableModel(models.Model):
    """Abstract base for publishable content."""
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

    def publish(self):
        self.status = self.STATUS_PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at'])

    @property
    def is_published(self):
        return self.status == self.STATUS_PUBLISHED


class SlugModel(models.Model):
    """Abstract base with auto-slug generation."""
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = getattr(self, 'name', None) or getattr(self, 'title', '')
            self.slug = self._generate_unique_slug(slugify(base))
        super().save(*args, **kwargs)

    def _generate_unique_slug(self, slug):
        model_class = self.__class__
        unique_slug = slug
        counter = 1
        while model_class.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f'{slug}-{counter}'
            counter += 1
        return unique_slug


class SortableModel(models.Model):
    """Abstract base with ordering support."""
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['sort_order']