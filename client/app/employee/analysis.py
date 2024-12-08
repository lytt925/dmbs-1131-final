import requests
from config import API_BASE_URL
from datetime import datetime

def view_shelter_occupancy():
    print("收容率分析")
    
    try:
        response = requests.get(f"{API_BASE_URL}/shelters/occupancy")
        if response.status_code == 200:
            data = response.json().get("data", [])
            if not data:
                print("目前沒有可用的收容率資料。")
                return

            # 按照 shelter_id 排序
            sorted_data = sorted(data, key=lambda x: x['shelter_id'])

            print("\n收容所收容率（按收容所 ID 排序）：")
            for shelter in sorted_data:
                print(f"收容所 ID: {shelter['shelter_id']}")
                print(f"名稱: {shelter['name']}")
                print(f"容量: {shelter['capacity']} 隻")
                print(f"當前動物數量: {shelter['current_animals']}")
                print(f"收容率: {shelter['occupancy_rate_percent']:.2f}%\n")
        else:
            print(f"無法取得收容率資料，原因：{response.json().get('detail', '未知錯誤')}")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")



def view_average_animal_retention():
    print("平均滯留時間分析")
    
    try:
        response = requests.get(f"{API_BASE_URL}/shelters/retention")
        if response.status_code == 200:
            data = response.json().get("data", [])
            if not data:
                print("目前沒有可用的平均滯留時間資料。")
                return

            # 按照 shelter_id 排序
            sorted_data = sorted(data, key=lambda x: x['shelter_id'])

            print("\n收容所平均滯留時間（以天為單位，按收容所 ID 排序）：")
            for shelter in sorted_data:
                print(f"收容所 ID: {shelter['shelter_id']}")
                print(f"名稱: {shelter['shelter_name']}")
                print("動物品種平均滯留時間:")
                for species, avg_days in shelter["retention"].items():
                    print(f"  {species}: {avg_days:.2f} 天")
                print("\n")
        else:
            print(f"無法取得平均滯留時間資料，原因：{response.json().get('detail', '未知錯誤')}")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")



def view_monthly_adoption_stats():
    print("每月領養申請狀況")
    print("請選擇篩選條件：")
    print("1. 動物體型 (size)")
    print("2. 動物品種 (species)")
    print("3. 動物細分類品種 (breed)")
    print("4. 動物性別 (sex)")
    print("5. 收容所 ID (shelter_id)")
    
    filter_options = {
        "1": "size",
        "2": "species",
        "3": "breed",
        "4": "sex",
        "5": "shelter_id"
    }

    filter_choice = input("請輸入選擇 (1-5): ").strip()
    filter_key = filter_options.get(filter_choice)

    if not filter_key:
        print("無效的選擇，請重試。")
        return

    try:
        response = requests.get(f"{API_BASE_URL}/applications/stats/{filter_key}")
        print(f"完整回應: {response.text}")  # 添加這行以打印 API 回應

        if response.status_code == 200:
            data = response.json()
            if not data:
                print("目前沒有可用的統計資料。")
                return

            print(f"\n每月領養申請統計（篩選條件：{filter_key}）：")
            for stat in data:
                print(f"月份: {stat['month']}")
                print(f"{filter_key}: {stat[filter_key]}")
                print(f"總申請數: {stat['total_applications']}")
                print(f"成功申請數: {stat['successful_rate']}")
                print(f"失敗申請數: {stat['fail_rate']}\n")
        else:
            print(f"無法取得統計資料，原因：{response.json().get('detail', '未知錯誤')}")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")


def view_employee_stats():
    print("員工打卡與照顧統計")

    try:
        # 要求輸入統計的時間範圍
        start_time_str = input("請輸入統計開始時間 (格式: YYYY-MM-DD): ").strip()
        end_time_str = input("請輸入統計結束時間 (格式: YYYY-MM-DD): ").strip()

        # 驗證輸入格式並轉換為 datetime
        try:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d")
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d")
        except ValueError:
            print("時間格式錯誤，請使用 YYYY-MM-DD 格式。")
            return

        # 發送請求至 API
        response = requests.get(
            f"{API_BASE_URL}/employees/stats/",
            params={"start_time": start_time.isoformat(), "end_time": end_time.isoformat()}
        )

        if response.status_code == 200:
            data = response.json()
            if not data:
                print("目前沒有符合條件的統計資料。")
                return

            # 顯示員工打卡數與照顧數統計
            print("\n員工打卡數與照顧數統計：")
            for stat in data:
                print(f"員工 ID: {stat['employee_id']}")
                print(f"姓名: {stat['employeename']}")
                print(f"打卡次數: {stat['punchcount']}")
                print(f"照顧動物數量: {stat['careanimalcount']}\n")
        else:
            print(f"無法取得統計資料，原因：{response.json().get('detail', '未知錯誤')}")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")