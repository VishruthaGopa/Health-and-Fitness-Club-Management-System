from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2
from django.contrib.auth import authenticate
from HealthandFitnessClubProject.databaseConnection import connect

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
                
                # Get the user's role and ID
                user_info = get_user_info(username)
                print("User ID:", user_info['user_id'])  # Print user ID

                # Redirect based on user role
                if user_info['role'] == 'member':
                    return redirect('HealthandFitnessApp-homepage', user_id=user_info['user_id'])
                elif user_info['role'] == 'trainer':
                    return redirect('TrainerApp-trainer_profile', user_id=user_info['user_id'])
                elif user_info['role'] == 'admin':
                    return redirect('AdminApp-home') 

            else:
                print("Incorrect username or password.")
                message = "Incorrect username or password."

        else:
            print("Username and password are required for login.")
            message = "Username and password are required for login."
    return render(request, 'HealthandFitnessClubApp/login.html', {'message': message})

# Create your views here.
def homePage(request, user_id):
    return render(request, 'HealthandFitnessClubApp/homePage.html', {'user_id': user_id,})

def get_user_info(username):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, role FROM \"User\" WHERE username = %s", [username])
    row = cursor.fetchone()
    if row:
        user_id, role = row
        return {'user_id': user_id, 'role': role}
    else:
        return None

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


# # Connect to PostgreSQL database
# def connect():
#     try:
#         # Update the database connection details to match your PostgreSQL configuration 
#         connection = psycopg2.connect(
#             host="localhost",
#             database="fitnessManagement_db",
#             user="postgres",
#             password="postgres"
#         )
#         #print("Connected to the database successfully.")
#         return connection
    
#     except psycopg2.Error as e:
#         print("Unable to connect to the database.")
#         print(e)
