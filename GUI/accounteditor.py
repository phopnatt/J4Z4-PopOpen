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

class Cookiehandler:
    def __init__(self, parent=None, on_added=None):
        # popup เปิดเหนือหน้าต่างหลัก (parent) ถ้าไม่ส่งมาก็เปิดเดี่ยวๆ ได้
        # on_added: callback ที่จะเรียกหลัง add สำเร็จ (เช่น refresh list)
        self.on_added = on_added
        self.windows = ctk.CTkToplevel(parent)
        self.windows.geometry("400x200")
        self.windows.title("Cookie Handler")
        self.windows.resizable(False, False)

        # ทำให้เป็น popup จริง: ลอยเหนือ parent + โฟกัสที่หน้าต่างนี้
        if parent is not None:
            self.windows.transient(parent)
        self.windows.grab_set()
        self.windows.focus()

        ctk.CTkLabel(self.windows, text="Enter your .ROBLOSECURITY cookie:").pack(pady=(20, 10))

        self.cookie_entry = ctk.CTkEntry(self.windows, width=300,
                                         placeholder_text=".ROBLOSECURITY ...")
        self.cookie_entry.pack(pady=5)
        self.cookie_entry.focus()

        btnbar = ctk.CTkFrame(self.windows, fg_color="transparent")
        btnbar.pack(pady=15)
        ctk.CTkButton(btnbar, text="Add",command=self.onadd).pack(side="left", padx=6)
        ctk.CTkButton(btnbar, text="Cancel", fg_color="gray40", hover_color="gray30",
                      command=self.windows.destroy).pack(side="left", padx=6)
    def onadd(self):
        cookie = self.cookie_entry.get()
        bot = Robloxtools(cookie)
        if bot.Checkauthentoken()==None:
            warning(self.windows)
        else:
            account=accountloader(cookie)
            account.Addaccount()
            if self.on_added is not None:
                self.on_added()      # refresh list หลัง add สำเร็จ
            self.windows.destroy()   # ปิด popup

if __name__ == "__main__":
    # รันทดสอบ: หน้าต่างหลักมีปุ่ม -> กดแล้ว popup Cookie Handler เด้งขึ้น
    root = ctk.CTk()
    root.geometry("400x200")
    root.title("Demo")
    ctk.CTkButton(root, text="Add cookie",command=lambda: Cookiehandler(root)).pack(expand=True)
    root.mainloop()
    
