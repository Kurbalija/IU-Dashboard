import csv

class Student:
    """
    Repräsentiert einen Studierenden mit Name, Studiengang und
    einem selbst definierten Ziel an ECTS.
    """

    def __init__(self, name, studiengang, ziel_ects):
        """
        Erstellt ein Student-Objekt.

        :param name: Name des Studenten
        :param studiengang: Studiengangs-Bezeichnung, z. B. "Informatik"
        :param ziel_ects: gewünschte Ziel-ECTS (int), z. B. 180
        """
        self.name = name
        self.studiengang = studiengang
        self.ziel_ects = int(ziel_ects)


class Kurs:
    """
    Einzelner Kurs/Modul mit Kurscode, Bezeichnung, ECTS und einer Note.
    'A' (angerechnet) wird intern als 0.0 gespeichert.
    """

    def __init__(self, kurscode, name, ects, note=None):
        """
        Legt einen Kurs an, inkl. automatischer Umwandlung der Note.

        :param kurscode: z. B. "MAT01" oder "PROG02"
        :param name: Klartextname, z. B. "Mathematik I"
        :param ects: Anzahl der ECTS-Punkte als String oder int
        :param note: entweder None, Float/String oder "A" (angerechnet)
        """
        self.kurscode = kurscode
        self.name = name
        self.ects = int(ects)

        if note == "A":
            # Angerechnete Leistung -> 0.0
            self.note = 0.0
        elif note:
            try:
                self.note = float(note)
            except ValueError:
                self.note = None
        else:
            self.note = None


class KursRepository:
    """
    Statische Methoden zum Laden/Speichern einer Liste von Kurs-Objekten.
    Nutzt CSV-Dateien im DictWriter/DictReader-Format.
    """
    HEADERS = ["Kurscode", "Kursname", "ECTS", "Note"]

    @staticmethod
    def lade_kurse(dateipfad):
        """
        Liest Kursdaten aus einer CSV-Datei und gibt sie als Liste von Kurs-Objekten zurück.

        :param dateipfad: Pfad zur CSV-Datei, z. B. "CSV/kurse.csv"
        :return: Liste von Kurs-Objekten
        """
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
        """
        Schreibt eine Liste von Kurs-Objekten in eine CSV-Datei.
        Falls eine Note 0.0 ist, wird "A" in die CSV geschrieben.

        :param dateipfad: Pfad zur CSV-Datei, z. B. "CSV/kurse.csv"
        :param kurse: Liste von Kurs-Objekten
        """
        with open(dateipfad, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=KursRepository.HEADERS)
            writer.writeheader()
            for k in kurse:
                # 0.0 wird im System als angerechnet ("A") dargestellt
                n = "A" if k.note == 0.0 else (k.note if k.note is not None else "")
                writer.writerow({
                    "Kurscode": k.kurscode,
                    "Kursname": k.name,
                    "ECTS": k.ects,
                    "Note": n
                })


class StudentRepository:
    """
    Statische Methoden zum Laden/Speichern eines einzigen Studenten in einer CSV-Datei.
    """
    HEADERS = ["Name", "Studiengang", "Ziel-ECTS"]

    @staticmethod
    def lade_student(dateipfad):
        """
        Liest einen Studenten aus der CSV-Datei. Ist die Datei leer oder unvollständig,
        wird None zurückgegeben.

        :param dateipfad: Pfad zur CSV-Datei, z. B. "CSV/student.csv"
        :return: Ein Student-Objekt oder None
        """
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
        """
        Speichert die Daten des Studenten in eine CSV-Datei (überschreibt vorhandene Daten).

        :param dateipfad: Pfad zur CSV-Datei, z. B. "CSV/student.csv"
        :param student: Student-Objekt, das gespeichert werden soll
        """
        with open(dateipfad, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=StudentRepository.HEADERS)
            writer.writeheader()
            writer.writerow({
                "Name": student.name,
                "Studiengang": student.studiengang,
                "Ziel-ECTS": student.ziel_ects
            })
