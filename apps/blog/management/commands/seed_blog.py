"""
apps/blog/management/commands/seed_blog.py
------------------------------------------
Management command seed demo data cho Blog.

Chạy:
    python manage.py seed_blog
    python manage.py seed_blog --posts 30
    python manage.py seed_blog --flush          # xoá data cũ rồi seed lại
    python manage.py seed_blog --no-relations   # bỏ qua gắn products/solutions
    python manage.py seed_blog --with-author    # gán author cho các bài viết
"""

import random
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Seed demo data cho Blog (BlogCategory + Post)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--posts", type=int, default=20,
            help="Số lượng bài viết cần tạo (mặc định: 20)",
        )
        parser.add_argument(
            "--flush", action="store_true",
            help="Xoá toàn bộ blog data trước khi seed",
        )
        parser.add_argument(
            "--no-relations", action="store_true",
            help="Bỏ qua gắn related_products và related_solutions",
        )
        parser.add_argument(
            "--with-author", action="store_true",
            help="Tự động gán author từ Customer có sẵn trong database",
        )

    def handle(self, *args, **options):
        from apps.blog.factories import (
            BlogCategoryFactory, PostFactory, BLOG_CATEGORIES,
        )
        from apps.blog.models import BlogCategory, Post

        n_posts       = options["posts"]
        do_flush      = options["flush"]
        no_relations  = options["no_relations"]
        with_author   = options["with_author"]

        self.stdout.write(self.style.MIGRATE_HEADING("\n🌱  SEED BLOG DATA\n"))

        # ── 1. Flush ──────────────────────────────────────────────────────────
        if do_flush:
            self.stdout.write("  ⚠  Đang xoá blog data cũ...")
            Post.objects.all().delete()
            BlogCategory.objects.all().delete()
            self.stdout.write(self.style.WARNING("  ✓  Đã xoá data cũ\n"))

        # ── 2. Lấy author (nếu cần) ───────────────────────────────────────────
        author = None
        if with_author:
            try:
                from apps.customers.models import Customer
                author = (
                    Customer.objects.filter(is_staff=True).order_by("?").first()
                    or Customer.objects.order_by("?").first()
                )
                if author:
                    self.stdout.write(
                        f"  👤  Sẽ gán author: {author.get_full_name()} ({author.email})\n"
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("  ⚠  Không tìm thấy Customer. Bỏ qua author.\n")
                    )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ⚠  Không thể lấy author: {e}\n"))

        with transaction.atomic():

            # ── 3. Tạo BlogCategories ──────────────────────────────────────────
            self.stdout.write("  📂  Tạo blog categories...")
            categories = []
            for name, slug in BLOG_CATEGORIES:
                cat, _ = BlogCategory.objects.get_or_create(
                    slug=slug,
                    defaults={"name": name, "is_active": True},
                )
                categories.append(cat)
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(categories)} categories\n"))

            # ── 4. Chuẩn bị related data (nếu cần) ────────────────────────────
            available_products  = []
            available_solutions = []

            if not no_relations:
                try:
                    from apps.products.models import Product
                    available_products = list(
                        Product.objects.filter(status="published").order_by("?")[:30]
                    )
                    self.stdout.write(
                        f"  📦  Tìm thấy {len(available_products)} sản phẩm để liên kết\n"
                    )
                except Exception:
                    pass

                try:
                    from apps.solutions.models import Solution
                    available_solutions = list(
                        Solution.objects.filter(status="published").order_by("?")[:15]
                    )
                    self.stdout.write(
                        f"  🔧  Tìm thấy {len(available_solutions)} giải pháp để liên kết\n"
                    )
                except Exception:
                    pass

            # ── 5. Tạo Posts ───────────────────────────────────────────────────
            self.stdout.write(f"  📝  Tạo {n_posts} bài viết...")
            posts = []

            for i in range(n_posts):
                cat = random.choice(categories)

                post_kwargs = dict(
                    category=cat,
                )

                if author:
                    post_kwargs["author"] = author

                # related_products
                if available_products and not no_relations:
                    n_products = random.randint(0, min(3, len(available_products)))
                    post_kwargs["with_related_products"] = (
                        random.sample(available_products, n_products)
                        if n_products else None
                    )

                # related_solutions
                if available_solutions and not no_relations:
                    n_solutions = random.randint(0, min(2, len(available_solutions)))
                    post_kwargs["with_related_solutions"] = (
                        random.sample(available_solutions, n_solutions)
                        if n_solutions else None
                    )

                try:
                    post = PostFactory(**post_kwargs)
                    posts.append(post)
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠  Bỏ qua bài viết #{i+1}: {e}\n")
                    )
                    continue

                # Progress bar
                if (i + 1) % 5 == 0 or (i + 1) == n_posts:
                    pct = int((i + 1) / n_posts * 20)
                    bar = "█" * pct + "░" * (20 - pct)
                    self.stdout.write(
                        f"\r  [{bar}] {i+1}/{n_posts}", ending=""
                    )
                    self.stdout.flush()

            self.stdout.write("")  # newline sau progress bar
            self.stdout.write(self.style.SUCCESS(f"  ✓  {len(posts)} bài viết đã tạo\n"))

            # ── 6. Đảm bảo có bài featured ────────────────────────────────────
            if posts:
                featured = random.sample(posts, min(3, len(posts)))
                Post.objects.filter(pk__in=[p.pk for p in featured]).update(is_featured=True)
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓  Đánh dấu {len(featured)} bài viết nổi bật\n")
                )

        # ── 7. Summary ────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("📊  Tổng kết:"))
        self.stdout.write(f"     BlogCategories : {BlogCategory.objects.count()}")
        self.stdout.write(f"     Posts (total)  : {Post.objects.count()}")
        self.stdout.write(f"     Posts published: {Post.objects.filter(status='published').count()}")
        self.stdout.write(f"     Posts featured : {Post.objects.filter(is_featured=True).count()}")

        # Breakdown by post_type
        from django.db.models import Count
        by_type = Post.objects.values("post_type").annotate(n=Count("id"))
        for row in by_type:
            label = dict(Post.POST_TYPE_CHOICES).get(row["post_type"], row["post_type"])
            self.stdout.write(f"       • {label:<25}: {row['n']}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅  Seed blog hoàn tất!\n"))
        self.stdout.write(
            "💡  Tip: Kết hợp với các lệnh khác để có full data:\n"
            "    python manage.py seed_demo && "
            "python manage.py seed_solutions && "
            "python manage.py seed_blog --with-author\n"
        )