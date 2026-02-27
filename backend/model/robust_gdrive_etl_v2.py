import os
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

load_dotenv()

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s')
logger = logging.getLogger("GDriveETLv4")

# Suppress noisy Google API warnings
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore", message="file_cache is only supported with oauth2client<4.0.0")

# Configuration Constants
# Fix 6: Move ROOT_FOLDER_ID to environment variable
ROOT_FOLDER_ID = os.getenv('GDRIVE_ROOT_FOLDER_ID', '1ltTYjekxZsk2CdF20tSk1B2FnRn4119E')
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'honey-bee-digital-d96daf6e6faf.json')
# DB Config
DB_USER = os.getenv('DB_USER')
DB_PASS = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', '3306')
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class GDriveHighSpeedIngestor:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly'])
        # Producer uses a standard pool since it's threaded, not gevent
        self.engine = create_engine(DATABASE_URI, pool_size=35, max_overflow=25, pool_pre_ping=True, pool_recycle=3600, isolation_level="READ COMMITTED")
        self.table_name = "raw_google_map_drive_data"
        self.task_queue = queue.Queue(maxsize=100)
        self.folder_registry = {}  # Changed to Dict {folder_id: modified_time}
        self.processed_files = {}  # Fix 8: Dict {file_id: file_hash} instead of set
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
        """Load already processed file IDs + hashes, folder timestamps."""
        logger.info("Loading Registry Checkpoints...")
        with self.engine.connect() as conn:
            # Fix 8: Load file hashes for change detection
            files = conn.execute(text("SELECT drive_file_id, file_hash FROM file_registry"))
            self.processed_files = {row[0]: row[1] for row in files}
            
            # Load Folder Registry (ID -> ModifiedTime)
            folders = conn.execute(text("SELECT folder_id, drive_modified_at FROM drive_folder_registry"))
            self.folder_registry = {row[0]: row[1] for row in folders}
            
            # Load Token
            res = conn.execute(text("SELECT meta_value FROM etl_metadata WHERE meta_key='last_change_token'"))
            row = res.fetchone()
            if row: self.page_token = row[0] if row else None

        logger.info(f"Registry loaded: {len(self.processed_files)} files, {len(self.folder_registry)} folders.")

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

    def scanner_producer(self, folder_id, folder_name, path=""):
        if self.shutdown_event.is_set(): return
        
        # Check if folder is already fully processed in db
        recorded_mod = self.folder_registry.get(folder_id)
        # If it exists, SKIP the folder entirely to prevent re-scanning 125,000 files
        if recorded_mod:
            logger.debug(f"⏭ SKIPPING Folder: {folder_name} (Already indexed)")
            with self.stats_lock:
                self.total_skipped_folders += 1
            return
            
        # 1. Fetch items
        items = self.list_files(folder_id)
        
        folder_skipped = 0
        folder_dispatched = 0
        
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Recursive Scan with Cache Check
                # If folder is in registry and modification time matches, we can skip deep scan
                # BUT: GDrive folders don't always update mod_time when children change. 
                # So we verify strictly.
                
                self.scanner_producer(item['id'], item['name'], f"{path}/{folder_name}")
            
            elif item['name'].lower().endswith('.csv'):
                # Fix 8: Hash-based change detection
                current_hash = self.get_file_hash(item['id'], item.get('modifiedTime', ''))
                existing_hash = self.processed_files.get(item['id'])
                
                if existing_hash and existing_hash == current_hash:
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
                if existing_hash:
                    logger.debug(f"[RE-DISPATCH] {item['name']} (hash changed)")
                else:
                    logger.debug(f"[DISPATCH] {item['name']}")
                
        # Log Summary for this folder
        if folder_dispatched > 0:
            logger.debug(f"📂 [SCANNED] {folder_name}: {folder_dispatched} new tasks, {folder_skipped} skipped.")
            
        with self.stats_lock:
            self.total_scanned_folders += 1
            self.total_dispatched_files += folder_dispatched
            
            # Periodic Heartbeat (Every 200 folders)
            total_processed = self.total_scanned_folders + self.total_skipped_folders
            if total_processed % 200 == 0:
                logger.info(f"⏳ [PROGRESS] Scanned {self.total_scanned_folders} | Skipped {self.total_skipped_folders} | Dispatched {self.total_dispatched_files} files...")
            
        # Update folder state (Legacy logic, keeping it for now)
        mod_time = datetime.utcnow().isoformat() + "Z"
        if items:
            mod_time = items[0].get('modifiedTime', mod_time)
        self.register_folder(folder_id, folder_name, mod_time, 0)

    # REMOVED: download_csv, worker_consumer, process_file, commit_batch
    # These are now handled by Celery in tasks/gdrive_task/etl_tasks.py

    def run_pipeline(self):
        start_time = time.time()
        self.load_registry()
        
        logger.info("="*60)
        logger.info(f"📊 [STARTUP SUMMARY]")
        logger.info(f"   - Processed Files in DB: {len(self.processed_files)}")
        logger.info(f"   - Registered Folders:    {len(self.folder_registry)}")
        logger.info("="*60)
        
        self.scanners_finished.clear()
        
        # Reset Stats for new run
        with self.stats_lock:
            self.total_scanned_folders = 0
            self.total_skipped_folders = 0
            self.total_dispatched_files = 0
            
        # 1. INITIAL FULL SCAN (Only on first start)
        if self.first_run:
            # Reset Celery Aggregated Counters in Redis ONLY on first startup
            try:
                r = redis.Redis(host='localhost', port=6379, db=0)
                r.set('celery_files_processed', 0)
                r.set('celery_rows_inserted', 0)
                logger.info("🔄 Redis Counters Reset (files & rows)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to reset Redis counters: {e}")

            logger.info("🎬 Initializing GDrive Orchestrator v6.0 (Celery Mode)...")
            top_folders = [f for f in self.list_files(ROOT_FOLDER_ID) if f['mimeType'] == 'application/vnd.google-apps.folder']
            
            # We still use a ThreadPool for SCANNING (iterating folders), but not for processing
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(self.scanner_producer, f['id'], f['name'], "ROOT") for f in top_folders]
                for f in as_completed(futures): pass
                self.scanners_finished.set()
            
            # Removed redundant Producer-side stats refresh (handled by Celery now)
            self.first_run = False
            self.save_change_token(self.page_token)
            logger.info("="*60)
            logger.info(f"✅ Initial Scan Complete in {time.time() - start_time:.2f}s")
            logger.info(f"   - Total Folders Scanned: {self.total_scanned_folders}")
            logger.info(f"   - Total Folders Skipped: {self.total_skipped_folders}")
            logger.info(f"   - Total Files Dispatched: {self.total_dispatched_files}")
            logger.info("="*60)
            return

        # 2. REACTIVE TARGETED SYNC
        changes = self.get_changes()
        if not changes:
            logger.info("⚡ System Idle... No new changes detected.")
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
                if file['id'] not in self.processed_files:
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
                for f in folders_to_scan:
                    executor.submit(self.scanner_producer, f['id'], f['name'], "REACTIVE")
            
        self.save_change_token(self.page_token)
        logger.info(f"✨ Reactive Cycle dispatched in {time.time() - start_time:.2f}s")

