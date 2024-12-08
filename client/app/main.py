import sys
from user import main as user
from employee import main as employee

def main():
    print("歡迎使用動物收容所系統！")
    print("請選擇登入身份:")
    print("1. 一般使用者")
    print("2. 員工")
    print("3. 離開")
    role = input("請輸入選項編號: ")
    if role == "1":
        print("開始使用:")
        print("1. 註冊")
        print("2. 登入")
        operation = input("請輸入選項編號: ")
        if operation == "1":
            name = input("姓名: ")
            email = input("電子郵件: ")
            phone = input("電話: ")
            gender = input("性別: ")
            password = input("密碼: ")
            # user.register(name, email, password, phone, address)
            print("註冊成功！")
            print("請重新登入。")
            email = input("電子郵件: ")
            password = input("密碼: ")
            # user(email)
        elif operation == "2":
            email = input("電子郵件: ")
            password = input("密碼: ")
            user.main(email)
    elif role == "2":
        employee_id = input("員工 ID: ")
        password = input("密碼: ")
        # 呼叫employee的main程式，執行登入並顯示員工相關選單
        employee.main(int(employee_id), password)
        
    elif role == "3":
        print("系統關閉中...")
        sys.exit()
    else:
        print("錯誤的選項，請重新輸入。")

if __name__ == "__main__":
    main()
