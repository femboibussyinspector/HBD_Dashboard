from flask import Blueprint, request, jsonify
from extensions import db
from model.google_map_scrape import GoogleMapScrape

google_map_scrape_bp = Blueprint('google_map_scrape_bp', __name__)

@google_map_scrape_bp.route('/fetch-data', methods=['GET'])
def fetch_google_map_scrape_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')

        query = GoogleMapScrape.query
        
        if search:
            query = query.filter(GoogleMapScrape.name.ilike(f"%{search}%"))
        
        if city:
            # Since there is no 'city' column, we search within the address
            query = query.filter(GoogleMapScrape.address.ilike(f"%{city}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
        
    except Exception as e:
        print(f"❌ Google Map Scrape Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500