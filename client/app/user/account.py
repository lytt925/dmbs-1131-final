import requests
from datetime import datetime
from config import API_BASE_URL

gender = {'M': '男', 'F': '女'}
sex = {'M': '公', 'F': '母'}
type_name = {'C': '認養培訓課程', 'V': '愛心志工活動'}

def account(user_id: str):
    user_input = ''
    while user_input != '4':
        print ("\n1. 會員資訊\n2. 我的活動\n3. 我的認養申請\n4. 上一頁")
        user_input = input("請輸入欲查看的選項: ")

        match(user_input):
            case "1":
                response = requests.get(f"{API_BASE_URL}/users", params={"user_id": user_id})
                user = response.json()
                print(f"\n{user['name']}\n | 性別: {gender[user['gender']]} | 電子郵件: {user['email']}\n | 電話: {user['phone']}\n")
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
                        print(application['update_at'])
                        date_time_obj = datetime.strptime(application['update_at'], "%Y-%m-%dT%H:%M:%S.%f")
                        print(date_time_obj)
                        date = date_time_obj.strftime("%B %d, %Y")  # 日期：如 December 10, 2024
                        print(date)
                        print(f"{application['name']} ({date})")
                        print(f" | 品種: {application['breed']}\n | 性別: {sex[application['sex']]}\n | 體型: {application['size']}\n")
                except:
                    print("\n您尚未提交認養申請。\n")