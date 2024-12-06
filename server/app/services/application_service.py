from app.database import db
from datetime import datetime
from typing import Optional

class ApplicationService:
    @staticmethod
    def create_application(application_id: int,
                           update_at: datetime,
                           status: str,
                           user_id: int,
                           animal_id: int) -> Optional[dict]:
        query = """
        INSERT INTO application (application_id, update_at, status, user_id, animal_id)
        SELECT %s, %s, %s, %s, %s
        WHERE EXISTS (
            SELECT 1 FROM animal
            WHERE animal_id = %s
              AND adoption_status = '未領養'
        )
        AND EXISTS (
            SELECT 1 FROM registration
            WHERE user_id = %s
              AND status = 'C'
        )
        RETURNING *;
        """
        
        params = (application_id, update_at, status, user_id, animal_id, animal_id, user_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                created_application = cur.fetchone()
                conn.commit()

                if created_application:
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, created_application))
                else:
                    return None


    @staticmethod
    def get_applications(user_id: int=None, animal_id: int=None):
        # 根據傳入參數組成動態的 SQL 條件式與參數
        conditions = []
        params = []

        if user_id is not None:
            conditions.append("user_id = %s")
            params.append(user_id)
        if animal_id is not None:
            conditions.append("animal_id = %s")
            params.append(animal_id)

        base_query = "SELECT * FROM application"
        
        if conditions:
            # 使用 AND 串接條件
            where_clause = " WHERE " + " AND ".join(conditions)
            query = base_query + where_clause
        else:
            # 若沒有傳入任何條件，就直接不加 WHERE，返回所有紀錄(或視需求返回 None)
            # 如果不想在沒有條件時返回所有紀錄，可以選擇在 Router 層報錯。
            query = base_query

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, tuple(params))
                applications = cur.fetchall()
                if not applications:
                    return None
                columns = [desc[0] for desc in cur.description]
                result = [dict(zip(columns, app)) for app in applications]
                return result
            
    @staticmethod
    def update_application_status(application_id: int, status: str):
        query = """
        UPDATE application
        SET status = %s
        WHERE application_id = %s
        RETURNING application_id, update_at, status, user_id, animal_id;
        """
        params = (status, application_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                updated_application = cur.fetchone()
                conn.commit()

                if updated_application:
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, updated_application))
                else:
                    return None