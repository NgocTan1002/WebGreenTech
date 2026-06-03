-- FUNCTION: public.fn_get_cart_detail(uuid)

-- DROP FUNCTION IF EXISTS public.fn_get_cart_detail(uuid);

CREATE OR REPLACE FUNCTION public.fn_get_cart_detail(
	p_cart_id uuid)
    RETURNS TABLE(item_id bigint, product_id bigint, product_name character varying, product_sku character varying, product_slug character varying, thumbnail character varying, stock_status character varying, quantity integer, unit_price numeric, line_total numeric) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        ci.id, p.id, p.name, p.sku, p.slug,
        p.thumbnail, p.stock_status,
        ci.quantity, ci.unit_price,
        ci.quantity * ci.unit_price AS line_total
    FROM cart_cartitem ci
    JOIN products_product p ON p.id = ci.product_id
    WHERE ci.cart_id = p_cart_id
    ORDER BY ci.created_at;
$BODY$;

ALTER FUNCTION public.fn_get_cart_detail(uuid)
    OWNER TO postgres;

