from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),    
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('updateProfile/<int:user_id>', views.update_profile, name='updateProfile'),
    path('groupFitnessClasses/<int:user_id>', views.groupFitnessClasses, name='groupFitnessClasses'),
    path('personalTrainingSessions/<int:user_id>', views.personalTrainingSessions, name='personalTrainingSessions'),
    path('book_classes/<int:user_id>', views.bookClasses, name='book_classes'),
    path('remove_class', views.removeClass, name='remove_class'),
]