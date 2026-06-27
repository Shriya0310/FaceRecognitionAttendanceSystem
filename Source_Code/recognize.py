import customtkinter as ctk
from tkinter import filedialog

import sqlite3
import pickle
import cv2
import numpy as np

from insightface.app import FaceAnalysis

ctk.set_appearance_mode("dark")

face_app = FaceAnalysis()
face_app.prepare(ctx_id=-1)

selected_image = None

app = ctk.CTk()
app.geometry("700x500")
app.title("Recognition")

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def choose_image():
    global selected_image

    selected_image = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png")
        ]
    )

    if selected_image:
        status_label.configure(
            text="Image Selected"
        )

def recognize_person():

    global selected_image

    if not selected_image:
        status_label.configure(
            text="Please select image"
        )
        return

    img = cv2.imread(selected_image)

    faces = face_app.get(img)

    if len(faces) == 0:
        status_label.configure(
            text="No face detected"
        )
        return

    test_embedding = faces[0].embedding

    conn = sqlite3.connect(
        "database/faces.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, embedding FROM persons"
    )

    rows = cursor.fetchall()

    conn.close()

    best_name = "Unknown"
    best_score = 0

    for name, emb_blob in rows:

        stored_embedding = pickle.loads(
            emb_blob
        )

        similarity = cosine_similarity(
            test_embedding,
            stored_embedding
        )

        if similarity > best_score:
            best_score = similarity
            best_name = name

    confidence = best_score * 100

    if best_score < 0.50:
        best_name = "Unknown"

    result_label.configure(
        text=f"Name: {best_name}"
    )

    confidence_label.configure(
        text=f"Confidence: {confidence:.2f}%"
    )

title = ctk.CTkLabel(
    app,
    text="Face Recognition",
    font=("Segoe UI", 26, "bold")
)

title.pack(pady=20)

select_btn = ctk.CTkButton(
    app,
    text="Select Image",
    command=choose_image
)

select_btn.pack(pady=10)

recognize_btn = ctk.CTkButton(
    app,
    text="Recognize",
    command=recognize_person
)

recognize_btn.pack(pady=10)

result_label = ctk.CTkLabel(
    app,
    text="Name: -",
    font=("Segoe UI", 20)
)

result_label.pack(pady=20)

confidence_label = ctk.CTkLabel(
    app,
    text="Confidence: -",
    font=("Segoe UI", 20)
)

confidence_label.pack(pady=20)

status_label = ctk.CTkLabel(
    app,
    text="Waiting..."
)

status_label.pack(pady=20)

app.mainloop()