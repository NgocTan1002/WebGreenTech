-- FUNCTION: public.fn_get_posts(text, text, text, integer, integer)

-- DROP FUNCTION IF EXISTS public.fn_get_posts(text, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.fn_get_posts(
	p_category_slug text DEFAULT NULL::text,
	p_post_type text DEFAULT NULL::text,
	p_search text DEFAULT NULL::text,
	p_limit integer DEFAULT 12,
	p_offset integer DEFAULT 0)
    RETURNS TABLE(id bigint, title character varying, slug character varying, post_type character varying, short_description text, thumbnail character varying, read_time integer, author_name text, category_name character varying, published_at timestamp with time zone, view_count integer, total_count bigint) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        p.id, p.title, p.slug, p.post_type,
        p.short_description, p.thumbnail, p.read_time,
        (c2.first_name || ' ' || c2.last_name) AS author_name,
        bc.name AS category_name,
        p.published_at, p.view_count,
        COUNT(*) OVER() AS total_count
    FROM blog_post p
    LEFT JOIN blog_blogcategory  bc ON bc.id = p.category_id
    LEFT JOIN customers_customer c2 ON c2.id = p.author_id
    WHERE p.status = 'published'
      AND (p_category_slug IS NULL OR bc.slug     = p_category_slug)
      AND (p_post_type     IS NULL OR p.post_type = p_post_type)
      AND (p_search        IS NULL OR p.title ILIKE '%' || p_search || '%')
    ORDER BY p.published_at DESC NULLS LAST
    LIMIT p_limit OFFSET p_offset;
$BODY$;

ALTER FUNCTION public.fn_get_posts(text, text, text, integer, integer)
    OWNER TO postgres;

