import requests
import json
api_key = "hsk_3fdbf10eda9e7404c00d45dc378a8137416c07ad6b5f00c30740a087105c72e2"
endpoint = f"https://highspec.gg/api/v1/external/job/captcha/submit?api_key={api_key}&priority=false&service=directapi"

#payload
# json_data = {
#     "accounts": [
#         {
#             "username": "highspecgg",
#             "cookie": "_|WARNING:-DO-NOT-SHARE-THIS.|XXXXXXXXXXXXXXXXXX"
#         },
#         {
#             "username": "highspecgg2", 
#             "cookie": "_|WARNING:-DO-NOT-SHARE-THIS.|XXXXXXXXXXXXXXXXXX"
#         }
#     ]
# }
def LoadSaved(): ## คืน dict ฟอร์แมต {"accounts":[{"username":..,"cookie":..}]} คืน accounts ว่างถ้าไฟล์ไม่มี/พัง
    alt = {
        "accounts": []
    }
    try:
        with open("Data/account.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            accounts = data["AccountData"]   # AccountData เป็น list ของ account
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return alt
    # วนทีละ account แล้วแปลงเป็นฟอร์แมตที่ highspec ต้องการ
    for acc in accounts:
        alt["accounts"].append({
            "username": acc["name"],
            "cookie": acc["Cookies"]
        })
    return alt
Accountinram2 = LoadSaved()
json_data = Accountinram2



r = requests.post(endpoint, json=json_data)
print(r.status_code)
print(r.json())