from django.db import connection


def _call(func_name: str, params: list) -> list[dict]:
    sql = f"SELECT * FROM {func_name}({', '.join(['%s'] * len(params))})"
    with connection.cursor() as cur:
        cur.execute(sql, params)
        if cur.description is None:
            return []
        cols = [col.name for col in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def _call_one(func_name: str, params: list) -> dict | None:
    """Gọi function và trả về row đầu tiên hoặc None."""
    results = _call(func_name, params)
    return results[0] if results else None


def _call_void(func_name: str, params: list) -> None:
    """Gọi function không trả về giá trị (RETURNS VOID)."""
    sql = f"SELECT {func_name}({', '.join(['%s'] * len(params))})"
    with connection.cursor() as cur:
        cur.execute(sql, params)


# PRODUCTS

def get_products(
    category_id=None,
    brand_id=None,
    min_price=None,
    max_price=None,
    stock_only=False,
    search=None,
    sort_by="featured",
    limit=24,
    offset=0,
) -> tuple[list[dict], int]:
    """
    Trả về (danh_sach_san_pham, tong_so_luong).
    total_count nằm trong mỗi row — lấy từ row đầu tiên.
    """
    rows = _call("fn_get_products", [
        category_id, brand_id,
        min_price, max_price,
        stock_only, search,
        sort_by, limit, offset,
    ])
    total = rows[0]["total_count"] if rows else 0
    return rows, total


def get_product_detail(slug: str) -> dict | None:
    return _call_one("fn_get_product_detail", [slug])


def get_product_specs(product_id: int) -> list[dict]:
    return _call("fn_get_product_specs", [product_id])


def get_product_images(product_id: int) -> list[dict]:
    return _call("fn_get_product_images", [product_id])


def get_related_products(product_id: int, limit: int = 6) -> list[dict]:
    return _call("fn_get_related_products", [product_id, limit])


def increment_product_views(product_id: int) -> None:
    _call_void("fn_increment_product_views", [product_id])

# SOLUTIONS

def get_solutions(
    category_slug=None,
    limit=12,
    offset=0,
) -> tuple[list[dict], int]:
    rows = _call("fn_get_solutions", [category_slug, limit, offset])
    total = rows[0]["total_count"] if rows else 0
    return rows, total


def get_solution_detail(slug: str) -> dict | None:
    return _call_one("fn_get_solution_detail", [slug])


def get_solution_products(
    solution_id: int,
    featured_only: bool = False,
) -> list[dict]:
    return _call("fn_get_solution_products", [solution_id, featured_only])


def increment_solution_views(solution_id: int) -> None:
    _call_void("fn_increment_solution_views", [solution_id])

# CATEGORIES

def get_category_tree(active_only: bool = True) -> list[dict]:
    return _call("fn_get_category_tree", [active_only])


def count_products_in_category(category_id: int) -> int:
    row = _call_one("fn_count_products_in_category", [category_id])
    return row["fn_count_products_in_category"] if row else 0


def get_category_ancestors(category_id: int) -> list[dict]:
    return _call("fn_get_category_ancestors", [category_id])


# CART

def get_cart_detail(cart_id: str) -> list[dict]:
    return _call("fn_get_cart_detail", [cart_id])


def get_cart_summary(cart_id: str) -> dict:
    return _call_one("fn_get_cart_summary", [cart_id]) or {
        "total_items": 0,
        "subtotal": 0,
    }


def upsert_cart_item(
    cart_id: str,
    product_id: int,
    quantity: int,
    unit_price,
) -> dict:
    return _call_one("fn_upsert_cart_item", [
        cart_id, product_id, quantity, unit_price,
    ])


# ORDERS

def create_order_from_cart(
    cart_id: str,
    order_type: str,
    customer_id,
    email: str,
    first_name: str,
    last_name: str,
    company_name: str,
    phone: str,
    shipping_address: dict,
    notes: str = "",
) -> dict | None:
    import json
    return _call_one("fn_create_order_from_cart", [
        cart_id, order_type, customer_id,
        email, first_name, last_name,
        company_name, phone,
        json.dumps(shipping_address, ensure_ascii=False),
        notes,
    ])


def get_customer_orders(
    customer_id: int,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    return _call("fn_get_customer_orders", [customer_id, limit, offset])

# BLOG

def get_posts(
    category_slug=None,
    post_type=None,
    search=None,
    limit=12,
    offset=0,
) -> tuple[list[dict], int]:
    rows = _call("fn_get_posts", [
        category_slug, post_type, search, limit, offset,
    ])
    total = rows[0]["total_count"] if rows else 0
    return rows, total


def increment_post_views(post_id: int) -> None:
    _call_void("fn_increment_post_views", [post_id])

# SEARCH
def search_autocomplete(query: str, limit: int = 5) -> list[dict]:
    if not query or len(query) < 2:
        return []
    return _call("fn_search_autocomplete", [query, limit])