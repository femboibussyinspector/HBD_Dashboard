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
# db_pass = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT', '3306')

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(config.DATABASE_URI)

with engine.connect() as conn:
    raw = conn.execute(text("SELECT COUNT(*) FROM raw_google_map_drive_data")).fetchone()[0]
    clean = conn.execute(text("SELECT COUNT(*) FROM raw_clean_google_map_data")).fetchone()[0]
    gmap_master = conn.execute(text("SELECT COUNT(*) FROM g_map_master_table")).fetchone()[0]
    meta = conn.execute(text("SELECT meta_value FROM etl_metadata WHERE meta_key='last_processed_id'")).fetchone()
    
    print(f"Raw Count: {raw}")
    print(f"Clean Count: {clean}")
    print(f"G-Map Master Count: {gmap_master}")
    print(f"Last Processed ID: {meta[0] if meta else 'None'}")
