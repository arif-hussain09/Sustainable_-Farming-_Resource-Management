# Generated by Django 5.1 on 2024-11-07 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0004_alter_crop_yield_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='crop_image',
            field=models.ImageField(blank=True, null=True, upload_to='crops/'),
        ),
    ]