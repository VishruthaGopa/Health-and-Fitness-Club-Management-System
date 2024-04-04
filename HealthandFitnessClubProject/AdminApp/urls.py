from django.urls import path
from . import views

urlpatterns = [
    path('home/<int:user_id>/', views.home, name='AdminApp-home'),
    path('updateProfile/<int:user_id>/', views.updateProfile, name='AdminApp-update_profile'),
    path('members/<int:user_id>/', views.display_members, name='AdminApp-display_members'),
    path('rooms/<int:user_id>/', views.display_room_bookings, name='AdminApp-display_room_bookings'),
    path('personalTraining/<int:user_id>/', views.display_personal_fitness_classes, name='AdminApp-display_personal_training'),
    path('groupFitness/<int:user_id>/', views.display_group_fitness, name='AdminApp-display_group_fitness'),
    path('cancel_personal_training/<int:session_id>/<int:user_id>/', views.cancel_personal_training, name='AdminApp-cancel_personal_training'),
    path('cancel_group_fitness/<int:class_id>/<int:user_id>/', views.cancel_group_fitness, name='AdminApp-cancel_group_fitness'),
    path('equipmentMaintenance/<int:user_id>/', views.display_equipment_maintenance, name='AdminApp-equipment_maintenance'),
    path('updateEquipment/<int:equipment_id>/<int:user_id>/', views.update_equipment, name='AdminApp-update_equipment'),
    path('submitEquipmentUpdate/<int:equipment_id>/<int:user_id>/', views.submit_equipment_update, name='AdminApp-submit_equipment_update'),
    path('addMember/<int:user_id>/', views.addMember, name='AdminApp-addMember'),
    path('refundPersonalTraining/<int:session_id>/<int:user_id>/', views.refundPersonalTraining, name='AdminApp-refund'),
    path('trainers/<int:user_id>/', views.display_trainers, name='AdminApp-trainers'),
    path('addTrainer/<int:user_id>/', views.addTrainer, name='AdminApp-addTrainer'),
    path('deleteEquipment/<int:equipment_id>/<int:user_id>/', views.deleteEquipment, name='AdminApp-deleteEquipment'),
    path('addEquipment/<int:user_id>/', views.addEquipment, name='AdminApp-addEquipment'),
]   

