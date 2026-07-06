import requests
import json

class Robloxtools:
    def __init__(self, token: str):
        self.token = token
    def Checkauthentoken(self): ## Return name(str) if sucess if not return none
        session = requests.Session()
        session.cookies.set(".ROBLOSECURITY", self.token , domain=".roblox.com", path="/")
        try:
            r = session.get("https://www.roblox.com/my/account/json")
        except:
            print("Authenication Error")
            return None
        if r.status_code == 200:
            user = r.json()
            return user['Name']
        else:
            print(f"Unexpected error occur")
            return None
    def Formatsaved(self):
        if self.Checkauthentoken()!=None :
            formatsave=self.Checkauthentoken()+ ":" + self.token
            print(formatsave)
            return formatsave

    def Nameoutput(self):
        if self.Checkauthentoken()!=None :
            print(self.Checkauthentoken())
            return self.Checkauthentoken()
    def Outputtoken(self):
            if self.Checkauthentoken()!=None :
                return self.token

class accountloader :
    def __init__(self, token: str):
        self.token = token
    def LoadSaved(self): ## Return list of account(list) คืน list ว่างถ้าไฟล์ไม่มี/พัง
        try:
            with open("Data/account.json","r",encoding="utf-8") as f:
                data = json.load(f)
                accounts = data["AccountData"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return []
        for acc in accounts:          ## เติม default ให้ record เก่าที่ยังไม่มีฟิลด์ Logged
            acc.setdefault("Logged", False)
        return accounts

    def Addaccount(self): ## เพิ่ม account จาก self.token Return True ถ้าสำเร็จ ไม่ผ่านคืน False
        name = Robloxtools(self.token).Checkauthentoken()
        if name == None :
            return False
        accounts = self.LoadSaved()
        for acc in accounts :
            if acc["name"] == name :
                acc["Cookies"] = self.token  ## มีอยู่แล้วอัปเดต cookie
                acc.setdefault("Logged", False)  ## กัน record เก่าที่ยังไม่มีฟิลด์นี้
                break
        else :
            accounts.append({"name": name, "Cookies": self.token,"Logged":False})
        with open("Data/account.json","w",encoding="utf-8") as f:
            json.dump({"AccountData": accounts}, f, ensure_ascii=False, indent=2)
        return True

    def SetLogged(self, name: str, state: bool): ## อัปเดตสถานะ Logged ของ account คืน True ถ้าเจอ
        accounts = self.LoadSaved()
        for acc in accounts :
            if acc["name"] == name :
                acc["Logged"] = bool(state)
                with open("Data/account.json","w",encoding="utf-8") as f:
                    json.dump({"AccountData": accounts}, f, ensure_ascii=False, indent=2)
                return True
        return False

    def SetLastPlace(self, name: str, place): ## จำ place ล่าสุดที่กด Launch ไว้ให้ auto relaunch ใช้ คืน True ถ้าเจอ
        accounts = self.LoadSaved()
        for acc in accounts :
            if acc["name"] == name :
                acc["LastPlace"] = str(place)
                with open("Data/account.json","w",encoding="utf-8") as f:
                    json.dump({"AccountData": accounts}, f, ensure_ascii=False, indent=2)
                return True
        return False

    def Remove(self, name: str): ## ลบ account ตามชื่อ Return True ถ้าลบเจอ
        accounts = self.LoadSaved()
        newaccounts = [acc for acc in accounts if acc["name"] != name]
        if len(newaccounts) == len(accounts) :
            return False
        with open("Data/account.json","w",encoding="utf-8") as f:
            json.dump({"AccountData": newaccounts}, f, ensure_ascii=False, indent=2)
        return True


if __name__ == "__main__":
    cookie = "ํUR Cookies"
    bot = Robloxtools(cookie)
    bot.Checkauthentoken()
    bot.Formatsaved()
