import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_heyplaces_data(file_paths):

    if not file_paths:
        raise ValueError("No files provided to upload.")
    
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
                        safe_get(row, 'Number'),
                        safe_get(row, 'Website'),
                        safe_get(row, 'category'),
                        safe_get(row, 'city'),
                        )
                        chunk_data.append(row_tuple)


                    # execute batch insert
                    insert_query = '''
                        INSERT INTO heyplaces (
                            name, address, number, website, category, city
                        ) VALUES (%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            number = VALUES(number),
                            website = VALUES(website),
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