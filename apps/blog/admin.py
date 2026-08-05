from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import BlogCategory, Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 5}),
            'content': CKEditorWidget(config_name='default'),
        }


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'post_type', 'category', 'author', 'status', 'is_featured', 'view_count', 'published_at']
    list_filter = ['status', 'post_type', 'category']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'published_at'
 
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'post_type', 'category', 'author']}),
        ('Hình ảnh', {'fields': ['thumbnail']}),
        ('Nội dung', {'fields': ['short_description', 'content', 'read_time', 'tags'], 'classes': ['wide']}),
        ('Liên kết', {'fields': ['related_products', 'related_solutions']}),
        ('SEO', {'fields': ['meta_title', 'meta_description'], 'classes': ['collapse']}),
        ('Xuất bản', {'fields': ['status', 'published_at', 'is_featured', 'sort_order']}),
    ]
