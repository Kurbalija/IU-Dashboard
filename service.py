class Service:
    """
    Bündelt zentrale Berechnungs- und Validierungsfunktionen,
    die unabhängig von GUI oder Repositories sind.
    """

    @staticmethod
    def berechne_ects(kurse):
        """
        Summiert alle ECTS der Kurse, bei denen eine Note vorhanden ist.
        Angerechnete Kurse (Note == 0.0) zählen auch als 'vorhandene' Note.

        :param kurse: Liste von Kurs-Objekten
        :return: Gesamtanzahl erreichter ECTS (int)
        """
        return sum(k.ects for k in kurse if k.note is not None)

    @staticmethod
    def berechne_durchschnitt(kurse):
        """
        Berechnet den gewichteten Notendurchschnitt (Note * ECTS),
        ignoriert Kurse ohne Note (None) oder angerechnete (== 0.0).

        :param kurse: Liste von Kurs-Objekten
        :return: Rundeter Durchschnittswert (float) oder None, wenn keine validen Noten
        """
        valid = [k for k in kurse if k.note is not None and k.note != 0.0]
        if not valid:
            return None
        s = sum(k.note * k.ects for k in valid)
        e = sum(k.ects for k in valid)
        return round(s / e, 2)

    @staticmethod
    def setze_note(kurse, kurscode, raw_input):
        """
        Sucht anhand eines Kurscodes das passende Kurs-Objekt
        und interpretiert die Benutzereingabe als Note.

        Eingabe-Optionen:
          - Leer oder '-' => Note wird entfernt (None)
          - 'A' => angerechnet (Note = 0.0)
          - Zahlenwert [1..5] => gültige Note
          - Anderes => False

        :param kurse: Liste von Kurs-Objekten
        :param kurscode: Identifizierender Code des Kurses
        :param raw_input: String vom Benutzer (z. B. "2.3", "A", "-")
        :return: True bei Erfolg, False sonst
        """
        for k in kurse:
            if k.kurscode == kurscode:
                txt = raw_input.strip().upper()

                if not txt or txt == "-":
                    k.note = None
                    return True

                if txt == "A":
                    k.note = 0.0
                    return True

                try:
                    val = float(txt)
                    if 1 <= val <= 5:
                        k.note = round(val, 2)
                        return True
                    return False
                except ValueError:
                    return False

        return False
