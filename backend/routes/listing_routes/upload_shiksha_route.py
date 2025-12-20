from flask import Blueprint,request,jsonify
from tasks.listings_task.upload_shiksha_task import process_shiksha_task
from werkzeug.utils import secure_filename 
import os
from utils.storage import get_upload_base_dir

shiksha_bp = Blueprint('shiksha_bp',__name__)

@shiksha_bp.route("/upload/shiksha-data", methods=["POST"])
def upload_shiksha_route():
    try:
        files = request.files.getlist("files")
        print("FILES RECEIVED:", files)

        if not files:
            return jsonify({"error": "No files provided"}), 400

        UPLOAD_DIR = get_upload_base_dir()/"shiksha"
        UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
        paths = []
        for f in files:
            print("Saving file:", f.filename)
            filename = secure_filename(f.filename)
            filepath = UPLOAD_DIR/filename
            print("Saving to:", filepath)
            f.save(filepath)
            paths.append(str(filepath))

        print("SAVED PATHS:", paths)

        task = process_shiksha_task.delay(paths)

        return jsonify({
            "status": "files_accepted",
            "task_id": task.id
        }), 202

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500