import requests
from datetime import datetime
from config import API_BASE_URL

sex = {'M': '男', 'F': '女'}
type_name = {'C': '認養培訓課程', 'V': '愛心志工活動'}

def account(user_id: str):
    user_input = ''
    while user_input != '4':
        print ("\n1. 會員資訊\n2. 我的活動\n3. 我的認養申請\n 4. 上一頁")
        choice = input("請輸入欲查看的選項: ")

        match(choice):
            case "1":
                response = requests.get(f"{API_BASE_URL}/users", params={"user_id": user_id})
                user = response.json()
                print(f"\n | 姓名: {user['name']}\n 性別: {sex[user['sex']]} | 電子郵件: {user['email']}\n | 電話: {user['phone']}\n")
            case "2":
                try:
                    response = requests.get(f"{API_BASE_URL}/registrations", params={"user_id": user_id})
                    activities = response.json()['data']
                    print("\n已報名的活動:\n")
                    for i, activity in enumerate(activities):
                        date_time_obj = datetime.strptime(activity['time'], "%Y-%m-%dT%H:%M:%S")

                        date = date_time_obj.strftime("%B %d, %Y")  # 日期：如 December 10, 2024
                        time = date_time_obj.strftime("%I:%M %p")    # 時間：如 10:00 AM
                        print(f"[{type_name[activity['activity_type']]}] {date}\n")
                        print(f" | 地點: {activity['location']}\n | 時間: {time}\n")
                except:
                    print("\n您尚未報名任何活動。\n")
            case "3":
                try:
                    response = requests.get(f"{API_BASE_URL}/applications", params={"user_id": user_id})
                    applications = response.json()
                    print("\n認養申請:\n")
                    for i, application in enumerate(applications):
                        print(f"{i + 1}. {application['status']}\n")
                        print(f" | 動物: {application['animal_name']}\n | 收容所: {application['shelter_name']}\n")
                except:
                    print("\n您尚未提交認養申請。\n")
