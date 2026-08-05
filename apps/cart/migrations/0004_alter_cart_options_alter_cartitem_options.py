from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_fix_unit_price_decimal_places'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={
                'verbose_name': 'Giỏ hàng',
                'verbose_name_plural': 'Giỏ hàng',
            },
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={
                'verbose_name': 'Sản phẩm trong giỏ hàng',
                'verbose_name_plural': 'Sản phẩm trong giỏ hàng',
            },
        ),
    ]
