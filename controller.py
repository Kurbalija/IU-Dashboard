from model import StudentRepository, KursRepository
from service import Service

class Controller:
    def __init__(self):
        self.student = StudentRepository.lade_student("CSV/student.csv")
        self.kurse = KursRepository.lade_kurse("CSV/kurse.csv")
        self.ects = Service.berechne_ects(self.kurse)
        self.durchschnitt = Service.berechne_durchschnitt(self.kurse)
        from view import View
        self.view = View(self, self.student, self.kurse, self.ects, self.durchschnitt)

    def start(self):
        self.view.mainloop()

    def aktualisiere_note(self, kurscode, raw_input):
        ok = Service.setze_note(self.kurse, kurscode, raw_input)
        if ok:
            KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
            self._update_stats()
        return ok

    def aktualisiere_kursname(self, kurscode, neuer_name):
        for k in self.kurse:
            if k.kurscode == kurscode:
                k.name = neuer_name
                KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
                self._update_stats()
                return True
        return False

    def aktualisiere_kurscode(self, alter_kurscode, neuer_kurscode):
        for k in self.kurse:
            if k.kurscode == alter_kurscode:
                k.kurscode = neuer_kurscode
                KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)
                self._update_stats()
                return True
        return False

    def aktualisiere_kurs_ects(self, kurscode, neuer_ects):
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
        self.student.name = name
        self.student.studiengang = studiengang
        self.student.ziel_ects = ziel_ects
        StudentRepository.speichere_student("CSV/student.csv", self.student)
        self._update_stats()

    def _update_stats(self):
        self.ects = Service.berechne_ects(self.kurse)
        self.durchschnitt = Service.berechne_durchschnitt(self.kurse)
        self.view.update_student_info(self.student, self.ects, self.durchschnitt)

if __name__ == "__main__":
    c = Controller()
    c.start()
