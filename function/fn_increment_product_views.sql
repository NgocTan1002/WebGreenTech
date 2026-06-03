-- FUNCTION: public.fn_increment_product_views(bigint)

-- DROP FUNCTION IF EXISTS public.fn_increment_product_views(bigint);

CREATE OR REPLACE FUNCTION public.fn_increment_product_views(
	p_product_id bigint)
    RETURNS void
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
    UPDATE products_product
    SET view_count = view_count + 1
    WHERE id = p_product_id;
$BODY$;

ALTER FUNCTION public.fn_increment_product_views(bigint)
    OWNER TO postgres;

