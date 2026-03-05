from flask import Blueprint, request, jsonify
import threading
from extensions import db
from model.product_model.amazon_product import AmazonProduct
from services.scrapers.amazon_service import scrape_amazon_search

amazon_api_bp = Blueprint('amazon_api_bp', __name__)

# --- ROUTE 1: Start Scraping ---
@amazon_api_bp.route('/scrape_amazon', methods=['POST'])
def scrape_and_insert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        search_term = data.get('search_term')
        pages = int(data.get('pages', 1))
        
        if not search_term:
            return jsonify({'error': 'search_term is required'}), 400
            
        # Start the service via Celery to avoid worker multiplication issues
        from tasks.products_task.amazon_scraper_task import run_amazon_scraper
        run_amazon_scraper.delay(search_term, pages)
        
        return jsonify({"status": "started", "message": f"Scraping '{search_term}' started via Celery"}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ROUTE 2: Fetch Data (Using SQLAlchemy) ---
@amazon_api_bp.route('/amazon-data', methods=['GET']) 
def get_amazon_data():
    try:
        # Fetch latest 1000 products using SQLAlchemy
        products = AmazonProduct.query.order_by(AmazonProduct.id.desc()).limit(1000).all()
        
        # Manually serialize the data since we can't edit the Model to add .to_dict()
        results = []
        for p in products:
            results.append({
                "id": p.id,
                "ASIN": p.ASIN,
                "Product_name": p.Product_name,
                "price": p.price,
                "rating": p.rating,
                "Number_of_ratings": p.Number_of_ratings,
                "Brand": p.Brand,
                "link": p.link,
                "Image_URLs": p.Image_URLs,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })
            
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500