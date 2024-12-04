import random
import psycopg2
from config import db_config
import numpy as np

# 三國演義人物名字
names = [
    "劉備", "關羽", "張飛", "諸葛亮", "趙雲", "馬超", "黃忠", "曹操", "夏侯惇", "許褚", 
    "司馬懿", "郭嘉", "荀彧", "典韋", "張遼", "呂布", "貂蟬", "董卓", "袁紹", "田豐",
    "顏良", "文醜", "孫權", "周瑜", "魯肅", "陸遜", "甘寧", "黃蓋", "程普", "呂蒙",
    "太史慈", "華佗", "張仲景", "龐統", "徐庶", "孟獲", "祝融夫人", "魏延", "姜維", "鄧艾",
    "鐘會", "黃月英", "馬良", "馬謖", "陳到", "徐晃", "曹仁", "曹洪", "夏侯淵", "曹植",
    "曹丕", "郭淮", "張郃", "文聘", "袁術", "張任", "李嚴", "蔣琬", "費禕", "姜維",
    "楊儀", "魏延", "龔景", "李恢", "董襲", "步練師", "丁奉", "徐盛", "諸葛瑾", "龐德",
    "蔣幹", "韓當", "張昭", "張溫", "華雄", "張角", "張寶", "張梁", "何進", "王允",
    "韓馥", "公孫瓚", "李傕", "郭汜", "華雄", "于禁", "呂布", "陳宮", "高順", "張楊",
    "劉表", "蔡瑁", "蒯越", "黃忠", "馬騰", "韓遂", "馬超", "龐德", "韓浩", "胡車兒"
]

# 職位
positions = ["護理員", "管理員", "行政員", "清潔員", "獸醫助理", "營運主管"]
genders = ["男", "女"]

# 隨機生成電話號碼
def generate_phone():
    return f"09{random.randint(10000000, 99999999)}"

def generate_password():
    return "password123"

# 生成員工數據
employees = [
    (
        names[i],  # 姓名
        random.choice(genders),  # 性別
        random.choice(positions),  # 職位
        generate_phone(),  # 電話
        generate_password(),  # 密碼
        (i % 10) + 1  # 收容所ID（平均分配）
    )
    for i in range(100)
]

# SQL 插入語句
insert_query = """
INSERT INTO employee (name, gender, position, phone, password, shelter_id)
VALUES (%s, %s, %s, %s, %s, %s);
"""

try:
    # 連接資料庫
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # 批量插入員工數據
            cursor.executemany(insert_query, employees)
            print("100名員工數據已成功插入。")
except Exception as e:
    print(f"發生錯誤: {e}")
