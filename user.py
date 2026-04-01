from db import get_connection
def register_user(name, phone, email):
    conn = get_connection()
    cur = conn.cursor()

    
    cur.execute("""
        INSERT INTO user (name, phone, email, role)
        VALUES (?, ?, ?, 'Guest')
    """, (name, phone, email))

    conn.commit()
    conn.close()


def login_user(email, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role
        FROM user
        WHERE email = ? AND phone = ?
    """, (email, phone))

    user = cur.fetchone()
    conn.close()

    return user
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()

    conn.close()
    return rows
