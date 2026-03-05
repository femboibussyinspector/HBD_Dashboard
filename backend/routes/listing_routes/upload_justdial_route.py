from flask import Blueprint, request, jsonify
from extensions import db
from model.justdial import JustDial

justdial_bp = Blueprint('justdial_bp', __name__)

@justdial_bp.route('/fetch-data', methods=['GET'])
def fetch_justdial_data():
    try:
        # Get query parameters for pagination and filtering
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')

        query = JustDial.query

        # Filtering based on the ACTUAL database column: 'company'
        if search:
            query = query.filter(JustDial.company.ilike(f"%{search}%"))
        
        # Filtering based on the 'city' column
        if city:
            query = query.filter(JustDial.city.ilike(f"%{city}%"))
        
        # Use Flask-SQLAlchemy pagination
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200

    except Exception as e:
        # This will print the exact traceback in your foreground terminal
        print(f"❌ JustDial Route Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500