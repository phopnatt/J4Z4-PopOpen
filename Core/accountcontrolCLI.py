import sys, os, time, json, threading
from collections import deque
from contextlib import asynccontextmanager

# เพิ่ม root โปรเจกต์เข้า path + ยืนที่ root เสมอ (Filehandler เปิด "Data/account.json" แบบ relative)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from fastapi import FastAPI, Request
import uvicorn
from Core.Filehandler import accountloader
from Core.accountmanagement import RobloxJoiner

# ================== ตั้งค่า ==================
HOST = "127.0.0.1"   # ฟังแค่ในเครื่องพอ อย่าเปิด 0.0.0.0 (คนอื่นในวง LAN จะยิงเข้าได้)
PORT = 8000          # ต้องตรงกับ Url ใน ConfigJ4Z$.lua
BEAT_TIMEOUT = 20    # เงียบเกินกี่วิ = ถือว่าตาย (ฝั่ง Lua ยิงทุก 5 วิ)
CHECK_EVERY = 5      # watchdog ตรวจทุกกี่วิ
LAUNCH_GRACE = 90    # หลังสั่ง relaunch ให้เวลา Roblox เปิด+inject กี่วิ ก่อนเริ่มจับผิดใหม่
# =============================================

last_seen = {}          # {name: เวลา beat ล่าสุด}
last_place = {}         # {name: place ล่าสุดที่รู้จาก beat}
grace_until = {}        # {name: ห้ามตัดสินว่าตายก่อนเวลานี้ (ช่วงรอเกมเปิด)}
relaunches = {}         # {name: สั่ง relaunch ไปแล้วกี่ครั้ง}
noplace_warned = set()  # กันเตือน "ไม่รู้ place" ซ้ำทุกรอบ
events = deque(maxlen=10)  # log ล่าสุดไว้โชว์ใต้ตาราง


def log(msg):
    events.append(f"[{time.strftime('%H:%M:%S')}] {msg}")


@asynccontextmanager
async def lifespan(app):
    # server เปิดสำเร็จแล้วค่อยปล่อย watchdog เริ่มจับเวลา
    threading.Thread(target=watchdog, daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    # ให้ GUI เช็คว่ามี CLI เปิดรออยู่แล้วหรือยัง
    return {"ok": True}


@app.post("/beat")
async def beat(request: Request):
    # รับ heartbeat จาก executor
    # รองรับ 2 แบบ: JSON {"name":..,"place":..,"job":..} หรือส่งชื่อมาเปล่าๆ แบบเก่า
    raw = (await request.body()).decode("utf-8", errors="ignore").strip()
    name, place = raw, None
    try:
        data = json.loads(raw)
        name = str(data.get("name") or "").strip()
        place = data.get("place")
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass  # ไม่ใช่ JSON -> ถือว่า body ทั้งก้อนคือชื่อ account
    if not name:
        return {"ok": False}

    now = time.time()
    prev = last_seen.get(name)
    last_seen[name] = now
    if place:
        last_place[name] = str(place)
    if prev is None:
        log(f"beat แรกจาก {name}" + (f" (place {place})" if place else ""))
    elif now - prev > BEAT_TIMEOUT:
        log(f"{name} กลับมา online")
    return {"ok": True}


@app.post("/shutdown")
def shutdown():
    # ให้ GUI สั่งปิดตอนสับ switch Auto Relaunch เป็น off
    threading.Timer(0.3, lambda: os._exit(0)).start()
    return {"ok": True}


def relaunch(name, place):
    # สั่ง rejoin ด้วย place ล่าสุดที่รู้ (ไม่ล็อค job เดิม เพราะ server เก่าอาจเต็ม/ปิดไปแล้ว)
    n = relaunches.get(name, 0) + 1
    relaunches[name] = n
    log(f"{name} เงียบเกิน {BEAT_TIMEOUT}s -> สั่ง relaunch ครั้งที่ {n} (place {place})")
    try:
        RobloxJoiner(name).joinbyname(name, str(place), "")
    except Exception as e:
        log(f"relaunch {name} พัง: {e}")
    grace_until[name] = time.time() + LAUNCH_GRACE


def watchdog():
    while True:
        now = time.time()
        rows = []
        # อ่านไฟล์ใหม่ทุกรอบ เผื่อ user กด Login/Remove เพิ่มระหว่างรัน
        for acc in accountloader("").LoadSaved():
            if not acc.get("Logged"):
                continue
            name = acc["name"]
            # place ที่จะใช้ relaunch: จาก beat ล่าสุด > จาก LastPlace ที่จำไว้ตอนกด Launch
            place = last_place.get(name) or acc.get("LastPlace")
            seen = last_seen.get(name)

            # เพิ่งเจอ account นี้ครั้งแรกและยังไม่มี beat -> ให้เวลาพิสูจน์ตัว 1 ช่วงก่อน
            if seen is None and name not in grace_until:
                grace_until[name] = now + BEAT_TIMEOUT

            if seen is not None and now - seen <= BEAT_TIMEOUT:
                status = "ONLINE"   # มี beat สดๆ = รอดแน่นอน ไม่ต้องสน grace
            elif now < grace_until.get(name, 0):
                status = "LAUNCHING" if relaunches.get(name) else "WAITING"
            elif not place:
                # ตายแต่ไม่รู้จะส่งกลับเข้า place ไหน
                status = "NO PLACE"
                if name not in noplace_warned:
                    noplace_warned.add(name)
                    log(f"{name} เงียบแต่ไม่รู้ Place ID -> กด Launch จาก GUI สัก 1 ครั้งก่อน")
            else:
                relaunch(name, place)
                status = "LAUNCHING"

            rows.append((name, status, seen, place))
        draw(rows, now)
        time.sleep(CHECK_EVERY)


def draw(rows, now):
    # หน้าจอสถานะวาดใหม่ทุกรอบ (ข้ามการ clear ถ้า output ไม่ใช่จอจริง เช่นตอนเทส)
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")
    print("=" * 64)
    print(f"  J4Z4 Auto Relaunch  |  รอ heartbeat ที่ http://{HOST}:{PORT}/beat")
    print(f"  เงียบเกิน {BEAT_TIMEOUT}s = สั่ง relaunch อัตโนมัติ (เช็คทุก {CHECK_EVERY}s)")
    print("=" * 64)
    if not rows:
        print("  ยังไม่มี account ที่ Logged=true — กด Login ในหน้าหลักก่อน")
    else:
        print(f"  {'ACCOUNT':<22}{'STATUS':<12}{'LAST BEAT':<12}{'PLACE':<13}{'RELAUNCH'}")
        for name, status, seen, place in rows:
            ago = "-" if seen is None else f"{int(now - seen)}s ago"
            print(f"  {name:<22}{status:<12}{ago:<12}{str(place or '?'):<13}{relaunches.get(name, 0)}")
    print("-" * 64)
    for e in events:
        print(" ", e)
    sys.stdout.flush()


if __name__ == "__main__":
    try:
        uvicorn.run(app, host=HOST, port=PORT, log_level="warning", access_log=False)
    except (Exception, SystemExit) as e:
        # ส่วนใหญ่คือ port ถูกใช้อยู่ (มี CLI ตัวเก่าเปิดค้าง) — ค้างหน้าต่างไว้ให้อ่าน error
        print(f"\n[!] เปิด server ไม่ได้: {e}")
        print(f"    เช็คว่ามีหน้าต่าง Auto Relaunch เก่าเปิดค้างอยู่หรือเปล่า (port {PORT})")
        input("กด Enter เพื่อปิด...")
