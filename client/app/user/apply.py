import requests
from config import API_BASE_URL

sex = {'M': '公', 'F': '母'}

def apply(user_id: str):
    print("\n選擇您想查詢的收容所: ")
    response = requests.get(f"{API_BASE_URL}/shelters")
    shelters = response.json()['data']
    for i, shelter in enumerate(shelters):
        print(f"{i + 1}. {shelter['name']}")
    print("\n")
    shelter_id = int(input("請輸入選項編號: "))
    shelter_id = shelters[shelter_id - 1]['shelter_id']

    response = requests.get(f"{API_BASE_URL}/animals/unadopted", params={"shelter_id": shelter_id})
    all_animals = response.json()
    pages = len(all_animals) // 5 + 1
    page = 0

    while True:
        animals = all_animals[page * 5: (page + 1) * 5]
        print(f"\n動物列表: ({page+1}/{pages} 頁)")

        for i, animal in enumerate(animals):
            print(f"{page * 5 + i + 1}. {animal['name']}\n | 品種: {animal['species']}\n | 性別: {sex[animal['sex']]}\n | 體型: {animal['size']}")
            print("\n")
        page =  input("請輸入您想查看的頁數 (輸入 'Exit' 以結束瀏覽): ")
        if page == 'Exit':
            break
        page = int(page) - 1

    animal_id = int(input("請輸入您想申請認養的動物編號: "))
    print("提出申請中...")
    animal_id = all_animals[animal_id - 1]['animal_id']
    response = requests.post(f"{API_BASE_URL}/applications", json={"user_id": user_id, "animal_id": animal_id})
    print("\n")
    print("❤️ 申請已提交！請耐心等候收容所的回覆。\n")