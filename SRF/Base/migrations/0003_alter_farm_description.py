# Generated by Django 5.1 on 2024-11-05 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_alter_farmer_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
