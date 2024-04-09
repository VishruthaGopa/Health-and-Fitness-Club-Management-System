from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),    
    path('viewMembers/<int:user_id>/', views.members, name='TrainerApp-viewMembers'),
    path('trainer_profile/<int:user_id>/', views.trainer_profile, name='TrainerApp-trainer_profile'),
    path('sessions_classes/<int:user_id>/', views.sessions_classes, name='TrainerApp-sessions_classes'),

    path('addSession/<int:user_id>/', views.addSession, name='TrainerApp-addSession'),
    path('addClass/<int:user_id>/', views.addClass, name='TrainerApp-addClass'),

]