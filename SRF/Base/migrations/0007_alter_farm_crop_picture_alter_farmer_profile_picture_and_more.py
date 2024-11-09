# Generated by Django 5.1.3 on 2024-11-08 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0006_farm_crop_picture_alter_farmer_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='crop_picture',
            field=models.ImageField(blank=True, null=True, upload_to='crops/'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='farmers/'),
        ),
        migrations.AlterField(
            model_name='resources',
            name='resource_type',
            field=models.CharField(choices=[('fertilizer', 'Fertilizer'), ('equipment', 'Equipment'), ('water', 'Water'), ('seeds', 'Seeds'), ('pesticides', 'Pesticides')], max_length=50),
        ),
    ]