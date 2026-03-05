from flask import Blueprint, request, jsonify
from extensions import db
from model.heyplaces import HeyPlaces

# The name must match what you imported in app.py
heyplaces_bp = Blueprint('heyplaces_bp', __name__)

@heyplaces_bp.route('/fetch-data', methods=['GET'])
def fetch_heyplaces_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '') # Added this to match your React frontend

        query = HeyPlaces.query

        # Filter by Business Name
        if search:
            query = query.filter(HeyPlaces.name.ilike(f"%{search}%"))
        
        # Filter by City
        if city:
            query = query.filter(HeyPlaces.city.ilike(f"%{city}%"))
        
        # Paginate results
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200

    except Exception as e:
        print(f"❌ Error in HeyPlaces fetch: {str(e)}")
        return jsonify({"error": str(e)}), 500