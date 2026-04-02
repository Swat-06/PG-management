import tkinter as tk
from tkinter import messagebox
from db import conn, cursor


# 🔹 Add Staff
def add_staff(name, phone, role, salary):
    try:
        cursor.execute("""
            INSERT INTO staff (name, phone, role, salary)
            VALUES (%s, %s, %s, %s)
        """, (name, phone, role, salary))

        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 🔹 Get Staff
def get_staff():
    cursor.execute("SELECT * FROM staff")
    return cursor.fetchall()


# 🔹 Delete Staff
def delete_staff(staff_id):
    try:
        cursor.execute("DELETE FROM staff WHERE staff_id=%s", (staff_id,))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 🔹 Assign Staff to Room
def assign_staff(staff_id, room_id):
    try:
        cursor.execute("""
            INSERT INTO staff_assignment (staff_id, room_id)
            VALUES (%s, %s)
        """, (staff_id, room_id))

        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 🔹 View Assignments
def get_assignments():
    cursor.execute("""
        SELECT s.name, s.role, r.room_number
        FROM staff s
        JOIN staff_assignment sa ON s.staff_id = sa.staff_id
        JOIN room r ON sa.room_id = r.room_id
    """)
    return cursor.fetchall()


# 🔹 Center Window
def center_window(win, width, height):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


# 🔹 Add Staff Popup
def add_staff_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Add Staff")
    center_window(popup, 300, 300)

    tk.Label(popup, text="Add Staff").pack(pady=10)

    e1 = tk.Entry(popup); e1.pack()
    e2 = tk.Entry(popup); e2.pack()
    e3 = tk.Entry(popup); e3.pack()
    e4 = tk.Entry(popup); e4.pack()

    def submit():
        if add_staff(e1.get(), e2.get(), e3.get(), e4.get()):
            messagebox.showinfo("Success", "Added")
            popup.destroy()

    tk.Button(popup, text="Add", command=submit).pack(pady=10)


# 🔹 Assign Staff Popup
def assign_staff_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Assign Staff")
    center_window(popup, 300, 250)

    tk.Label(popup, text="Staff ID").pack()
    e1 = tk.Entry(popup); e1.pack()

    tk.Label(popup, text="Room ID").pack()
    e2 = tk.Entry(popup); e2.pack()

    def assign():
        if assign_staff(e1.get(), e2.get()):
            messagebox.showinfo("Success", "Assigned")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Failed")

    tk.Button(popup, text="Assign", command=assign).pack(pady=10)


# 🔹 View Assignments Popup
def view_assignments_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Assignments")
    center_window(popup, 350, 300)

    rows = get_assignments()

    for r in rows:
        tk.Label(popup, text=str(r)).pack()


# 🔹 View Staff Popup
def view_staff_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Staff List")
    center_window(popup, 300, 300)

    rows = get_staff()
    for r in rows:
        tk.Label(popup, text=str(r)).pack()


# 🔹 Delete Staff Popup
def delete_staff_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Delete Staff")
    center_window(popup, 300, 200)

    tk.Label(popup, text="Enter Staff ID").pack()
    e = tk.Entry(popup); e.pack()

    def delete():
        if delete_staff(e.get()):
            messagebox.showinfo("Deleted", "Success")
            popup.destroy()

    tk.Button(popup, text="Delete", command=delete).pack(pady=10)


# ✅ TEST BLOCK (LIKE BOOKING MODULE)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Staff Test")
    root.geometry("400x300")

    tk.Button(root, text="Add Staff",
              command=lambda: add_staff_popup(root)).pack(pady=10)

    tk.Button(root, text="View Staff",
              command=lambda: view_staff_popup(root)).pack(pady=10)

    tk.Button(root, text="Assign Staff",
              command=lambda: assign_staff_popup(root)).pack(pady=10)

    tk.Button(root, text="View Assignments",
              command=lambda: view_assignments_popup(root)).pack(pady=10)

    tk.Button(root, text="Delete Staff",
              command=lambda: delete_staff_popup(root)).pack(pady=10)

    root.mainloop()

