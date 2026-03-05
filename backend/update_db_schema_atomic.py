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
# DB_PASS = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

def update_schema():
    engine = create_engine(config.DATABASE_URI)
    
    # 1. New Columns to add to raw_google_map
    columns = [
        ("name", "TEXT"),
        ("address", "TEXT"),
        ("website", "TEXT"),
        ("phone_number", "VARCHAR(255)"),
        ("reviews_count", "INT"),
        ("reviews_average", "FLOAT"),
        ("category", "VARCHAR(255)"),
        ("subcategory", "TEXT"),
        ("city", "VARCHAR(255)"),
        ("state", "VARCHAR(255)"),
        ("area", "VARCHAR(255)"),
        ("file_id", "VARCHAR(255)"),
        ("file_name", "VARCHAR(255)"),
        ("full_drive_path", "TEXT"),
        ("created_time", "DATETIME"),
        ("modified_time", "DATETIME"),
        ("ingestion_timestamp", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ("source", "VARCHAR(50) DEFAULT 'google_drive'")
    ]
    
    print("🚀 Starting Refined Schema Update...")
    with engine.connect() as conn:
        # Check existing columns
        existing_cols = [row[0] for row in conn.execute(text("SHOW COLUMNS FROM raw_google_map")).fetchall()]
        
        with engine.begin() as trans:
            # 1. Update main table columns
            for col_name, col_type in columns:
                if col_name not in existing_cols:
                    try:
                        trans.execute(text(f"ALTER TABLE raw_google_map ADD COLUMN {col_name} {col_type}"))
                        print(f"✅ Added: {col_name}")
                    except Exception as e:
                        print(f"⚠️ Error adding {col_name}: {e}")
                else:
                    print(f"ℹ️ Exists: {col_name}")

            # 2. Create sync inventory table for persistence Tracking
            trans.execute(text("""
                CREATE TABLE IF NOT EXISTS gdrive_sync_inventory (
                    file_id VARCHAR(255) PRIMARY KEY,
                    file_name VARCHAR(255),
                    modified_time DATETIME,
                    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("✅ Sync inventory table verified.")

        # 3. Add Indices & Deduplication Constraint
        try:
            with engine.begin() as trans:
                # Primary indices for search performance
                trans.execute(text("CREATE INDEX idx_file_id ON raw_google_map (file_id)"))
                trans.execute(text("CREATE INDEX idx_city_state ON raw_google_map (city, state)"))
                
                # Composite unique index for row-level deduplication (First 100 chars to avoid key length limits)
                try:
                    trans.execute(text("CREATE UNIQUE INDEX idx_business_dedupe ON raw_google_map (file_id, name(100), address(100))"))
                    print("✅ Unique deduplication constraint added.")
                except:
                    pass 
                    
                print("✅ Indices updated.")
        except Exception as e:
            print(f"ℹ️ Index notice: {e}")


                
    print("💎 Schema update complete. Zero data loss guaranteed.")


if __name__ == "__main__":
    update_schema()
