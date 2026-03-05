from flask import Blueprint, request, jsonify
from extensions import db
from model.product_model.bigbasket_product_model import BigBasket

bigbasket_bp = Blueprint('bigbasket_bp', __name__)

@bigbasket_bp.route('/fetch-data', methods=['GET'])
def fetch_bigbasket_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # Capture all three search inputs
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        sub_category = request.args.get('subcategory', '')

        query = BigBasket.query
        
        # Apply filters conditionally
        if search:
            query = query.filter(BigBasket.product.ilike(f"%{search}%"))
        
        if category:
            query = query.filter(BigBasket.category.ilike(f"%{category}%"))
            
        if sub_category:
            query = query.filter(BigBasket.sub_category.ilike(f"%{sub_category}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
        
    except Exception as e:
        print(f"❌ BigBasket Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500