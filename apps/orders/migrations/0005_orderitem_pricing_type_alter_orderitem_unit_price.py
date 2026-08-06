from django.db import migrations, models


FORWARD_CREATE_ORDER_SQL = r"""
CREATE OR REPLACE FUNCTION public.fn_create_order_from_cart(
    p_cart_id uuid, p_order_type text, p_customer_id bigint,
    p_email text, p_first_name text, p_last_name text,
    p_company_name text, p_phone text, p_shipping_addr jsonb,
    p_notes text DEFAULT ''::text
)
RETURNS TABLE(order_id uuid, order_number text, total numeric)
LANGUAGE plpgsql
VOLATILE
PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_order_id UUID := gen_random_uuid();
    v_order_number TEXT;
    v_subtotal NUMERIC;
    v_prefix TEXT;
BEGIN
    v_prefix := CASE p_order_type WHEN 'purchase' THEN 'PO' ELSE 'QT' END;
    v_order_number := v_prefix || '-' || TO_CHAR(NOW(), 'YYYYMM') || '-'
        || LPAD(FLOOR(RANDOM() * 90000 + 10000)::TEXT, 5, '0');

    IF NOT EXISTS (SELECT 1 FROM cart_cartitem WHERE cart_id = p_cart_id) THEN
        RAISE EXCEPTION 'Giỏ hàng trống, không thể tạo đơn hàng.';
    END IF;

    IF p_order_type = 'purchase' AND EXISTS (
        SELECT 1 FROM cart_cartitem
        WHERE cart_id = p_cart_id
          AND (pricing_type <> 'fixed' OR unit_price IS NULL)
    ) THEN
        RAISE EXCEPTION 'Không thể tạo đơn mua hàng khi còn sản phẩm chờ báo giá.';
    END IF;

    SELECT COALESCE(SUM(ci.quantity * ci.unit_price), 0)
    INTO v_subtotal
    FROM cart_cartitem ci
    WHERE ci.cart_id = p_cart_id;

    INSERT INTO orders_order (
        id, order_number, order_type, status,
        customer_id, email, first_name, last_name,
        company_name, phone, shipping_address, billing_address,
        customer_notes, subtotal, total,
        created_at, updated_at
    ) VALUES (
        v_order_id, v_order_number, p_order_type, 'pending',
        p_customer_id, p_email, p_first_name, p_last_name,
        p_company_name, p_phone, p_shipping_addr, p_shipping_addr,
        p_notes, v_subtotal, v_subtotal, NOW(), NOW()
    );

    INSERT INTO orders_orderitem (
        order_id, product_id, product_name, product_sku,
        quantity, pricing_type, unit_price
    )
    SELECT
        v_order_id, ci.product_id, p.name, p.sku,
        ci.quantity, ci.pricing_type, ci.unit_price
    FROM cart_cartitem ci
    JOIN products_product p ON p.id = ci.product_id
    WHERE ci.cart_id = p_cart_id;

    UPDATE cart_cart
    SET is_active = FALSE, updated_at = NOW()
    WHERE id = p_cart_id;

    RETURN QUERY SELECT v_order_id, v_order_number, v_subtotal;
END;
$BODY$;
"""


REVERSE_CREATE_ORDER_SQL = r"""
CREATE OR REPLACE FUNCTION public.fn_create_order_from_cart(
    p_cart_id uuid, p_order_type text, p_customer_id bigint,
    p_email text, p_first_name text, p_last_name text,
    p_company_name text, p_phone text, p_shipping_addr jsonb,
    p_notes text DEFAULT ''::text
)
RETURNS TABLE(order_id uuid, order_number text, total numeric)
LANGUAGE plpgsql
VOLATILE
PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_order_id UUID := gen_random_uuid();
    v_order_number TEXT;
    v_subtotal NUMERIC;
    v_prefix TEXT;
BEGIN
    v_prefix := CASE p_order_type WHEN 'purchase' THEN 'PO' ELSE 'QT' END;
    v_order_number := v_prefix || '-' || TO_CHAR(NOW(), 'YYYYMM') || '-'
        || LPAD(FLOOR(RANDOM() * 90000 + 10000)::TEXT, 5, '0');

    SELECT COALESCE(SUM(ci.quantity * COALESCE(ci.unit_price, 0)), 0)
    INTO v_subtotal FROM cart_cartitem ci WHERE ci.cart_id = p_cart_id;
    IF NOT EXISTS (SELECT 1 FROM cart_cartitem WHERE cart_id = p_cart_id) THEN
        RAISE EXCEPTION 'Giỏ hàng trống, không thể tạo đơn hàng.';
    END IF;

    INSERT INTO orders_order (
        id, order_number, order_type, status,
        customer_id, email, first_name, last_name,
        company_name, phone, shipping_address, billing_address,
        customer_notes, subtotal, total,
        created_at, updated_at
    ) VALUES (
        v_order_id, v_order_number, p_order_type, 'pending',
        p_customer_id, p_email, p_first_name, p_last_name,
        p_company_name, p_phone, p_shipping_addr, p_shipping_addr,
        p_notes, v_subtotal, v_subtotal, NOW(), NOW()
    );

    INSERT INTO orders_orderitem (
        order_id, product_id, product_name, product_sku, quantity, unit_price
    )
    SELECT v_order_id, ci.product_id, p.name, p.sku,
           ci.quantity, COALESCE(ci.unit_price, 0)
    FROM cart_cartitem ci
    JOIN products_product p ON p.id = ci.product_id
    WHERE ci.cart_id = p_cart_id;

    UPDATE cart_cart SET is_active = FALSE, updated_at = NOW()
    WHERE id = p_cart_id;
    RETURN QUERY SELECT v_order_id, v_order_number, v_subtotal;
END;
$BODY$;
"""


def migrate_order_prices(apps, schema_editor):
    schema_editor.execute("""
        UPDATE orders_orderitem AS oi
        SET
            pricing_type = CASE
                WHEN p.id IS NOT NULL AND p.requires_quote THEN 'quote'
                WHEN p.id IS NOT NULL THEN p.pricing_type
                WHEN oi.unit_price = 0 THEN 'quote'
                ELSE 'fixed'
            END,
            unit_price = CASE
                WHEN p.id IS NOT NULL AND (p.requires_quote OR p.pricing_type <> 'fixed') THEN NULL
                WHEN p.id IS NULL AND oi.unit_price = 0 THEN NULL
                ELSE oi.unit_price
            END
        FROM products_product AS p
        WHERE p.id = oi.product_id;

        UPDATE orders_orderitem
        SET pricing_type = 'quote', unit_price = NULL
        WHERE product_id IS NULL AND unit_price = 0;
    """)


def reverse_order_prices(apps, schema_editor):
    schema_editor.execute(
        "UPDATE orders_orderitem SET unit_price = 0 WHERE unit_price IS NULL;"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cartitem_pricing_type_alter_cartitem_unit_price'),
        ('orders', '0004_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='pricing_type',
            field=models.CharField(
                choices=[
                    ('fixed', 'Giá cố định'),
                    ('quote', 'Yêu cầu báo giá'),
                    ('contact', 'Liên hệ để biết giá'),
                ],
                default='fixed',
                max_length=20,
                verbose_name='Loại giá tại thời điểm gửi',
            ),
        ),
        migrations.AlterField(
            model_name='orderitem',
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
            migrate_order_prices,
            reverse_code=reverse_order_prices,
        ),
    ]
