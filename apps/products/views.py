from django.http import Http404
from django.views.generic import TemplateView
from django.core.cache import cache
from apps.core.db import (
    get_products, get_product_detail,
    get_product_specs, get_product_images,
    get_related_products, get_category_tree,
)
from apps.products.tasks import increment_product_views_task
from apps.categories.models import Category


class ProductListView(TemplateView):
    template_name = "products/list.html"

    def _get_int(self, key, default=1, min_val=None, max_val=None):
        try:
            val = int(self.request.GET.get(key, default))
        except (ValueError, TypeError):
            return default
        if min_val is not None:
            val = max(min_val, val)
        if max_val is not None:
            val = min(max_val, val)
        return val

    def _get_decimal(self, key):
        from decimal import Decimal, InvalidOperation
        raw = self.request.GET.get(key, "").strip()
        if not raw:
            return None
        try:
            val = Decimal(raw)
            return val if val >= 0 else None
        except InvalidOperation:
            return None

    def _get_bool(self, key):
        return self.request.GET.get(key, "").lower() in ("1", "true", "yes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        limit  = 24
        page   = self._get_int("page", default=1, min_val=1)
        offset = (page - 1) * limit

        # ✅ Chuyển slug → ID
        category_slug = self.request.GET.get("category") or None
        category_id = None
        if category_slug:
            try:
                category_id = Category.objects.get(slug=category_slug).id
            except Category.DoesNotExist:
                pass

        products, total = get_products(
            category_id = category_id,
            brand_id    = self.request.GET.get("brand") or None,
            min_price   = self._get_decimal("min_price"),
            max_price   = self._get_decimal("max_price"),
            stock_only  = self._get_bool("in_stock"),
            search      = self.request.GET.get("q") or None,
            sort_by     = self.request.GET.get("sort", "featured"),
            limit       = limit,
            offset      = offset,
        )

        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        paginator = Paginator(range(total), limit)
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        from apps.core.db import count_products_in_category
        def _build_enriched_categories():
            raw = get_category_tree(active_only=True)
            for cat in raw:
                cat["count"] = count_products_in_category(cat["id"])
            return raw

        categories = cache.get_or_set(
            "sidebar_category_tree",
            _build_enriched_categories,
            timeout=900,
        )

        context.update({
            "products":     products,
            "total":        total,
            "page":         page_obj.number,
            "total_pages":  paginator.num_pages,
            "has_previous": page_obj.has_previous(),
            "has_next":     page_obj.has_next(),
            "prev_page":    page_obj.previous_page_number() if page_obj.has_previous() else None,
            "next_page":    page_obj.next_page_number() if page_obj.has_next() else None,
            "categories":   categories,
            "current_sort": self.request.GET.get("sort", "featured"),
            "page_obj":     page_obj,
            "paginator":    paginator,
            "is_paginated": paginator.num_pages > 1,
            "total_count":  total,
        })
        return context


class ProductDetailView(TemplateView):
    template_name = "products/detail.html"

    def get(self, request, slug, *args, **kwargs):
        self.slug = slug
        response = super().get(request, *args, **kwargs)
        product = self._get_product()
        if product:
            increment_product_views_task.delay(product["id"])
        return response

    def _get_product(self):
        cache_key = f"product_detail_{self.slug}"
        product = cache.get(cache_key)
        if not product:
            product = get_product_detail(self.slug)
            if product:
                cache.set(cache_key, product, 300)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self._get_product()
        
        if not product:
            raise Http404("Sản phẩm không tồn tại")
        
        if product.get('sale_price') and product.get('price') and product['price'] > 0:
            discount = int((1 - product['sale_price'] / product['price']) * 100) 
            product['discount_percent'] = discount
        else:
            product['discount_percent'] = 0

        product_id = product["id"]

        specs   = get_product_specs(product_id)
        images  = get_product_images(product_id)
        related = get_related_products(product_id, limit=6)

        from apps.products.models import ProductDocument
        documents = list(
                ProductDocument.objects.filter(product_id=product_id)
                .order_by('sort_order')
                .values('id', 'title', 'doc_type', 'file', 'file_size', 'sort_order')
        )

        specs_grouped = {}
        for s in specs:
            specs_grouped.setdefault(s["spec_group"], []).append(s)

        context.update({
            "product":       product,
            "specs_grouped": specs_grouped,
            "images":        images,
            "related":       related,
            "documents":     documents,
        })
        return context