from app.database import db


class UserService:
    @staticmethod
    def get_user_by_id(user_id: int):
        query = "SELECT * FROM public.user WHERE user_id = %s"
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id,))
                user = cur.fetchone()
                if user:
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, user))
                return None

    @staticmethod
    def create_user(name: str, email: str):
        query = "INSERT INTO public.user (name, email) VALUES (%s, %s) RETURNING *"
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, email))
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id