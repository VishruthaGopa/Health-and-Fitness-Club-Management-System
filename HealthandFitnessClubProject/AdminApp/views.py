from django.shortcuts import render, redirect
from HealthandFitnessClubProject.databaseConnection import connect
from django.contrib import messages



#trainer home and updating profile functions:
def home(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    #displays personal admin information
    cursor.execute("SELECT * FROM Admin WHERE admin_id = %s", [user_id])
    admin_data = cursor.fetchall()
    connection.close()


    return render(request, 'AdminApp/home.html', {'user_id': user_id, 'admin_data': admin_data})
 

#function that updates admin profile
def updateProfile(request, user_id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        try:
            #allows admin to update profile
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE Admin SET first_name = %s, last_name = %s, email = %s, phone_number=%s WHERE admin_id = %s",
                           [first_name, last_name, email, phone, user_id])
            connection.commit()
            connection.close()
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
            return redirect('AdminApp-home', user_id=user_id)

        return redirect('AdminApp-home', user_id=user_id)
    return redirect('AdminApp-home', user_id=user_id)




#Member related functions 

#Function that allows admins to add new member, must pay member starter fee as well
def addMember(request, user_id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        date_of_birth=request.POST.get('date_of_birth')
        address = request.POST.get('address')
        username=request.POST.get('username')

        try:
            connection = connect()
            cursor = connection.cursor()
            #makes them a user first with log in infromation
            cursor.execute('INSERT INTO "User" (username, password, role) VALUES (%s, %s, %s) RETURNING user_id', 
                   [username, 'defaultPassword', 'member'])
            member_id = cursor.fetchone()[0]
            connection.commit()
            
            #add them to the member table using the user_id
            cursor.execute('INSERT INTO Member (member_id, first_name, last_name, gender, ' +
               'email, date_of_birth, address, phone_number, payment_status) ' +
               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
               [member_id, first_name, last_name, gender, email, date_of_birth, address, phone, True])
            connection.commit()

            connection.close()
            return redirect('AdminApp-display_members', user_id=user_id)

        except Exception as e:
          messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
          return redirect('AdminApp-display_members', user_id=user_id)
    return render(request, 'AdminApp/addMember.html', {'user_id': user_id})


#displays the members for the admin
def display_members(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Member")
    members = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/members.html', {'members': members, 'user_id': user_id})




#personal training related functions 

#allows admin to refund the personal training session for the users, just clears
#out their name and changes payment status to unpaid
def refundPersonalTraining(request, session_id, user_id):
    if request.method == 'POST':
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE Personal_Training_Sessions SET member_id=%s, payment_status= false WHERE session_id=%s",[None, session_id])
            connection.commit()
            connection.close()
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Refund unsuccessful!")
            return redirect('AdminApp-display_personal_training', user_id=user_id)

        return redirect('AdminApp-display_personal_training', user_id=user_id)

    return redirect('AdminApp-display_personal_training', user_id=user_id)


#gives admin access to scheduled personal fitness classes
def display_personal_fitness_classes(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT PTS.session_id, TR.first_name AS trainer_first_name, TR.last_name AS trainer_last_name," +
                   "M.first_name AS member_first_name, M.last_name AS member_last_name,"+
                   "PTS.session_date, PTS.session_time, PTS.duration, RB.room_name, PTS.price,"+
                   "PTS.payment_status, RB.room_id FROM Personal_Training_Sessions PTS JOIN Trainer TR ON PTS.trainer_id = TR.trainer_id "+
                   "LEFT OUTER JOIN Member M ON PTS.member_id = M.member_id JOIN Room_Bookings RB ON PTS.room_id = RB.room_id;")
    personal_sessions = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/personal_fitness_classes.html', {'personal_sessions': personal_sessions, 'user_id': user_id})


#allows admin to cancel a personal training session
def cancel_personal_training(request, user_id, session_id):
    if request.method == 'POST':
        session_time=request.POST.get('session_time')

        session_date=request.POST.get('session_date')
        room_id=request.POST.get('room_id')


        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Personal_Training_Sessions WHERE session_id = %s", [session_id])
            
            #updates the room booking to false
            cursor.execute("UPDATE Room_Bookings SET booked = FALSE WHERE room_id = %s AND date = %s AND time = %s", [room_id, session_date, session_time])
            connection.commit()
            connection.close()
            return redirect('AdminApp-display_personal_training', user_id=user_id)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Cancellation unsuccessful!")
            return redirect('AdminApp-display_personal_training', user_id=user_id)
    return redirect('AdminApp-display_personal_training', user_id=user_id)


#allows admin to change the location of a personal training session
def updatePersonalTraining(request, session_id, user_id):
    if request.method == 'POST':
        try:
            #this if statment updates everything 
            # Extract the old room and the new room from the form data
            old_room = request.POST.get('room_id')
            new_room_id = request.POST.get('new_room_id')

            # Update the session with the new room and mark it as booked
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE Personal_Training_Sessions SET room_id = %s WHERE session_id = %s", [new_room_id, session_id])
            connection.commit()


            # Mark the old room as not booked
            cursor = connection.cursor()
            cursor.execute("UPDATE Room_Bookings SET booked = false WHERE room_id = %s", [old_room])
            connection.commit()
    

            cursor = connection.cursor()
            cursor.execute("UPDATE Room_Bookings SET booked = true WHERE room_id = %s", [new_room_id])
            connection.commit()
            connection.close()

        
            return redirect('AdminApp-display_personal_training', user_id=user_id)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
            return redirect('AdminApp-display_personal_training', user_id=user_id)
    else:
        #if its a get method, then it extracts information from the database about available rooms
        try:
            session_time = request.GET.get('session_time')

            #turns the time into something readable by the database
            session_hour=session_time.split()
            session_time=int(session_hour[0])+12
            session_time = f"{session_time}:00:00"

            session_date = request.GET.get('session_date')
            room_name=request.GET.get('room_name')
            room_id=request.GET.get('session_room')
            

            connection = connect()
            cursor = connection.cursor()

            # Query the database to find available rooms at the specified session time and date
            cursor.execute("SELECT room_id, room_name FROM Room_Bookings WHERE booked = false AND time = %s AND date = %s", [ session_time, session_date])
            available_rooms = cursor.fetchall()

            connection.close()
            return render(request, 'AdminApp/updatePersonal.html', {'user_id': user_id, 'available_rooms': available_rooms, 'session_id':session_id, 
                                                                    'session_date':session_date, 'session_time':session_time, 'room_name':room_name, 'room_id':room_id})
        except Exception as e:
            print('Error:', e)

    return redirect('AdminApp-display_personal_training', user_id=user_id)

        




#group fitness related functions

#display all scheduled group fitness classes
def display_group_fitness(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT GFC.class_id, T.first_name AS trainer_first_name, T.last_name AS trainer_last_name," +
                   "GFC.class_name, GFC.description, GFC.session_date, GFC.session_time," +
                   "RB.room_name, RB.room_id FROM Group_Fitness_Classes GFC JOIN Trainer T ON GFC.trainer_id = T.trainer_id JOIN Room_Bookings RB ON GFC.room_id = RB.room_id;")
    group_fitness = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/group_fitness_classes.html', {'group_fitness': group_fitness, 'user_id': user_id})


#allows admin to cancel a group fitness class if needed
def cancel_group_fitness(request, user_id, class_id):
    if request.method == 'POST':
        try:

            session_time=request.POST.get('session_time')


            session_date=request.POST.get('session_date')
            room_id=request.POST.get('session_room')

            connection = connect()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Group_Fitness_Classes WHERE class_id = %s", [class_id])
           #room gets changed to not booked
            cursor.execute("UPDATE Room_Bookings SET booked = FALSE WHERE room_id = %s AND date = %s AND time = %s", [room_id, session_date, session_time])
            connection.commit()
            connection.close()
            return redirect('AdminApp-display_group_fitness', user_id=user_id)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Cancellation unsuccessful!")
            return redirect('AdminApp-display_group_fitness', user_id=user_id)
    return redirect('AdminApp-display_group_fitness', user_id=user_id)


#allows admin to change the room of a group fitness class
def updateGroupFitness(request, class_id, user_id):
    if request.method == 'POST':
        #this if statment takes user input and updates the rooms as well as the class
        try:
            # Extract the old room and the new room from the form data
            old_room = request.POST.get('room_id')
            new_room_id = request.POST.get('new_room_id')

            # Update the session with the new room and mark it as booked
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE Group_Fitness_Classes SET room_id = %s WHERE class_id = %s", [new_room_id, class_id])
            connection.commit()


            # Mark the old room as not booked
            cursor = connection.cursor()
            cursor.execute("UPDATE Room_Bookings SET booked = false WHERE room_id = %s", [old_room])
            connection.commit()
    

            cursor = connection.cursor()
            cursor.execute("UPDATE Room_Bookings SET booked = true WHERE room_id = %s", [new_room_id])
            connection.commit()
            connection.close()

    
            return redirect('AdminApp-display_group_fitness', user_id=user_id)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
            return redirect('AdminApp-display_group_fitness', user_id=user_id)
    else:
        #this statment for the get method extracts infromation from the database about room availability 
        try:

            session_time = request.GET.get('session_time')
            #turns the time into something readable by the database 
            session_hour=session_time.split()
            session_time=int(session_hour[0])+12
            session_time = f"{session_time}:00:00"

            session_date = request.GET.get('session_date')
            room_name=request.GET.get('room_name')
            room_id=request.GET.get('session_room')

            connection = connect()
            cursor = connection.cursor()

            # Query the database to find available rooms at the specified session time and date
            cursor.execute("SELECT room_id, room_name FROM Room_Bookings WHERE booked = false AND time = %s AND date = %s", [ session_time, session_date])
            available_rooms = cursor.fetchall()
    

            connection.close()
            return render(request, 'AdminApp/updateGroup.html', {'user_id': user_id, 'available_rooms': available_rooms, 'class_id':class_id, 
                                                                    'session_date':session_date, 'session_time':session_time, 'room_name':room_name, 'room_id':room_id})
        except Exception as e:
            print(e)

    return redirect('AdminApp-display_group_fitness', user_id=user_id)

        





#room booking functions

#admin can see the room availablity and booking status
def display_room_bookings(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Room_Bookings")
    room_bookings = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/room_bookings.html', {'room_bookings': room_bookings, 'user_id': user_id})




#equipment related functions

#admin can see al equipment related infromation
def display_equipment_maintenance(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Equipment_Maintenance")
    equipment = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/equipmentMaintenance.html', {'equipment': equipment, 'user_id': user_id})


#admin can update equipment maintenance infromation
def update_equipment(request, user_id, equipment_id):
    if request.method == 'POST':
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Equipment_Maintenance WHERE equipment_id = %s", [equipment_id])
        equipment = cursor.fetchone()  # Assuming there's only one equipment with the given ID
        connection.close()
        return render(request, 'AdminApp/updateEquipment.html', {'equipment': equipment, 'user_id': user_id})
    return render(request, 'AdminApp/updateEquipment.html', {'equipment': equipment, 'user_id': user_id})



def submit_equipment_update(request, user_id, equipment_id):
    if request.method == 'POST':
        #extract user input 
        last_maintained_date = request.POST.get('last_maintained_date')
        next_maintenance_date = request.POST.get('next_maintenance_date')
        performed_by = request.POST.get('performed_by')

        try:
            #update in the database
            connection = connect()
            cursor = connection.cursor()
            cursor.execute("UPDATE Equipment_Maintenance SET last_maintained_date = %s, next_maintenance = %s, performed_by = %s WHERE equipment_id = %s",
                           [last_maintained_date, next_maintenance_date, performed_by, equipment_id])
            connection.commit()
            connection.close()
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
            return redirect('AdminApp-equipment_maintenance', user_id=user_id)

        return redirect('AdminApp-equipment_maintenance', user_id=user_id)

    return redirect('AdminApp-equipment_maintenance', user_id=user_id)


#admin can delete any equipment they want 
def deleteEquipment(request, equipment_id, user_id):
        if request.method == 'POST':
            try:
                connection = connect()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Equipment_Maintenance WHERE equipment_id = %s", [equipment_id])
                connection.commit()
                connection.close()
                return redirect('AdminApp-equipment_maintenance', user_id=user_id)

            except Exception as e:
                messages.add_message(request, messages.ERROR, f"Delete unsuccessful!")
                return redirect('AdminApp-equipment_maintenance', user_id=user_id)

        return redirect('AdminApp-equipment_maintenance', user_id=user_id)



#admin can add a new piece of equipment, simply by giving it a name 
def addEquipment(request, user_id):
    if request.method == 'POST':
        equipment_name = request.POST.get('equipment_name')

        try:
            connection = connect()
            cursor = connection.cursor()
           
            
            cursor.execute('INSERT INTO Equipment_Maintenance (equipment_name) ' +
               'VALUES (%s)', 
               [equipment_name])
            connection.commit()

            connection.close()
            return redirect('AdminApp-equipment_maintenance', user_id=user_id)

        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
            return redirect('AdminApp-equipment_maintenance', user_id=user_id)
            
    return render(request, 'AdminApp/addEquipment.html', {'user_id': user_id})





#trainer related functions

#admin can view all trainers 
def display_trainers(request, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Trainer")
    trainers = cursor.fetchall()
    connection.close()
    return render(request, 'AdminApp/trainers.html', {'trainers': trainers, 'user_id': user_id})


#admins can add trainers 
def addTrainer(request, user_id):
    #specializations a trainer can have 
    specializations = ['Cardio', 'Weightlifting', 'Yoga', 'Pilates', 'Crossfit', 'Kickboxing']
    if request.method == 'POST':

        #extract user input
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        username=request.POST.get('username')
        selected_specializations = request.POST.getlist('specializations')

        try:
            connection = connect()
            cursor = connection.cursor()
            #make a new user with log in information
            cursor.execute('INSERT INTO "User" (username, password, role) VALUES (%s, %s, %s) RETURNING user_id', 
                   [username, 'defaultPassword', 'trainer'])
            trainer_id = cursor.fetchone()[0]
            connection.commit()
            
            #use the id to make a new trainer with trainer previliges 
            cursor.execute('INSERT INTO Trainer (trainer_id, first_name, last_name, ' +
               'email, phone_number, specializations) ' +
               'VALUES (%s, %s, %s, %s, %s, %s)', 
               [trainer_id, first_name, last_name, email, phone, selected_specializations])
            connection.commit()

            connection.close()
            return redirect('AdminApp-trainers', user_id=user_id)


        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Update unsuccessful!")
            return redirect('AdminApp-trainers', user_id=user_id)
            
    return render(request, 'AdminApp/addTrainer.html', {'user_id': user_id, 'specializations':specializations})

