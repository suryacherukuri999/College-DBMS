from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()  # load env vars

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key") # for encryption purpose

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'college_db')
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

# List all the departments
@app.route('/departments')
def list_departments():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.*,
               COUNT(i.instructor_id) AS num_instructors,
               COUNT(DISTINCT c.course_id) AS num_courses
        FROM Departments d
        LEFT JOIN Instructors i ON d.dept_id = i.dept_id
        LEFT JOIN Courses c ON d.dept_id = c.dept_id
        GROUP BY d.dept_id
        ORDER BY d.dept_id
    """
    cursor.execute(query)
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('departments.html', departments=departments)

# Find all courses by the department
@app.route('/courses_by_department', methods=['GET', 'POST'])
def courses_by_department():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT dept_id, dept_name FROM Departments ORDER BY dept_name")
    departments = cursor.fetchall()

    courses = []
    if request.method == 'POST':
        dept_id = request.form.get('dept_id')
        query = """
            SELECT c.*, d.dept_name, CONCAT(i.first_name, ' ', i.last_name) AS instructor_name
            FROM Courses c
            JOIN Departments d ON c.dept_id = d.dept_id
            JOIN Instructors i ON c.instructor_id = i.instructor_id
            WHERE c.dept_id = %s
            ORDER BY c.course_code
        """
        cursor.execute(query, (dept_id,))
        courses = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('courses_by_department.html', departments=departments, courses=courses)

# Find instructor information like name, dept name, and course he/she teach
@app.route('/instructor_info', methods=['GET', 'POST'])
def instructor_info():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT instructor_id, CONCAT(first_name, ' ', last_name) AS name  
        FROM Instructors
        ORDER BY last_name, first_name
    """)
    instructors = cursor.fetchall()  # initial rendering 

    instructor_data = None
    teaching_courses = []

    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')

        # Get instructor details
        query = """
            SELECT i.*, d.dept_name,
                   (SELECT COUNT(*) 
                    FROM DepartmentHeads dh
                    WHERE dh.instructor_id = i.instructor_id) AS is_head
            FROM Instructors i
            JOIN Departments d ON i.dept_id = d.dept_id
            WHERE i.instructor_id = %s
        """
        cursor.execute(query, (instructor_id,))
        instructor_data = cursor.fetchone()

        # Get courses taught
        query = """
            SELECT c.*, COUNT(e.student_id) AS enrolled_students
            FROM Courses c
            LEFT JOIN Enrollments e ON c.course_id = e.course_id
            WHERE c.instructor_id = %s
            GROUP BY c.course_id
            ORDER BY c.course_code
        """
        cursor.execute(query, (instructor_id,))
        teaching_courses = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('instructor_info.html',
                           instructors=instructors,
                           instructor=instructor_data,
                           courses=teaching_courses)

# Student enrollment status
@app.route('/student_enrollment', methods=['GET', 'POST'])
def student_enrollment():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Students for dropdown
    cursor.execute("""
        SELECT student_id, CONCAT(first_name, ' ', last_name) AS name
        FROM Students
        ORDER BY last_name, first_name
    """)
    students = cursor.fetchall()

    # Courses for dropdown
    cursor.execute("""
        SELECT course_id, CONCAT(course_code, ': ', title) AS name
        FROM Courses
        ORDER BY course_code
    """)
    courses = cursor.fetchall()

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        enrollment_date = request.form.get('enrollment_date')

        try:
            # Check if already enrolled
            cursor.execute(
                "SELECT * FROM Enrollments WHERE student_id=%s AND course_id=%s",
                (student_id, course_id)
            )
            existing = cursor.fetchone()
            if existing:
                flash('Student is already enrolled in this course!', 'check again')
            else:
                cursor.execute(
                    """INSERT INTO Enrollments (student_id, course_id, enrollment_date)
                       VALUES (%s, %s, %s)""",
                    (student_id, course_id, enrollment_date)
                )
                conn.commit()
                flash('Enrollment successful!', 'success')
        except Error as e:
            flash(f'Error: {e}', 'check again')

    cursor.close()
    conn.close()
    return render_template('student_enrollment.html', students=students, courses=courses)

# department statistics like no of teachers, students in a specific department
@app.route('/department_statistics')
def department_statistics():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Updated query: no WHERE clause excluding null grades,
    # so newly enrolled students appear in counts
    query = """
    SELECT
        d.dept_id,
        d.dept_name,
        COUNT(DISTINCT i.instructor_id) AS num_instructors,
        COUNT(DISTINCT c.course_id) AS num_courses,
        COUNT(DISTINCT e.student_id) AS num_students,
        AVG(
            CASE 
                WHEN e.grade = 'A+' THEN 4.0
                WHEN e.grade = 'A' THEN 3.9
                WHEN e.grade = 'A-' THEN 3.7
                WHEN e.grade = 'B+' THEN 3.4
                WHEN e.grade = 'B' THEN 3.1
                WHEN e.grade = 'B-' THEN 2.8
                WHEN e.grade = 'C+' THEN 2.4
                WHEN e.grade = 'C' THEN 2.1
                WHEN e.grade = 'C-' THEN 1.8
                WHEN e.grade = 'D+' THEN 1.5
                WHEN e.grade = 'D' THEN 1.0
                WHEN e.grade = 'F' THEN 0.0
                ELSE NULL
            END
        ) AS avg_gpa
    FROM Departments d
    LEFT JOIN Instructors i ON d.dept_id = i.dept_id
    LEFT JOIN Courses c ON d.dept_id = c.dept_id
    LEFT JOIN Enrollments e ON c.course_id = e.course_id
    GROUP BY d.dept_id
    ORDER BY d.dept_id
    """
    cursor.execute(query)
    statistics = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('department_statistics.html', statistics=statistics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
