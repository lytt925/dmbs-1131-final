import requests
from config import API_BASE_URL

def query_care_records():
    print("查詢照顧紀錄")
    
    # 直接要求輸入 animal_id
    animal_id_input = input("請輸入要查詢的動物 ID: ").strip()

    try:
        # 直接使用路由中的 animal_id 參數
        response = requests.get(f"{API_BASE_URL}/carerecords/{animal_id_input}")

        if response.status_code == 200:
            care_records = response.json()
            
            if not care_records:
                print("找不到任何照顧紀錄。")
                return
            
            print("找到的照顧紀錄：")
            for record in care_records:
                print(f"動物 ID: {record.get('animal_id')}")
                print(f"員工 ID: {record.get('employee_id')}")
                print(f"照顧類型: {record.get('care_type')}")
                print(f"開始時間: {record.get('start_at')}\n")
        else:
            error_detail = response.json().get('detail', '查詢照顧紀錄時發生錯誤')
            print(error_detail)
    except Exception as e:
        print(f"發生錯誤：{e}")




def create_care_record(employee_id):
    print("新增照顧紀錄")
    
    # 輸入動物 ID
    animal_id = input("請輸入動物 ID: ")

    # 照顧類型選擇
    print("照顧類型：")
    print("C: 清潔 (Cleaning)")
    print("F: 餵食 (Feeding)")
    print("W: 遛狗/遛貓 (Walking)")
    
    care_type = input("請選擇照顧類型 (C/F/W): ").upper()
    
    # 驗證照顧類型
    while care_type not in ['C', 'F', 'W']:
        print("無效的照顧類型，請重新輸入。")
        care_type = input("請選擇照顧類型 (C/F/W): ").upper()

    # 呼叫 API 新增照顧紀錄
    try:
        response = requests.post(f"{API_BASE_URL}/carerecords/", 
                                 params={
                                     "animal_id": animal_id, 
                                     "employee_id": employee_id, 
                                     "care_type": care_type
                                 })

        if response.status_code == 200:
            print("照顧紀錄新增成功！")
        else:
            error_detail = response.json().get('detail', '新增照顧紀錄時發生錯誤')
            print(error_detail)
    except Exception as e:
        print(f"發生錯誤：{e}")