from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import openai
import os
import sqlite3
import streamlit as st

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("API_KEY")

# Function to get SQL query from LLM based on user question and prompt
def get_gemini_response(question, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        max_tokens=100,
        temperature=0
    )
    return response.choices[0].message.content.strip()

# Function to execute SQL query on the database and fetch results
def read_sql_query(sql, db):
    connection = sqlite3.connect(db)  # Connect to SQLite database
    cursor = connection.cursor()
    data = cursor.execute("SELECT * FROM students").fetchall()  # Fetch all records from students table
    connection.close()  # Close the database connection
    for row in data:
        print(row)  # Print each row to the console
    return data

# Prompt for the LLM to instruct it how to generate SQL queries
prompt = """You are an expert in converting natural language to SQL queries.
The  SQL database has a table named 'students' with the following columns:
- id, name, age, grade \n
Given a question, generate the corresponding SQL query to fetch the required data from the 'students' table.
Only provide the SQL query without any additional text or explanation.\n\n
Example1:\n
Question: give the total count of students like this SELECT COUNT(*) FROM STUDENTS \nExample2:\n
Question: List all students with grade A like this SELECT * FROM STUDENTS WHERE GRADE='A' \nExample3:\n
Question: List the names of students older than 21 like this SELECT NAME FROM STUDENTS WHERE AGE>21 \n """

# Streamlit UI setup
st.set_page_config(page_title="Natural Language to SQL Query with Gemini Pro")
st.header("Natural Language to SQL Query with Gemini Pro")

# Input box for user to enter their question
user_question = st.text_input("Enter your question about the students database:")

# Button to trigger SQL query generation and execution
if st.button("Get SQL Query"): 
    if user_question:
        sql_query = get_gemini_response(user_question, prompt)  # Get SQL query from LLM
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language='sql')
        st.subheader("Query Result:")
        result = read_sql_query(sql_query, 'student.db')  # Execute SQL query and get results
        for row in result:
            print(row)
        st.write(result)  # Display results in Streamlit app
    else:
        st.warning("Please enter a question.")  # Warn if no question is entered