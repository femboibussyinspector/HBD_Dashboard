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
    try:
        log = conn.execute(text("SELECT id, last_id FROM data_validation_log ORDER BY id DESC LIMIT 1")).fetchone()
        print("Last log:", log)
    except Exception as e: print("Log error:", e)

    try:
        raw_max = conn.execute(text("SELECT MAX(id) FROM raw_google_map_drive_data")).fetchone()[0]
        print("Max raw ID:", raw_max)
    except Exception as e: print("Raw max error:", e)
