from celery import shared_task
from services.scrapers.amazon_service import scrape_amazon_search

@shared_task(name="tasks.products.scrape_amazon", ignore_result=True)
def run_amazon_scraper(search_term, pages=1):
    """
    Celery task wrapper for Amazon live scraping.
    """
    scrape_amazon_search(search_term, pages)
