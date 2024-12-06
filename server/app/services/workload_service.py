from app.database import db

class WorkloadService:
    @staticmethod
    def get_averaged_workload(employee_id: int=None, month: str=None):
        if not(employee_id or month):
            return None
        if employee_id and month:
            condition = "WHERE employee_id = %s AND TO_CHAR(start_at, 'YYYY-MM') = %s"
            param = (employee_id, month)
        elif employee_id:
            condition = "WHERE employee_id = %s"
            param = (employee_id,)
        else :
            condition = "WHERE TO_CHAR(start_at, 'YYYY-MM') = %s"
            param = (month,)

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
                cur.execute(query, param)
                averaged_workload = cur.fetchall()
                if len(averaged_workload) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, aw)) for aw in averaged_workload]
                    return response
                return None
            