from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2

# Create your views here.
def members(request, user_id):
    print("member view")
    print("MV - Trainer ID:", user_id)  # Print user ID
    search_query = request.GET.get('search', '')  # Get the search query from the request
    users = displayMembers(search_query)  # Pass the search query to displayMembers
    print(users)  # testing
    return render(request, 'TrainerApp/members.html', { 'user_id': user_id,'users': users})

# Display the Members table with optional search query
def displayMembers(search_query=None):
    connection = connect()
    cursor = connection.cursor()
    if search_query:  # Check if search_query is not empty
        # ILIKE operator to search for names containing the search query -> not case-sensitive
        cursor.execute("SELECT * FROM \"User\" WHERE role = 'member' AND username ILIKE %s", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM \"User\" WHERE role = 'member'")
    users = cursor.fetchall()
    connection.close()
    return users


def trainer_profile(request, user_id):
    # Execute the query with the form data
    connection = connect()
    cursor = connection.cursor()
    print("Trainer ID:", user_id)  # Print user ID

    if request.method == 'POST':
        save_trainer_profile(request, user_id)        
    
    # Retrieve trainer's profile information from the database
    trainer_data = get_trainer_data(user_id)

    # Define all specializations
    all_specializations = ['Cardio', 'Weightlifting', 'Yoga', 'Pilates', 'Crossfit', 'Kickboxing']

    # Create a dictionary to hold whether each specialization is selected for the trainer
    selected_specializations = {spec: spec in trainer_data[4] for spec in all_specializations}
    print(selected_specializations)
            
    return render(request, 'TrainerApp/trainer_profile.html', {
        'user_id': user_id,
        'trainer_data': trainer_data,
        'all_specializations': all_specializations,
        'selected_specializations': selected_specializations
    })

def save_trainer_profile(request, user_id):
    connection = connect()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        specializations = request.POST.getlist('specialization')  # Retrieve list of selected specializations

        # Execute SQL query to check if trainer exists
        cursor.execute("SELECT COUNT(*) FROM Trainer WHERE trainer_id = %s", [user_id])
        trainer_exists = cursor.fetchone()[0]

        # SQL query to update or insert data into the Trainer table
        if trainer_exists:
            cursor.execute("""
                UPDATE Trainer 
                SET first_name = %s, last_name = %s, email = %s, phone_number = %s, specializations = %s
                WHERE trainer_id = %s
            """, [first_name, last_name, email, phone, specializations, user_id])
        else:
            cursor.execute("""
                INSERT INTO Trainer (trainer_id, first_name, last_name, email, phone_number, specializations)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [user_id, first_name, last_name, email, phone, specializations])

        connection.commit()

def get_trainer_data(trainer_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
            SELECT first_name, last_name, email, phone_number, specializations
            FROM Trainer
            WHERE trainer_id = %s
        """, [trainer_id])
    trainer_data =  cursor.fetchone()
    print(trainer_data)
    return trainer_data

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
