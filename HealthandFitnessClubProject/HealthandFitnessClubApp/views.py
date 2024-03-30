from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2

# Create your views here.
def home(request):
    message = None  # Initialize message var

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)
        print("Password:", password)

        # Check if both username and password are not empty
        if username and password:
            # Call the login_user function to verify credentials
            if login_user(username, password):
                # Redirect to the updateProfile page if login is successful
                return redirect('HealthandFitnessApp-updateProfile')
            else:
                print("Incorrect username or password.")
                message = "Incorrect username or password."

        else:
            print("Username and password are required for login.")
            message = "Username and password are required for login."


    return render(request, 'HealthandFitnessClubApp/login.html', {'message': message})


def register(request):
    message = None  # Initialize message variable

    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        print("New Username:", new_username)
        print("New Password:", new_password)

        # Check if both username and password are not empty
        if new_username and new_password:
            # Call the register_user function to register the new user
            registration_status = register_user(new_username, new_password)
            if registration_status:
                message = "Registration successful. You can now login."
            else:
                message = "Username already exists. Please choose a different username."
        else:
            message = "Username and password are required for registration."

    return render(request, 'HealthandFitnessClubApp/register.html', {'message': message})

def updateProfile(request):
    return render(request, 'HealthandFitnessClubApp/updateProfile.html')


# Function to log in a user
def login_user(username, password):
    connection = connect()
    cursor = connection.cursor()

    # Check if the username and password match
    cursor.execute('SELECT * FROM \"User\" WHERE username = %s AND password = %s', (username, password))
    if cursor.fetchone() is not None:
        print("Login successful!")
        connection.close()
        return True
    else:
        connection.close()
        return False


# Function to register a new user (default is member)
def register_user(username, password):
    connection = connect()
    cursor = connection.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM "User" WHERE username = %s', (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print('Username already exists. Please choose a different username.')
        connection.close()
        return False
    
    # Insert the new user into the User table (default role member)
    cursor.execute("INSERT INTO \"User\" (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()
    print("Member registered successfully.")
    connection.close()
    return True


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
