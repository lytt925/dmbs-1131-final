import requests
from config import API_BASE_URL

def query_applications():
    print("Query Adoption Applications")
    print("You can provide user_id, animal_id, both or none.")
    user_id_input = input("Enter user_id (or leave blank): ")
    animal_id_input = input("Enter animal_id (or leave blank): ")

    params = {}
    if user_id_input.strip():
        params["user_id"] = user_id_input.strip()
    if animal_id_input.strip():
        params["animal_id"] = animal_id_input.strip()

    # 呼叫後端 API 取得申請紀錄
    response = requests.get(f"{API_BASE_URL}/applications", params=params)

    if response.status_code == 200:
        apps = response.json()
        if not apps:
            print("No applications found.")
            return
        print("Applications Found:")
        for app in apps:
            # 假設 application 表包含以下欄位: application_id, user_id, animal_id, status, update_at
            # 可視實際欄位情況做顯示調整
            print(f"Application ID: {app['application_id']}")
            print(f"User ID: {app['user_id']}")
            print(f"Animal ID: {app['animal_id']}")
            print(f"Status: {app['status']}")
            print(f"Update At: {app['update_at']}\n")
    else:
        error_detail = response.json().get('detail', 'Error fetching applications')
        print(error_detail)

def update_application_status():
    application_id = input("Enter the application_id you want to update: ")
    status = input("Enter the new status (e.g., 'S' for success, 'F' for fail, 'P' for pending): ")
    response = requests.put(f"{API_BASE_URL}/applications/{application_id}/status", params={"status": status})
    if response.status_code == 200:
        updated_app = response.json()
        print("Application status updated successfully!")
        print(updated_app)
    else:
        error_detail = response.json().get('detail', 'Error updating application status')
        print(error_detail)
