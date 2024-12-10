import random
from faker import Faker
import psycopg2
from datetime import date

# Database configuration
db_config = {
    'dbname': 'db',
    'user': 'postgres',
    'password': 'pwd',
    'host': 'somewhere',
    'port': 5432
}

# Create a Faker instance for generating random data
fake = Faker()

# Predefined breeds, sizes, and sexes for animals
cat_breeds = ['短毛貓', '長毛貓', '折耳貓', '波斯貓', '暹羅貓']
dog_breeds = ['拉布拉多', '黃金獵犬', '柴犬', '法鬥', '德國牧羊犬']
sizes = ['XS', 'S', 'M', 'L', 'XL']
sexes = ['M', 'F']

# Function to generate random animal records
def generate_animal_data(num_records=10000):
    animal_data = []
    for _ in range(num_records):
        name = fake.first_name() 
        species = random.choice(['貓', '狗'])
        breed = random.choice(cat_breeds if species == '貓' else dog_breeds)
        size = random.choice(sizes)
        sex = random.choice(sexes)
        is_sterilized = random.choice([True, False])
        shelter_id = random.randint(1, 10)  # Random shelter_id between 1 and 10
        arrived_at = fake.date_between(start_date=date(2026, 1, 1), end_date=date(2026, 1, 31))
        animal_data.append((name, species, breed, size, sex, is_sterilized, shelter_id, arrived_at))
    return animal_data

# Insert data into the database
def insert_animal_data(animal_data):
    insert_query = """
    INSERT INTO animal (name, species, breed, size, sex, is_sterilized, shelter_id, arrived_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        # Connect to the database
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Insert animal data in batches
                cursor.executemany(insert_query, animal_data)
                print("Animal data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Generate and insert animal data
    print("Generating animal data...")
    animal_data = generate_animal_data(1000)
    print("Inserting animal data into the database...")
    insert_animal_data(animal_data)
