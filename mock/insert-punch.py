import psycopg2
import random
from datetime import datetime, timedelta

db_config = {
    'dbname': 'shelter_db',
    'user': 'postgres',
    'password': 'pg_password',
    'host': 'hpc.psy.ntu.edu.tw',
    'port': 5432
}

# Generate attendance data
def generate_attendance_data():
    attendance_data = []
    used_dates = set()  # To track used dates for employees
    start_date = datetime(2024, 12, 1, 8, 0, 0)  # Start date for records
    employee_ids = range(1, 101)  # Employee IDs from 1 to 100

    # Ensure each employee has at least 4 valid records (2 days of I/O)
    for employee_id in employee_ids:
        day_count = 0
        while day_count < 2:
            work_date = start_date + timedelta(days=random.randint(0, 30))
            if (employee_id, work_date.date()) not in used_dates:
                # Generate valid punch-in and punch-out times
                punch_in = datetime.combine(work_date.date(), datetime.min.time()) + timedelta(hours=random.randint(8, 10))  # Random punch-in between 8:00 and 10:00
                punch_out = punch_in + timedelta(hours=random.randint(4, 8))  # Random punch-out 4-8 hours later
                attendance_data.append((employee_id, punch_in, 'I'))
                attendance_data.append((employee_id, punch_out, 'O'))
                used_dates.add((employee_id, work_date.date()))
                day_count += 1

    # Generate additional records to reach 1000 total
    while len(attendance_data) < 1000:
        employee_id = random.choice(employee_ids)
        work_date = start_date + timedelta(days=random.randint(0, 30))
        if (employee_id, work_date.date()) not in used_dates:
            punch_in = datetime.combine(work_date.date(), datetime.min.time()) + timedelta(hours=random.randint(8, 10))
            punch_out = punch_in + timedelta(hours=random.randint(4, 8))
            attendance_data.append((employee_id, punch_in, 'I'))
            attendance_data.append((employee_id, punch_out, 'O'))
            used_dates.add((employee_id, work_date.date()))
    
    return attendance_data

# Insert query
insert_query = """
INSERT INTO attendance (employee_id, created_at, punch_type)
VALUES (%s, %s, %s);
"""

try:
    # Connect to the database
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Generate mock data
            attendance_data = generate_attendance_data()
            # Insert attendance records
            cursor.executemany(insert_query, attendance_data)
            print("Mock attendance data inserted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
