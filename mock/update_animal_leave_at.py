import random
import psycopg2
from datetime import timedelta, date

# Database configuration
db_config = {
    'dbname': 'shelter_db',
    'user': 'postgres',
    'password': 'pg_password',
    'host': 'hpc.psy.ntu.edu.tw',
    'port': 5432
}

# Function to calculate random retention periods
def generate_retention_periods(arrived_at_date):
    # Generate a random retention period between 10 and 300 days
    retention_period = int(random.gauss(30, 10))  # Mean 30, standard deviation 10
    # Ensure retention period is within the valid range
    retention_period = max(10, min(retention_period, 300))
    return arrived_at_date + timedelta(days=retention_period)

# Update the `leaved_at` field for all animals
def update_leaved_at():
    try:
        # Connect to the database
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Fetch all animals with their `arrived_at` date
                select_query = "SELECT animal_id, arrived_at FROM animal WHERE leave_at IS NULL;"
                cursor.execute(select_query)
                animals = cursor.fetchall()
                
                # Update each animal's `leaved_at` date
                update_query = "UPDATE animal SET leave_at = %s WHERE animal_id = %s;"
                for animal_id, arrived_at in animals:
                    leave_at = generate_retention_periods(arrived_at)
                    cursor.execute(update_query, (leave_at, animal_id))
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Updating leaved_at dates for all animals...")
    update_leaved_at()
    print(f"Update complete.")
