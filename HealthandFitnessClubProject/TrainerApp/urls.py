from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),    
    path('viewMembers', views.members, name='TrainerApp-viewMembers'),
    path('', views.trainer_profile, name='TrainerApp-trainer_profile'),
]