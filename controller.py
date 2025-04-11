from model import StudentRepository, KursRepository
from service import Service

class Controller:
    """
    Vermittelt zwischen View, Model (Student/Kurs) und Service/Repositories.
    Lädt bei der Initialisierung die Student- und Kursdaten,
    erstellt die View und aktualisiert diese bei Änderungen.
    """

    def __init__(self):
        """
        Lädt beim Programmstart den/die Student(en) und Kurse aus CSV-Dateien,
        berechnet den anfänglichen ECTS-Stand sowie den Notendurchschnitt.
        Initialisiert dann die View, übergibt relevante Daten und zeigt sie an.
        """
        self.student = StudentRepository.lade_student("CSV/student.csv")
        self.kurse = KursRepository.lade_kurse("CSV/kurse.csv")
        self.ects = Service.berechne_ects(self.kurse)
        self.durchschnitt = Service.berechne_durchschnitt(self.kurse)

        # Import der View hier, um Zirkularimporte zu vermeiden
        from view import View
        self.view = View(self, self.student, self.kurse, self.ects, self.durchschnitt)

    def start(self):
        """
        Startet die Haupt-Ereignisschleife der GUI,
        sodass Benutzerinteraktionen verarbeitet werden können.
        """
        self.view.mainloop()

    def aktualisiere_note(self, kurscode, raw_input):
        """
        Versucht, die Note für den Kurs (kurscode) zu aktualisieren,
        indem der Service die Eingabe (raw_input) validiert.
        Speichert die Kurse bei Erfolg in CSV und aktualisiert die Stats.

        :param kurscode: Code des zu ändernden Kurses
        :param raw_input: Benutzereingabe für die Note (z.B. "2.3", "A", "-")
        :return: True, wenn die Note erfolgreich gesetzt wurde, sonst False
        """
        ok = Service.setze_note(self.kurse, kurscode, raw_input)
        if ok:
            KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
            self._update_stats()
        return ok

    def aktualisiere_kursname(self, kurscode, neuer_name):
        """
        Sucht das Kurs-Objekt anhand seines Codes und ändert den Kursnamen.
        Speichert die Änderung in CSV und aktualisiert den View, wenn erfolgreich.

        :param kurscode: Identifizierender Code (z.B. "MAT01")
        :param neuer_name: Neuer Name (z.B. "Mathematik I")
        :return: True, wenn gefunden und Name geändert, sonst False
        """
        for k in self.kurse:
            if k.kurscode == kurscode:
                k.name = neuer_name
                KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
                self._update_stats()
                return True
        return False

    def aktualisiere_kurscode(self, alter_kurscode, neuer_kurscode):
        """
        Ersetzt den Kurscode eines vorhandenen Kurses und speichert den Datensatz.
        Ideal, wenn Kurse umbenannt wurden oder ein Tippfehler korrigiert werden muss.

        :param alter_kurscode: Bisheriger Code
        :param neuer_kurscode: Neuer Code, z.B. "PROG02"
        :return: True, wenn der Kurscode aktualisiert wurde, sonst False
        """
        for k in self.kurse:
            if k.kurscode == alter_kurscode:
                k.kurscode = neuer_kurscode
                KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
                self._update_stats()
                return True
        return False

    def aktualisiere_kurs_ects(self, kurscode, neuer_ects):
        """
        Aktualisiert die ECTS-Zahl eines Kurses. Versucht, den Wert zu konvertieren.
        Falls kein numerischer Wert, wird False zurückgegeben.

        :param kurscode: Code des Kurses
        :param neuer_ects: ECTS-Angabe als String (wird in int konvertiert)
        :return: True, wenn ECTS erfolgreich geändert; False, wenn Konvertierung fehlschlug
        """
        for k in self.kurse:
            if k.kurscode == kurscode:
                try:
                    k.ects = int(neuer_ects)
                except ValueError:
                    return False
                KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
                self._update_stats()
                return True
        return False

    def aktualisiere_student(self, name, studiengang, ziel_ects):
        """
        Ändert die Basisdaten des Studierenden (Name, Studiengang, Ziel-ECTS).
        Aktualisiert danach die CSV-Datei und ruft _update_stats() auf.

        :param name: Neuer Name des Studenten
        :param studiengang: Neuer Studiengang
        :param ziel_ects: Neue Zielzahl von ECTS (int)
        """
        self.student.name = name
        self.student.studiengang = studiengang
        self.student.ziel_ects = ziel_ects
        StudentRepository.speichere_student("CSV/student.csv", self.student)
        self._update_stats()

    def _update_stats(self):
        """
        Aktualisiert die globalen Statistiken (ECTS-Summe, Durchschnitt)
        und weist die View an, ihre Darstellung ebenfalls zu erneuern.
        """
        self.ects = Service.berechne_ects(self.kurse)
        self.durchschnitt = Service.berechne_durchschnitt(self.kurse)
        self.view.update_student_info(self.student, self.ects, self.durchschnitt)


if __name__ == "__main__":
    # Falls die Datei direkt ausgeführt wird, starten wir den Controller
    c = Controller()
    c.start()
