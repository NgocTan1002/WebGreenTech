from django.conf import settings
from django.core.cache import cache
from apps.solutions.models import Solution, SolutionCategory
from apps.categories.models import Brand, Category
from apps.products.models import Product


def global_context(request):
    cache_key = 'global_context_data'
    cached = cache.get(cache_key)

    if not cached:
        nav_solutions = list(
            Solution.objects.filter(status='published', is_featured=True)
            .values('title', 'slug', 'solution_category__name')
            .order_by('sort_order')[:8]
        )
        solution_categories = list(
            SolutionCategory.objects.filter(is_active=True).values('name', 'slug').order_by('sort_order')
        )
        nav_categories = list(
            Category.objects.filter(level=0, is_active=True, show_in_nav=True)
            .order_by('sort_order')[:10]
        )
        # Footer: 4 solutions thực tế
        footer_solutions = list(
            Solution.objects.filter(status='published')
            .values('title', 'slug')
            .order_by('sort_order', '-created_at')[:4]
        )
        # Footer: 4 products thực tế
        footer_products = list(
            Product.objects.filter(status='published')
            .values('name', 'slug')
            .order_by('sort_order', '-created_at')[:4]
        )
        featured_brands = list(
            Brand.objects.filter(is_active=True, is_featured=True)
            .order_by('sort_order', 'name')[:12]
        )
        cached = {
            'nav_solutions': nav_solutions,
            'solution_categories': solution_categories,
            'nav_categories': nav_categories,
            'footer_solutions': footer_solutions,
            'footer_products': footer_products,
            'featured_brands': featured_brands,
        }
        cache.set(cache_key, cached, 600)
    
    cart_count = 0
    try:
        from apps.cart.models import Cart
        from apps.core.db import get_cart_summary

        session_key = request.session.session_key
        if session_key:
            if request.user.is_authenticated:
                cart = Cart.objects.filter(customer=request.user, is_active=True).values('id').first()
            else:
                cart = Cart.objects.filter(session_key=session_key, is_active=True, customer=None).values('id').first()
            
            if cart:
                summary = get_cart_summary(str(cart['id']))
                cart_count = int(summary.get('total_items', 0))
    except Exception:
        cart_count = 0

    return {
        **cached,
        'SITE_URL': settings.SITE_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
        'cart_count': cart_count,
    }
