import requests
from config import API_BASE_URL

def login_employee(employee_id: int, password: str):
    # 呼叫後端提供的員工登入 API
    response = requests.get(f"{API_BASE_URL}/employees/login", params={"employee_id": employee_id, "password": password})
    
    if response.status_code == 200:
        # 登入成功，回傳員工資訊
        return response.json()
    else:
        # 登入失敗，印出錯誤訊息
        error_detail = response.json().get('detail', 'Invalid credentials')
        print(error_detail)
        return None
