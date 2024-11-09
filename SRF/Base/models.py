from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

# Create Farmer
class Farmer(models.Model):
    farmer_id=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name=models.CharField( max_length=100,null=False ,blank=False)
    contact=models.CharField(max_length=15)
    profile_picture=models.ImageField(upload_to="farmers/",blank=True ,null=True)

    # for traking the performance of farmer
    performance=models.DecimalField(max_digits=5, decimal_places=2)

    # Many to many relationship with farmers and farm
    farms = models.ManyToManyField('Farm', related_name='farmers', blank=True)
    
    def farm_count(self):
        return self.farms.count()
    
    def total_yield(self):
        return sum(crop.yield_amount  for farm in  self.farms.all() for crop  in farm.crops.all())
    
    def __str__(self):
        return f'Name: {self.name}'
# Create Farms
class Farm(models.Model):
    # Primary key
    farm_id=models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    weather_condition=models.CharField(max_length=100)
    soil_type=models.CharField(max_length=100)

    # many to many relationship of farms and crops
    crops = models.ManyToManyField('Crop', related_name='farms', blank=True)
    crop_picture=models.ImageField(upload_to="crops/",null=True , blank=True)
    # description about the farm
    description=models.TextField(blank=True , null=True)
    size=models.DecimalField(max_digits=10, decimal_places=3)

    def total_yield(self):
       
        return sum(crop.yield_amount for crop in self.crops.all())

    def __str__(self):
        return f'FarmName: { self.name}'
    
# Create Resources
class Resources(models.Model):
    RESOURCE_CHOICES = [
        ('fertilizer', 'Fertilizer'),
        ('equipment', 'Equipment'),
        ('water', 'Water'),
        ('seeds', 'Seeds'),
        ('pesticides', 'Pesticides'),
    ]
    
    farm = models.ForeignKey(Farm, related_name="resources", on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    quantity_imported = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_stored = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.resource_type} - {self.quantity_available} available'


# Crop
class Crop(models.Model):
    name=models.CharField(max_length=100)
    crop_image=models.ImageField(upload_to="crops/" ,blank=True ,null=True)
    crop_type=models.CharField(max_length=100)
    growing_season=models.CharField(max_length=100)
    yield_amount=models.DecimalField(max_digits=10 , decimal_places=3,default=0)

    def __str__(self):
        return f'CropName: { self.name}'

# Create Farm_report
class FarmReport(models.Model):
    farm = models.ForeignKey(Farm, related_name="farm_reports", on_delete=models.CASCADE)
    report_date=models.DateField()
    report_details=models.TextField()
    

    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']
# Create Health_report

class HealthReport(models.Model):
    farm = models.ForeignKey(Farm, related_name="health_reports", on_delete=models.CASCADE)
    report_date=models.DateField()
    crop_health=models.CharField( max_length=50)
    soil_health=models.CharField(max_length=50)
    water_availability=models.CharField(max_length=50)

    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']