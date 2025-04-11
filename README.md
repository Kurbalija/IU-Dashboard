# IU Progress Tracker

Dieses Python-Projekt bietet ein **grafisches Dashboard**, das den Studienfortschritt eines Studierenden verwaltet und visualisiert. Noten, ECTS und allgemeine Studierendendaten werden in CSV-Dateien gespeichert und können über die GUI (tkinter) angezeigt und bearbeitet werden.

---

## Projektüberblick

- **Ziel**: Einen übersichtlichen und leicht bedienbaren Überblick über den eigenen Studienstand zu ermöglichen.  
- **Features**:  
  - Anzeigen aller Kurse mit Noten, ECTS und Kurscode  
  - Bearbeiten der Noten (Doppelklick in der Tabelle)  
  - Aktualisieren von Kurstiteln, ECTS und Kurscodes  
  - Verwalten der Studierendendaten (Name, Studiengang, Ziel-ECTS)  
  - Automatische Berechnung von ECTS-Summe, Notendurchschnitt und Fortschrittsanzeige in Prozent

---

## Installation & Voraussetzungen

1. **Python-Version**  
   Empfohlen ist **Python 3.13** oder höher.  

2. **Clonen oder Entpacken**  
   - Lade das gesamte Projekt herunter oder klone das Repository.  
   - Stelle sicher, dass sich die CSV-Dateien (z. B. `student.csv`, `kurse.csv`) in einem Unterordner namens `CSV` befinden.

3. **Optionale Abhängigkeiten**  
   - Das Projekt nutzt **tkinter** (in Python standardmäßig enthalten).  
   - Keine weiteren Bibliotheken erforderlich (außer Standardbibliotheken wie `csv` und `platform`).

---

## Projektstruktur

```
.
├── controller.py      # Steuert Datenfluss und UI-Aktionen
├── model.py           # Enthält Student/Kurs Klassen sowie Repositories
├── service.py         # Berechnung von ECTS, Notendurchschnitt, Note-Validierung
├── view.py            # tkinter-GUI (Dark Theme)
└── CSV
    ├── student.csv    # Musterdaten für Student
    └── kurse.csv      # Musterdaten für Kurse
```

- **model.py**  
  Enthält die Datenklassen `Student`, `Kurs` sowie die Klassen `StudentRepository` und `KursRepository` für das Lesen und Speichern der CSV-Dateien.  
- **service.py**  
  Bietet zentrale Methoden für ECTS-Berechnungen, Notendurchschnitt und Validierung von Noteneingaben.  
- **controller.py**  
  Verbindet Model, Service und View. Lädt Daten aus CSV, initialisiert die View und reagiert auf Nutzeraktionen (z. B. Notenänderungen).  
- **view.py**  
  Erzeugt eine tkinter-Oberfläche, zeigt Kurse an (in einer `Treeview`) und aktualisiert den Fortschrittsbalken.

---

## Ausführung

1. **Sicherstellen**, dass du dich im Projektverzeichnis befindest:  
   ```bash
   cd /pfad/zum/projekt
   ```

2. **Starten**  
   ```bash
   python controller.py
   ```
   - Ein randloses Fenster öffnet sich. Oberhalb befindet sich eine Titelzeile mit Schließen-Button (außer auf macOS).  
   - Im linken Bereich siehst du die Studierenden-Infos und erreichbare ECTS. Rechts daneben wird der prozentuale Fortschritt in einem Kreisdiagramm angezeigt.  
   - Unten listet eine Tabelle alle Kurse auf. Per Doppelklick kannst du Noten ändern oder Kursinformationen anpassen.

---

## Benutzung

- **Noten ändern**  
  - Doppelklicke in der Tabellenansicht auf den jeweiligen Kurs. Ein Popup-Fenster erscheint, in dem du Kurscode, Name, ECTS und Note bearbeiten kannst.  
  - Erlaubte Notenwerte sind: Zahlen 1–5, `'A'` (angerechnet, intern 0.0) oder `'-'` (keine Note).  

- **Ändern der Studierendendaten**  
  - Klicke auf das Zahnrad-Symbol im Statistikbereich (oben links). Ein kleines Fenster erscheint, in dem du Name, Studiengang und Ziel-ECTS anpassen kannst.

- **Fortschrittsanzeige**  
  - Das Kreisdiagramm zeigt, welcher Anteil der Ziel-ECTS bereits erreicht wurde (inkl. angerechneter Kurse).  
  - Der Notendurchschnitt berücksichtigt nur Kurse, die eine „echte“ Note (1–5) haben.

---

## Datenhaltung & Erweiterung

- Alle **Daten** liegen in einfachen **CSV-Dateien**:  
  - `student.csv` enthält Name, Studiengang und Ziel-ECTS.  
  - `kurse.csv` enthält Zeilen mit `Kurscode, Kursname, ECTS, Note`.  
- Du kannst die Dateien problemlos anpassen oder neue Kurse hinzufügen. Beim nächsten Programmstart werden sie eingelesen.  

**Viel Spaß mit dem IU Progress Tracker!**