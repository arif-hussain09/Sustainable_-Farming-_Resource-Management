# forms.py

from django import forms
from .models import Farmer, Farm, Resources, Crop, FarmReport, HealthReport
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resources
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
         'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class FarmerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'contact', 'profile_picture', 'performance', 'farms']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'performance': forms.NumberInput(attrs={'class': 'form-control'}),
            'farms': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }



class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'weather_condition', 'soil_type', 'crops', 'description', 'size']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'weather_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'soil_type': forms.TextInput(attrs={'class': 'form-control'}),
            'crops': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class ResourcesForm(forms.ModelForm):
    class Meta:
        model = Resources
        exclude = ['farm']
        widgets = {
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity_imported': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_used': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_stored': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'crop_image', 'crop_type', 'growing_season', 'yield_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop name'}),
            'crop_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'crop_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop type'}),
            'growing_season': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter growing season'}),
            'yield_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter yield amount'}),
        }

class FarmReportForm(forms.ModelForm):
    class Meta:
        model = FarmReport
        fields = ['farm', 'report_date', 'report_details']
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'report_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'report_details': forms.Textarea(attrs={'class': 'form-control'}),
        }

class HealthReportForm(forms.ModelForm):
    class Meta:
        model = HealthReport
        fields = ['farm', 'report_date', 'crop_health', 'soil_health', 'water_availability']
        widgets = {
            'farm': forms.Select(attrs={'class': 'form-control'}),
            'report_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'crop_health': forms.TextInput(attrs={'class': 'form-control'}),
            'soil_health': forms.TextInput(attrs={'class': 'form-control'}),
            'water_availability': forms.TextInput(attrs={'class': 'form-control'}),
        }

