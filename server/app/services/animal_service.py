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
    def update_animals_adoption(
        adoption_status: str,
        animal_name: str = None, animal_id: int = None, shelter_id: int = None,
    ):
        current_time = datetime.now()
        if animal_id:
            query = """
            UPDATE animal
            SET adoption_status = %s, leave_at = %s
            WHERE animal_id = %s;
            """
            params = (adoption_status, current_time, animal_id)
        elif animal_name and shelter_id:
            query = """
            UPDATE animal
            SET adoption_status = %s, leave_at = %s
            WHERE name = %s AND shelter_id = %s;
            """
            params = (adoption_status, current_time, animal_name, shelter_id)
        else:
            query = """
            UPDATE animal
            SET adoption_status = %s, leave_at = %s
            WHERE name = %s OR shelter_id = %s;
            """
            params = (adoption_status, current_time, animal_name, shelter_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                if cur.rowcount == 0:
                    return None
                return {
                    "message": "Animal adoption status updated successfully",
                    "animal_id": animal_id,
                    "leave_at": current_time,
                }

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
            RETURNING animal_id, name, species, breed, size, is_sterilized, adoption_status, sex, shelter_id, death_time, leave_at, arrived_at;
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
