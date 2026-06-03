-- FUNCTION: public.fn_get_customer_orders(bigint, integer, integer)

-- DROP FUNCTION IF EXISTS public.fn_get_customer_orders(bigint, integer, integer);

CREATE OR REPLACE FUNCTION public.fn_get_customer_orders(
	p_customer_id bigint,
	p_limit integer DEFAULT 20,
	p_offset integer DEFAULT 0)
    RETURNS TABLE(order_id uuid, order_number text, order_type text, status text, total numeric, item_count bigint, created_at timestamp with time zone) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        o.id, o.order_number, o.order_type, o.status,
        o.total,
        COUNT(oi.id) AS item_count,
        o.created_at
    FROM orders_order o
    LEFT JOIN orders_orderitem oi ON oi.order_id = o.id
    WHERE o.customer_id = p_customer_id
    GROUP BY o.id
    ORDER BY o.created_at DESC
    LIMIT p_limit OFFSET p_offset;
$BODY$;

ALTER FUNCTION public.fn_get_customer_orders(bigint, integer, integer)
    OWNER TO postgres;

