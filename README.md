# IU Progress Tracker

Dieses Python-Projekt bietet ein kleines Dashboard (GUI), um den Studienfortschritt eines Studenten **übersichtlich** zu verwalten. 

- **Model** (Student, Kurs + CSV-Repositories)  
- **Service** (Berechnungen für ECTS, Notendurchschnitt und Notenvalidierung)  
- **Controller** (Steuert alle Datenflüsse und aktualisiert die View)  
- **View** (tkinter-Oberfläche mit dunklem Design)

## Features

- **Module/Kurse ansehen** (Kurscode, Name, ECTS, Note)  
- **Noten bearbeiten** (Doppelklick auf Kurseintrag)  
- **Studentendaten ändern** (Name, Studiengang, Ziel-ECTS)  
- **Statistiken** zu ECTS, Notendurchschnitt und prozentualem Fortschritt (Kreisdiagramm)  
- **CSV-Dateien bereits enthalten** (keine separate Erstellung nötig)

## Installation & Start

1. **Python 3.13** (oder höher) installieren  
2. **Projekt** entpacken oder klonen (die `CSV`-Dateien liegen bereits im Ordner `CSV`)  
3. **Starten**  
   ```bash
   python controller.py
   ```
   - Auf Windows/Linux erscheint ein randloses Fenster mit Minimieren-/Schließen-Buttons  
   - Auf macOS ist das Fenster ebenfalls randlos; zum Verschieben in der Titelzeile anklicken und ziehen

## Bedienung

- **Noten ändern**  
  - Doppelklick in der Tabelle → Eingabe-Fenster (1–5, „A“ für angerechnete Note, „-“ für keine Note)  
- **Studentendaten anpassen**  
  - Klick auf Zahnrad-Symbol → Popup für Name, Studiengang, Ziel-ECTS  
- **Fortschritt**  
  - Kreisdiagramm zeigt den anteiligen Fortschritt basierend auf allen Modulen, die eine Note (inkl. „A“) haben  
- **Wahlfächer**  
  - Die `kurse.csv` enthält bereits mehrere Einträge, darunter auch Wahlfächer

## Ordnerstruktur

```
.
├── controller.py
├── model.py
├── service.py
├── view.py
└── CSV
    ├── student.csv
    └── kurse.csv
```

- **model.py**: Datenklassen (`Student`, `Kurs`) und CSV-Lade-/Speicherfunktionen (`StudentRepository`, `KursRepository`)  
- **service.py**: Berechnung von ECTS, Notendurchschnitt, Validierung von Noten  
- **controller.py**: Lädt Daten, erzeugt GUI, verarbeitet Änderungen (z. B. Noten, Studentendaten)  
- **view.py**: tkinter-GUI (dunkles Design), Tabellenansicht, Kreisdiagramm