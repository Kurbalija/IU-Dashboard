import tkinter as tk
from tkinter import ttk, Canvas
import platform

from model import KursRepository
from service import Service

class View(tk.Tk):
    def __init__(self, student, kurse, ects, durchschnitt):
        super().__init__()
        # Rahmenloses Hauptfenster
        self.overrideredirect(True)
        self.geometry("900x600")
        self.configure(bg="#2C2F33")

        # Farben / States
        self.background_color = "#2C2F33"
        self.border_color = "#36393F"
        self.foreground_color = "#DCDDDE"
        self.accent_color = "#7289DA"
        self.hover_close_color = "#E57373"
        self.hover_minimize_color = "#555555"

        # Daten
        self.student = student
        self.kurse = kurse
        self.ects = ects
        self.durchschnitt = durchschnitt
        self.item_kurs_map = {}  # Zuordnung Tree-Item -> Kurs

        # Style für Treeview
        style = ttk.Style(self)
        style.theme_use("clam")
        style.layout("Borderless.Treeview", [("Borderless.Treeview.treearea", {"sticky": "nswe"})])
        style.element_create("Borderless.Treeview.treearea", "from", "clam")
        style.configure(
            "Borderless.Treeview",
            background=self.border_color,
            foreground=self.foreground_color,
            rowheight=30,
            fieldbackground=self.border_color,
            font=("Consolas", 12),
            borderwidth=0,
            relief="flat"
        )
        style.map(
            "Borderless.Treeview",
            background=[("selected", self.accent_color)],
            foreground=[("selected", "#FFFFFF")]
        )
        style.configure(
            "Borderless.Treeview.Heading",
            background=self.border_color,
            foreground=self.foreground_color,
            font=("Consolas", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        style.map("Borderless.Treeview.Heading", background=[])

        # Titelzeile
        title_bar = tk.Frame(self, bg=self.border_color, height=40)
        title_bar.pack(side="top", fill="x")
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.on_move)

        tk.Label(
            title_bar,
            text="🎓 IU Progress Tracker",
            font=("Consolas", 16, "bold"),
            fg=self.accent_color,
            bg=self.border_color
        ).pack(side="left", padx=10)

        # Buttons nur anzeigen, wenn nicht macOS
        if platform.system() != "Darwin":
            btn_close = tk.Button(
                title_bar,
                text="X",
                font=("Consolas", 12),
                bg=self.border_color,
                fg=self.foreground_color,
                width=3,
                height=1,
                borderwidth=0,
                command=self.destroy,
                highlightthickness=0,
                activebackground=self.border_color
            )
            btn_close.pack(side="right", padx=(0, 10))
            btn_close.bind("<Enter>", lambda e: btn_close.config(bg=self.hover_close_color))
            btn_close.bind("<Leave>", lambda e: btn_close.config(bg=self.border_color))

            btn_min = tk.Button(
                title_bar,
                text="–",
                font=("Consolas", 12),
                bg=self.border_color,
                fg=self.foreground_color,
                width=3,
                height=1,
                borderwidth=0,
                command=self.iconify,
                highlightthickness=0,
                activebackground=self.border_color
            )
            btn_min.pack(side="right", padx=5)
            btn_min.bind("<Enter>", lambda e: btn_min.config(bg=self.hover_minimize_color))
            btn_min.bind("<Leave>", lambda e: btn_min.config(bg=self.border_color))

        # Hauptbereich (Grid)
        main_frame = tk.Frame(self, bg=self.background_color)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=3)

        # Statistik-Frame
        stats_frame = tk.Frame(main_frame, bg=self.border_color)
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        stats_card = tk.Frame(stats_frame, bg=self.border_color)
        stats_card.pack(expand=True)

        # Variablen für Statistik
        self.ects_var = tk.StringVar(value=str(self.ects))
        self.durchschnitt_var = tk.StringVar(value=str(durchschnitt or "-"))

        self.add_stat_label(stats_card, "Name", student.name, 0)
        self.add_stat_label(stats_card, "Studiengang", student.studiengang, 1)
        self.add_stat_label(stats_card, "Ziel-ECTS", student.ziel_ects, 2)
        self.add_stat_label(stats_card, "Erreichte ECTS", self.ects_var, 3)
        self.add_stat_label(stats_card, "Notendurchschnitt", self.durchschnitt_var, 4)

        # Progress-Frame
        prog_frame = tk.Frame(main_frame, bg=self.border_color)
        prog_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        prog_card = tk.Frame(prog_frame, bg=self.border_color)
        prog_card.pack(expand=True)

        tk.Label(
            prog_card,
            text="Fortschritt",
            font=("Consolas", 12, "bold"),
            bg=self.border_color,
            fg=self.foreground_color
        ).pack(pady=(0, 5))

        self.circle_frame = tk.Frame(prog_card, bg=self.border_color)
        self.circle_frame.pack()

        self.draw_circle(self.circle_frame, self.ects, student.ziel_ects, size=130, bottom_pad=20)

        # Tabelle (unten)
        tbl_frame = tk.Frame(main_frame, bg=self.background_color)
        tbl_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(
            tbl_frame,
            style="Borderless.Treeview",
            columns=("Kurscode", "Kursname", "ECTS", "Note"),
            show="headings",
            height=12
        )
        self.tree.pack(fill="both", expand=True)
        self.tree.heading("Kurscode", text="Kurscode")
        self.tree.heading("Kursname", text="Kursname")
        self.tree.heading("ECTS", text="ECTS")
        self.tree.heading("Note", text="Note")

        # Spaltenbreite
        self.tree.column("Kurscode", width=100, anchor="center")
        self.tree.column("Kursname", width=400, anchor="w")
        self.tree.column("ECTS", width=40, anchor="center")
        self.tree.column("Note", width=40, anchor="center")

        # Einfügen der Kurse
        for k in kurse:
            note_txt = "A" if k.note == 0 else (f"{k.note:.2f}" if k.note is not None else "-")
            iid = self.tree.insert("", "end", values=(k.kurscode, k.name, k.ects, note_txt))
            self.item_kurs_map[iid] = k

        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Motion>", self.on_hover_motion)

    # Baum-Events
    def on_tree_double_click(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.open_note_popup(row)

    def on_hover_motion(self, event):
        row = self.tree.identify_row(event.y)
        region = self.tree.identify("region", event.x, event.y)
        for iid in self.tree.get_children():
            self.tree.item(iid, tags=())
        if region == "cell" and row:
            self.tree.item(row, tags=("hover",))
            self.tree.tag_configure("hover", background="#44474C")

    # Popup: Note bearbeiten
    def open_note_popup(self, iid):
        kurs = self.item_kurs_map.get(iid)
        if not kurs:
            return
        top = tk.Toplevel(self)
        top.overrideredirect(True)
        top.resizable(False, False)
        w, h = 270, 115
        x = self.winfo_x() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

        outer = tk.Frame(top, bg=self.background_color)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer, bg=self.border_color)
        card.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(
            card,
            text="Note (1-5), 'A' oder '-'",
            font=("Consolas", 12),
            bg=self.border_color,
            fg=self.foreground_color
        ).pack(pady=(5, 3))

        note_var = tk.StringVar()
        if kurs.note == 0:
            note_var.set("A")
        elif kurs.note is None:
            note_var.set("-")
        else:
            note_var.set(f"{kurs.note:.2f}")

        self.entry_field = tk.Entry(
            card,
            textvariable=note_var,
            font=("Consolas", 12),
            bg="#2C2F33",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.entry_field.pack(pady=(0, 5))

        btn_row = tk.Frame(card, bg=self.border_color)
        btn_row.pack()

        save_btn = tk.Label(
            btn_row,
            text="Speichern",
            width=10,
            bg=self.accent_color,
            fg="#FFFFFF",
            font=("Consolas", 12, "bold"),
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=5)
        self.add_hover(save_btn, self.accent_color)
        save_btn.bind("<Button-1>", lambda _: self.save_note(kurs, note_var.get(), top))

        cancel_btn = tk.Label(
            btn_row,
            text="Abbrechen",
            width=10,
            bg=self.border_color,
            fg=self.foreground_color,
            font=("Consolas", 12),
            cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=5)
        self.add_hover(cancel_btn, self.border_color)
        cancel_btn.bind("<Button-1>", lambda _: top.destroy())

    def save_note(self, kurs, raw_input, dialog):
        txt = raw_input.strip().upper()
        if not txt or txt == "-":
            kurs.note = None
        elif txt == "A":
            kurs.note = 0
        else:
            try:
                val = float(txt)
                if 1 <= val <= 5:
                    kurs.note = round(val, 2)
                else:
                    self.highlight_invalid(self.entry_field)
                    return
            except ValueError:
                self.highlight_invalid(self.entry_field)
                return
        self.highlight_valid(self.entry_field)
        KursRepository.speichere_kurse("CSV/kurse.csv", self.kurse)

        # UI-Refresh
        row_id = None
        for iid, obj in self.item_kurs_map.items():
            if obj == kurs:
                row_id = iid
                break
        if row_id:
            disp = "-" if kurs.note is None else ("A" if kurs.note == 0 else f"{kurs.note:.2f}")
            self.tree.set(row_id, "Note", disp)

        self.refresh_stats()
        dialog.destroy()

    # Statistik + Kreis aktualisieren
    def refresh_stats(self):
        self.ects = Service.berechne_ects(self.kurse)
        self.durchschnitt = Service.berechne_durchschnitt(self.kurse)
        self.ects_var.set(str(self.ects))
        self.durchschnitt_var.set(str(self.durchschnitt or "-"))
        for c in self.circle_frame.winfo_children():
            c.destroy()
        self.draw_circle(self.circle_frame, self.ects, self.student.ziel_ects, size=130, bottom_pad=20)

    # Hilfsfunktionen
    def highlight_invalid(self, entry):
        entry.config(highlightthickness=2, highlightcolor="#FF0000")

    def highlight_valid(self, entry):
        entry.config(highlightthickness=0)

    def add_stat_label(self, parent, title, val, row):
        tk.Label(
            parent,
            text=title,
            font=("Consolas", 12, "bold"),
            bg="#36393F",
            fg="#DCDDDE"
        ).grid(row=row, column=0, sticky="w", padx=(5, 25), pady=3)

        if isinstance(val, tk.StringVar):
            tk.Label(
                parent,
                textvariable=val,
                font=("Consolas", 12),
                bg="#36393F",
                fg="#7289DA"
            ).grid(row=row, column=1, sticky="w", padx=(0, 10), pady=3)
        else:
            tk.Label(
                parent,
                text=str(val),
                font=("Consolas", 12),
                bg="#36393F",
                fg="#7289DA"
            ).grid(row=row, column=1, sticky="w", padx=(0, 10), pady=3)

    def draw_circle(self, parent, reached, goal, size=130, bottom_pad=0):
        c = Canvas(parent, width=size, height=size, bg="#36393F", highlightthickness=0)
        c.pack(pady=(0, bottom_pad))
        pct = (reached / goal * 100) if goal > 0 else 0
        angle = (pct / 100) * 360
        pad = 10
        c.create_oval(pad, pad, size - pad, size - pad, outline=self.background_color, width=8)
        c.create_arc(
            pad,
            pad,
            size - pad,
            size - pad,
            start=-90,
            extent=-angle,
            outline=self.accent_color,
            width=8,
            style="arc"
        )
        c.create_text(
            size / 2,
            size / 2,
            text=f"{pct:.0f}%",
            fill=self.foreground_color,
            font=("Consolas", 14, "bold")
        )

    def add_hover(self, lbl, normal_bg):
        def on_enter(_):
            lbl.config(bg=self.hover_minimize_color)
        def on_leave(_):
            lbl.config(bg=normal_bg)
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

    # Fenster bewegen
    def start_move(self, e):
        self._x = e.x
        self._y = e.y

    def stop_move(self, e):
        self._x = None
        self._y = None

    def on_move(self, e):
        x = self.winfo_x() + (e.x - (self._x or 0))
        y = self.winfo_y() + (e.y - (self._y or 0))
        self.geometry(f"+{x}+{y}")
