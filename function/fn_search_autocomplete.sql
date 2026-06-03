-- FUNCTION: public.fn_search_autocomplete(text, integer)

-- DROP FUNCTION IF EXISTS public.fn_search_autocomplete(text, integer);

CREATE OR REPLACE FUNCTION public.fn_search_autocomplete(
	p_query text,
	p_limit integer DEFAULT 5)
    RETURNS TABLE(result_type text, label text, slug text, sku text) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
	SELECT * FROM (
	    SELECT 'product'::TEXT, p.name, p.slug, p.sku
	    FROM products_product p
	    WHERE p.status = 'published'
	      AND (p.name ILIKE '%' || p_query || '%' OR p.sku ILIKE '%' || p_query || '%')
	    ORDER BY p.is_featured DESC, p.view_count DESC
	    LIMIT p_limit
	) products_results
	
	UNION ALL
	
	SELECT * FROM (
	    SELECT 'solution'::TEXT, s.title, s.slug, NULL
	    FROM solutions_solution s
	    WHERE s.status = 'published'
	      AND s.title ILIKE '%' || p_query || '%'
	    ORDER BY s.is_featured DESC
	    LIMIT 3
	) solutions_results;
$BODY$;

ALTER FUNCTION public.fn_search_autocomplete(text, integer)
    OWNER TO postgres;

