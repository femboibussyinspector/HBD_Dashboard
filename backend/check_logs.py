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

load_dotenv(r'd:\Honeybee digital\Dashboard latest\backend\.env')
db_pass = getattr(config, "DB_PASSWORD", "")
# db_pass = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_pass}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(config.DATABASE_URI)

with engine.connect() as conn:
    print("Last 10 validation logs (with missing_count):")
    try:
        res = conn.execute(text("SELECT id, total_processed, missing_count, valid_count, duplicate_count, cleaned_count, last_id, timestamp FROM data_validation_log ORDER BY id DESC LIMIT 10")).fetchall()
        for row in res:
            print(row)
    except Exception as e:
        print(f"Validation log error: {e}")
