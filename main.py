import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from user_room import register_user, login_user, get_users, add_room, get_rooms
from booking import get_bookings, rooms_for_booking  
from payment import show_all_payments, record_payments, show_guest_payments
from staff import view_staff_popup , view_assignments_popup, assign_staff_popup


def center_window(win, width, height):
    win.update_idletasks()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry(f"{width}x{height}+{x}+{y}")


def view_guests(parent, user_id):
    win = tk.Toplevel(parent)
    win.title("Guests")
    center_window(win, 700, 450)

    tk.Label(win, text="Guest List",
             font=("Arial", 16, "bold")).pack(pady=10)

    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    users = get_users(user_id)

    if not users:
        tk.Label(container, text="No guests found").pack()
        return

    table = tk.Frame(container)
    table.pack(fill="x")

    headers = ["User ID", "Name", "Phone", "Email", "Room"]
    for col, h in enumerate(headers):
        tk.Label(table, text=h,
                 font=("Arial", 12, "bold"),
                 bg="#e6e6e6",
                 width=15,
                 padx=5, pady=5,
                 relief="solid").grid(row=0, column=col, sticky="nsew")

    for i, u in enumerate(users, start=1):
        values = [u[0], u[1], u[2], u[3], u[4]]

        for col, val in enumerate(values):
            tk.Label(table, text=val,
                     font=("Arial", 12),
                     width=15,
                     padx=5, pady=5,
                     relief="solid").grid(row=i, column=col, sticky="nsew")

    for col in range(len(headers)):
        table.grid_columnconfigure(col, weight=1)



def show_rooms(parent, user_id):
    win = tk.Toplevel(parent)
    win.title("Rooms")
    center_window(win, 700, 450)

    tk.Label(win, text="Rooms",
             font=("Arial", 16, "bold")).pack(pady=10)

    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    rooms = get_rooms()

    if not rooms:
        tk.Label(container, text="No rooms available").pack()
        return

    table = tk.Frame(container)
    table.pack(fill="x")

    headers = ["Room No", "Type", "Rent", "Status"]
    for col, h in enumerate(headers):
        tk.Label(table, text=h,
                 font=("Arial", 12, "bold"),
                 bg="#e6e6e6",
                 width=15,
                 padx=5, pady=5,
                 relief="solid").grid(row=0, column=col, sticky="nsew")

    for i, r in enumerate(rooms, start=1):
        values = [r[1], r[2], f"₹{r[3]}", r[4]]

        for col, val in enumerate(values):
            tk.Label(table, text=val,
                     font=("Arial", 12),
                     width=15,
                     padx=5, pady=5,
                     relief="solid").grid(row=i, column=col, sticky="nsew")

    for col in range(len(headers)):
        table.grid_columnconfigure(col, weight=1)

    tk.Button(win, text="Add Room",
              bg="#2ecc71", fg="white",
              font=("Arial", 11, "bold"),
              command=lambda: add_room_popup(win, user_id)
              ).pack(pady=15)


def add_room_popup(parent, user_id):
    popup = tk.Toplevel(parent)
    popup.title("Add Room")

    center_window(popup, 350, 300)

    frame = tk.Frame(popup)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Add Room",
             font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(frame, text="Room Number").pack(anchor="w")
    room_no = tk.Entry(frame)
    room_no.pack(fill="x", pady=5)

    tk.Label(frame, text="Room Type").pack(anchor="w")
    room_type = tk.Entry(frame)
    room_type.pack(fill="x", pady=5)

    tk.Label(frame, text="Rent per Month").pack(anchor="w")
    rent = tk.Entry(frame)
    rent.pack(fill="x", pady=5)

    def submit():
        rn = room_no.get().strip()
        rt = room_type.get().strip()
        r = rent.get().strip()

    
        if rn == "" or rt == "" or r == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            r = float(r)
        except:
            messagebox.showerror("Error", "Rent must be a number")
            return


        success = add_room(rn, rt, r, "Available", user_id)

        if success:
            messagebox.showinfo("Success", "Room Added Successfully")
            popup.destroy()
            parent.destroy()
            show_rooms(root, user_id)
        else:
            messagebox.showerror("Error", "Failed to add room")


    tk.Button(frame, text="Add Room",
              command=submit).pack(pady=10)

    tk.Button(frame, text="Cancel",
              command=popup.destroy).pack()


def show_payments_menu(parent, user_id):
    win = tk.Toplevel(parent)
    win.title("Payments")

    center_window(win, 500, 350)

    win.transient(parent)
    win.grab_set()

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=40, pady=40)

    tk.Label(frame, text="Payments",
             font=("Arial", 18, "bold")).pack(pady=15)

    tk.Button(frame,
              text="View Payments",
              font=("Arial", 12),
              height=2,
              command=lambda: show_all_payments(win)
              ).pack(fill="x", pady=10)

    tk.Button(frame,
              text="Record Payments",
              font=("Arial", 12),
              height=2,
              command=lambda: record_payments(win)
              ).pack(fill="x", pady=10)

    tk.Button(frame,
              text="⬅ Back",
              font=("Arial", 11),
              command=win.destroy).pack(pady=15)

    win.protocol("WM_DELETE_WINDOW", win.destroy)

def show_staff_menu(parent, user_id):
    win = tk.Toplevel(parent)
    win.title("Staff Management")
    center_window(win, 500, 400)

    frame = tk.Frame(win)
    frame.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(frame, text="Staff Management",
             font=("Arial", 18, "bold")).pack(pady=15)

    tk.Button(frame, text="View Staff",
              command=lambda: view_staff_popup(win)).pack(fill="x", pady=5)

    tk.Button(frame, text="Assign Staff",
              command=lambda: assign_staff_popup(win)).pack(fill="x", pady=5)

    tk.Button(frame, text="View Assignments",
              command=lambda: view_assignments_popup(win)).pack(fill="x", pady=5)

    tk.Button(frame, text="⬅ Back",
              command=win.destroy).pack(pady=15)
    

def show_bookings(parent, user_id):
    win = tk.Toplevel(parent)
    win.title("Bookings")
    center_window(win, 800, 450)

    tk.Label(win, text="Bookings",
             font=("Arial", 16, "bold")).pack(pady=10)

    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=20, pady=10)

    bookings = get_bookings(user_id, "Host")

    if not bookings:
        tk.Label(container, text="No bookings found").pack()
        return

    table = tk.Frame(container)
    table.pack(fill="x")

    headers = ["Booking ID", "Guest", "Room", "Check-in", "Check-out", "Status"]
    for col, h in enumerate(headers):
        tk.Label(table, text=h,
                 font=("Arial", 12, "bold"),
                 bg="#e6e6e6",
                 width=15,
                 padx=5, pady=5,
                 relief="solid").grid(row=0, column=col, sticky="nsew")

    for i, b in enumerate(bookings, start=1):
        values = [b[0], b[1], b[2], b[3], b[4] if b[4] else "-", b[5]  ]

        for col, val in enumerate(values):
            tk.Label(table, text=val,
                     font=("Arial", 12),
                     width=15,
                     padx=5, pady=5,
                     relief="solid").grid(row=i, column=col, sticky="nsew")

    for col in range(len(headers)):
        table.grid_columnconfigure(col, weight=1)


def show_host_menu(root, user_id):
    menu = tk.Toplevel(root)
    menu.title("Host Dashboard")

    center_window(menu, 700, 600)   

    menu.configure(bg="#f5f5f5")   


    frame = tk.Frame(menu, bg="#f5f5f5")
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    
    tk.Label(frame, text="HOST DASHBOARD",
             font=("Arial", 30, "bold"),
             bg="#f5f5f5").pack(pady=10)

    tk.Label(frame, text="Manage your PG easily",
             font=("Arial", 20),
             bg="#f5f5f5").pack(pady=5)

    
    def make_button(text, cmd):
        return tk.Button(
            frame,
            text=text,
            font=("Arial", 12),
            height=2,
            command=cmd
        )

    make_button("👥 View Guests",
                lambda: view_guests(menu,user_id)).pack(fill="x", pady=8)

    make_button("🏠 Rooms",
                lambda: show_rooms(menu, user_id)).pack(fill="x", pady=8)

    make_button("📘 Bookings",
                lambda: show_bookings(menu, user_id)).pack(fill="x", pady=8)

    make_button("💰 Payments",
                lambda: show_payments_menu(menu,user_id)).pack(fill="x", pady=8)
    make_button("👨‍🔧 Staff Management",
            lambda: show_staff_menu(menu, user_id)).pack(fill="x", pady=8)


    def logout():
        menu.destroy()

        try:
            email_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
        except:
            pass

        root.deiconify()

    tk.Button(frame, text="🚪 Logout",
              font=("Arial", 12, "bold"),
              bg="#e74c3c", fg="white",
              height=2,
              command=logout).pack(fill="x", pady=20)

    menu.protocol("WM_DELETE_WINDOW", logout)


def show_user_bookings(root, user_id):
    window = tk.Toplevel(root)
    window.title("My Bookings")
    center_window(window, 700, 500)
    window.configure(bg="#f5f5f5")

    tk.Label(window, text="My Bookings",
             font=("Arial", 18, "bold"),
             bg="#f5f5f5").pack(pady=15)

    container = tk.Frame(window, bg="#f5f5f5")
    container.pack(padx=20, pady=10)

    header = tk.Frame(container, bg="#f5f5f5")
    header.pack(pady=5)

    tk.Label(header, text="Room", width=12, font=("Arial", 13, "bold")).grid(row=0, column=0)
    tk.Label(header, text="Check-in", width=12, font=("Arial", 13, "bold")).grid(row=0, column=1)
    tk.Label(header, text="Check-out", width=12, font=("Arial", 13, "bold")).grid(row=0, column=2)
    tk.Label(header, text="Status", width=12, font=("Arial", 13, "bold")).grid(row=0, column=3)

    
    bookings = get_bookings(user_id, "Guest")

    if not bookings:
        tk.Label(window, text="No bookings found",
                 font=("Arial", 13, "bold"),
                 bg="#f5f5f5").pack(pady=20)
        return

    
    for b in bookings:
        frame = tk.Frame(container, bd=1, relief="solid")
        frame.pack(fill="x", pady=5)

        tk.Label(frame, text=b[1], width=13, font=("Arial", 13)).grid(row=0, column=0)
        tk.Label(frame, text=str(b[2]) if b[2] else "-", width=15, font=("Arial", 13)).grid(row=0, column=1)
        tk.Label(frame, text=str(b[3]) if b[3] else "-", width=12, font=("Arial", 13)).grid(row=0, column=2)
        tk.Label(frame, text=b[4], width=15, font=("Arial", 13)).grid(row=0, column=3)


def show_guest_menu(root, user_id):
    menu = tk.Toplevel(root)
    menu.title("Guest Dashboard")

    center_window(menu, 700, 600)

    menu.configure(bg="#f5f5f5")

    
    frame = tk.Frame(menu, bg="#f5f5f5")
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    
    tk.Label(frame, text="GUEST DASHBOARD",
             font=("Arial", 30, "bold"),
             bg="#f5f5f5").pack(pady=10)

    tk.Label(frame, text="Access your PG services",
             font=("Arial", 20),
             bg="#f5f5f5").pack(pady=5)

    
    def make_button(text, cmd):
        return tk.Button(
            frame,
            text=text,
            font=("Arial", 12),
            height=2,
            command=cmd
        )

    
    make_button("🏠 Rooms",
                lambda: rooms_for_booking(menu, user_id)).pack(fill="x", pady=8)

    make_button("📘 My Bookings",
                lambda: show_user_bookings(menu, user_id)).pack(fill="x", pady=8)

    make_button("💰 My Payments",
                lambda: show_guest_payments(menu, user_id)).pack(fill="x", pady=8)

    
    def logout():
        menu.destroy()

        try:
            email_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
        except:
            pass

        root.deiconify()

    tk.Button(frame, text="🚪 Logout",
              font=("Arial", 12, "bold"),
              bg="#e74c3c", fg="white",
              height=2,
              command=logout).pack(fill="x", pady=20)

    menu.protocol("WM_DELETE_WINDOW", logout)



def handle_login():
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if email == "" or phone == "":
        messagebox.showerror("Error", "All fields are required")
        return

    user = login_user(email, phone)

    if user:
        user_id, role = user   

        #messagebox.showinfo("Success", "Login Successful")

        root.withdraw()  

        if role == "Host":
            show_host_menu(root, user_id)
        else:
            show_guest_menu(root, user_id)

    else:
        messagebox.showerror("Error", "Invalid Credentials")



def open_register():
    reg = tk.Toplevel(root)
    reg.title("Register")
    center_window(reg, 400, 400)

    frame = tk.Frame(reg)
    frame.pack(expand=True)

    tk.Label(frame, text="Register", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(frame, text="Create your account", font=("Arial", 13), fg="gray" ).pack(pady=15)

    tk.Label(frame, text="Name").pack()
    name = tk.Entry(frame)
    name.pack()
    
    tk.Label(frame, text="Email").pack()
    email = tk.Entry(frame)
    email.pack()

    tk.Label(frame, text="Phone").pack()
    phone = tk.Entry(frame)
    phone.pack()

   
    def submit(): 
        n = name.get().strip()
        e = email.get().strip()
        p = phone.get().strip()

        if n == "" or e == "" or p == "":
            messagebox.showerror("Error", "All fields are required", parent=reg)
            reg.lift()      
            reg.focus_force()
            return

        user_id = register_user(n, p, e)

        if not user_id:
            messagebox.showerror("Error", "Invalid data or User already Exists", parent=reg)
            reg.lift()
            reg.focus_force()
            return

        messagebox.showinfo("Success", "Registered Successfully", parent=reg)
        reg.destroy()
        root.withdraw()
        show_guest_menu(root, user_id)

    tk.Button(frame, text="Register", width=10, command=submit).pack(pady=10)
    tk.Button(frame, text="Back", width=10, command=reg.destroy).pack()


root = tk.Tk()
root.title("PG Management System")
center_window(root, 700, 500)

frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="Sunrise PG Management System",
         font=("Segoe UI", 18, "bold")).pack(pady=10)

img = Image.open("logo.jpeg")  
img = img.resize((220, 160))   

photo = ImageTk.PhotoImage(img)

img_label = tk.Label(frame, image=photo)
img_label.image = photo   
img_label.pack(pady=10)

tk.Label(frame, text="Email").pack()
email_entry = tk.Entry(frame, width=30)
email_entry.pack(pady=3)

tk.Label(frame, text="Phone").pack()
phone_entry = tk.Entry(frame, width=30)
phone_entry.pack(pady=3)

# Buttons
tk.Button(frame, text="Login", width=15,
          command=handle_login).pack(pady=5)

tk.Button(frame, text="Go to Register", width=15,
          command=open_register).pack(pady=5)


root.mainloop()

