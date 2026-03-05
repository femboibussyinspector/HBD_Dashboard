from flask import Blueprint, request, jsonify
from extensions import db
from model.yellow_pages import YellowPages

yellow_pages_bp = Blueprint('yellow_pages_bp', __name__)

@yellow_pages_bp.route('/fetch-data', methods=['GET'])
def fetch_yellow_pages_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')

        query = YellowPages.query
        
        # Filtering by the 'name' and 'city' columns
        if search:
            query = query.filter(YellowPages.name.ilike(f"%{search}%"))
        
        if city:
            query = query.filter(YellowPages.city.ilike(f"%{city}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
        
    except Exception as e:
        print(f"❌ Yellow Pages Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500