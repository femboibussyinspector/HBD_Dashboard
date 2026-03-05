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
    print("--- ALL TABLES ---")
    try:
        res = conn.execute(text("SHOW TABLES")).fetchall()
        for r in res:
            print(f"  {r[0]}")
    except Exception as e:
        print(f"Error listing tables: {e}")

    print("\n--- TABLE: raw_google_map (Sample) ---")
    try:
        count = conn.execute(text("SELECT COUNT(*) FROM raw_google_map")).scalar()
        print(f"Count: {count}")
        res = conn.execute(text("SELECT * FROM raw_google_map LIMIT 1")).fetchone()
        print(f"Sample: {res}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- TABLE: raw_google_map_data ---")
    try:
        count = conn.execute(text("SELECT COUNT(*) FROM raw_google_map_data")).scalar()
        print(f"Count: {count}")
        cols = conn.execute(text("DESCRIBE raw_google_map_data")).fetchall()
        for c in cols:
            print(f"  {c[0]} ({c[1]})")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- TABLE: raw_google_map_records ---")
    try:
        count = conn.execute(text("SELECT COUNT(*) FROM raw_google_map_records")).scalar()
        print(f"Count: {count}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- TABLE: master_table ---")
    try:
        count = conn.execute(text("SELECT COUNT(*) FROM master_table")).scalar()
        print(f"Count: {count}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- TABLE: google_Map ---")
    try:
        count = conn.execute(text("SELECT COUNT(*) FROM google_Map")).scalar()
        print(f"Count: {count}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- TABLE: raw_cleaned_data ---")
    try:
        count = conn.execute(text("SELECT COUNT(*) FROM raw_cleaned_data")).scalar()
        print(f"Count: {count}")
    except Exception as e:
        print(f"Error: {e}")
