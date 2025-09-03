import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
connection = sqlite3.connect('student.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# SQL statement to create the 'students' table if it doesn't already exist
table_info = """
CREATE TABLE IF NOT EXISTS students (   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL,
    age INTEGER,
    grade VARCHAR(25)
);
"""

# Execute the table creation statement
cursor.execute(table_info)

# Insert sample student records into the 'students' table
cursor.execute("INSERT INTO students (name, age, grade) VALUES ('Alice', 20, 'A')")
cursor.execute("INSERT INTO students (name, age, grade) VALUES ('Bob', 22, 'B')")
cursor.execute("INSERT INTO students (name, age, grade) VALUES ('Charlie', 23, 'C')")
cursor.execute("INSERT INTO students (name, age, grade) VALUES ('David', 21, 'B+')")
cursor.execute("INSERT INTO students (name, age, grade) VALUES ('Eva', 19, 'A-')")

# Fetch all records from the 'students' table
data = cursor.execute("SELECT * FROM students").fetchall()

# Print each row to the console
for row in data:
    print(row)  

# Commit the changes and close the connection
connection.commit()
connection.close()