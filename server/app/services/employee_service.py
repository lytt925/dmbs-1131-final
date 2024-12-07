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