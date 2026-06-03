-- FUNCTION: public.fn_increment_post_views(bigint)

-- DROP FUNCTION IF EXISTS public.fn_increment_post_views(bigint);

CREATE OR REPLACE FUNCTION public.fn_increment_post_views(
	p_post_id bigint)
    RETURNS void
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
    UPDATE blog_post
    SET view_count = view_count + 1
    WHERE id = p_post_id;
$BODY$;

ALTER FUNCTION public.fn_increment_post_views(bigint)
    OWNER TO postgres;

