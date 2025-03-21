College Database Management System
A comprehensive database management system for a college that tracks departments, instructors, courses, students, and enrollments.

Project Description
This database system manages the academic structure of a college, focusing on the relationships between departments, instructors, courses, and students. It enables the college to manage course offerings, track instructor workloads, maintain student enrollment records, and organize departmental structures efficiently. The project uses Python, Flask, and MySQL, and it follows best practices in relational database design and normalization.

Requirements
Python 3.8+
MySQL or MariaDB
Flask
mysql-connector-python
Faker (for data generation)
python-dotenv (for environment variable management)

Project Structure
Here’s an example of what your folder might look like in Visual Studio Code:
COLLEGE-DBMS/
├── app.py               # Main Flask application
├── app.sh               # Bash script to automate setup and launch
├── create_database.sql  # SQL script to create database and tables
├── data_generator.py    # Python script to generate sample data (CSV files)
├── department_heads.csv # Generated CSV (department heads)
├── departments.csv      # Generated CSV (departments)
├── enrollments.csv      # Generated CSV (enrollments)
├── instructors.csv      # Generated CSV (instructors)
├── load_data.py         # Python script to load generated CSV data into MySQL
├── requirements.txt     # Project dependencies
├── students.csv         # Generated CSV (students)
├── .env                 # Environment variables (not in repo by default)
└── templates/           # HTML templates for the web interface (Flask + Jinja2)
    ├── base.html
    ├── courses_by_department.html
    ├── department_statistics.html
    ├── departments.html
    ├── index.html
    ├── instructor_info.html
    └── student_enrollment.html

Installation and Setup
1. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install Dependencies
pip install -r requirements.txt
3. Configure Your Database Settings
Create a .env file in the project root with variables similar to these:
DB_HOST=localhost
DB_USER=dbuser
DB_PASSWORD=Security@137
DB_NAME=college_db
SECRET_KEY=some_random_secret_key
If you’re on a system that requires a custom socket path, add:
DB_SOCKET=/var/run/mysqld/mysqld.sock
(Adjust the socket path as necessary.)
4. Use app.sh to Automate Setup
The app.sh script simplifies the process of generating data, creating/loading the database, and launching the Flask app. Before running it, make sure the credentials in your .env or the script itself match your MySQL setup. Then run:
chmod +x app.sh
./app.sh
What app.sh does:
Removes old CSV files (so you start fresh).
Generates sample data by calling python data_generator.py.
Creates the database and loads schema via create_database.sql.
Loads data from the newly generated CSV files by calling load_data.py.
Starts the Flask application (app.py).
6. Access the Application
Once app.sh completes, the Flask server should be running. Open your web browser and navigate to:
http://localhost:5000
You’ll see the homepage of the College Database Management System. From there, you can explore departments, courses, instructors, and enroll students via the interface.
