from app.database import db


class ActivityService:
    @staticmethod
    def get_all_activities_from_now(shelter_id: int = None):
        query = """
        SELECT * FROM activity
        WHERE time >= NOW()
        {shelter_filter};
        """.format(shelter_filter=f"AND shelter_id = {shelter_id}" if shelter_id is not None else "")
        
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                if not rows:
                    return []
                columns = [desc[0] for desc in cur.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result