-- Create User table
CREATE TABLE IF NOT EXISTS "User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    role VARCHAR(20) DEFAULT 'member' NOT NULL
);

-- Create Member table
CREATE TABLE IF NOT EXISTS Member (
    member_id INTEGER PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(20) UNIQUE NOT NULL,
    date_of_birth DATE,
    address VARCHAR(255),
    phone_number VARCHAR(15),
    start_date DATE DEFAULT CURRENT_DATE,
    payment_status BOOLEAN DEFAULT TRUE
	FOREIGN KEY (member_id) REFERENCES "User"(user_id)

);

-- Create Member_Health table
CREATE TABLE IF NOT EXISTS Member_Health (
    member_id INTEGER PRIMARY KEY,
    start_weight DECIMAL,
    current_weight DECIMAL,
    height DECIMAL,
    age INTEGER,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Create Fitness_Goals table
CREATE TABLE IF NOT EXISTS Fitness_Goals (
    member_id INTEGER PRIMARY KEY,
    weight_goal DECIMAL,
    time_goal INTEGER,
    diet_goal TEXT,
    form_of_exercise TEXT[],
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);


-- Create Exercise_Routine table
CREATE TABLE IF NOT EXISTS Exercise_Routine (
    routine_id SERIAL PRIMARY KEY,
    member_id INTEGER,
    routine_name VARCHAR(50),
    description TEXT,
    duration INTERVAL,
    date_created DATE,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Create Admin table
CREATE TABLE IF NOT EXISTS Admin (
    admin_id INTEGER PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
	FOREIGN KEY (admin_id) REFERENCES "User"(user_id)
);

-- Create Trainer table
CREATE TABLE IF NOT EXISTS Trainer (
    trainer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    specializations TEXT[],
	FOREIGN KEY (trainer_id) REFERENCES "User"(user_id)
);

-- Create Room_Bookings table
CREATE TABLE IF NOT EXISTS Room_Bookings (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50),
    room_location VARCHAR(50),
    booked BOOLEAN,
    time TIME,
    date DATE,
    duration INTERVAL
);

-- Create Personal_Training_Sessions table
CREATE TABLE IF NOT EXISTS Personal_Training_Sessions (
    session_id SERIAL PRIMARY KEY,
    trainer_id INTEGER,
    member_id INTEGER,
    session_date DATE,
    session_time TIME,
    duration INTERVAL DEFAULT '1 hour', -- Set default duration to 1 hour
    room_id INTEGER,
    price DECIMAL,
    payment_status BOOLEAN DEFAULT NULL, -- Set default payment_status to NULL
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id),
    FOREIGN KEY (room_id) REFERENCES Room_Bookings(room_id)
);

-- Create Group_Fitness_Classes table
CREATE TABLE IF NOT EXISTS Group_Fitness_Classes (
    class_id SERIAL PRIMARY KEY,
    trainer_id INTEGER,
    room_id INTEGER,
    class_name VARCHAR(100),
    description TEXT,
    session_date DATE,
    session_time TIME,
    member_ids INTEGER[],
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),
    FOREIGN KEY (room_id) REFERENCES Room_Bookings(room_id)
);


-- Create Equipment_Maintenance table
CREATE TABLE IF NOT EXISTS Equipment_Maintenance (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100),
    last_maintained_date DATE,
    next_maintenance DATE,
    performed_by INTEGER,
    FOREIGN KEY (performed_by) REFERENCES Admin(admin_id)
);
