import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from GUI.accountlist import *
from GUI.accounteditor import *
from Core.accountmanagement import RobloxJoiner
class maingui:
    def __init__(self):
        self.windows = ctk.CTk()
        self.windows.geometry("800x400")
        self.windows.title("J4Z4 PoP Open")
        self.RemoveAddhandlerbutton()
        self.PlaceIDundJobIDHandler()
        self.accountlist = scrollingframe(self.windows)
    def run(self):
        self.windows.mainloop()
    def onclickadd(self):
        Cookiehandler(self.windows, on_added=self.accountlist.refresh_accounts)
    def onclickremove(self):
        name = self.accountlist.get_selected_name()
        if name is None:
            return  # ยังไม่ได้เลือก account
        accountloader("kuy").Remove(name)
        self.accountlist.refresh_accounts()  # โหลด list ใหม่หลังลบ
    def joinevent(self):
        name = self.accountlist.get_selected_name()
        if name is None:
            print("ยังไม่ได้เลือก account")
            return
        place = self.place_entry.get().strip()
        job = self.job_entry.get().strip()
        if not place:
            print("ยังไม่ได้ใส่ Place ID")
            return
        RobloxJoiner(name).joinbyname(name, place, job)
    def RemoveAddhandlerbutton(self):
        removeadd = ctk.CTkFrame(self.windows)
        removeadd.pack(side="bottom", pady=10)
        ctk.CTkButton(removeadd, text="Remove account",command=self.onclickremove).pack(side="left", padx=30)
        ctk.CTkButton(removeadd, text="Add account",command=self.onclickadd).pack(side="left", padx=30)
    def PlaceIDundJobIDHandler(self):
        btnfr = ctk.CTkFrame(self.windows)
        btnfr.pack(pady=20, padx=10, fill="x")
        Lable = ctk.CTkLabel(btnfr, text="Place ID: ")
        Lable.pack(side="left", padx=(30, 2))
        self.place_entry = ctk.CTkEntry(btnfr, width=200)
        self.place_entry.pack(side="left", padx=(0, 30))
        Lablee = ctk.CTkLabel(btnfr, text="Job ID: ")
        Lablee.pack(side="left", padx=(30, 2))
        self.job_entry = ctk.CTkEntry(btnfr, width=200)
        self.job_entry.pack(side="left", padx=(0, 30))
        ctk.CTkButton(btnfr, text="Launch",command=self.joinevent).pack(side="right", padx=30)


