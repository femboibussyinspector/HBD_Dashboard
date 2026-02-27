from flask import Blueprint, request, jsonify, current_app
from extensions import db
from model.scraper_task import ScraperTask

from tasks.deep_scraper_task import run_deep_scraper

scraper_bp = Blueprint('scraper_bp', __name__)

# --- CORRECTED ROUTES (Removed '/api' prefix) ---

@scraper_bp.route('/tasks', methods=['GET'])  # url_prefix makes this /api/tasks
def get_tasks():
    try:
        tasks = ScraperTask.query.order_by(ScraperTask.id.desc()).all()
        return jsonify([{
            "id": t.id,
            "platform": t.platform,
            "query": t.search_query,
            "status": t.status,
            "progress": t.progress,
            "errorMsg": t.error_message
        } for t in tasks]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scraper_bp.route('/stop', methods=['POST'])  # url_prefix makes this /api/stop
def stop_task():
    data = request.json
    task_id = data.get('task_id')
    task = ScraperTask.query.get(task_id)
    if task:
        task.should_stop = True
        db.session.commit()
        return jsonify({"message": "Stop signal sent"}), 200
    return jsonify({"error": "Task not found"}), 404

@scraper_bp.route('/tasks/<int:task_id>', methods=['DELETE']) # url_prefix makes this /api/tasks/<id>
def delete_task(task_id):
    task = ScraperTask.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"error": "Task not found"}), 404

@scraper_bp.route('/scrape', methods=['POST']) # url_prefix makes this /api/scrape
def start_deep_scrape():
    data = request.json
    category = data.get('category')
    city = data.get('city')
    platform = data.get('platform', 'Google Maps')

    # 1. Create Task in DB
    new_task = ScraperTask(
        platform=platform,
        search_query=f"{category} in {city}",
        location=city,
        status="starting"
    )
    db.session.add(new_task)
    db.session.commit()

    # 2. Dispatch scraper to Celery worker
    run_deep_scraper.delay(new_task.id)

    return jsonify({"message": "Deep Scraper Started", "task_id": new_task.id}), 202

@scraper_bp.route('/results', methods=['GET']) # url_prefix makes this /api/results
def api_results():
    pass