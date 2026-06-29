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
                return data["AccountData"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return []

    def Addaccount(self): ## เพิ่ม account จาก self.token Return True ถ้าสำเร็จ ไม่ผ่านคืน False
        name = Robloxtools(self.token).Checkauthentoken()
        if name == None :
            return False
        accounts = self.LoadSaved()
        for acc in accounts :
            if acc["name"] == name :
                acc["Cookies"] = self.token  ## มีอยู่แล้วอัปเดต cookie
                break
        else :
            accounts.append({"name": name, "Cookies": self.token})
        with open("Data/account.json","w",encoding="utf-8") as f:
            json.dump({"AccountData": accounts}, f, ensure_ascii=False, indent=2)
        return True

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
