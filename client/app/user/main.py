from config import API_BASE_URL
from apply import apply

def main(email):
    print("Welcome to the Animal Shelter System!")
    print("Menu:")
    print("1. My Accounts")
    print("2. Join Acitivities")
    print("3. Apply for Adoption")
    print("4. Exit")
    operation = input("Enter your choice: ")
    match(operation):
        case "1":
            print("My Accounts:")
        case "2":
            print("Upcoming Acitivities:")
        case "3":
            apply(email)
        case "4":
            return
        case _:
            print("Invalid choice. Please try again.")