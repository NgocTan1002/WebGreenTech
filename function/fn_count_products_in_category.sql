-- FUNCTION: public.fn_count_products_in_category(bigint)

-- DROP FUNCTION IF EXISTS public.fn_count_products_in_category(bigint);

CREATE OR REPLACE FUNCTION public.fn_count_products_in_category(
	p_category_id bigint)
    RETURNS bigint
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
AS $BODY$
    SELECT COUNT(*)
    FROM products_product p
    JOIN categories_category c ON c.id = p.category_id
    WHERE p.status = 'published'
      AND c.tree_id = (SELECT tree_id FROM categories_category WHERE id = p_category_id)
      AND c.lft  >= (SELECT lft  FROM categories_category WHERE id = p_category_id)
      AND c.rght <= (SELECT rght FROM categories_category WHERE id = p_category_id);
$BODY$;

ALTER FUNCTION public.fn_count_products_in_category(bigint)
    OWNER TO postgres;

