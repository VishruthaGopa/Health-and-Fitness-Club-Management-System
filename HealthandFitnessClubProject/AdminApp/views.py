from django.shortcuts import render, redirect
import psycopg2
from HealthandFitnessClubProject.databaseConnection import connect

def home(request):
    return render(request, 'AdminApp/home.html', {'title':'home'})

def about(request):
    return render(request, 'AdminApp/about.html', {'title':'about'})


def display_personal_fitness_classes(request):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Personal_Training_Sessions")
    personal_sessions = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/personal_fitness_classes.html', {'personal_sessions': personal_sessions})

def display_room_bookings(request):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Room_Bookings")
    room_bookings = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/room_bookings.html', {'room_bookings': room_bookings})

def display_members(request):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Member")
    members = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/members.html', {'members': members})

def display_group_fitness(request):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Group_Fitness_Classes")
    group_fitness = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/group_fitness_classes.html', {'group_fitness' : group_fitness})
    
       
def cancel_group_fitness(request, class_id):
    if request.method == 'POST':
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Group_Fitness_Classes WHERE class_id = %s", [class_id])
            connection.close()
            return redirect('display_group_fitness')
        except Exception as e:
            pass  # Handle case where the class does not exist
    return redirect('AdminApp/display_group_fitness')


def cancel_personal_training(request, session_id):
    if request.method == 'POST':
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Personal_Training_Sessions WHERE session_id = %s", [session_id])
            connection.close()
            return redirect('display_group_fitness')
        except Exception as e:
            pass  # Handle case where the class does not exist
    return redirect('AdminApp/display_group_fitness')


