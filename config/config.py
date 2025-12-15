import os
from dotenv import load_dotenv
from lib.db import Database

load_dotenv()

def get_database():
    db_host = os.getenv("POSTGRES_HOST")
    db_port = int(os.getenv("POSTGRES_PORT"))
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")

    return Database(
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password
    )
