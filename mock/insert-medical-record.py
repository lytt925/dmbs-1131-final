import random
import psycopg2
from datetime import datetime, timedelta
from config import db_config

# Database connection setup
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Define hospital names based on shelter locations
shelter_hospitals = {
    1: "台北動物醫院",
    2: "新北動物醫院",
    3: "桃園動物醫院",
    4: "台中動物醫院",
    5: "高雄動物醫院",
    6: "台南動物醫院",
    7: "基隆動物醫院",  
    8: "新竹動物醫院",
    9: "嘉義動物醫院",
    10: "花蓮動物醫院",
}

# Fetch animals and employees data
cursor.execute("SELECT animal_id, name, shelter_id FROM animal")
animals = cursor.fetchall()

cursor.execute(
    "SELECT employee_id, name, position, shelter_id FROM employee WHERE position IN ('獸醫助理', '管理員')"
)
employees = cursor.fetchall()

# Process animals and employees
for animal_id, animal_name, animal_shelter_id in animals:
    # Filter employees in the same shelter
    shelter_employees = [emp for emp in employees if emp[3] == animal_shelter_id]

    if shelter_employees:
        for _ in range(10):  # Insert 10 records for each animal
            # Select a random employee from the shelter
            selected_employee = random.choice(shelter_employees)
            employee_id, employee_name, position, shelter_id = selected_employee

            # Generate medical record details
            hospital = shelter_hospitals.get(animal_shelter_id, "不明動物醫院")
            item = random.choice(["疫苗接種", "身體檢查", "驅蟲", "手術"])
            reason = f"{animal_name}的{item}"
            cost = random.randint(500, 2000)  # Random cost
            time = datetime.now() + timedelta(
                days=random.randint(1, 3 * 365)
            )  # Random date within the next 3 years

            # Check details with SELECT before insertion
            cursor.execute(
                """
                SELECT animal.animal_id, employee.employee_id, animal.shelter_id 
                FROM animal
                JOIN employee ON animal.shelter_id = employee.shelter_id
                WHERE animal.animal_id = %s AND employee.employee_id = %s
                """,
                (animal_id, employee_id),
            )

            details = cursor.fetchone()

            if details:
                # Insert medical record
                cursor.execute(
                    """
                    INSERT INTO medical_record (animal_id, employee_id, time, hospital, reason, item, cost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (animal_id, employee_id, time, hospital, reason, item, cost),
                )
                print(
                    f"成功新增 {animal_name} 的醫療紀錄 (醫院: {hospital}, 員工: {employee_name}, 時間: {time})"
                )

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
