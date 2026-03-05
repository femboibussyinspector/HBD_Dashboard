import logging
from sqlalchemy import text, inspect
from extensions import db

logger = logging.getLogger(__name__)

def run_pending_migrations(app):
    """
    Executes safe, idempotent database migrations on application startup.
    Handles:
    1. Schema updates (ENUM fixes)
    2. Index creation
    """
    with app.app_context():
        try:
            logger.info("🔄 Checking for pending DB migrations...")
            engine = db.engine
            
            with engine.connect() as conn:
                # === ISSUE 2: drive_folder_registry Status ENUM Fix ===
                # 1. Update existing legacy values to match new ENUM
                # Mapping: 'Completed'/'UPDATED' -> 'DONE', 'Processing' -> 'SCANNING', etc.
                
                # Check if current column type is already correct to avoid redundant work
                # (Simple heuristic or just run updates safely)
                
                trans = conn.begin()
                try:
                    # Safe updates for legacy string values
                    conn.execute(text("UPDATE drive_folder_registry SET status='DONE' WHERE status IN ('Completed', 'UPDATED', 'Processed')"))
                    conn.execute(text("UPDATE drive_folder_registry SET status='SCANNING' WHERE status IN ('Processing', 'Scanning', 'InProgress')"))
                    conn.execute(text("UPDATE drive_folder_registry SET status='PENDING' WHERE status IN ('Pending', 'New')"))
                    conn.execute(text("UPDATE drive_folder_registry SET status='ERROR' WHERE status IN ('Error', 'Failed')"))
                    
                    # 2. ALTER Table to ENUM
                    # We use a try-catch for the ALTER because it might fail if bad data remains, 
                    # but we tried to clean it above.
                    # Note: We can't easily check "IF column is enum", so we just run it. 
                    # If it's already ENUM, this refactoring is usually harmless or quick in MySQL provided data fits.
                    conn.execute(text("""
                        ALTER TABLE drive_folder_registry 
                        MODIFY COLUMN status ENUM('PENDING', 'SCANNING', 'DONE', 'ERROR') 
                        DEFAULT 'PENDING'
                    """))
                    logger.info("✅ `drive_folder_registry` status column migrated to ENUM.")
                except Exception as e:
                    logger.warning(f"⚠️ drive_folder_registry migration skipped or failed (might be already done): {e}")
                    # Don't rollback immediately, indexes might still be needed. 
                    # But if transaction failed, we might need new one.
                    # For safety in this script, we treat this block as one unit.
                    trans.rollback()
                else:
                    trans.commit()

                # === ISSUE 1.5: Missing Columns (full_drive_path) ===
                try:
                    # Check if column exists
                    col_check = text("""
                        SELECT COUNT(*) FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'raw_google_map_drive_data' 
                        AND COLUMN_NAME = 'full_drive_path'
                    """)
                    if conn.execute(col_check).scalar() == 0:
                        logger.info("⚠️ Column `full_drive_path` missing. Adding it now...")
                        conn.execute(text("ALTER TABLE raw_google_map_drive_data ADD COLUMN full_drive_path TEXT"))
                        logger.info("✅ Column `full_drive_path` added successfully.")
                except Exception as e:
                    logger.error(f"❌ Failed to add column `full_drive_path`: {e}")
                
                # === ISSUE 2.5: Missing Column (drive_uploaded_time) ===
                try:
                    col_check_2 = text("""
                        SELECT COUNT(*) FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'raw_google_map_drive_data' 
                        AND COLUMN_NAME = 'drive_uploaded_time'
                    """)
                    if conn.execute(col_check_2).scalar() == 0:
                        logger.info("⚠️ Column `drive_uploaded_time` missing. Adding it now...")
                        conn.execute(text("ALTER TABLE raw_google_map_drive_data ADD COLUMN drive_uploaded_time DATETIME"))
                        logger.info("✅ Column `drive_uploaded_time` added successfully.")
                except Exception as e:
                    logger.error(f"❌ Failed to add column `drive_uploaded_time`: {e}")

                # === ISSUE 2.6: Missing Column (source) ===
                for col_name, col_type in [("source", "VARCHAR(50)"), ("area", "VARCHAR(255)")]:
                    try:
                        col_check_x = text(f"""
                            SELECT COUNT(*) FROM information_schema.COLUMNS 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'raw_google_map_drive_data' 
                            AND COLUMN_NAME = '{col_name}'
                        """)
                        if conn.execute(col_check_x).scalar() == 0:
                            logger.info(f"⚠️ Column `{col_name}` missing. Adding it now...")
                            conn.execute(text(f"ALTER TABLE raw_google_map_drive_data ADD COLUMN {col_name} {col_type}"))
                            logger.info(f"✅ Column `{col_name}` added successfully.")
                    except Exception as e:
                        logger.error(f"❌ Failed to add column `{col_name}`: {e}")

                # === ISSUE 1: Missing Indexes ===
                # We use specific exception handling for "Duplicate key name" which is error code 1061
                
                indexes_to_create = [
                    ("idx_city", "CREATE INDEX idx_city ON raw_google_map_drive_data(city)"),
                    ("idx_state_category", "CREATE INDEX idx_state_category ON raw_google_map_drive_data(state, category)")
                ]

                for name, sql in indexes_to_create:
                    try:
                        # Check if index exists using information_schema to be safe 
                        # (MySQL 'IF NOT EXISTS' syntax for indexes was added in 8.0, 
                        # but some older local environments might lack it. This is universally safe.)
                        check_sql = text("""
                            SELECT COUNT(1) IndexIsThere 
                            FROM INFORMATION_SCHEMA.STATISTICS 
                            WHERE table_schema = DATABASE() 
                            AND table_name = 'raw_google_map_drive_data' 
                            AND index_name = :idx_name
                        """)
                        result = conn.execute(check_sql, {"idx_name": name}).scalar()
                        
                        if result == 0:
                            conn.execute(text(sql))
                            logger.info(f"✅ Created index: {name}")
                        else:
                            logger.info(f"⏩ Index {name} already exists.")
                            
                    except Exception as e:
                        logger.error(f"❌ Failed to create index {name}: {e}")

                # === ISSUE 3: Dead Letter Queue Table ===
                try:
                    table_check = text("""
                        SELECT COUNT(*) FROM information_schema.TABLES
                        WHERE TABLE_SCHEMA = DATABASE()
                        AND TABLE_NAME = 'etl_dlq'
                    """)
                    if conn.execute(table_check).scalar() == 0:
                        logger.info("⚠️ Table `etl_dlq` missing. Creating it now...")
                        conn.execute(text("""
                            CREATE TABLE etl_dlq (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                file_id VARCHAR(255) NOT NULL,
                                file_name VARCHAR(500),
                                error TEXT,
                                task_id VARCHAR(255),
                                retry_count INT DEFAULT 0,
                                failed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                INDEX idx_failed_at (failed_at)
                            )
                        """))
                        logger.info("✅ Table `etl_dlq` created successfully.")
                    else:
                        logger.info("⏩ Table `etl_dlq` already exists.")
                except Exception as e:
                    logger.error(f"❌ Failed to create `etl_dlq` table: {e}")

                # === ISSUE 4: Data Lineage Columns on raw_google_map_drive_data ===
                lineage_columns = [
                    ("etl_version", "VARCHAR(20)"),
                    ("processed_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                    ("task_id", "VARCHAR(255)"),
                    ("file_hash", "VARCHAR(32)"),
                ]
                for col_name, col_type in lineage_columns:
                    try:
                        col_check = text(f"""
                            SELECT COUNT(*) FROM information_schema.COLUMNS
                            WHERE TABLE_SCHEMA = DATABASE()
                            AND TABLE_NAME = 'raw_google_map_drive_data'
                            AND COLUMN_NAME = '{col_name}'
                        """)
                        if conn.execute(col_check).scalar() == 0:
                            logger.info(f"⚠️ Column `{col_name}` missing on raw_google_map_drive_data. Adding...")
                            conn.execute(text(f"ALTER TABLE raw_google_map_drive_data ADD COLUMN {col_name} {col_type}"))
                            logger.info(f"✅ Column `{col_name}` added to raw_google_map_drive_data.")
                    except Exception as e:
                        logger.error(f"❌ Failed to add column `{col_name}` to raw_google_map_drive_data: {e}")

                # === ISSUE 5: file_hash Column on file_registry ===
                try:
                    col_check = text("""
                        SELECT COUNT(*) FROM information_schema.COLUMNS
                        WHERE TABLE_SCHEMA = DATABASE()
                        AND TABLE_NAME = 'file_registry'
                        AND COLUMN_NAME = 'file_hash'
                    """)
                    if conn.execute(col_check).scalar() == 0:
                        print("⚠️ Column `file_hash` missing on file_registry. Adding...")
                        conn.execute(text("ALTER TABLE file_registry ADD COLUMN file_hash VARCHAR(32)"))
                        print("✅ Column `file_hash` added to file_registry.")
                    else:
                        print("⏩ Column `file_hash` already exists on file_registry.")
                except Exception as e:
                    print(f"❌ Failed to add `file_hash` to file_registry: {e}")

                # === ISSUE 6: Validation, Cleaning and Logging Tables ===
                try:
                    tables_to_create = [
                        ("validation_raw_google_map", """
                            CREATE TABLE IF NOT EXISTS validation_raw_google_map (
                                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                                raw_id BIGINT UNIQUE NOT NULL COMMENT 'FK to raw_google_map_drive_data.id',
                                name VARCHAR(500),
                                address TEXT,
                                website TEXT,
                                phone_number VARCHAR(100),
                                reviews_count INT DEFAULT 0,
                                reviews_avg FLOAT DEFAULT 0.00,
                                category VARCHAR(255),
                                subcategory VARCHAR(255),
                                city VARCHAR(255),
                                state VARCHAR(255),
                                area VARCHAR(255),
                                created_at DATETIME,
                                validation_status ENUM('PENDING', 'STRUCTURED', 'INVALID', 'UNSTRUCTURED', 'DUPLICATE', 'MISSING', 'VALID') NOT NULL DEFAULT 'PENDING',
                                cleaning_status ENUM('NOT_STARTED', 'CLEANED') NOT NULL DEFAULT 'NOT_STARTED',
                                missing_fields TEXT,
                                invalid_format_fields TEXT,
                                duplicate_reason TEXT,
                                processed_at DATETIME NULL,
                                UNIQUE INDEX idx_raw_id (raw_id),
                                INDEX idx_validation_status (validation_status),
                                INDEX idx_cleaning_status (cleaning_status),
                                INDEX idx_composite_snapshot (name(100), address(100), phone_number)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                        """),
                        ("raw_clean_google_map_data", """
                            CREATE TABLE IF NOT EXISTS raw_clean_google_map_data (
                                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                                raw_id BIGINT UNIQUE NOT NULL COMMENT 'Refers to validation_raw_google_map.raw_id',
                                name VARCHAR(500),
                                address TEXT,
                                website TEXT,
                                phone_number VARCHAR(100),
                                reviews_count INT DEFAULT 0,
                                reviews_avg FLOAT DEFAULT 0.00,
                                category VARCHAR(255),
                                subcategory VARCHAR(255),
                                city VARCHAR(255),
                                state VARCHAR(255),
                                area VARCHAR(255),
                                created_at DATETIME,
                                UNIQUE INDEX idx_raw_id (raw_id),
                                UNIQUE INDEX idx_composite_dedup (name(100), phone_number, city(50), address(100))
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                        """),
                        ("data_validation_log", """
                            CREATE TABLE IF NOT EXISTS data_validation_log (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                total_processed INT,
                                missing_count INT,
                                valid_count INT,
                                duplicate_count INT,
                                cleaned_count INT,
                                last_id BIGINT,
                                timestamp DATETIME
                            );
                        """),
                        ("invalid_google_map_data", """
                            CREATE TABLE IF NOT EXISTS invalid_google_map_data (
                                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                                raw_id BIGINT,
                                name VARCHAR(500),
                                address TEXT,
                                website TEXT,
                                phone_number VARCHAR(100),
                                bank_number VARCHAR(100) COMMENT 'Original phone number before cleaning',
                                reviews_count INT DEFAULT 0,
                                reviews_avg FLOAT DEFAULT 0.00,
                                category VARCHAR(255),
                                subcategory VARCHAR(255),
                                city VARCHAR(255),
                                state VARCHAR(255),
                                area VARCHAR(255),
                                validation_label VARCHAR(100) COMMENT 'MISSING, INVALID',
                                missing_fields TEXT,
                                invalid_format_fields TEXT,
                                error_reason TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                        """),
                        ("g_map_master_table", """
                            CREATE TABLE IF NOT EXISTS g_map_master_table (
                                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(500),
                                address TEXT,
                                website TEXT,
                                phone_number VARCHAR(100),
                                reviews_count INT DEFAULT 0,
                                reviews_avg FLOAT DEFAULT 0.00,
                                category VARCHAR(255),
                                subcategory VARCHAR(255),
                                city VARCHAR(255),
                                state VARCHAR(255),
                                area VARCHAR(255),
                                created_at DATETIME,
                                UNIQUE INDEX idx_unique_business (name(100), phone_number, city(50), address(100))
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                        """)
                    ]
                    for t_name, t_sql in tables_to_create:
                        conn.execute(text(t_sql))
                        logger.info(f"✅ Ensured table `{t_name}` exists.")
                except Exception as e:
                    logger.error(f"❌ Failed to ensure validation tables exist: {e}")

            print("🏁 DB Migrations check complete.")
            
        except Exception as e:
            logger.error(f"❌ Critical Migration Error: {e}")
