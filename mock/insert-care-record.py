import psycopg2
import random
from datetime import datetime, timedelta
from config import db_config

# Database connection setup
conn = psycopg2.connect(**db_config)

# 從 animal 表格中取得動物資訊的函數
def get_animal_info(conn):
    query = """
    SELECT animal_id, shelter_id, arrived_at, leave_at 
    FROM animal;
    """  # 包含所有動物，不限制 leave_at 是否為 NULL
    
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()  # 返回包含動物資訊的列表

# 從 employee 表格中取得同一 shelter 的職員資訊
def get_employee_ids_by_shelter(conn, shelter_id):
    query = """
    SELECT employee_id 
    FROM employee
    WHERE shelter_id = %s;
    """
    
    with conn.cursor() as cur:
        cur.execute(query, (shelter_id,))
        return [row[0] for row in cur.fetchall()]  # 返回職員ID列表

# 隨機生成 n 筆資料，並確保滿足時間與 shelter 限制
def generate_random_data(conn, animal_info, n):
    records = []
    care_types = ['C', 'F', 'W']  # C: 清潔, F: 餵食, W: 散步
    for id in range(len(animal_info)):
        animal = animal_info[id]
        animal_id = animal[0]
        shelter_id = animal[1]
        arrived_at = animal[2]
        leave_at = animal[3]
        # 查詢對應該 shelter 的職員
        employee_ids = get_employee_ids_by_shelter(conn, shelter_id)
        if not employee_ids:
            continue  # 若沒有符合條件的職員，跳過此動物
        
        for _ in range(n):
            employee_id = random.choice(employee_ids)
            care_type = random.choice(care_types)

            # 隨機生成 care 的開始和結束時間
            # 如果 leave_at 為 NULL，則只考慮 arrived_at 作為下限
            if leave_at:
                max_days = (leave_at - arrived_at).days
            else:
                max_days = 20

            # 生成隨機的到達時間，包含天數、隨機小時和分鐘
            start_at = arrived_at + timedelta(
                days=random.randint(0, max_days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            records.append((animal_id, employee_id, care_type, start_at))

    return records

# 插入資料到資料庫的函數
def insert_care_records(conn, records):
    try:
        with conn.cursor() as cur:
            # 插入資料的 SQL 語法
            insert_query = """
            INSERT INTO care_record (animal_id, employee_id, care_type, start_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (animal_id, employee_id, start_at) DO NOTHING;
            """

            # 執行插入操作
            cur.executemany(insert_query, records)
            conn.commit()

            print(f"成功插入 {cur.rowcount} 筆資料")
    
    except Exception as e:
        print(f"資料插入失敗: {e}")

# 主程式
try:
    # 建立資料庫連接
    conn = psycopg2.connect(**db_config)

    # 從 animal 表格獲取動物資訊
    animal_info = get_animal_info(conn)
    if not animal_info:
        print("無可用的動物資訊")
    else:
        n = 15  # 指定要生成的資料筆數
        random_records = generate_random_data(conn, animal_info, n)
        insert_care_records(conn, random_records)

except Exception as e:
    print(f"資料庫連接失敗: {e}")

finally:
    if conn:
        conn.close()
