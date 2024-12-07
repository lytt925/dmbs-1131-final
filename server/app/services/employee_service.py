from app.database import db
from typing import List, Dict
from datetime import datetime


class EmployeeService:
    @staticmethod
    def get_all_employees_stats(start_time: datetime, end_time: datetime) -> List[Dict]:
        query = """
        SELECT 
            E.Employee_Id,
            E.Name AS EmployeeName,
            COUNT(DISTINCT P.Created_At) AS PunchCount,
            COUNT(DISTINCT C.Animal_Id) AS CareAnimalCount
        FROM 
            Employee E
        LEFT JOIN 
            Punch P ON E.Employee_Id = P.Employee_Id 
                     AND P.Created_At BETWEEN %s AND %s
        LEFT JOIN 
            Care_record C ON E.Employee_Id = C.Employee_Id 
                         AND C.Start_At BETWEEN %s AND %s
        GROUP BY E.Employee_Id, E.Name
        ORDER BY E.Employee_Id;
        """

        params = (start_time, end_time, start_time, end_time)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                if not rows:
                    return []
                columns = [desc[0] for desc in cur.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result

    @staticmethod
    def create_punch_for_user(employee_id: int, punch_type: str) -> List[Dict]:
        query = """
        INSERT INTO punch (employee_id, punch_type) 
        VALUES (%s, %s)
        RETURNING employee_id, created_at, punch_type;
        """
        # punch_type = 'I' or 'O'
        params = (employee_id, punch_type)
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                row = cur.fetchone()
                conn.commit()
                return {
                    "employee_id": row[0],
                    "created_at": row[1],
                    "punch_type": row[2],
                }

    @staticmethod
    def get_averaged_workload_by_month(
        employee_id: int = None, month: str = None, year: str = None
    ) -> List[Dict]:
        if not (employee_id or month):
            return {
                "status": "error",
                "message": "Please specify at least one of the following parameters: employee_id, month",
                "error_code": 400,  # 400 Bad Request
            }

        if not (year):
            year = datetime.now().strftime("%Y")
        if employee_id and month:
            condition = f"WHERE employee_id = {employee_id} AND TO_CHAR(start_at, 'YYYY-MM') = '{year}-{month}'"
        elif employee_id:
            condition = f"WHERE employee_id = {employee_id}"
        else:
            condition = f"WHERE TO_CHAR(start_at, 'YYYY-MM') = '{year}-{month}'"

        query = f"""
            SELECT employee_id,
            DATE_TRUNC('month', start_at) AS month,  
            COUNT(animal_id) AS avg_animal
            FROM care_record
            {condition}
            GROUP BY employee_id, month;
        """
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
                    "error_code": 404,  # 404 Not Found
                }
