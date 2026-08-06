CREATE OR REPLACE FUNCTION public.fn_get_cart_detail_v2(p_cart_id uuid)
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
