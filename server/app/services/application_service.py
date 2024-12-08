from app.database import db
from datetime import datetime
from typing import Optional, Dict, List


class ApplicationService:
    @staticmethod
    def create_application(user_id: int, animal_id: int) -> Dict:
        update_at = datetime.now()
        # user_id 在 registration 表中至少有一筆 status = 'A'
        # ---------------------------------------------------------
        check_user_query = """
        SELECT 1 FROM registration r
        JOIN activity a on a.activity_id = r.activity_id
        WHERE user_id = %s AND status = 'A' AND a.activity_type = 'C';
        """
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(check_user_query, (user_id,))
                user_check = cur.fetchone()

        # 若有任何條件不符合，直接返回失敗原因
        if user_check is None:
            return {"success": False, "reasons": "請至少參加一次活動"}

        # ---------------------------------------------------------
        # 檢查三個月內是否有過申請
        check_application_query = """
        SELECT 1 FROM application
        WHERE user_id = %s 
          AND update_at >= NOW() - INTERVAL '3 months';
        """

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(check_application_query, (user_id,))
                application_check = cur.fetchone()
        
        if application_check is not None:
            return {"success": False, "reasons": "三個月內不得重複申請"}

        insert_query = """
        INSERT INTO application (update_at, status, user_id, animal_id)
        VALUES (%s, 'P', %s, %s)
        RETURNING *;
        """
        params = (update_at, user_id, animal_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(insert_query, params)
                created_application = cur.fetchone()
                conn.commit()
                if created_application:
                    columns = [desc[0] for desc in cur.description]
                    return {
                        "success": True,
                        "data": dict(zip(columns, created_application)),
                    }

    @staticmethod
    def get_applications(user_id: int = None, animal_id: int = None):
        # 根據傳入參數組成動態的 SQL 條件式與參數
        conditions = []
        params = []

        if user_id is not None:
            conditions.append("user_id = %s")
            params.append(user_id)
        if animal_id is not None:
            conditions.append("animal_id = %s")
            params.append(animal_id)

        base_query = "SELECT * FROM application JOIN animal USING (animal_id)"

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
        SET status = %s,
            update_at = NOW()
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

    @staticmethod
    def fail_all_prev_applications(animal_id: int, exclude_application_id: int):
        # 將同一 animal_id 下狀態為 'P' 且非剛剛更新成功的 application 全部改為 'F'
        query = """
        UPDATE application
        SET status = 'F',
            update_at = NOW()
        WHERE animal_id = %s
          AND application_id != %s
          AND status = 'P';
        """
        params = (animal_id, exclude_application_id)

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()

    @staticmethod
    def get_total_application_statistics():
        query = """
            SELECT DATE_TRUNC('month', update_at) AS month, 
            COUNT(*) AS total_applications, 
            SUM(CASE WHEN status = 'S' THEN 1 ELSE 0 END) AS successful_rate,
            SUM(CASE WHEN status = 'F' THEN 1 ELSE 0 END) AS fail_rate
            FROM application AS app
            GROUP BY month;            
        """
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                statistics = cur.fetchall()
                if len(statistics) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, s)) for s in statistics]
                    return response
                return None

    @staticmethod
    def get_filtered_application_statistics(filter: str):
        if filter not in ["size", "species", "breed", "sex", "shelter_id"]:
            return None
        query = f"""
            SELECT {filter},
            DATE_TRUNC('month', update_at) AS month, 
            COUNT(*) AS total_applications, 
            SUM(CASE WHEN status = 'S' THEN 1 ELSE 0 END) AS successful_rate,
            SUM(CASE WHEN status = 'F' THEN 1 ELSE 0 END) AS fail_rate
            FROM application AS app
            JOIN animal AS ani ON 
                app.animal_id = ani.animal_id
            GROUP BY month, {filter};            
        """
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                statistics = cur.fetchall()
                if len(statistics) != 0:
                    columns = [desc[0] for desc in cur.description]
                    response = [dict(zip(columns, s)) for s in statistics]
                    return response
                return None
