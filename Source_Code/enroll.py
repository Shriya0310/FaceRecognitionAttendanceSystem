import customtkinter as ctk
from tkinter import filedialog

import sqlite3
import pickle
import cv2

from insightface.app import FaceAnalysis
ctk.set_appearance_mode("dark")

app_face = FaceAnalysis()
app_face.prepare(ctx_id=-1)

app = ctk.CTk()

app.title("Enroll Person")
app.geometry("700x500")

selected_image = None

def choose_image():
    global selected_image

    selected_image = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png")
        ]
    )

    if selected_image:
        status_label.configure(
            text="Image Selected Successfully"
        )

title = ctk.CTkLabel(
    app,
    text="Enroll New Person",
    font=("Segoe UI", 26, "bold")
)

title.pack(pady=30)

name_entry = ctk.CTkEntry(
    app,
    width=300,
    placeholder_text="Enter Person Name"
)

name_entry.pack(pady=20)

select_btn = ctk.CTkButton(
    app,
    text="Select Face Image",
    command=choose_image
)

select_btn.pack(pady=15)

def enroll_person():

    global selected_image

    name = name_entry.get().strip()

    if not name:
        status_label.configure(
            text="Please enter a name"
        )
        return

    if not selected_image:
        status_label.configure(
            text="Please select an image"
        )
        return

    img = cv2.imread(selected_image)

    faces = app_face.get(img)

    if len(faces) == 0:
        status_label.configure(
            text="No face detected"
        )
        return

    embedding = faces[0].embedding

    embedding_blob = pickle.dumps(
        embedding
    )

    conn = sqlite3.connect(
        "database/faces.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO persons
        (name, embedding)
        VALUES (?, ?)
        """,
        (name, embedding_blob)
    )

    conn.commit()
    conn.close()

    status_label.configure(
        text=f"{name} enrolled successfully!"
    )

enroll_btn = ctk.CTkButton(
    app,
    text="Enroll",
    command=enroll_person
)
enroll_btn.pack(pady=15)

status_label = ctk.CTkLabel(
    app,
    text="Waiting for input..."
)

status_label.pack(pady=30)

app.mainloop()