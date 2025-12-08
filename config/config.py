import os
from dotenv import load_dotenv

from lib.db import Database

load_dotenv()

def get_database():
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = int(os.getenv("POSTGRES_PORT", 5432))
    db_name = os.getenv("POSTGRES_DB", "piomadb")
    db_user = os.getenv("POSTGRES_USER", "piomauser")
    db_password = os.getenv("POSTGRES_PASSWORD", "superhaslo123")

    return Database(
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password
    )
