import psycopg2

db_config = {
    'dbname': 'shelter_db',
    'user': 'postgres',
    'password': 'pg_password',
    'host': 'hpc.psy.ntu.edu.tw',
    'port': 5432
}

shelters = [
    ("台北市流浪動物之家", "台北市內湖區民權東路6段", "0227298888", 100),
    ("新北市流浪動物之家", "新北市板橋區文化路2段", "0222645678", 150),
    ("桃園市動物保護教育園區", "桃園市中壢區環中東路", "0345890123", 200),
    ("台中市動物之家", "台中市西屯區文心路四段", "0423776655", 120),
    ("高雄市動物之家", "高雄市三民區鼎中路", "0723456789", 180),
    ("台南市動物之家", "台南市永康區中正南路", "0624567890", 140),
    ("基隆市動物之家", "基隆市仁愛區孝三路", "0245678901", 80),
    ("新竹市動物之家", "新竹市東區光復路", "0356789012", 90),
    ("嘉義市動物之家", "嘉義市東區忠孝路", "0523456789", 110),
    ("花蓮縣動物之家", "花蓮縣吉安鄉建國路", "0389123456", 70)
]

insert_query = """
INSERT INTO shelter (name, address, phone, capacity)
VALUES (%s, %s, %s, %s);
"""

try:
    # Connect to the database
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Insert each shelter record
            cursor.executemany(insert_query, shelters)
            print("Mock data inserted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
