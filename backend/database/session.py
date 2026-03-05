from sqlalchemy import create_engine
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

print(f"DEBUG ENV -> HOST: {DB_HOST} USER: {DB_USER} PASS: {'*' * len(DB_PASSWORD or '')} DB: {DB_NAME}")

import urllib.parse
# Construct database URL dynamically from environment variables
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD or '')}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Engine creation
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_pre_ping=True,    
    pool_recycle=1800       
)

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
