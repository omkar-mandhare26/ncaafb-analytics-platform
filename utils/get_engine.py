import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

host=os.getenv("DB_HOST")
port=int(os.getenv("DB_PORT"))
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
database=os.getenv("DB_NAME")

db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

def get_engine():
    return create_engine(db_uri)
