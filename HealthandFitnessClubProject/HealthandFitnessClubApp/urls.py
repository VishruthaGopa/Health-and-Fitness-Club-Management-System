from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='HealthandFitnessApp-login'),
    path('register/', views.register, name='HealthandFitnessApp-register'),
    #path('', views.home, name='HealthandFitnessApp-homepage'),
   
]