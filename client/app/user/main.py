import requests
from config import API_BASE_URL
from user.apply import apply
from user.register import register

def main(email):
    print("\nWelcome to the Animal Shelter System!\n")
    user_id = requests.get(f"{API_BASE_URL}/users", params={"email": email}).json()['user_id']
    while True:
        print("選單:")
        print("1. 我的帳號🙍")
        print("2. 參加活動☀️")
        print("3. 認養申請✎")
        print("4. 登出")
        operation = input("Enter your choice: ")
        match(operation):
            case "1":
                print("My Accounts:")
            case "2":
                register(user_id)
            case "3":
                apply(user_id)
            case "4":
                return
            case _:
                print("Invalid choice. Please try again.")