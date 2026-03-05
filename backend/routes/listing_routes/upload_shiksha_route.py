from flask import Blueprint, request, jsonify
from extensions import db
from model.shiksha import Shiksha

shiksha_bp = Blueprint('shiksha_bp', __name__)

@shiksha_bp.route('/fetch-data', methods=['GET'])
def fetch_shiksha_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')

        query = Shiksha.query
        
        if search:
            query = query.filter(Shiksha.name.ilike(f"%{search}%"))
        
        # Filtering by 'area' since 'city' doesn't exist in the table
        if city:
            query = query.filter(Shiksha.area.ilike(f"%{city}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
        
    except Exception as e:
        print(f"❌ Shiksha Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500