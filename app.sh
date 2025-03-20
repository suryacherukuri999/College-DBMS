#!/bin/bash
set -e 

rm -rf *.csv


# Generate sample data
echo "Generating Sample Data..."
python data_generator.py

# Create database and load schema
echo "Creating database tables..."
#mysql -u dbuser -p college_db < create_database.sql
mysql -u dbuser -pSecurity@137 college_db --socket=/var/run/mysqld/mysqld.sock < create_database.sql

# Load data into database
echo "Loading data..."
python load_data.py

# Run the Flask app
echo "Starting Flask application..."
python app.py