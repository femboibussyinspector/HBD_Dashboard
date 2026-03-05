from sqlalchemy import create_engine, text
import os
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
db_port = os.getenv('DB_PORT')

engine = create_engine(config.DATABASE_URI)

fixes = {
    "Andhrapradesh": "Andhra Pradesh",
    "Arunachalpradesh": "Arunachal Pradesh",
    "Uttarpradesh": "Uttar Pradesh",
    "Madhyapradesh": "Madhya Pradesh",
    "Himachalpradesh": "Himachal Pradesh",
    "Westbengal": "West Bengal",
    "Tamilnadu": "Tamil Nadu",
}

with engine.begin() as conn:
    for old, new in fixes.items():
        res = conn.execute(text("UPDATE raw_google_map_drive_data SET state = :new WHERE state = :old"), {"new": new, "old": old})
        print(f"Fixed {old} -> {new}: {res.rowcount} rows")
    
    # Fuzzy fix for Arunachal
    res = conn.execute(text("UPDATE raw_google_map_drive_data SET state = 'Arunachal Pradesh' WHERE state LIKE 'Arunachalpradesh%'"))
    print(f"Fixed Arunachal (wildcard): {res.rowcount} rows")
