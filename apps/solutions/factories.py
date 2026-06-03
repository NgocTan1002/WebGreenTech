"""
apps/solutions/factories.py
----------------------------
Factory Boy factories cho toàn bộ models của solutions app.
Dùng để seed demo data hoặc viết tests.

Sử dụng nhanh:
    from apps.solutions.factories import SolutionFactory
    SolutionFactory.create_batch(5)
"""

import io
import random

import factory
from factory.django import DjangoModelFactory, ImageField
from django.utils.text import slugify
from faker import Faker

from apps.solutions.models import (
    SolutionCategory,
    Solution,
    SolutionProduct,
    ArchitectureBlock,
    WorkflowStep,
    CustomerCase,
)

fake = Faker("vi_VN")

# ─────────────────────────────────────────────────────────────────────────────
# Dữ liệu mẫu IoT / công nghiệp
# ─────────────────────────────────────────────────────────────────────────────

SOLUTION_CATEGORIES_DATA = [
    ("Nông nghiệp thông minh",    "nong-nghiep-thong-minh"),
    ("Giám sát nhà máy",          "giam-sat-nha-may"),
    ("Quản lý năng lượng",        "quan-ly-nang-luong"),
    ("Hạ tầng thông minh",        "ha-tang-thong-minh"),
    ("Môi trường & Nước",         "moi-truong-nuoc"),
    ("Hậu cần & Kho bãi",         "hau-can-kho-bai"),
]

SOLUTION_TITLES = [
    ("Giám sát nhà kính thông minh",        "giam-sat-nha-kinh-thong-minh",        "nong-nghiep-thong-minh"),
    ("Hệ thống tưới tiêu tự động",          "tuoi-tieu-tu-dong",                   "nong-nghiep-thong-minh"),
    ("Quan trắc chất lượng nước ao nuôi",   "quan-trac-chat-luong-nuoc-ao-nuoi",   "nong-nghiep-thong-minh"),
    ("Giám sát toàn diện dây chuyền SX",    "giam-sat-day-chuyen-san-xuat",        "giam-sat-nha-may"),
    ("Bảo trì dự đoán thiết bị công nghiệp","bao-tri-du-doan-thiet-bi",            "giam-sat-nha-may"),
    ("Kiểm soát chất lượng realtime",       "kiem-soat-chat-luong-realtime",       "giam-sat-nha-may"),
    ("Quản lý tiêu thụ điện nhà máy",       "quan-ly-tieu-thu-dien-nha-may",       "quan-ly-nang-luong"),
    ("Tối ưu hóa năng lượng tòa nhà",       "toi-uu-nang-luong-toa-nha",           "quan-ly-nang-luong"),
    ("Giám sát điện mặt trời phân tán",     "giam-sat-dien-mat-troi-phan-tan",     "quan-ly-nang-luong"),
    ("Quản lý hạ tầng đô thị thông minh",   "ha-tang-do-thi-thong-minh",           "ha-tang-thong-minh"),
    ("Giám sát chất lượng không khí",       "giam-sat-chat-luong-khong-khi",       "moi-truong-nuoc"),
    ("Quan trắc nước thải nhà máy",         "quan-trac-nuoc-thai-nha-may",         "moi-truong-nuoc"),
    ("Theo dõi hàng hóa trong kho lạnh",    "theo-doi-hang-hoa-kho-lanh",          "hau-can-kho-bai"),
    ("Quản lý vận chuyển & GPS tracking",   "quan-ly-van-chuyen-gps",              "hau-can-kho-bai"),
]

SUBTITLES = [
    "Giải pháp IoT end-to-end từ cảm biến đến dashboard",
    "Tối ưu vận hành, giảm chi phí, tăng năng suất",
    "Kết nối dữ liệu realtime, cảnh báo tức thì",
    "Nền tảng giám sát & điều khiển tập trung",
    "Tự động hóa thông minh với AI & Machine Learning",
    "Hệ thống SCADA hiện đại trên nền tảng IoT",
    "Giải pháp toàn diện cho ngành công nghiệp 4.0",
]

PAIN_POINTS_POOL = [
    {"title": "Khó giám sát từ xa", "description": "Không có dữ liệu realtime, phải đến tận nơi kiểm tra."},
    {"title": "Chi phí vận hành cao", "description": "Lãng phí điện, nước, nguyên vật liệu do thiếu kiểm soát."},
    {"title": "Sự cố xảy ra bất ngờ", "description": "Thiết bị hỏng đột ngột gây dừng sản xuất, thiệt hại lớn."},
    {"title": "Dữ liệu phân tán, khó tổng hợp", "description": "Thông tin nằm rải rác, không có báo cáo thống nhất."},
    {"title": "Phụ thuộc nhân công cao", "description": "Cần nhiều người ghi chép, kiểm tra thủ công tốn thời gian."},
    {"title": "Thiếu cảnh báo sớm", "description": "Không có hệ thống thông báo khi thông số vượt ngưỡng."},
    {"title": "Khó mở rộng quy mô", "description": "Hệ thống cũ không linh hoạt khi mở rộng nhà máy hoặc trang trại."},
    {"title": "Tuân thủ quy định môi trường", "description": "Khó chứng minh tuân thủ do thiếu dữ liệu lịch sử có hệ thống."},
]

BENEFITS_POOL = [
    {"title": "Giảm chi phí vận hành", "metric": "30%", "description": "Tối ưu hóa sử dụng điện, nước và nguyên vật liệu."},
    {"title": "Tăng năng suất", "metric": "25%", "description": "Tự động hóa quy trình, giảm công việc thủ công."},
    {"title": "Phát hiện sự cố sớm", "metric": "90%", "description": "Cảnh báo tức thì, xử lý trước khi thiệt hại xảy ra."},
    {"title": "Uptime thiết bị", "metric": "99.5%", "description": "Bảo trì dự đoán giúp thiết bị luôn hoạt động ổn định."},
    {"title": "Tiết kiệm nhân lực", "metric": "40%", "description": "Giảm tải công việc giám sát và ghi chép thủ công."},
    {"title": "ROI nhanh chóng", "metric": "18 tháng", "description": "Hoàn vốn đầu tư trong vòng 12-18 tháng triển khai."},
    {"title": "Dữ liệu lịch sử đầy đủ", "metric": "100%", "description": "Lưu trữ toàn bộ dữ liệu phục vụ phân tích và báo cáo."},
    {"title": "Giảm tiêu thụ năng lượng", "metric": "20%", "description": "Tối ưu lịch vận hành thiết bị theo nhu cầu thực tế."},
]

WORKFLOW_STEPS_POOL = [
    (1, "Thu thập dữ liệu",       "Cảm biến IoT đo lường thông số thực tế tại hiện trường 24/7."),
    (2, "Truyền dữ liệu",         "Gateway tổng hợp và gửi dữ liệu lên cloud qua 4G/LoRa/Ethernet."),
    (3, "Xử lý & lưu trữ",        "Platform cloud xử lý, chuẩn hóa và lưu trữ dữ liệu an toàn."),
    (4, "Phân tích & cảnh báo",   "AI phân tích xu hướng, phát hiện bất thường và gửi cảnh báo."),
    (5, "Trực quan hóa",          "Dashboard realtime hiển thị KPI, biểu đồ và báo cáo tự động."),
    (6, "Điều khiển tự động",     "Hệ thống tự động điều chỉnh thiết bị theo quy tắc đã định."),
]

ARCHITECTURE_TITLES = [
    ("Lớp cảm biến hiện trường",  "Các cảm biến IoT công nghiệp kết nối RS485/4-20mA đo lường trực tiếp."),
    ("Lớp Edge Gateway",          "Gateway thu thập, lọc và chuyển tiếp dữ liệu lên cloud."),
    ("Lớp truyền thông",          "Kết nối 4G LTE, LoRaWAN hoặc Ethernet tùy địa hình."),
    ("Lớp Cloud Platform",        "Hạ tầng cloud xử lý và lưu trữ dữ liệu quy mô lớn."),
    ("Lớp ứng dụng",              "Dashboard web/mobile, API tích hợp và hệ thống cảnh báo."),
]

COMPANIES = [
    ("Vinamilk",             "Chế biến thực phẩm",    "Việt Nam"),
    ("TH True Milk",         "Nông nghiệp công nghệ", "Việt Nam"),
    ("Hòa Phát Group",       "Thép & Công nghiệp",    "Việt Nam"),
    ("Nhà máy Samsung SEV",  "Điện tử",               "Hàn Quốc"),
    ("Lotte Mart",           "Bán lẻ & Hậu cần",      "Hàn Quốc"),
    ("Phúc Sinh Coffee",     "Nông nghiệp",            "Việt Nam"),
    ("Masan Consumer",       "Sản xuất FMCG",         "Việt Nam"),
    ("EVN HCMC",             "Điện lực",               "Việt Nam"),
]

TESTIMONIALS = [
    "Hệ thống giúp chúng tôi giảm 35% chi phí điện và phát hiện sự cố trước khi xảy ra.",
    "Dashboard realtime giúp ban quản lý nắm bắt tình hình sản xuất mọi lúc mọi nơi.",
    "Việc triển khai nhanh chóng, đội kỹ sư hỗ trợ tận tình. Chúng tôi rất hài lòng.",
    "ROI đạt được chỉ sau 14 tháng, vượt kỳ vọng ban đầu của chúng tôi.",
    "Giải pháp linh hoạt, dễ mở rộng khi chúng tôi phát triển thêm cơ sở mới.",
]


# ─────────────────────────────────────────────────────────────────────────────
# SolutionCategory Factory
# ─────────────────────────────────────────────────────────────────────────────

class SolutionCategoryFactory(DjangoModelFactory):
    class Meta:
        model = SolutionCategory
        django_get_or_create = ("slug",)

    name      = factory.Sequence(lambda n: f"Ngành {n}")
    slug      = factory.LazyAttribute(lambda o: slugify(o.name) or f"category-{fake.uuid4()[:8]}")
    is_active = True
    sort_order = factory.Sequence(lambda n: n)


# ─────────────────────────────────────────────────────────────────────────────
# Solution Factory
# ─────────────────────────────────────────────────────────────────────────────

class SolutionFactory(DjangoModelFactory):
    class Meta:
        model = Solution
        django_get_or_create = ("slug",)

    title             = factory.Sequence(lambda n: f"Giải pháp IoT {n:02d}")
    slug              = factory.LazyAttribute(lambda o: slugify(o.title) or f"solution-{fake.uuid4()[:8]}")
    subtitle          = factory.LazyFunction(lambda: random.choice(SUBTITLES))
    solution_category = factory.SubFactory(SolutionCategoryFactory)
    thumbnail         = factory.django.ImageField(
        filename=factory.LazyFunction(lambda: f"{fake.uuid4()[:8]}.jpg"),
    )
    short_description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    overview          = factory.LazyFunction(lambda: (
        f"<h2>Tổng quan giải pháp</h2>"
        f"<p>{fake.paragraph(nb_sentences=4)}</p>"
        f"<h3>Tại sao chọn chúng tôi?</h3>"
        f"<p>{fake.paragraph(nb_sentences=3)}</p>"
        f"<ul>"
        + "".join(f"<li>{fake.sentence()}</li>" for _ in range(4))
        + "</ul>"
    ))
    pain_points       = factory.LazyFunction(lambda: random.sample(PAIN_POINTS_POOL, random.randint(3, 5)))
    benefits          = factory.LazyFunction(lambda: random.sample(BENEFITS_POOL, random.randint(3, 5)))
    workflow_title    = factory.LazyFunction(lambda: "Quy trình hoạt động hệ thống")
    workflow_description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    cta_title         = factory.LazyFunction(lambda: random.choice([
        "Sẵn sàng triển khai giải pháp?",
        "Bắt đầu chuyển đổi số ngay hôm nay",
        "Tư vấn miễn phí với kỹ sư chuyên môn",
    ]))
    cta_primary_text  = "Đặt lịch demo miễn phí"
    cta_primary_url   = "/contact/demo/"
    cta_secondary_text = "Yêu cầu báo giá"
    cta_secondary_url  = "/orders/quote/"
    status            = "published"
    is_featured       = factory.LazyFunction(lambda: random.random() < 0.4)
    sort_order        = factory.Sequence(lambda n: n)
    view_count        = factory.LazyFunction(lambda: random.randint(0, 2000))

    # SEO
    meta_title        = factory.LazyAttribute(lambda o: o.title[:70])
    meta_description  = factory.LazyAttribute(lambda o: o.short_description[:160])

    @factory.post_generation
    def with_workflow_steps(obj, create, extracted, **kwargs):
        if not create:
            return
        count = extracted if extracted is not None else random.randint(4, 6)
        steps = WORKFLOW_STEPS_POOL[:count]
        for step_num, title, desc in steps:
            WorkflowStep.objects.create(
                solution=obj,
                step_number=step_num,
                title=title,
                description=desc,
                sort_order=step_num,
            )

    @factory.post_generation
    def with_architecture_blocks(obj, create, extracted, **kwargs):
        if not create:
            return
        count = extracted if extracted is not None else random.randint(2, 4)
        chosen = random.sample(ARCHITECTURE_TITLES, min(count, len(ARCHITECTURE_TITLES)))
        for i, (title, desc) in enumerate(chosen):
            ArchitectureBlock.objects.create(
                solution=obj,
                title=title,
                description=desc,
                sort_order=i + 1,
            )

    @factory.post_generation
    def with_customer_cases(obj, create, extracted, **kwargs):
        if not create:
            return
        count = extracted if extracted is not None else random.randint(1, 2)
        companies = random.sample(COMPANIES, min(count, len(COMPANIES)))
        for company_name, industry, country in companies:
            CustomerCase.objects.create(
                solution=obj,
                company_name=company_name,
                industry=industry,
                country=country,
                slug=slugify(f"{company_name}-{obj.slug}")[:200] or f"case-{fake.uuid4()[:8]}",
                challenge=fake.paragraph(nb_sentences=3),
                solution_applied=fake.paragraph(nb_sentences=3),
                results=[
                    {"metric": "Tiết kiệm chi phí", "value": str(random.randint(15, 40)), "unit": "%"},
                    {"metric": "Tăng năng suất",    "value": str(random.randint(10, 30)), "unit": "%"},
                    {"metric": "Thời gian ROI",      "value": str(random.randint(12, 24)), "unit": " tháng"},
                ],
                testimonial=random.choice(TESTIMONIALS),
                testimonial_author=f"{fake.first_name()} {fake.last_name()}",
                testimonial_title=random.choice(["Giám đốc sản xuất", "CTO", "Trưởng bộ phận kỹ thuật", "CEO"]),
                status="published",
                sort_order=random.randint(1, 10),
            )

    @factory.post_generation
    def with_products(obj, create, extracted, **kwargs):
        """Gắn sản phẩm vào solution — truyền danh sách Product instances."""
        if not create or not extracted:
            return
        for i, product in enumerate(extracted):
            SolutionProduct.objects.get_or_create(
                solution=obj,
                product=product,
                defaults={
                    "is_featured": i < 3,
                    "role_description": random.choice([
                        "Cảm biến chính đo lường hiện trường",
                        "Gateway truyền dữ liệu trung tâm",
                        "Bộ điều khiển và tự động hóa",
                        "Thiết bị thu thập và ghi dữ liệu",
                        "Module kết nối không dây",
                    ]),
                    "sort_order": i + 1,
                },
            )


# ─────────────────────────────────────────────────────────────────────────────
# WorkflowStep Factory (standalone)
# ─────────────────────────────────────────────────────────────────────────────

class WorkflowStepFactory(DjangoModelFactory):
    class Meta:
        model = WorkflowStep

    solution    = factory.SubFactory(SolutionFactory)
    step_number = factory.Sequence(lambda n: n + 1)
    title       = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    sort_order  = factory.SelfAttribute("step_number")


# ─────────────────────────────────────────────────────────────────────────────
# ArchitectureBlock Factory (standalone)
# ─────────────────────────────────────────────────────────────────────────────

class ArchitectureBlockFactory(DjangoModelFactory):
    class Meta:
        model = ArchitectureBlock

    solution    = factory.SubFactory(SolutionFactory)
    title       = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=2))
    sort_order  = factory.Sequence(lambda n: n)


# ─────────────────────────────────────────────────────────────────────────────
# CustomerCase Factory (standalone)
# ─────────────────────────────────────────────────────────────────────────────

class CustomerCaseFactory(DjangoModelFactory):
    class Meta:
        model = CustomerCase

    solution       = factory.SubFactory(SolutionFactory)
    company_name   = factory.LazyFunction(lambda: fake.company())
    industry       = factory.LazyFunction(lambda: random.choice([
        "Nông nghiệp", "Sản xuất", "Điện lực", "Thực phẩm & Đồ uống", "Hậu cần"
    ]))
    country        = "Việt Nam"
    slug           = factory.LazyAttribute(
        lambda o: slugify(o.company_name)[:200] or f"case-{fake.uuid4()[:8]}"
    )
    challenge      = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=3))
    solution_applied = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=3))
    results        = factory.LazyFunction(lambda: [
        {"metric": "Tiết kiệm chi phí", "value": str(random.randint(15, 40)), "unit": "%"},
        {"metric": "Tăng năng suất",    "value": str(random.randint(10, 30)), "unit": "%"},
    ])
    testimonial    = factory.LazyFunction(lambda: random.choice(TESTIMONIALS))
    testimonial_author = factory.LazyFunction(lambda: fake.name())
    testimonial_title  = factory.LazyFunction(lambda: random.choice([
        "Giám đốc sản xuất", "CTO", "Trưởng bộ phận kỹ thuật", "CEO",
    ]))
    status         = "published"
    sort_order     = factory.Sequence(lambda n: n)