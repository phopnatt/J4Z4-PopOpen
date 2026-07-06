import sys, os
# เพิ่ม root โปรเจกต์เข้า path เพื่อให้ import GUI.* / Core.* ได้แม้กด Run จากไฟล์นี้ตรงๆ
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from GUI.accountlist import scrollingframe          # reuse list เดิม ไม่ก็อปซ้ำ
from Core.accountcontrolmodule import AccountControl


class accountcontrol:
    """หน้าต่าง Account Control — คุมบัญชีที่รันอยู่
    switch Auto Relaunch จะเด้งหน้าต่าง CLI (accountcontrolCLI) ขึ้นมารอรับ heartbeat
    ถ้า account ไหนเงียบนานเกิน timeout CLI จะสั่ง rejoin ให้เอง
    """
    def __init__(self, parent=None):
        # มี parent -> เปิดเป็น popup ลอยเหนือหน้าหลัก, ไม่มี -> เปิดเดี่ยวๆ (ไว้เทส)
        self.controller = ctk.CTkToplevel(parent) if parent is not None else ctk.CTk()
        self.controller.geometry("500x450")
        self.controller.title("Account Control")
        if parent is not None:
            self.controller.transient(parent)

        self.ctrl = AccountControl()                 # logic คุมบัญชีที่รันอยู่
        # แสดงเฉพาะบัญชีที่ Logged==True เท่านั้น
        self.accountlist = scrollingframe(self.controller, only_logged=True)
        self.Toolbar()
        # ถ้ามี CLI เปิดค้างอยู่จากรอบก่อน ให้ switch ติด on ตามความเป็นจริง
        if self.ctrl.cli_is_running():
            self.auto_switch.select()

    def Toolbar(self):
        bar = ctk.CTkFrame(self.controller)
        bar.pack(side="bottom", pady=10, padx=10, fill="x")

        # switch เปิด/ปิด auto relaunch
        self.auto_switch = ctk.CTkSwitch(bar, text="Auto Relaunch",
                                         command=self.on_toggle_auto)
        self.auto_switch.pack(side="left", padx=15)

        ctk.CTkButton(bar, text="Remove Selected", fg_color="gray40",
                      hover_color="gray30",
                      command=self.on_remove).pack(side="left", padx=8)

    def on_toggle_auto(self):
        self.ctrl.set_auto_relaunch(self.auto_switch.get())

    def on_remove(self):
        name = self.accountlist.get_selected_name()
        if name is None:
            return  # ยังไม่ได้เลือก account
        self.ctrl.remove_selected(name)       # Logged=False + บันทึกไฟล์
        self.accountlist.refresh_accounts()   # โหลด list ใหม่ (บัญชีจะหายจากหน้านี้)


if __name__ == "__main__":
    # เทสหน้าต่าง Account Control แบบเดี่ยวๆ
    win = accountcontrol()
    win.controller.mainloop()
