CREATE OR REPLACE FUNCTION public.fn_upsert_cart_item_v2(
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
