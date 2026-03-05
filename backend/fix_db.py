import os
from flask import Flask
from extensions import db
from config import Config
from utils.db_migrations import run_pending_migrations

def fix():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        print("🛠️ Manually running Database Migrations...")
        try:
            run_pending_migrations(app)
            print("✨ Database Migrations complete!")
        except Exception as e:
            print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    fix()
