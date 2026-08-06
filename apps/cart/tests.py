from decimal import Decimal

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse

from apps.categories.models import Category
from apps.customers.models import Customer
from apps.products.models import Product

from .admin import CartAdmin
from .models import Cart, CartItem


class CartSubtotalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Thiết bị kiểm thử',
            slug='thiet-bi-kiem-thu',
        )
        cls.fixed_product = Product.objects.create(
            name='Sản phẩm giá cố định',
            slug='san-pham-gia-co-dinh',
            sku='TEST-FIXED-001',
            category=cls.category,
            pricing_type=Product.PRICING_FIXED,
            price=Decimal('100000'),
        )
        cls.quote_product = Product.objects.create(
            name='Sản phẩm chờ báo giá',
            slug='san-pham-cho-bao-gia',
            sku='TEST-QUOTE-001',
            category=cls.category,
            pricing_type=Product.PRICING_QUOTE,
        )

    def setUp(self):
        self.cart_admin = CartAdmin(Cart, AdminSite())

    def test_subtotal_only_sums_items_with_known_prices(self):
        cart = Cart.objects.create(session_key='mixed-cart')
        CartItem.objects.create(
            cart=cart,
            product=self.fixed_product,
            quantity=2,
        )
        CartItem.objects.create(
            cart=cart,
            product=self.quote_product,
            quantity=1,
        )

        self.assertEqual(cart.subtotal, Decimal('200000'))
        self.assertTrue(cart.has_pending_quote)
        self.assertEqual(
            self.cart_admin.subtotal_display(cart),
            '200,000 ₫ + Chờ báo giá',
        )

    def test_quote_only_cart_is_not_displayed_as_free(self):
        cart = Cart.objects.create(session_key='quote-cart')
        CartItem.objects.create(
            cart=cart,
            product=self.quote_product,
            quantity=3,
        )

        self.assertEqual(cart.subtotal, Decimal('0'))
        self.assertTrue(cart.has_pending_quote)
        self.assertEqual(
            self.cart_admin.subtotal_display(cart),
            'Chờ báo giá',
        )

    def test_fixed_price_cart_keeps_numeric_subtotal(self):
        cart = Cart.objects.create(session_key='fixed-cart')
        CartItem.objects.create(
            cart=cart,
            product=self.fixed_product,
            quantity=2,
        )

        self.assertEqual(cart.subtotal, Decimal('200000'))
        self.assertFalse(cart.has_pending_quote)
        self.assertEqual(
            self.cart_admin.subtotal_display(cart),
            '200,000 ₫',
        )


class CartAdminChangelistTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name='Danh mục admin test',
            slug='danh-muc-admin-test',
        )
        quote_product = Product.objects.create(
            name='Sản phẩm báo giá admin test',
            slug='san-pham-bao-gia-admin-test',
            sku='ADMIN-QUOTE-001',
            category=category,
            pricing_type=Product.PRICING_QUOTE,
        )
        cart = Cart.objects.create(session_key='admin-quote-cart')
        CartItem.objects.create(
            cart=cart,
            product=quote_product,
            quantity=1,
        )
        cls.admin_user = Customer.objects.create_superuser(
            email='cart-admin@example.com',
            password='test-password',
            first_name='Cart',
            last_name='Admin',
        )

    def test_changelist_supports_quote_items_without_prices(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse('admin:cart_cart_changelist'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chờ báo giá')
