# Generated by Django 5.1 on 2024-11-03 12:33

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('crop_type', models.CharField(max_length=100)),
                ('growing_season', models.CharField(max_length=100)),
                ('yield_amount', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('farm_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('weather_condition', models.CharField(max_length=100)),
                ('soil_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('size', models.DecimalField(decimal_places=3, max_digits=10)),
                ('crops', models.ManyToManyField(blank=True, related_name='farms', to='Base.crop')),
            ],
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('farmer_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=15)),
                ('profile_picture', models.ImageField(upload_to='farmers/')),
                ('performance', models.DecimalField(decimal_places=2, max_digits=5)),
                ('farms', models.ManyToManyField(blank=True, related_name='farmers', to='Base.farm')),
            ],
        ),
        migrations.CreateModel(
            name='FarmReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField()),
                ('report_details', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_reports', to='Base.farm')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='HealthReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField()),
                ('crop_health', models.CharField(max_length=50)),
                ('soil_health', models.CharField(max_length=50)),
                ('water_availability', models.CharField(max_length=50)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_reports', to='Base.farm')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(max_length=50)),
                ('quantity_imported', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity_used', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity_available', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity_stored', models.DecimalField(decimal_places=2, max_digits=10)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='Base.farm')),
            ],
        ),
    ]
