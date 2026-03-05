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
DB_PORT = os.getenv('DB_PORT', '3306')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(config.DATABASE_URI)

try:
    with engine.connect() as conn:
        print("--- ALL Processes ---")
        res = conn.execute(text("SHOW FULL PROCESSLIST"))
        for row in res:
            # id, user, host, db, command, time, state, info
            print(f"ID: {row[0]}, User: {row[1]}, Command: {row[4]}, State: {row[6]}, Time: {row[5]}, Info: {row[7]}")
                
except Exception as e:
    print(f"Error: {e}")
