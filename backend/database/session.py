from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base class for all models
Base = declarative_base()

# Database URL (MySQL) - Read from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

# Construct database URL dynamically from environment variables
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Engine creation
engine = create_engine(
    DATABASE_URL,
    echo=False,              # Set to False to reduce log noise
    future=True,
    pool_pre_ping=True,    
    pool_recycle=3600       
)

# Test database connection on startup
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Database connected successfully")
except Exception as e:
    print(f"❌ Database connection failed: {type(e).__name__}")

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session (thread-safe)
db_session = scoped_session(SessionLocal)

# Utility function to get a session
def get_db_session():
    """
    Returns a new database session.
    In Flask routes you must close() manually after use.
    """
    return db_session()

