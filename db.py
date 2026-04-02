import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="swathi@06",
        database="pg_management"
    )

    if conn.is_connected():
        print("Connected to MySQL database")

        cursor = conn.cursor()

except Error as e:
    print("Error:", e)
