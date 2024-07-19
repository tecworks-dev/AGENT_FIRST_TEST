import sqlite3
import traceback
from config import DATABASE_URI

def init_db():
    """
    Initializes the database connection.
    """
    try:
        conn = sqlite3.connect(DATABASE_URI)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        traceback.print_exc()

def execute_query(query, params=None):
    """
    Executes a database query.

    :param query: SQL query string
    :param params: Parameters for the query (optional)
    :return: Result of the query execution
    """
    try:
        conn = sqlite3.connect(DATABASE_URI)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        traceback.print_exc()
        return None