from app.database import db
from datetime import datetime

class CareService:
    @staticmethod
    def get_care_by_id(animal_id: int=None, employee_id: int=None):
        if (animal_id and employee_id):
            query = "SELECT * FROM care_record WHERE animal_id = %s AND employee_id = %s"
        else:
            query = "SELECT * FROM care_record WHERE animal_id = %s OR employee_id = %s"
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (animal_id, employee_id))
                care_record = cur.fetchall()
                if len(care_record) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [] 
                    for c in care_record:
                        response.append(dict(zip(columns, c)))
                    return response
                return None
            
    @staticmethod
    def create_care(animal_id: int, employee_id: int, care_type: str):
        query = '''
            INSERT INTO care_record (animal_id, employee_id, care_type, start_at)
            VALUES (%s, %s, %s, %s) 
            RETURNING *
        '''
        start_at = datetime.now().replace(microsecond=0)
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (animal_id, employee_id, care_type, start_at))
                care_record = cur.fetchone()
                conn.commit()
                return care_record
                