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

SQL_CREATE_SUMMARY = """
CREATE TABLE IF NOT EXISTS dashboard_stats_summary_v5 (
    id INT PRIMARY KEY DEFAULT 1,
    total_records BIGINT DEFAULT 0,
    total_states INT DEFAULT 0,
    total_categories INT DEFAULT 0,
    total_csvs INT DEFAULT 0,
    last_updated DATETIME
);
"""

SQL_CREATE_STATE_CAT = """
CREATE TABLE IF NOT EXISTS state_category_summary_v5 (
    state VARCHAR(255),
    category VARCHAR(255),
    record_count INT,
    PRIMARY KEY (state, category)
);
"""

def refresh_summary():
    with engine.begin() as conn:
        print("Refreshing Global Summary...")
        # Global Summary
        conn.execute(text("INSERT IGNORE INTO dashboard_stats_summary_v5 (id, last_updated) VALUES (1, NOW())"))
        
        # Calculate totals
        res = conn.execute(text("SELECT COUNT(*), COUNT(DISTINCT state), COUNT(DISTINCT category), COUNT(DISTINCT drive_file_id) FROM raw_google_map_drive_data")).fetchone()
        
        conn.execute(text("""
            UPDATE dashboard_stats_summary_v5 
            SET total_records = :total, 
                total_states = :states, 
                total_categories = :cats, 
                total_csvs = :csvs, 
                last_updated = NOW() 
            WHERE id = 1
        """), {"total": res[0], "states": res[1], "cats": res[2], "csvs": res[3]})
        
        print("Refreshing State-Category Summary...")
        # State-Category Summary
        conn.execute(text("DELETE FROM state_category_summary_v5"))
        conn.execute(text("""
            INSERT INTO state_category_summary_v5 (state, category, record_count)
            SELECT state, category, COUNT(*) 
            FROM raw_google_map_drive_data 
            GROUP BY state, category
        """))
        print("Summary updated successfully.")

if __name__ == "__main__":
    with engine.begin() as conn:
        conn.execute(text(SQL_CREATE_SUMMARY))
        conn.execute(text(SQL_CREATE_STATE_CAT))
    refresh_summary()
