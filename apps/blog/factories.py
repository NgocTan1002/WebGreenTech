"""
apps/blog/factories.py
----------------------
Factory Boy factories cho Blog app (BlogCategory, Post).
Dùng để seed demo data hoặc viết tests.

Cài đặt:
    pip install factory-boy Pillow faker

Sử dụng nhanh:
    from apps.blog.factories import PostFactory, BlogCategoryFactory

    # Tạo 1 category + 1 post liên kết
    cat = BlogCategoryFactory()
    PostFactory(category=cat)

    # Tạo batch 20 bài viết (category tự động tạo)
    PostFactory.create_batch(20)

    # Tạo bài viết loại cụ thể
    PostFactory(post_type='guide', with_related_products=3)
"""

import random

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory, ImageField
from django.utils.text import slugify
from django.utils import timezone
from faker import Faker

from apps.blog.models import BlogCategory, Post

fake = Faker("vi_VN")

# ─────────────────────────────────────────────────────────────────────────────
# Dữ liệu mẫu IoT / công nghiệp
# ─────────────────────────────────────────────────────────────────────────────

BLOG_CATEGORIES = [
    ("Tự động hoá",        "tu-dong-hoa"),
    ("IoT & Kết nối",      "iot-ket-noi"),
    ("Cảm biến",           "cam-bien"),
    ("Năng lượng",         "nang-luong"),
    ("Nông nghiệp số",     "nong-nghiep-so"),
    ("Hướng dẫn kỹ thuật", "huong-dan-ky-thuat"),
    ("Tin tức ngành",      "tin-tuc-nganh"),
    ("Case Study",         "case-study"),
]

POST_TITLES = {
    "article": [
        "Giao thức Modbus RTU: Hướng dẫn kết nối cảm biến RS485 với PLC",
        "So sánh LoRaWAN vs NB-IoT cho ứng dụng giám sát nông nghiệp",
        "Tối ưu hoá băng thông MQTT cho hệ thống IoT quy mô lớn",
        "Cảm biến pH công nghiệp: Nguyên lý hoạt động và cách hiệu chỉnh",
        "Bảo trì dự đoán (Predictive Maintenance) với Machine Learning",
        "Thiết kế hệ thống SCADA hiện đại trên nền tảng Web",
        "Tích hợp OPC-UA với hệ thống ERP nhà máy",
        "Edge Computing trong công nghiệp: Khi nào nên xử lý tại chỗ?",
        "Chuẩn giao tiếp 4-20mA: Tại sao vẫn phổ biến sau 50 năm?",
        "Hướng dẫn lập trình PLC Siemens S7-1200 từ cơ bản đến nâng cao",
    ],
    "news": [
        "Xu hướng IoT công nghiệp 2025: Những điểm nổi bật cần biết",
        "Chính phủ đẩy mạnh hỗ trợ chuyển đổi số cho doanh nghiệp vừa và nhỏ",
        "Triển lãm Automation Expo 2025: Điểm mặt công nghệ mới nhất",
        "Việt Nam vươn lên top 10 thị trường IoT tăng trưởng nhanh Đông Nam Á",
        "Cảnh báo: Lỗ hổng bảo mật trong gateway công nghiệp phổ biến",
        "Siemens ra mắt dòng PLC thế hệ mới tích hợp AI tại chỗ",
    ],
    "case_study": [
        "Case Study: Giám sát 500 ao nuôi tôm tại Cà Mau bằng IoT",
        "Case Study: Tối ưu tiêu thụ điện nhà máy may mặc giảm 28%",
        "Case Study: Hệ thống tưới tiêu thông minh cho trang trại dưa lưới",
        "Case Study: Bảo trì dự đoán giúp nhà máy xi măng giảm 60% downtime",
        "Case Study: Giám sát chất lượng không khí 50 trạm đo tại TP.HCM",
    ],
    "guide": [
        "Hướng dẫn cài đặt và cấu hình Gateway LoRaWAN từ A đến Z",
        "Hướng dẫn kết nối cảm biến nhiệt độ PT100 với bộ chuyển đổi 4-20mA",
        "Hướng dẫn xây dựng dashboard giám sát realtime với Grafana + InfluxDB",
        "Hướng dẫn lập trình Modbus TCP với Python: từ cơ bản đến thực chiến",
        "Hướng dẫn chọn cảm biến DO phù hợp cho hệ thống nuôi trồng thủy sản",
        "Hướng dẫn thiết kế tủ điện điều khiển IoT đạt chuẩn IP54",
    ],
}

TAGS_POOL = [
    "PLC", "IoT", "Cảm biến", "Modbus", "MQTT", "RS485",
    "LoRaWAN", "4G", "Automation", "SCADA", "Gateway",
    "Python", "Raspberry Pi", "Arduino", "Edge Computing",
    "AI", "Machine Learning", "Predictive Maintenance",
    "Nông nghiệp thông minh", "Nhà máy thông minh",
    "Năng lượng tái tạo", "Điện mặt trời", "Biến tần",
    "HMI", "OPC-UA", "Datalogger", "Cloud", "Dashboard",
]

SHORT_DESCRIPTIONS = [
    "Bài viết phân tích chuyên sâu, kèm ví dụ thực tế và code mẫu giúp bạn triển khai ngay.",
    "Hướng dẫn từng bước với hình ảnh minh hoạ rõ ràng, phù hợp cho cả người mới bắt đầu.",
    "Tổng hợp kinh nghiệm thực chiến từ hàng trăm dự án IoT công nghiệp tại Việt Nam.",
    "So sánh chi tiết ưu nhược điểm, giúp bạn đưa ra lựa chọn phù hợp nhất cho dự án.",
    "Case study thực tế với số liệu cụ thể về ROI, tiết kiệm chi phí và tăng hiệu suất.",
    "Cập nhật xu hướng mới nhất trong ngành tự động hoá và công nghiệp 4.0.",
    "Phân tích kỹ thuật chuyên sâu kết hợp thực tiễn triển khai tại doanh nghiệp Việt Nam.",
    "Chia sẻ bài học kinh nghiệm và những sai lầm phổ biến cần tránh khi triển khai hệ thống IoT.",
]

CONTENT_BLOCKS = [
    "<h2>Giới thiệu</h2>\n<p>{p1}</p>",
    "<h2>Tổng quan kỹ thuật</h2>\n<p>{p2}</p>\n<ul>{ul}</ul>",
    "<h2>Hướng dẫn thực hiện</h2>\n<p>{p3}</p>",
    "<h2>Ưu điểm và lưu ý</h2>\n<p>{p4}</p>",
    "<h2>Kết luận</h2>\n<p>{p5}</p>",
]

HIGHLIGHTS = [
    "Tiết kiệm 30% chi phí vận hành so với phương pháp truyền thống.",
    "Giảm downtime thiết bị xuống dưới 1% nhờ bảo trì dự đoán.",
    "Dashboard realtime giúp quản lý nắm bắt tình hình mọi lúc, mọi nơi.",
    "Hệ thống tự động cảnh báo qua SMS/email khi thông số vượt ngưỡng.",
    "Tích hợp dễ dàng với hệ thống ERP/MES hiện có của nhà máy.",
    "ROI dương sau 14-18 tháng triển khai dựa trên số liệu thực tế.",
]


# ─────────────────────────────────────────────────────────────────────────────
# BlogCategory Factory
# ─────────────────────────────────────────────────────────────────────────────

class BlogCategoryFactory(DjangoModelFactory):
    class Meta:
        model = BlogCategory
        django_get_or_create = ("slug",)

    name = factory.Iterator(
        [name for name, _ in BLOG_CATEGORIES],
        cycle=True,
    )
    slug = factory.LazyAttribute(
        lambda o: slugify(o.name) or f"blog-cat-{fake.uuid4()[:8]}"
    )
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    is_active   = True
    sort_order  = factory.Sequence(lambda n: n)


# ─────────────────────────────────────────────────────────────────────────────
# Post Factory
# ─────────────────────────────────────────────────────────────────────────────

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ("slug",)

    # ── Loại bài viết ──────────────────────────────────────────────────────
    post_type = factory.fuzzy.FuzzyChoice(
        [Post.POST_TYPE_ARTICLE] * 5   # bài viết kỹ thuật chiếm nhiều nhất
        + [Post.POST_TYPE_NEWS] * 2
        + [Post.POST_TYPE_GUIDE] * 2
        + [Post.POST_TYPE_CASE]
    )

    # ── Tiêu đề: lấy từ pool theo post_type ──────────────────────────────
    title = factory.LazyAttribute(
        lambda o: random.choice(
            POST_TITLES.get(o.post_type, POST_TITLES["article"])
        ) + f" [{fake.bothify('??##').upper()}]"
        # Thêm suffix ngẫu nhiên để tránh unique slug conflict
    )

    slug = factory.LazyAttribute(
        lambda o: slugify(o.title)[:200] or f"post-{fake.uuid4()[:8]}"
    )

    # ── Quan hệ ────────────────────────────────────────────────────────────
    category = factory.SubFactory(BlogCategoryFactory)
    author   = None  # để None để không phụ thuộc CustomerFactory; override khi cần

    # ── Media ──────────────────────────────────────────────────────────────
    thumbnail = factory.django.ImageField(
        filename=factory.LazyFunction(lambda: f"blog-{fake.uuid4()[:8]}.jpg"),
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "green", "orange", "red", "purple", "teal"])
        ),
    )

    # ── Nội dung ──────────────────────────────────────────────────────────
    short_description = factory.LazyAttribute(
        lambda o: random.choice(SHORT_DESCRIPTIONS)
    )

    content = factory.LazyFunction(
        lambda: "\n\n".join([
            f"<h2>Giới thiệu</h2><p>{fake.paragraph(nb_sentences=4)}</p>",
            f"<h2>Tổng quan kỹ thuật</h2><p>{fake.paragraph(nb_sentences=5)}</p>"
            f"<ul>" + "".join(f"<li>{fake.sentence()}</li>" for _ in range(4)) + "</ul>",
            f"<h2>Hướng dẫn thực hiện</h2><p>{fake.paragraph(nb_sentences=5)}</p>",
            f"<blockquote><p>{random.choice(HIGHLIGHTS)}</p></blockquote>",
            f"<h2>Ưu điểm và lưu ý thực tế</h2><p>{fake.paragraph(nb_sentences=4)}</p>",
            f"<h2>Kết luận</h2><p>{fake.paragraph(nb_sentences=3)}</p>",
        ])
    )

    read_time = factory.LazyFunction(lambda: random.randint(3, 15))

    # ── Tags ───────────────────────────────────────────────────────────────
    tags = factory.LazyFunction(
        lambda: ", ".join(random.sample(TAGS_POOL, random.randint(3, 6)))
    )

    # ── Analytics ─────────────────────────────────────────────────────────
    view_count = factory.LazyFunction(lambda: random.randint(0, 5000))

    # ── PublishableModel fields ────────────────────────────────────────────
    status       = "published"
    is_featured  = factory.LazyFunction(lambda: random.random() < 0.2)
    published_at = factory.LazyFunction(
        lambda: fake.date_time_between(
            start_date="-2y",
            end_date="now",
            tzinfo=timezone.get_current_timezone(),
        )
    )
    sort_order = factory.Sequence(lambda n: n)

    # ── SEO ────────────────────────────────────────────────────────────────
    meta_title       = factory.LazyAttribute(lambda o: o.title[:70])
    meta_description = factory.LazyAttribute(lambda o: o.short_description[:160])

    # ── Post generators ────────────────────────────────────────────────────

    @factory.post_generation
    def with_related_products(obj, create, extracted, **kwargs):
        """
        Gắn sản phẩm liên quan. Truyền số lượng hoặc list Product instances.

        Ví dụ:
            PostFactory(with_related_products=3)
            PostFactory(with_related_products=[p1, p2])
        """
        if not create:
            return
        if extracted is None:
            return

        if isinstance(extracted, int):
            try:
                from apps.products.models import Product
                products = list(
                    Product.objects.filter(status="published")
                    .order_by("?")[:extracted]
                )
                if products:
                    obj.related_products.set(products)
            except Exception:
                pass
        elif hasattr(extracted, "__iter__"):
            obj.related_products.set(list(extracted))

    @factory.post_generation
    def with_related_solutions(obj, create, extracted, **kwargs):
        """
        Gắn giải pháp liên quan. Truyền số lượng hoặc list Solution instances.

        Ví dụ:
            PostFactory(with_related_solutions=2)
        """
        if not create:
            return
        if extracted is None:
            return

        if isinstance(extracted, int):
            try:
                from apps.solutions.models import Solution
                solutions = list(
                    Solution.objects.filter(status="published")
                    .order_by("?")[:extracted]
                )
                if solutions:
                    obj.related_solutions.set(solutions)
            except Exception:
                pass
        elif hasattr(extracted, "__iter__"):
            obj.related_solutions.set(list(extracted))

    @classmethod
    def _create_with_author(cls, **kwargs):
        """
        Helper tạo Post có author (Customer).
        Ví dụ: PostFactory._create_with_author(post_type='guide')
        """
        try:
            from apps.customers.models import Customer
            author = Customer.objects.filter(is_staff=True).order_by("?").first()
            if not author:
                author = Customer.objects.order_by("?").first()
            kwargs.setdefault("author", author)
        except Exception:
            pass
        return cls.create(**kwargs)