from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_author_alter_post_content_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={
                'ordering': ['sort_order', 'name'],
                'verbose_name': 'Danh mục bài viết',
                'verbose_name_plural': 'Danh mục bài viết',
            },
        ),
        migrations.AlterModelOptions(
            name='post',
            options={
                'ordering': ['-published_at', '-created_at'],
                'verbose_name': 'Bài viết',
                'verbose_name_plural': 'Bài viết',
            },
        ),
    ]
