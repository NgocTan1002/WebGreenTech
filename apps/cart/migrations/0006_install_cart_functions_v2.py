from pathlib import Path

from django.conf import settings
from django.db import migrations


FUNCTION_FILES = (
    'fn_get_cart_detail_v2.sql',
    'fn_upsert_cart_item_v2.sql',
)


def install_functions(apps, schema_editor):
    function_dir = Path(settings.BASE_DIR) / 'function'
    for file_name in FUNCTION_FILES:
        schema_editor.execute(
            (function_dir / file_name).read_text(encoding='utf-8')
        )


def remove_functions(apps, schema_editor):
    schema_editor.execute(
        'DROP FUNCTION IF EXISTS public.fn_get_cart_detail_v2(uuid);'
    )
    schema_editor.execute(
        'DROP FUNCTION IF EXISTS public.fn_upsert_cart_item_v2(uuid, bigint, integer, numeric);'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cartitem_pricing_type_alter_cartitem_unit_price'),
    ]

    operations = [
        migrations.RunPython(
            install_functions,
            reverse_code=remove_functions,
        ),
    ]
