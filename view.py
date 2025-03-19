import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
    def __init__(self, student, kurse, ects, durchschnitt):
        super().__init__()
        self.title("Dashboard")
        self.geometry("600x400")
        self.config(bg="white")

        # Statistik
        label = tk.Label(self, text="STUDENTEN-ÜBERSICHT", font=("Arial", 16), bg="white")
        label.pack(pady=5)

        tk.Label(self, text=f"Name: {student.name}", bg="white").pack()
        tk.Label(self, text=f"Studiengang: {student.studiengang}", bg="white").pack()
        tk.Label(self, text=f"Ziel-ECTS: {student.ziel_ects}", bg="white").pack()
        tk.Label(self, text=f"Erreichte ECTS: {ects}", bg="white").pack()
        tk.Label(self, text=f"Notendurchschnitt: {durchschnitt if durchschnitt else '-'}", bg="white").pack()

        # Fortschrittsbalken
        self.progress = ttk.Progressbar(self, length=400, mode="determinate")
        self.progress.pack(pady=5)
        fortschritt = (ects / student.ziel_ects) * 100 if student.ziel_ects > 0 else 0
        self.progress["value"] = fortschritt

        # Kurse
        for kurs in kurse:
            note = "A" if kurs.note == 0 else (f"{kurs.note:.2f}" if kurs.note is not None else "-")
            tk.Label(self, text=f"{kurs.kurscode} - {kurs.name} - {kurs.ects} ECTS - Note: {note}", bg="white").pack()

        tk.Button(self, text="Schließen", command=self.destroy).pack(pady=5)
