import os
import re
import io
import csv
import time
import random
import hashlib
import logging
import threading
import queue
import redis
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv

from .normalizer import UniversalNormalizer
from utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError
from config import config

load_dotenv()

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s')
logger = logging.getLogger("GDriveETLv4")

# Suppress noisy Google API warnings
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore", message="file_cache is only supported with oauth2client<4.0.0")

# Configuration Constants
ROOT_FOLDER_ID = os.getenv('GDRIVE_ROOT_FOLDER_ID', '1ltTYjekxZsk2CdF20tSk1B2FnRn4119E')
SERVICE_ACCOUNT_FILE = config.SERVICE_ACCOUNT_FILE
DATABASE_URI = config.DATABASE_URI

class GDriveHighSpeedIngestor:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly'])
        # Producer uses a standard pool since it's threaded, not gevent
        # Reduced pool size to save memory on 3.5GB systems
        self.engine = create_engine(DATABASE_URI, pool_size=10, max_overflow=5, pool_pre_ping=True, pool_recycle=1800, pool_timeout=30, isolation_level="READ COMMITTED")
        self.table_name = "raw_google_map_drive_data"
        self.task_queue = queue.Queue(maxsize=100)
        self.folder_registry = {}  # Changed to Dict {folder_id: modified_time}
        self.shutdown_event = threading.Event()
        self.scanners_finished = threading.Event()
        self._tls = threading.local()
        self.first_run = True  # Track if we need an initial full scan
        self.page_token = None
        # Circuit breaker for Google Drive API calls
        self.api_breaker = CircuitBreaker(name="gdrive_api")
        
        # Stats & Heartbeat
        self.stats_lock = threading.Lock()
        self.total_scanned_folders = 0
        self.total_skipped_folders = 0
        self.total_dispatched_files = 0

    def shutdown(self):
        """Signal the ingestor to stop."""
        self.shutdown_event.set()

    def get_service(self):
        if not hasattr(self._tls, 'service'):
            self._tls.service = build('drive', 'v3', credentials=self.creds, cache_discovery=False)
        return self._tls.service

    def retry_on_429(func):
        def wrapper(*args, **kwargs):
            for attempt in range(5):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if '429' in str(e) or 'rate limit' in str(e).lower():
                        wait = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Rate limited. Retrying in {wait:.2f}s...")
                        time.sleep(wait)
                    else: raise
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def get_file_hash(file_id, modified_time):
        """Generate a hash for file change detection."""
        return hashlib.md5(f"{file_id}:{modified_time}".encode()).hexdigest()

    def load_registry(self):
        """Load folder timestamps from the database. File tracking is now stateless."""
        logger.debug("Loading Folder Registry Checkpoints...")
        with self.engine.connect() as conn:

            # Load Folder Registry (ID -> ModifiedTime)
            folders = conn.execute(text("SELECT folder_id, drive_modified_at FROM drive_folder_registry"))
            self.folder_registry = {row[0]: row[1] for row in folders}
            
            # Query for processed files count
            try:
                self.files_processed_count = conn.execute(text("SELECT COUNT(*) FROM file_registry WHERE status = 'PROCESSED'")).scalar()
            except Exception:
                self.files_processed_count = 0
                
            # Query for processed folders count
            try:
                self.folders_processed_count = conn.execute(text("SELECT COUNT(DISTINCT drive_folder_id) FROM file_registry WHERE status = 'PROCESSED' AND drive_folder_id IS NOT NULL")).scalar()
            except Exception:
                self.folders_processed_count = 0

            
            # Load Token
            res = conn.execute(text("SELECT meta_value FROM etl_metadata WHERE meta_key='last_change_token'"))
            row = res.fetchone()
            if row: self.page_token = row[0] if row else None

        logger.debug(f"Registry loaded: {len(self.folder_registry)} folders, {self.files_processed_count} files processed.")

    def save_change_token(self, token):
        with self.engine.begin() as conn:
            conn.execute(text("INSERT INTO etl_metadata (meta_key, meta_value) VALUES ('last_change_token', :token) ON DUPLICATE KEY UPDATE meta_value = :token"), {"token": token})

    def get_changes(self):
        """Fetch all pending changes from Google Drive since last token."""
        service = self.get_service()
        if not self.page_token:
            token_res = service.changes().getStartPageToken().execute()
            self.page_token = token_res.get('startPageToken')
            self.save_change_token(self.page_token)
            return []

        try:
            all_changes = []
            current_token = self.page_token
            while True:
                response = service.changes().list(
                    pageToken=current_token, 
                    spaces='drive', 
                    pageSize=100,
                    fields="nextPageToken, newStartPageToken, changes(fileId, removed, file(id, name, mimeType, parents, modifiedTime))"
                ).execute()
                all_changes.extend(response.get('changes', []))
                if 'nextPageToken' in response:
                    current_token = response['nextPageToken']
                else:
                    self.page_token = response.get('newStartPageToken') or current_token
                    break
            
            return all_changes
        except Exception as e:
            logger.warning(f"Changes API error: {e}. Token might be expired.")
            token_res = service.changes().getStartPageToken().execute()
            self.page_token = token_res.get('startPageToken')
            self.save_change_token(self.page_token)
            return []

    def register_folder(self, folder_id, folder_name, modified_at, csv_count=0):
        try:
            with self.engine.begin() as conn:
                sql = text("""
                    INSERT INTO drive_folder_registry (folder_id, folder_name, drive_modified_at, csv_count, status, scanned_at) 
                    VALUES (:id, :name, :mod, :count, 'DONE', NOW()) 
                    ON DUPLICATE KEY UPDATE 
                        drive_modified_at=VALUES(drive_modified_at), 
                        csv_count=VALUES(csv_count), 
                        status='DONE',
                        scanned_at=NOW()
                """)
                conn.execute(sql, {"id": folder_id, "name": folder_name, "mod": modified_at, "count": csv_count})
            
            # Update In-Memory Cache
            self.folder_registry[folder_id] = modified_at
        except Exception as e:
            logger.error(f"Failed to register folder {folder_name}: {e}")

    @retry_on_429
    def list_files(self, parent_id):
        # Circuit breaker + rate limit protected API call
        def _list():
            return self.get_service().files().list(
                q=f"'{parent_id}' in parents and trashed=false", 
                fields="files(id, name, mimeType, modifiedTime)",
                orderBy="modifiedTime desc",
                pageSize=1000 
            ).execute().get('files', [])
        try:
            return self.api_breaker.call(_list)
        except CircuitBreakerOpenError as e:
            logger.warning(f"Circuit breaker OPEN, skipping list_files for {parent_id}: {e}")
            return []

    def has_file_changed(self, file_id, current_hash):
        """Stateless DB-backed check to see if a file needs processing."""
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT file_hash, status FROM file_registry WHERE drive_file_id = :id"), {"id": file_id}).fetchone()
            if result:
                # Processed successfully and hash hasn't changed = SKIP
                if result[1] == 'PROCESSED' and result[0] == current_hash:
                    return False
            # Needs processing
            return True

    def scanner_producer(self, folder_id, folder_name, path=""):
        if self.shutdown_event.is_set(): return
        
        # Check if folder is already fully processed in db
        recorded_mod = self.folder_registry.get(folder_id)
        # If it exists, SKIP the folder entirely to prevent re-scanning 125,000 files
        if recorded_mod:
            logger.debug(f"⏭ SKIPPING Folder: {folder_name} (Already indexed)")
            return
            
        # 1. Fetch items
        items = self.list_files(folder_id)
        
        # Separate Folders and Files to guarantee processing order
        folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
        csv_files = [item for item in items if item['name'].lower().endswith('.csv')]
        
        # Process NEWEST CSV FILES first
        folder_skipped = 0
        folder_dispatched = 0
        
        for item in csv_files:
            if self.shutdown_event.is_set(): break
            
            # Stateless change detection
            current_hash = self.get_file_hash(item['id'], item.get('modifiedTime', ''))
            
            if not self.has_file_changed(item['id'], current_hash):
                folder_skipped += 1
                continue
                
            # New or modified file -> Dispatch
            from tasks.gdrive_task.etl_tasks import process_csv_task
            process_csv_task.delay(
                file_id=item['id'], 
                file_name=item['name'],
                folder_id=folder_id, 
                folder_name=folder_name,
                path=f"{path}/{folder_name}", 
                modified_time=item.get('modifiedTime')
            )
            folder_dispatched += 1
            logger.debug(f"[DISPATCH] {item['name']}")

        # Then recursively scan NEWEST SUBFOLDERS (Phase 2)
        for folder in folders:
            if self.shutdown_event.is_set(): break
            self.scanner_producer(folder['id'], folder['name'], f"{path}/{folder_name}")
                
        # Log Summary for this folder
        if folder_dispatched > 0:
            logger.debug(f"📂 [SCANNED] {folder_name}: {folder_dispatched} new tasks, {folder_skipped} skipped.")
            
        with self.stats_lock:
            self.total_scanned_folders += 1
            self.total_dispatched_files += folder_dispatched
            
        # Register folder scan as done
        mod_time = items[0].get('modifiedTime') if items else datetime.utcnow().isoformat() + "Z"
        if 'T' in mod_time: 
            mod_time = mod_time.replace('T', ' ').replace('Z', '').split('.')[0]
        self.register_folder(folder_id, folder_name, mod_time, len(csv_files))

    # REMOVED: download_csv, worker_consumer, process_file, commit_batch
    # These are now handled by Celery in tasks/gdrive_task/etl_tasks.py

    def run_pipeline(self):
        start_time = time.time()
        self.load_registry()
        
        processed_f = getattr(self, 'folders_processed_count', 0)
        remaining_f = len(self.folder_registry) - processed_f
        
        if self.first_run:
            logger.info("="*60)
            logger.info(f"📊 [STARTUP SUMMARY]")
            logger.info(f"   - Registered Folders:    {len(self.folder_registry)}")
            logger.info(f"   - Processed Folders:     {processed_f}")
            logger.info(f"   - Remaining Folders:     {remaining_f}")
            logger.info(f"   - Files Processed:       {getattr(self, 'files_processed_count', 0)}")
            logger.info("="*60)
        else:
            logger.debug("="*60)
            logger.debug(f"📊 [CYCLE SUMMARY]")
            logger.debug(f"   - Registered Folders:    {len(self.folder_registry)}")
            logger.debug(f"   - Processed Folders:     {processed_f}")
            logger.debug(f"   - Remaining Folders:     {remaining_f}")
            logger.debug(f"   - Files Processed:       {getattr(self, 'files_processed_count', 0)}")
            logger.debug("="*60)
        
        self.scanners_finished.clear()
        
        # Reset Stats for new run
        with self.stats_lock:
            self.total_scanned_folders = 0
            self.total_dispatched_files = 0
            
        # 1. INITIAL FULL SCAN (Only on first start)
        if self.first_run:
            # Reset Celery Aggregated Counters in Redis ONLY on first startup
            try:
                r = redis.Redis(host='localhost', port=6379, db=0)
                r.set('celery_files_processed', 0)
                r.set('celery_rows_inserted', 0)
                logger.debug("🔄 Redis Counters Reset (files & rows)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to reset Redis counters: {e}")

            logger.info("🎬 Initializing GDrive Orchestrator v6.0 (Celery Mode)...")
            top_folders = [f for f in self.list_files(ROOT_FOLDER_ID) if f['mimeType'] == 'application/vnd.google-apps.folder']
            
            # Reduced workers for scanning to avoid overhead.
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(self.scanner_producer, f['id'], f['name'], "ROOT") for f in top_folders]
                for f in as_completed(futures):
                    if self.shutdown_event.is_set():
                        logger.info("Shutdown requested. Cancelling remaining scanners.")
                        break
                self.scanners_finished.set()
            
            # Removed redundant Producer-side stats refresh (handled by Celery now)
            self.first_run = False
            self.save_change_token(self.page_token)
            logger.info("="*60)
            logger.info(f"✅ Initial Scan Complete in {time.time() - start_time:.2f}s")
            logger.info(f"   - Total Folders Scanned: {self.total_scanned_folders}")
            logger.info(f"   - Total Files Dispatched: {self.total_dispatched_files}")
            logger.info("="*60)
            return

        # 2. REACTIVE TARGETED SYNC
        changes = self.get_changes()
        if not changes:
            logger.debug("⚡ System Idle... No new changes detected.")
            return

        logger.info(f"🚀 Reactive Trigger! Disptaching {len(changes)} updates to Celery...")
        
        from tasks.gdrive_task.etl_tasks import process_csv_task
        
        folders_to_scan = []

        for c in changes:
            if c.get('removed'): continue
            file = c.get('file', {})
            if not file: continue
            
            # Identify what changed
            if file.get('name', '').lower().endswith('.csv'):
                file_hash = self.get_file_hash(file['id'], file.get('modifiedTime', ''))
                if self.has_file_changed(file['id'], file_hash):
                     logger.debug(f"🆕 REACTIVE TASK: {file['name']}")
                     process_csv_task.delay(
                        file_id=file['id'], 
                        file_name=file['name'],
                        folder_id="TARGETED", 
                        folder_name="Reactive",
                        path="REACTIVE", 
                        modified_time=file.get('modifiedTime')
                     )
            elif file.get('mimeType') == 'application/vnd.google-apps.folder':
                folders_to_scan.append(file)
        
        # Deduplicate folders to prevent parallel scans of the same folder
        if folders_to_scan:
            seen_ids = set()
            unique_folders = []
            for f in folders_to_scan:
                if f['id'] not in seen_ids:
                    seen_ids.add(f['id'])
                    unique_folders.append(f)
            folders_to_scan = unique_folders
            logger.info(f"📂 Scanning {len(folders_to_scan)} unique reactive folders...")

            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(self.scanner_producer, f['id'], f['name'], "REACTIVE") for f in folders_to_scan]
                for f in as_completed(futures):
                    if self.shutdown_event.is_set():
                        break
            
        self.save_change_token(self.page_token)
        logger.info(f"✨ Reactive Cycle dispatched in {time.time() - start_time:.2f}s")

class ValidationQualityProcessor:
    """
    Continuous Validation, Cleaning & Master Sync Layer
    Processes raw_google_map_drive_data -> raw_clean_google_map_data & master_table
    Ensures zero data loss, applying robust validation, normalization, and deduplication.
    """
    def __init__(self, engine, shutdown_event):
        self.engine = engine
        self.shutdown_event = shutdown_event
        self.batch_size = 2000 # Smaller batch for stability
        self.consecutive_errors = 0
        self.max_backoff = 60  # Max sleep on consecutive errors
        # Aggregated counters for periodic summary logging
        self._agg_total = 0
        self._agg_valid = 0
        self._agg_missing = 0
        self._agg_dup = 0
        self._agg_cleaned = 0
        self._agg_batches = 0

    @staticmethod
    def safe_str(val, default=""):
        """Safe string conversion that never throws."""
        if val is None:
            return default
        try:
            s = str(val).strip()
            return default if s.lower() in ('nan', 'none', 'nat', '') else s
        except Exception:
            return default

    @staticmethod
    def safe_int(val, default=0):
        """Safe int conversion that never throws."""
        try:
            if val is None: return default
            s = str(val).strip()
            if s.lower() in ('', 'nan', 'none', 'nat'): return default
            import re as _re
            m = _re.search(r'\d+', s)
            return int(m.group()) if m else default
        except Exception:
            return default

    @staticmethod
    def safe_float(val, default=0.0):
        """Safe float conversion that never throws."""
        try:
            if val is None: return default
            s = str(val).strip()
            if s.lower() in ('', 'nan', 'none', 'nat'): return default
            import re as _re
            m = _re.search(r'[-+]?\d*\.?\d+', s)
            return float(m.group()) if m else default
        except Exception:
            return default

    def get_last_processed_id(self):
        try:
            with self.engine.connect() as conn:
                # Priority 1: Check newest log entry for last_id
                res = conn.execute(text("SELECT last_id FROM data_validation_log ORDER BY id DESC LIMIT 1"))
                row = res.fetchone()
                if row and row[0]:
                    return int(row[0])
                
                # Priority 2: Fallback to etl_metadata
                res = conn.execute(text("SELECT meta_value FROM etl_metadata WHERE meta_key='last_processed_id'"))
                row = res.fetchone()
                return int(row[0]) if row and str(row[0]).isdigit() else 0
        except Exception:
            return 0

    def update_last_processed_id(self, last_id):
        try:
            with self.engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO etl_metadata (meta_key, meta_value) 
                    VALUES ('last_processed_id', :val) 
                    ON DUPLICATE KEY UPDATE meta_value = :val
                """), {"val": str(last_id)})
        except Exception as e:
            logger.warning(f"Failed to update last_processed_id: {e}")

    def log_validation_batch(self, summary):
        try:
            with self.engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO data_validation_log 
                    (total_processed, missing_count, valid_count, duplicate_count, cleaned_count, last_id, timestamp)
                    VALUES (:total, :missing, :valid, :duplicate, :cleaned, :last_id, NOW())
                """), summary)
        except Exception as e:
            logger.warning(f"Failed to log validation batch: {e}")

    def is_missing(self, val):
        return val is None or str(val).strip() == ""

    def validate_row(self, row):
        """Validate a single row. Never throws."""
        try:
            mandatory_fields = ["name", "address", "phone_number", "city", "state", "category"]
            missing = [f for f in mandatory_fields if self.is_missing(row.get(f))]
            
            is_structured = len(missing) == 0
            invalid_fields = []
            
            # Phone: Numeric only, 8-18 digits
            raw_phone = self.safe_str(row.get('phone_number', ''))
            clean_phone = re.sub(r'\D', '', raw_phone)
            if clean_phone and not re.match(r'^\d{8,18}$', clean_phone):
                invalid_fields.append("phone_number")
            elif not clean_phone:
                if "phone_number" not in missing:
                    missing.append("phone_number")
                
            # Website: Must contain "." if present
            website = self.safe_str(row.get('website', ''))
            if website and '.' not in website:
                invalid_fields.append("website")
                
            is_valid = len(invalid_fields) == 0 and is_structured
            return is_structured, is_valid, missing, invalid_fields, clean_phone
        except Exception:
            return False, False, ["unknown"], [], ""

    def check_duplicates_batch(self, signatures, conn):
        """Batch check signatures against the clean table. Never throws."""
        if not signatures:
            return set()
        
        results = set()
        sig_list = list(signatures)
        
        for i in range(0, len(sig_list), 500):
            batch = sig_list[i:i+500]
            conditions = []
            params = {}
            for idx, (phone, name, addr, city) in enumerate(batch):
                conditions.append(f"(phone_number = :p{idx} AND LOWER(TRIM(name)) = :n{idx} AND LOWER(TRIM(COALESCE(address,''))) = :a{idx} AND LOWER(TRIM(COALESCE(city,''))) = :c{idx})")
                params[f"p{idx}"] = phone
                params[f"n{idx}"] = name
                params[f"a{idx}"] = addr
                params[f"c{idx}"] = city
            
            if not conditions:
                continue
                
            query = f"""SELECT LOWER(TRIM(name)) as n, phone_number as p, 
                              LOWER(TRIM(COALESCE(address,''))) as a, 
                              LOWER(TRIM(COALESCE(city,''))) as ct
                       FROM raw_clean_google_map_data 
                       WHERE {' OR '.join(conditions)}"""
            try:
                rows = conn.execute(text(query), params).fetchall()
                for r in rows:
                    results.add((str(r[1]), str(r[0]), str(r[2]), str(r[3])))
            except Exception as e:
                logger.warning(f"Duplicate check sub-batch failed (non-fatal): {e}")
        return results

    def start_pipeline(self):
        """Main loop for the quality assurance and master sync thread. NEVER exits on error."""
        last_id = self.get_last_processed_id()
        logger.info(f"Data Quality Processor Started from ID: {last_id}")
        
        while not self.shutdown_event.is_set():
            try:
                with self.engine.begin() as conn:
                    # READ UNCOMMITTED: prevents locking raw table during read
                    conn.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED"))
                    
                    # 1. Fetch batch from Tier 1 (Raw)
                    rows = conn.execute(text("""
                        SELECT id, name, address, website, phone_number, 
                                reviews_count, reviews_average, category, subcategory, 
                                city, state, area
                        FROM raw_google_map_drive_data 
                        WHERE id > :last_id 
                        ORDER BY id ASC 
                        LIMIT :limit
                    """), {"last_id": last_id, "limit": self.batch_size}).fetchall()
                
                    if not rows:
                        conn.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
                        self.consecutive_errors = 0  # Reset on successful idle
                        if self.shutdown_event.wait(timeout=10):
                            break
                        continue

                    batch_summary = {
                        "total": 0, "missing": 0, "valid": 0,
                        "duplicate": 0, "cleaned": 0
                    }
                    
                    current_max_id = last_id
                    clean_data_batch = []
                    master_data_batch = []
                    batch_rows = []
                    signatures = set()
                    
                    # 2. Process batch — each row is individually protected
                    for row_obj in rows:
                        try:
                            raw_row = row_obj._asdict() if hasattr(row_obj, '_asdict') else row_obj._mapping
                            norm_row = UniversalNormalizer.normalize_row_full(dict(raw_row))
                            norm_row['id'] = raw_row['id']
                            
                            # Ensure all string fields are safe
                            for key in ['name', 'address', 'website', 'phone_number', 'category', 'subcategory', 'city', 'state', 'area']:
                                norm_row[key] = self.safe_str(norm_row.get(key))
                            norm_row['reviews_count'] = self.safe_int(norm_row.get('reviews_count'))
                            norm_row['reviews_average'] = self.safe_float(norm_row.get('reviews_average'))
                            
                            batch_rows.append(norm_row)
                            current_max_id = max(current_max_id, norm_row['id'])
                            
                            sig = (norm_row['phone_number'], norm_row['name'].lower(), norm_row['address'].lower(), norm_row['city'].lower())
                            signatures.add(sig)
                        except Exception as row_err:
                            # Skip bad row, advance cursor past it
                            try:
                                current_max_id = max(current_max_id, raw_row['id'])
                            except Exception:
                                pass
                            logger.warning(f"Row normalization failed (skipping): {str(row_err)[:100]}")
                            continue

                    # Bulk Duplicate Check
                    existing_sigs = self.check_duplicates_batch(signatures, conn)
                    
                    # Switch back to safe mode for writes
                    conn.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ"))

                    for row in batch_rows:
                        try:
                            batch_summary["total"] += 1
                            
                            is_structured, is_valid, missing_list, invalid_list, clean_phone = self.validate_row(row)
                            
                            sig = (row['phone_number'], row['name'].lower(), row['address'].lower(), row['city'].lower())
                            is_duplicate = sig in existing_sigs if is_structured else False

                            status = "VALID"
                            if not is_structured: 
                                status = "MISSING"
                                batch_summary["missing"] += 1
                            elif is_duplicate: 
                                status = "DUPLICATE"
                                batch_summary["duplicate"] += 1
                            elif not is_valid: 
                                status = "INVALID"
                            else:
                                batch_summary["valid"] += 1

                            if status in ["VALID", "MISSING", "INVALID", "DUPLICATE"]:
                                created_at = row.get('created_at')
                                if not created_at:
                                    created_at = datetime.now()
                                
                                clean_data_batch.append({
                                    "raw_id": row['id'], "name": row['name'], "address": row['address'],
                                    "website": row['website'], "phone": row['phone_number'], 
                                    "reviews": self.safe_int(row.get('reviews_count', 0)),
                                    "avg": self.safe_float(row.get('reviews_average', 0.00)),
                                    "cat": row['category'], "sub": row['subcategory'], "city": row['city'],
                                    "state": row['state'], "area": row['area'], "created": created_at,
                                    "val_status": status, 
                                    "clean_status": "CLEANED" if status == "VALID" else "FAILED_VALIDATION" if status != "DUPLICATE" else "DUPLICATE_FOUND", 
                                    "missing": ",".join(missing_list) if missing_list else None, 
                                    "invalid": ",".join(invalid_list) if invalid_list else None, 
                                    "duplicate_reason": "Exact match (Phone, Name, Address, City)" if status == "DUPLICATE" else None, 
                                    "processed_at": datetime.now()
                                })
                                
                                if status == "VALID":
                                    master_data_batch.append({
                                        "name": row['name'],
                                        "address": row['address'],
                                        "website": row['website'],
                                        "phone_number": row['phone_number'],
                                        "reviews_count": self.safe_int(row.get('reviews_count', 0)),
                                        "reviews_avg": self.safe_float(row.get('reviews_average', 0.00)),
                                        "category": row['category'],
                                        "subcategory": row['subcategory'],
                                        "city": row['city'],
                                        "state": row['state'],
                                        "area": row['area'],
                                        "created_at": created_at
                                    })
                                    batch_summary["cleaned"] += 1
                        except Exception as row_err:
                            logger.warning(f"Row validation failed (skipping): {str(row_err)[:100]}")
                            continue

                    # 4. Execute Batch Writes — each INSERT is individually protected
                    if clean_data_batch:
                        try:
                            conn.execute(text("""
                                INSERT IGNORE INTO validation_raw_google_map 
                                (raw_id, name, address, website, phone_number, reviews_count, reviews_avg,
                                 category, subcategory, city, state, area, created_at,
                                 validation_status, cleaning_status, missing_fields, invalid_format_fields, duplicate_reason, processed_at)
                                VALUES (:raw_id, :name, :address, :website, :phone, :reviews, :avg, :cat, :sub, :city, :state, :area, :created,
                                        :val_status, :clean_status, :missing, :invalid, :duplicate_reason, :processed_at)
                            """), clean_data_batch)
                        except Exception as e:
                            logger.warning(f"Clean table batch insert failed (non-fatal): {str(e)[:200]}")
                        
                    if master_data_batch:
                        try:
                            conn.execute(text("""
                                INSERT IGNORE INTO g_map_master_table 
                                (name, address, website, phone_number, reviews_count, reviews_avg, category, subcategory, city, state, area, created_at)
                                VALUES (:name, :address, :website, :phone_number, :reviews_count, :reviews_avg, :category, :subcategory, :city, :state, :area, :created_at)
                            """), master_data_batch)
                        except Exception as e:
                            logger.warning(f"Master table batch insert failed (non-fatal): {str(e)[:200]}")

                # 5. Finalize batch — ALWAYS advance the cursor
                batch_summary['last_id'] = current_max_id
                self.update_last_processed_id(current_max_id)
                self.log_validation_batch(batch_summary)
                last_id = current_max_id
                self.consecutive_errors = 0  # Reset on success
                
                # Aggregate counters for periodic summary
                self._agg_total += batch_summary['total']
                self._agg_valid += batch_summary['valid']
                self._agg_missing += batch_summary['missing']
                self._agg_dup += batch_summary['duplicate']
                self._agg_cleaned += batch_summary['cleaned']
                self._agg_batches += 1
                
                # Per-batch detail goes to DEBUG (log file only)
                logger.debug(f"Quality Cycle Complete: Processed {batch_summary['total']} | Valid: {batch_summary['valid']} | Missing: {batch_summary['missing']} | Dup: {batch_summary['duplicate']} | Master: {batch_summary['cleaned']} | Last ID: {last_id}")
                
                # Print summary to console every 50 batches (~100K rows)
                if self._agg_batches % 50 == 0:
                    logger.info(f"⚡ Validation Progress: {self._agg_total:,} rows | Valid: {self._agg_valid:,} | Missing: {self._agg_missing:,} | Dup: {self._agg_dup:,} | Master: {self._agg_cleaned:,} | Last ID: {last_id}")

            except Exception as e:
                self.consecutive_errors += 1
                backoff = min(self.consecutive_errors * 5, self.max_backoff)
                msg = str(e)
                if "[parameters:" in msg:
                    msg = msg.split("[parameters:")[0] + " [Params hidden]"
                logger.warning(f"Validation Loop Error (retry in {backoff}s, attempt #{self.consecutive_errors}): {msg[:200]}")
                if self.shutdown_event.wait(timeout=backoff):
                    break

def get_engine():
    return GDriveHighSpeedIngestor()

def start_background_etl():
    """Started by app.py to orchestrate the scanning."""
    ingestor = get_engine()
    
    # Start Drive Scanner Thread
    def scanner_loop():
        while not ingestor.shutdown_event.is_set():
            try:
                ingestor.run_pipeline()
                logger.info("Scanner sleeping for 30s...")
                if ingestor.shutdown_event.wait(timeout=30):
                    break
            except Exception as e:
                logger.error(f"Scanner Loop error: {e}")
                time.sleep(10)
    
    t_scanner = threading.Thread(target=scanner_loop, name="ScannerThread", daemon=True)
    t_scanner.start()

    # Start Validation & Cleaning Thread
    validator = ValidationQualityProcessor(ingestor.engine, ingestor.shutdown_event)
    t_validator = threading.Thread(target=validator.start_pipeline, name="QualityThread", daemon=True)
    t_validator.start()

    return ingestor

if __name__ == "__main__":
    start_background_etl()
    while True: time.sleep(1)
