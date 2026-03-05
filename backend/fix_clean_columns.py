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

DB_USER = os.getenv('DB_USER')
DB_PASS = getattr(config, "DB_PASSWORD", "")
# DB_PASS = quote_plus(os.getenv('DB_PASSWORD_PLAIN'))  # REFACTORED: Now using config.py
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(config.DATABASE_URI)

with engine.connect() as conn:
    print("Checking columns...")
    res = conn.execute(text("DESCRIBE raw_clean_google_map_data"))
    cols = [r[0] for r in res.fetchall()]
    
    queries = [
        ('validation_status', "ALTER TABLE raw_clean_google_map_data ADD COLUMN validation_status varchar(50) DEFAULT 'VALID' AFTER area"),
        ('cleaning_status', "ALTER TABLE raw_clean_google_map_data ADD COLUMN cleaning_status varchar(50) DEFAULT 'CLEANED' AFTER validation_status"),
        ('missing_fields', "ALTER TABLE raw_clean_google_map_data ADD COLUMN missing_fields text AFTER cleaning_status"),
        ('invalid_format_fields', "ALTER TABLE raw_clean_google_map_data ADD COLUMN invalid_format_fields text AFTER missing_fields"),
        ('duplicate_reason', "ALTER TABLE raw_clean_google_map_data ADD COLUMN duplicate_reason text AFTER invalid_format_fields"),
        ('processed_at', "ALTER TABLE raw_clean_google_map_data ADD COLUMN processed_at datetime DEFAULT NULL AFTER duplicate_reason")
    ]
    
    for col, q in queries:
        if col not in cols:
            print(f"Adding {col}...")
            conn.execute(text(q))
    
    conn.commit()
    print("Done.")
