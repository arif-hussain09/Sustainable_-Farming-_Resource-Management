from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('crop/<str:crop_name>/',views.Crops,name='crop'),
    path('crops/',views.All_Crops,name='crops'),
    path('resources/',views.Resource,name='resources'),
    path('resourceForm/',views.Resource_Form,name='resourceForm'),
    path('farmers/<uuid:farmer_id>/',views.Farmers,name='farmer_profile'),
    path('farm/<uuid:farm_id>/add-resource/', views.Resource_Form, name='add_resource'),
    path('farmers/',views.Farmer_list,name='farmer_list'),
    path('farms/',views.Farms,name='farms'),
    path('farm/<uuid:farm_id>',views.Farms_,name='farm'),
    path('update-farmForm/<uuid:farm_id>',views.Update_Farm_Form,name='update-farmForm'),
    path('farm_report/<uuid:farm_id>',views.Farm_report,name='farm_report'),
    path('get_resource_data/<uuid:farm_id>/', views.get_resource_data, name='get_resource_data'),

    path('health_report/<uuid:farm_id>',views.Health_report,name='health_report'),
 
    path('farmerForm/',views.Farmer_Form,name='farmerForm'),
    path('update-farmerForm/<uuid:farmer_id>/',views.Update_Farmer_Form,name='update-farmerForm'),
    path('cropForm/',views.Crop_Form,name='cropForm'),
    path('farmForm/',views.Farm_Form,name='farmForm'),
    path('farmReportForm/',views.Farm_Report_Form,name='farmReportForm'),
    path('healthReportForm/',views.Health_Report_Form,name='healthReportForm'),
    # path('Farmer_login/',views.Login_Page,name='Farmer_login'),
    # path('Farmer_signup/',views.Registration_Page,name='Farmer_signup'),
    
    
]
