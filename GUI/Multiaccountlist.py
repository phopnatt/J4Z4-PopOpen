import sys, os
# เพิ่ม root โปรเจกต์เข้า path เพื่อให้ import Core ได้แม้กด Run จากไฟล์นี้ตรงๆ
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from Core.Filehandler import *

class warning:##warning when wrong cookies
    def __init__(self, parent=None):
        self.windows = ctk.CTkToplevel(parent)
        self.windows.geometry("200x200")
        self.windows.title("Warning")
        label = ctk.CTkLabel(self.windows, text="Authenication error", anchor="center")
        self.windows.resizable(False, False)
        label.pack(fill="x")

class Multicookiehandler:
    def __init__(self, parent=None, on_added=None):
        # popup เปิดเหนือหน้าต่างหลัก (parent) ถ้าไม่ส่งมาก็เปิดเดี่ยวๆ ได้
        # on_added: callback ที่จะเรียกหลัง add สำเร็จ (เช่น refresh list)
        self.on_added = on_added
        self.windows = ctk.CTkToplevel(parent)
        self.windows.geometry("400x500")
        self.windows.title("Cookie Handler")
        self.windows.resizable(False, False)

        # ทำให้เป็น popup จริง: ลอยเหนือ parent + โฟกัสที่หน้าต่างนี้
        if parent is not None:
            self.windows.transient(parent)
        self.windows.grab_set()
        self.windows.focus()

        ctk.CTkLabel(self.windows, text="Enter your .ROBLOSECURITY cookie (บรรทัดละ 1 อัน):").pack(pady=(20, 10))

        # ช่องกรอก cookie แบบหลายบรรทัด เก็บไว้ที่ self เพื่อให้ onaddmulti อ่านได้
        self.text_area = ctk.CTkTextbox(self.windows, wrap="word", font=("Consolas", 12))
        self.text_area.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        btnbar = ctk.CTkFrame(self.windows, fg_color="transparent")
        btnbar.pack(pady=15)
        ctk.CTkButton(btnbar, text="Add", command=self.onaddmulti).pack(side="left", padx=6)
        ctk.CTkButton(btnbar, text="Cancel", fg_color="gray40", hover_color="gray30",
                      command=self.windows.destroy).pack(side="left", padx=6)

    def onaddmulti(self):
        content = self.text_area.get("1.0", ctk.END)
        added = 0                          # นับว่าเพิ่มสำเร็จกี่อัน
        for line in content.splitlines():
            line = line.strip()
            if not line:                   # ข้ามบรรทัดว่าง
                continue
            bot = Robloxtools(line)
            if bot.Checkauthentoken() is None:
                warning(self.windows)      # cookie ใช้ไม่ได้ เด้งเตือน
            else:
                accountloader(line).Addaccount()
                added += 1

        if added > 0:
            if self.on_added is not None:
                self.on_added()            # refresh list หลัง add สำเร็จ
            self.windows.destroy()         # ปิด popup เมื่อเพิ่มได้อย่างน้อย 1 อัน

if __name__ == "__main__":
    # รันทดสอบ: หน้าต่างหลักมีปุ่ม -> กดแล้ว popup Cookie Handler เด้งขึ้น
    root = ctk.CTk()
    root.geometry("400x200")
    root.title("Demo")
    ctk.CTkButton(root, text="Add cookie",command=lambda: Multicookiehandler(root)).pack(expand=True)
    root.mainloop()
    
