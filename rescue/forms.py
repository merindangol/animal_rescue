from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import AdoptionApplication, Animal, LostFound, RescueReport, VolunteerApplication


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class RescueReportForm(forms.ModelForm):
    class Meta:
        model = RescueReport
        fields = ('animal_name', 'animal_type', 'description', 'location', 'contact_number', 'image')
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ('message',)
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class LostFoundForm(forms.ModelForm):
    class Meta:
        model = LostFound
        fields = (
            'report_type', 'animal_name', 'animal_type', 'description', 'location',
            'date_lost_found', 'contact_number', 'image',
        )
        widgets = {
            'date_lost_found': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ('phone', 'availability', 'interests', 'experience', 'message')
        widgets = {
            'experience': forms.Textarea(attrs={'rows': 4}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ('name', 'animal_type', 'age', 'gender', 'description', 'location', 'image', 'health_status', 'adoption_status')
        widgets = {'description': forms.Textarea(attrs={'rows': 5})}
