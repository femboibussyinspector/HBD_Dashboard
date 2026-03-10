import os
import sys
import logging
from app import app
from extensions import db
from services.location_validator_service import process_master_table_fixes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_fix(limit=5000):
    """
    Runs the location fix process within the Flask app context.
    """
    logger.info(f"🚀 Starting Master Table Location Fix (Limit: {limit})...")
    
    with app.app_context():
        try:
            fixed_count = process_master_table_fixes(db.session, limit=limit)
            logger.info(f"✨ SUCCESS! Fixed {fixed_count} records in master_table.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Fix failed: {e}")
            raise

if __name__ == "__main__":
    # Allow passing limit as an argument
    limit = 5000
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            logger.warning(f"Invalid limit '{sys.argv[1]}', using default 5000")
            
    run_fix(limit=limit)
