from django.db import migrations, models


FORWARD_FUNCTION_SQL = """
CREATE FUNCTION public.fn_get_solution_detail(p_slug text)
RETURNS TABLE(
    id bigint,
    title character varying,
    slug character varying,
    subtitle character varying,
    short_description text,
    overview text,
    deployment_site character varying,
    deployment_location character varying,
    deployed_at date,
    pain_points jsonb,
    benefits jsonb,
    workflow_title character varying,
    workflow_description text,
    cta_title character varying,
    cta_primary_text character varying,
    cta_primary_url character varying,
    cta_secondary_text character varying,
    cta_secondary_url character varying,
    hero_image character varying,
    hero_video_url character varying,
    thumbnail character varying,
    category_name character varying,
    view_count integer
)
LANGUAGE sql
STABLE
PARALLEL UNSAFE
AS $BODY$
    SELECT
        s.id, s.title, s.slug, s.subtitle,
        s.short_description, s.overview,
        s.deployment_site, s.deployment_location, s.deployed_at,
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
"""


REVERSE_FUNCTION_SQL = """
CREATE FUNCTION public.fn_get_solution_detail(p_slug text)
RETURNS TABLE(
    id bigint,
    title character varying,
    slug character varying,
    subtitle character varying,
    short_description text,
    overview text,
    pain_points jsonb,
    benefits jsonb,
    workflow_title character varying,
    workflow_description text,
    cta_title character varying,
    cta_primary_text character varying,
    cta_primary_url character varying,
    cta_secondary_text character varying,
    cta_secondary_url character varying,
    hero_image character varying,
    hero_video_url character varying,
    thumbnail character varying,
    category_name character varying,
    view_count integer
)
LANGUAGE sql
STABLE
PARALLEL UNSAFE
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
"""


def install_forward_function(apps, schema_editor):
    schema_editor.execute(
        "DROP FUNCTION IF EXISTS public.fn_get_solution_detail(text);"
    )
    schema_editor.execute(FORWARD_FUNCTION_SQL)


def install_reverse_function(apps, schema_editor):
    schema_editor.execute(
        "DROP FUNCTION IF EXISTS public.fn_get_solution_detail(text);"
    )
    schema_editor.execute(REVERSE_FUNCTION_SQL)


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0003_solution_cta_primary_text_solution_cta_primary_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='deployed_at',
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name='Thời gian triển khai',
            ),
        ),
        migrations.AddField(
            model_name='solution',
            name='deployment_location',
            field=models.CharField(
                blank=True,
                help_text='Ví dụ: KCN Quế Võ, Bắc Ninh',
                max_length=255,
                verbose_name='Địa chỉ triển khai',
            ),
        ),
        migrations.AddField(
            model_name='solution',
            name='deployment_site',
            field=models.CharField(
                blank=True,
                help_text='Ví dụ: Nhà máy ABC',
                max_length=200,
                verbose_name='Đơn vị / địa điểm triển khai',
            ),
        ),
        migrations.RunPython(
            install_forward_function,
            reverse_code=install_reverse_function,
        ),
    ]
