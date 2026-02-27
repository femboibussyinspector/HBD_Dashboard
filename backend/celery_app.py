from gevent import monkey
monkey.patch_all()

import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import pathlib
import logging
import os
import logging
import redis
import requests
from celery import Celery
from celery.signals import worker_ready, setup_logging

import re
# ... (rest of imports)

celery = Celery("tasks")

# Custom Formatter to strip ANSI codes and format consistently
class LogFormatter(logging.Formatter):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def format(self, record):
        record_copy = logging.makeLogRecord(record.__dict__)
        if isinstance(record_copy.msg, str):
            record_copy.msg = self.ansi_escape.sub('', record_copy.msg)
        record_copy.levelname = f"{record_copy.levelname:<8}"
        return super().format(record_copy)

# SECTION: Logging Configuration via Signal
# This ensures Celery doesn't override our logging config
@setup_logging.connect
def setup_celery_logging(**kwargs):
    # Setup logging to file (rotates daily)
    log_dir = pathlib.Path(__file__).parent / 'logs' / 'celery'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_filename = log_dir / f"celery_{datetime.now().strftime('%Y-%m-%d')}.log"

    # Define format: Date Time | Level | Logger | Message
    log_format = '%(asctime)s | %(levelname)s | %(name)-15s : %(message)s'

    file_handler = TimedRotatingFileHandler(str(log_filename), when='midnight', backupCount=14, encoding='utf-8')
    file_formatter = LogFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging.INFO)

    # Attach handlers to root logger to capture ALL logs (including libraries)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [] # Clear existing handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
    
    # Explicitly setup celery specific loggers to propagate to root
    logging.getLogger('celery').setLevel(logging.INFO)
    logging.getLogger('celery').propagate = True
    
    # Silence Noisy Celery Internal Loggers
    # "Task received" logs come from here -> Set to WARNING to hide them
    logging.getLogger('celery.worker.strategy').setLevel(logging.WARNING) 
    # "Mingle: searching for neighbors" -> Set to WARNING
    logging.getLogger('celery.worker.consumer.mingle').setLevel(logging.WARNING)
    logging.getLogger('celery.worker.gossip').setLevel(logging.WARNING)
    logging.getLogger('celery.worker.control').setLevel(logging.WARNING)
    
    # Silence 'Task succeeded' default log
    logging.getLogger('celery.app.trace').setLevel(logging.WARNING)

# SECTION 2: Celery Worker — Full Optimized Config
celery.conf.update(
    broker_url = os.getenv("CELERY_BROKER_URL"),
    result_backend = os.getenv("CELERY_RESULT_BACKEND"),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Optimizations:
    worker_prefetch_multiplier=1,      # Prevent worker from hoarding tasks (fair distribution)
    task_acks_late=True,               # Only ack after successful return (reliability)
    task_reject_on_worker_lost=True,   # Re-queue task if worker crashes
    result_expires=86400,              # Expire results after 24h to save Redis RAM
)

# SECTION 6: Periodic Stats Refresh Schedule
celery.conf.beat_schedule = {
    'refresh-stats-every-5-mins': {
        'task': 'tasks.gdrive.refresh_stats',
        'schedule': 300.0,
    },
}

celery.autodiscover_tasks(["tasks"])

import tasks.listings_task.upload_asklaila_task
import tasks.listings_task.upload_atm_task
import tasks.listings_task.upload_bank_task
import tasks.listings_task.upload_college_dunia_task
import tasks.listings_task.upload_freelisting_task
import tasks.listings_task.upload_google_map_scrape_task
import tasks.listings_task.upload_google_map_task
import tasks.listings_task.upload_heyplaces_task
import tasks.listings_task.upload_justdial_task
import tasks.listings_task.upload_magicpin_task
import tasks.listings_task.upload_nearbuy_task
import tasks.listings_task.upload_pinda_task
import tasks.listings_task.upload_post_office_task
import tasks.listings_task.upload_schoolgis_task
import tasks.listings_task.upload_yellow_pages_task
import tasks.listings_task.upload_shiksha_task
import tasks.products_task.upload_amazon_products_task
import tasks.products_task.upload_big_basket_task
import tasks.gdrive_task.etl_tasks
import tasks.deep_scraper_task


# SECTION 8: Prometheus Metrics Server (starts with worker)
@worker_ready.connect
def start_metrics_on_worker_ready(**kwargs):
    """Start Prometheus metrics endpoint when the Celery worker boots."""
    try:
        from utils.metrics import start_metrics_server
        start_metrics_server()
    except Exception as e:
        logging.warning(f"Could not start Prometheus metrics server: {e}")


# SECTION 7: Queue Backlog Monitor
def check_queue_health():
    """
    Checks the default Celery queue length dynamically.
    Returns: int (queue length)
    """
    try:
        broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        r = redis.from_url(broker_url)
        
        # Dynamic queue name detection
        default_queue = celery.conf.task_default_queue or 'celery'
        
        length = r.llen(default_queue)
        
        if length > 100:
            logging.warning(f"[ALERT] High Queue Depth: {length} pending tasks in '{default_queue}'!")
            
            # Slack Webhook Integration (set SLACK_WEBHOOK_URL in .env)
            slack_url = os.getenv('SLACK_WEBHOOK_URL')
            if slack_url:
                try:
                    requests.post(slack_url, json={"text": f"Queue Alert: {length} tasks pending!"}, timeout=5)
                except Exception:
                    pass
                
        return int(length)
    except Exception as e:
        logging.warning(f"Failed to check queue health: {e}")
        return 0