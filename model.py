import csv

class Student:
    def __init__(self, name, studiengang, ziel_ects):
        self.name = name
        self.studiengang = studiengang
        self.ziel_ects = int(ziel_ects)

class Kurs:
    def __init__(self, kurscode, name, ects, note=None):
        self.kurscode = kurscode
        self.name = name
        self.ects = int(ects)
        if note == "A":
            self.note = 0.0
        elif note:
            try:
                self.note = float(note)
            except ValueError:
                self.note = None
        else:
            self.note = None

class KursRepository:
    HEADERS = ["Kurscode", "Kursname", "ECTS", "Note"]

    @staticmethod
    def lade_kurse(dateipfad):
        kurse = []
        with open(dateipfad, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                k = Kurs(
                    kurscode=row["Kurscode"],
                    name=row["Kursname"],
                    ects=row["ECTS"],
                    note=row["Note"]
                )
                kurse.append(k)
        return kurse

    @staticmethod
    def speichere_kurse(dateipfad, kurse):
        with open(dateipfad, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=KursRepository.HEADERS)
            writer.writeheader()
            for k in kurse:
                n = "A" if k.note == 0.0 else (k.note if k.note is not None else "")
                writer.writerow({
                    "Kurscode": k.kurscode,
                    "Kursname": k.name,
                    "ECTS": k.ects,
                    "Note": n
                })

class StudentRepository:
    HEADERS = ["Name", "Studiengang", "Ziel-ECTS"]

    @staticmethod
    def lade_student(dateipfad):
        with open(dateipfad, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            daten = next(reader, None)
            if daten:
                return Student(
                    name=daten["Name"],
                    studiengang=daten["Studiengang"],
                    ziel_ects=daten["Ziel-ECTS"]
                )
            return None

    @staticmethod
    def speichere_student(dateipfad, student):
        with open(dateipfad, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=StudentRepository.HEADERS)
            writer.writeheader()
            writer.writerow({
                "Name": student.name,
                "Studiengang": student.studiengang,
                "Ziel-ECTS": student.ziel_ects
            })
