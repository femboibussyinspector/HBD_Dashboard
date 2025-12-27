from flask import Flask,request,jsonify,Blueprint
from tasks.listings_task.upload_yellow_pages_task import process_yellow_pages_task
from werkzeug.utils import secure_filename
import os 
from utils.storage import get_upload_base_dir


yellow_pages_bp = Blueprint("yellow_pages_bp",__name__)
@yellow_pages_bp.route("/upload/yellow-pages-data",methods=["POST"])
def upload_yellow_pages_upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error":"No files provided"}),400
    UPLOAD_DIR = get_upload_base_dir()/"yellow_pages"
    UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
    paths = []
    for f in files:
        filename = secure_filename(f.filename)
        filepath = UPLOAD_DIR/filename
        f.save(filepath)
        paths.append(str(filepath))
    try:
        task = process_yellow_pages_task.delay(paths)
        return jsonify({
            "status":"files_accepted",
            "task_id":task.id
            }),202
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),500