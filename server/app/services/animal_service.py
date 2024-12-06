from app.database import db

class AnimalService:
    @staticmethod
    def get_animals(animal_name: str=None, animal_id: int=None, shelter_id: int=None):
        if not(animal_name or shelter_id or animal_id):
            return None
        if animal_id:
            query = "SELECT * FROM animal WHERE animal_id = %s"
            animal_param = (animal_id,)
        elif (animal_name and shelter_id):
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