class Service:
    @staticmethod
    def berechne_ects(kurse):
        return sum(k.ects for k in kurse if k.note is not None)

    @staticmethod
    def berechne_durchschnitt(kurse):
        valid = [k for k in kurse if k.note is not None and k.note != 0.0]
        if not valid:
            return None
        s = sum(k.note * k.ects for k in valid)
        e = sum(k.ects for k in valid)
        return round(s / e, 2)

    @staticmethod
    def setze_note(kurse, kurscode, raw_input):
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