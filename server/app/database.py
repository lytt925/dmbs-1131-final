import psycopg2
from contextlib import contextmanager
from app.config import Config

class Database:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def connect(self):
        return psycopg2.connect(**self.db_config)

    @contextmanager
    def get_connection(self):
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()

db = Database(Config.DATABASE_CONFIG)
