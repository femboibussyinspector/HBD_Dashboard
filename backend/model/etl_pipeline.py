import os
import re
import sys
import pandas as pd
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
import time
import logging

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Configure logging with UTF-8 encoding
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("etl_pipeline.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Load environment variables
load_dotenv('.env')

DB_USER = os.getenv('DB_USER')
DB_PASS = getattr(config, "DB_PASSWORD", "")
# DB_PASS = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or '')  # REFACTORED: Now using config.py
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', '3306')

DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(config.DATABASE_URI)

BATCH_SIZE = 1500

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
        
    # Website: Must contain domain (if present)
    website = str(row.get('website', '')).lower().strip()
    if website and '.' not in website:
        invalid_fields.append("website")
            
    # Reviews Avg: 0-5
    try:
        avg = float(row.get('reviews_avg', 0) or 0)
        if not (0 <= avg <= 5):
            invalid_fields.append("reviews_avg")
    except:
        invalid_fields.append("reviews_avg")
        
    return invalid_fields

def normalize_text(text):
    if not text:
        return ""
    return str(text).lower().strip()

def normalize_phone(phone):
    return re.sub(r'\D', '', str(phone) if phone else "")

# ---------------- CORE PIPELINE ---------------- #

def run_ingestion():
    """Phase 1: Raw → Validation (INSERT ONLY)"""
    logger.info("📥 [INGESTION] Starting Phase 1 — Raw -> Validation...")
    query = text("""
    INSERT INTO validation_raw_google_map (
        raw_id, name, address, website, phone_number, reviews_count, reviews_avg, 
        category, subcategory, city, state, area, created_at, validation_status, cleaning_status
    )
    SELECT 
        r.id, r.name, r.address, r.website, r.phone_number, r.reviews_count, r.reviews_average, 
        r.category, r.subcategory, r.city, r.state, r.area, r.added_time, 'PENDING', 'NOT_STARTED'
    FROM raw_google_map_drive_data r
    LEFT JOIN validation_raw_google_map v ON r.id = v.raw_id
    WHERE v.raw_id IS NULL
    LIMIT :limit;
    """)
    
    try:
        with engine.begin() as conn:
            result = conn.execute(query, {"limit": BATCH_SIZE})
            logger.info(f"📥 [INGESTION] Phase 1 Complete. Rows inserted: {result.rowcount}")
    except Exception as e:
        logger.error(f"📥 [INGESTION] Phase 1 Failed: {e}")
        raise

def run_validation():
    """Phase 2: Validation Engine"""
    logger.info("🔍 [VALIDATION] Starting Phase 2 — Checking PENDING rows...")
    
    # Fetch PENDING rows
    try:
        df = pd.read_sql("SELECT * FROM validation_raw_google_map WHERE validation_status = 'PENDING' LIMIT %s" % BATCH_SIZE, engine)
    except Exception as e:
        logger.error(f"🔍 [VALIDATION] Failed to fetch pending rows: {e}")
        return

    if df.empty:
        logger.info("🔍 [VALIDATION] No pending data to validate.")
        return

    updates = []
    
    # Pre-fetch potential duplicates from clean table? 
    # Or check one by one? Doing one by one inside loop is slow. 
    # But for 5000 rows, maybe okay. 
    # Optimizing: Fetch clean data that might match? Too complex.
    # Let's do batch check or stick to row-by-row for simplicity/safety first, maybe optimize if slow.
    # Actually, we can check duplicates in Python if we load clean table, but that's too big.
    # We will query DB for duplicates.

    # Prepare connection for duplicate checking to reuse
    with engine.connect() as conn:
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
            
            # 3. Duplicate Detection
            if validation_status == "STRUCTURED":
                # Normalize for check
                norm_name = normalize_text(row['name'])
                norm_addr = normalize_text(row['address'])[:100] # match index length
                norm_phone = normalize_phone(row['phone_number'])
                
                check_query = text("""
                    SELECT id FROM raw_clean_google_map_data 
                    WHERE name = :name AND address LIKE :address AND phone_number = :phone LIMIT 1
                """)
                # Note: Exact match on normalized fields might be tricky in pure SQL without stored stored generated columns.
                # But requirement says "Match using normalized name, normalized address, normalized phone".
                # The clean table has specific data, but the query uses `name`, `address` columns.
                # We assume the CLEAN table data IS normalized.
                # So we should compare `row` (which is raw) normalized vs clean table.
                # We can try to match loosely or we rely on the clean table being clean.
                
                # Let's use the provided logic: "Match using normalized name, normalized address, normalized phone"
                # Since we can't easily normalize on the fly in SQL for the clean table index unless it's stored that way,
                # We will assume exact string match against the clean table constitutes a duplicate for now, 
                # as the clean table contains normalized data.
                
                dup = conn.execute(check_query, {
                    "name": row['name'], # This is raw name. 
                    # If we want to match normalized, we need to normalize `row` data here.
                    # But the clean table `name` is the CLEANED name.
                    # So we should compare `clean(row['name'])` vs `clean_table.name`.
                    # But we are in Validation phase, not Cleaning phase.
                    # The prompt says: "Match using normalized name...".
                    # Implicitly, we should normalize the current row's data just for the CHECK.
                     
                    "name": str(row['name']).strip(), # Basic normalization
                    "address": str(row['address']).strip() + '%', # robust check?
                    "phone": re.sub(r'\D', '', str(row['phone_number']))
                }).fetchone()
                
                if dup:
                    validation_status = "DUPLICATE"
                    duplicate_reason = "Exact match in clean data"

            updates.append({
                "id": row['id'],
                "validation_status": validation_status,
                "missing_fields": ",".join(missing_fields) if missing_fields else None,
                "invalid_format_fields": ",".join(invalid_format_fields) if invalid_format_fields else None,
                "duplicate_reason": duplicate_reason,
                "processed_at": time.strftime('%Y-%m-%d %H:%M:%S')
            })

    # Bulk update
    if updates:
        try:
            with engine.begin() as conn:
                # We use individual updates or a case statement. SQLAlchemy `update` with list of dicts is efficient if driver supports executemany.
                # But detailed updates with different statuses might be complex for single query.
                # Let's use loop for safety and simplicity, wrapped in transaction.
                for update_data in updates:
                    conn.execute(text("""
                        UPDATE validation_raw_google_map 
                        SET validation_status = :validation_status,
                            missing_fields = :missing_fields,
                            invalid_format_fields = :invalid_format_fields,
                            duplicate_reason = :duplicate_reason,
                            processed_at = :processed_at
                        WHERE id = :id
                    """), update_data)
            logger.info(f"🔍 [VALIDATION] Phase 2 Complete. Rows processed: {len(updates)}")
        except Exception as e:
            logger.error(f"🔍 [VALIDATION] Phase 2 Update Failed: {e}")
            raise

def run_cleaning():
    """Phase 3: Cleaning Engine"""
    logger.info("🧹 [CLEANING] Starting Phase 3 — Processing STRUCTURED rows...")
    
    try:
        df = pd.read_sql("""
            SELECT * FROM validation_raw_google_map 
            WHERE validation_status = 'STRUCTURED' AND cleaning_status = 'NOT_STARTED' 
            LIMIT %s
        """ % BATCH_SIZE, engine)
    except Exception as e:
        logger.error(f"🧹 [CLEANING] Failed to fetch rows for cleaning: {e}")
        return
    
    if df.empty:
        logger.info("🧹 [CLEANING] No data to clean.")
        return
        
    cleaned_rows = []
    validation_ids_to_update = []

    for index, row in df.iterrows():
        # Clean data
        website = str(row['website']).lower().strip() if row['website'] else None
        if website and not (website.startswith('http://') or website.startswith('https://')):
             website = 'https://' + website
             
        phone = re.sub(r'\D', '', str(row['phone_number']))

        clean_row = {
            "raw_id": row['raw_id'],
            "name": str(row['name']).strip(),
            "address": str(row['address']).strip(),
            "website": website,
            "phone_number": phone,
            "reviews_count": row['reviews_count'],
            "reviews_avg": row['reviews_avg'],
            "category": row['category'],
            "subcategory": row['subcategory'],
            "city": row['city'],
            "state": row['state'],
            "area": row['area'],
            "created_at": row['created_at'] # Preserve created_at
        }
        
        cleaned_rows.append(clean_row)
        validation_ids_to_update.append(row['id'])

    if cleaned_rows:
        try:
            with engine.begin() as conn:
                # Insert into clean table
                # We do row by row or multi-row insert.
                # INSERT IGNORE to prevent duplicates
                for row in cleaned_rows:
                    conn.execute(text("""
                        INSERT IGNORE INTO raw_clean_google_map_data (
                            raw_id, name, address, website, phone_number, reviews_count, reviews_avg,
                            category, subcategory, city, state, area, created_at
                        ) VALUES (
                            :raw_id, :name, :address, :website, :phone_number, :reviews_count, :reviews_avg,
                            :category, :subcategory, :city, :state, :area, :created_at
                        )
                    """), row)
                
                # Update validation table status
                # We can do this in one go
                if validation_ids_to_update:
                    # chunking updates if needed, but for 5000 it's fine
                     conn.execute(text(f"""
                        UPDATE validation_raw_google_map 
                        SET cleaning_status = 'CLEANED' 
                        WHERE id IN ({','.join(map(str, validation_ids_to_update))})
                    """))
                    
            logger.info(f"🧹 [CLEANING] Phase 3 Complete. Rows processed: {len(cleaned_rows)}")
        except Exception as e:
            logger.error(f"🧹 [CLEANING] Phase 3 Failed: {e}")
            raise

def run_full_pipeline():
    logger.info("🚀 ====== ETL PIPELINE STARTED ======")
    try:
        run_ingestion()
        run_validation()
        run_cleaning()
        logger.info("✅ ====== ETL PIPELINE CYCLE FINISHED ======")
    except Exception as e:
        logger.critical(f"🔥 ====== ETL PIPELINE CRASH: {e} ======")

if __name__ == "__main__":
    run_full_pipeline()
