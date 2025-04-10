import tkinter as tk
from tkinter import ttk, Canvas
import platform

class View(tk.Tk):
    def __init__(self, controller, student, kurse, ects, durchschnitt):
        super().__init__()
        self.controller = controller
        self.student = student
        self.kurse = kurse
        self.ects = ects
        self.durchschnitt = durchschnitt
        self.overrideredirect(True)
        self.geometry("900x600")
        self.configure(bg="#2C2F33")
        self.background_color = "#2C2F33"
        self.border_color = "#36393F"
        self.foreground_color = "#DCDDDE"
        self.accent_color = "#7289DA"
        self.hover_close_color = "#E57373"
        self.name_var = tk.StringVar(value=self.student.name)
        self.studiengang_var = tk.StringVar(value=self.student.studiengang)
        self.ziel_ects_var = tk.StringVar(value=str(self.student.ziel_ects))
        self.ects_var = tk.StringVar(value=str(self.ects))
        self.durchschnitt_var = tk.StringVar(value=str(self.durchschnitt or "-"))
        self.item_kurs_map = {}
        self._init_style()
        self._build_titlebar()
        self._build_main()

    def _init_style(self):
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
        style.map("Borderless.Treeview", background=[("selected", self.accent_color)], foreground=[("selected", "#FFFFFF")])
        style.configure(
            "Borderless.Treeview.Heading",
            background=self.border_color,
            foreground=self.foreground_color,
            font=("Consolas", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        style.map("Borderless.Treeview.Heading", background=[])

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=self.border_color, height=40)
        bar.pack(side="top", fill="x")
        bar.bind("<ButtonPress-1>", self._start_move)
        bar.bind("<ButtonRelease-1>", self._stop_move)
        bar.bind("<B1-Motion>", self._on_move)
        tk.Label(
            bar,
            text="🎓 IU Progress Tracker",
            font=("Consolas", 16, "bold"),
            fg=self.accent_color,
            bg=self.border_color
        ).pack(side="left", padx=10)
        if platform.system() != "Darwin":
            close_btn = tk.Button(
                bar,
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
            close_btn.pack(side="right", padx=(0, 10))
            close_btn.bind("<Enter>", lambda e: close_btn.config(bg=self.hover_close_color))
            close_btn.bind("<Leave>", lambda e: close_btn.config(bg=self.border_color))

    def _build_main(self):
        main_frame = tk.Frame(self, bg=self.background_color)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=3)
        stats_frame = tk.Frame(main_frame, bg=self.border_color)
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        stats_card = tk.Frame(stats_frame, bg=self.border_color)
        stats_card.pack(expand=True, fill="both")
        stats_card.grid_columnconfigure(2, weight=1)
        self._add_stat_label(stats_card, "Name", self.name_var, 0)
        self._add_stat_label(stats_card, "Studiengang", self.studiengang_var, 1)
        self._add_stat_label(stats_card, "Ziel-ECTS", self.ziel_ects_var, 2)
        self._add_stat_label(stats_card, "Erreichte ECTS", self.ects_var, 3)
        self._add_stat_label(stats_card, "Notendurchschnitt", self.durchschnitt_var, 4)
        gear_btn = tk.Label(
            stats_card,
            text="⚙",
            font=("Consolas", 14),
            bg=self.border_color,
            fg=self.foreground_color,
            width=2,
            height=1,
            borderwidth=0,
            cursor="hand2"
        )
        gear_btn.grid(row=0, column=3, sticky="ne", padx=(20, 10))
        gear_btn.bind("<Button-1>", lambda e: self.open_student_popup())
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
        self._draw_circle(self.circle_frame, self.ects, self.student.ziel_ects, 130, 20)
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
        self.tree.column("Kurscode", width=100, anchor="center")
        self.tree.column("Kursname", width=400, anchor="w")
        self.tree.column("ECTS", width=40, anchor="center")
        self.tree.column("Note", width=40, anchor="center")
        for k in self.kurse:
            note_txt = "A" if k.note == 0.0 else (f"{k.note:.2f}" if k.note is not None else "-")
            iid = self.tree.insert("", "end", values=(k.kurscode, k.name, k.ects, note_txt))
            self.item_kurs_map[iid] = k
        self.tree.bind("<Double-1>", self._on_tree_double_click)
        self.tree.bind("<Motion>", self._on_hover_motion)

    def _on_tree_double_click(self, event):
        row = self.tree.identify_row(event.y)
        if not row:
            return
        kurs = self.item_kurs_map.get(row)
        if not kurs:
            return
        self.open_course_edit_popup(kurs)

    def _on_hover_motion(self, event):
        row = self.tree.identify_row(event.y)
        region = self.tree.identify("region", event.x, event.y)
        for iid in self.tree.get_children():
            self.tree.item(iid, tags=())
        if region == "cell" and row:
            self.tree.item(row, tags=("hover",))
            self.tree.tag_configure("hover", background="#44474C")

    def open_course_edit_popup(self, kurs):
        top = tk.Toplevel(self)
        top.overrideredirect(True)
        top.resizable(False, False)
        w, h = 800, 250
        x = self.winfo_x() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.config(bg=self.background_color)
        outer = tk.Frame(top, bg=self.background_color)
        outer.pack(fill="both", expand=True)
        card = tk.Frame(outer, bg=self.border_color)
        card.pack(padx=20, pady=20, fill="both", expand=True)
        code_var = tk.StringVar(value=kurs.kurscode)
        name_var = tk.StringVar(value=kurs.name)
        ects_var = tk.StringVar(value=str(kurs.ects))
        note_txt = "-" if kurs.note is None else ("A" if kurs.note == 0.0 else f"{kurs.note:.2f}")
        note_var = tk.StringVar(value=note_txt)
        def add_field(lbl, var, row_index, width=30):
            tk.Label(
                card,
                text=lbl,
                font=("Consolas", 12),
                bg=self.border_color,
                fg=self.foreground_color
            ).grid(row=row_index, column=0, sticky="e", padx=5, pady=5)
            tk.Entry(
                card,
                textvariable=var,
                font=("Consolas", 12),
                bg="#2C2F33",
                fg="#FFFFFF",
                insertbackground="#FFFFFF",
                bd=0,
                highlightthickness=0,
                relief="flat",
                width=width
            ).grid(row=row_index, column=1, sticky="w", padx=5, pady=5)
        add_field("Kurscode:", code_var, 0, 20)
        add_field("Kursname:", name_var, 1, 50)
        add_field("ECTS:", ects_var, 2, 5)
        add_field("Note (1-5, 'A', '-'):", note_var, 3, 10)
        row_btns = tk.Frame(card, bg=self.border_color)
        row_btns.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        save_btn = tk.Label(
            row_btns,
            text="Speichern",
            width=10,
            bg=self.accent_color,
            fg="#FFFFFF",
            font=("Consolas", 12, "bold"),
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=5)
        save_btn.bind("<Button-1>", lambda _: self._save_course_changes(
            kurs, code_var.get(), name_var.get(), ects_var.get(), note_var.get(), top
        ))
        cancel_btn = tk.Label(
            row_btns,
            text="Abbrechen",
            width=10,
            bg=self.border_color,
            fg=self.foreground_color,
            font=("Consolas", 12),
            cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=5)
        cancel_btn.bind("<Button-1>", lambda _: top.destroy())

    def _save_course_changes(self, kurs, new_code, new_name, new_ects, new_note, dialog):
        old_code = kurs.kurscode
        if new_code != old_code:
            ok_code = self.controller.aktualisiere_kurscode(old_code, new_code)
            if not ok_code:
                return
        if new_name.strip() != kurs.name:
            self.controller.aktualisiere_kursname(new_code, new_name.strip())
        if str(kurs.ects) != new_ects.strip():
            ok_ects = self.controller.aktualisiere_kurs_ects(new_code, new_ects.strip())
            if not ok_ects:
                return
        if not self.controller.aktualisiere_note(new_code, new_note):
            return
        dialog.destroy()

    def open_student_popup(self):
        top = tk.Toplevel(self)
        top.overrideredirect(True)
        top.resizable(False, False)
        w, h = 350, 200
        x = self.winfo_x() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        outer = tk.Frame(top, bg=self.background_color)
        outer.pack(fill="both", expand=True)
        card = tk.Frame(outer, bg=self.border_color)
        card.pack(padx=20, pady=20, fill="both", expand=True)
        entries = {
            "Name": tk.StringVar(value=self.student.name),
            "Studiengang": tk.StringVar(value=self.student.studiengang),
            "Ziel-ECTS": tk.StringVar(value=str(self.student.ziel_ects))
        }
        row_idx = 0
        for lbl, var in entries.items():
            tk.Label(
                card,
                text=lbl,
                font=("Consolas", 12),
                bg=self.border_color,
                fg=self.foreground_color
            ).grid(row=row_idx, column=0, sticky="e", padx=5, pady=5)
            tk.Entry(
                card,
                textvariable=var,
                font=("Consolas", 12),
                bg="#2C2F33",
                fg="#FFFFFF",
                insertbackground="#FFFFFF",
                bd=0,
                highlightthickness=0,
                relief="flat",
                width=20
            ).grid(row=row_idx, column=1, sticky="w", padx=5, pady=5)
            row_idx += 1
        row_btns = tk.Frame(card, bg=self.border_color)
        row_btns.grid(row=row_idx, column=0, columnspan=2, pady=(20, 0))
        save_btn = tk.Label(
            row_btns,
            text="Speichern",
            width=10,
            bg=self.accent_color,
            fg="#FFFFFF",
            font=("Consolas", 12, "bold"),
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=5)
        save_btn.bind("<Button-1>", lambda _: self._save_student_data(entries, top))
        cancel_btn = tk.Label(
            row_btns,
            text="Abbrechen",
            width=10,
            bg=self.border_color,
            fg=self.foreground_color,
            font=("Consolas", 12),
            cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=5)
        cancel_btn.bind("<Button-1>", lambda _: top.destroy())

    def _save_student_data(self, entries, dialog):
        name_val = entries["Name"].get().strip()
        stud_val = entries["Studiengang"].get().strip()
        try:
            ziel = int(entries["Ziel-ECTS"].get().strip())
        except ValueError:
            return
        self.controller.aktualisiere_student(name_val, stud_val, ziel)
        dialog.destroy()

    def update_student_info(self, student, ects, durchschnitt):
        self.student = student
        self.ects = ects
        self.durchschnitt = durchschnitt
        self.name_var.set(student.name)
        self.studiengang_var.set(student.studiengang)
        self.ziel_ects_var.set(str(student.ziel_ects))
        self.ects_var.set(str(ects))
        self.durchschnitt_var.set(str(durchschnitt or "-"))
        for c in self.circle_frame.winfo_children():
            c.destroy()
        self._draw_circle(self.circle_frame, ects, student.ziel_ects, 130, 20)
        for iid, k in self.item_kurs_map.items():
            self.tree.set(iid, "Kurscode", k.kurscode)
            self.tree.set(iid, "Kursname", k.name)
            self.tree.set(iid, "ECTS", k.ects)
            disp_note = "-" if k.note is None else ("A" if k.note == 0.0 else f"{k.note:.2f}")
            self.tree.set(iid, "Note", disp_note)


    def _add_stat_label(self, parent, title, val, row):
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
                fg=self.accent_color
            ).grid(row=row, column=1, sticky="w", padx=(0, 10), pady=3)
        else:
            tk.Label(
                parent,
                text=str(val),
                font=("Consolas", 12),
                bg="#36393F",
                fg=self.accent_color
            ).grid(row=row, column=1, sticky="w", padx=(0, 10), pady=3)

    def _draw_circle(self, parent, reached, goal, size, bottom_pad):
        c = Canvas(parent, width=size, height=size, bg=self.border_color, highlightthickness=0)
        c.pack(pady=(0, bottom_pad))
        pct = (reached / goal * 100) if goal > 0 else 0
        angle = (pct / 100) * 360
        pad = 10
        c.create_oval(pad, pad, size - pad, size - pad, outline=self.background_color, width=8)
        c.create_arc(pad, pad, size - pad, size - pad, start=-90, extent=-angle, outline=self.accent_color, width=8, style="arc")
        c.create_text(
            size / 2, size / 2,
            text=f"{pct:.0f}%",
            fill=self.foreground_color,
            font=("Consolas", 14, "bold")
        )

    def _start_move(self, e):
        self._x = e.x
        self._y = e.y

    def _stop_move(self, e):
        self._x = None
        self._y = None

    def _on_move(self, e):
        x = self.winfo_x() + (e.x - (self._x or 0))
        y = self.winfo_y() + (self._y or 0)
        y = self.winfo_y() + (e.y - (self._y or 0))
        self.geometry(f"+{x}+{y}")
