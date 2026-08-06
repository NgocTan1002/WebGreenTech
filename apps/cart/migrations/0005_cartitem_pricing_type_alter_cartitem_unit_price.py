from django.db import migrations, models


FORWARD_CART_DETAIL_SQL = """
CREATE FUNCTION public.fn_get_cart_detail(p_cart_id uuid)
RETURNS TABLE(
    item_id bigint,
    product_id bigint,
    product_name character varying,
    product_sku character varying,
    product_slug character varying,
    thumbnail character varying,
    stock_status character varying,
    quantity integer,
    pricing_type character varying,
    unit_price numeric,
    price_pending boolean,
    line_total numeric
)
LANGUAGE sql
STABLE
PARALLEL UNSAFE
AS $BODY$
    SELECT
        ci.id, p.id, p.name, p.sku, p.slug,
        p.thumbnail, p.stock_status,
        ci.quantity, ci.pricing_type, ci.unit_price,
        (ci.pricing_type <> 'fixed' OR ci.unit_price IS NULL) AS price_pending,
        CASE
            WHEN ci.pricing_type <> 'fixed' OR ci.unit_price IS NULL THEN NULL
            ELSE ci.quantity * ci.unit_price
        END AS line_total
    FROM cart_cartitem ci
    JOIN products_product p ON p.id = ci.product_id
    WHERE ci.cart_id = p_cart_id
    ORDER BY ci.created_at;
$BODY$;
"""


REVERSE_CART_DETAIL_SQL = """
CREATE FUNCTION public.fn_get_cart_detail(p_cart_id uuid)
RETURNS TABLE(
    item_id bigint,
    product_id bigint,
    product_name character varying,
    product_sku character varying,
    product_slug character varying,
    thumbnail character varying,
    stock_status character varying,
    quantity integer,
    unit_price numeric,
    line_total numeric
)
LANGUAGE sql
STABLE
PARALLEL UNSAFE
AS $BODY$
    SELECT
        ci.id, p.id, p.name, p.sku, p.slug,
        p.thumbnail, p.stock_status,
        ci.quantity, COALESCE(ci.unit_price, 0),
        ci.quantity * COALESCE(ci.unit_price, 0) AS line_total
    FROM cart_cartitem ci
    JOIN products_product p ON p.id = ci.product_id
    WHERE ci.cart_id = p_cart_id
    ORDER BY ci.created_at;
$BODY$;
"""


FORWARD_UPSERT_SQL = """
CREATE OR REPLACE FUNCTION public.fn_upsert_cart_item(
    p_cart_id uuid,
    p_product_id bigint,
    p_quantity integer,
    p_unit_price numeric
)
RETURNS TABLE(item_id bigint, quantity integer, created boolean)
LANGUAGE plpgsql
VOLATILE
PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_item_id BIGINT;
    v_quantity INT;
    v_created BOOLEAN := FALSE;
    v_pricing_type VARCHAR(20);
BEGIN
    SELECT CASE
        WHEN requires_quote OR pricing_type <> 'fixed' OR p_unit_price IS NULL THEN 'quote'
        ELSE 'fixed'
    END
    INTO v_pricing_type
    FROM products_product
    WHERE id = p_product_id;

    IF v_pricing_type IS NULL THEN
        RAISE EXCEPTION 'Sản phẩm không tồn tại.';
    END IF;

    SELECT id, cart_cartitem.quantity
    INTO v_item_id, v_quantity
    FROM cart_cartitem
    WHERE cart_id = p_cart_id AND product_id = p_product_id;

    IF v_item_id IS NULL THEN
        INSERT INTO cart_cartitem (
            cart_id, product_id, quantity, pricing_type, unit_price,
            created_at, updated_at
        ) VALUES (
            p_cart_id, p_product_id, p_quantity, v_pricing_type,
            CASE WHEN v_pricing_type = 'fixed' THEN p_unit_price ELSE NULL END,
            NOW(), NOW()
        )
        RETURNING id INTO v_item_id;
        v_quantity := p_quantity;
        v_created := TRUE;
    ELSE
        UPDATE cart_cartitem
        SET quantity = cart_cartitem.quantity + p_quantity,
            pricing_type = v_pricing_type,
            unit_price = CASE WHEN v_pricing_type = 'fixed' THEN p_unit_price ELSE NULL END,
            updated_at = NOW()
        WHERE id = v_item_id
        RETURNING cart_cartitem.quantity INTO v_quantity;
    END IF;

    RETURN QUERY SELECT v_item_id, v_quantity, v_created;
END;
$BODY$;
"""


REVERSE_UPSERT_SQL = """
CREATE OR REPLACE FUNCTION public.fn_upsert_cart_item(
    p_cart_id uuid,
    p_product_id bigint,
    p_quantity integer,
    p_unit_price numeric
)
RETURNS TABLE(item_id bigint, quantity integer, created boolean)
LANGUAGE plpgsql
VOLATILE
PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_item_id BIGINT;
    v_quantity INT;
    v_created BOOLEAN := FALSE;
BEGIN
    SELECT id, cart_cartitem.quantity
    INTO v_item_id, v_quantity
    FROM cart_cartitem
    WHERE cart_id = p_cart_id AND product_id = p_product_id;

    IF v_item_id IS NULL THEN
        INSERT INTO cart_cartitem (
            cart_id, product_id, quantity, unit_price, created_at, updated_at
        ) VALUES (
            p_cart_id, p_product_id, p_quantity, COALESCE(p_unit_price, 0), NOW(), NOW()
        )
        RETURNING id INTO v_item_id;
        v_quantity := p_quantity;
        v_created := TRUE;
    ELSE
        UPDATE cart_cartitem
        SET quantity = cart_cartitem.quantity + p_quantity,
            updated_at = NOW()
        WHERE id = v_item_id
        RETURNING cart_cartitem.quantity INTO v_quantity;
    END IF;

    RETURN QUERY SELECT v_item_id, v_quantity, v_created;
END;
$BODY$;
"""


def migrate_cart_prices(apps, schema_editor):
    schema_editor.execute("""
        UPDATE cart_cartitem AS ci
        SET
            pricing_type = CASE
                WHEN p.requires_quote THEN 'quote'
                ELSE p.pricing_type
            END,
            unit_price = CASE
                WHEN p.requires_quote OR p.pricing_type <> 'fixed' THEN NULL
                WHEN ci.unit_price = 0 AND p.price IS NULL THEN NULL
                ELSE ci.unit_price
            END
        FROM products_product AS p
        WHERE p.id = ci.product_id;
    """)


def reverse_cart_prices(apps, schema_editor):
    schema_editor.execute(
        "UPDATE cart_cartitem SET unit_price = 0 WHERE unit_price IS NULL;"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cart_options_alter_cartitem_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='pricing_type',
            field=models.CharField(
                choices=[
                    ('fixed', 'Giá cố định'),
                    ('quote', 'Yêu cầu báo giá'),
                    ('contact', 'Liên hệ để biết giá'),
                ],
                default='fixed',
                max_length=20,
                verbose_name='Loại giá tại thời điểm thêm',
            ),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='unit_price',
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                max_digits=15,
                null=True,
                verbose_name='Đơn giá tạm tính',
            ),
        ),
        migrations.RunPython(
            migrate_cart_prices,
            reverse_code=reverse_cart_prices,
        ),
    ]
