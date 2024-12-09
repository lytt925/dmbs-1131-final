from app.database import db

class UserService:
    @staticmethod
    def get_user(user_id: int=None, email: str=None):
        if not (user_id or email):
            return None
        if user_id:
            query = "SELECT * FROM public.user WHERE user_id = %s"
            params = (user_id,)
        elif email:
            query = "SELECT * FROM public.user WHERE email = %s"
            params = (email,)
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                user = cur.fetchone()
                if user:
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, user))
                return None

    @staticmethod
    def create_user(name: str, email: str, gender: str, password: str, phone: str):
        query = "INSERT INTO users (name, email, gender, password, phone) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, email, gender, password, phone))
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id