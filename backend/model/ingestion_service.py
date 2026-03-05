"""
Deprecated ingestion entrypoint.

This module previously implemented a Pandas-based ETL pipeline reading entire
CSV files from Google Drive into memory and writing them to MySQL. That
approach is unsafe for large files and is no longer used in production.

All GDrive ingestion is now handled by the streaming, Celery-based engine:
  - model.robust_gdrive_etl_v2.GDriveHighSpeedIngestor (scanner/producer)
  - tasks.gdrive_task.etl_tasks.process_csv_task (streaming CSV consumer)

This file is kept only to avoid import errors in legacy scripts.
"""

raise RuntimeError(
    "ingestion_service.py is deprecated. "
    "Use the robust GDrive ETL (worker_etl.py + Celery tasks.gdrive_task.etl_tasks) instead."
)

