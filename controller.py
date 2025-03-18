from model import KursRepository, StudentRepository
from service import Service
from view import View

class Controller:
    @staticmethod
    def start():
        # 1. Lade die Daten
        student = StudentRepository.lade_student('student.csv')
        kurse = KursRepository.lade_kurse('kurse.csv')

        while True:
            # 2. Berechne die Werte
            ects = Service.berechne_ects(kurse)
            durchschnitt = Service.berechne_durchschnitt(kurse)

            # 3. Zeige die Ergebnisse in der View
            View.zeige_statistik(student, ects, durchschnitt)
            View.zeige_kurse(kurse)

            # 4. Beispiel: Note setzen
            kurscode = input("Gib den Kurscode für die neue Note ein (oder 'q' zum Beenden): ")
            if kurscode.lower() == 'q':
                break

            note = input("Gib die neue Note ein: ")
            try:
                note = float(note)
                if Service.setze_note(kurse, kurscode, note):
                    # Aktualisierte Werte speichern
                    KursRepository.speichere_kurse('kurse.csv', kurse)
                    View.zeige_nachricht("Note erfolgreich gespeichert!")
                else:
                    View.zeige_fehler("Ungültiger Kurscode!")
            except ValueError:
                View.zeige_fehler("Ungültige Eingabe für die Note!")

        View.zeige_nachricht("Anwendung beendet.")

# Startpunkt der Anwendung
if __name__ == "__main__":
    Controller.start()