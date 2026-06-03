from django.views.generic import TemplateView, ListView
from django.db.models import Q, Prefetch
from django.core.cache import cache
from django.http import JsonResponse
from apps.products.models import Product
from apps.solutions.models import Solution
from apps.categories.models import Category, Brand
from apps.blog.models import Post
from apps.core.db import search_autocomplete


class HomeView(TemplateView):
    """
    Home page view.
    Cached aggressively - full page cache 5 minutes.
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = 'home_page_context'
        cached = cache.get(cache_key)

        if cached:
            context.update(cached)
            return context

        # Featured solutions
        featured_solutions = list(
            Solution.objects.filter(status='published', is_featured=True)
            .select_related('solution_category')
            .order_by('sort_order')[:6]
        )

        # Featured products
        featured_products = list(
            Product.objects.filter(status='published', is_featured=True)
            .select_related('category', 'brand')
            .prefetch_related('images')
            .order_by('sort_order')[:8]
        )

        # New products
        new_products = list(
            Product.objects.filter(status='published', is_new=True)
            .select_related('category')
            .order_by('-created_at')[:4]
        )

        # Featured brands
        featured_brands = list(
            Brand.objects.filter(is_active=True, is_featured=True)
            .order_by('sort_order')[:12]
        )

        # Latest blog posts
        latest_posts = list(
            Post.objects.filter(status='published')
            .select_related('category', 'author')
            .order_by('-published_at')[:3]
        )

        # Stats for social proof section
        stats = {
            'products_count': Product.objects.filter(status='published').count(),
            'solutions_count': Solution.objects.filter(status='published').count(),
        }
        default_solution_names = [
            "Nông nghiệp thông minh",
            "Giám sát nhà máy",
            "Quản lý năng lượng",
            "Hạ tầng thông minh",
            "Môi trường & Nước",
            "Hậu cần & Kho bãi"
        ]
        payload = {
            'featured_solutions': featured_solutions,
            'featured_products': featured_products,
            'new_products': new_products,
            'featured_brands': featured_brands,
            'latest_posts': latest_posts,
            'stats': stats,
            'default_solution_names': default_solution_names,
        }
        context['search_hints'] = [
            "Cảm biến nhiệt độ",
            "Gateway 4G",
            "PLC",
            "Giám sát nhà kính"
        ]

        cache.set(cache_key, payload, 300)  # 5 minutes
        context.update(payload)
        return context


class SearchView(ListView):
    """
    Unified search across products and solutions.
    Supports pagination and filtering.
    """
    template_name = 'core/search.html'
    context_object_name = 'results'
    paginate_by = 24

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        search_type = self.request.GET.get('type', 'products')

        if not query or len(query) < 2:
            return Product.objects.none()

        if search_type == 'solutions':
            return Solution.objects.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query),
                status='published',
            ).select_related('solution_category').order_by('-is_featured', '-view_count')

        # Default: products
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(short_description__icontains=query) |
            Q(part_number__icontains=query),
            status='published',
        ).select_related('category', 'brand').prefetch_related('images').order_by('-is_featured', '-view_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['search_type'] = self.request.GET.get('type', 'products')
        context['total_count'] = self.get_queryset().count()
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = 'about_page_stats'
        cached = cache.get(cache_key)

        if cached:
            context['stats'] = cached
            return context

        stats = {
            'products_count': Product.objects.filter(status='published').count(),
        }

        cache.set(cache_key, stats, 300)  # 5 minutes
        context['stats'] = stats
        return context


class SitemapDataView(TemplateView):
    """Dynamic JSON sitemap data for frontend use."""
    def get(self, request, *args, **kwargs):
        data = {
            'solutions': list(
                Solution.objects.filter(status='published')
                .values('title', 'slug', 'updated_at')
            ),
            'products': list(
                Product.objects.filter(status='published')
                .values('name', 'slug', 'updated_at')
            ),
        }
        return JsonResponse(data)


def autocomplete_view(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse({"results": []})
 
    cache_key = f"autocomplete_{query}"
    cached = cache.get(cache_key)
    if cached:
        return JsonResponse({"results": cached})
 
    results = search_autocomplete(query, limit=8)
    cache.set(cache_key, results, 120)
    return JsonResponse({"results": results})