from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_
from model.master_table_model import MasterTable
from database.session import get_db_session

master_table_bp = Blueprint("master_table", __name__)

@master_table_bp.route("/master_table/list", methods=["GET"])
def get_master_table_list():
    session = get_db_session()
    try:
        limit = request.args.get("limit", 10, type=int)
        cursor = request.args.get("cursor", type=int)

        limit = max(1, min(limit, 50))

        query = session.query(MasterTable).order_by(MasterTable.id.desc())
        if cursor:
            query = query.filter(MasterTable.id < cursor)

        rows = query.limit(limit + 1).all()

        has_next = len(rows) > limit
        rows = rows[:limit]

        data = [row.to_dict() for row in rows]
        next_cursor = data[-1]["id"] if has_next else None

        return jsonify({
            "limit": limit,
            "next_cursor": next_cursor,
            "has_next": has_next,
            "data": data
        })
    finally:
        session.close()

@master_table_bp.route("/master_table/stats", methods=["GET"])
def get_master_table_stats():
    session = get_db_session()
    try:
        total_records = session.query(func.count(MasterTable.id)).scalar()

        total_cities = session.query(
            func.count(func.distinct(MasterTable.city))
        ).filter(MasterTable.city.isnot(None)).scalar()

        total_areas = session.query(
            func.count(func.distinct(MasterTable.area))
        ).filter(MasterTable.area.isnot(None)).scalar()

        total_categories = session.query(
            func.count(func.distinct(MasterTable.business_category))
        ).filter(MasterTable.business_category.isnot(None)).scalar()

        matched = session.query(func.count(MasterTable.id))\
            .filter(MasterTable.city.isnot(None)).scalar()

        city_match_status = {
            "matched": matched,
            "unmatched": total_records - matched
        }

        missing_values = {
            "missing_phone": session.query(func.count(MasterTable.id)).filter(
                or_(MasterTable.primary_phone.is_(None), MasterTable.primary_phone == "")
            ).scalar(),
            "missing_email": session.query(func.count(MasterTable.id)).filter(
                or_(MasterTable.email.is_(None), MasterTable.email == "")
            ).scalar(),
            "missing_address": session.query(func.count(MasterTable.id)).filter(
                or_(MasterTable.address.is_(None), MasterTable.address == "")
            ).scalar()
        }

        top_city_categories_query = session.query(
            MasterTable.city,
            MasterTable.business_category,
            func.count(MasterTable.id).label("count")
        ).filter(
            MasterTable.city.isnot(None),
            MasterTable.business_category.isnot(None)
        ).group_by(
            MasterTable.city,
            MasterTable.business_category
        ).order_by(
            func.count(MasterTable.id).desc()
        ).limit(5).all()

        top_city_categories = [
            {
                "city": city,
                "category": category,
                "count": count
            }
            for city, category, count in top_city_categories_query
        ]

        return jsonify({
            "total_records": total_records,
            "total_cities": total_cities,
            "total_areas": total_areas,
            "total_categories": total_categories,
            "city_match_status": city_match_status,
            "missing_values": missing_values,
            "top_city_categories": top_city_categories
        })
    finally:
        session.close()
