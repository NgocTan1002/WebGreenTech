from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.core.sitemaps import (
    StaticViewSitemap,
    ProductSitemap,
    SolutionSitemap,
    CategorySitemap,
    BlogSitemap,
)
 
sitemaps = {
    'static':     StaticViewSitemap,
    'products':   ProductSitemap,
    'solutions':  SolutionSitemap,
    'categories': CategorySitemap,
    'blog':       BlogSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",         include("apps.core.urls",      namespace="core")),
    path("products/", include("apps.products.urls", namespace="products")),
    path("solutions/", include("apps.solutions.urls", namespace="solutions")),
    path("cart/",    include("apps.cart.urls",      namespace="cart")),
    path("orders/",  include("apps.orders.urls",    namespace="orders")),
    path("categories/",  include("apps.categories.urls",    namespace="categories")),
    path("contact/", include("apps.contacts.urls",  namespace="contacts")),
    path("blog/",    include("apps.blog.urls",      namespace="blog")),
    path("customers/", include("apps.customers.urls", namespace="customers")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)