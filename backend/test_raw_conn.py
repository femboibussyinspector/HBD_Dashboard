import os
import time
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
# Use the raw password from env if available
raw_pass = os.getenv('DB_PASSWORD') 

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', '3306')

print(f"Attempting connection to {DB_HOST}...")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{raw_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(config.DATABASE_URI)

try:
    start = time.time()
    with engine.connect() as conn:
        print(f"Connected in {time.time()-start:.2f}s")
        res = conn.execute(text("SELECT 1")).scalar()
        print(f"Query Result: {res}")
            
except Exception as e:
    print(f"Error: {e}")
