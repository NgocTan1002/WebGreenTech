"""
apps/products/factories.py
--------------------------
Factory Boy factories cho toàn bộ models của products app.
Dùng để seed demo data hoặc viết tests.

Cài đặt:
    pip install factory-boy Pillow faker

Sử dụng nhanh:
    from apps.products.factories import ProductFactory
    ProductFactory.create_batch(20)
"""

import io
import random
from decimal import Decimal

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory, ImageField
from django.utils.text import slugify
from faker import Faker

from apps.categories.models import Category, Brand
from apps.products.models import (
    Product,
    ProductImage,
    ProductSpecification,
    ProductDocument,
    RelatedProduct,
)

fake = Faker("vi_VN")

# ─────────────────────────────────────────────────────────────────────────────
# Dữ liệu mẫu IoT / công nghiệp
# ─────────────────────────────────────────────────────────────────────────────

PRODUCT_NAMES = [
    "Cảm biến nhiệt độ PT100",
    "Cảm biến độ ẩm SHT31",
    "Cảm biến pH công nghiệp",
    "Cảm biến DO hoà tan",
    "Cảm biến lưu lượng điện từ",
    "Cảm biến áp suất 4-20mA",
    "Cảm biến mực nước siêu âm",
    "Cảm biến CO2 NDIR",
    "Cảm biến rung động MEMS",
    "Cảm biến khí NH3 công nghiệp",
    "Gateway IoT 4G LTE RS485",
    "Gateway Modbus TCP/RTU",
    "Gateway LoRaWAN Class A/C",
    "Gateway MQTT Ethernet",
    "Bộ thu thập dữ liệu 8 kênh",
    "Datalogger 16 kênh analog",
    "Bộ điều khiển PLC Micro",
    "PLC 32 I/O Modbus RTU",
    "Màn hình HMI 7 inch cảm ứng",
    "Màn hình HMI 10 inch công nghiệp",
    "Biến tần 1.5kW 3 pha",
    "Biến tần 5.5kW Vector",
    "Relay nhiệt bảo vệ motor",
    "Bộ chuyển đổi RS232/RS485",
    "Modem 4G công nghiệp",
    "Bộ lưu điện UPS 1000VA",
    "Nguồn tổ ong 24VDC 5A",
    "Nguồn switching 48VDC 10A",
    "Tủ điện điều khiển IoT",
    "Antenna LoRa 915MHz",
]

BRANDS_DATA = [
    ("Siemens",     "siemens"),
    ("Schneider",   "schneider"),
    ("Omron",       "omron"),
    ("Endress+Hauser", "endress-hauser"),
    ("Yokogawa",    "yokogawa"),
    ("WEG",         "weg"),
    ("Advantech",   "advantech"),
    ("Weidmuller",  "weidmuller"),
    ("Phoenix Contact", "phoenix-contact"),
    ("Autonics",    "autonics"),
]

CATEGORIES_DATA = [
    ("Cảm biến",           "cam-bien",        None),
    ("Gateway & Router",   "gateway",          None),
    ("Datalogger",         "datalogger",       None),
    ("PLC & HMI",          "plc-hmi",          None),
    ("Biến tần & Drive",   "bien-tan",         None),
    ("Nguồn công nghiệp",  "nguon-cong-nghiep",None),
    # Sub-categories
    ("Cảm biến nhiệt độ",  "cam-bien-nhiet-do", "cam-bien"),
    ("Cảm biến khí",       "cam-bien-khi",      "cam-bien"),
    ("Cảm biến nước",      "cam-bien-nuoc",     "cam-bien"),
]

SPEC_GROUPS = {
    "Thông số điện": [
        ("Điện áp cấp", ["12VDC", "24VDC", "220VAC", "110VAC"]),
        ("Dòng tiêu thụ", ["50mA", "100mA", "200mA", "500mA"]),
        ("Ngõ ra", ["4-20mA", "0-10V", "RS485", "Modbus RTU"]),
    ],
    "Thông số đo": [
        ("Dải đo", ["-40~125°C", "0~14 pH", "0~100% RH", "0~10 bar"]),
        ("Độ chính xác", ["±0.1°C", "±0.5%", "±1%", "±2%"]),
        ("Tốc độ lấy mẫu", ["1 Hz", "10 Hz", "100 Hz", "1 kHz"]),
    ],
    "Môi trường": [
        ("Cấp bảo vệ", ["IP65", "IP67", "IP68", "NEMA4X"]),
        ("Nhiệt độ hoạt động", ["-20~70°C", "-40~85°C", "0~50°C"]),
        ("Độ ẩm", ["0~95% RH", "5~90% RH (không đọng sương)"]),
    ],
    "Kết nối": [
        ("Giao thức", ["Modbus RTU", "MQTT", "REST API", "LoRaWAN"]),
        ("Cổng vật lý", ["RS485 2-wire", "Ethernet RJ45", "4G LTE", "Wi-Fi 2.4GHz"]),
    ],
}

HIGHLIGHTS_POOL = [
    "Chuẩn IP67 — hoạt động dưới nước",
    "Giao tiếp Modbus RTU/TCP",
    "Hỗ trợ MQTT và REST API",
    "Nguồn 9~36VDC wide range",
    "Cấu hình qua web browser",
    "Chứng nhận CE / RoHS",
    "Vỏ inox 316L chống ăn mòn",
    "Cáp kết nối M12 chống nước",
    "Hiệu chỉnh tự động (auto-calibration)",
    "Màn hình LCD tích hợp",
    "PoE 802.3af hỗ trợ",
    "Bộ nhớ nội 8GB lưu dữ liệu offline",
    "Bảo hành 24 tháng",
    "Made in Germany",
]

DOC_TITLES = [
    ("Datasheet",                    "datasheet"),
    ("Hướng dẫn cài đặt nhanh",     "manual"),
    ("Hướng dẫn sử dụng đầy đủ",    "manual"),
    ("Bản vẽ kích thước (DWG)",      "drawing"),
    ("Chứng nhận CE",                "certification"),
    ("Chứng nhận RoHS",              "certification"),
    ("Driver & Phần mềm cấu hình",   "software"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Helper: tạo ảnh placeholder bằng Pillow (không cần file thật)
# ─────────────────────────────────────────────────────────────────────────────

def _make_placeholder_image(width=400, height=400, color=None):
    """Trả về BytesIO chứa ảnh JPEG placeholder."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise ImportError("Cài Pillow: pip install Pillow")

    if color is None:
        color = random.choice([
            (99, 102, 241),   # indigo
            (16, 185, 129),   # emerald
            (245, 158, 11),   # amber
            (59, 130, 246),   # blue
            (139, 92, 246),   # violet
        ])

    img = Image.new("RGB", (width, height), color=(30, 41, 59))  # slate-800
    draw = ImageDraw.Draw(img)

    # Hình chữ nhật màu ở giữa
    margin = 60
    draw.rectangle(
        [margin, margin, width - margin, height - margin],
        fill=color,
        outline=(255, 255, 255, 40),
        width=2,
    )

    # Text đơn giản
    text = f"{width}×{height}"
    try:
        bbox = draw.textbbox((0, 0), text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(
            ((width - tw) // 2, (height - th) // 2),
            text,
            fill=(255, 255, 255),
        )
    except Exception:
        pass

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# Category Factory
# ─────────────────────────────────────────────────────────────────────────────

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("slug",)

    name       = factory.Sequence(lambda n: f"Danh mục {n}")
    slug       = factory.LazyAttribute(lambda o: slugify(o.name) or f"category-{fake.uuid4()[:8]}")
    # Thêm các trường khác nếu Category có (description, parent...)


# ─────────────────────────────────────────────────────────────────────────────
# Brand Factory
# ─────────────────────────────────────────────────────────────────────────────

class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ("slug",)

    name = factory.Sequence(lambda n: f"Brand {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name) or f"brand-{fake.uuid4()[:8]}")


# ─────────────────────────────────────────────────────────────────────────────
# Product Factory
# ─────────────────────────────────────────────────────────────────────────────

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ("sku",)

    # Identity
    name = factory.LazyFunction(
        lambda: random.choice(PRODUCT_NAMES) + f" — {fake.bothify('??##').upper()}"
    )
    sku  = factory.Sequence(lambda n: f"SKU-{n:05d}")
    part_number = factory.LazyFunction(
        lambda: fake.bothify("???-####-??").upper()
    )

    # Relationships
    category = factory.SubFactory(CategoryFactory)
    brand    = factory.SubFactory(BrandFactory)

    # Pricing
    pricing_type = factory.fuzzy.FuzzyChoice(
        [Product.PRICING_FIXED, Product.PRICING_FIXED,   # fixed xuất hiện nhiều hơn
         Product.PRICING_FIXED, Product.PRICING_QUOTE,
         Product.PRICING_CONTACT]
    )
    price = factory.LazyAttribute(
        lambda o: (
            Decimal(random.choice([
                490000, 990000, 1490000, 1990000,
                2500000, 4500000, 6900000, 9900000,
                15000000, 25000000, 45000000,
            ]))
            if o.pricing_type == Product.PRICING_FIXED else None
        )
    )
    sale_price = factory.LazyAttribute(
        lambda o: (
            o.price * Decimal("0.85")
            if o.pricing_type == Product.PRICING_FIXED and random.random() < 0.3
            else None
        )
    )
    min_order_qty = factory.fuzzy.FuzzyChoice([1, 1, 1, 2, 5, 10])

    # Stock
    stock_status   = factory.fuzzy.FuzzyChoice([
        Product.STOCK_IN, Product.STOCK_IN, Product.STOCK_IN,
        Product.STOCK_LOW, Product.STOCK_OUT,
    ])
    stock_quantity = factory.LazyAttribute(
        lambda o: (
            random.randint(10, 500) if o.stock_status == Product.STOCK_IN
            else random.randint(1, 9)  if o.stock_status == Product.STOCK_LOW
            else 0
        )
    )

    # Thumbnail — tạo ảnh placeholder thật sự
    thumbnail = factory.django.ImageField(
        filename=factory.LazyFunction(lambda: f"{fake.uuid4()[:8]}.jpg"),
    )

    # Content
    short_description = factory.LazyFunction(
        lambda: fake.paragraph(nb_sentences=2)
    )
    description = factory.LazyFunction(
        lambda: "\n\n".join([
            f"<h2>{fake.sentence(nb_words=5)}</h2>",
            f"<p>{fake.paragraph(nb_sentences=4)}</p>",
            "<ul>" + "".join(f"<li>{h}</li>" for h in random.sample(HIGHLIGHTS_POOL, 4)) + "</ul>",
            f"<p>{fake.paragraph(nb_sentences=3)}</p>",
        ])
    )
    highlights = factory.LazyFunction(
        lambda: random.sample(HIGHLIGHTS_POOL, random.randint(3, 6))
    )

    # Physical
    weight     = factory.LazyFunction(lambda: round(random.uniform(0.1, 5.0), 3))
    dim_length = factory.LazyFunction(lambda: round(random.uniform(50, 300), 1))
    dim_width  = factory.LazyFunction(lambda: round(random.uniform(30, 200), 1))
    dim_height = factory.LazyFunction(lambda: round(random.uniform(20, 150), 1))

    # Flags
    is_new        = factory.LazyFunction(lambda: random.random() < 0.25)
    is_bestseller = factory.LazyFunction(lambda: random.random() < 0.15)
    is_featured   = factory.LazyFunction(lambda: random.random() < 0.20)
    requires_quote = factory.LazyAttribute(
        lambda o: o.pricing_type == Product.PRICING_QUOTE
    )

    # PublishableModel — published by default cho demo
    status = "published"

    # SEO
    meta_title       = factory.LazyAttribute(lambda o: o.name[:70])
    meta_description = factory.LazyAttribute(lambda o: o.short_description[:160])

    # Slug
    slug = factory.LazyAttribute(
        lambda o: slugify(o.name)[:80] or f"product-{fake.uuid4()[:8]}"
    )

    @factory.post_generation
    def with_specs(obj, create, extracted, **kwargs):
        """Tự động tạo specifications sau khi product được tạo."""
        if not create:
            return
        count = extracted if extracted is not None else random.randint(2, 4)
        for group_name, specs in list(SPEC_GROUPS.items())[:count]:
            for key, values in specs:
                ProductSpecification.objects.create(
                    product=obj,
                    group=group_name,
                    key=key,
                    value=random.choice(values),
                )

    @factory.post_generation
    def with_images(obj, create, extracted, **kwargs):
        """Tạo thêm gallery images."""
        if not create:
            return
        count = extracted if extracted is not None else random.randint(0, 3)
        for i in range(count):
            ProductImageFactory(product=obj, is_primary=(i == 0))

    @factory.post_generation
    def with_documents(obj, create, extracted, **kwargs):
        """Tạo tài liệu đính kèm."""
        if not create:
            return
        count = extracted if extracted is not None else random.randint(1, 3)
        chosen = random.sample(DOC_TITLES, min(count, len(DOC_TITLES)))
        for title, doc_type in chosen:
            ProductDocumentFactory(product=obj, title=title, doc_type=doc_type)


# ─────────────────────────────────────────────────────────────────────────────
# ProductImage Factory
# ─────────────────────────────────────────────────────────────────────────────

class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product    = factory.SubFactory(ProductFactory)
    image      = factory.django.ImageField(
        filename=factory.Sequence(lambda n: f"gallery_{n}.jpg"),
        color=factory.LazyFunction(lambda: random.choice([
            "blue", "green", "orange", "red", "purple"
        ])),
    )
    alt_text   = factory.LazyAttribute(lambda o: o.product.name)
    is_primary = False
    sort_order = factory.Sequence(lambda n: n)


# ─────────────────────────────────────────────────────────────────────────────
# ProductSpecification Factory
# ─────────────────────────────────────────────────────────────────────────────

class ProductSpecificationFactory(DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product    = factory.SubFactory(ProductFactory)
    group      = factory.fuzzy.FuzzyChoice(list(SPEC_GROUPS.keys()))
    key        = factory.LazyFunction(lambda: fake.word().capitalize())
    value      = factory.LazyFunction(lambda: fake.bothify("##??").upper())
    unit       = factory.fuzzy.FuzzyChoice(["V", "A", "°C", "mA", "Hz", "mm", "kg", ""])
    sort_order = factory.Sequence(lambda n: n)


# ─────────────────────────────────────────────────────────────────────────────
# ProductDocument Factory
# ─────────────────────────────────────────────────────────────────────────────

class ProductDocumentFactory(DjangoModelFactory):
    class Meta:
        model = ProductDocument

    product  = factory.SubFactory(ProductFactory)
    title    = factory.LazyFunction(lambda: random.choice(DOC_TITLES)[0])
    doc_type = factory.LazyFunction(lambda: random.choice(DOC_TITLES)[1])
    file = factory.django.FileField(
        filename=factory.Sequence(lambda n: f"doc_{n}.pdf"),
        data=b"%PDF-1.4 fake pdf content for demo",
    )
    file_size = factory.LazyFunction(lambda: random.randint(100_000, 5_000_000))
    sort_order = factory.Sequence(lambda n: n)


# ─────────────────────────────────────────────────────────────────────────────
# RelatedProduct Factory
# ─────────────────────────────────────────────────────────────────────────────

class RelatedProductFactory(DjangoModelFactory):
    class Meta:
        model = RelatedProduct

    product       = factory.SubFactory(ProductFactory)
    related       = factory.SubFactory(ProductFactory)
    relation_type = factory.fuzzy.FuzzyChoice([
        RelatedProduct.RELATION_ACCESSORY,
        RelatedProduct.RELATION_COMPATIBLE,
        RelatedProduct.RELATION_ALTERNATIVE,
    ])
    sort_order = factory.Sequence(lambda n: n)