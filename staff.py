import tkinter as tk
from tkinter import messagebox
from db import conn, cursor



def add_staff(name, phone, role):
    try:
        cursor.execute("""
            INSERT INTO staff (name, phone, role)
            VALUES (%s, %s, %s)
        """, (name, phone, role))

        conn.commit()
        print("Inserted into DB") 
        return True

    except Exception as e:
        print("Error:", e)
        return False



def get_staff():
    cursor.execute("SELECT * FROM staff")
    return cursor.fetchall()



def delete_staff(staff_id):
    try:
        cursor.execute("DELETE FROM staff_assignment WHERE staff_id = %s", (staff_id,))
        cursor.execute("DELETE FROM staff WHERE staff_id = %s", (staff_id,))
        
        conn.commit()
        return True

    except Exception as e:
        print("Delete Error:", e)
        return False



def assign_staff(staff_id, room_id, task_type, status):
    try:
        cursor.execute("""
            INSERT INTO staff_assignment 
            (staff_id, room_id, task_type, assigned_date, task_status)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (staff_id, room_id, task_type, status))
        conn.commit()
        return True
    except Exception as e:
        print("Assign Error:", e)
        return False

def get_assignments():
    cursor.execute("""
        SELECT s.name, s.role, r.room_number
        FROM staff s
        JOIN staff_assignment sa ON s.staff_id = sa.staff_id
        JOIN room r ON sa.room_id = r.room_id
    """)
    return cursor.fetchall()



def center_window(win, width, height):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")



def add_staff_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Add Staff")
    center_window(popup, 300, 300)

    tk.Label(popup, text="Add Staff", font=("Arial", 12)).pack(pady=10)

    tk.Label(popup, text="Name").pack()
    e1 = tk.Entry(popup)
    e1.pack(pady=5)

    tk.Label(popup, text="Phone").pack()
    e2 = tk.Entry(popup)
    e2.pack(pady=5)

    tk.Label(popup, text="Role").pack()
    e3 = tk.Entry(popup)
    e3.pack(pady=5)

    def submit():
        if add_staff(e1.get(), e2.get(), e3.get()):
            messagebox.showinfo("Success", "Staff Added")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Failed")

    tk.Button(popup, text="Add", command=submit).pack(pady=10)


def assign_staff_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Assign Staff")
    center_window(popup, 350, 300)

    tk.Label(popup, text="Assign Staff", font=("Arial", 12)).pack(pady=10)

    tk.Label(popup, text="Staff ID").pack()
    e1 = tk.Entry(popup)
    e1.pack(pady=5)

    tk.Label(popup, text="Room ID").pack()
    e2 = tk.Entry(popup)
    e2.pack(pady=5)

    tk.Label(popup, text="Task Type").pack()
    e3 = tk.Entry(popup)
    e3.pack()

    tk.Label(popup, text="Status").pack()
    e4 = tk.Entry(popup)
    e4.pack()

    def assign():
        if assign_staff(e1.get(), e2.get(),e3.get(), e4.get()):
            messagebox.showinfo("Success", "Assigned")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Failed")

    tk.Button(popup, text="Assign", command=assign).pack(pady=10)


def view_staff_popup(parent):
    win = tk.Toplevel(parent)
    win.title("Staff")
    center_window(win, 700, 450)

    tk.Label(win, text="Staff",
             font=("Arial", 16, "bold")).pack(pady=10)

    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    staff = get_staff()

    if not staff:
        tk.Label(container, text="No staff found").pack()
    else:
        table = tk.Frame(container)
        table.pack(fill="x")

        headers = ["ID", "Name", "Phone", "Role", "Action"]
        for col, h in enumerate(headers):
            tk.Label(table, text=h,
                     font=("Arial", 12, "bold"),
                     bg="#e6e6e6",
                     width=15,
                     padx=5, pady=5,
                     relief="solid").grid(row=0, column=col, sticky="nsew")

        for i, s in enumerate(staff, start=1):
            values = [s[0], s[1], s[2], s[3]]

            for col, val in enumerate(values):
                tk.Label(table, text=val,
                         font=("Arial", 12),
                         width=15,
                         padx=5, pady=5,
                         relief="solid").grid(row=i, column=col, sticky="nsew")

            tk.Button(table, text="Delete",
                      bg="#e74c3c", fg="white",
                      command=lambda sid=s[0]: delete_staff_popup(sid, win)
                      ).grid(row=i, column=4, padx=5, pady=5)

        for col in range(len(headers)):
            table.grid_columnconfigure(col, weight=1)

    
    tk.Button(win, text="Add Staff",
              bg="#2ecc71", fg="white",
              font=("Arial", 11, "bold"),
              command=lambda: add_staff_popup(win)
              ).pack(pady=15)

def delete_staff_popup(staff_id, parent_window):
    popup = tk.Toplevel(parent_window)
    popup.title("Confirm Delete")
    center_window(popup, 300, 180)

    frame = tk.Frame(popup)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame,
             text="Are you sure you want to\n delete this staff?",
             font=("Arial", 12),
             justify="center").pack(pady=15)

    def confirm_delete():
        if delete_staff(staff_id):
            messagebox.showinfo("Success", "Staff deleted successfully")
            popup.destroy()
            parent_window.destroy()   
            view_staff_popup(root)          
        else:
            messagebox.showerror("Error", "Failed to delete")

    tk.Button(frame, text="Yes, Delete",
              bg="#e74c3c", fg="white",
              command=confirm_delete).pack(pady=5)

    tk.Button(frame, text="Cancel",
              command=popup.destroy).pack(pady=5)
    
def view_assignments_popup(parent):
    win = tk.Toplevel(parent)
    win.title("Staff Assignments")
    center_window(win, 700, 400)

    tk.Label(win, text="Staff Assignments",
             font=("Arial", 16, "bold")).pack(pady=10)

    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    assignments = get_assignments()

    if not assignments:
        tk.Label(container, text="No assignments found").pack()
        return

    table = tk.Frame(container)
    table.pack(fill="x")

    headers = ["Staff Name", "Role", "Room Number"]

    for col, h in enumerate(headers):
        tk.Label(table, text=h,
                 font=("Arial", 12, "bold"),
                 bg="#e6e6e6",
                 width=20,
                 padx=5, pady=5,
                 relief="solid").grid(row=0, column=col, sticky="nsew")

    for i, a in enumerate(assignments, start=1):
        for col, val in enumerate(a):
            tk.Label(table, text=val,
                     font=("Arial", 12),
                     width=20,
                     padx=5, pady=5,
                     relief="solid").grid(row=i, column=col, sticky="nsew")

    for col in range(len(headers)):
        table.grid_columnconfigure(col, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Staff Test")
    root.geometry("400x300")

    tk.Button(root, text="View Staff",
              command=lambda: view_staff_popup(root)).pack(pady=10)

    tk.Button(root, text="Assign Staff",
              command=lambda: assign_staff_popup(root)).pack(pady=10)


    root.mainloop()
