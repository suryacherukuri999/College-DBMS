-- create database. DDL compilation

DROP DATABASE IF EXISTS college_db;
CREATE DATABASE college_db;
USE college_db;

-- This is Departments table
CREATE TABLE Departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    established DATE,
    CONSTRAINT unique_dept_name UNIQUE (dept_name)  -- has to be unique as its dept name
);

-- Create the Instructors table
CREATE TABLE Instructors (
    instructor_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(50),      -- phone no. kept 50 size for safety
    hire_date DATE,
    dept_id INT NOT NULL,
    CONSTRAINT unique_instructor_email UNIQUE (email),
    CONSTRAINT fk_instructor_department FOREIGN KEY (dept_id) 
        REFERENCES Departments(dept_id) ON DELETE RESTRICT
);

-- Create the DepartmentHeads table
CREATE TABLE DepartmentHeads (
    dept_id INT PRIMARY KEY,
    instructor_id INT UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    CONSTRAINT fk_head_department FOREIGN KEY (dept_id) 
        REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    CONSTRAINT fk_head_instructor FOREIGN KEY (instructor_id) 
        REFERENCES Instructors(instructor_id) ON DELETE RESTRICT
);

-- Create the Courses table
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL,
    title VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    description TEXT,
    dept_id INT NOT NULL,
    instructor_id INT NOT NULL,
    CONSTRAINT unique_course_code UNIQUE (course_code),
    CONSTRAINT fk_course_department FOREIGN KEY (dept_id) 
        REFERENCES Departments(dept_id) ON DELETE RESTRICT,
    CONSTRAINT fk_course_instructor FOREIGN KEY (instructor_id) 
        REFERENCES Instructors(instructor_id) ON DELETE RESTRICT
);

-- Create the Students table
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    enrollment_date DATE NOT NULL,
    major VARCHAR(100),
    CONSTRAINT unique_student_email UNIQUE (email)
);

-- Create the Enrollments table
CREATE TABLE Enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE NOT NULL,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id),
    CONSTRAINT fk_enrollment_student FOREIGN KEY (student_id) 
        REFERENCES Students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_enrollment_course FOREIGN KEY (course_id) 
        REFERENCES Courses(course_id) ON DELETE CASCADE
);
