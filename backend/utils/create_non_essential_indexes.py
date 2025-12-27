def create_non_essential_indexes(cursor,tableName,indexes):
    cursor.execute("""
        SELECT index_name
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = %s
    """, (tableName,))

    existing_indexes = {row[0] for row in cursor.fetchall()}

    for index in indexes:
        idx_name = f"idx_{index}"
        if idx_name not in existing_indexes:
            cursor.execute(f"CREATE INDEX {idx_name} ON {tableName}({index})")