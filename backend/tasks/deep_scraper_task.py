from celery import shared_task

from services.scrapers.google_maps_service import run_google_maps_scraper



@shared_task(name="tasks.deep_scraper.run", ignore_result=True)
def run_deep_scraper(task_id: int) -> None:
    """
    Celery task wrapper around the Playwright-based deep scraper.
    Ensures the scraper runs in a worker process, not in the web server.
    """
    from app import app as flask_app
    run_google_maps_scraper(task_id, flask_app)


