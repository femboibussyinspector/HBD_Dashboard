import re
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import sys
import os
# Ensure config.py is importable
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) if 'model' in os.path.dirname(__file__) or 'database' in os.path.dirname(__file__) else os.path.abspath(os.path.dirname(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
from config import config

# Load environment variables
load_dotenv('.env') 

DB_USER = os.getenv('DB_USER')
DB_PASS = getattr(config, "DB_PASSWORD", "")
# DB_PASS = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or '')  # REFACTORED: Now using config.py
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(config.DATABASE_URI)

# ---------------- VALIDATORS ---------------- #

def is_placeholder(val):
    if not val: return True
    placeholders = ['n/a', 'none', 'null', 'placeholder', 'unknown']
    return str(val).lower().strip() in placeholders

def check_mandatory(row):
    required = ["name", "address", "category", "city", "state", "phone_number"]
    missing = [f for f in required if not row.get(f) or str(row.get(f)).strip() == "" or is_placeholder(row.get(f))]
    return missing

def validate_formats(row):
    invalid_fields = []
    
    # Phone: 10-15 digits
    phone = re.sub(r'\D', '', str(row.get('phone_number', '')))
    if not (10 <= len(phone) <= 15):
        invalid_fields.append("phone_number")
        
    # Website: Force https (if present)
    website = str(row.get('website', '')).lower().strip()
    if website and not (website.startswith('http://') or website.startswith('https://')):
        # We can clean this later, but for now mark as invalid if it's garbage
        if '.' not in website:
            invalid_fields.append("website")
            
    # Reviews Avg: 0-5
    try:
        avg = float(row.get('reviews_avg', 0) or 0)
        if not (0 <= avg <= 5):
            invalid_fields.append("reviews_avg")
    except:
        invalid_fields.append("reviews_avg")
        
    return invalid_fields

# ---------------- CORE PIPELINE ---------------- #

def run_ingestion():
    """Phase 1: Raw → Validation (INSERT ONLY)"""
    query = text("""
    INSERT INTO validation_raw_google_map (
        raw_id, name, address, website, phone_number, reviews_count, reviews_avg, 
        category, subcategory, city, state, area, created_at
    )
    SELECT 
        r.id, r.name, r.address, r.website, r.phone_number, r.reviews_count, r.reviews_avg, 
        r.category, r.subcategory, r.city, r.state, r.area, r.created_at
    FROM raw_google_map_drive_data r
    LEFT JOIN validation_raw_google_map v ON r.id = v.raw_id
    WHERE v.raw_id IS NULL;
    """)
    with engine.begin() as conn:
        conn.execute(query)
    print("✅ Ingestion Phase Complete.")

def run_validation():
    """Phase 2: Validation Engine"""
    # Fetch PENDING rows
    df = pd.read_sql("SELECT * FROM validation_raw_google_map WHERE validation_status = 'PENDING' LIMIT 5000", engine)

    if df.empty:
        print("ℹ️ No pending data to validate.")
        return

    for index, row in df.iterrows():
        validation_status = "STRUCTURED"
        missing_fields = []
        invalid_format_fields = []
        duplicate_reason = None
        
        # 1. Mandatory Fields
        missing = check_mandatory(row)
        if missing:
            validation_status = "UNSTRUCTURED"
            missing_fields = missing
        
        # 2. Format Validation
        if validation_status == "STRUCTURED":
            invalid = validate_formats(row)
            if invalid:
                validation_status = "INVALID"
                invalid_format_fields = invalid
        
        # 3. Duplicate Detection (check against clean table)
        if validation_status == "STRUCTURED":
            # Simple check for now: name + address + phone
            check_query = text("""
                SELECT id FROM raw_clean_google_map_data 
                WHERE name = :name AND address = :address AND phone_number = :phone LIMIT 1
            """)
            with engine.connect() as conn:
                dup = conn.execute(check_query, {
                    "name": row['name'], 
                    "address": row['address'], 
                    "phone": row['phone_number']
                }).fetchone()
                if dup:
                    validation_status = "DUPLICATE"
                    duplicate_reason = "Exact match in clean data"

        # Update the validation record
        update_query = text("""
            UPDATE validation_raw_google_map 
            SET validation_status = :status,
                missing_fields = :missing,
                invalid_format_fields = :invalid,
                duplicate_reason = :dup_reason,
                processed_at = NOW()
            WHERE id = :id
        """)
        with engine.begin() as conn:
            conn.execute(update_query, {
                "status": validation_status,
                "missing": ",".join(missing_fields) if missing_fields else None,
                "invalid": ",".join(invalid_format_fields) if invalid_format_fields else None,
                "dup_reason": duplicate_reason,
                "id": row['id']
            })

    print(f"✅ Validation Phase Complete for {len(df)} rows.")

def run_cleaning():
    """Phase 3: Cleaning Engine"""
    df = pd.read_sql("""
        SELECT * FROM validation_raw_google_map 
        WHERE validation_status = 'STRUCTURED' AND cleaning_status = 'NOT_STARTED' 
        LIMIT 5000
    """, engine)
    
    if df.empty:
        print("ℹ️ No data to clean.")
        return
        
    for index, row in df.iterrows():
        # Clean data in memory
        clean_row = {
            "raw_id": row['raw_id'],
            "name": str(row['name']).strip(),
            "address": str(row['address']).strip(),
            "website": str(row['website']).lower().strip() if row['website'] else None,
            "phone_number": re.sub(r'\D', '', str(row['phone_number'])),
            "reviews_count": row['reviews_count'],
            "reviews_avg": row['reviews_avg'],
            "category": row['category'],
            "subcategory": row['subcategory'],
            "city": row['city'],
            "state": row['state'],
            "area": row['area'],
            "created_at": row['created_at'],
            "cleaning_status": "CLEANED"
        }
        
        # Force https on website if missing
        if clean_row['website'] and not (clean_row['website'].startswith('http://') or clean_row['website'].startswith('https://')):
            clean_row['website'] = 'https://' + clean_row['website']

        # Insert into clean table
        insert_query = text("""
            INSERT IGNORE INTO raw_clean_google_map_data (
                raw_id, name, address, website, phone_number, reviews_count, reviews_avg,
                category, subcategory, city, state, area, created_at, cleaning_status
            ) VALUES (
                :raw_id, :name, :address, :website, :phone_number, :reviews_count, :reviews_avg,
                :category, :subcategory, :city, :state, :area, :created_at, :cleaning_status
            )
        """)
        
        with engine.begin() as conn:
            conn.execute(insert_query, clean_row)
            
            # Update cleaning status in validation table
            conn.execute(text("UPDATE validation_raw_google_map SET cleaning_status = 'CLEANED' WHERE id = :id"), {"id": row['id']})
            
    print(f"✅ Cleaning Phase Complete for {len(df)} rows.")

def run_full_pipeline():
    print("🚀 Starting ETL Pipeline...")
    run_ingestion()
    run_validation()
    run_cleaning()
    print("⭐ ETL Pipeline Cycle Finished.")

if __name__ == "__main__":
    run_full_pipeline()
