-- FUNCTION: public.fn_get_cart_summary(uuid)

-- DROP FUNCTION IF EXISTS public.fn_get_cart_summary(uuid);

CREATE OR REPLACE FUNCTION public.fn_get_cart_summary(
	p_cart_id uuid)
    RETURNS TABLE(total_items bigint, subtotal numeric) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        COALESCE(SUM(quantity), 0)             AS total_items,
        COALESCE(SUM(quantity * unit_price), 0) AS subtotal
    FROM cart_cartitem
    WHERE cart_id = p_cart_id;
$BODY$;

ALTER FUNCTION public.fn_get_cart_summary(uuid)
    OWNER TO postgres;

