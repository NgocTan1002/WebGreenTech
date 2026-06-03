"""XML Sitemaps for all public content."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.products.models import Product
from apps.solutions.models import Solution
from apps.categories.models import Category
from apps.blog.models import Post


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'solutions:list', 'products:list', 'contacts:contact']
        # 'blog:list' — uncomment when blog URLs are wired into config/urls.py

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    limit = 50000  # Django splits into sitemap-products.xml, sitemap-products1.xml … automatically

    def items(self):
        return (
            Product.objects
            .filter(status='published')
            .only('slug', 'updated_at')
            .order_by('-updated_at')
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class SolutionSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return (
            Solution.objects
            .filter(status='published')
            .only('slug', 'updated_at')
            .order_by('-updated_at')
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return (
            Category.objects
            .filter(is_active=True)
            .only('slug', 'updated_at')
            .order_by('tree_id', 'lft')   # MPTT natural order, avoids filesort
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return (
            Post.objects
            .filter(status='published')
            .only('slug', 'updated_at', 'published_at')
            .order_by('-published_at')
        )

    def lastmod(self, obj):
        # published_at is more semantically correct than updated_at for posts
        return obj.published_at or obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()