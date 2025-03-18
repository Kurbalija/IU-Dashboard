class Service:
    @staticmethod
    def berechne_ects(kurse):
        # 0 wird berücksichtigt, da angerechnete Fächer gezählt werden
        return sum(kurs.ects for kurs in kurse if kurs.note is not None)

    @staticmethod
    def berechne_durchschnitt(kurse):
        # 0 wird ignoriert, da es ein angerechnetes Fach ist
        summe_gewichtete_noten = sum(
            kurs.note * kurs.ects for kurs in kurse if kurs.note is not None and kurs.note != 0
        )
        summe_ects = sum(
            kurs.ects for kurs in kurse if kurs.note is not None and kurs.note != 0
        )
        return round(summe_gewichtete_noten / summe_ects, 2) if summe_ects > 0 else None
    
    @staticmethod
    def setze_note(kurse, kurscode, neue_note):
        for kurs in kurse:
            if kurs.kurscode == kurscode:
                if neue_note == "A":
                    kurs.note = 0  # A wird intern als 0 gespeichert
                    return True
                try:
                    neue_note = float(neue_note)
                    if 1 <= neue_note <= 5:
                        kurs.note = neue_note
                        return True
                    else:
                        return False
                except ValueError:
                    return False
        return False