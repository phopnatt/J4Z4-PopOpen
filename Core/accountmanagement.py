import os
import json
import requests
import time
import random
import urllib.parse
import subprocess
from Filehandler import *




class RobloxJoiner:
    def __init__(self,Name:str):
        self.Name==
    def findcookieforacc(self,Name:str):
        Loader=accountloader()
        data=Loader.LoadSaved()
        for i in data :
            if data["AccountData"]["name"]==Name:
                return data["AccountData"]["Cookies"]
            else:
                return None
            
    def joinbyname(self,Name : str,Place : int,Job:str):
        COOKIE = self.findcookieforacc(Name)
        PLACE_ID = Place
        JOB_ID = Job
        if (COOKIE or PLACE_ID)==None:
            print("Cookie or place ID expect nil")
            return 
        
        session = requests.Session()
        session.cookies.set(".ROBLOSECURITY", COOKIE, domain=".roblox.com", path="/")
        r = session.post(
            "https://auth.roblox.com/v1/authentication-ticket/",
            headers={"Referer": "https://www.roblox.com/", "Content-Type": "application/json"},
            json={},
        )
        csrf = r.headers.get("x-csrf-token")
        if not csrf:
            print("[FAIL] ขอ CSRF Token ไม่ได้")
            exit()

        print(f"[OK] CSRF Token: {csrf[:20]}...")

        r = session.post(
            "https://auth.roblox.com/v1/authentication-ticket/",
            headers={
                "X-CSRF-TOKEN": csrf,
                "Referer": "https://www.roblox.com/",
                "Content-Type": "application/json",
            },
            json={},
        )
        ticket = r.headers.get("rbx-authentication-ticket")
        if not ticket:
            print(f"[FAIL] ขอ Auth Ticket ไม่ได้ (status {r.status_code})")
            exit()

        print(f"[OK] Auth Ticket: {ticket[:40]}...")

        if not JOB_ID:
            r = session.get(
                f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/public",
                params={"sortOrder": "Asc", "limit": 100},
            )
            if r.status_code == 200:
                servers = r.json().get("data", [])
                valid = [
                    s["id"]
                    for s in servers
                    if s["playing"] > 0 and s["playing"] < s["maxPlayers"]
                ]
                if valid:
                    JOB_ID = random.choice(valid)
                    print(f"[OK] สุ่มได้ server: {JOB_ID[:20]}...")
                else:
                    print("[INFO] ไม่เจอ server ว่าง → จะเข้าแบบสุ่มอัตโนมัติ")

        launch_time = int(time.time() * 1000)
        browser_tracker = str(random.randint(100000, 175000)) + str(random.randint(100000, 900000))

        if JOB_ID:
            launcher_url = (
                f"https://assetgame.roblox.com/game/PlaceLauncher.ashx"
                f"?request=RequestGameJob"
                f"&browserTrackerId={browser_tracker}"
                f"&placeId={PLACE_ID}"
                f"&gameId={JOB_ID}"
                f"&isPlayTogetherGame=false"
            )
        else:
            launcher_url = (
                f"https://assetgame.roblox.com/game/PlaceLauncher.ashx"
                f"?request=RequestGame"
                f"&browserTrackerId={browser_tracker}"
                f"&placeId={PLACE_ID}"
                f"&isPlayTogetherGame=false"
            )

        uri = (
            f"roblox-player:1"
            f"+launchmode:play"
            f"+gameinfo:{ticket}"
            f"+launchtime:{launch_time}"
            f"+placelauncherurl:{urllib.parse.quote(launcher_url)}"
            f"+browsertrackerid:{browser_tracker}"
            f"+robloxLocale:en_us"
            f"+gameLocale:en_us"
            f"+channel:"
            f"+LaunchExp:InApp"
        )

        subprocess.Popen(["open", uri])
        print(f"[OK] กำลังเปิด Roblox เข้า Place {PLACE_ID}...")
                