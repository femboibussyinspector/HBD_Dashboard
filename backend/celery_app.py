from celery import Celery
import os

# REDIS_URL = os.getenv("REDIS_URL")

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

celery = Celery('tasks', broker=broker_url, backend=result_backend)
celery.conf.update(
    broker_url = os.getenv("CELERY_BROKER_URL"),
    result_backend = os.getenv("CELERY_RESULT_BACKEND"),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

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
import tasks.upload_master_task
import tasks.products_task.upload_blinkit_task
import tasks.products_task.upload_dmart_task
import tasks.products_task.upload_flipkart_task
import tasks.products_task.upload_india_mart_task
import tasks.products_task.upload_jio_mart_task
import tasks.products_task.upload_vivo_task
