from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2

# Create your views here.
def members(request):
    print("member view")
    users = displayMembers()
    print(users)  # testing
    
    return render(request, 'TrainerApp/members.html', {'users': users})

# Display the Members table
def displayMembers():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM \"User\" where role = 'member'")
    users = cursor.fetchall()
    connection.close()
    return users

# Connect to PostgreSQL database
def connect():
    try:
        # Update the database connection details to match your PostgreSQL configuration 
        connection = psycopg2.connect(
            host="localhost",
            database="fitnessManagement_db",
            user="postgres",
            password="postgres"
        )
        #print("Connected to the database successfully.")
        return connection
    
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
