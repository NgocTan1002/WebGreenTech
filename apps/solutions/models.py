from django.db import models
from django.urls import reverse
from apps.core.models import (
    TimeStampedModel, SEOModel, SlugModel, PublishableModel, SortableModel,
)


class SolutionCategory(TimeStampedModel, SlugModel, SortableModel):
    """Danh mục ngành / lĩnh vực (Nông nghiệp, Nhà máy, Năng lượng...)."""
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon_class  = models.CharField(max_length=100, blank=True, help_text='CSS icon class')
    thumbnail   = models.ImageField(upload_to='solutions/categories/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Solution Category'
        verbose_name_plural = 'Solution Categories'

    def __str__(self):
        return self.name


class Solution(TimeStampedModel, SEOModel, SlugModel, PublishableModel, SortableModel):
    """
    Trang giải pháp đầy đủ.
    Mỗi record = 1 use-case (ví dụ: Giám sát nông nghiệp thông minh).
    """
    # ─── Identity ─────────────────────────────────────────────────────────────
    title             = models.CharField(max_length=300, db_index=True)
    subtitle          = models.CharField(max_length=300, blank=True)
    solution_category = models.ForeignKey(
        SolutionCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='solutions',
    )

    # ─── Media ────────────────────────────────────────────────────────────────
    thumbnail      = models.ImageField(upload_to='solutions/thumbnails/')
    hero_image     = models.ImageField(upload_to='solutions/hero/', blank=True, null=True)
    hero_video_url = models.URLField(blank=True, help_text='URL nhúng YouTube / Vimeo')

    # ─── Nội dung ─────────────────────────────────────────────────────────────
    short_description = models.TextField(max_length=500)
    overview          = models.TextField(help_text='Nội dung HTML đầy đủ (dùng CKEditor)')

    # ─── Pain Points & Benefits (JSON đơn giản) ───────────────────────────────
    pain_points = models.JSONField(
        default=list, blank=True,
        help_text='Ví dụ: [{"title": "Khó giám sát từ xa", "icon": "eye-off"}]',
    )
    benefits = models.JSONField(
        default=list, blank=True,
        help_text='Ví dụ: [{"title": "Tiết kiệm 30% nước", "metric": "30%", "icon": "droplet"}]',
    )

    # ─── Workflow ─────────────────────────────────────────────────────────────
    workflow_title       = models.CharField(max_length=200, blank=True)
    workflow_description = models.TextField(blank=True)

    # ─── Sản phẩm liên quan (M2M qua through model) ───────────────────────────
    products = models.ManyToManyField(
        'products.Product',
        through='SolutionProduct',
        blank=True,
        related_name='solutions',
    )

    # CTA
    cta_title         = models.CharField(max_length=200, blank=True)
    cta_primary_text  = models.CharField(max_length=100, blank=True)
    cta_primary_url   = models.CharField(max_length=200, blank=True)
    cta_secondary_text = models.CharField(max_length=100, blank=True)
    cta_secondary_url  = models.CharField(max_length=200, blank=True)

    # ─── Analytics ────────────────────────────────────────────────────────────
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', '-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['solution_category', 'status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('solutions:detail', kwargs={'slug': self.slug})

    def get_featured_products(self):
        """Trả về các sản phẩm được đánh dấu nổi bật cho trang solution."""
        return self.products.filter(
            status='published',
            solutionproduct__is_featured=True,
        ).order_by('solutionproduct__sort_order')

    def get_all_products(self):
        """Trả về toàn bộ sản phẩm published của solution."""
        return self.products.filter(status='published').order_by('solutionproduct__sort_order')


class SolutionProduct(SortableModel):
    """
    Through model Solution ↔ Product.
    Cho phép sắp xếp và đánh dấu sản phẩm nổi bật theo từng solution.
    """
    solution         = models.ForeignKey(Solution, on_delete=models.CASCADE)
    product          = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    is_featured      = models.BooleanField(default=False,
                                           help_text='Hiển thị nổi bật trên trang solution')
    role_description = models.CharField(max_length=300, blank=True,
                                        help_text='Mô tả vai trò sản phẩm trong giải pháp')

    class Meta:
        unique_together = ('solution', 'product')
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.solution.title} → {self.product.name}'


class ArchitectureBlock(TimeStampedModel, SortableModel):
    """
    Khối sơ đồ kiến trúc hệ thống trong trang solution.
    Mỗi block = 1 ảnh + tiêu đề + mô tả.
    """
    solution    = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='architecture_blocks')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='solutions/architecture/', blank=True, null=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Architecture Block'

    def __str__(self):
        return f'{self.solution.title} — {self.title}'


class WorkflowStep(TimeStampedModel, SortableModel):
    """Các bước quy trình trong trang solution."""
    solution    = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='workflow_steps')
    step_number = models.PositiveSmallIntegerField()
    title       = models.CharField(max_length=200)
    description = models.TextField()
    icon_class  = models.CharField(max_length=100, blank=True, help_text='CSS icon class')
    image       = models.ImageField(upload_to='solutions/workflow/', blank=True, null=True)

    class Meta:
        ordering = ['step_number']
        verbose_name = 'Workflow Step'

    def __str__(self):
        return f'Bước {self.step_number}: {self.title}'


class CustomerCase(TimeStampedModel, SlugModel, PublishableModel, SortableModel):
    """Case study / câu chuyện thành công của khách hàng, gắn với solution."""
    solution          = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='customer_cases')
    company_name      = models.CharField(max_length=200)
    company_logo      = models.ImageField(upload_to='cases/logos/', blank=True, null=True)
    industry          = models.CharField(max_length=100)
    country           = models.CharField(max_length=100, default='Việt Nam')
    challenge         = models.TextField(help_text='Thách thức / vấn đề ban đầu')
    solution_applied  = models.TextField(help_text='Giải pháp đã áp dụng')
    results           = models.JSONField(
        default=list,
        help_text='Ví dụ: [{"metric": "Tiết kiệm điện", "value": "35", "unit": "%"}]',
    )
    testimonial        = models.TextField(blank=True)
    testimonial_author = models.CharField(max_length=200, blank=True)
    testimonial_title  = models.CharField(max_length=200, blank=True,
                                          help_text='Chức danh người trích dẫn')

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Customer Case'
        verbose_name_plural = 'Customer Cases'

    def __str__(self):
        return f'{self.company_name} — {self.solution.title}'