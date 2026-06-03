from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from apps.core.db import (
    get_category_tree,
    get_category_ancestors,
    get_products,
)
from .models import Category, Brand


class CategoryListView(ListView):
    template_name = "categories/list.html"
    context_object_name = "categories"

    def get_queryset(self):
        cache_key = "root_categories"
        qs = cache.get(cache_key)
        if not qs:
            qs = list(
                Category.objects.filter(level=0, is_active=True)
                .order_by("sort_order", "name")
            )
            cache.set(cache_key, qs, 900)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.core.db import count_products_in_category
        for cat in context["categories"]:
            cat.product_count_val = count_products_in_category(cat.id)

        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "categories/detail.html"
    context_object_name = "category"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        cache_key = f"category_obj_{slug}"
        obj = cache.get(cache_key)
        if not obj:
            obj = get_object_or_404(Category, slug=slug, is_active=True)
            cache.set(cache_key, obj, 600)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        req = self.request

        limit  = 24
        page   = max(1, int(req.GET.get("page", 1)))
        offset = (page - 1) * limit

        products, total = get_products(
            category_id = category.id,
            brand_id    = req.GET.get("brand") or None,
            min_price   = req.GET.get("min_price") or None,
            max_price   = req.GET.get("max_price") or None,
            stock_only  = bool(req.GET.get("in_stock")),
            search      = req.GET.get("q") or None,
            sort_by     = req.GET.get("sort", "featured"),
            limit       = limit,
            offset      = offset,
        )

        total_pages  = max(1, (total + limit - 1) // limit)
        has_previous = page > 1
        has_next     = page < total_pages

        cache_key_bc = f"category_breadcrumb_{category.id}"
        breadcrumb = cache.get(cache_key_bc)
        if not breadcrumb:
            breadcrumb = get_category_ancestors(category.id)
            cache.set(cache_key_bc, breadcrumb, 600)

        child_categories = list(
            category.get_children().filter(is_active=True).order_by("sort_order")
        )

        cache_key_brands = f"category_brands_{category.id}"
        brands = cache.get(cache_key_brands)
        if not brands:
            brands = list(
                Brand.objects.filter(
                    products__category__tree_id=category.tree_id,
                    products__category__lft__gte=category.lft,
                    products__category__rght__lte=category.rght,
                    products__status="published",
                    is_active=True,
                ).distinct().order_by("name")
            )
            cache.set(cache_key_brands, brands, 600)

        context.update({
            "products":       products,
            "total":          total,
            "page":           page,
            "total_pages":    total_pages,
            "has_previous":   has_previous,
            "has_next":       has_next,
            "prev_page":      page - 1,
            "next_page":      page + 1,
            "breadcrumb":     breadcrumb,
            "child_categories": child_categories,
            "brands":         brands,
            "current_sort":   req.GET.get("sort", "featured"),
            "active_brand":   req.GET.get("brand", ""),
        })
        return context


class BrandDetailView(ListView):
    """
    Trang thương hiệu — hiển thị tất cả sản phẩm của một brand.
    URL: /category/brand/<slug>/
    """
    template_name = "categories/brand.html"
    context_object_name = "products"
    paginate_by = 24

    def get_queryset(self):
        self.brand = get_object_or_404(Brand, slug=self.kwargs["slug"], is_active=True)

        limit  = 24
        page   = max(1, int(self.request.GET.get("page", 1)))
        offset = (page - 1) * limit

        products, total = get_products(
            brand_id   = self.brand.id,
            stock_only = bool(self.request.GET.get("in_stock")),
            sort_by    = self.request.GET.get("sort", "featured"),
            limit      = limit,
            offset     = offset,
        )
        self._total = total
        self._page  = page
        self._limit = limit
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_pages = max(1, (self._total + self._limit - 1) // self._limit)

        context.update({
            "brand":        self.brand,
            "total":        self._total,
            "page":         self._page,
            "total_pages":  total_pages,
            "has_previous": self._page > 1,
            "has_next":     self._page < total_pages,
            "prev_page":    self._page - 1,
            "next_page":    self._page + 1,
            "current_sort": self.request.GET.get("sort", "featured"),
        })
        return context