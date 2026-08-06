from __future__ import annotations

import base64
from datetime import date
from pathlib import Path
from decimal import Decimal

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import TransactionTestCase

from apps.core import db as core_db
from apps.customers.models import Customer
from apps.categories.models import Category, Brand
from apps.blog.models import BlogCategory, Post
from apps.products.models import (
    Product,
    ProductImage,
    ProductSpecification,
    RelatedProduct,
)
from apps.solutions.models import (
    SolutionCategory,
    Solution,
    SolutionDeploymentImage,
    SolutionProduct,
)
from apps.cart.models import Cart


DUMMY_PNG = base64.b64decode(
    # 1x1 transparent PNG
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+lmU0AAAAASUVORK5CYII="
)


def dummy_image(name: str = "test.png") -> SimpleUploadedFile:
    return SimpleUploadedFile(name=name, content=DUMMY_PNG, content_type="image/png")


class SqlFunctionsLoaderMixin:
    """
    Load ONLY selected SQL functions into the test database.

    Note:
    - Your project currently uses a hybrid approach (Django models + hand-written SQL functions).
    - Some SQL functions may be temporarily out-of-sync with models; tests should not execute every fn_* blindly.
    """

    # relative to <BASE_DIR>/function/
    FUNCTION_FILES: list[str] = []

    @classmethod
    def load_sql_functions(cls) -> None:
        if not cls.FUNCTION_FILES:
            return

        func_dir = Path(settings.BASE_DIR) / "function"
        with connection.cursor() as cursor:
            for file_name in cls.FUNCTION_FILES:
                path = func_dir / file_name
                sql = path.read_text(encoding="utf-8").strip()
                if not sql:
                    continue

                # Split CREATE and ALTER to avoid "cannot execute multiple commands" issues.
                marker = "\nALTER FUNCTION"
                idx = sql.find(marker)
                if idx == -1:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql[:idx].strip())
                    cursor.execute(sql[idx + 1 :].strip())


class CoreDbFunctionTests(TransactionTestCase, SqlFunctionsLoaderMixin):
    # Pick functions that are likely compatible with current Django models.
    FUNCTION_FILES = [
        # "fn_get_product.sql",
        # "fn_get_product_detail.sql",
        # "fn_get_posts.sql",
        # "fn_count_products_in_category.sql",
        # "fn_create_order_from_cart.sql",
        # "fn_get_customer_orders.sql",
        "fn_get_category_tree.sql",
        "fn_get_category_ancestors.sql",
        "fn_search_autocomplete.sql",
        "fn_increment_product_views.sql",
        "fn_get_product_specs.sql",
        "fn_get_product_images.sql",
        "fn_get_related_products.sql",
        "fn_get_solutions.sql",
        "fn_get_solution_products.sql",
        "fn_get_solution_detail.sql",
        "fn_increment_solution_views.sql",
        "fn_increment_post_views.sql",
        "fn_get_cart_detail.sql",
        "fn_get_cart_summary.sql",
        "fn_upsert_cart_item.sql",
    ]

    # ------------------------------------------------------------------ #
    # FIX: TransactionTestCase KHÔNG hỗ trợ setUpTestData vì nó không    #
    # wrap các test trong transaction. setUpTestData là tính năng riêng   #
    # của TestCase (dùng savepoint). Phải dùng setUp() thay thế.          #
    #                                                                      #
    # Đánh đổi: setUp() chạy lại trước MỖI test (chậm hơn), nhưng đây   #
    # là cách duy nhất đúng khi kết hợp TransactionTestCase + test data. #
    # ------------------------------------------------------------------ #

    @classmethod
    def setUpClass(cls) -> None:
        # setUpClass vẫn dùng được với TransactionTestCase.
        # Database đã tồn tại ở thời điểm này nên load SQL functions là an toàn.
        super().setUpClass()
        cls.load_sql_functions()

    def setUp(self) -> None:
        """Tạo lại toàn bộ test data trước mỗi test."""

        # ── Categories ────────────────────────────────────────────────────
        self.root_category = Category.objects.create(
            name="Sensors",
            slug="sensors",
            description="Root category",
            icon_class="fa-solid fa-sensor",
            is_active=True,
            show_in_nav=True,
            sort_order=1,
            low_stock_threshold=10,
        )
        self.child_category = Category.objects.create(
            name="IoT Sensors",
            slug="iot-sensors",
            description="Child category",
            parent=self.root_category,
            icon_class="fa-solid fa-iot",
            is_active=True,
            show_in_nav=True,
            sort_order=1,
            low_stock_threshold=5,
        )
        # Rebuild MPTT tree sau khi tạo categories để đảm bảo
        # các truy vấn ancestor/descendant hoạt động đúng.
        Category.objects.rebuild()

        # ── Brand ─────────────────────────────────────────────────────────
        self.brand = Brand.objects.create(
            name="Acme",
            slug="acme",
            country="Vietnam",
            is_active=True,
            is_featured=True,
            sort_order=1,
        )

        # ── Products ──────────────────────────────────────────────────────
        self.product = Product.objects.create(
            name="IoT Sensor X",
            slug="iot-sensor-x",
            sku="SKU-IOT-X",
            part_number="PN-IOT-X",
            thumbnail=dummy_image("product-thumbnail.png"),
            category=self.child_category,
            brand=self.brand,
            status="published",
            pricing_type=Product.PRICING_FIXED,
            price=Decimal("100000"),
            sale_price=Decimal("80000"),
            stock_status=Product.STOCK_IN,
            stock_quantity=100,
            min_order_qty=1,
            short_description="Test product",
            description="Full description",
            highlights=["IP67", "RS485"],
            view_count=0,
        )
        self.related_product = Product.objects.create(
            name="IoT Sensor Y",
            slug="iot-sensor-y",
            sku="SKU-IOT-Y",
            part_number="PN-IOT-Y",
            category=self.child_category,
            brand=self.brand,
            status="published",
            pricing_type=Product.PRICING_FIXED,
            price=Decimal("120000"),
            sale_price=None,
            stock_status=Product.STOCK_LOW,
            stock_quantity=5,
            min_order_qty=1,
            short_description="Related product",
            description="Full description",
            highlights=["IP65"],
            view_count=0,
        )

        self.spec_1 = ProductSpecification.objects.create(
            product=self.product,
            group="Thông số điện",
            key="Điện áp",
            value="220",
            unit="VAC",
            sort_order=1,
        )

        self.img_1 = ProductImage.objects.create(
            product=self.product,
            image=dummy_image("product-main.png"),
            alt_text="Main image",
            is_primary=True,
            sort_order=1,
        )
        self.img_2 = ProductImage.objects.create(
            product=self.product,
            image=dummy_image("product-2.png"),
            alt_text="Second image",
            is_primary=False,
            sort_order=2,
        )

        self.related = RelatedProduct.objects.create(
            product=self.product,
            related=self.related_product,
            relation_type=RelatedProduct.RELATION_COMPATIBLE,
            sort_order=1,
        )

        # ── Solutions ─────────────────────────────────────────────────────
        self.solution_category = SolutionCategory.objects.create(
            name="Smart Agriculture",
            slug="smart-agri",
            description="Industry category",
            is_active=True,
            sort_order=1,
        )
        self.solution = Solution.objects.create(
            title="Farming Monitoring",
            slug="farming-monitoring",
            subtitle="Monitoring & control",
            solution_category=self.solution_category,
            thumbnail=dummy_image("solution.png"),
            short_description="Solution short description",
            overview="<p>Overview</p>",
            deployment_site="GreenTech Factory",
            deployment_location="Que Vo Industrial Park, Bac Ninh",
            deployed_at=date(2025, 6, 1),
            pain_points=["Remote monitoring difficulty"],
            benefits=["Save water"],
            workflow_title="Workflow",
            workflow_description="Step 1 ...",
            cta_title="CTA",
            cta_primary_text="Primary",
            cta_primary_url="https://example.com/primary",
            cta_secondary_text="Secondary",
            cta_secondary_url="https://example.com/secondary",
            status="published",
            is_featured=True,
            sort_order=1,
            view_count=0,
        )
        SolutionProduct.objects.create(
            solution=self.solution,
            product=self.product,
            is_featured=True,
            role_description="Main sensor product",
            sort_order=1,
        )
        SolutionProduct.objects.create(
            solution=self.solution,
            product=self.related_product,
            is_featured=False,
            role_description="Supporting product",
            sort_order=2,
        )

        # ── Cart ──────────────────────────────────────────────────────────
        self.cart = Cart.objects.create(session_key="sess-test", is_active=True)

        # ── Author + Blog Post ────────────────────────────────────────────
        self.author = Customer.objects.create_user(
            email="author@example.com",
            password="pass1234",
            first_name="Author",
            last_name="User",
            company_name="TestCo",
        )
        self.blog_category = BlogCategory.objects.create(
            name="Automation",
            slug="automation",
            is_active=True,
            sort_order=1,
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            post_type=Post.POST_TYPE_ARTICLE,
            category=self.blog_category,
            author=self.author,
            thumbnail=dummy_image("post.png"),
            short_description="Short description",
            content="<p>Hello</p>",
            read_time=3,
            tags="PLC, IoT",
            status="published",
            is_featured=False,
            sort_order=1,
            view_count=0,
        )

    # ------------------------------------------------------------------ #
    # Tests                                                                #
    # ------------------------------------------------------------------ #

    def test_get_category_tree_and_ancestors(self):
        tree = core_db.get_category_tree(active_only=True)
        slugs = {row["slug"] for row in tree}
        self.assertIn(self.root_category.slug, slugs)
        self.assertIn(self.child_category.slug, slugs)

        ancestors = core_db.get_category_ancestors(self.child_category.id)
        ancestor_slugs = [row["slug"] for row in ancestors]
        self.assertIn(self.root_category.slug, ancestor_slugs)

    def test_search_autocomplete(self):
        results = core_db.search_autocomplete("iot", limit=5)
        self.assertTrue(any(r["result_type"] in {"product", "solution"} for r in results))

    def test_product_specs_images_and_related_products(self):
        specs = core_db.get_product_specs(self.product.id)
        self.assertTrue(any(s["spec_key"] == self.spec_1.key for s in specs))

        images = core_db.get_product_images(self.product.id)
        self.assertTrue(any(img["is_primary"] for img in images))

        related = core_db.get_related_products(self.product.id, limit=6)
        self.assertTrue(any(r["sku"] == self.related_product.sku for r in related))

    def test_solutions_list_detail_and_products(self):
        solutions, total = core_db.get_solutions(limit=10, offset=0)
        self.assertGreaterEqual(total, 1)
        self.assertTrue(any(s["slug"] == self.solution.slug for s in solutions))

        detail = core_db.get_solution_detail(self.solution.slug)
        self.assertIsNotNone(detail)
        self.assertEqual(detail["slug"], self.solution.slug)
        self.assertEqual(detail["deployment_site"], "GreenTech Factory")
        self.assertEqual(detail["deployment_location"], "Que Vo Industrial Park, Bac Ninh")
        self.assertEqual(detail["deployed_at"], date(2025, 6, 1))

        first_photo = SolutionDeploymentImage.objects.create(
            solution=self.solution,
            image=dummy_image("deployment-1.png"),
            caption="Control cabinet installed on site",
            alt_text="Installed control cabinet",
            is_primary=True,
            sort_order=1,
        )
        second_photo = SolutionDeploymentImage.objects.create(
            solution=self.solution,
            image=dummy_image("deployment-2.png"),
            caption="System commissioning",
            is_primary=True,
            sort_order=2,
        )
        first_photo.refresh_from_db()
        self.assertFalse(first_photo.is_primary)
        self.assertTrue(second_photo.is_primary)

        response = self.client.get(self.solution.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "System commissioning")

        sol_products = core_db.get_solution_products(self.solution.id, featured_only=False)
        self.assertTrue(any(p["product_sku"] == self.product.sku for p in sol_products))

    def test_increment_product_solution_and_post_views(self):
        core_db.increment_product_views(self.product.id)
        self.product.refresh_from_db()
        self.assertEqual(self.product.view_count, 1)

        core_db.increment_solution_views(self.solution.id)
        self.solution.refresh_from_db()
        self.assertEqual(self.solution.view_count, 1)

        core_db.increment_post_views(self.post.id)
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)

    def test_cart_upsert_detail_and_summary(self):
        result1 = core_db.upsert_cart_item(
            cart_id=str(self.cart.id),
            product_id=self.product.id,
            quantity=2,
            unit_price=Decimal("90000"),
        )
        self.assertTrue(result1["created"])
        self.assertEqual(int(result1["quantity"]), 2)

        result2 = core_db.upsert_cart_item(
            cart_id=str(self.cart.id),
            product_id=self.product.id,
            quantity=1,
            unit_price=Decimal("90000"),
        )
        self.assertFalse(result2["created"])
        self.assertEqual(int(result2["quantity"]), 3)

        summary = core_db.get_cart_summary(str(self.cart.id))
        self.assertEqual(int(summary["total_items"]), 3)
        self.assertEqual(Decimal(str(summary["subtotal"])), Decimal("270000"))

        detail = core_db.get_cart_detail(str(self.cart.id))
        self.assertEqual(len(detail), 1)
        self.assertEqual(int(detail[0]["quantity"]), 3)

        session = self.client.session
        session["cart_session_key"] = self.cart.session_key
        session.save()
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'/media/{self.product.thumbnail.name}')
