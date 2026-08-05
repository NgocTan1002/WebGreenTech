from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0004_solution_deployment_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionDeploymentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sort_order', models.PositiveIntegerField(db_index=True, default=0)),
                ('image', models.ImageField(upload_to='solutions/deployments/', verbose_name='Ảnh triển khai')),
                ('caption', models.CharField(blank=True, max_length=255, verbose_name='Chú thích')),
                ('alt_text', models.CharField(blank=True, max_length=255, verbose_name='Mô tả ảnh (SEO)')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Ảnh chính')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deployment_images', to='solutions.solution', verbose_name='Giải pháp')),
            ],
            options={
                'verbose_name': 'Ảnh triển khai giải pháp',
                'verbose_name_plural': 'Ảnh triển khai giải pháp',
                'ordering': ['-is_primary', 'sort_order', 'id'],
            },
        ),
    ]
