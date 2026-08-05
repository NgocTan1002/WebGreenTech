from django.db import models
from django.urls import reverse
from django.conf import settings
from apps.core.models import TimeStampedModel, SEOModel, SlugModel, PublishableModel, SortableModel


class BlogCategory(TimeStampedModel, SlugModel, SortableModel):
    """Danh mục bài viết (Automation, IoT, Tutorial, Tin tức...)."""
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Danh mục bài viết'
        verbose_name_plural = 'Danh mục bài viết'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'category_slug': self.slug})


class Post(TimeStampedModel, SEOModel, SlugModel, PublishableModel, SortableModel):
    """
    Bài viết kỹ thuật, tin tức, case study, hướng dẫn.
    related_products / related_solutions hỗ trợ cross-linking SEO.
    """
    POST_TYPE_ARTICLE   = 'article'
    POST_TYPE_NEWS      = 'news'
    POST_TYPE_CASE      = 'case_study'
    POST_TYPE_GUIDE     = 'guide'
    POST_TYPE_CHOICES   = [
        (POST_TYPE_ARTICLE, 'Bài viết kỹ thuật'),
        (POST_TYPE_NEWS,    'Tin tức'),
        (POST_TYPE_CASE,    'Case Study'),
        (POST_TYPE_GUIDE,   'Hướng dẫn'),
    ]

    title             = models.CharField(max_length=300, db_index=True)
    post_type         = models.CharField(max_length=20, choices=POST_TYPE_CHOICES,
                                         default=POST_TYPE_ARTICLE)
    category          = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='posts',
    )
    author            = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='posts',
    )
    thumbnail         = models.ImageField(upload_to='blog/thumbnails/')
    short_description = models.TextField(max_length=500)
    content           = models.TextField(help_text='Nội dung HTML đầy đủ (dùng CKEditor)')
    read_time         = models.PositiveIntegerField(default=5,
                                                    help_text='Thời gian đọc ước tính (phút)')

    # ─── Quan hệ cross-link ────────────────────────────────────────────────────
    related_products  = models.ManyToManyField('products.Product', blank=True,
                                               related_name='blog_posts')
    related_solutions = models.ManyToManyField('solutions.Solution', blank=True,
                                               related_name='blog_posts')

    # ─── Tags (đơn giản, phân cách dấu phẩy) ─────────────────────────────────
    tags = models.CharField(max_length=500, blank=True,
                            help_text='Tags phân cách bởi dấu phẩy. Ví dụ: PLC, IoT, Cảm biến')

    # ─── Analytics ────────────────────────────────────────────────────────────
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        indexes = [
            models.Index(fields=['status', 'post_type']),
            models.Index(fields=['status', 'category']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_tags_list(self) -> list[str]:
        """Trả về danh sách tags đã loại bỏ khoảng trắng thừa."""
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []
