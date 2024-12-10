import requests
from datetime import datetime
from config import API_BASE_URL

type_name = {'C': '認養培訓課程', 'V': '愛心志工活動'}

def register(user_id: str): 
    print("\n選擇您想查詢的收容所: ")
    response = requests.get(f"{API_BASE_URL}/shelters")
    shelters = response.json()['data']
    for i, shelter in enumerate(shelters):
        print(f"{i + 1}. {shelter['name']}")
    print("\n")
    shelter_id = int(input("請輸入選項編號: "))
    shelter_id = shelters[shelter_id - 1]['shelter_id'] 
    try:
        response = requests.get(f"{API_BASE_URL}/activities", params={"shelter_id": shelter_id})
        activities = response.json()
        print("\n本收容所的最新活動:")
        for i, activity in enumerate(activities):
            # 使用 strptime 將字串轉換為 datetime 物件
            date_time_obj = datetime.strptime(activity['time'], "%Y-%m-%dT%H:%M:%S")

            # 格式化日期和時間
            date = date_time_obj.strftime("%B %d, %Y")  # 日期：如 December 10, 2024
            time = date_time_obj.strftime("%I:%M %p")    # 時間：如 10:00 AM
            print(f"{i + 1}. [{type_name[activity['activity_type']]}] {date}\n")
            print(f" | 地點: {activity['location']}\n | 時間: {time}\n | 人數上限: {activity['capacity']}\n | 剩餘名額: {activity['remain_tickets']}\n")
    
        done = False
        while(not done):
            activity_id = int(input("請輸入欲報名的活動編號: "))
            print("報名中...")
            activity_id = activities[activity_id - 1]['activity_id']
            try:
                response = requests.post(f"{API_BASE_URL}/registrations", json={"user_id": user_id, "activity_id": activity_id})
                done = True
            except:
                print("\n❌ 此場次已額滿。\n")
        print("\n❤️ 報名成功！請至<我的帳號>查看報名資訊。\n")
    except:
        print("\n❌ 此收容所目前無活動。\n")
