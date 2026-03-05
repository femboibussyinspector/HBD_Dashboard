import os
import threading
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import sys
import os
# Ensure config.py is importable
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) if 'model' in os.path.dirname(__file__) or 'database' in os.path.dirname(__file__) else os.path.abspath(os.path.dirname(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
from config import config

load_dotenv(r'd:\Honeybee digital\Dashboard latest\backend\.env')
db_pass = getattr(config, "DB_PASSWORD", "")
# db_pass = quote_plus(os.getenv('DB_PASSWORD_PLAIN') or "")  # REFACTORED: Now using config.py
DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_pass}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(config.DATABASE_URI)

from model.robust_gdrive_etl_v2 import ValidationQualityProcessor
import logging
logging.basicConfig(level=logging.DEBUG)

shutdown_event = threading.Event()
validator = ValidationQualityProcessor(engine, shutdown_event)
validator.batch_size = 20000

def run_once():
    validator.start_pipeline()

t = threading.Thread(target=run_once)
t.start()
import time
time.sleep(15)
shutdown_event.set()
t.join()
