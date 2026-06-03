-- FUNCTION: public.fn_get_category_tree(boolean)

-- DROP FUNCTION IF EXISTS public.fn_get_category_tree(boolean);

CREATE OR REPLACE FUNCTION public.fn_get_category_tree(
	p_active_only boolean DEFAULT true)
    RETURNS TABLE(id bigint, name character varying, slug character varying, parent_id bigint, level integer, lft integer, rght integer, tree_id integer, is_active boolean, show_in_nav boolean, sort_order integer, icon_class character varying) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        id, name, slug, parent_id,
        level, lft, rght, tree_id,
        is_active, show_in_nav, sort_order, icon_class
    FROM categories_category
    WHERE (NOT p_active_only OR is_active = TRUE)
    ORDER BY tree_id, lft;
$BODY$;

ALTER FUNCTION public.fn_get_category_tree(boolean)
    OWNER TO postgres;

