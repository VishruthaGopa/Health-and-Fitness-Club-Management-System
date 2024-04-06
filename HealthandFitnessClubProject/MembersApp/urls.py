from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='HealthandFitnessApp-login'),  
    path('homePage/<int:user_id>', views.homePage, name='MembersApp-homepage'),
    path('update_health_statistics/<int:user_id>', views.update_Health_Statistics, name='update_health_statistics'),
    path('update_exercise_routine/<int:routine_id>', views.update_exercise_routine, name='update_exercise_routine'),
    path('groupFitnessClasses/<int:user_id>', views.groupFitnessClasses, name='groupFitnessClasses'),  
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('updateProfile/<int:user_id>', views.update_profile, name='updateProfile'),
    path('groupFitnessClasses/<int:user_id>', views.groupFitnessClasses, name='groupFitnessClasses'),
    path('personalTrainingSessions/<int:user_id>', views.personalTrainingSessions, name='personalTrainingSessions'),
    path('book_classes/<int:user_id>', views.bookClasses, name='book_classes'),
    path('remove_class', views.removeClass, name='remove_class'),
    path('book_personal_training_session/<int:user_id>/', views.bookPersonalTrainingSession, name='book_personal_training_session'),
    path('remove_personal_training_session', views.removeSession, name='remove_personal_training_session'),
    path('get_payment_info/<int:user_id>', views.getPaymentInfo, name='get_payment_info'),
]