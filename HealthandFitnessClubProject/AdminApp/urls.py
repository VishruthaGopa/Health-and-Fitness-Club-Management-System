from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='AdminApp-home'),
    path('about/', views.about, name='AdminApp-about'),
    path('members/', views.display_members, name='AdminApp-display_members'),
    path('rooms/', views.display_room_bookings, name='AdminApp-display_room_bookings'),
    path('personalTraining/', views.display_personal_fitness_classes, name='AdminApp-display_personal_training'),
    path('groupFitness/', views.display_group_fitness, name='AdminApp-display_group_fitness'),
    path('cancel_personal_training/<int:session_id>/', views.cancel_personal_training, name='AdminApp-cancel_personal_training'),
    path('cancel_group_fitness/<int:class_id>/', views.cancel_group_fitness, name='AdminApp-cancel_group_fitness'),
]