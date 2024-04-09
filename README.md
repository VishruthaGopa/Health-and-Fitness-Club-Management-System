# Health and Fitness Club Management System

## Overview
This application implements a Health and Fitness Club Management System using Django, a Python web framework. It provides functionalities for members, trainers, and administrators to manage various aspects of the fitness club, including user registration, profile management, scheduling, and administrative tasks.

## Features

### Members
- Profile management
- Dashboard displaying fitness progress
- Schedule personal training sessions and group fitness classes

### Trainers
- Profile management
- Search for member profiles
- Manage and add personal training sessions and group fitness classes

### Administrators
- Profile management
- Manage room bookings and equipment maintenance
- Update class schedules

## Prerequisites
Ensure that the following are installed:
- Django
- PostgreSQL
- Python

## Setup
1. **Database Setup**:
   - Create a PostgreSQL database called `fitnessManagement_db`.
   - Use the DDL file (`ddl.sql`) to create the schema for the database.

2. **Populate Database**:
   - Use the DML file (`dml.sql`) to populate the database with sample data.

3. **Configure Database Connection**:
   - Navigate to the `databaseConnection.py` file located in the `HealthandFitnessClubProject` directory.
   - Update the database connection details in `databaseConnection.py` to match your PostgreSQL configuration.
4. **Run the Application**:
   - Open a terminal and navigate to the `HealthandFitnessClubProject` directory.
   - Run the command `python manage.py runserver` to start the Django development server.
5. **Access the Application**:
   - Open a web browser and go to http://localhost:8000/ to access the application.

## Testing
- Members can register using the registration page.
- Use the following credentials to access trainer functionalities:
    - Username: trainer1, Password: trainerpassword1
    - Username: trainer2, Password: pass2
- Use the following credentials to access admin functionalities:
    - Username: admin1, Password: adminpassword1
    - Username: admin2, Password: adminpass2

## Bonus Features
The web application includes a recommendation system that suggests trainers and their specializations based on user fitness goals.

## YouTube Link
[Insert YouTube link here]

## Contributors:
- Vishrutha Gopa
- Nermeen El-Sherbiny
- Rimsha Atif
