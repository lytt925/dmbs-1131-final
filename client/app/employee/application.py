import requests
from config import API_BASE_URL

def query_applications():
    print("查詢領養申請")
    print("您可以提供以下條件進行查詢：")
    print("1. user_id")
    print("2. animal_id")
    print("3. shelter_id")
    print("您可以選擇提供其中一個或多個條件，若不提供則顯示所有申請。")

    user_id_input = input("請輸入 user_id (若不使用此條件請留空): ").strip()
    animal_id_input = input("請輸入 animal_id (若不使用此條件請留空): ").strip()
    shelter_id_input = input("請輸入 shelter_id (若不使用此條件請留空): ").strip()

    params = {}
    if user_id_input:
        params["user_id"] = int(user_id_input)
    if animal_id_input:
        params["animal_id"] = int(animal_id_input)
    if shelter_id_input:
        params["shelter_id"] = int(shelter_id_input)

    # 呼叫後端 API 取得申請紀錄
    response = requests.get(f"{API_BASE_URL}/applications", params=params)

    if response.status_code == 200:
        apps = response.json()
        if not apps:
            print("找不到符合條件的申請記錄。")
            return
        print("找到的申請：")
        for app in apps:
            # 假設 application 表包含以下欄位: application_id, user_id, animal_id, status, update_at, shelter_id
            # 根據需求顯示額外的 shelter_id 資訊
            print(f"申請 ID: {app['application_id']}")
            print(f"使用者 ID: {app['user_id']}")
            print(f"動物 ID: {app['animal_id']}")
            print(f"狀態: {app['status']}")
            print(f"更新時間: {app['update_at']}\n")
    else:
        error_detail = response.json().get('detail', '查詢申請時發生錯誤')
        print(f"查詢失敗，原因：{error_detail}")


def update_application_status():
    application_id = input("請輸入您要更新的申請 ID: ")
    status = input("請輸入新的狀態 (例如：'S' 代表成功, 'F' 代表失敗, 'P' 代表處理中): ")
    response = requests.put(f"{API_BASE_URL}/applications/{application_id}/status", params={"status": status})
    if response.status_code == 200:
        updated_app = response.json()
        print("申請狀態更新成功！")
        print(updated_app)
    else:
        error_detail = response.json().get('detail', '更新申請狀態時發生錯誤')
        print(error_detail)


