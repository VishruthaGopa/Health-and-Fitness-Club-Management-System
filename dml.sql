-- Inserting sample data into the User table
INSERT INTO "User" (username, password, role) VALUES
('user1', 'pass1', 'member'),
('user2', 'pass2', 'member'),
('admin1', 'adminpassword1', 'admin'),
('trainer1', 'trainerpassword1', 'trainer');

-- Inserting sample data into the Member table
INSERT INTO Member (member_id, first_name, last_name, gender, email, date_of_birth, address, phone_number, start_date, payment_status) VALUES
(1, 'John', 'Doe', 'Male', 'john@example.com', '1990-01-01', '123 Main St, City', '1234567890', '2024-01-01', true),
(2, 'Jane', 'Doe', 'Female', 'jane@example.com', '1995-05-05', '456 Elm St, Town', '0987654321', '2024-02-15', true);

-- Inserting sample data into the Member_Health table
INSERT INTO Member_Health (member_id, start_weight, current_weight, height, age) VALUES
(1, 80.5, 75.2, 180, 34),
(2, 65.2, 63.0, 165, 29);

-- Inserting sample data into the Fitness_Goals table
INSERT INTO Fitness_Goals (member_id, weight_goal, time_goal, diet_goal, form_of_exercise) VALUES
(1, 70.0, 6, 'Eat healthier meals', '{Cardio, Weightlifting}'),
(2, 60.0, 3, 'Cut down on sugar intake', '{Yoga, Pilates}');

-- Inserting sample data into the Exercise_Routine table
INSERT INTO Exercise_Routine (member_id, routine_name, description, duration, date_created) VALUES
(1, 'Morning Cardio', '30 minutes of running', '30 minutes', '2024-01-10'),
(2, 'Evening Yoga', 'Relaxing yoga session', '45 minutes', '2024-02-20');

-- Inserting sample data into the Admin table
INSERT INTO Admin (admin_id, first_name, last_name, email, phone_number) VALUES
(1, 'Admin', 'Smith', 'admin@example.com', '1112223333');

-- Inserting sample data into the Trainer table
INSERT INTO Trainer (trainer_id, first_name, last_name, email, phone_number, specializations) VALUES
(1, 'Trainer', 'Johnson', 'trainer@example.com', '9998887777', '{Weightlifting, Yoga}');

-- Inserting sample data into the Room_Bookings table
INSERT INTO Room_Bookings (room_name, room_location, booked, time, date, duration) VALUES
('Room 1', 'Main Building', false, '09:00:00', '2024-03-25', '1 hour'),
('Room 2', 'Annex Building', true, '14:00:00', '2024-03-25', '2 hours');

-- Inserting sample data into the Personal_Training_Sessions table
INSERT INTO Personal_Training_Sessions (trainer_id, member_id, session_date, session_time, duration, room_id, price, payment_status) VALUES
(1, 1, '2024-03-26', '10:00:00', '1 hour', 1, 30.00, true),
(1, 2, '2024-03-27', '15:00:00', '1 hour', 2, 40.00, true);

-- Inserting sample data into the Group_Fitness_Classes table
INSERT INTO Group_Fitness_Classes (trainer_id, room_id, class_name, description, session_date, session_time, member_ids) VALUES
(1, 1, 'Morning Yoga', 'Beginner-friendly yoga class', '2024-03-28', '08:00:00', '{1, 2}'),
(1, 2, 'Pilates Core Workout', 'Strengthen your core with pilates', '2024-03-29', '16:00:00', '{2}');
