import os
import pymysql
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Database Config
DB_HOST = "localhost" # Force localhost for local migration script run
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "hbd_dashboard")
DB_PORT = int(os.getenv("DB_PORT", 3306))

def migrate_db():
    print(f"Connecting to database {DB_NAME} at {DB_HOST}...")
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Check if columns exist
            print("Checking for existing columns...")
            cursor.execute(f"SHOW COLUMNS FROM users LIKE 'reset_otp'")
            result_otp = cursor.fetchone()
            
            cursor.execute(f"SHOW COLUMNS FROM users LIKE 'reset_otp_expiry'")
            result_expiry = cursor.fetchone()

            if not result_otp:
                print("Adding 'reset_otp' column...")
                cursor.execute("ALTER TABLE users ADD COLUMN reset_otp VARCHAR(6) NULL")
            else:
                print("'reset_otp' column already exists.")

            if not result_expiry:
                print("Adding 'reset_otp_expiry' column...")
                cursor.execute("ALTER TABLE users ADD COLUMN reset_otp_expiry DATETIME NULL")
            else:
                print("'reset_otp_expiry' column already exists.")

        connection.commit()
        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    migrate_db()
