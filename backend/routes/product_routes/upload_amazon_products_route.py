from flask import Blueprint, request, jsonify
from extensions import db
from model.product_model.amazon_product import AmazonProduct

amazon_bp = Blueprint('amazon_bp', __name__)

@amazon_bp.route('/fetch-data', methods=['GET'])
def fetch_amazon_data():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '') # Swapped city for category

        query = AmazonProduct.query
        
        if search:
            query = query.filter(AmazonProduct.Product_name.ilike(f"%{search}%"))
        
        if category:
            query = query.filter(AmazonProduct.category.ilike(f"%{category}%"))
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in pagination.items],
            "total_pages": pagination.pages,
            "total_count": pagination.total,
            "current_page": page
        }), 200
        
    except Exception as e:
        print(f"❌ Amazon Route Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500