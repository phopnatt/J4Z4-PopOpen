import sys, os, shlex, subprocess
# เพิ่ม root โปรเจกต์เข้า path เพื่อให้ import Core.* ได้แม้กด Run จากไฟล์นี้ตรงๆ
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from Core.Filehandler import accountloader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_FILE = os.path.join(ROOT, "Core", "accountcontrolCLI.py")
CLI_URL = "http://127.0.0.1:8000"   # ต้องตรงกับ HOST:PORT ใน accountcontrolCLI.py


class AccountControl:
    """คุมบัญชีที่กำลังรันอยู่ (running instances)
    switch Auto Relaunch = เปิด/ปิดหน้าต่าง CLI (accountcontrolCLI) ที่คอยรับ heartbeat
    """
    def __init__(self):
        self.auto_relaunch = False
        # เก็บสถานะ account ที่กำลังคุมอยู่ {name: {...}} ไว้ต่อ logic จริงทีหลัง
        self.running = {}

    def load_accounts(self):
        # คืนเฉพาะ account ที่ Logged==True (บัญชีที่กำลังคุมอยู่)
        return [acc for acc in accountloader("").LoadSaved() if acc.get("Logged")]

    def login(self, Name:str):
        # mark เป็น Logged=True แล้วบันทึกลงไฟล์ คืน True ถ้าเจอ
        if not Name:
            return False
        return accountloader("").SetLogged(Name, True)

    # ---------- Auto Relaunch CLI ----------
    def cli_is_running(self):
        # เช็คว่ามีหน้าต่าง CLI เปิดรออยู่แล้วไหม (ยิง /ping ไปถาม)
        try:
            return requests.get(CLI_URL + "/ping", timeout=1).status_code == 200
        except requests.RequestException:
            return False

    def start_cli(self):
        # เด้งหน้าต่าง terminal ขึ้นมารัน accountcontrolCLI (ถ้ายังไม่ได้เปิด)
        if self.cli_is_running():
            return
        if sys.platform == "darwin":
            # macOS: สั่งให้ Terminal.app เปิดหน้าต่างใหม่แล้วรัน CLI
            cmd = f"cd {shlex.quote(ROOT)} && {shlex.quote(sys.executable)} {shlex.quote(CLI_FILE)}"
            script = cmd.replace("\\", "\\\\").replace('"', '\\"')
            subprocess.Popen([
                "osascript",
                "-e", f'tell application "Terminal" to do script "{script}"',
                "-e", 'tell application "Terminal" to activate',
            ])
        elif os.name == "nt":
            # Windows: เปิด console window ใหม่
            subprocess.Popen([sys.executable, CLI_FILE], cwd=ROOT,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # linux/อื่นๆ: รันเป็น process เงียบๆ ไปก่อน
            subprocess.Popen([sys.executable, CLI_FILE], cwd=ROOT)

    def stop_cli(self):
        # สั่งให้ CLI ปิดตัวเอง (ถ้าเปิดอยู่)
        try:
            requests.post(CLI_URL + "/shutdown", timeout=1)
        except requests.RequestException:
            pass

    def set_auto_relaunch(self, enabled):
        # เปิด/ปิด auto relaunch -> เปิด/ปิดหน้าต่าง CLI ตามไปด้วย
        self.auto_relaunch = bool(enabled)
        if self.auto_relaunch:
            self.start_cli()
        else:
            self.stop_cli()
        return self.auto_relaunch

    def remove_selected(self, Name:str):
        # เอาออกจากการคุม -> Logged=False แล้วบันทึกลงไฟล์ คืน True ถ้าเจอ
        if not Name:
            return False
        return accountloader("").SetLogged(Name, False)
