from django.shortcuts import render, redirect
from django.http import HttpResponse
from HealthandFitnessClubProject.databaseConnection import connect
from datetime import datetime

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


def sessions_classes(request, user_id):
    # Fetch personal sessions using the helper function
    personal_sessions = fetch_personal_sessions(user_id)

    # Fetch classes using the helper function
    classes = fetch_classes(user_id)

    return render(request, 'TrainerApp/sessions_classes.html', {'user_id': user_id, 'personal_training_sessions': personal_sessions, 'group_classes': classes})


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


def fetch_available_times(selected_date):
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


def fetch_available_rooms(selected_date, selected_time):
    # Establish connection
    connection = connect()
    cursor = connection.cursor()

    #  SQL query to fetch available rooms for the selected date, time
    sql_query = """
        SELECT room_id, room_name, room_location
        FROM Room_Bookings
        WHERE date = %s AND time = %s AND booked = false
        ORDER BY room_id;
    """

    # Execute the query
    cursor.execute(sql_query, (selected_date, selected_time))

    # Fetch all available rooms with their details
    available_rooms = [{
        'room_id': row[0],
        'room_name': row[1],
        'room_location': row[2]
    } for row in cursor.fetchall()]

    # Close the database connection
    connection.close()

    return available_rooms


#
#
# ADDING FITNESS CLASSES
#
#
def addClass(request, user_id):
    # Fetch available dates from Room_Bookings table
    available_dates = fetch_available_dates()
    print("Available Dates:", available_dates)
    
    room_bookings = None
    #room_bookings = fetch_available_room_bookings()
    #print("room booking" , room_bookings)

    return render(request, 'TrainerApp/add_class.html', {'user_id': user_id, 'available_dates': available_dates, 'room_bookings': room_bookings})

def secondSectionForm(request, user_id):
    if request.method == 'POST':
        # Access form data
        class_name = request.POST.get('class_name')
        description = request.POST.get('description')
        date = request.POST.get('date')

        # Print out the form data
        print("Class Name:", class_name)
        print("Description:", description)
        print("Date:", date)

        # Convert the selected date to SQL format (YYYY-MM-DD)
        selected_date_obj = datetime.strptime(date, "%B %d, %Y")
        sql_formatted_date = selected_date_obj.strftime("%Y-%m-%d")
        print("Selected Date (SQL format):", sql_formatted_date)

        #Fetch available times
        available_times = fetch_available_times(sql_formatted_date)
        print("Available Times:", available_times)

        return render(request, 'TrainerApp/secondSectionForm.html', {'user_id': user_id, 'available_times': available_times, 'class_name': class_name, 'description': description, 'date': sql_formatted_date})

    return render(request, 'TrainerApp/secondSectionForm.html', {'user_id': user_id})

def thirdSectionForm(request, user_id):
    if request.method == 'POST':
        # Access form data
        class_name = request.POST.get('class_name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Print out the form data
        print("Class Name:", class_name)
        print("Description:", description)
        print("Date:", date)
        print("Time:", time)
        
        # Remove dots from the time string
        time = time.replace('.', '')

        # Convert time to SQL format (HH:MM:SS)
        time = datetime.strptime(time, "%I %p")
        time = time.strftime("%H:%M:%S")
        print("Time:", time)

        #Fetch available rooms
        available_rooms = fetch_available_rooms(date, time)
        print("Available Rooms:", available_rooms)

        return render(request, 'TrainerApp/thirdSectionForm.html', {'user_id': user_id, 'available_rooms': available_rooms, 'class_name': class_name, 'description': description, 'date': date, 'time': time})
    
    return render(request, 'TrainerApp/thirdSectionForm.html', {'user_id': user_id})

def updateClassDB(request, user_id):
    if request.method == 'POST':
        # Access form data
        class_name = request.POST.get('class_name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        room_id = request.POST.get('room')  # Retrieve the selected room ID

        # Print out the form data
        print("Trainer ID:", user_id)
        print("Class Name:", class_name)
        print("Description:", description)
        print("Date:", date)
        print("Time:", time)
        print("Room ID:", room_id)  # Print out the selected room ID

        connection = connect()
        cursor = connection.cursor()

        # SQL query to insert class details into Group_Fitness_Classes table
        insert_query = """
        INSERT INTO Group_Fitness_Classes (trainer_id, room_id, class_name, description, session_date, session_time) 
        VALUES (%s, %s, %s, %s, %s, %s);

        """
        cursor.execute(insert_query, (user_id, room_id, class_name, description, date, time))

        # SQL query to update Room_Bookings table to mark the room as booked
        update_query = """
        UPDATE Room_Bookings
        SET booked = true
        WHERE room_id = %s AND date = %s AND time = %s
        """
        cursor.execute(update_query, (room_id, date, time))
        connection.commit()

    # Redirect to sessions_classes page after updating
    return redirect('TrainerApp-sessions_classes', user_id=user_id)





#
#
# ADDING PERSONAL SESSIONS
#
#
def addSession(request, user_id):
    # Fetch available dates from Room_Bookings table
    available_dates = fetch_available_dates()
    print("Available Dates:", available_dates)

    return render(request, 'TrainerApp/add_session.html', {'user_id': user_id, 'available_dates': available_dates})

def secondSectionForm_Session(request, user_id):
    if request.method == 'POST':
        # Access form data
        price = request.POST.get('price')
        date = request.POST.get('date')

        # Print out the form data
        print("Price:", price)
        print("Date:", date)

        # Convert the selected date to SQL format (YYYY-MM-DD)
        selected_date_obj = datetime.strptime(date, "%B %d, %Y")
        sql_formatted_date = selected_date_obj.strftime("%Y-%m-%d")
        print("Selected Date (SQL format):", sql_formatted_date)

        #Fetch available times
        available_times = fetch_available_times(sql_formatted_date)
        print("Available Times:", available_times)

        return render(request, 'TrainerApp/secondSectionForm-Session.html', {'user_id': user_id, 'available_times': available_times, 'price': price, 'date': sql_formatted_date})

    return render(request, 'TrainerApp/secondSectionForm-Session.html', {'user_id': user_id})

def thirdSectionForm_Session(request, user_id):
    if request.method == 'POST':
        # Access form data
        price = request.POST.get('price')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Print out the form data
        print("Price:", price)
        print("Date:", date)
        print("Time:", time)
        
        # Remove dots from the time string
        time = time.replace('.', '')

        # Convert time to SQL format (HH:MM:SS)
        time = datetime.strptime(time, "%I %p")
        time = time.strftime("%H:%M:%S")
        print("Time:", time)

        #Fetch available rooms
        available_rooms = fetch_available_rooms(date, time)
        print("Available Rooms:", available_rooms)

        return render(request, 'TrainerApp/thirdSectionForm-Session.html', {'user_id': user_id, 'available_rooms': available_rooms, 'price': price, 'date': date, 'time': time})
    
    return render(request, 'TrainerApp/thirdSectionForm-Session.html', {'user_id': user_id})


def updateSessionDB(request, user_id):
    if request.method == 'POST':
        # Access form data
        price = request.POST.get('price')
        date = request.POST.get('date')
        time = request.POST.get('time')
        room_id = request.POST.get('room')

        # Print out the form data
        print("Trainer ID:", user_id)
        print("Price:", price)
        print("Date:", date)
        print("Time:", time)
        print("Room ID:", room_id)

        connection = connect()
        cursor = connection.cursor()

        # SQL query to insert personal session details into Personal_Training_Sessions table
        insert_query = """
        INSERT INTO Personal_Training_Sessions (trainer_id, session_date, session_time, room_id, price) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, date, time, room_id, price))

        # SQL query to update Room_Bookings table to mark the room as booked
        update_query = """
        UPDATE Room_Bookings
        SET booked = true
        WHERE room_id = %s AND date = %s AND time = %s
        """
        cursor.execute(update_query, (room_id, date, time))
        connection.commit()

    # Redirect to sessions_classes page after updating
    return redirect('TrainerApp-sessions_classes', user_id=user_id)
