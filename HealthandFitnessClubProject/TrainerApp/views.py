from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2
from HealthandFitnessClubProject.databaseConnection import connect

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
        cursor.execute("""
            SELECT 
                U.*, 
                M.email, 
                CONCAT(M.first_name, ' ', M.last_name) AS full_name, 
                M.gender, 
                M.date_of_birth 
            FROM 
                "User" U 
            INNER JOIN 
                Member M ON U.user_id = M.member_id 
            WHERE 
                U.role = 'member' AND 
                (U.username ILIKE %s OR 
                M.first_name ILIKE %s OR 
                M.last_name ILIKE %s)
        """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("""
            SELECT 
                U.*, 
                M.email, 
                CONCAT(M.first_name, ' ', M.last_name) AS full_name, 
                M.gender, 
                M.date_of_birth 
            FROM 
                "User" U 
            INNER JOIN 
                Member M ON U.user_id = M.member_id 
            WHERE 
                U.role = 'member'
        """)
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


# Define a helper function to execute the SQL query and fetch data
def fetch_personal_sessions(user_id):
    # Establish connection
    connection = connect()
    cursor = connection.cursor()

    # SQL query
    sql_query = """
        SELECT 
            PTS.session_id, 
            CONCAT(M.first_name, ' ', M.last_name) AS member_name,
            PTS.session_date, 
            PTS.session_time, 
            PTS.duration, 
            RB.room_name, 
            RB.room_location, 
            PTS.price,
            PTS.payment_status 
        FROM 
            Personal_Training_Sessions PTS 
        JOIN 
            Trainer TR ON PTS.trainer_id = TR.trainer_id 
        LEFT OUTER JOIN 
            Member M ON PTS.member_id = M.member_id 
        JOIN 
            Room_Bookings RB ON PTS.room_id = RB.room_id
        WHERE 
            PTS.trainer_id = %s;
    """

    # Execute the query with the given user_id
    cursor.execute(sql_query, (user_id,))

    # Fetch all records
    personal_sessions = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Return fetched data
    return personal_sessions

# Define a helper function to execute the SQL query and fetch classes
def fetch_classes(user_id):
    # Establish connection
    connection = connect()
    cursor = connection.cursor()

    # SQL query
    sql_query = """
        SELECT 
            GFC.class_name,
            GFC.description,
            GFC.session_date, 
            GFC.session_time, 
            RB.room_name, 
            RB.room_location,
            ARRAY_AGG(CONCAT(M.first_name, ' ', M.last_name)) AS member_names
        FROM 
            Group_Fitness_Classes GFC
        JOIN 
            Trainer TR ON GFC.trainer_id = TR.trainer_id 
        JOIN 
            Room_Bookings RB ON GFC.room_id = RB.room_id
        LEFT JOIN 
            Member M ON M.member_id IN (SELECT UNNEST(GFC.member_ids))
        WHERE 
            GFC.trainer_id = %s
        GROUP BY 
            GFC.class_name,
            GFC.description,
            GFC.session_date, 
            GFC.session_time, 
            RB.room_name, 
            RB.room_location;

    """

    # Execute the query with the given user_id
    cursor.execute(sql_query, (user_id,))

    # Fetch all records
    classes = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Return fetched data
    return classes


# Define a helper function to fetch available dates, times, and rooms based on Room_Bookings table
def fetch_availability():
    connection = connect()
    cursor = connection.cursor()

    # Fetch available dates, times, and rooms
    cursor.execute("""
        SELECT DISTINCT session_date FROM Room_Bookings
        WHERE session_date >= CURRENT_DATE
        ORDER BY session_date
    """)
    dates = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT session_time FROM Room_Bookings
        WHERE session_date >= CURRENT_DATE
        ORDER BY session_time
    """)
    times = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT room_id, room_name FROM Room_Bookings
        WHERE session_date >= CURRENT_DATE
        ORDER BY room_id
    """)
    rooms = cursor.fetchall()

    connection.close()

    return dates, times, rooms

# Define the view function
def sessions_classes(request, user_id):
    # Fetch personal sessions using the helper function
    personal_sessions = fetch_personal_sessions(user_id)

    # Fetch classes using the helper function
    classes = fetch_classes(user_id)

    selected_date = None  # Initialize selected_date variable

    if request.method == 'GET':
        selected_date = request.GET.get('session_date')  # Get the selected date from the form
        print("Request method:", request.method)  # Debug: Print request method
        print("GET data:", request.GET)  # Debug: Print entire GET data
        print("Selected Date:", selected_date)  # Debug: Print the selected date

    # Fetch available dates from Room_Bookings table
    available_dates = fetch_available_dates()

    return render(request, 'TrainerApp/sessions_classes.html', {'user_id': user_id, 'personal_training_sessions': personal_sessions, 'group_classes': classes, 'available_dates': available_dates})


# Define a helper function to fetch available dates from Room_Bookings table
def fetch_available_dates():
    # Establish connection
    connection = connect()
    cursor = connection.cursor()

    # SQL query to fetch distinct session dates
    sql_query = """
        SELECT DISTINCT date
        FROM Room_Bookings
        WHERE booked = false
        ORDER BY date;
    """

    # Execute the query
    cursor.execute(sql_query)

    # Fetch all distinct dates
    available_dates = [date[0] for date in cursor.fetchall()]

    # Close the database connection
    connection.close()

    # Return available dates
    return available_dates


def fetch_available_times(request):
    selected_date = request.GET['date']
        
    # Raw SQL query to fetch available times for the selected date
    sql_query = """
            SELECT DISTINCT time
            FROM Room_Bookings
            WHERE date = %s AND booked = false
            ORDER BY time;
        """
    # Establish connection
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(sql_query, [selected_date])         # Execute the SQL query
    available_times = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    connection.close()

    return available_times


def fetch_available_rooms(request, selected_date, selected_time):
    # Establish connection
    connection = connect()
    cursor = connection.cursor()

    #  SQL query to fetch available rooms for the selected date, time
    sql_query = """
        SELECT DISTINCT room_id
        FROM Room_Bookings
        WHERE date = %s AND time = %s AND booked = false
        ORDER BY room_id;
    """

    # Execute the query
    cursor.execute(sql_query, (selected_date, selected_time))

    # Fetch all distinct room IDs
    available_rooms = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    connection.close()

    return available_rooms
