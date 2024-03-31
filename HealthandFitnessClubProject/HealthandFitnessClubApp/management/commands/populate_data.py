from django.core.management.base import BaseCommand
from HealthandFitnessClubApp.models import User, Member, Member_Health, Fitness_Goals, Exercise_Routine, Admin, Trainer, Room_Bookings, Personal_Training_Sessions, Group_Fitness_Classes, Equipment_Maintenance

class Command(BaseCommand):
    help = 'Populate tables with sample data'

    def handle(self, *args, **kwargs):
        # Insert sample data into User table
        user1 = User.objects.create(username='user1', password='pass1', role='member')
        user2 = User.objects.create(username='user2', password='pass2', role='member')
        admin1 = User.objects.create(username='admin1', password='adminpassword1', role='admin')
        trainer_user = User.objects.create(username='trainer1', password='trainerpassword1', role='trainer')

        # Insert sample data into Trainer table
        trainer1 = Trainer.objects.create(user=trainer_user, first_name='Trainer', last_name='Johnson', email='trainer@example.com', phone_number='9998887777', specializations='{Weightlifting, Yoga}')

        # Insert sample data into Member table
        member1 = Member.objects.create(user=user1, member_id=1, first_name='John', last_name='Doe', gender='Male', email='john@example.com', date_of_birth='1990-01-01', address='123 Main St, City', phone_number='1234567890', start_date='2024-01-01', payment_status=True)
        member2 = Member.objects.create(user=user2, member_id=2, first_name='Jane', last_name='Doe', gender='Female', email='jane@example.com', date_of_birth='1995-05-05', address='456 Elm St, Town', phone_number='0987654321', start_date='2024-02-15', payment_status=True)

        Member_Health.objects.create(member=member1, start_weight=80.5, current_weight=75.2, height=180, age=34)
        Member_Health.objects.create(member=member2, start_weight=65.2, current_weight=63.0, height=165, age=29)

        # Insert sample data into the Fitness_Goals table
        Fitness_Goals.objects.create(member=member1, weight_goal=70.0, time_goal=6, diet_goal='Eat healthier meals', form_of_exercise='{Cardio, Weightlifting}')
        Fitness_Goals.objects.create(member=member2, weight_goal=60.0, time_goal=3, diet_goal='Cut down on sugar intake', form_of_exercise='{Yoga, Pilates}')

        # Insert sample data into the Exercise_Routine table
        Exercise_Routine.objects.create(member=member1, routine_name='Morning Cardio', description='30 minutes of running', duration='30 minutes', date_created='2024-01-10')
        Exercise_Routine.objects.create(member=member2, routine_name='Evening Yoga', description='Relaxing yoga session', duration='45 minutes', date_created='2024-02-20')

        # Insert sample data into the Admin table
        Admin.objects.create(user=admin1, first_name='Admin', last_name='Smith', email='admin@example.com', phone_number='1112223333')

        # Insert sample data into the Room_Bookings table
        Room_Bookings.objects.create(room_name='Room 1', room_location='Main Building', booked=False, time='09:00:00', date='2024-03-25', duration='1 hour')
        Room_Bookings.objects.create(room_name='Room 2', room_location='Annex Building', booked=True, time='14:00:00', date='2024-03-25', duration='2 hours')

        # Manually set the many-to-many field for Group_Fitness_Classes
        group_class1 = Group_Fitness_Classes.objects.create(trainer=trainer1, room_id=1, class_name='Morning Yoga', description='Beginner-friendly yoga class', session_date='2024-03-28', session_time='08:00:00')
        group_class1.member_ids.set([member1.member_id, member2.member_id])

        group_class2 = Group_Fitness_Classes.objects.create(trainer=trainer1, room_id=2, class_name='Pilates Core Workout', description='Strengthen your core with pilates', session_date='2024-03-29', session_time='16:00:00')
        group_class2.member_ids.set([member2.member_id])
