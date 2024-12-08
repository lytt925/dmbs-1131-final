import sys
from user import main as user
from employee import main as employee

def main():
    print("Welcome to the Animal Shelter Application System!")
    print("Please select an login option:")
    print("1. User")
    print("2. Employee")
    print("3. Exit")
    role = input("Enter your choice: ")
    if role == "1":
        print("Please select an operation:")
        print("1. Register")
        print("2. Login")
        operation = input("Enter your choice: ")
        if operation == "1":
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            phone = input("Phone: ")
            address = input("Address: ")
            # user.register(name, email, password, phone, address)
            print("Registration successful!")
            print("Please login to continue.")
            email = input("Email: ")
            password = input("Password: ")
            # user(email)
        elif operation == "2":
            email = input("Email: ")
            password = input("Password: ")
            user.main(email)
    elif role == "2":
        employee_id = input("Employee ID: ")
        password = input("Password: ")
        # 呼叫employee的main程式，執行登入並顯示員工相關選單
        employee.main(int(employee_id), password)
        
    elif role == "3":
        print("Exiting...")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
