import csv
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='dbuser',           
            password='Security@137', 
            database='college_db',
            unix_socket='/var/run/mysqld/mysqld.sock' 

        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def load_departments(conn):
    cursor = conn.cursor()
    try:
        with open('departments.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # skip header
            for row in csv_data:
                query = """INSERT INTO Departments 
                           (dept_id, dept_name, location, established)
                           VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, tuple(row))
        conn.commit()
        print("Loaded departments data successfully.")
    except Error as e:
        print(f"Error loading departments data: {e}")
    finally:
        cursor.close()

def load_instructors(conn):
    cursor = conn.cursor()
    try:
        with open('instructors.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)
            for row in csv_data:
                query = """INSERT INTO Instructors
                           (instructor_id, first_name, last_name, email, phone, hire_date, dept_id)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, tuple(row))
        conn.commit()
        print("Loaded instructors data successfully.")
    except Error as e:
        print(f"Error loading instructors data: {e}")
    finally:
        cursor.close()

def load_department_heads(conn):
    cursor = conn.cursor()
    try:
        with open('department_heads.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)
            for row in csv_data:
                query = """INSERT INTO DepartmentHeads 
                           (dept_id, instructor_id, start_date)
                           VALUES (%s, %s, %s)"""
                cursor.execute(query, tuple(row))
        conn.commit()
        print("Loaded department heads data successfully.")
    except Error as e:
        print(f"Error loading department heads data: {e}")
    finally:
        cursor.close()

def load_courses(conn):
    cursor = conn.cursor()
    try:
        with open('courses.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)
            for row in csv_data:
                query = """INSERT INTO Courses
                           (course_id, course_code, title, credits, description, dept_id, instructor_id)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, tuple(row))
        conn.commit()
        print("Loaded courses data successfully.")
    except Error as e:
        print(f"Error loading courses data: {e}")
    finally:
        cursor.close()

def load_students(conn):
    cursor = conn.cursor()
    try:
        with open('students.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)
            count = 0
            for row in csv_data:
                query = """INSERT INTO Students
                           (student_id, first_name, last_name, email, enrollment_date, major)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, tuple(row))
                count += 1
                if count % 1000 == 0:
                    conn.commit()
                    print(f"Processed {count} students...")
        conn.commit()
        print(f"Loaded students data successfully. Total {count} students processed.")
    except Error as e:
        print(f"Error loading students data: {e}")
    finally:
        cursor.close()

def load_enrollments(conn):
    cursor = conn.cursor()
    try:
        with open('enrollments.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)
            count = 0
            for row in csv_data:
                grade = row[3] if row[3] and row[3].lower() != 'null' else None
                query = """INSERT INTO Enrollments 
                           (student_id, course_id, enrollment_date, grade)
                           VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (row[0], row[1], row[2], grade))
                count += 1
                if count % 1000 == 0:
                    conn.commit()
                    print(f"Processed {count} enrollments...")
        conn.commit()
        print(f"Loaded enrollments data successfully. Total {count} enrollments processed.")
    except Error as e:
        print(f"Error loading enrollments data: {e}")
    finally:
        cursor.close()

def main():
    conn = connect_to_database()
    if conn:
        try:
            print("Loading data into database...")
            load_departments(conn)
            load_instructors(conn)
            load_department_heads(conn)
            load_courses(conn)
            load_students(conn)
            load_enrollments(conn)
            print("All data loaded successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                conn.close()
                print("Database connection closed.")

if __name__ == "__main__":
    main()
