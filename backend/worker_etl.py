import signal
import time
import logging

from model.robust_gdrive_etl_v2 import GDriveHighSpeedIngestor


logger = logging.getLogger("GDriveETLWorker")
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    )


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
    try:
        while not ingestor.shutdown_event.is_set():
            try:
                ingestor.run_pipeline()
                logger.info("ETL cycle complete. Sleeping for 60s...")
                if ingestor.shutdown_event.wait(timeout=60):
                    break
            except Exception as e:
                logger.error("ETL loop error: %s", e)
                # Back off briefly before retrying
                time.sleep(10)
    finally:
        logger.info("GDrive ETL worker exiting.")


if __name__ == "__main__":
    main()

