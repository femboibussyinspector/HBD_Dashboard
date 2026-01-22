# model/upload_master_reports_model.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, Index
from sqlalchemy.sql import func
from extensions import db

class UploadReport(db.Model):
    __tablename__ = "upload_reports"

    id = Column(Integer, primary_key=True)
    task_id = Column(String(36), nullable=False, unique=True, index=True)

    status = Column(String(20), nullable=False)

    total_processed = Column(Integer, default=0)
    inserted = Column(Integer, default=0)
    updated = Column(Integer, default=0)

    total_cities = Column(Integer, default=0)
    total_areas = Column(Integer, default=0)
    total_categories = Column(Integer, default=0)

    missing_primary_phone = Column(Integer, default=0)
    missing_email = Column(Integer, default=0)
    missing_address = Column(Integer, default=0)

    stats = Column(JSON)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
