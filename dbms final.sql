
CREATE DATABASE dbproj;
USE  dbproj;

-- TABLE: rooms
CREATE TABLE rooms (
    Room_no INT PRIMARY KEY,
    room_type VARCHAR(50),
    cost_per_night DECIMAL(10,2)
);

-- TABLE: employee
CREATE TABLE employee (
    emp_ID INT PRIMARY KEY,
    E_Name VARCHAR(30),
    Designation VARCHAR(30),
    Department VARCHAR(30),
    Date_of_joining DATE
);

-- TABLE: departments
CREATE TABLE departments (
    dep_id INT PRIMARY KEY,
    department_name VARCHAR(30),
    no_of_workers INT,
    head_emp_id INT,
    FOREIGN KEY (head_emp_id) REFERENCES employee(emp_ID)
);

-- TABLE: customers
CREATE TABLE customers (
    cust_id INT PRIMARY KEY,
    cust_name VARCHAR(30),
    check_in_date DATE,
    check_out_date DATE,
    room_no INT,
    no_in_party INT,
    gender VARCHAR(10),
    aadhar_no VARCHAR(12) NOT NULL,
    phone_no VARCHAR(10),
    email_id VARCHAR(60) UNIQUE,
    FOREIGN KEY (room_no) REFERENCES rooms(Room_no)
);

-- TABLE: bookings
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY,
    cust_id INT,
    room_no INT,
    cust_name VARCHAR(30),
    room_type VARCHAR(50),
    check_in_date DATE,
    check_out_date DATE,
    total_Amt DECIMAL(10,2),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id),
    FOREIGN KEY (room_no) REFERENCES rooms(room_no)
);

-- TABLE: restaurant
CREATE TABLE restaurant (
    ID INT PRIMARY KEY,
    Cust_ID INT,
    Cust_Name VARCHAR(40),
    room_no INT,
    Table_no INT,
    No_in_Party INT,
    Meals VARCHAR(15),
    Type_of_Meal VARCHAR(15),
    FOREIGN KEY (Cust_ID) REFERENCES customers(cust_id),
    FOREIGN KEY (room_no) REFERENCES rooms(room_no)
);



-- INSERT INTO rooms
INSERT INTO rooms (room_no, room_type, price) VALUES
(101, 'standard', 2000.00),
(102, 'standard', 2000.00),
(103, 'standard', 2000.00),
(104, 'standard', 2000.00),
(105, 'deluxe', 3000.00),
(106, 'deluxe', 3000.00),
(107, 'deluxe', 3000.00),
(108, 'suite', 5000.00),
(109, 'suite', 5000.00),
(201, 'suite', 5000.00),
(202, 'suite', 5000.00),
(203, 'family suite', 7000.00),
(204, 'standard', 2000.00),
(205, 'presidential suite', 9000.00),
(206, 'presidential suite', 9000.00),
(301, 'deluxe', 3000.00),
(302, 'standard', 2000.00),
(303, 'deluxe', 3000.00),
(304, 'deluxe', 3000.00),
(305, 'standard', 2000.00),
(306, 'suite', 5000.00),
(307, 'deluxe', 3000.00),
(308, 'standard', 2000.00),
(309, 'suite', 5000.00),
(401, 'suite', 5000.00);

select * from bookings;

-- INSERT INTO departments
INSERT INTO departments (dep_id, department_name, head_emp_id) VALUES
(1, 'IT', 6),
(2, 'HR', 4),
(3, 'Housekeeping', 8),
(4, 'Finance', 11),
(5, 'Restaurant', 12),
(6, 'Security', 17),
(7, 'Concierge', 20),
(8, 'Maintenance', 18),
(9, 'Front Desk', 15);







