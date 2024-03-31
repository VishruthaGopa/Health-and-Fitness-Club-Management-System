from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2

# Create your views here.
def members(request):
    print("member view")
    search_query = request.GET.get('search', '')  # Get the search query from the request
    users = displayMembers(search_query)  # Pass the search query to displayMembers
    print(users)  # testing
    return render(request, 'TrainerApp/members.html', {'users': users})

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



def trainer_profile(request):
    # If this is a POST request, process the form data
    if request.method == 'POST':
        # Process your form data here, for example:
        # specialization = request.POST.get('specialization')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # phone = request.POST.get('phone')
        # Save the data to your model...
        
        # Redirect to a new URL, or indicate success
        return redirect('some-view-name')

    # If a GET (or any other method), just render the form
    return render(request, 'TrainerApp/trainer_profile.html')


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
