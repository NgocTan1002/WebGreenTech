-- FUNCTION: public.fn_get_product_specs(bigint)

-- DROP FUNCTION IF EXISTS public.fn_get_product_specs(bigint);

CREATE OR REPLACE FUNCTION public.fn_get_product_specs(
	p_product_id bigint)
    RETURNS TABLE(spec_group character varying, spec_key character varying, spec_value character varying, unit character varying, sort_order integer) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        COALESCE(NULLIF(ps.group, ''), 'Thông số chung') AS spec_group,
        ps.key,
        ps.value,
        ps.unit,
        ps.sort_order
    FROM products_productspecification ps
    WHERE ps.product_id = p_product_id
    ORDER BY ps.sort_order, ps.key;
$BODY$;

ALTER FUNCTION public.fn_get_product_specs(bigint)
    OWNER TO postgres;

