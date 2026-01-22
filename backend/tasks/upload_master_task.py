from celery_app import celery
from services.master_uploader import upload_master_csv
from database.session import get_db_session
from model.upload_master_reports_model import UploadReport

@celery.task(bind=True, task_time_limit=14400)  # 4 hours
def process_master_upload_task(self, file_paths):
    session = get_db_session()
    task_id = self.request.id

    try:
        report = session.query(UploadReport).filter_by(task_id=task_id).first()
        if not report:
            report = UploadReport(task_id=task_id, status="PROCESSING")
            session.add(report)
            session.commit()

        upload_master_csv(file_paths, session, report)

        report.status = "COMPLETED"
        session.commit()
        
        return {"task_id": task_id, "status": "COMPLETED"}

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        
        if report:
            try:
                report.status = "FAILED"
                report.stats = {"error": str(e)[:1000]}
                session.commit()
            except:
                session.rollback()
        raise

    finally:
        session.close()