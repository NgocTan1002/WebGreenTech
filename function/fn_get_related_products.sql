-- FUNCTION: public.fn_get_related_products(bigint, integer)

-- DROP FUNCTION IF EXISTS public.fn_get_related_products(bigint, integer);

CREATE OR REPLACE FUNCTION public.fn_get_related_products(
	p_product_id bigint,
	p_limit integer DEFAULT 6)
    RETURNS TABLE(id bigint, name character varying, slug character varying, sku character varying, price numeric, thumbnail character varying, stock_status character varying, relation_type character varying) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        p.id, p.name, p.slug, p.sku,
        p.price, p.thumbnail, p.stock_status,
        rp.relation_type
    FROM products_relatedproduct rp
    JOIN products_product p ON p.id = rp.related_id
    WHERE rp.product_id = p_product_id AND p.status = 'published'
    ORDER BY rp.sort_order
    LIMIT p_limit;
$BODY$;

ALTER FUNCTION public.fn_get_related_products(bigint, integer)
    OWNER TO postgres;

