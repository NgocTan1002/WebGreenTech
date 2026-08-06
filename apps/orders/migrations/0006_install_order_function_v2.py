from pathlib import Path

from django.conf import settings
from django.db import migrations


def install_function(apps, schema_editor):
    sql_path = Path(settings.BASE_DIR) / 'function' / 'fn_create_order_from_cart_v2.sql'
    schema_editor.execute(sql_path.read_text(encoding='utf-8'))


def remove_function(apps, schema_editor):
    schema_editor.execute(
        'DROP FUNCTION IF EXISTS public.fn_create_order_from_cart_v2('
        'uuid, text, bigint, text, text, text, text, text, jsonb, text);'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_install_cart_functions_v2'),
        ('orders', '0005_orderitem_pricing_type_alter_orderitem_unit_price'),
    ]

    operations = [
        migrations.RunPython(
            install_function,
            reverse_code=remove_function,
        ),
    ]
