-- fitnessManagement_db

-- "User" table
INSERT INTO "User" (username, password, role) VALUES
('user1', 'pass1', 'member'),
('user2', 'pass2', 'member'),
('admin1', 'adminpassword1', 'admin'),
('trainer1', 'trainerpassword1', 'trainer'),
('trainer2', 'pass2', 'trainer'),
('admin2', 'adminpass2', 'admin');

-- Member table
INSERT INTO Member (member_id, first_name, last_name, gender, email, date_of_birth, address, phone_number, start_date, payment_status) VALUES
(1, 'John', 'Doe', 'Male', 'john@example.com', '1990-01-01', '123 Main St, City', '1234567890', '2024-01-01', true),
(2, 'Jane', 'Smith', 'Female', 'jane@example.com', '1995-05-05', '456 Elm St, Town', '0987654321', '2024-02-15', true);

-- Member_Health table
INSERT INTO Member_Health (member_id, start_weight, current_weight, height, age) VALUES
(1, 80.5, 75.2, 180, 34),
(2, 65.2, 63.0, 165, 29);

-- Fitness_Goals table
INSERT INTO Fitness_Goals (member_id, weight_goal, time_goal, diet_goal, form_of_exercise) VALUES
(1, 70.0, 6, 'Eat healthier meals', '{Cardio, Weightlifting}'),
(2, 60.0, 3, 'Cut down on sugar intake', '{Yoga, Pilates}');

-- Exercise_Routine table
INSERT INTO Exercise_Routine (member_id, routine_name, description, duration, date_created) VALUES
(1, 'Morning Cardio', '30 minutes of running', '30 minutes', '2024-01-10'),
(2, 'Evening Yoga', 'Relaxing yoga session', '45 minutes', '2024-02-20');

-- Admin table
INSERT INTO Admin (admin_id, first_name, last_name, email, phone_number) VALUES
(3, 'Admin', 'Smith', 'admin@example.com', '1112223333'),
(6, 'Admin', 'Melissa', 'melisaa@gmail.com', '7682943323');

-- Trainer table
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




-- Personal_Training_Sessions table
INSERT INTO Personal_Training_Sessions (trainer_id, member_id, session_date, session_time, room_id, price, payment_status) VALUES
(4, NULL, CURRENT_DATE + INTERVAL '1' DAY, '16:00:00', 1, 35.00, NULL),
(5, 2, CURRENT_DATE + INTERVAL '1' DAY, '18:00:00', 9, 35.00, true),
(5, 1, CURRENT_DATE + INTERVAL '1' DAY, '20:00:00', 14, 50.00, true),
(4, NULL, CURRENT_DATE + INTERVAL '2' DAY, '17:00:00', 23, 45.00, NULL),
(4, 2, CURRENT_DATE + INTERVAL '2' DAY, '19:00:00', 28, 45.00, true),
(5, 1, CURRENT_DATE + INTERVAL '2' DAY, '21:00:00', 36, 40.00, true),
(4, NULL, CURRENT_DATE + INTERVAL '3' DAY, '18:00:00', 45, 40.00, NULL),
(5, 1, CURRENT_DATE + INTERVAL '3' DAY, '20:00:00', 51, 50.00, true),
(5, NULL, CURRENT_DATE + INTERVAL '3' DAY, '21:00:00', 52, 40.00, NULL);

-- Group_Fitness_Classes table
INSERT INTO Group_Fitness_Classes (trainer_id, room_id, class_name, description, session_date, session_time, member_ids) VALUES
(4, 4, 'Evening Pilates', 'Pilates class for all levels', CURRENT_DATE + INTERVAL '1' DAY, '17:00:00', '{}'),
(5, 18, 'Strength Training', 'Focus on building strength and muscle', CURRENT_DATE + INTERVAL '1' DAY, '21:00:00', '{1, 2}'),
(5, 25, 'Cardio Blast', 'High-intensity cardio workout', CURRENT_DATE + INTERVAL '2' DAY, '18:00:00', '{2}'),
(5, 29, 'Cardio', 'Cardio workout', CURRENT_DATE + INTERVAL '2' DAY, '19:00:00', '{}'),
(4, 44, 'Morning Bootcamp', 'Bootcamp-style workout session', CURRENT_DATE + INTERVAL '3' DAY, '18:00:00', '{1}');


-- Update the booked status in Room_Bookings based on Personal_Training_Sessions
UPDATE Room_Bookings AS rb
SET booked = TRUE
FROM Personal_Training_Sessions AS pts
WHERE rb.room_id = pts.room_id
  AND rb.time = pts.session_time
  AND rb.date = pts.session_date;

-- Update the booked status in Room_Bookings based on Group_Fitness_Classes
UPDATE Room_Bookings AS rb
SET booked = TRUE
FROM Group_Fitness_Classes AS gfc
WHERE rb.room_id = gfc.room_id
  AND rb.time = gfc.session_time
  AND rb.date = gfc.session_date;

-- Equipment_Maintenance table
INSERT INTO Equipment_Maintenance (equipment_name, last_maintained_date, next_maintenance, performed_by) VALUES
('Treadmill', '2024-01-01', '2024-04-01', 3),
('Exercise Bike', '2024-02-15', '2024-04-15', 6),
('Dumbbells Set', '2024-03-20', '2024-04-20', 5),
('Leg Press Machine', '2024-01-03', '2024-04-03', 3),
('Chest Press Machine', '2024-01-14', '2024-04-14', 3),
('Rowing Machine', '2024-01-10', '2024-04-10', 6);
