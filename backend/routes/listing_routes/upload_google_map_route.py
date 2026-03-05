from flask import Blueprint, request, jsonify
from extensions import db

# Make sure this import matches your exact filename (you mentioned googlepay.py)
# If your file is googlepay.py, change this to: from model.googlepay import GoogleMapData
from model.googlemap_data import GoogleMapData 

google_map_bp = Blueprint('google_map_bp', __name__)

@google_map_bp.route('/fetch-data', methods=['GET'])
def fetch_google_map_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')

        query = GoogleMapData.query
        
        # 1. Searching by 'business_name' because that is the column in your model
        if search:
            query = query.filter(GoogleMapData.business_name.ilike(f"%{search}%"))
        
        # 2. Searching by 'address' because your model does not have a 'city' column
        if city:
            query = query.filter(GoogleMapData.address.ilike(f"%{city}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
        
    except Exception as e:
        print(f"❌ Google Map Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500