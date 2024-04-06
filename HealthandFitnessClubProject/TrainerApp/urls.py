from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),    
    path('viewMembers/<int:user_id>/', views.members, name='TrainerApp-viewMembers'),
    path('trainer_profile/<int:user_id>/', views.trainer_profile, name='TrainerApp-trainer_profile'),
    path('sessions_classes/<int:user_id>/', views.sessions_classes, name='TrainerApp-sessions_classes'),

    path('fetch_available_times/<int:user_id>/', views.fetch_available_times, name='TrainerApp-fetch_available_times'),

]