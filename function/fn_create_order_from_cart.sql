-- FUNCTION: public.fn_create_order_from_cart(uuid, text, bigint, text, text, text, text, text, jsonb, text)

-- DROP FUNCTION IF EXISTS public.fn_create_order_from_cart(uuid, text, bigint, text, text, text, text, text, jsonb, text);

CREATE OR REPLACE FUNCTION public.fn_create_order_from_cart(
	p_cart_id uuid,
	p_order_type text,
	p_customer_id bigint,
	p_email text,
	p_first_name text,
	p_last_name text,
	p_company_name text,
	p_phone text,
	p_shipping_addr jsonb,
	p_notes text DEFAULT ''::text)
    RETURNS TABLE(order_id uuid, order_number text, total numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_order_id     UUID := gen_random_uuid();
    v_order_number TEXT;
    v_subtotal     NUMERIC;
    v_prefix       TEXT;
BEGIN
    v_prefix := CASE p_order_type WHEN 'purchase' THEN 'PO' ELSE 'QT' END;
    v_order_number := v_prefix || '-' || TO_CHAR(NOW(), 'YYYYMM') || '-'
                      || LPAD(FLOOR(RANDOM() * 90000 + 10000)::TEXT, 5, '0');

    SELECT COALESCE(SUM(ci.quantity * ci.unit_price), 0)
    INTO v_subtotal
    FROM cart_cartitem ci
    WHERE ci.cart_id = p_cart_id;

    IF NOT EXISTS (
        SELECT 1 FROM cart_cartitem WHERE cart_id = p_cart_id
    ) THEN
        RAISE EXCEPTION 'Giỏ hàng trống, không thể tạo đơn hàng.';
    END IF;

    IF p_order_type = 'purchase' AND EXISTS (
        SELECT 1
        FROM cart_cartitem
        WHERE cart_id = p_cart_id
          AND (pricing_type <> 'fixed' OR unit_price IS NULL)
    ) THEN
        RAISE EXCEPTION 'Không thể tạo đơn mua hàng khi còn sản phẩm chờ báo giá.';
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
        p_notes, v_subtotal, v_subtotal,
        NOW(), NOW()
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

ALTER FUNCTION public.fn_create_order_from_cart(uuid, text, bigint, text, text, text, text, text, jsonb, text)
    OWNER TO postgres;

