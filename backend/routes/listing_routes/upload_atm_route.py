from flask import Flask,request,jsonify,Blueprint
from tasks.listings_task.upload_atm_task import process_atm_task
from werkzeug.utils import secure_filename
import os 
from utils.storage import get_upload_base_dir

atm_bp = Blueprint("atm_bp",__name__)

@atm_bp.route('/upload/atm-data',methods=["POST"])
def upload_atm_route():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error":"No files provided"}),400
    UPLOAD_DIR = get_upload_base_dir()/"atm"
    UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
    paths = []
    for f in files:
        filename = secure_filename(f.filename)
        filepath = UPLOAD_DIR/filename
        f.save(filepath)
        paths.append(str(filepath))
    try:
        task = process_atm_task.delay(paths)
        return jsonify({
            "status":"files_accepted",
            "task_id": task.id
            }), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500