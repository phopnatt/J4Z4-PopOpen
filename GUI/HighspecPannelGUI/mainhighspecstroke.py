import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SettingsPopup(ctk.CTkToplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.on_save = on_save

        self.title("Launch Settings")
        self.geometry("400x340")
        self.resizable(False, False)

        # ทำให้เป็น popup จริง เหมือน Multiaccountlist: ลอยเหนือ parent + โฟกัสหน้าต่างนี้
        if parent is not None:
            self.transient(parent)
        self.grab_set()  # modal
        self.focus()

        self._build_ui()

    def _build_ui(self):
        PAD = 20

        # ── Falcon ──────────────────────────────────────────
        row_falcon = ctk.CTkFrame(self, fg_color="transparent")
        row_falcon.pack(fill="x", padx=PAD, pady=(PAD, 4))

        ctk.CTkLabel(row_falcon, text="Falcon", width=58, anchor="e",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        self.falcon_entry = ctk.CTkEntry(row_falcon, placeholder_text="Enter falcon ID…",
                                         height=28, font=ctk.CTkFont(size=13))
        self.falcon_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        _divider(self)

        # ── FACC (สวิตช์ On/Off) ─────────────────────────────
        self.facc_var = self._toggle_row("FACC", default=True)

        # ── Cap (สวิตช์ On/Off) ──────────────────────────────
        self.cap_var = self._toggle_row("Cap", default=False)

        _divider(self)

        # ── Rec (สวิตช์ On/Off) ──────────────────────────────
        self.rec_var = self._toggle_row("Rec", default=False)

        _divider(self)

        # ── Delay ────────────────────────────────────────────
        row_delay = ctk.CTkFrame(self, fg_color="transparent")
        row_delay.pack(fill="x", padx=PAD, pady=4)

        ctk.CTkLabel(row_delay, text="Delay", width=58, anchor="e",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        self.delay_entry = ctk.CTkEntry(row_delay, width=70, height=28,
                                         font=ctk.CTkFont(size=13), justify="center")
        self.delay_entry.insert(0, "4")
        self.delay_entry.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(row_delay, text="seconds", font=ctk.CTkFont(size=12),
                     text_color="gray").pack(side="left", padx=(6, 0))

        # ── Footer buttons ────────────────────────────────────
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=PAD, pady=(12, PAD), side="bottom")

        ctk.CTkButton(footer, text="Cancel", width=90, height=28,
                      fg_color="#e5e5e5", text_color="#333", hover_color="#d0d0d0",
                      font=ctk.CTkFont(size=13), command=self.destroy).pack(side="right", padx=(6, 0))
        ctk.CTkButton(footer, text="Save", width=90, height=28,
                      font=ctk.CTkFont(size=13), command=self._save).pack(side="right")

    def _toggle_row(self, name, default=False):
        # สร้างแถวสวิตช์ On/Off 1 แถว แล้วคืน BooleanVar ไว้ให้ _save อ่านค่า
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(row, text=name, width=58, anchor="e",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")

        var = ctk.BooleanVar(value=default)
        label = ctk.CTkLabel(row, font=ctk.CTkFont(size=12))

        def refresh():
            if var.get():
                label.configure(text="On", text_color="#1a7a34")
            else:
                label.configure(text="Off", text_color="gray")

        ctk.CTkSwitch(row, text="", variable=var,
                      width=44, command=refresh).pack(side="left", padx=(10, 0))
        label.pack(side="left", padx=(6, 0))
        refresh()  # ตั้งข้อความเริ่มต้นให้ตรงกับค่า default
        return var

    def _save(self):
        result = {
            "falcon": self.falcon_entry.get(),
            "facc":   self.facc_var.get(),
            "cap":    self.cap_var.get(),
            "rec":    self.rec_var.get(),
            "delay":  self.delay_entry.get(),
        }
        if self.on_save:
            self.on_save(result)
        self.destroy()


def _divider(parent):
    ctk.CTkFrame(parent, height=1, fg_color="#d0d0d0").pack(fill="x", padx=20, pady=4)


# ── quick preview (ลบออกตอนรวมกับโปรเจกต์หลักได้เลย) ──────────────────────
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("J4Z4MAC Manager")
    root.geometry("520x400")

    def open_settings():
        def on_save(data):
            print("Saved:", data)
        SettingsPopup(root, on_save=on_save)

    ctk.CTkButton(root, text="⚙ Settings", command=open_settings).pack(pady=20)
    root.mainloop()