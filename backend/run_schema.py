import os
import pymysql
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
# DB_PASS = os.getenv('DB_PASSWORD_PLAIN')  # REFACTORED: Now using config.py
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

sql_file = os.path.join('sql', 'architect_schema.sql')

conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT,
    client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
)

try:
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    with conn.cursor() as cursor:
        print(f"Executing {sql_file}...")
        cursor.execute(sql_content)
    conn.commit()
    print("✅ Schema applied successfully.")
finally:
    conn.close()
