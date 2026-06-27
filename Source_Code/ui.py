import customtkinter as ctk
import sqlite3
import subprocess

def open_enroll():
    subprocess.Popen(
        ["python", "enroll.py"]
    )

def open_recognition():
    subprocess.Popen(
        ["python", "recognize.py"]
    )

def open_users():
    subprocess.Popen(
        ["python", "view_users.py"]
    )

def open_delete_user():
    subprocess.Popen(
        ["python", "delete_user.py"]
    )

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("Face Recognition System")
app.geometry("1000x600")

# Sidebar
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

title = ctk.CTkLabel(
    sidebar,
    text="Face Recognition",
    font=("Segoe UI", 22, "bold")
)
title.pack(pady=(30, 20))

enroll_btn = ctk.CTkButton(
    sidebar,
    text="Enroll Person",
    width=180,
    height=40,
    command=open_enroll
)
enroll_btn.pack(pady=10)

recognize_btn = ctk.CTkButton(
    sidebar,
    text="Start Recognition",
    width=180,
    height=40,
    command=open_recognition
)
recognize_btn.pack(pady=10)

users_btn = ctk.CTkButton(
    sidebar,
    text="View Users",
    width=180,
    height=40,
    command=open_users
)

users_btn.pack(pady=10)

delete_btn = ctk.CTkButton(
    sidebar,
    text="Delete User",
    width=180,
    height=40,
    command=open_delete_user
)

delete_btn.pack(pady=10)

# Main Area
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

heading = ctk.CTkLabel(
    main_frame,
    text="Dashboard",
    font=("Segoe UI", 28, "bold")
)
heading.pack(pady=20)

# Cards
card1 = ctk.CTkFrame(main_frame, width=250, height=120)
card1.pack(pady=15)

card1.pack_propagate(False)

def get_user_count():

    conn = sqlite3.connect(
        "database/faces.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM persons"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def refresh_dashboard():

    users_label.configure(
        text=f"Registered Users\n{get_user_count()}"
    )

    app.after(
        3000,
        refresh_dashboard
    )


users_label = ctk.CTkLabel(
    card1,
    text=f"Registered Users\n{get_user_count()}",
    font=("Segoe UI", 20)
)
users_label.pack(expand=True)

card2 = ctk.CTkFrame(main_frame, width=250, height=120)
card2.pack(pady=15)

card2.pack_propagate(False)

db_label = ctk.CTkLabel(
    card2,
    text="Database Status\nConnected",
    font=("Segoe UI", 20)
)
db_label.pack(expand=True)

def open_users():
    subprocess.Popen(
        ["python", "view_users.py"]
    )

refresh_dashboard()

app.mainloop()
