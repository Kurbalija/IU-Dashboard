class View:
    @staticmethod
    def zeige_statistik(student, ects, durchschnitt):
        breite = 80
        print("\n" + "=" * breite)
        print(f"{'STUDENTEN-ÜBERSICHT'.center(breite)}")
        print("=" * breite)
        print(f"{'Name:':<20}{student.name}")
        print(f"{'Studiengang:':<20}{student.studiengang}")
        print(f"{'Ziel-ECTS:':<20}{student.ziel_ects}")
        print(f"{'Erreichte ECTS:':<20}{ects}")
        print(f"{'Notendurchschnitt:':<20}{durchschnitt:.2f}" if durchschnitt is not None else f"{'Notendurchschnitt:':<20}-")

        # Fortschritt direkt anzeigen
        View.zeige_fortschritt(ects, student.ziel_ects)

        print("=" * breite + "\n")

    @staticmethod
    def zeige_kurse(kurse):
        breite = 80
        print("\n" + "=" * breite)
        print(f"{'KURSE'.center(breite)}")
        print("=" * breite)
        print(f"{'Kurscode':<15} {'Kursname':<50} {'ECTS':<5} {'Note'}")
        print("-" * breite)
        for kurs in kurse:
            if kurs.note == 0:
                note = "A"
            elif kurs.note is not None:
                note = f"{kurs.note:.2f}"
            else:
                note = "-"

            print(f"{kurs.kurscode:<15} {kurs.name[:50]:<50} {kurs.ects:<5} {note}")
        print("=" * breite + "\n")

    @staticmethod
    def zeige_fortschritt(erreichte_ects, ziel_ects):
        if ziel_ects == 0:
            print("Fortschritt: Keine Ziel-ECTS definiert.")
            return

        prozent = (erreichte_ects / ziel_ects) * 100
        balkenbreite = 60
        gefuellt = int(balkenbreite * (prozent / 100))
        leer = balkenbreite - gefuellt

        balken = f"[{'█' * gefuellt}{'-' * leer}]"
        print(f"\nFortschritt: {balken} {prozent:.2f}%\n")

    @staticmethod
    def zeige_nachricht(nachricht):
        print(f"\n[✔️] {nachricht}\n")

    @staticmethod
    def zeige_fehler(fehlermeldung):
        print(f"\n[❌] {fehlermeldung}\n")