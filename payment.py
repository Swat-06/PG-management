import tkinter as tk
from tkinter import messagebox
from db import conn, cursor


# 🔹 Get payments for guest
def get_guest_payments(user_id):
    cursor.execute("""
        SELECT p.payment_id, r.room_number, p.amount,
               p.payment_date, p.payment_status
        FROM payment p
        JOIN booking b ON p.booking_id = b.booking_id
        JOIN room r ON b.room_id = r.room_id
        WHERE b.guest_id = %s
    """, (user_id,))
    return cursor.fetchall()


# 🔹 Get all payments (Host view)
def get_all_payments():
    cursor.execute("""
        SELECT p.payment_id, u.name, r.room_number,
               p.amount, p.payment_date, p.payment_status
        FROM payment p
        JOIN booking b ON p.booking_id = b.booking_id
        JOIN users u ON b.guest_id = u.user_id
        JOIN room r ON b.room_id = r.room_id
    """)
    return cursor.fetchall()


# 🔹 Get pending payments (for record payments)
def get_pending_payments():
    cursor.execute("""
        SELECT p.payment_id, u.name, r.room_number,
               p.amount, p.payment_date, p.payment_status
        FROM payment p
        JOIN booking b ON p.booking_id = b.booking_id
        JOIN users u ON b.guest_id = u.user_id
        JOIN room r ON b.room_id = r.room_id
        WHERE p.payment_status = 'Pending'
    """)
    return cursor.fetchall()


# 🔹 Update payment (HOST ACTION)
def update_payment_status(payment_id):
    try:
        cursor.execute("""
            UPDATE payment
            SET payment_status = 'Paid',
                payment_date = CURDATE()
            WHERE payment_id = %s
        """, (payment_id,))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False

def center_window(win, width, height):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry(f"{width}x{height}+{x}+{y}")



# 🔹 Guest UI → View Payments
def show_guest_payments(root, user_id):
    window = tk.Toplevel(root)
    window.title("My Payments")
    center_window(window, 700, 400)
    window.configure(bg="#f5f5f5")

    tk.Label(window, text="My Payments", font=("Arial", 16)).pack(pady=10)

    header = tk.Frame(window)
    header.pack(fill="x", padx=20)

    tk.Label(header, text="Room", width=10).grid(row=0, column=0)
    tk.Label(header, text="Amount", width=10).grid(row=0, column=1)
    tk.Label(header, text="Date", width=15).grid(row=0, column=2)
    tk.Label(header, text="Status", width=10).grid(row=0, column=3)

    payments = get_guest_payments(user_id)

    if not payments:
        tk.Label(window, text="No payments found").pack(pady=20)
        return

    for p in payments:
        frame = tk.Frame(window, bd=1, relief="solid")
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(frame, text=p[1], width=10).grid(row=0, column=0)
        tk.Label(frame, text=f"₹{p[2]}", width=10).grid(row=0, column=1)
        tk.Label(frame, text=str(p[3]) if p[3] else "-", width=15).grid(row=0, column=2)
        tk.Label(frame, text=p[4], width=10).grid(row=0, column=3)


# 🔹 Host UI → View Payments
def show_all_payments(root):
    window = tk.Toplevel(root)
    window.title("All Payments")
    center_window(window, 700, 400)

    tk.Label(window, text="All Payments", font=("Arial", 16)).pack(pady=10)

    header = tk.Frame(window)
    header.pack(fill="x", padx=20)

    tk.Label(header, text="Guest", width=12).grid(row=0, column=0)
    tk.Label(header, text="Room", width=10).grid(row=0, column=1)
    tk.Label(header, text="Amount", width=10).grid(row=0, column=2)
    tk.Label(header, text="Date", width=15).grid(row=0, column=3)
    tk.Label(header, text="Status", width=10).grid(row=0, column=4)

    payments = get_all_payments()

    if not payments:
        tk.Label(window, text="No payments found").pack(pady=20)
        return

    for p in payments:
        frame = tk.Frame(window, bd=1, relief="solid")
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(frame, text=p[1], width=12).grid(row=0, column=0)
        tk.Label(frame, text=p[2], width=10).grid(row=0, column=1)
        tk.Label(frame, text=f"₹{p[3]}", width=10).grid(row=0, column=2)
        tk.Label(frame, text=str(p[4]) if p[4] else "-", width=15).grid(row=0, column=3)
        tk.Label(frame, text=p[5], width=10).grid(row=0, column=4)


# 🔹 Host UI → Record Payments
def record_payments(root):
    window = tk.Toplevel(root)
    window.title("Record Payments")
    center_window(window, 700, 400)
    window.configure(bg="#f5f5f5")

    window.transient(root)
    window.grab_set()

    tk.Label(window, text="Pending Payments", font=("Arial", 16)).pack(pady=10)

    header = tk.Frame(window)
    header.pack(fill="x", padx=20)

    tk.Label(header, text="Guest", width=12).grid(row=0, column=0)
    tk.Label(header, text="Room", width=10).grid(row=0, column=1)
    tk.Label(header, text="Amount", width=10).grid(row=0, column=2)
    tk.Label(header, text="Date", width=15).grid(row=0, column=3)
    tk.Label(header, text="Status", width=10).grid(row=0, column=4)

    payments = get_pending_payments()

    if not payments:
        tk.Label(window, text="No pending payments").pack(pady=20)
        return

    for p in payments:
        frame = tk.Frame(window, bd=1, relief="solid")
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(frame, text=p[1], width=12).grid(row=0, column=0)
        tk.Label(frame, text=p[2], width=10).grid(row=0, column=1)
        tk.Label(frame, text=f"₹{p[3]}", width=10).grid(row=0, column=2)
        tk.Label(frame, text=str(p[4]) if p[4] else "-", width=15).grid(row=0, column=3)
        tk.Label(frame, text=p[5], width=10).grid(row=0, column=4)

        tk.Button(
            frame,
            text="Record Payment",
            bg="#4CAF50",
            fg="white",
            command=lambda pid=p[0]: handle_record_payment(window, root, pid)
        ).grid(row=0, column=5, padx=10)


# 🔹 Handle record payment
def handle_record_payment(window, root, payment_id):
    success = update_payment_status(payment_id)

    if success:
        messagebox.showinfo("Success", "Payment recorded successfully")
        window.destroy()
        record_payments(root)

    else:
        messagebox.showerror("Error", "Failed to update payment")


#TEST
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Payment Test")
    root.geometry("400x300")

    # Test buttons
    tk.Button(root, text="Guest Payments",
              command=lambda: show_guest_payments(root, 2)).pack(pady=10)

    tk.Button(root, text="All Payments (Host)",
              command=lambda: show_all_payments(root)).pack(pady=10)

    tk.Button(root, text="Record Payments",
              command=lambda: record_payments(root)).pack(pady=10)

    root.mainloop()
