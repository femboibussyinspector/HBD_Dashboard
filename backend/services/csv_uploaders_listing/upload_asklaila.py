import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.clean_data_decimal import clean_data_decimal
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_asklaila_data(file_paths):
    if not file_paths:
        raise ValueError("No file paths provided to upload.")    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 10000
    # upload_success = False
    try:
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:
                chunkFile_data = pd.read_csv(file,chunksize = batch_size)
                for chunk in chunkFile_data:
                    chunk_data = []
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'name'),
                        clean_data_decimal(safe_get(row, 'phone_1')),
                        clean_data_decimal(safe_get(row, 'phone_2')),
                        safe_get(row, 'category'),
                        safe_get(row, 'sub_category'),
                        safe_get(row, 'email'),
                        safe_get(row, 'url'),
                        safe_get(row, 'ratings'),
                        safe_get(row, 'address'),
                        safe_get(row,'pincode'),
                        safe_get(row,'area'),
                        safe_get(row,'city'),
                        safe_get(row,'state'),
                        safe_get(row,'country'),
                        )
                        chunk_data.append(row_tuple)

            # execute batch insert
                    insert_query = '''
                        INSERT INTO asklaila (
                            name, number1, number2, category,
                            subcategory, email, url, ratings, address, pincode, area, city, state, country
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            number1 = VALUES(number1),
                            number2 = VALUES(number2),
                            category = VALUES(category),
                            subcategory = VALUES(subcategory),
                            email = VALUES(email),
                            url = VALUES(url),
                            ratings = VALUES(ratings),
                            pincode = VALUES(pincode),
                            area = VALUES(area),
                            city = VALUES(city),
                            state = VALUES(state),
                            country = VALUES(country);
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