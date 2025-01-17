import mysql.connector
import os

host = os.getenv('MYSQL_HOST')
db_user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DB')

# Establish connection to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=db_user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Register a new user
def register_user(name,email, password):
    connection = create_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        try:
            insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name,email,password))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Get user details (for login)
def get_user(email, password):
    connection = create_connection()
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        try:
            select_query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(select_query, (email, password))
            user = cursor.fetchone()
            return user
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def check_user_credentials(email, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=db_user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
