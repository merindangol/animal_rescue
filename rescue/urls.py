from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rescue/', views.rescue, name='rescue'),
    path('adopt/', views.adopt, name='adopt'),
    path('adopt/<int:animal_id>/apply/', views.apply_to_adopt, name='apply-to-adopt'),
    path('lost-found/', views.lost_found, name='lost-found'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('about/', views.about, name='about'),
]