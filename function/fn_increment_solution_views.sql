-- FUNCTION: public.fn_increment_solution_views(bigint)

-- DROP FUNCTION IF EXISTS public.fn_increment_solution_views(bigint);

CREATE OR REPLACE FUNCTION public.fn_increment_solution_views(
	p_solution_id bigint)
    RETURNS void
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
    UPDATE solutions_solution
    SET view_count = view_count + 1
    WHERE id = p_solution_id;
$BODY$;

ALTER FUNCTION public.fn_increment_solution_views(bigint)
    OWNER TO postgres;

