from django.contrib import admin
from django import forms
from django.core.cache import cache
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import Solution, SolutionCategory, SolutionProduct, ArchitectureBlock, WorkflowStep, CustomerCase


class SolutionAdminForm(forms.ModelForm):
    pain_points = forms.CharField(
        required=False,
        label='Vấn đề khách hàng',
        help_text='Mỗi dòng: Tiêu đề | Mô tả | icon. Ví dụ: Khó giám sát từ xa | Không có dữ liệu realtime | eye-off',
        widget=forms.Textarea(attrs={'rows': 6}),
    )
    benefits = forms.CharField(
        required=False,
        label='Lợi ích',
        help_text='Mỗi dòng: Tiêu đề | Metric | Mô tả | icon. Ví dụ: Giảm chi phí vận hành | 30% | Tối ưu điện nước | trending-down',
        widget=forms.Textarea(attrs={'rows': 6}),
    )

    class Meta:
        model = Solution
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 5}),
            'overview': CKEditorWidget(config_name='default'),
            'workflow_description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            if isinstance(self.instance.pain_points, list):
                self.initial['pain_points'] = '\n'.join(
                    ' | '.join(
                        str(item.get(key, ''))
                        for key in ('title', 'description', 'icon')
                        if item.get(key, '') != ''
                    )
                    for item in self.instance.pain_points
                    if isinstance(item, dict)
                )
            if isinstance(self.instance.benefits, list):
                self.initial['benefits'] = '\n'.join(
                    ' | '.join(
                        str(item.get(key, ''))
                        for key in ('title', 'metric', 'description', 'icon')
                        if item.get(key, '') != ''
                    )
                    for item in self.instance.benefits
                    if isinstance(item, dict)
                )

    def clean_pain_points(self):
        return self._parse_rows(
            self.cleaned_data.get('pain_points') or '',
            ('title', 'description', 'icon'),
        )

    def clean_benefits(self):
        return self._parse_rows(
            self.cleaned_data.get('benefits') or '',
            ('title', 'metric', 'description', 'icon'),
        )

    @staticmethod
    def _parse_rows(value, keys):
        rows = []
        for line in value.splitlines():
            parts = [part.strip() for part in line.lstrip('-•').split('|')]
            if not any(parts):
                continue
            item = {
                key: parts[index]
                for index, key in enumerate(keys)
                if index < len(parts) and parts[index]
            }
            if item:
                rows.append(item)
        return rows


class CustomerCaseAdminForm(forms.ModelForm):
    results = forms.CharField(
        required=False,
        label='Kết quả đạt được',
        help_text='Mỗi dòng: Chỉ số | Giá trị | Đơn vị. Ví dụ: Tiết kiệm điện | 35 | %',
        widget=forms.Textarea(attrs={'rows': 5}),
    )

    class Meta:
        model = CustomerCase
        fields = '__all__'
        widgets = {
            'challenge': forms.Textarea(attrs={'rows': 5}),
            'solution_applied': forms.Textarea(attrs={'rows': 5}),
            'testimonial': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and isinstance(self.instance.results, list):
            self.initial['results'] = '\n'.join(
                ' | '.join(
                    str(item.get(key, ''))
                    for key in ('metric', 'value', 'unit')
                    if item.get(key, '') != ''
                )
                for item in self.instance.results
                if isinstance(item, dict)
            )

    def clean_results(self):
        rows = []
        for line in (self.cleaned_data.get('results') or '').splitlines():
            parts = [part.strip() for part in line.lstrip('-•').split('|')]
            if not any(parts):
                continue
            item = {}
            if len(parts) > 0 and parts[0]:
                item['metric'] = parts[0]
            if len(parts) > 1 and parts[1]:
                item['value'] = parts[1]
            if len(parts) > 2 and parts[2]:
                item['unit'] = parts[2]
            if item:
                rows.append(item)
        return rows


class SolutionProductInline(admin.TabularInline):
    model = SolutionProduct
    extra = 2
    autocomplete_fields = ['product']
    fields = ['product', 'is_featured', 'role_description', 'sort_order']

class ArchitectureBlockInline(admin.StackedInline):
    model = ArchitectureBlock
    extra = 1
    fields = ['title', 'description', 'image', 'sort_order']
    verbose_name = "Khối kiến trúc"
    verbose_name_plural = "Các khối kiến trúc"

class WorkflowStepInline(admin.TabularInline):
    model = WorkflowStep
    extra = 3
    fields = ['step_number', 'title', 'description', 'icon_class', 'image']
    verbose_name = "Bước quy trình"
    verbose_name_plural = "Các bước quy trình"

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    form = SolutionAdminForm
    list_display = ['thumbnail_preview', 
                    'title',
                    'solution_category',
                    'status',
                    'is_featured',
                    'view_count'
                    ]
    list_display_links = ['thumbnail_preview', 'title']
    list_filter = ['status', 'solution_category', 'is_featured']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    list_select_related = ['solution_category']
    save_on_top = True

    inlines = [SolutionProductInline, ArchitectureBlockInline, WorkflowStepInline]

    fieldsets = [
        ('Thông tin cơ bản', {
            'fields': ['title', 'subtitle', 'slug', 'solution_category']
        }),

        ('Hình ảnh & Media', {
            'fields': ['thumbnail', 'hero_image', 'hero_video_url']
        }),

        ('Nội dung chính', {
            'fields': ['short_description', 'overview'],
            'classes': ['wide']
        }),

        ('Triển khai thực tế', {
            'fields': ['deployment_site', 'deployment_location', 'deployed_at'],
            'description': 'Không bắt buộc. Chỉ hiển thị trên trang khi có ít nhất một thông tin.',
        }),

        ('Vấn đề khách hàng', {
            'fields': ['pain_points'],
            'classes': ['collapse']
        }),

        ('Lợi ích', {
            'fields': ['benefits'],
            'classes': ['collapse']
        }),

        ('Quy trình hoạt động', {
            'fields': ['workflow_title', 'workflow_description']
        }),

        ('Kêu gọi hành động (CTA)', {
            'fields': [
                'cta_title',
                'cta_primary_text', 'cta_primary_url',
                'cta_secondary_text', 'cta_secondary_url'
            ]
        }),

        ('Xuất bản', {
            'fields': ['status', 'published_at', 'is_featured', 'sort_order']
        }),
    ]

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;" />', obj.thumbnail.url)
        return '-'
    thumbnail_preview.short_description = ''

    def save_model(self, request, obj, form, change):
        old_slug = None
        if change and obj.pk:
            old_slug = Solution.objects.filter(pk=obj.pk).values_list('slug', flat=True).first()

        super().save_model(request, obj, form, change)

        cache.delete(f'solution_detail_{obj.slug}')
        if old_slug and old_slug != obj.slug:
            cache.delete(f'solution_detail_{old_slug}')

    def delete_model(self, request, obj):
        cache.delete(f'solution_detail_{obj.slug}')
        super().delete_model(request, obj)

@admin.register(SolutionCategory)
class SolutionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'sort_order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'sort_order']
 
 
@admin.register(CustomerCase)
class CustomerCaseAdmin(admin.ModelAdmin):
    form = CustomerCaseAdminForm
    list_display = ['company_name', 'solution', 'industry', 'country', 'status']
    list_filter = ['status', 'industry']
    prepopulated_fields = {'slug': ('company_name',)}
