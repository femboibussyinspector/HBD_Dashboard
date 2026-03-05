from flask import Blueprint, request, jsonify
from extensions import db
from model.post_office import PostOffice

post_office_bp = Blueprint('post_office_bp', __name__)

@post_office_bp.route('/fetch-data', methods=['GET'])
def fetch_post_office_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '') # Search by area
        city = request.args.get('city', '')

        query = PostOffice.query

        if search:
            query = query.filter(PostOffice.area.ilike(f"%{search}%"))
        if city:
            query = query.filter(PostOffice.city.ilike(f"%{city}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200

    except Exception as e:
        print(f"❌ PostOffice Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500