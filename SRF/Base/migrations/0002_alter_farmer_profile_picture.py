# Generated by Django 5.1 on 2024-11-04 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='farmers/'),
        ),
    ]
