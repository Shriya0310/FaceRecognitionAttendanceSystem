import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")

app = ctk.CTk()

app.title("Registered Users")
app.geometry("700x500")

title = ctk.CTkLabel(
    app,
    text="Registered Users",
    font=("Segoe UI", 24, "bold")
)

title.pack(pady=20)

textbox = ctk.CTkTextbox(
    app,
    width=600,
    height=350
)

textbox.pack(pady=20)

conn = sqlite3.connect(
    "database/faces.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT id, name FROM persons"
)

rows = cursor.fetchall()

conn.close()

textbox.insert(
    "end",
    "ID\tName\n"
)

textbox.insert(
    "end",
    "-" * 30 + "\n"
)

for user_id, name in rows:

    textbox.insert(
        "end",
        f"{user_id}\t{name}\n"
    )

textbox.configure(
    state="disabled"
)

app.mainloop()