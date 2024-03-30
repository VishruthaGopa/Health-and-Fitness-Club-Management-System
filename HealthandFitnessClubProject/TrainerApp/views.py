from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2

# Create your views here.
def members(request):
    print("member view")

    #return HttpResponse('<h1>Trainer Page</h1>')
    return render(request, 'TrainerApp/members.html')

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
