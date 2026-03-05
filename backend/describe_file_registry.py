from config import config
from sqlalchemy import create_engine, text

engine = create_engine(config.DATABASE_URI)

with engine.connect() as conn:
    result = conn.execute(text("DESCRIBE file_registry"))
    cols = [row[0] for row in result]
    print("COLUMNS IN FILE_REGISTRY:", cols)
