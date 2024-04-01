from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='HealthandFitnessApp-login'),
    path('register/', views.register, name='HealthandFitnessApp-register'),
    path('homePage/<int:user_id>', views.homePage, name='HealthandFitnessApp-homepage'),
    path('members/', include('MembersApp.urls')),
]