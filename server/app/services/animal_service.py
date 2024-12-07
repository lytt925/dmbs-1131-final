from app.database import db
from datetime import datetime
from typing import Optional
from app.models.animal import AnimalModel


class AnimalService:
    @staticmethod
    def get_animals(
        animal_name: str = None, animal_id: int = None, shelter_id: int = None
    ):
        if not (animal_name or shelter_id or animal_id):
            return None
        if animal_id:
            query = "SELECT * FROM animal WHERE animal_id = %s"
            animal_param = (animal_id,)
        elif animal_name and shelter_id:
            query = "SELECT * FROM animal WHERE name = %s AND shelter_id = %s"
            animal_param = (animal_name, shelter_id)
        else:
            query = "SELECT * FROM animal WHERE name = %s OR shelter_id = %s"
            animal_param = (animal_name, shelter_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, animal_param)
                animals = cur.fetchall()
                if len(animals) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, animal)) for animal in animals]
                    return response
                return None

    @staticmethod
    def get_unadopted_animals(shelter_id: int = None):
        query = """
        SELECT * FROM animal 
        WHERE adoption_status = '未領養' AND shelter_id = %s;
        """
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (shelter_id,))
                animals = cur.fetchall()
                if animals:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, animal)) for animal in animals]
                    return response
                return None

    @staticmethod
    def update_animals_adoption(animal_id: int, adoption_status: str):
        if adoption_status == "已領養":
            leave_at_time = datetime.now()
        else:
            leave_at_time = None
        
        query = """
        UPDATE animal
        SET adoption_status = %s, leave_at = %s
        WHERE animal_id = %s;
        """
        params = (adoption_status, leave_at_time, animal_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                if cur.rowcount == 0:
                    return None
                return {"animal_id": animal_id, "adoption_status": adoption_status}

    @staticmethod
    def create_animal(
        name: str,
        species: str,
        breed: str,
        size: str,
        is_sterilized: bool,
        sex: str,
        shelter_id: int,
    ):
        query = """
            INSERT INTO animal (name, species, breed, size, is_sterilized, sex, shelter_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
         """
        params = (
            name,
            species,
            breed,
            size,
            is_sterilized,
            sex,
            shelter_id,
        )

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                row = cur.fetchone()
                conn.commit()
                columns = [desc[0] for desc in cur.description]
                animal = dict(zip(columns, row))
                animal = AnimalModel(**animal)
                conn.commit()
                return animal

    @staticmethod
    def check_animal_availability(animal_id: int):
        query = """
        SELECT adoption_status FROM animal WHERE animal_id = %s;
        """
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (animal_id,))
                adoption_status = cur.fetchone()
                if adoption_status:
                    if adoption_status[0] == "未領養":
                        return True
                    return False
                if not adoption_status:
                    return None
    
    @staticmethod
    def fail_all_prev_applications(animal_id: int):
        query = """
        UPDATE application
        SET status = 'F'
        WHERE animal_id = %s AND status = 'P';
        """
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (animal_id,))
                conn.commit()
                return True
