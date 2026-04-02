import tkinter as tk
from tkinter import messagebox

import user
import room

# ---------------- LOGIN WINDOW ----------------

def login_window():
    win = tk.Tk()
    win.title("Login")
    win.geometry("500x400")   # ✅ added

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="LOGIN", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(frame, text="Email").pack()
    entry_email = tk.Entry(frame, width=30)
    entry_email.pack(pady=5)

    tk.Label(frame, text="Phone").pack()
    entry_phone = tk.Entry(frame, width=30)
    entry_phone.pack(pady=5)

    tk.Button(frame, text="Login", width=20, height=2,
              command=lambda: login_action()).pack(pady=15)

    def login_action():
        user_data = user.login_user(entry_email.get(), entry_phone.get())

        if user_data is None:
            messagebox.showerror("Error", "Invalid Login")
        else:
            user_id, name, role = user_data
            win.destroy()

            if role == "Host":
                host_window()
            else:
                guest_window()

    win.mainloop()
# ---------------- REGISTER WINDOW ----------------

def register_window():
    win = tk.Tk()
    win.title("Register")
    win.geometry("500x400")   # ✅ added

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="REGISTER", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(frame, text="Name").pack()
    entry_name = tk.Entry(frame, width=30)
    entry_name.pack(pady=5)

    tk.Label(frame, text="Phone").pack()
    entry_phone = tk.Entry(frame, width=30)
    entry_phone.pack(pady=5)

    tk.Label(frame, text="Email").pack()
    entry_email = tk.Entry(frame, width=30)
    entry_email.pack(pady=5)

    def register_action():
        user.register_user(
            entry_name.get(),
            entry_phone.get(),
            entry_email.get()
        )
        messagebox.showinfo("Success", "Registered Successfully")
        win.destroy()
        login_window()

    tk.Button(frame, text="Register", width=20, height=2,
              command=register_action).pack(pady=15)

    win.mainloop()

# ---------------- HOST WINDOW ----------------

def host_window():
    win = tk.Tk()
    win.title("Host Dashboard")
    win.geometry("500x400")   # ✅ added

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="HOST DASHBOARD",
             font=("Arial", 16, "bold")).pack(pady=15)

    entry_rno = tk.Entry(frame, width=30); entry_rno.pack(pady=5)
    entry_rtype = tk.Entry(frame, width=30); entry_rtype.pack(pady=5)
    entry_rent = tk.Entry(frame, width=30); entry_rent.pack(pady=5)
    entry_status = tk.Entry(frame, width=30); entry_status.pack(pady=5)
    entry_hostid = tk.Entry(frame, width=30); entry_hostid.pack(pady=5)

    tk.Button(frame, text="Add Room", width=20, height=2,
              command=lambda: add_room_gui()).pack(pady=5)

    tk.Button(frame, text="View Rooms", width=20, height=2,
              command=lambda: view_rooms_gui()).pack(pady=5)

    def add_room_gui():
        room.add_room(
            entry_rno.get(),
            entry_rtype.get(),
            entry_rent.get(),
            entry_status.get(),
            entry_hostid.get()
        )
        messagebox.showinfo("Success", "Room Added")

    def view_rooms_gui():
        rows = room.get_rooms()
        data = "\n".join(str(r) for r in rows)
        messagebox.showinfo("Rooms", data)

    win.mainloop()

# ---------------- GUEST WINDOW ----------------

def guest_window():
    win = tk.Tk()
    win.title("Guest Dashboard")
    win.geometry("500x400")   # ✅ added

    frame = tk.Frame(win)
    frame.pack(expand=True)

    tk.Label(frame, text="GUEST DASHBOARD",
             font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(frame, text="View Available Rooms",
              width=25, height=2,
              command=lambda: view_rooms_gui()).pack(pady=20)

    def view_rooms_gui():
        rows = room.get_available_rooms()
        data = "\n".join(str(r) for r in rows)
        messagebox.showinfo("Available Rooms", data)

    win.mainloop()
    

# ---------------- START WINDOW ----------------

root = tk.Tk()
root.title("PG Management System")
root.geometry("400x300")

frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="PG MANAGEMENT SYSTEM", 
         font=("Arial", 18, "bold")).pack(pady=20)
tk.Button(frame, text="Login", 
          width=20, height=2,
          font=("Arial", 12),
          command=lambda: [root.destroy(), login_window()]
          ).pack(pady=10)

tk.Button(frame, text="Register", 
          width=20, height=2,
          font=("Arial", 12),
          command=lambda: [root.destroy(), register_window()]
          ).pack(pady=10)

root.mainloop()
