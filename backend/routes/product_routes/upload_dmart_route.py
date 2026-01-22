from flask import Flask,request,jsonify,Blueprint
from tasks.products_task.upload_dmart_task import process_dmart_task
from werkzeug.utils import secure_filename
import os 
from utils.storage import get_upload_base_dir

dmart_bp = Blueprint("dmart_bp",__name__)

@dmart_bp.route("/upload/dmart-data",methods=["POST"])
def upload_dmart_route():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error":"No files provided"}),400
    UPLOAD_DIR = get_upload_base_dir()/"dmart"
    UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
    paths = []
    for f in files:
        filename = secure_filename(f.filename)
        filepath = UPLOAD_DIR/filename
        f.save(filepath)
        paths.append(str(filepath))
    try:
        task = process_dmart_task.delay(paths)
        return jsonify({
            "status":"files_accepted",
            "task_id":task.id
            }),202
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),500