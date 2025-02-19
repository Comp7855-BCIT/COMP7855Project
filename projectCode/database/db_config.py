# db_config.py

import psycopg2

#DB_NAME = "student_management"      # change if necessary
DB_USER = "postgres"               # your postgres username
DB_PASSWORD = "1234"      # replace with your password
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection(DB_NAME):
    """
    Creates and returns a new database connection.
    Remember to close the connection after you're done.
    """
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn
