from django.shortcuts import render,HttpResponse,redirect ,get_object_or_404
from django.contrib.auth import authenticate, login
from .froms import CustomLoginForm
from .froms import CustomUserCreationForm ,FarmerRegistrationForm , FarmForm ,ResourcesForm,CropForm ,FarmReportForm,HealthReportForm
from django.contrib.auth.forms import UserCreationForm 
from django.db.models import Q,Sum
from django.contrib import messages
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse  # Import reverse to dynamically build URLs
import requests

from .models import *


def Home(request):
    q = request.GET.get('q', "").strip()  # Set default to empty string and strip whitespace
    
    # Filter farmers based on search query and fetch related farms
    farmers = Farmer.objects.filter(
        Q(name__icontains=q) |
        Q(farmer_id__icontains=q) |
        Q(performance__icontains=q) |
        Q(farms__name__icontains=q)
    ).distinct().prefetch_related('farms')  # Efficiently fetch of distinct farmers with the related farms 

    farms = Farm.objects.all()
    crops = set()
    farm_data = {}

    for farm in farms:
        crop_yields = {}
        for crop in farm.crops.all():
            crop_yields[crop.name] = float(crop.yield_amount)  # Assuming yield_kg is the attribute for crop yield
                                                            # also converting the value  decimal to float formate for javascript usage
            crops.add(crop.name)
        farm_data[farm.name] = crop_yields

# formating the farms beacuse the are as query set
    formatted_farms=[farm.name  for farm in farms]

    context = {
        'Farmers':farmers,
        'farm_data': farm_data,
        'farms':formatted_farms,
        'crops': list(crops),
        'Farmers': farmers,
    }

    return render(request, 'Base/home.html', context=context)


def Farmers(request,farmer_id):
    
     # Use get_object_or_404 to get the farmer by farmer_id
    _farmer = get_object_or_404(Farmer, farmer_id=farmer_id)

    # Fetch the farms related to this farmer
    farms = Farm.objects.filter(farmers=_farmer)   # in Farm have many-to-many relationship with farmer
                                                    #related name -farmers
   
    context={
        'farmer':_farmer,
        'farms':farms,
    }
    return render(request,'Base/farmers.html',context=context)

    
def Delete_page(request):
    ...

# For all the farms
def Farms(request):
    farms=Farm.objects.all()

    crops=Crop.objects.all().distinct()
    total_farm=Farm.objects.count()
    total_area=Farm.objects.aggregate(Sum('size'))['size__sum']  # as return a dictionary key:size__sum and value is our total area
    
    
    farms_with_yield=Farm.objects.annotate(total_yield=Sum('crops__yield_amount'))
    total_yield = farms_with_yield.aggregate(total_yield_sum=Sum('total_yield'))['total_yield_sum'] or 0
    
    
     # Calculate the total yield for each crop across all farms
    crop_yields = Crop.objects.annotate(total_yield=Sum('farms__crops__yield_amount')).order_by('name')

    # Prepare crop names and their corresponding yields
    crop_names = [crop.name for crop in crop_yields]
    crop_yield_values = [float(crop.yield_amount) if crop.yield_amount else 0 for crop in crop_yields]

    total_yield = sum(crop_yield_values)
    context={
        'Farms':farms,
        'Crops':crops,
        'Total_farm':total_farm,
        'Total_area':total_area,
        'Total_yield':total_yield,
        'Crop_yields':crop_yield_values,
        'Crop_names':crop_names,
    }


    return render(request,'Base/farms.html',context=context)
def Farmer_list(request):
    farmers=Farmer.objects.all()
    context={
        'farmers':farmers,
    }
    return render(request,"Base/farmer_list.html",context=context)
def Farms_(request,farm_id):
    _farm=get_object_or_404(Farm, farm_id=farm_id)
    latest_farm_report=_farm.farm_reports.first()
    latest_health_report=_farm.health_reports.first()
    context={
        'Farm':_farm,
        'latest_farm_report':latest_farm_report,
        'latest_health_report':latest_health_report,
    }

    return render(request,'Base/farm.html',context=context)
    ...
def Crops(request,crop_name):
    crop=get_object_or_404(Crop,name=crop_name)
     # Wikipedia API to get additional information
       # Wikipedia API to get crop information
    wiki_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{crop.name}"
    wiki_response = requests.get(wiki_api_url).json()

    # Extract information
    description = wiki_response.get("extract", "Description not available.")
    image_url = wiki_response.get("thumbnail", {}).get("source", "")
    page_url = wiki_response.get("content_urls", {}).get("desktop", {}).get("page", "")
    history_api_url = f"https://en.wikipedia.org/api/rest_v1/page/related/{crop.name}"
    
    # Fetch history-related content
    history_response = requests.get(history_api_url).json()
    history_info = history_response.get("pages", [{}])[0].get("extract", "Historical information not available.")

    # Context for template rendering
    context = {
        'crop': crop,
        'description': description,
        'wiki_image_url': image_url,
        'wiki_page_url': page_url,
        'history_info': history_info
    }

    return render(request, 'Base/crop.html',context=context)

def All_Crops(request):
    crops=Crop.objects.all()

    context={
        'crops':crops,

    }
    return render(request,'Base/Crops.html',context=context)
def Resource(request):
    resource=Resources.objects.all()
    farms=Farm.objects.prefetch_related('resources').all()

    context={
        'Resource':resource,
        'Farms':farms,
    }
    return render(request, 'Base/resources.html',context=context)

def Farm_report(request, farm_id):
    farm = get_object_or_404(Farm, farm_id=farm_id)
    resources = farm.resources.all()
    # Fetch unique resource types for dropdown
    resource_types = resources.values_list('resource_type', flat=True).distinct()
    context = {
        'Farm': farm,
        'resource_types': list(resource_types),
    }
    return render(request, 'Base/farm_report.html', context=context)

# AJAX Handler for resource data

def get_resource_data(request, farm_id):
    resource_type = request.GET.get('resource_type')
    if not resource_type:
        return JsonResponse({'success': False, 'message': 'Resource type not specified'})

    try:
        # Filter by farm ID (UUID) and resource type
        resource = Resources.objects.filter(farm__farm_id=farm_id, resource_type=resource_type).first()
        if resource:
            data = [
                float(resource.quantity_imported),
                float(resource.quantity_used),
                float(resource.quantity_available),
                float(resource.quantity_stored),
            ]
            return JsonResponse({'success': True, 'resource_data': {'type': resource_type, 'data': data}})
        else:
            return JsonResponse({'success': False, 'message': 'No data found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def Health_report(request,farm_id):
    health_reports=HealthReport.objects.filter(farm_id=farm_id)
    farm=Farm.objects.filter(farm_id=farm_id)
    try:
        # Attempt to get the most recent health report
        recent_health_report = HealthReport.objects.latest('report_date')
    except HealthReport.DoesNotExist:
        # If no health report exists, set to None
        recent_health_report = None
    context={
        "Farm":farm,
        "Health_reports":health_reports,
        "Recent_Health_report":recent_health_report,
    }
    return render(request,'Base/health_report.html',context=context)

def Farmer_Form(request):
    
    form=FarmerRegistrationForm()

    if request.method=="POST":
        form=FarmerRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    context={
            'Form':form,
        }

    return render(request,"Base/farmerForm.html",context=context)


def Update_Farmer_Form(request,farmer_id):
    farmer=get_object_or_404(Farmer,farmer_id=farmer_id)
    form=FarmerRegistrationForm(instance=farmer)
    if request.method=="POST":
        form=FarmerRegistrationForm(request.POST,request.FILES,instance=farmer)
        if form.is_valid():
            form.save()
             # Redirect to the specific farmer's profile page
            return redirect(reverse('farmer_profile', kwargs={'farmer_id': farmer_id}))
    context={
        'form':form,
    }
    return render(request,"Base/farmForm.html",context=context)


def Crop_Form(request):
    form=CropForm()
    if request.method=="POST":
        form=CropForm(request.POST,request.FILES)
        # Checking is the form is valid or not
        if form.is_valid():
            form.save()
            return redirect('home')
    context={
        "Form":form,
    }

    return render(request,"Base/cropForm.html",context=context)

def Update_Crop_Form(request,crop_name):
    crop=get_object_or_404(Crop,name=crop_name)
    form=CropForm(instance=crop)
    if request.method=="POST":
        form=CropForm(request.POST ,instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop', crop_name=crop_name)    
    context={
        'Form':form,
    }
    return render(request,"Base/cropForm.html",context=context)


def Farm_Form(request):
    form=FarmForm()
    if request.method=="POST":
        form=FarmForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    context={
        'form':form,
    }

    return render(request,"Base/farmForm.html",context=context)

def Update_Farm_Form(request,farm_id):
    farm=get_object_or_404(Farm,farm_id=farm_id)
    form=FarmForm(instance=farm)
    if request.method=="POST":
        form=FarmForm(request.POST,request.FILES ,instance=farm)

        if form.is_valid():
            form.save()
        return redirect(reverse('farm', kwargs={'farm_id': farm_id}))
    context={
        'form':form,
    }
    return render(request,'Base/farmForm.html',context=context)

def Resource_Form(request,farm_id):
    # Get the farm object based on the farm_id passed in the URL
    farm = get_object_or_404(Farm, farm_id=farm_id)

    if request.method == 'POST':
        form = ResourcesForm(request.POST)
        if form.is_valid():
            # Set the farm to the one from the URL
            form.instance.farm = farm

            resource_type = form.cleaned_data['resource_type']
            quantity_imported = form.cleaned_data['quantity_imported']
            
            # Check if the resource already exists for the selected farm
            resource, created = Resources.objects.get_or_create(
                farm=farm,
                resource_type=resource_type,
                defaults={
                    'quantity_imported': quantity_imported,
                    'quantity_used': form.cleaned_data['quantity_used'],
                    'quantity_available': form.cleaned_data['quantity_available'],
                    'quantity_stored': form.cleaned_data['quantity_stored']
                }
            )

            # If resource already exists, just update the imported quantity
            if not created:
                resource.quantity_imported += quantity_imported
                resource.save()

            messages.success(request, f"Resource '{resource_type}' for farm '{farm.name}' has been updated!")
            return redirect('farm', farm_id=farm_id)  # Redirect back to farm profile
    else:
        form = ResourcesForm()

    return render(request, 'Base/resourcesForm.html', {'form': form, 'farm': farm})


def Farm_Report_Form(request):
    form=FarmReportForm()
    if request.method=="POST":
        form=FarmReportForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    context={
        'form':form,
    }

    return render(request,"Base/farmReportForm.html",context=context)
def Health_Report_Form(request):
    form=HealthReportForm()
    if request.method=="POST":
        form=HealthReportForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    context={
        'form':form,
    }

    return render(request,"Base/healthReportForm.html",context=context)



