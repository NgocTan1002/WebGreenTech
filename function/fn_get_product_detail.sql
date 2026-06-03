-- FUNCTION: public.fn_get_product_detail(text)

-- DROP FUNCTION IF EXISTS public.fn_get_product_detail(text);

CREATE OR REPLACE FUNCTION public.fn_get_product_detail(
	p_slug text)
    RETURNS TABLE(
	id bigint,
	name character varying,
	slug character varying,
	sku character varying,
	part_number character varying, 
	pricing_type character varying,
	price numeric, 
	sale_price numeric,
	min_order_qty integer, 
	stock_status character varying, 
	stock_quantity integer,
	short_description text,
	description text, 
	highlights jsonb,
	weight numeric,
	dim_length numeric,
	dim_width numeric,           
	dim_height numeric,   
	is_featured boolean,
	is_new boolean,
	is_bestseller boolean,
	requires_quote boolean,
	category_id bigint,
	category_name character varying,
	brand_id bigint,
	brand_name character varying,
	view_count integer) 
    LANGUAGE 'sql'
    COST 100
    STABLE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
    SELECT
        p.id, p.name, p.slug, p.sku, p.part_number,
        p.pricing_type, p.price, p.sale_price,
        p.min_order_qty, p.stock_status, p.stock_quantity,
        p.short_description, p.description, p.highlights,
        p.weight,
		p.dim_length, p.dim_width, p.dim_height,
        p.is_featured, p.is_new, p.is_bestseller,
		p.requires_quote,
        c.id   AS category_id,
        c.name AS category_name,
        b.id   AS brand_id,
        b.name AS brand_name,
        p.view_count
    FROM products_product p
    JOIN  categories_category c ON c.id = p.category_id
    LEFT JOIN categories_brand b ON b.id = p.brand_id
    WHERE p.slug = p_slug AND p.status = 'published'
    LIMIT 1;
$BODY$;

ALTER FUNCTION public.fn_get_product_detail(text)
    OWNER TO postgres;

