from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AdoptionApplicationForm,
    LostFoundForm,
    RegistrationForm,
    RescueReportForm,
    VolunteerApplicationForm,
)
from .models import AdoptionApplication, Animal, LostFound, RescueReport, VolunteerApplication


def home(request):
    animals = Animal.objects.filter(adoption_status='Available')[:6]
    rescue_reports = RescueReport.objects.exclude(status='Closed')[:6]
    return render(request, 'home.html', {'animals': animals, 'rescue_reports': rescue_reports})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your account was created successfully. Please log in.')
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f'Welcome back, {form.get_user().username}.')
        return redirect('dashboard')
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    context = {
        'rescue_reports': RescueReport.objects.filter(user=request.user),
        'adoption_applications': AdoptionApplication.objects.filter(user=request.user).select_related('animal'),
        'lost_found_reports': LostFound.objects.filter(user=request.user),
        'volunteer_applications': VolunteerApplication.objects.filter(user=request.user),
    }
    return render(request, 'dashboard.html', context)


def rescue(request):
    reports = RescueReport.objects.exclude(status='Closed')
    form = RescueReportForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        form = RescueReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Your rescue report was submitted successfully.')
            return redirect('rescue')
    return render(request, 'rescue.html', {'reports': reports, 'form': form})


def adopt(request):
    animals = Animal.objects.filter(adoption_status='Available')
    return render(request, 'adopt.html', {'animals': animals})


@login_required
def apply_to_adopt(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    if AdoptionApplication.objects.filter(user=request.user, animal=animal).exists():
        messages.info(request, 'You have already applied to adopt this animal.')
        return redirect('adopt')
    form = AdoptionApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.animal = animal
        try:
            application.save()
        except IntegrityError:
            messages.info(request, 'You have already applied to adopt this animal.')
        else:
            messages.success(request, 'Your adoption application was submitted.')
        return redirect('dashboard')
    return render(request, 'adoption_apply.html', {'animal': animal, 'form': form})


def lost_found(request):
    reports = LostFound.objects.all()
    report_type = request.GET.get('type', '')
    search = request.GET.get('q', '').strip()
    if report_type in ('Lost', 'Found'):
        reports = reports.filter(report_type=report_type)
    if search:
        reports = reports.filter(animal_name__icontains=search) | reports.filter(animal_type__icontains=search) | reports.filter(location__icontains=search)
    form = LostFoundForm(initial={'report_type': report_type} if report_type in ('Lost', 'Found') else None)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        form = LostFoundForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Your lost and found report was submitted.')
            return redirect('lost-found')
    return render(request, 'lost_found.html', {'reports': reports.distinct(), 'form': form, 'report_type': report_type, 'search': search})


def volunteer(request):
    form = VolunteerApplicationForm(request.POST or None)
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    if request.method == 'POST' and form.is_valid():
        if VolunteerApplication.objects.filter(user=request.user, status='Pending').exists():
            messages.info(request, 'You already have an active volunteer application.')
        else:
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Your volunteer application was submitted.')
        return redirect('dashboard')
    return render(request, 'volunteer.html', {'form': form})


def about(request):
    return render(request, 'about.html')