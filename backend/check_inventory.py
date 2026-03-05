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
    f_count = conn.execute(text("SELECT COUNT(*) FROM gdrive_inventory_folders")).scalar()
    file_count = conn.execute(text("SELECT COUNT(*) FROM raw_google_map")).scalar()
    print(f"Total Folders Ingested: {f_count}")
    print(f"Total Files Ingested: {file_count}")
    
    print("\nRecent Folders (Today):")
    recent = conn.execute(text("SELECT name, city, category, modified_time FROM gdrive_inventory_folders WHERE modified_time >= '2026-02-02' LIMIT 10")).fetchall()
    for r in recent:
        print(f" - {r[0]} | {r[1]} > {r[2]} | {r[3]}")
