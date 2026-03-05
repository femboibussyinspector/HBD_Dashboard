import os
import threading
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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ForceProcess")

load_dotenv()

db_pass = getattr(config, "DB_PASSWORD", "")
# db_pass = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_pass}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(config.DATABASE_URI)

from model.robust_gdrive_etl_v2 import ValidationCleaningProcessor

def run():
    shutdown_event = threading.Event()
    processor = ValidationCleaningProcessor(engine, shutdown_event)
    
    # Process the gap
    start_id = 97052
    end_id = 100000 # Let's try a small chunk first
    
    print(f"Processing range {start_id} to {end_id}...")
    try:
        processor.process_range(start_id, end_id)
        print("Success!")
    except Exception as e:
        print(f"Failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()
