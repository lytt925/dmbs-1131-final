import requests
from config import API_BASE_URL

def apply(email: str):
    user_id = requests.get(f"{API_BASE_URL}/users", params={"email": email}).json()['user_id']

    print("\nPlease select a shelter:")
    response = requests.get(f"{API_BASE_URL}/shelters")
    shelters = response.json()['data']
    for i, shelter in enumerate(shelters):
        print(f"{i + 1}. {shelter['name']}")
    print("\n")
    shelter_id = int(input("Enter your choice: "))
    shelter_id = shelters[shelter_id - 1]['shelter_id']

    response = requests.get(f"{API_BASE_URL}/animals/unadopted", params={"shelter_id": shelter_id})
    animals = response.json()
    print("\nAvailable animals:")
    for i, animal in enumerate(animals):
        print(f"{i + 1}. {animal['name']}\n | 品種: {animal['species']}\n | 性別: {animal['sex']}\n | 體型: {animal['size']}")
        print("\n")

    animal_id = int(input("Enter the animal ID you want to apply for: "))
    print("Applying for adoption...")
    animal_id = animals[animal_id - 1]['animal_id']
    response = requests.post(f"{API_BASE_URL}/applications", json={"user_id": user_id, "animal_id": animal_id})
    print("\n")
    print("Application submitted successfully!\nPlease wait for the shelter to review your application.")