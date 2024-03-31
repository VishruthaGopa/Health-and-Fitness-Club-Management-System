import psycopg2

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