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

load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = getattr(config, "DB_PASSWORD", "")
# db_pass = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or '')  # REFACTORED: Now using config.py
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
engine = create_engine(config.DATABASE_URI)

files_to_check = [
    'google_maps_data_Popular_Computer_Training_Institutes_Hojai_Assam.csv',
    'google_maps_data_Popular_Computer_Training_Institutes_Sivasagar_Assam.csv'
]

print("Checking ingestion status for specific files...")
with engine.connect() as conn:
    for file_name in files_to_check:
        query = text("SELECT count(*), city, state, category FROM raw_google_map WHERE file_name = :fname GROUP BY city, state, category")
        res = conn.execute(query, {"fname": file_name}).fetchall()
        if res:
            for row in res:
                print(f"✅ FOUND: {file_name}")
                print(f"   - Count: {row[0]} records")
                print(f"   - City: {row[1]}")
                print(f"   - State: {row[2]}")
                print(f"   - Category: {row[3]}")
        else:
            print(f"❌ NOT FOUND: {file_name}")
