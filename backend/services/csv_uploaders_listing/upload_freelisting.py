import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes


def upload_freelisting_data(file_paths):
    if not file_paths:
        raise ValueError("No files provided for upload.")
    
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
                        safe_get(row, 'name'),
                        safe_get(row, 'phone'),
                        safe_get(row, 'address'),
                        safe_get(row, 'description'),
                        safe_get(row, 'category'),
                        safe_get(row, 'url'),
                        safe_get(row, 'subcategory_1'),
                        safe_get(row, 'subcategory_2'),
                        safe_get(row, 'subcategory'),
                        safe_get(row, 'catagories_4'),
                        safe_get(row, 'catagories_href_3'),
                        )
                        chunk_data.append(row_tuple)

                    # execute batch insert
                    insert_query = '''
                        INSERT INTO freelisting (
                            name, number, address, description, category, url, subcategory_1, subcategory_2, subcategory, categories_4, categories_href_3
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            number = VALUES(number),
                            description = VALUES(description),
                            category = VALUES(category),
                            url = VALUES(url),
                            subcategory_1 = VALUES(subcategory_1),
                            subcategory_2 = VALUES(subcategory_2),
                            subcategory = VALUES(subcategory),
                            categories_4 = VALUES(categories_4),
                            categories_href_3 = VALUES(categories_href_3);
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