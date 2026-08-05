from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_demorequest_solution'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactinquiry',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Yêu cầu liên hệ',
                'verbose_name_plural': 'Yêu cầu liên hệ',
            },
        ),
        migrations.AlterModelOptions(
            name='demorequest',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Yêu cầu đăng ký demo',
                'verbose_name_plural': 'Yêu cầu đăng ký demo',
            },
        ),
        migrations.AlterField(
            model_name='contactinquiry',
            name='inquiry_type',
            field=models.CharField(
                choices=[
                    ('general', 'Tư vấn chung'),
                    ('technical', 'Hỗ trợ kỹ thuật'),
                    ('sales', 'Kinh doanh / Báo giá'),
                    ('support', 'Hỗ trợ sau bán hàng'),
                    ('partnership', 'Hợp tác'),
                ],
                default='general',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='contactinquiry',
            name='status',
            field=models.CharField(
                choices=[
                    ('new', 'Mới'),
                    ('read', 'Đã đọc'),
                    ('replied', 'Đã trả lời'),
                    ('closed', 'Đã đóng'),
                ],
                db_index=True,
                default='new',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='demorequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('new', 'Mới'),
                    ('scheduled', 'Đã lên lịch'),
                    ('completed', 'Hoàn thành'),
                    ('cancelled', 'Đã hủy'),
                ],
                default='new',
                max_length=20,
            ),
        ),
    ]
