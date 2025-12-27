import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_schoolgis_data(file_paths):
    if not file_paths:
        raise ValueError("No file paths provided for upload.")
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 10000
    upload_success = False
    try:
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:
                chunkFile_data = pd.read_csv(file,chunksize = batch_size)
                for chunk in chunkFile_data:
                    chunk_data = []
                    chunk = chunk.rename(columns=lambda c: c.replace(" ", "_"))
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'Name'),
                        safe_get(row, 'Pincode'),
                        safe_get(row, 'Latitude'),
                        safe_get(row, 'Longitude'),
                        safe_get(row, 'Subcategory'),
                        safe_get(row, 'City'),
                        safe_get(row, 'State'),
                        safe_get(row, 'Country'),
                        safe_get(row, 'Category')
                        )
                        chunk_data.append(row_tuple)

            # execute batch insert
                    insert_query = '''
                        INSERT INTO schoolgis (
                            name, pincode, latitude, longitude, subcategory,
                            city, state, country,category
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            pincode = VALUES(pincode),
                            subcategory = VALUES(subcategory),
                            city = VALUES(city),
                            state = VALUES(state),
                            country = VALUES(country),
                            category = VALUES(category);
                        '''
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