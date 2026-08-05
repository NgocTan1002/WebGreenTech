from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0005_solutiondeploymentimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='architectureblock',
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Khối kiến trúc',
                'verbose_name_plural': 'Khối kiến trúc',
            },
        ),
        migrations.AlterModelOptions(
            name='customercase',
            options={
                'ordering': ['-published_at'],
                'verbose_name': 'Dự án khách hàng',
                'verbose_name_plural': 'Dự án khách hàng',
            },
        ),
        migrations.AlterModelOptions(
            name='solution',
            options={
                'ordering': ['sort_order', '-created_at'],
                'verbose_name': 'Giải pháp',
                'verbose_name_plural': 'Giải pháp',
            },
        ),
        migrations.AlterModelOptions(
            name='solutioncategory',
            options={
                'ordering': ['sort_order', 'name'],
                'verbose_name': 'Danh mục giải pháp',
                'verbose_name_plural': 'Danh mục giải pháp',
            },
        ),
        migrations.AlterModelOptions(
            name='solutionproduct',
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Sản phẩm trong giải pháp',
                'verbose_name_plural': 'Sản phẩm trong giải pháp',
            },
        ),
        migrations.AlterModelOptions(
            name='workflowstep',
            options={
                'ordering': ['step_number'],
                'verbose_name': 'Bước quy trình',
                'verbose_name_plural': 'Bước quy trình',
            },
        ),
    ]
