# Generated by Django 5.1 on 2024-08-17 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_event_existing_data_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_image',
            field=models.ImageField(blank=True, default='static/images/アイコン.png', null=True, upload_to='static/images/', verbose_name='イベント画像'),
        ),
    ]
