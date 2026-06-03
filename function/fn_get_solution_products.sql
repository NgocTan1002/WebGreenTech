-- FUNCTION: public.fn_get_solution_products(bigint, boolean)

-- DROP FUNCTION IF EXISTS public.fn_get_solution_products(bigint, boolean);

CREATE OR REPLACE FUNCTION public.fn_get_solution_products(
	p_solution_id bigint,
	p_featured_only boolean DEFAULT false)
    RETURNS TABLE(product_id bigint, product_name character varying, product_slug character varying, product_sku character varying, price numeric, thumbnail character varying, stock_status character varying, is_featured boolean, role_description character varying, sort_order integer) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        p.id, p.name, p.slug, p.sku,
        p.price, p.thumbnail, p.stock_status,
        sp.is_featured, sp.role_description, sp.sort_order
    FROM solutions_solutionproduct sp
    JOIN products_product p ON p.id = sp.product_id
    WHERE sp.solution_id = p_solution_id
      AND p.status = 'published'
      AND (NOT p_featured_only OR sp.is_featured = TRUE)
    ORDER BY sp.sort_order;
$BODY$;

ALTER FUNCTION public.fn_get_solution_products(bigint, boolean)
    OWNER TO postgres;

