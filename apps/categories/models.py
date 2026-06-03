from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import TimeStampedModel, SEOModel, SlugModel, SortableModel


class Category(MPTTModel, TimeStampedModel, SEOModel, SlugModel, SortableModel):
    name = models.CharField(max_length=200, db_index=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='Danh mục cha'
    )
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='categories/thumbnails/', blank=True, null=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text='CSS icon class (e.g. heroicon name)')
    is_active = models.BooleanField(default=True, db_index=True)
    show_in_nav = models.BooleanField(default=True, db_index=True)

    low_stock_threshold = models.PositiveIntegerField(
    default=10,
    help_text="Tồn kho thấp hơn giá trị này sẽ hiển thị trạng thái 'Sắp hết hàng'"
    )

    class MPTTMeta:
        order_insertion_by = ['sort_order', 'name']

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        # Đếm số lượng sản phẩm trong danh mục này và tất cả sản phẩm con của nó
        from apps.products.models import Product
        category_ids = self.get_descendants(include_self=True).values_list('id', flat=True)
        return Product.objects.filter(category_id__in=category_ids, status='published').count()

    def get_ancestors_breadcrumb(self):
        return list(self.get_ancestors(include_self=True))


class Brand(TimeStampedModel, SlugModel, SortableModel):
    name = models.CharField(max_length=200, verbose_name='Tên')
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True, verbose_name='Logo')
    website = models.URLField(blank=True, verbose_name='Website')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    country = models.CharField(max_length=100, blank=True, verbose_name='Quốc gia')
    is_active = models.BooleanField(default=True, verbose_name='Kích hoạt')
    is_featured = models.BooleanField(default=False, verbose_name='Nổi bật')

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Thương hiệu'
        verbose_name_plural = 'Thương hiệu'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:brand', kwargs={'slug': self.slug})