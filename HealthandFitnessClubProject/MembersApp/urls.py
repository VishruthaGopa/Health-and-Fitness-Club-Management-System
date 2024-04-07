from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [  
    path('homePage/<int:user_id>', views.homePage, name='MembersApp-homepage'),
    path('groupFitnessClasses/<int:user_id>', views.groupFitnessClasses, name='groupFitnessClasses'),  
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('updateProfile/<int:user_id>', views.update_profile, name='updateProfile'),
    path('groupFitnessClasses/<int:user_id>', views.groupFitnessClasses, name='groupFitnessClasses'),
    path('personalTrainingSessions/<int:user_id>', views.personalTrainingSessions, name='personalTrainingSessions'),

    path('update_health_statistics/<int:user_id>', views.update_Health_Statistics, name='update_health_statistics'),
    path('update_exercise_routine/<int:user_id>', views.update_exercise_routine, name='update_exercise_routine'),
    path('add_fitness_goal/<int:user_id>', views.add_fitness_goal, name='add_fitness_goal'),
    path('edit_exercise_routine/<int:user_id>', views.edit_exercise_routine, name='edit_exercise_routine'),

    path('create_exercise_routine/<int:user_id>', views.create_exercise_routine, name='create_exercise_routine'),
    path('create_fitness_goal/<int:user_id>', views.create_fitness_goal, name='create_fitness_goal'),

    path('delete_exercise_routine/<int:user_id>', views.delete_exercise_routine, name='delete_exercise_routine'),
    path('delete_fitness_goal/<int:user_id>', views.delete_fitness_goal, name='delete_fitness_goal'),

    
    path('book_classes/<int:user_id>', views.bookClasses, name='book_classes'),
    path('book_personal_training_session/<int:user_id>/', views.bookPersonalTrainingSession, name='book_personal_training_session'),
    path('get_payment_info/<int:user_id>', views.getPaymentInfo, name='get_payment_info'),
    
    path('remove_class', views.removeClass, name='remove_class'),
    path('remove_personal_training_session', views.removeSession, name='remove_personal_training_session'),
   
]