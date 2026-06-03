"""
apps/solutions/management/commands/seed_solutions.py
-----------------------------------------------------
Management command seed demo data cho Solutions.

Chạy:
    python manage.py seed_solutions
    python manage.py seed_solutions --solutions 10
    python manage.py seed_solutions --flush          # xoá data cũ rồi seed lại
    python manage.py seed_solutions --no-products    # bỏ qua gắn sản phẩm
    python manage.py seed_solutions --no-cases       # bỏ qua customer cases
"""

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed demo data cho Solutions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--solutions", type=int, default=8,
            help="Số lượng solution cần tạo (mặc định: 8)",
        )
        parser.add_argument(
            "--flush", action="store_true",
            help="Xoá toàn bộ solutions data trước khi seed",
        )
        parser.add_argument(
            "--no-products", action="store_true",
            help="Bỏ qua bước gắn sản phẩm vào solution",
        )
        parser.add_argument(
            "--no-cases", action="store_true",
            help="Bỏ qua bước tạo customer cases",
        )

    def handle(self, *args, **options):
        from apps.solutions.models import (
            SolutionCategory, Solution, SolutionProduct,
            ArchitectureBlock, WorkflowStep, CustomerCase,
        )
        from apps.solutions.factories import (
            SolutionFactory, SolutionCategoryFactory,
            SOLUTION_CATEGORIES_DATA, SOLUTION_TITLES,
        )

        n_solutions  = options["solutions"]
        do_flush     = options["flush"]
        no_products  = options["no_products"]
        no_cases     = options["no_cases"]

        self.stdout.write(self.style.MIGRATE_HEADING("\n🌱  SEED SOLUTIONS DATA\n"))

        # ── 1. Flush ──────────────────────────────────────────────────────────
        if do_flush:
            self.stdout.write("  ⚠  Đang xoá data solutions cũ...")
            CustomerCase.objects.all().delete()
            WorkflowStep.objects.all().delete()
            ArchitectureBlock.objects.all().delete()
            SolutionProduct.objects.all().delete()
            Solution.objects.all().delete()
            SolutionCategory.objects.all().delete()
            self.stdout.write(self.style.WARNING("  ✓  Đã xoá data cũ\n"))

        with transaction.atomic():

            # ── 2. Tạo SolutionCategories ──────────────────────────────────────
            self.stdout.write("  📂  Tạo solution categories...")
            cat_map = {}
            for name, slug in SOLUTION_CATEGORIES_DATA:
                cat, _ = SolutionCategory.objects.get_or_create(
                    slug=slug,
                    defaults={"name": name, "is_active": True},
                )
                cat_map[slug] = cat
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(cat_map)} categories\n"))

            # ── 3. Lấy danh sách products để gắn vào solution ─────────────────
            available_products = []
            if not no_products:
                try:
                    from apps.products.models import Product
                    available_products = list(
                        Product.objects.filter(status="published").order_by("?")[:50]
                    )
                    if available_products:
                        self.stdout.write(
                            f"  📦  Tìm thấy {len(available_products)} sản phẩm để gắn vào solutions\n"
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                "  ⚠  Không có sản phẩm nào. Chạy seed_demo trước "
                                "hoặc dùng --no-products\n"
                            )
                        )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  ⚠  Không thể lấy products: {e}\n"))

            # ── 4. Tạo Solutions ───────────────────────────────────────────────
            self.stdout.write(f"  🔧  Tạo {n_solutions} solutions...")

            # Ưu tiên dùng dữ liệu mẫu có tên thực tế
            title_pool = list(SOLUTION_TITLES)
            random.shuffle(title_pool)

            solutions = []
            for i in range(n_solutions):
                # Lấy title/slug/category từ pool nếu còn, ngược lại tự sinh
                if title_pool:
                    title, slug, cat_slug = title_pool.pop()
                    category = cat_map.get(cat_slug, random.choice(list(cat_map.values())))
                else:
                    from faker import Faker
                    _fake = Faker("vi_VN")
                    title = f"Giải pháp IoT {i + 1:02d} — {_fake.word().capitalize()}"
                    slug  = slugify(title)[:200]
                    category = random.choice(list(cat_map.values()))

                # Gắn products (lấy 4–8 sản phẩm ngẫu nhiên)
                solution_products = []
                if available_products:
                    n_products_for_sol = random.randint(4, min(8, len(available_products)))
                    solution_products = random.sample(available_products, n_products_for_sol)

                sol = SolutionFactory(
                    title=title,
                    slug=slug,
                    solution_category=category,
                    with_workflow_steps=random.randint(4, 6),
                    with_architecture_blocks=random.randint(3, 5),
                    with_customer_cases=0 if no_cases else random.randint(1, 2),
                    with_products=solution_products if solution_products else None,
                )
                solutions.append(sol)

                # Progress
                if (i + 1) % 2 == 0 or (i + 1) == n_solutions:
                    pct = int((i + 1) / n_solutions * 20)
                    bar = "█" * pct + "░" * (20 - pct)
                    self.stdout.write(f"\r  [{bar}] {i+1}/{n_solutions}", ending="")
                    self.stdout.flush()

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(solutions)} solutions\n"))

            # Đảm bảo ít nhất 1-2 solution là featured
            featured = random.sample(solutions, min(3, len(solutions)))
            for sol in featured:
                Solution.objects.filter(pk=sol.pk).update(is_featured=True)

        # ── 5. Summary ────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("📊  Tổng kết:"))
        self.stdout.write(f"     SolutionCategories  : {SolutionCategory.objects.count()}")
        self.stdout.write(f"     Solutions           : {Solution.objects.count()}")
        self.stdout.write(f"     WorkflowSteps       : {WorkflowStep.objects.count()}")
        self.stdout.write(f"     ArchitectureBlocks  : {ArchitectureBlock.objects.count()}")
        self.stdout.write(f"     SolutionProducts    : {SolutionProduct.objects.count()}")
        self.stdout.write(f"     CustomerCases       : {CustomerCase.objects.count()}")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅  Seed solutions hoàn tất!\n"))
        self.stdout.write(
            "💡  Tip: Chạy cùng với seed_demo để có sản phẩm gắn vào solutions:\n"
            "    python manage.py seed_demo && python manage.py seed_solutions\n"
        )