from django.contrib import admin
from django import forms
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import (
    Product, ProductImage, ProductSpecification,
    ProductDocument, RelatedProduct,
)


class ProductAdminForm(forms.ModelForm):
    highlights = forms.CharField(
        required=False,
        label='Tính năng nổi bật',
        help_text='Nhập mỗi tính năng trên một dòng.',
        widget=forms.Textarea(attrs={
            'rows': 7,
            'placeholder': (
                'Phạm vi đo: (-20 đến 70) oC; (0 đến 100) %RH.\n'
                'Độ chính xác: ± 2%RH; ± 0,5 oC.\n'
                'Số kênh đo: 10 kênh;'
            ),
        }),
    )

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea(attrs={
                'rows': 7,
                'placeholder': (
                    '- Phạm vi đo: (-20 đến 70) oC; (0 đến 100) %RH.\n'
                    '- Độ chính xác: ± 2%RH; ± 0,5 oC.\n'
                    '- Số kênh đo: 10 kênh;'
                ),
            }),
            'description': CKEditorWidget(config_name='default'),
        }
        help_texts = {
            'short_description': (
                'Có thể nhập mỗi tính năng trên một dòng, bắt đầu bằng dấu "-". '
                'Không cần nhập HTML.'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and isinstance(self.instance.highlights, list):
            self.initial['highlights'] = '\n'.join(str(item) for item in self.instance.highlights)

    def clean_highlights(self):
        value = self.cleaned_data.get('highlights') or ''
        if isinstance(value, list):
            return value
        return [
            line.lstrip('-•').strip()
            for line in value.splitlines()
            if line.lstrip('-•').strip()
        ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image_preview', 'image', 'alt_text', 'is_primary', 'sort_order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Xem trước'


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 3
    fields = ['group', 'key', 'value', 'unit', 'sort_order']


class ProductDocumentInline(admin.TabularInline):
    """
    Tất cả tài liệu (datasheet, manual, certificate...) quản lý tại đây.
    Không cần FileField riêng lẻ trên Product nữa.
    """
    model = ProductDocument
    extra = 1
    fields = ['title', 'doc_type', 'file', 'sort_order']


class RelatedProductInline(admin.TabularInline):
    model = RelatedProduct
    fk_name = 'product'
    extra = 2
    fields = ['related', 'relation_type', 'sort_order']
    autocomplete_fields = ['related']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        'thumbnail_preview', 'name', 'sku',
        'category', 'brand',
        'pricing_type', 'display_price_col',
        'stock_status_badge', 'status',
        'is_featured', 'is_new',
        'view_count', 'created_at',
    ]
    list_display_links = ['thumbnail_preview', 'name']
    list_filter = [
        'status', 'pricing_type', 'stock_status',
        'category', 'brand',
        'is_featured', 'is_new', 'is_bestseller',
    ]
    search_fields = ['name', 'sku', 'part_number', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status', 'is_featured', 'is_new']
    readonly_fields = [
        'thumbnail_preview_large',
        'view_count', 'quote_count',
        'created_at', 'updated_at',
    ]
    autocomplete_fields = ['category', 'brand']
    save_on_top = True
    list_per_page = 50
    date_hierarchy = 'created_at'
    inlines = [
        ProductImageInline,
        ProductSpecificationInline,
        ProductDocumentInline,
        RelatedProductInline,
    ]

    fieldsets = [
        ('Thông tin cơ bản', {
            'fields': [
                'name', 'slug', 'sku', 'part_number',
                'category', 'brand',
            ],
        }),
        ('Ảnh đại diện', {
            'fields': ['thumbnail', 'thumbnail_preview_large'],
        }),
        ('Giá bán', {
            'fields': [
                'pricing_type', 'price', 'sale_price', 'min_order_qty',
            ],
            'description': 'Đơn vị: VND. Để trống nếu pricing_type không phải "Giá cố định".',
        }),
        ('Tồn kho', {
            'fields': ['stock_status', 'stock_quantity'],
        }),
        ('Nội dung', {
            'fields': ['short_description', 'description', 'highlights'],
            'classes': ['wide'],
        }),
        ('Thông số vật lý', {
            'fields': ['weight', 'dim_length', 'dim_width', 'dim_height'],
            'classes': ['collapse'],
            'description': 'Khối lượng (kg) và kích thước (mm). Để trống nếu không có.',
        }),
        ('SEO', {
            'fields': [
                'meta_title', 'meta_description',
                'meta_keywords', 'canonical_url', 'og_image',
            ],
            'classes': ['collapse'],
        }),
        ('Xuất bản', {
            'fields': [
                'status', 'published_at',
                'is_featured', 'is_new', 'is_bestseller',
                'requires_quote', 'sort_order',
            ],
        }),
        ('Thống kê', {
            'fields': ['view_count', 'quote_count', 'created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    actions = [
        'action_publish',
        'action_unpublish',
        'action_mark_featured',
        'action_mark_new',
        'action_clear_featured',
    ]

    # ── Cột hiển thị ──────────────────────────────────────────────────────────

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="48" height="48" '
                'style="object-fit:cover;border-radius:6px;" />',
                obj.thumbnail.url,
            )
        return '—'
    thumbnail_preview.short_description = ''

    def thumbnail_preview_large(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="180" height="180" '
                'style="object-fit:contain;border-radius:8px;'
                'border:1px solid #eee;padding:4px;" />',
                obj.thumbnail.url,
            )
        return 'Chưa có ảnh'
    thumbnail_preview_large.short_description = 'Ảnh hiện tại'

    def display_price_col(self, obj):
        if obj.display_price is not None:
            price_str = f'{int(obj.display_price):,} ₫'
            if obj.discount_percent:
                price_str += (
                    f' <small style="color:#e53e3e;font-weight:600">'
                    f'-{obj.discount_percent}%</small>'
                )
            return format_html(price_str)
        return obj.get_pricing_type_display()  # quote/contact hiển thị label
    display_price_col.short_description = 'Giá'
    display_price_col.admin_order_field = 'price'

    def stock_status_badge(self, obj):
        colors = {
            'in_stock':     ('#276749', '#c6f6d5'),
            'low_stock':    ('#744210', '#fefcbf'),
            'out_of_stock': ('#742a2a', '#fed7d7'),
            'pre_order':    ('#2a4365', '#bee3f8'),
        }
        fg, bg = colors.get(obj.stock_status, ('#555', '#eee'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:10px;font-size:11px;font-weight:600">{}</span>',
            bg, fg, obj.get_stock_status_display(),
        )
    stock_status_badge.short_description = 'Tồn kho'

    # ── Bulk actions ───────────────────────────────────────────────────────────

    @admin.action(description='Xuất bản sản phẩm đã chọn')
    def action_publish(self, request, queryset):
        n = queryset.update(status='published')
        self.message_user(request, f'Đã xuất bản {n} sản phẩm.')

    @admin.action(description='Hủy xuất bản sản phẩm đã chọn')
    def action_unpublish(self, request, queryset):
        n = queryset.update(status='draft')
        self.message_user(request, f'Đã hủy xuất bản {n} sản phẩm.')

    @admin.action(description='Đánh dấu nổi bật')
    def action_mark_featured(self, request, queryset):
        n = queryset.update(is_featured=True)
        self.message_user(request, f'Đã đánh dấu nổi bật {n} sản phẩm.') 

    @admin.action(description='Đánh dấu Mới')
    def action_mark_new(self, request, queryset):
        n = queryset.update(is_new=True)
        self.message_user(request, f'Đã đánh dấu mới {n} sản phẩm.')

    @admin.action(description='Bỏ đánh dấu nổi bật')
    def action_clear_featured(self, request, queryset):
        n = queryset.update(is_featured=False)
        self.message_user(request, f'Đã bỏ đánh dấu nổi bật {n} sản phẩm.')
