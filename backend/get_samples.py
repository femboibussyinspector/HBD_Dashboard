import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv
import sys
import os
# Ensure config.py is importable
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) if 'model' in os.path.dirname(__file__) or 'database' in os.path.dirname(__file__) else os.path.abspath(os.path.dirname(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
from config import config
import json

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = getattr(config, "DB_PASSWORD", "")
# DB_PASS = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

def get_samples():
    engine = create_engine(config.DATABASE_URI)
    with engine.connect() as conn:
        query = text("SELECT name, address, phone_number, city, state, category, source FROM raw_google_map WHERE name IS NOT NULL ORDER BY ingestion_timestamp DESC LIMIT 5")
        results = conn.execute(query).fetchall()
        for row in results:
            print(f"Name: {row.name}")
            print(f"Address: {row.address}")
            print(f"Phone: {row.phone_number}")
            print(f"Location: {row.city}, {row.state}")
            print(f"Category: {row.category}")
            print(f"Source: {row.source}")
            print("-" * 30)


if __name__ == "__main__":
    get_samples()
