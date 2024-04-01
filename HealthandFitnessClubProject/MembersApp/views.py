from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
from HealthandFitnessClubProject.databaseConnection import connect
from django.shortcuts import render, redirect
from django.contrib import messages



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
    