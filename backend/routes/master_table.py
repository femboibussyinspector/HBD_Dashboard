from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_
from model.master_table_model import MasterTable
from database.session import get_db_session
from utils.storage import get_upload_base_dir
from werkzeug.utils import secure_filename
from tasks.upload_master_task import process_master_upload_task
from model.upload_master_reports_model import UploadReport

master_table_bp = Blueprint("master_table", __name__)

@master_table_bp.route("/upload/master", methods=["POST"])
def upload_master():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files provided"}), 400

    UPLOAD_DIR = get_upload_base_dir()/"master"
    UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

    paths = []
    for f in files:
        filename = secure_filename(f.filename)
        path = UPLOAD_DIR/filename
        f.save(path)
        paths.append(str(path))

    task = process_master_upload_task.delay(paths)

    return jsonify({
        "status": "files_accepted",
        "task_id": task.id
    }), 202

@master_table_bp.route("/upload/report/<task_id>", methods=["GET"])
def get_upload_report(task_id):
    session = get_db_session()

    try:
        report = session.query(UploadReport).filter_by(task_id=task_id).first()

        if not report:
            return jsonify({
                "status": "not_found",
                "task_id": task_id
            }), 404

        # Base stats
        base_stats = {
            "total_records": report.total_processed or 0,
            "total_cities": report.total_cities or 0,
            "total_areas": report.total_areas or 0,
            "total_categories": report.total_categories or 0,
            "city_match_status": (report.stats or {}).get(
                "city_match_status",
                {"matched": 0, "unmatched": 0}
            ),
            "missing_values": {
                "missing_phone": report.missing_primary_phone or 0,
                "missing_email": report.missing_email or 0,
                "missing_address": report.missing_address or 0
            }
        }

        return jsonify({
            "task_id": report.task_id,
            "status": report.status,
            "stats": base_stats
        })

    finally:
        session.close()

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
