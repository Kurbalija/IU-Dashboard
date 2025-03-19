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
        
        if note == 'A':
            self.note = 0  # "A" wird intern als 0 gespeichert
        elif note:
            try:
                self.note = float(note)
            except ValueError:
                self.note = None
        else:
            self.note = None

class KursRepository:
    HEADERS = ['Kurscode', 'Kursname', 'ECTS', 'Note']

    @staticmethod
    def lade_kurse(dateipfad):
        kurse = []
        with open(dateipfad, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                kurs = Kurs(
                    kurscode=row['Kurscode'],
                    name=row['Kursname'],
                    ects=row['ECTS'],
                    note=row['Note']
                )
                kurse.append(kurs)
        return kurse
    
    @staticmethod
    def speichere_kurse(dateipfad, kurse):
        with open(dateipfad, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=KursRepository.HEADERS)
            writer.writeheader()
            for kurs in kurse:
                writer.writerow({
                    'Kurscode': kurs.kurscode,
                    'Kursname': kurs.name,
                    'ECTS': kurs.ects,
                    'Note': 'A' if kurs.note == 0 else (kurs.note if kurs.note is not None else '')
                })

class StudentRepository:
    HEADERS = ['Name', 'Studiengang', 'Ziel-ECTS']

    @staticmethod
    def lade_student(dateipfad):
        with open(dateipfad, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            daten = next(reader, None)
            if daten is not None:
                student = Student(
                    name=daten['Name'],
                    studiengang=daten['Studiengang'],
                    ziel_ects=daten['Ziel-ECTS']
                )
                return student
            else:
                print("Keine Studentendaten gefunden!")
                return None
    
    @staticmethod
    def speichere_student(dateipfad, student):
        with open(dateipfad, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=StudentRepository.HEADERS)
            writer.writeheader()
            writer.writerow({
                'Name': student.name,
                'Studiengang': student.studiengang,
                'Ziel-ECTS': student.ziel_ects
            })
