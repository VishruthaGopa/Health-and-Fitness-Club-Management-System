from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),    
    path('viewMembers/<int:user_id>/', views.members, name='TrainerApp-viewMembers'),
    path('trainer_profile/<int:user_id>/', views.trainer_profile, name='TrainerApp-trainer_profile'),
    path('sessions_classes/<int:user_id>/', views.sessions_classes, name='TrainerApp-sessions_classes'), #View already booked Sessions and Classes

    # Adding Class Forms
    path('addClass/<int:user_id>/', views.addClass, name='TrainerApp-addClass'),
    path('secondSectionForm/<int:user_id>/', views.secondSectionForm, name='TrainerApp-secondSectionForm'),
    path('thirdSectionForm/<int:user_id>/', views.thirdSectionForm, name='TrainerApp-thirdSectionForm'),
    path('updateClassDB/<int:user_id>/', views.updateClassDB, name='TrainerApp-updateClassDB'),

    # Adding Session Forms
    path('addSession/<int:user_id>/', views.addSession, name='TrainerApp-addSession'),
    path('secondSectionForm-Session/<int:user_id>/', views.secondSectionForm_Session, name='TrainerApp-secondSectionForm-Session'),
    path('thirdSectionForm-Session/<int:user_id>/', views.thirdSectionForm_Session, name='TrainerApp-thirdSectionForm-Session'),
    path('updateSessionDB-Session/<int:user_id>/', views.updateSessionDB, name='TrainerApp-updateSessionDB-Session'),

    # Cancel Session
    path('cancel-session/<int:user_id>/<int:session_id>/', views.cancel_session, name='TrainerApp-cancelSession'),

    #Cancel Class
    path('cancel-class/<int:user_id>/<int:class_id>/', views.cancel_class, name='TrainerApp-cancelClass'),

]
