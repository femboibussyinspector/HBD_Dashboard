import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

try:
    print(f"Connecting to {DB_NAME} at {DB_HOST}...")
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    # helper to ignore "column exists" errors
    def execute_ignore_sqls(sqls):
        for sql in sqls:
            try:
                cursor.execute(sql)
                print(f"Success: {sql[:50]}...")
            except mysql.connector.Error as err:
                print(f"Note: {err}")

    # Modify password_hash to be nullable
    execute_ignore_sqls(["ALTER TABLE users MODIFY password_hash VARCHAR(200) NULL;"])
    
    # Add new columns
    execute_ignore_sqls([
        "ALTER TABLE users ADD COLUMN google_id VARCHAR(255) UNIQUE;",
        "ALTER TABLE users ADD COLUMN name VARCHAR(255);",
        "ALTER TABLE users ADD COLUMN profile_picture TEXT;",
        "ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE users ADD COLUMN verification_token VARCHAR(100) UNIQUE;"
    ])

    conn.commit()
    conn.close()
    print("Database update script completed.")

except Exception as e:
    print(f"Error: {e}")
