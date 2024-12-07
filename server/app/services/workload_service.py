from app.database import db
from datetime import datetime

class WorkloadService:
    @staticmethod
    def get_averaged_workload_by_month(employee_id: int=None, year: str=None, month: str=None):
        if not(employee_id or month):
            return {
                "status": "error",
                "message": "Please specify at least one of the following parameters: employee_id, month",
                "error_code": 400  # 400 Bad Request
            }
        
        if not(year):
            year = datetime.now().strftime('%Y')
        if employee_id and month:
            condition = f"WHERE employee_id = {employee_id} AND TO_CHAR(start_at, 'YYYY-MM') = '{year}-{month}'"
        elif employee_id:
            condition = f"WHERE employee_id = {employee_id}"
        else :
            condition = f"WHERE TO_CHAR(start_at, 'YYYY-MM') = '{year}-{month}'"

        query = f'''
            SELECT employee_id,
            DATE_TRUNC('month', start_at) AS month,  
            COUNT(animal_id) AS avg_animal
            FROM care_record
            {condition}
            GROUP BY employee_id, month;
        '''
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                averaged_workload = cur.fetchall()
                if len(averaged_workload) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, aw)) for aw in averaged_workload]
                    return response
                return {
                    "status": "error",
                    "message": "No workload data found for the provided parameters",
                    "error_code": 404  # 404 Not Found
                }
            