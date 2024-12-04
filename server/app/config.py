import os
from dotenv import load_dotenv

# Load .env file from the server folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

class Config:
    DATABASE_CONFIG = {
        'dbname': os.getenv("DB_NAME"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'port': int(os.getenv("DB_PORT", 5432)),  # Default to 5432 if not set
    }
