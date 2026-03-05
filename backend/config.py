import os
from dotenv import load_dotenv
from datetime import timedelta
import urllib.parse  # Added for password encoding

load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  

    # --- Database configuration (FIXED for special characters) ---
    DB_USER = os.getenv('DB_USER')
    # Use quote_plus to handle '@' or other special chars in the password
    DB_PASSWORD = urllib.parse.quote_plus(os.getenv('DB_PASSWORD', ''))
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,
        "max_overflow": 10,
        "pool_recycle": 280,
        "pool_pre_ping": True, # Checks if DB is alive before the query
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- JWT CONFIGURATION ---
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY must be set in .env file")
    
    # 1. Store token in cookies (Auto-login)
    JWT_TOKEN_LOCATION = ['cookies']

    # 2. Set to True because your live site uses HTTPS
    JWT_COOKIE_SECURE = True 

    # 3. Disable CSRF for now
    JWT_COOKIE_CSRF_PROTECT = False

    # 4. Session Timeout: 30 DAYS
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30) 

    # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Add ETL/Google Drive/Batch config for Celery tasks
    SERVICE_ACCOUNT_FILE = os.getenv(
        "SERVICE_ACCOUNT_FILE",
        os.path.join(os.getcwd(), "model", "honey-bee-digital-d96daf6e6faf.json")
    )
    # Define a single source for the database URI to avoid confusion and errors
    DATABASE_URI = SQLALCHEMY_DATABASE_URI
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    ETL_VERSION = os.getenv("ETL_VERSION", "2.0.0")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2000"))

# Instantiate config for import convenience
config = Config()
