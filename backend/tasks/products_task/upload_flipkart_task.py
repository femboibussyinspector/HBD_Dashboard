from services.csv_uploaders_product.upload_flipkart import upload_flipkart_products_data
from celery_app import celery
import os

@celery.task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 3,'countdown': 5},retry_jitter=True,acks_late=True)
def process_flipkart_products_task(self,file_paths):
    if not file_paths:
        raise ValueError("No file provided")
    result = upload_flipkart_products_data(file_paths)

    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except PermissionError:
            pass
    return result