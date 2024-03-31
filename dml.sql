-- fitnessManagement_db

-- Inserting sample data into the User table
INSERT INTO "User" (username, password, role) VALUES
('user1', 'pass1', 'member'),
('user2', 'pass2', 'member'),
('admin1', 'adminpassword1', 'admin'),
('trainer1', 'trainerpassword1', 'trainer'),
('trainer2', 'pass2', 'trainer');

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
(3, 'Admin', 'Smith', 'admin@example.com', '1112223333');

-- Inserting sample data into the Trainer table
INSERT INTO Trainer (trainer_id, first_name, last_name, email, phone_number, specializations) VALUES
(4, 'Trainer1', 'Johnson', 'trainer@example.com', '9998887777', '{Weightlifting, Yoga, Pilates}'),
(5, 'Trainer2', 'Bobby', 'bobby@example.com', '5552229865', '{Pilates, Yoga, Cardio}');



-- Room_Bookings table
-- Inserting bookings for the next 3 days with 3 rooms available from 4 PM to 9 PM for 1-hour durations

-- Create a temporary table to store time slots
CREATE TEMP TABLE TimeSlots AS (
    SELECT time_slot
    FROM (
        SELECT '16:00'::time AS time_slot
        UNION ALL SELECT '17:00'::time
        UNION ALL SELECT '18:00'::time
        UNION ALL SELECT '19:00'::time
        UNION ALL SELECT '20:00'::time
        UNION ALL SELECT '21:00'::time
    ) AS slots
);

-- Insert bookings for each room for the next 3 days
INSERT INTO Room_Bookings (room_name, room_location, booked, time, date, duration)
SELECT room_name, room_location, false, time_slot, CURRENT_DATE + INTERVAL '1' DAY, INTERVAL '1 hour'
FROM (
    SELECT 'Room 1' AS room_name, 'Main Building' AS room_location
    UNION ALL
    SELECT 'Room 2', 'Annex Building'
    UNION ALL
    SELECT 'Room 3', 'Main Building'
) AS rooms, TimeSlots
UNION ALL
SELECT room_name, room_location, false, time_slot, CURRENT_DATE + INTERVAL '2' DAY, INTERVAL '1 hour'
FROM (
    SELECT 'Room 1' AS room_name, 'Main Building' AS room_location
    UNION ALL
    SELECT 'Room 2', 'Annex Building'
    UNION ALL
    SELECT 'Room 3', 'Main Building'
) AS rooms, TimeSlots
UNION ALL
SELECT room_name, room_location, false, time_slot, CURRENT_DATE + INTERVAL '3' DAY, INTERVAL '1 hour'
FROM (
    SELECT 'Room 1' AS room_name, 'Main Building' AS room_location
    UNION ALL
    SELECT 'Room 2', 'Annex Building'
    UNION ALL
    SELECT 'Room 3', 'Main Building'
) AS rooms, TimeSlots;

-- Drop the temporary table
DROP TABLE TimeSlots;




-- Inserting additional sample data into the Personal_Training_Sessions table
INSERT INTO Personal_Training_Sessions (trainer_id, member_id, session_date, session_time, duration, room_id, price, payment_status) VALUES
(4, NULL, '2024-03-26', '11:00:00', '1 hour', 1, 35.00, true),
(5, 1, '2024-03-27', '16:00:00', '1 hour', 2, 45.00, true),
(4, NULL, '2024-03-28', '12:00:00', '1 hour', 1, 40.00, true),
(5, 2, '2024-03-29', '17:00:00', '1 hour', 2, 50.00, true),
(4, NULL, '2024-03-30', '13:00:00', '1 hour', 1, 30.00, true),
(5, 1, '2024-03-31', '18:00:00', '1 hour', 2, 40.00, true),
(4, NULL, '2024-04-01', '14:00:00', '1 hour', 1, 35.00, true),
(5, 2, '2024-04-02', '19:00:00', '1 hour', 2, 45.00, true),
(4, NULL, '2024-04-03', '15:00:00', '1 hour', 1, 40.00, true),
(5, 1, '2024-04-04', '20:00:00', '1 hour', 2, 50.00, true);

-- Inserting additional sample data into the Group_Fitness_Classes table
INSERT INTO Group_Fitness_Classes (trainer_id, room_id, class_name, description, session_date, session_time, member_ids) VALUES
(4, 1, 'Evening Pilates', 'Pilates class for all levels', '2024-03-26', '19:00:00', '{1, 2}'),
(5, 2, 'Cardio Blast', 'High-intensity cardio workout', '2024-03-27', '20:00:00', '{2}'),
(4, 1, 'Morning Bootcamp', 'Bootcamp-style workout session', '2024-03-28', '07:00:00', '{1}'),
(5, 2, 'Strength Training', 'Focus on building strength and muscle', '2024-03-29', '21:00:00', '{1, 2}'),
(5, 2, 'Cardio', 'cardio workout', '2024-04-04', '13:00:00', '{}');

