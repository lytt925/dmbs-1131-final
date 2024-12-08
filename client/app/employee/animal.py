import requests
from config import API_BASE_URL

def query_animals():
    print("查詢動物資料")
    print("您可以選擇輸入以下任一條件進行查詢：")
    print("1. 動物名稱")
    print("2. 動物 ID")
    print("3. 收容所 ID")
    
    animal_name = input("請輸入動物名稱 (若不使用此條件請留空): ")
    animal_id = input("請輸入動物 ID (若不使用此條件請留空): ")
    shelter_id = input("請輸入收容所 ID (若不使用此條件請留空): ")

    # 構建請求參數
    params = {}
    if animal_name.strip():
        params["animal_name"] = animal_name.strip()
    if animal_id.strip():
        params["animal_id"] = int(animal_id.strip())
    if shelter_id.strip():
        params["shelter_id"] = int(shelter_id.strip())

    # 發送查詢請求
    response = requests.get(f"{API_BASE_URL}/animals", params=params)

    if response.status_code == 200:
        animals = response.json()
        if not animals:
            print("找不到符合條件的動物資料。")
            return

        # 分頁邏輯
        items_per_page = 5
        pages = (len(animals) + items_per_page - 1) // items_per_page  # 計算總頁數（上取整）
        page = 0

        while True:
            # 顯示當前頁面的動物資料
            start_index = page * items_per_page
            end_index = start_index + items_per_page
            current_page_animals = animals[start_index:end_index]

            print(f"\n動物資料: ({page + 1}/{pages} 頁)")
            for i, animal in enumerate(current_page_animals):
                print(f"{start_index + i + 1}. 動物 ID: {animal['animal_id']}")
                print(f"   名稱: {animal['name']}")
                print(f"   品種: {animal['species']}")
                print(f"   性別: {animal['sex']}")
                print(f"   體型: {animal['size']}")
                print(f"   收容所 ID: {animal['shelter_id']}")
                print(f"   狀態: {animal['adoption_status']}\n")

            # 用戶輸入頁數
            user_input = input("請輸入想查看的頁數 (輸入 'Exit' 以結束瀏覽): ").strip()
            if user_input.lower() == 'exit':
                break

            try:
                new_page = int(user_input) - 1
                if new_page < 0 or new_page >= pages:
                    print("無效的頁數，請輸入有效的頁碼。")
                else:
                    page = new_page
            except ValueError:
                print("無效的輸入，請輸入有效的頁碼或 'Exit' 結束。")
    else:
        print(f"查詢失敗，原因：{response.json().get('detail', '未知錯誤')}")


def update_animal_adoption_status():
    print("修改動物領養狀態")
    animal_id = input("請輸入動物 ID: ")
    print("領養狀態：")
    print("1. 未領養")
    print("2. 申請處理中")
    print("3. 已領養")
    status_choice = input("請選擇領養狀態: ")
    adoption_status_map = {
        '1': '未領養',
        '2': '已領養'
    }
 
    while status_choice not in ['1', '2']:
        print("無效的選擇，請重新輸入。")
        status_choice = input("請選擇領養狀態: ")
    
    adoption_status = adoption_status_map[status_choice]

    try:
        response = requests.put(f"{API_BASE_URL}/animals", 
                                params={
                                    "animal_id": animal_id, 
                                    "adoption_status": adoption_status
                                })

        if response.status_code == 200:
            print("動物領養狀態更新成功！")
            result = response.json()
            print(f"動物 ID: {animal_id}")
            print(f"新的領養狀態: {adoption_status}")
        else:
            error_detail = response.json().get('detail', '更新動物領養狀態時發生錯誤')
            print(error_detail)
    except Exception as e:
        print(f"發生錯誤：{e}")

import requests
from config import API_BASE_URL

def add_animal_data():
    print("新增動物資料")
    name = input("請輸入動物名稱: ")
    species_options = ["狗", "貓"]
    while True:
        species = input("請輸入動物品種 (狗或貓): ").strip()
        if species in species_options:
            break
        print("無效的品種，請重新輸入 (僅限: 狗、貓)")

    breed = input("請輸入動物細分類品種 (例如：柴犬、波斯貓): ")
    size_options = ["XS", "S", "M", "L", "XL"]
    while True:
        size = input("請輸入動物體型 (XS, S, M, L, XL): ").strip().upper()
        if size in size_options:
            break
        print("無效的體型，請重新輸入 (僅限: XS, S, M, L, XL)")

    while True:
        is_sterilized_input = input("是否已絕育 (輸入 'true' 或 'false'): ").strip().lower()
        if is_sterilized_input in ["true", "false"]:
            is_sterilized = is_sterilized_input == "true"
            break
        print("無效的輸入，請重新輸入 (僅限: true 或 false)")

    sex_options = ["M", "F"]
    while True:
        sex = input("請輸入動物性別 (M 或 F): ").strip().upper()
        if sex in sex_options:
            break
        print("無效的性別，請重新輸入 (僅限: M 或 F)")

    shelter_id = input("請輸入收容所 ID: ")

    animal_data = {
        "name": name.strip(),
        "species": species,
        "breed": breed.strip(),
        "size": size,
        "is_sterilized": is_sterilized,
        "sex": sex,
        "shelter_id": int(shelter_id.strip())
    }

    response = requests.post(f"{API_BASE_URL}/animals", json=animal_data)

    if response.status_code == 200:
        created_animal = response.json()
        print("動物資料新增成功！")
        print(f"動物 ID: {created_animal['animal_id']}, 名稱: {created_animal['name']}")
        print(f"品種: {created_animal['species']} - {created_animal['breed']}")
        print(f"性別: {created_animal['sex']}, 體型: {created_animal['size']}")
        print(f"是否絕育: {'是' if created_animal['is_sterilized'] else '否'}, 收容所 ID: {created_animal['shelter_id']}\n")
    else:
        print(f"新增失敗，原因：{response.json().get('detail', '未知錯誤')}")
