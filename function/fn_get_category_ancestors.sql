-- FUNCTION: public.fn_get_category_ancestors(bigint)

-- DROP FUNCTION IF EXISTS public.fn_get_category_ancestors(bigint);

CREATE OR REPLACE FUNCTION public.fn_get_category_ancestors(
	p_category_id bigint)
    RETURNS TABLE(id bigint, name character varying, slug character varying, level integer) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT a.id, a.name, a.slug, a.level
    FROM categories_category a
    JOIN categories_category c ON
        a.tree_id = c.tree_id AND
        a.lft <= c.lft AND
        a.rght >= c.rght
    WHERE c.id = p_category_id
    ORDER BY a.lft;
$BODY$;

ALTER FUNCTION public.fn_get_category_ancestors(bigint)
    OWNER TO postgres;

