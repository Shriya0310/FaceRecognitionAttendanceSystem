import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")

app = ctk.CTk()

app.title("Delete User")
app.geometry("500x350")

def delete_user():

    user_id = id_entry.get()

    if not user_id:
        status_label.configure(
            text="Enter User ID"
        )
        return

    conn = sqlite3.connect(
        "database/faces.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM persons WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    status_label.configure(
        text="User Deleted"
    )

title = ctk.CTkLabel(
    app,
    text="Delete User",
    font=("Segoe UI", 24, "bold")
)

title.pack(pady=20)

id_entry = ctk.CTkEntry(
    app,
    width=250,
    placeholder_text="Enter User ID"
)

id_entry.pack(pady=20)

delete_btn = ctk.CTkButton(
    app,
    text="Delete",
    command=delete_user
)

delete_btn.pack(pady=20)

status_label = ctk.CTkLabel(
    app,
    text="Waiting..."
)

status_label.pack(pady=20)

app.mainloop()