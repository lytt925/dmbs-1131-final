from typing import List
from app.database import db 

class ShelterService:
    @staticmethod
    def get_shelters() -> List[dict]:
        query = """
        SELECT shelter_id, name, address, phone FROM shelter;
        """

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_shelter_occupancy() -> List[dict]:
        query = """
            SELECT
                s.shelter_id,
                s.name,
                s.capacity,
                COUNT(a.animal_id) AS current_animals,
                (COUNT(a.animal_id)::FLOAT / s.capacity) * 100 AS occupancy_rate_percent
            FROM
                shelter s
            LEFT JOIN
                animal a ON s.shelter_id = a.shelter_id AND a.leave_at IS NULL
            GROUP BY
                s.shelter_id, s.name, s.capacity;
        """
        
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_shelter_animal_retention() -> List[dict]:
        query = """
            SELECT
                a.shelter_id,
                s.name AS shelter_name,
                a.species,
                AVG(EXTRACT(EPOCH FROM COALESCE(a.leave_at, '2026-02-28') - a.arrived_at) / 86400) AS avg_stay_days
            FROM
                animal a
            JOIN
                shelter s ON a.shelter_id = s.shelter_id
            GROUP BY
                a.shelter_id, s.name, a.species;
        """

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                result = [dict(zip(columns, row)) for row in rows]
        
        shelters = {}
        for row in result:
            shelter_id = row["shelter_id"]
            if shelter_id not in shelters:
                shelters[shelter_id] = {
                    "shelter_id": shelter_id,
                    "shelter_name": row["shelter_name"],
                    "retention": {}
                }
            shelters[shelter_id]["retention"][row["species"]] = row["avg_stay_days"]

        return list(shelters.values())