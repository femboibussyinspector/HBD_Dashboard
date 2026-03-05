from flask import Blueprint, request, jsonify
from extensions import db
from model.nearbuy import NearBuy

nearbuy_bp = Blueprint('nearbuy_bp', __name__)

@nearbuy_bp.route('/fetch-data', methods=['GET'])
def fetch_nearbuy_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')

        query = NearBuy.query
        if search:
            query = query.filter(NearBuy.name.ilike(f"%{search}%"))
        if city:
            query = query.filter(NearBuy.city.ilike(f"%{city}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
    except Exception as e:
        print(f"❌ NearBuy SQL Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500