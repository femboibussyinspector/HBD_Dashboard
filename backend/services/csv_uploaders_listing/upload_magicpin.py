import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_magicpin_data(file_paths):
    if not file_paths:
        raise ValueError("No files provided for upload.")
    connection = get_mysql_connection()
    cursor = connection.cursor()
    batch_size = 10000
    inserted = 0
    upload_success = False
    try:
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:
                chunkFile_data = pd.read_csv(file,chunksize = batch_size)
                for chunk in chunkFile_data:
                    chunk_data = []
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'name'),
                        safe_get(row, 'number'),
                        safe_get(row, 'rating'),
                        safe_get(row, 'avgspent'),
                        safe_get(row, 'address'),
                        safe_get(row, 'area'),
                        safe_get(row, 'subcategory'),
                        safe_get(row, 'city'),
                        safe_get(row, 'category'),
                        safe_get(row, 'costfortwo'),
                        safe_get(row, 'latitude'),
                        safe_get(row, 'longitude')
                        )
                        chunk_data.append(row_tuple)
                    insert_query = """
                        INSERT INTO magicpin (
                            name,
                            number,
                            rating,
                            avg_spent,
                            address,
                            area,
                            subcategory,
                            city,
                            category,
                            cost_for_two,
                            latitude,
                            longitude
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE
                                    number = VALUES(number),
                                    rating = VALUES(rating),
                                    avg_spent = VALUES(avg_spent),
                                    area = VALUES(area),
                                    subcategory = VALUES(subcategory),
                                    city = VALUES(city),
                                    category = VALUES(category),
                                    cost_for_two = VALUES(cost_for_two),
                                    latitude = VALUES(latitude),
                                    longitude = VALUES(longitude);
                    """

                    try:
                        cursor.executemany(insert_query,chunk_data)
                        connection.commit()
                        inserted+=len(chunk_data)
                    except Exception:
                        print("roll error")
                        connection.rollback()
                        raise 
        # upload_success = True
        return inserted
    finally:
        cursor.close()
        connection.close()