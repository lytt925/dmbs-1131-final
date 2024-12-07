import requests
import json
from app.config import API_BASE_URL

API_BASE_URL += "/employees"

def employee_login():
    data = {
        "employee_id": int(input("Enter Employee ID: ")),
        "password": input("Enter Your Password"),
      
    }
    response = requests.post(f"{API_BASE_URL}/", json=data)
    if response.status_code == 200:
        print("Login Successfully!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
