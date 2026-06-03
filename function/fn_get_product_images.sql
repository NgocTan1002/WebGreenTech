-- FUNCTION: public.fn_get_product_images(bigint)

-- DROP FUNCTION IF EXISTS public.fn_get_product_images(bigint);

CREATE OR REPLACE FUNCTION public.fn_get_product_images(
	p_product_id bigint)
    RETURNS TABLE(id bigint, image character varying, alt_text character varying, is_primary boolean, sort_order integer) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT id, image, alt_text, is_primary, sort_order
    FROM products_productimage
    WHERE product_id = p_product_id
    ORDER BY is_primary DESC, sort_order ASC;
$BODY$;

ALTER FUNCTION public.fn_get_product_images(bigint)
    OWNER TO postgres;

