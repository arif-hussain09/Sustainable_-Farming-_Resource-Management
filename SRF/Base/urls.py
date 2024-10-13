from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('crops/',views.Crops,name='crops'),
    path('resources/',views.Resources,name='resources'),
    path('farmers/',views.Farmer,name='farmers'),
    path('farms/',views.Farms,name='farms'),
    
]
