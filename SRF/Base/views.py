from django.shortcuts import render,HttpResponse

# Create your views here.

def Home(request):
    return render(request,'Base/home.html')
def Farmer(request):
    return render(request,'Base/farmers.html')
def Login_page(request):
    ...
def Delete_page(request):
    ...
def Farms(request):
    return render(request,'Base/farms.html')
    ...
def Crops(request):
    return render(request, 'Base/crop.html')
    ...
def Resources(request):
    return render(request, 'Base/resources.html')
    ...
