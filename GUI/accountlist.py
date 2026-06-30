import sys, os
# เพิ่ม root โปรเจกต์เข้า path เพื่อให้ import GUI.* / Core.* ได้แม้กด Run จากไฟล์นี้ตรงๆ
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import customtkinter as ctk
from Core.Filehandler import *

def load():
        # placeholder — ยังไม่ผูก logic จริง ใส่ข้อมูลตัวอย่างไว้ดู UI ก่อน
    bro=accountloader("kuy")
    return bro.LoadSaved()


class scrollingframe:
    def __init__(self, parent):
        self.scroll_frame = ctk.CTkScrollableFrame(parent, width=350, height=250)
        self.scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.selected = {"item": None, "account": None}
        self.account_rows = []  # เก็บ label ทุกแถว ไว้ล้างตอน refresh
        self.refresh_accounts()

    def get_selected_name(self):
        # คืนชื่อไอดีที่เลือกอยู่ คืน None ถ้ายังไม่ได้เลือก
        if self.selected["account"] is None:
            return None
        return self.selected["account"]["name"]

    def selectedevent(self, label, account):
        # คืนสีเดิมให้อันที่เลือกไว้ก่อนหน้า
        if self.selected["item"] is not None:
            self.selected["item"].configure(fg_color="transparent")
        # อันใหม่เป็นสีฟ้า
        label.configure(fg_color="#3b8ed0")
        self.selected["item"] = label
        self.selected["account"] = account

    def refresh_accounts(self):
        # ล้างแถวเก่าออกก่อน
        for w in self.account_rows:
            w.destroy()
        self.account_rows.clear()
        self.selected["item"] = None
        self.selected["account"] = None

        accounts = load()
        if not accounts:
            lbl = ctk.CTkLabel(self.scroll_frame, text="ยังไม่มี account — กด Add account", anchor="w")
            lbl.pack(fill="x", pady=2, padx=4)
            self.account_rows.append(lbl)
            return

        # โหลด account จากไฟล์มาแสดงทีละแถว
        for acc in accounts:
            lbl = ctk.CTkLabel(self.scroll_frame, text=acc["name"], fg_color="transparent",
                               corner_radius=6, anchor="w")
            lbl.pack(fill="x", pady=2, padx=4)
            lbl.bind("<Button-1>", lambda e, l=lbl, a=acc: self.selectedevent(l, a))
            self.account_rows.append(lbl)


