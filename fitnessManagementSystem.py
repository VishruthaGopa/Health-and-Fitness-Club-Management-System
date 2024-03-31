# import the connect function
from databaseConnection import connect

# Display the User table
def displayAllUsers():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM \"User\"")
    users = cursor.fetchall()

    print("\nUser Table:")
    print("-----------------------------------------------------------------------")
    print("| {:<10} | {:<20} | {:<20} | {:<20} |".format("user_id", "username", "password", "role"))
    print("--------------------------------------------------------")
    
    for user in users:
        user_id, username, password, role = user
        print("| {:<10} | {:<20} | {:<20} | {:<20} |".format(user_id, username, password, role))
    
    print("-----------------------------------------------------------------------")
    connection.close()

# Register a new user (default is member)
def register_user(username, password):
    connection = connect()
    cursor = connection.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM \"User\" WHERE username = %s', (username,))
    if cursor.fetchone() is not None:
        print('Username already exists. Please choose a different username.')
        return
    
    # Insert the new user into the User table (default role member)
    cursor.execute("INSERT INTO \"User\" (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()
    print("Member registered successfully.")
    connection.close()

# Login user
def login_user(username, password):
    connection = connect()
    cursor = connection.cursor()

    # Check if the username and password match
    cursor.execute('SELECT * FROM \"User\" WHERE username = %s AND password = %s', (username, password))
    if cursor.fetchone() is not None:
        print("Login successful!")
    else:
        print("Incorrect username or password.")
    
    connection.close()


# Main menu
def main_menu():
    while True:
        print("\nWelcome to Fitness Management System!")
        print("1. Register")
        print("2. Login")
        print("3. View Users")
        print("4. Exit")
        choice = input("Please choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)
        elif choice == "3":
            displayAllUsers()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Main
def main():
    main_menu()

main()
