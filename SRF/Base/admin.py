from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(Crop)
admin.site.register(Resources)
admin.site.register(HealthReport)
admin.site.register(FarmReport)
