from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from apps.core.db import get_posts, increment_post_views
from apps.blog.models import Post, BlogCategory


def _get_active_categories():
    """
    TODO: Thêm fn_get_blog_categories() vào db.py + DB để dùng stored function.
    Hiện tại dùng ORM.
    """
    return BlogCategory.objects.filter(is_active=True).order_by('sort_order', 'name')


def _get_post_detail(slug: str) -> dict | None:
    """
    TODO: Thêm fn_get_post_detail(slug) vào db.py + DB.
    Function nên trả về đủ: id, title, content, thumbnail, author_name,
    published_at, read_time, tags, category_name, category_slug, post_type.
    Hiện tại dùng ORM.
    """
    try:
        return Post.objects.select_related('category', 'author').get(
            slug=slug, status='published'
        )
    except Post.DoesNotExist:
        return None


def _paginate(rows: list, page: int, per_page: int = 12):
    """Paginate một list thông thường (kết quả từ db.py)."""
    paginator = Paginator(rows, per_page)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


class PostListView(TemplateView):
    template_name = 'blog/list.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page     = self.request.GET.get('page', 1)
        query    = self.request.GET.get('q', '').strip()
        post_type = self.request.GET.get('type', None)

        # Normalize empty strings
        query     = query or None
        post_type = post_type or None

        rows, total = get_posts(
            post_type=post_type,
            search=query,
            limit=self.paginate_by,
            offset=(int(page) - 1) * self.paginate_by if str(page).isdigit() else 0,
        )

        # db.py trả về list — paginate thủ công với total từ DB
        # Dùng Paginator dummy để giữ interface nhất quán với template
        paginator = Paginator(range(total), self.paginate_by)  # dummy range
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        context.update({
            'posts': rows,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
            'total_count': total,
            'categories': _get_active_categories(),
            'current_type': post_type,
            'query': query or '',
            'POST_TYPES': Post.POST_TYPE_CHOICES,
        })
        return context


class PostDetailView(TemplateView):
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        self.post_obj = _get_post_detail(kwargs['slug'])
        if self.post_obj is None:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.post_obj

        # Tăng view count
        increment_post_views(post.id)

        # Bài viết liên quan — cùng category, loại trừ bài hiện tại
        category_slug = post.category.slug if post.category else None
        related_rows, _ = get_posts(
            category_slug=category_slug,
            limit=4,
            offset=0,
        )
        # Loại bài hiện tại
        related_posts = [r for r in related_rows if r.get('slug') != post.slug][:3]

        context.update({
            'post': post,
            'related_posts': related_posts,
            'tags': post.get_tags_list(),
            'breadcrumb': [
                {'name': 'Blog', 'url': '/blog/'},
                {'name': post.category.name, 'url': post.category.get_absolute_url()} if post.category else None,
                {'name': post.title, 'url': None},
            ],
        })
        # Lọc None khỏi breadcrumb
        context['breadcrumb'] = [b for b in context['breadcrumb'] if b]
        return context


class CategoryPostListView(TemplateView):
    template_name = 'blog/category.html'
    paginate_by = 12

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = get_object_or_404(
            BlogCategory, slug=kwargs['category_slug'], is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page', 1)
        offset = (int(page) - 1) * self.paginate_by if str(page).isdigit() else 0

        rows, total = get_posts(
            category_slug=self.category.slug,
            limit=self.paginate_by,
            offset=offset,
        )

        paginator = Paginator(range(total), self.paginate_by)
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        context.update({
            'posts': rows,
            'category': self.category,
            'categories': _get_active_categories(),
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
            'total_count': total,
        })
        return context


class PostSearchView(TemplateView):
    template_name = 'blog/search.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '').strip()
        page  = self.request.GET.get('page', 1)

        if query and len(query) >= 2:
            offset = (int(page) - 1) * self.paginate_by if str(page).isdigit() else 0
            rows, total = get_posts(
                search=query,
                limit=self.paginate_by,
                offset=offset,
            )
        else:
            rows, total = [], 0

        paginator = Paginator(range(total) if total else [], self.paginate_by)
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        context.update({
            'posts': rows,
            'query': query,
            'total_count': total,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
            'categories': _get_active_categories(),
            'search_active': True,

            'search_hints': [
                'PLC',
                'IoT',
                'Modbus',
                'LoRaWAN',
                'SCADA',
                'Cảm biến',
            ],
        })
        return context