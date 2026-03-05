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
db_port = os.getenv('DB_PORT', '3306')

engine = create_engine(config.DATABASE_URI)

with engine.connect() as conn:
    print("--- TABLES ---")
    tables = conn.execute(text("SHOW TABLES")).fetchall()
    for t in tables:
        print(t[0])
        # Get columns for specific tables
        if t[0] in ['raw_google_map_drive_data', 'drive_folder_registry', 'gdrive_inventory_folders', 'raw_google_map']:
            print(f"  Columns for {t[0]}:")
            cols = conn.execute(text(f"SHOW COLUMNS FROM {t[0]}")).fetchall()
            for c in cols:
                print(f"    {c[0]} ({c[1]})")
