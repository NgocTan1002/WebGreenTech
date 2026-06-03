-- FUNCTION: public.fn_get_solutions(text, integer, integer)

-- DROP FUNCTION IF EXISTS public.fn_get_solutions(text, integer, integer);

CREATE OR REPLACE FUNCTION public.fn_get_solutions(
	p_category_slug text DEFAULT NULL::text,
	p_limit integer DEFAULT 12,
	p_offset integer DEFAULT 0)
    RETURNS TABLE(id bigint, title character varying, slug character varying, subtitle character varying, short_description text, thumbnail character varying, is_featured boolean, category_name character varying, category_slug character varying, view_count integer, total_count bigint) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        s.id, s.title, s.slug, s.subtitle,
        s.short_description, s.thumbnail, s.is_featured,
        sc.name AS category_name,
        sc.slug AS category_slug,
        s.view_count,
        COUNT(*) OVER() AS total_count
    FROM solutions_solution s
    LEFT JOIN solutions_solutioncategory sc ON sc.id = s.solution_category_id
    WHERE s.status = 'published'
      AND (p_category_slug IS NULL OR sc.slug = p_category_slug)
    ORDER BY s.is_featured DESC, s.sort_order ASC
    LIMIT p_limit OFFSET p_offset;
$BODY$;

ALTER FUNCTION public.fn_get_solutions(text, integer, integer)
    OWNER TO postgres;

