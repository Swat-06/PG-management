import tkinter as tk
from tkinter import messagebox
from db import conn, cursor
from datetime import datetime   # 🔥 added for validation


# 🔹 Get available rooms
def get_available_rooms():
    cursor.execute("""
        SELECT room_id, room_number, room_type, rent_per_month
        FROM room
        WHERE status = 'Available'
    """)
    return cursor.fetchall()


# 🔹 Insert booking (DB-aligned)
def insert_booking(room_id, user_id, checkout_date=None):
    try:
        # 🔹 Insert booking
        if checkout_date:
            cursor.execute("""
                INSERT INTO booking (room_id, guest_id, check_out_date, booking_status)
                VALUES (%s, %s, %s, 'Booked')
            """, (room_id, user_id, checkout_date))
        else:
            cursor.execute("""
                INSERT INTO booking (room_id, guest_id, booking_status)
                VALUES (%s, %s, 'Booked')
            """, (room_id, user_id))

        # 🔹 Get booking_id
        booking_id = cursor.lastrowid

        # 🔹 Get room rent
        cursor.execute("""
            SELECT rent_per_month FROM room WHERE room_id=%s
        """, (room_id,))
        rent = cursor.fetchone()[0]

        # 🔹 Create payment record (Pending)
        cursor.execute("""
            INSERT INTO payment (booking_id, amount, payment_status)
            VALUES (%s, %s, 'Pending')
        """, (booking_id, rent))

        # 🔹 Update room status
        cursor.execute("""
            UPDATE room
            SET status = 'Occupied'
            WHERE room_id = %s
        """, (room_id,))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False


# ✅ ADD HERE
def center_window(win, width, height):
    win.update_idletasks()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry(f"{width}x{height}+{x}+{y}")


# 🔹 Booking popup (with optional checkout date + validation)
def confirm_booking_popup(room, user_id, parent):
    popup = tk.Toplevel(parent)
    popup.title("Confirm Booking")
    center_window(popup, 300, 250) 

    tk.Label(popup, text="Confirm Booking", font=("Arial", 12)).pack(pady=10)

    tk.Label(popup, text=f"Room: {room[1]}").pack()
    tk.Label(popup, text=f"Type: {room[2]}").pack()
    tk.Label(popup, text=f"Rent: ₹{room[3]}").pack()

    tk.Label(popup, text="Check-out Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(popup)
    date_entry.pack()

    def confirm():
        checkout = date_entry.get().strip()

        # 🔹 Validate date format if entered
        if checkout != "":
            try:
                datetime.strptime(checkout, "%Y-%m-%d")
            except:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return

        success = insert_booking(
            room_id=room[0],
            user_id=user_id,
            checkout_date=checkout if checkout != "" else None
        )

        if success:
            messagebox.showinfo("Success", "Room booked successfully!")
            popup.destroy()
            parent.destroy()  # close room list window
        else:
            messagebox.showerror("Error", "Booking failed")

    tk.Button(popup, text="Confirm", command=confirm).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack()


# 🔹 Show available rooms (UI)
def show_booking_screen(root, user_id):
    window = tk.Toplevel(root)
    window.title("Available Rooms")
    center_window(window, 700, 450)

    window.configure(bg="#f5f5f5")

    tk.Label(window, text="Available Rooms", font=("Arial", 18, "bold")).pack(pady=15)

    header = tk.Frame(window)
    header.pack(fill="x", padx=20)

    tk.Label(header, text="Room No", width=15, font=("Arial", 10, "bold")).grid(row=0, column=0)
    tk.Label(header, text="Type", width=15, font=("Arial", 10, "bold")).grid(row=0, column=1)
    tk.Label(header, text="Rent", width=15, font=("Arial", 10, "bold")).grid(row=0, column=2)

    rooms = get_available_rooms()

    if not rooms:
        tk.Label(window, text="No rooms available").pack(pady=20)
        return

    for room in rooms:
        frame = tk.Frame(window, bd=1, relief="solid")
        frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame, text=room[1], width=15).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame, text=room[2], width=15).grid(row=0, column=1, padx=10)
        tk.Label(frame, text=f"₹{room[3]}", width=15).grid(row=0, column=2, padx=10)

        tk.Button(
           frame,
           text="Book Now",
           bg="#4CAF50",
           fg="white",
           command=lambda r=room: confirm_booking_popup(r, user_id, window)
        ).grid(row=0, column=3, padx=10)


# 🔹 Get bookings (for Host / Guest)
def get_bookings(user_id, role):
    if role == "Host":
        cursor.execute("""
            SELECT b.booking_id, u.name, r.room_number,
                   b.check_in_date, b.check_out_date, b.booking_status
            FROM booking b
            JOIN users u ON b.guest_id = u.user_id
            JOIN room r ON b.room_id = r.room_id
        """)
    else:
        cursor.execute("""
            SELECT b.booking_id, r.room_number,
                   b.check_in_date, b.check_out_date, b.booking_status
            FROM booking b
            JOIN room r ON b.room_id = r.room_id
            WHERE b.guest_id = %s
        """, (user_id,))

    return cursor.fetchall()

#TEST
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Booking Test")
    root.geometry("400x300")

    # Simulate logged-in user (Meera = user_id 2)
    test_user_id = 2  

    tk.Button(root, text="Open Booking Screen",
              command=lambda: show_booking_screen(root, test_user_id)).pack(pady=40)

    root.mainloop()
