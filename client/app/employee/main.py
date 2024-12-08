from employee import login
from employee import application

def main(employee_id: int, password: str):
    employee = login.login_employee(employee_id, password)
    if not employee:
        # 登入失敗，直接返回
        return

    print(f"Welcome {employee['name']} (Employee ID: {employee['employee_id']}) to the Animal Shelter System!")
    while True:
        print("Menu:")
        print("1. 照顧紀錄 (Care Records)")
        print("2. 領養資訊 (Adoption Info)")
        print("3. 動物管理 (Animal Management)")
        print("4. 打卡 (Punch)")
        print("5. 營運分析 (Operations Analysis)")
        print("6. Logout")
        operation = input("Enter your choice: ")
        match operation:
            case "1":
                # 照顧紀錄相關功能 (未實作)
                print("Care Records: (TODO)")
            case "2":
                # 領養資訊子選單
                while True:
                    print("\nAdoption Info Menu:")
                    print("1. 查詢領養申請 (Query Applications)")
                    print("2. 修改領養申請狀態 (Update Application Status)")
                    print("3. 返回上層選單 (Back)")
                    sub_op = input("Enter your choice: ")
                    match sub_op:
                        case "1":
                            application.query_applications()
                        case "2":
                            application.update_application_status()
                        case "3":
                            break
                        case _:
                            print("Invalid choice. Please try again.")
            case "3":
                # 動物管理
                print("Animal Management: (TODO)")
            case "4":
                # 打卡
                print("Punch: (TODO)")
            case "5":
                # 營運分析
                print("Operations Analysis: (TODO)")
            case "6":
                # 登出
                return
            case _:
                print("Invalid choice. Please try again.")
