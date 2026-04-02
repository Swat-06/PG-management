from db import conn, cursor
def add_room(room_number, room_type, rent_per_month, status, host_id):
    cursor.execute("""
        INSERT INTO room (room_number, room_type, rent_per_month, status, host_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (room_number, room_type, rent_per_month, status, host_id))

    conn.commit()
def get_available_rooms():
    cursor.execute("""
        SELECT room_id, room_number, room_type, rent_per_month
        FROM room
        WHERE status = 'Available'
    """)
    return cursor.fetchall()
def get_rooms():
    cursor.execute("SELECT * FROM room")
    return cursor.fetchall()
