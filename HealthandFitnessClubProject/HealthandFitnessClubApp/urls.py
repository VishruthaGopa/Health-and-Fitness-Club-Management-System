from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='HealthandFitnessApp-homepage'),
    path('updateProfile/', views.updateProfile, name='HealthandFitnessApp-updateProfile'),
]