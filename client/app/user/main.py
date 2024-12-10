import requests
from config import API_BASE_URL
from user.apply import apply
from user.register import register
from user.account import account

def main(email):
    user = requests.get(f"{API_BASE_URL}/users", params={"email": email}).json()
    print(f"\n{user['name']}您好，歡迎使用動物收容所平台！")
    user_id = user['user_id']
    while True:
        print("\n選單:")
        print("1. 我的帳號🙍")
        print("2. 參加活動☀️")
        print("3. 認養申請✎")
        print("4. 登出")
        operation = input("請輸入選項編號: ")
        match(operation):
            case "1":
                account(user_id)
            case "2":
                register(user_id)
            case "3":
                apply(user_id)
            case "4":
                return
            case _:
                print("Invalid choice. Please try again.")