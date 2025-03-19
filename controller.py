from model import KursRepository, StudentRepository
from service import Service
from view import View

class Controller:
    @staticmethod
    def start():
        student = StudentRepository.lade_student('CSV\student.csv')
        kurse = KursRepository.lade_kurse('CSV\kurse.csv')

        ects = Service.berechne_ects(kurse)
        durchschnitt = Service.berechne_durchschnitt(kurse)

        # GUI starten
        app = View(student, kurse, ects, durchschnitt)
        app.mainloop()

if __name__ == "__main__":
    Controller.start()
