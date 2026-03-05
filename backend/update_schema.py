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

if __name__ == "__main__":
    engine = create_engine(config.DATABASE_URI)
    try:
        with engine.begin() as conn:
            # Check if columns exist first or just use ALTER TABLE
            # For MySQL, we can use a procedure or just try/except if we want to be safe, 
            # but usually ADD COLUMN IF NOT EXISTS is fine in newer MySQL
            print("Adding columns to raw_google_map_data...")
            try:
                conn.execute(text("ALTER TABLE raw_google_map_data ADD COLUMN drive_modified_at DATETIME AFTER state"))
                print("Added drive_modified_at")
            except Exception as e:
                print(f"drive_modified_at might already exist: {e}")

            try:
                conn.execute(text("ALTER TABLE raw_google_map_data ADD COLUMN drive_path TEXT AFTER drive_modified_at"))
                print("Added drive_path")
            except Exception as e:
                print(f"drive_path might already exist: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
