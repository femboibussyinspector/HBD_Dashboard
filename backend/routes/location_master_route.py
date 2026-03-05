from flask import Blueprint, request, jsonify
from extensions import db
from sqlalchemy import text

# Using a unique name to prevent the 'already registered' ValueError
location_master_bp = Blueprint('location_master_unique', __name__)

@location_master_bp.route("/fetch-data", methods=["GET"])
def fetch_location_data():
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page
    
    # Filter parameters from the React frontend
    area = request.args.get('area', '')
    city = request.args.get('city', '')
    state = request.args.get('state', '')

    where_clauses = ["1=1"]
    params = {"limit": per_page, "offset": offset}

    # Apply filters based on the Location_Master_India schema
    if area:
        where_clauses.append("l.area_name LIKE :area")
        params["area"] = f"%{area}%"
    if city:
        where_clauses.append("l.city_name LIKE :city")
        params["city"] = f"%{city}%"
    if state:
        where_clauses.append("l.state_full_name LIKE :state")
        params["state"] = f"%{state}%"

    where_str = " AND ".join(where_clauses)

    try:
        # The corrected JOIN: l.area_name maps to m.area
        query = text(f"""
            SELECT 
                l.id, l.area_name, l.city_name, l.state_full_name, l.state_short_code, l.country_name,
                COUNT(m.id) as total_records
            FROM Location_Master_India l
            LEFT JOIN master_table m ON 
                l.area_name COLLATE utf8mb4_general_ci = m.area COLLATE utf8mb4_general_ci 
                AND l.city_name COLLATE utf8mb4_general_ci = m.city COLLATE utf8mb4_general_ci
            WHERE {where_str}
            GROUP BY l.id, l.area_name, l.city_name, l.state_full_name, l.state_short_code, l.country_name
            ORDER BY total_records DESC
            LIMIT :limit OFFSET :offset
        """)
        
        results = db.session.execute(query, params).fetchall()
        
        # Prepare data for the React table
        data = []
        for row in results:
            data.append({
                "id": row.id,
                "area": row.area_name,
                "city": row.city_name,
                "state": f"{row.state_full_name} ({row.state_short_code})",
                "country": row.country_name,
                "total_records": row.total_records
            })

        # Calculate total pages for pagination
        count_query = text(f"SELECT COUNT(*) FROM Location_Master_India l WHERE {where_str}")
        total_count = db.session.execute(count_query, params).scalar()
        total_pages = (total_count + per_page - 1) // per_page

        return jsonify({
            "status": "SUCCESS",
            "data": data,
            "total_pages": total_pages
        })
    except Exception as e:
        # Log the error and return a 500 status
        print(f"❌ SQL Execution Error: {str(e)}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500