from employee import login, application, care_record, animal, analysis


def main(employee_id: int, password: str):
    employee = login.login_employee(employee_id, password)
    if not employee:
        # 登入失敗，直接返回
        return

    print(f"{employee['name']} (Employee ID: {employee['employee_id']}) 已登入動物收容所系統")
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
                # 照顧紀錄子選單
                while True:
                    print("\nCare Records Menu:")
                    print("1. 查詢照顧紀錄 (Query Care Records)")
                    print("2. 新增照顧紀錄 (Create Care Record)")
                    print("3. 返回上層選單 (Back)")
                    sub_op = input("Enter your choice: ")
                    match sub_op:
                        case "1":
                            care_record.query_care_records()
                        case "2":
                            care_record.create_care_record()
                        case "3":
                            break
                        case _:
                            print("Invalid choice. Please try again.")
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
                # 動物管理子選單
                while True:
                    print("\nAnimal Management Menu:")
                    print("1. 查詢動物資料 (Query Animals)")
                    print("2. 修改領養狀態 (Modify Adoption Status)")
                    print("3. 新增動物資料 (Add Animal Data)")
                    print("4. 返回上層選單 (Back)")
                    sub_op = input("Enter your choice: ")
                    match sub_op:
                        case "1":
                            animal.query_animals()
                        case "2":
                            animal.update_animal_adoption_status()
                        case "3":
                            animal.add_animal_data()
                        case "4":
                            break
                        case _:
                            print("Invalid choice. Please try again.")
            case "4":
                # 打卡
                print("Punch: (TODO)")
            case "5":
                # 營運分析子選單
                while True:
                    print("\nOperations Analysis Menu:")
                    print("1. 收容率 (Shelter Occupancy)")
                    print("2. 動物平均滯留時間 (Average Animal Stay)")
                    print("3. 每月領養申請狀況 (Monthly Adoption Stats)")
                    print("4. 員工打卡及照顧數 (Employee Punch and Care Records)")
                    print("5. 返回上層選單 (Back)")
                    sub_op = input("Enter your choice: ")
                    match sub_op:
                        case "1":
                            analysis.view_shelter_occupancy()
                        case "2":
                            analysis.view_average_animal_retention()
                        case "3":
                            analysis.view_monthly_adoption_stats()
                        case "4":
                            analysis.view_employee_stats() 
                        case "5":
                            break
                        case _:
                            print("Invalid choice. Please try again.")
            case "6":
                # 登出
                return
            case _:
                print("Invalid choice. Please try again.")
