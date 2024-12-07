import requests
import json
from config import API_BASE_URL

API_BASE_URL += "/applications"

# 建立一個 application 的資料
def create_application():
    data = {
        "application_id": int(input("Enter application ID: ")),
        "update_at": input("Enter update time (YYYY-MM-DD HH:MM:SS): "),
        "status": input("Enter status (default is 'P'): ") or "P",
        "user_id": int(input("Enter user ID: ")),
        "animal_id": int(input("Enter animal ID: "))
    }
    response = requests.post(f"{API_BASE_URL}/", json=data)
    if response.status_code == 200:
        print("Application created successfully!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# 查詢 applications 資料
def get_applications():
    user_id = input("Enter user ID (optional): ")
    animal_id = input("Enter animal ID (optional): ")
    params = {}
    if user_id:
        params["user_id"] = user_id
    if animal_id:
        params["animal_id"] = animal_id

    response = requests.get(f"{API_BASE_URL}/", params=params)
    if response.status_code == 200:
        applications = response.json()
        print(f"Found {len(applications)} applications:")
        print(json.dumps(applications, indent=4))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# 更新 application 的狀態
def update_application_status():
    application_id = int(input("Enter application ID: "))
    status = input("Enter new status: ")
    
    response = requests.put(f"{API_BASE_URL}/{application_id}/status", params={"status": status})
    if response.status_code == 200:
        print("Status updated successfully!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# 查詢 application 統計
def get_total_application_statistics():
    response = requests.get(f"{API_BASE_URL}/stats")
    if response.status_code == 200:
        print("Statistics:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# 查詢有過濾條件的統計資料
def get_filtered_statistics():
    filter_condition = input("Enter filter condition: ")
    response = requests.get(f"{API_BASE_URL}/stats/{filter_condition}")
    if response.status_code == 200:
        print("Filtered statistics:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# 主選單
def menu():
    while True:
        print("\n--- Application API Console ---")
        print("1. Create Application")
        print("2. Get Applications")
        print("3. Update Application Status")
        print("4. Get Total Application Statistics")
        print("5. Get Filtered Statistics")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            create_application()
        elif choice == "2":
            get_applications()
        elif choice == "3":
            update_application_status()
        elif choice == "4":
            get_total_application_statistics()
        elif choice == "5":
            get_filtered_statistics()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()