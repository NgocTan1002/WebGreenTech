-- FUNCTION: public.fn_get_solution_detail(text)

-- DROP FUNCTION IF EXISTS public.fn_get_solution_detail(text);

CREATE OR REPLACE FUNCTION public.fn_get_solution_detail(
	p_slug text)
    RETURNS TABLE(id bigint, title character varying, slug character varying, subtitle character varying, short_description text, overview text, pain_points jsonb, benefits jsonb, workflow_title character varying, workflow_description text, cta_title character varying, cta_primary_text character varying, cta_primary_url character varying, cta_secondary_text character varying, cta_secondary_url character varying, hero_image character varying, hero_video_url character varying, thumbnail character varying, category_name character varying, view_count integer) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        s.id, s.title, s.slug, s.subtitle,
        s.short_description, s.overview,
        s.pain_points, s.benefits,
        s.workflow_title, s.workflow_description,
        s.cta_title, s.cta_primary_text, s.cta_primary_url,
        s.cta_secondary_text, s.cta_secondary_url,
        s.hero_image, s.hero_video_url, s.thumbnail,
        sc.name AS category_name,
        s.view_count
    FROM solutions_solution s
    LEFT JOIN solutions_solutioncategory sc ON sc.id = s.solution_category_id
    WHERE s.slug = p_slug AND s.status = 'published'
    LIMIT 1;
$BODY$;

ALTER FUNCTION public.fn_get_solution_detail(text)
    OWNER TO postgres;

