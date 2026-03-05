import signal
import time
import logging
import threading
from logging.handlers import TimedRotatingFileHandler
import pathlib
from datetime import datetime

from model.robust_gdrive_etl_v2 import GDriveHighSpeedIngestor, ValidationQualityProcessor

# Set up Log Directory
log_dir = pathlib.Path(__file__).parent / 'logs' / 'ingestor'
log_dir.mkdir(parents=True, exist_ok=True)
log_filename = log_dir / f"ingestor_{datetime.now().strftime('%Y-%m-%d')}.log"

# Define Formatters
log_format = '%(asctime)s | %(levelname)-8s | [%(name)s] : %(message)s'
formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

# File Handler (Rotates daily, keeps 14 days of backups)
file_handler = TimedRotatingFileHandler(str(log_filename), when='midnight', backupCount=14, encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Console Handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

# Root Logger Config
logger = logging.getLogger("GDriveETLWorker")
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
# Apply same format to the internal library logger
internal_logger = logging.getLogger("GDriveETLv4")
if not internal_logger.hasHandlers():
    internal_logger.setLevel(logging.INFO)
    internal_logger.addHandler(file_handler)
    internal_logger.addHandler(stream_handler)


def main() -> None:
    """
    Standalone worker entrypoint for the GDrive ETL engine.
    Runs a single ingestor loop in this process only.
    """
    ingestor = GDriveHighSpeedIngestor()

    def _handle_shutdown(signum, frame):
        logger.info("Shutdown signal received (%s). Stopping ETL loop...", signum)
        ingestor.shutdown()

    try:
        signal.signal(signal.SIGINT, _handle_shutdown)
        signal.signal(signal.SIGTERM, _handle_shutdown)
    except (ValueError, OSError):
        # Signals might not be available on all platforms/contexts
        pass

    logger.info("Starting GDrive ETL worker loop.")

    # Start the Validation & Quality Pipeline in a background thread
    validator = ValidationQualityProcessor(ingestor.engine, ingestor.shutdown_event)
    validator_thread = threading.Thread(
        target=validator.start_pipeline,
        name="QualityThread",
        daemon=True
    )
    validator_thread.start()
    logger.info("Validation & Quality pipeline thread started.")

    try:
        while not ingestor.shutdown_event.is_set():
            try:
                ingestor.run_pipeline()
                logger.debug("ETL cycle complete. Sleeping for 60s...")
                # Use a loop with short sleeps so KeyboardInterrupt can be caught on Windows
                for _ in range(60):
                    if ingestor.shutdown_event.is_set():
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received in loop.")
                ingestor.shutdown()
                break
            except Exception as e:
                logger.error("ETL loop error: %s", e)
                # Back off briefly before retrying
                time.sleep(10)
    finally:
        logger.info("GDrive ETL worker exiting.")


if __name__ == "__main__":
    main()

