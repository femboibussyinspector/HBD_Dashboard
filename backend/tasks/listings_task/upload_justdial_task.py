from services.csv_uploaders_listing.upload_justdial import upload_justdial_data
from celery_app import celery
import os

@celery.task(bind=True,autoretry_for=(Exception,),retry_kwargs={'max_retries':3,'countdown':5},retry_jitter=True,acks_late=True,retry_backoff=True)
def process_justdial_task(self,file_paths):
    if not file_paths:
        raise ValueError("No file provided")
    result = upload_justdial_data(file_paths)

    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except PermissionError:
            pass
    return result