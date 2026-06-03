from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Brand

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    # Hiển thị category dạng cây kéo thả
    list_display = [
        "tree_actions",  # Cột chứa icon kéo thả
        "indented_title",  # Tên category có thụt lề theo cấp độ
        "slug",
        "is_active",
        "show_in_nav",
        "sort_order",
        "low_stock_threshold"
    ]
    list_display_links = ["indented_title"]  # Chỉ cho phép click vào tên category để vào edit page
    list_editable = ["is_active", "show_in_nav", "sort_order"]  # Cho phép chỉnh sửa trực tiếp các trường này trong list view
    search_fields = ["name", "slug"]  # Cho phép tìm kiếm theo tên và slug
    prepopulated_fields = {"slug": ("name",)}  # Tự động tạo slug từ name

    fieldsets = [
        (None, {
            "fields": ["name", "slug", "parent", "description", "thumbnail", "icon_class"],
        }),
        ("Cài đặt tồn kho", {
            "fields": ["low_stock_threshold"],
            "description": "Ngưỡng cảnh báo tồn kho thấp cho toàn bộ sản phẩm trong danh mục này",
        }),
        ("SEO", {
            "fields": ["meta_title", "meta_description", "meta_keywords"],
            "classes": ["collapse"],
        }),
        ("Hiển thị", {
            "fields": ["is_active", "show_in_nav", "sort_order"],
        }),
    ]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        "logo_preview", "name", "slug", "country",
        "is_active", "is_featured", "sort_order",
    ]
    list_display_links = ["logo_preview", "name"]
    list_editable = ["is_active", "is_featured", "sort_order"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["logo_preview"]
 
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="40" height="40" '
                'style="object-fit:contain;border-radius:4px;" />',
                obj.logo.url,
            )
        return "—"
    logo_preview.short_description = ""