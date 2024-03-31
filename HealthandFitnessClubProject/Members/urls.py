from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),    
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('updateProfile/<int:user_id>', views.update_profile, name='updateProfile'),

]