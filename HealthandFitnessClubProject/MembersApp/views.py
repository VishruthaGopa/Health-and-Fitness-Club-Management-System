from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
from HealthandFitnessClubProject.databaseConnection import connect


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
    
    

# Create your views here.
def update_profile(request, user_id):
    return request()