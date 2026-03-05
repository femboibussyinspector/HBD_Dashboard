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

db_pass = getattr(config, "DB_PASSWORD", "")
# db_pass = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_pass}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(config.DATABASE_URI)

with engine.connect() as conn:
    print("INDEXES:")
    res = conn.execute(text("SHOW INDEX FROM raw_google_map_drive_data")).fetchall()
    for r in res:
        print(f"Name: {r[2]}, Unique: {r[1] == 0}, Column: {r[4]}")
    
    print("\nSAMPLE (last 2):")
    res = conn.execute(text("SELECT id, name, drive_file_name FROM raw_google_map_drive_data ORDER BY id DESC LIMIT 2")).fetchall()
    for r in res:
        print(r)
