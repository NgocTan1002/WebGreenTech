"""
apps/products/management/commands/seed_demo.py
-----------------------------------------------
Management command seed toàn bộ demo data.

Chạy:
    python manage.py seed_demo
    python manage.py seed_demo --products 50
    python manage.py seed_demo --flush        # xoá data cũ rồi seed lại
    python manage.py seed_demo --no-images    # bỏ qua tạo ảnh (nhanh hơn)
"""

import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction


class Command(BaseCommand):
    help = "Seed demo data cho trang web IoT"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products", type=int, default=30,
            help="Số lượng sản phẩm cần tạo (mặc định: 30)",
        )
        parser.add_argument(
            "--flush", action="store_true",
            help="Xoá toàn bộ data products/categories/brands trước khi seed",
        )
        parser.add_argument(
            "--no-images", action="store_true",
            help="Bỏ qua bước tạo ảnh thumbnail (nhanh hơn khi test)",
        )

    def handle(self, *args, **options):
        # Import ở đây để tránh lỗi khi chưa migrate
        from apps.categories.models import Category, Brand
        from apps.products.factories import (
            CategoryFactory, BrandFactory, ProductFactory,
            RelatedProductFactory,
            CATEGORIES_DATA, BRANDS_DATA,
        )

        n_products = options["products"]
        do_flush   = options["flush"]
        no_images  = options["no_images"]

        self.stdout.write(self.style.MIGRATE_HEADING("\n🌱  SEED DEMO DATA\n"))

        # ── 1. Flush ──────────────────────────────────────────────────────────
        if do_flush:
            self.stdout.write("  ⚠  Đang xoá data cũ...")
            from apps.products.models import (
                Product, ProductImage, ProductSpecification,
                ProductDocument, RelatedProduct,
            )
            RelatedProduct.objects.all().delete()
            ProductDocument.objects.all().delete()
            ProductSpecification.objects.all().delete()
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("  ✓  Đã xoá data cũ\n"))

        with transaction.atomic():

            # ── 2. Tạo Brands ─────────────────────────────────────────────────
            self.stdout.write("  📦  Tạo brands...")
            brands = []
            for name, slug in BRANDS_DATA:
                b, created = Brand.objects.get_or_create(
                    slug=slug,
                    defaults={"name": name},
                )
                brands.append(b)
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(brands)} brands\n"))

            # ── 3. Tạo Categories (có cấu trúc cha-con) ───────────────────────
            self.stdout.write("  📂  Tạo categories...")
            cat_map = {}   # slug → instance

            # Tạo parent trước
            for name, slug, parent_slug in CATEGORIES_DATA:
                if parent_slug is None:
                    cat, _ = Category.objects.get_or_create(
                        slug=slug,
                        defaults={
                            "name": name,
                            "low_stock_threshold": random.randint(3, 10),
                        },
                    )
                    cat_map[slug] = cat

            # Tạo children sau
            for name, slug, parent_slug in CATEGORIES_DATA:
                if parent_slug is not None:
                    parent = cat_map.get(parent_slug)
                    cat, _ = Category.objects.get_or_create(
                        slug=slug,
                        defaults={
                            "name": name,
                            "parent": parent,
                            "low_stock_threshold": random.randint(3, 10),
                        },
                    )
                    cat_map[slug] = cat

            all_categories = list(cat_map.values())
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(all_categories)} categories\n"))

            # ── 4. Tạo Products ───────────────────────────────────────────────
            self.stdout.write(f"  🔧  Tạo {n_products} sản phẩm...")
            products = []

            for i in range(n_products):
                cat   = random.choice(all_categories)
                brand = random.choice(brands)

                p = ProductFactory(
                    category=cat,
                    brand=brand,
                    with_specs=random.randint(2, 4),       # số nhóm spec
                    with_images=0 if no_images else random.randint(0, 3),
                    with_documents=random.randint(1, 3),
                )
                products.append(p)

                # Progress bar đơn giản
                if (i + 1) % 5 == 0 or (i + 1) == n_products:
                    pct = int((i + 1) / n_products * 20)
                    bar = "█" * pct + "░" * (20 - pct)
                    self.stdout.write(
                        f"\r  [{bar}] {i+1}/{n_products}", ending=""
                    )
                    self.stdout.flush()

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(products)} sản phẩm\n"))

            # ── 5. Tạo Related Products ───────────────────────────────────────
            self.stdout.write("  🔗  Tạo liên kết sản phẩm liên quan...")
            related_count = 0
            for p in random.sample(products, min(len(products), n_products // 2)):
                candidates = [x for x in products if x != p]
                if not candidates:
                    continue
                for related in random.sample(candidates, min(3, len(candidates))):
                    try:
                        RelatedProductFactory(product=p, related=related)
                        related_count += 1
                    except Exception:
                        pass  # unique_together có thể bị trùng, bỏ qua

            self.stdout.write(self.style.SUCCESS(f"  ✓  {related_count} liên kết\n"))

        # ── 6. Summary ────────────────────────────────────────────────────────
        from apps.products.models import Product, ProductSpecification, ProductDocument
        self.stdout.write(self.style.MIGRATE_HEADING("📊  Tổng kết:"))
        self.stdout.write(f"     Brands        : {Brand.objects.count()}")
        self.stdout.write(f"     Categories    : {Category.objects.count()}")
        self.stdout.write(f"     Products      : {Product.objects.count()}")
        self.stdout.write(f"     Specifications: {ProductSpecification.objects.count()}")
        self.stdout.write(f"     Documents     : {ProductDocument.objects.count()}")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅  Seed hoàn tất! Chạy: python manage.py runserver"))