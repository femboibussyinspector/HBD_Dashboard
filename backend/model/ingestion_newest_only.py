
"""
Deprecated smart-ingestion entrypoint.

This module previously implemented a Pandas-based, recursive sync that loaded
entire CSV files from Google Drive into memory and wrote them directly to MySQL.
That approach is no longer used in production due to memory and duplication risks.

The authoritative ingestion path is now:
  - Scanner: model.robust_gdrive_etl_v2.GDriveHighSpeedIngestor
  - Worker: tasks.gdrive_task.etl_tasks.process_csv_task (streaming CSV)

If you need the city/category/path resolution logic that used to live here,
it should be refactored into a separate, pure utility module without Pandas or
database writes and then used from within the streaming ETL pipeline.
"""

raise RuntimeError(
    "ingestion_newest_only.py is deprecated. "
    "Use the robust GDrive ETL (worker_etl.py + Celery tasks.gdrive_task.etl_tasks) instead."
)

