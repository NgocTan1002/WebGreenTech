from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_remove_customer_preferred_currency_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={
                'verbose_name': 'Khách hàng',
                'verbose_name_plural': 'Khách hàng',
            },
        ),
        migrations.AlterModelOptions(
            name='customeraddress',
            options={
                'verbose_name': 'Địa chỉ khách hàng',
                'verbose_name_plural': 'Địa chỉ khách hàng',
            },
        ),
    ]
