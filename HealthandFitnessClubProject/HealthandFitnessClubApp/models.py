from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20, default='member')

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

class Member_Health(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
    start_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

class Fitness_Goals(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
    weight_goal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    time_goal = models.IntegerField(blank=True, null=True)
    diet_goal = models.TextField(blank=True, null=True)
    form_of_exercise = models.TextField(blank=True, null=True)

class Exercise_Routine(models.Model):
    routine_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    routine_name = models.CharField(max_length=50)
    description = models.TextField()
    duration = models.DurationField()
    date_created = models.DateField()

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20)

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    specializations = models.TextField()

class Room_Bookings(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=50)
    room_location = models.CharField(max_length=50)
    booked = models.BooleanField(default=False)
    time = models.TimeField()
    date = models.DateField()
    duration = models.DurationField()

class Personal_Training_Sessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    session_date = models.DateField()
    session_time = models.TimeField()
    duration = models.DurationField()
    room = models.ForeignKey(Room_Bookings, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.BooleanField(default=False)

class Group_Fitness_Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room_Bookings, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    description = models.TextField()
    session_date = models.DateField()
    session_time = models.TimeField()
    member_ids = models.ManyToManyField(Member)

class Equipment_Maintenance(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=100)
    last_maintained_date = models.DateField()
    next_maintenance = models.DateField()
    performed_by = models.ForeignKey(Admin, on_delete=models.CASCADE)

