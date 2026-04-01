from db import get_connection

def add_room(room_number, room_type, rent_per_month, status, host_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO room (room_number, room_type, rent_per_month, status, host_id)
        VALUES (?, ?, ?, ?, ?)
    """, (room_number, room_type, rent_per_month, status, host_id))

    conn.commit()
    conn.close()
    def get_available_rooms():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM room WHERE status = 'Available'")
    rows = cur.fetchall()

    conn.close()
    return rows
def get_rooms():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM room")
    rows = cur.fetchall()

    conn.close()
    return rows
