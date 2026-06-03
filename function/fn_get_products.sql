-- FUNCTION: public.fn_get_products(bigint, bigint, numeric, numeric, boolean, text, text, integer, integer)

-- DROP FUNCTION IF EXISTS public.fn_get_products(bigint, bigint, numeric, numeric, boolean, text, text, integer, integer);

CREATE OR REPLACE FUNCTION public.fn_get_products(
	p_category_id bigint DEFAULT NULL::bigint,
	p_brand_id bigint DEFAULT NULL::bigint,
	p_min_price numeric DEFAULT NULL::numeric,
	p_max_price numeric DEFAULT NULL::numeric,
	p_stock_only boolean DEFAULT false,
	p_search text DEFAULT NULL::text,
	p_sort_by text DEFAULT 'featured'::text,
	p_limit integer DEFAULT 24,
	p_offset integer DEFAULT 0)
    RETURNS TABLE(id bigint, name character varying, slug character varying, sku character varying, pricing_type character varying, price numeric, sale_price numeric, stock_status character varying, is_featured boolean, is_new boolean, thumbnail character varying, category_name character varying, brand_name character varying, total_count bigint) 
    LANGUAGE 'plpgsql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_order_clause TEXT;
BEGIN
    v_order_clause := CASE p_sort_by
        WHEN 'newest'     THEN 'p.created_at DESC'
        WHEN 'price_asc'  THEN 'p.price ASC NULLS LAST'
        WHEN 'price_desc' THEN 'p.price DESC NULLS LAST'
        WHEN 'name'       THEN 'p.name ASC'
        ELSE                   'p.is_featured DESC, p.sort_order ASC'
    END;

    RETURN QUERY EXECUTE format('
        SELECT
            p.id, p.name, p.slug, p.sku,
            p.pricing_type, p.price, p.sale_price,
            p.stock_status, p.is_featured, p.is_new, p.thumbnail,
            c.name  AS category_name,
            br.name AS brand_name,
            COUNT(*) OVER() AS total_count
        FROM products_product p
        JOIN  categories_category c  ON c.id  = p.category_id
        LEFT JOIN categories_brand br ON br.id = p.brand_id
        WHERE p.status = ''published''
            AND ($1 IS NULL OR p.category_id IN (
                SELECT id FROM categories_category
                WHERE tree_id = (SELECT tree_id FROM categories_category WHERE id = $1)
                  AND lft  >= (SELECT lft  FROM categories_category WHERE id = $1)
                  AND rght <= (SELECT rght FROM categories_category WHERE id = $1)
            ))
            AND ($2 IS NULL OR p.brand_id    = $2)
            AND ($3 IS NULL OR p.price      >= $3)
            AND ($4 IS NULL OR p.price      <= $4)
            AND (NOT $5     OR p.stock_status IN (''in_stock'', ''low_stock''))
            AND ($6 IS NULL OR (
                p.name              ILIKE ''%%'' || $6 || ''%%''
                OR p.sku            ILIKE ''%%'' || $6 || ''%%''
                OR p.short_description ILIKE ''%%'' || $6 || ''%%''
            ))
        ORDER BY %s
        LIMIT $7 OFFSET $8
    ', v_order_clause)
    USING p_category_id, p_brand_id, p_min_price, p_max_price,
          p_stock_only, p_search, p_limit, p_offset;
END;
$BODY$;

ALTER FUNCTION public.fn_get_products(bigint, bigint, numeric, numeric, boolean, text, text, integer, integer)
    OWNER TO postgres;

