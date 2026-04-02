from db import conn, cursor
def register_user(name, phone, email):
    cursor.execute("""
        INSERT INTO users (name, phone, email, role)
        VALUES (%s, %s, %s, 'Guest')
    """, (name, phone, email))

    conn.commit()


def login_user(email, phone):
    cursor.execute("""
        SELECT user_id, name, role
        FROM users
        WHERE email = %s AND phone = %s
    """, (email, phone))

    return cursor.fetchone() 

def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
