from xmlrpc.client import Boolean
from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
from HealthandFitnessClubProject.databaseConnection import connect
from django.shortcuts import render, redirect
from django.contrib import messages


def homePage(request, user_id):
    user_health_data = HealthStatistics(request, user_id)
    user_exercise_routines = ExerciseRoutines(request, user_id)
    return render(request, 'MembersApp/homePage.html', {
        'user_id': user_id,
        'user_data': user_health_data,
        'user_exercise_routines': user_exercise_routines
    })

def ExerciseRoutines(request, user_id):
    # Execute the query with the form data
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
            SELECT routine_id, routine_name, description, duration, date_created
            FROM exercise_routine
            WHERE member_id = %s
        """, [user_id])
    user_exercise_routines = cursor.fetchall()
    # Convert the list of tuples to a list of dictionaries
    user_exercise_routines_dicts = []
    for routine in user_exercise_routines:
        routine_dict = {
            'routine_id': routine[0],
            'routine_name': routine[1],
            'description': routine[2],
            'duration': routine[3],
            'date_created': routine[4]
        }
    user_exercise_routines_dicts.append(routine_dict)

    
    return user_exercise_routines_dicts

def HealthStatistics(request, user_id):
    # Execute the query with the form data
    connection = connect()
    cursor = connection.cursor()

    # if request.method == 'POST':
    #     update_HealthStatistics(request, user_id) 

    cursor.execute("""
            SELECT start_weight, current_weight, height, age
            FROM Member_Health
            WHERE member_id = %s
        """, [user_id])
    user_health_data = cursor.fetchone()
    print(user_health_data)
    # Pass the query result to the template context
    return user_health_data

def update_Health_Statistics(request, user_id):
    if request.method == 'POST':
        start_weight = request.POST.get('start_weight')
        current_weight = request.POST.get('current_weight')
        height = request.POST.get('height')
        age = request.POST.get('age')

        # Execute the query to update the health statistics in the database
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Member_Health
            SET start_weight = %s, current_weight = %s, height = %s, age = %s
            WHERE member_id = %s
        """, [start_weight, current_weight, height, age, user_id])
        connection.commit()

        # Redirect to the home page after updating the health statistics
        return redirect('MembersApp-homepage', user_id=user_id)

def update_exercise_routine(request, user_id):
    if request.method == 'POST':
        start_weight = request.POST.get('start_weight')
        current_weight = request.POST.get('current_weight')
        height = request.POST.get('height')
        age = request.POST.get('age')

        # Execute the query to update the health statistics in the database
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Member_Health
            SET start_weight = %s, current_weight = %s, height = %s, age = %s
            WHERE member_id = %s
        """, [start_weight, current_weight, height, age, user_id])
        connection.commit()

        # Redirect to the home page after updating the health statistics
        return redirect('MembersApp-homepage', user_id=user_id)

    

def profile(request, user_id):
    # Execute the query with the form data
    connection = connect()
    cursor = connection.cursor()


    if request.method == 'POST':
        update_profile(request, user_id)        
    
   
     # Retrieve users's profile information from the database
    user_data = get_user_info(request, user_id)
    
            
    return render(request, 'MembersApp/profile.html', {
        'user_id': user_id,
        'user_data': user_data
    })

def get_user_info(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
            SELECT first_name, last_name, gender, email, address, phone_number, start_date, payment_status
            FROM Member
            WHERE member_id = %s
        """, [user_id])
    user_data =  cursor.fetchone()
    cursor.execute("SELECT username FROM \"User\" WHERE user_id = %s", [user_id])
    username = cursor.fetchone()
     # Check if both user_data and username exist
    if user_data and username:
        # Create a dictionary with keys and values
        user_info = {
            'username': username[0],
            'first_name': user_data[0],
            'last_name': user_data[1],
            'gender': user_data[2],
            'email': user_data[3],
            'address': user_data[4],
            'phone_number': user_data[5],
            'start_date': user_data[6],
            'payment_status': user_data[7]
        }

        return user_info
    

def update_profile(request, user_id):
    connection = connect()
    cursor = connection.cursor()

    #Get updates information
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    gender = request.POST.get('gender')
    email = request.POST.get('email')
    address = request.POST.get('address')
    phone_number = request.POST.get('phone_number')
    start_date = request.POST.get('start_date')
    payment_status = request.POST.get('payment_status')

    cursor.execute("""
    UPDATE Member
    SET first_name = %s, last_name = %s, gender = %s, email = %s, address = %s, phone_number = %s, start_date = %s, payment_status = %s
    WHERE member_id = %s""", 
    [first_name, last_name, gender, email, address, phone_number, start_date, payment_status, user_id])
    connection.commit()

    # Add a success message
    messages.success(request, "Profile information has been updated successfully.")

    # Redirect to the profile page with the updated data and success message
    return redirect('profile', user_id=user_id)
    
def groupFitnessClasses(request, user_id):
    connection = connect()
    cursor = connection.cursor()

    # Retrieve classes that the member has enrolled in
    cursor.execute("""
        SELECT class_id, class_name, session_date, session_time
        FROM Group_Fitness_Classes
        WHERE %s = ANY(member_ids)
    """, [user_id])
    enrolled_classes = cursor.fetchall()

    # Retrieve all available classes
    cursor.execute("""
        SELECT class_id, class_name, description, session_date, session_time
        FROM Group_Fitness_Classes
    """)
    all_classes = cursor.fetchall()

    return render(request, 'MembersApp/groupFitnessClasses.html', {
        'user_id':user_id,
        'enrolled_classes': enrolled_classes,
        'all_classes': all_classes
    })
    #return render(request, 'MembersApp/groupFitnessClasses.html', {'user_id': user_id,})


def bookClasses(request, user_id):
    connection = connect()
    cursor = connection.cursor()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        selected_class_ids = request.POST.getlist('classes')
        # Logic to book selected classes using selected_class_ids
        # For example, update the database to add the user_id to the selected classes
        if selected_class_ids:
            for class_id in selected_class_ids:
            # Check if the member is not already enrolled in the class
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Group_Fitness_Classes
                    WHERE class_id = %s AND %s = ANY(member_ids)
                """, [class_id, user_id])
                already_enrolled = cursor.fetchone()[0]

                if not already_enrolled:
                    # Update Group_Fitness_Classes to add user_id to the class_id
                    cursor.execute("""
                        UPDATE Group_Fitness_Classes
                        SET member_ids = array_append(member_ids, %s)
                        WHERE class_id = %s;
                    """, [user_id, class_id])
                    connection.commit()
                    messages.success(request, "The class has been booked successfully!")
                else:
                    messages.success(request, "You have already registered for this class!")
            connection.close()
        else:
            messages.success(request, "No classes have been selected.")
    return redirect('groupFitnessClasses', user_id=user_id)

def removeClass(request):
    connection = connect()
    cursor = connection.cursor()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        cursor.execute("""
            UPDATE Group_Fitness_Classes
            SET member_ids = array_remove(member_ids, %s)
            WHERE class_id = %s;
        """, [user_id, request.POST.get('class_id')])
        connection.commit()
        messages.success(request, "The booking has been canceled.")
        connection.close()
     
    return redirect('groupFitnessClasses', user_id=user_id)

def personalTrainingSessions(request, user_id):
    connection = connect()
    cursor = connection.cursor()

    # Retrieve classes that the member has enrolled in
    cursor.execute("""
        SELECT session_id, trainer_id, session_date, session_time, room_id
        FROM personal_training_sessions
        WHERE member_id = %s
    """, [user_id])
    enrolled_sessions = cursor.fetchall()

    # Retrieve all available classes
    cursor.execute("""
        SELECT session_id, trainer_id, session_date, session_time, room_id, price, duration
        FROM personal_training_sessions WHERE member_id is NULL
    """)
    available_sessions = cursor.fetchall()

     # Retrieve all classes
    cursor.execute("""
        SELECT session_id, trainer_id, session_date, session_time, room_id, price, duration
        FROM personal_training_sessions 
    """)
    all_sessions = cursor.fetchall()

        # Create a dictionary to map trainer IDs to trainer names for available sessions
    trainer_names = {}
    for session in all_sessions:
        if session[1] not in trainer_names:
            cursor.execute("""SELECT first_name, last_name FROM trainer WHERE trainer_id = %s""", [session[1]])
            trainer_name = " ".join(cursor.fetchone())  # Concatenate first_name and last_name
            trainer_names[session[1]] = trainer_name

    # Update the enrolled sessions and available sessions with trainer names
    updated_enrolled_sessions = []
    for session in enrolled_sessions:
        updated_session = list(session)
        updated_session[1] = trainer_names.get(session[1], 'Unknown Trainer')
        updated_enrolled_sessions.append(updated_session)

    updated_all_sessions = []
    for session in available_sessions:
        updated_session = list(session)
        updated_session[1] = trainer_names.get(session[1], 'Unknown Trainer')
        updated_all_sessions.append(updated_session)

    connection.close()

    return render(request, 'MembersApp/personalTrainingSessions.html', {
        'user_id': user_id,
        'booked_sessions': updated_enrolled_sessions,
        'all_sessions': updated_all_sessions
    })

def bookPersonalTrainingSession(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    
    if request.method == 'POST':
        paid = request.POST.get('paid')
        if paid == "False":
        # Verify payment and get the response
            payment_verification_response = verifyPayment(request, user_id, request.POST.get('session_id'))
            
            # Check if the response is a rendered template
            if isinstance(payment_verification_response, HttpResponse):
                # Return the rendered template response
                return payment_verification_response
    
        selected_session_id = request.POST.get('session_id')
        # Logic to book selected classes using selected_class_ids
        # For example, update the database to add the user_id to the selected classes
        if selected_session_id:
            cursor.execute("""
                UPDATE personal_training_sessions
                SET member_id =  %s
                WHERE session_id = %s;
            """, [user_id, selected_session_id])
            connection.commit()
            messages.success(request, "The session has been booked successfully!")
        connection.close()
    return redirect('personalTrainingSessions', user_id=user_id)

def verifyPayment(request, user_id, session_id):
    context = {
        'user_id': user_id,
        'session_id': session_id
    }
    return render(request, 'MembersApp/payment_info.html', context)

def getPaymentInfo(request, user_id):
    if request.method == 'POST':
        # Process the payment information here
        # Once the payment is confirmed, call bookPersonalTrainingSession
        
        return bookPersonalTrainingSession(request, user_id)
    else:
        return HttpResponse("Invalid request method")

        

def removeSession(request):
    connection = connect()
    cursor = connection.cursor()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        cursor.execute("""
            UPDATE personal_training_sessions
            SET member_id = NULL
            WHERE session_id = %s;
        """, [ request.POST.get('session_id')])
        connection.commit()
        messages.success(request, "The booking has been canceled.")
        connection.close()
     
    return redirect('personalTrainingSessions', user_id=user_id)