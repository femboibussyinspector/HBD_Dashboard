import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.to_valid_json import to_valid_json
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_nearbuy_data(file_paths):

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
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'Name'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'Latitude'),
                        safe_get(row, 'Longitude'),
                        to_valid_json(safe_get(row, 'Number')),
                        safe_get(row, 'Rating'),
                        safe_get(row, 'Country'),
                        safe_get(row, 'City'),
                        )
                        chunk_data.append(row_tuple)


                    # execute batch insert
                    insert_query = '''
                        INSERT INTO nearbuy (
                            name, address, latitude, longitude, number, rating, country, city
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            address = VALUES(address),
                            number = VALUES(number),
                            rating = VALUES(rating),
                            country = VALUES(country),
                            city = VALUES(city);
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