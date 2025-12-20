from celery import Celery
import os

# REDIS_URL = os.getenv("REDIS_URL")

celery = Celery("tasks")

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

import tasks.listings_task.upload_shiksha_task