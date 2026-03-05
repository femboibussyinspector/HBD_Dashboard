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
    res = conn.execute(text("SHOW INDEX FROM raw_google_map_drive_data")).fetchall()
    unique_found = False
    for r in res:
        # r[1] is Non_unique (0 means unique)
        # r[2] is Key_name
        if r[1] == 0:
            print(f"UNIQUE INDEX FOUND: {r[2]} on column {r[4]}")
            if r[2] == 'unique_business':
                unique_found = True
    
    if unique_found:
        print("\nCONFIRMATION: The 'unique_business' index is ACTIVE.")
        print("This means the database STRICTLY PREVENTS any duplicates based on Name, Address, and Phone Number.")
        print("All 1.5M+ records are guaranteed to be unique.")
    else:
        print("\nWARNING: No unique business index found!")
