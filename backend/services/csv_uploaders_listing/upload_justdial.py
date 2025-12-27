import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.clean_data_decimal import clean_data_decimal
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_justdial_data(file_paths):
    if not file_paths:
        raise ValueError("No files provided for upload")
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
                            safe_get(row, 'category'),
                            safe_get(row, 'city'),
                            safe_get(row, 'company'),
                            safe_get(row, 'area'),
                            safe_get(row, 'address'),
                            clean_data_decimal(safe_get(row, 'pin')),
                            safe_get(row, 'emailaddress'),
                            safe_get(row, 'virtualnumber'),
                            safe_get(row, 'whatsapp'),
                            safe_get(row, 'phone1'),
                            safe_get(row, 'phone2'),
                            safe_get(row, 'phone3'),
                            safe_get(row, 'latitude'),
                            safe_get(row, 'longitude'),
                            safe_get(row, 'rating'),
                            clean_data_decimal(safe_get(row, 'reviews')),
                            safe_get(row, 'website'),
                        )
                        chunk_data.append(row_tuple)

                    # execute batch insert
                    insert_query = '''
                        INSERT INTO justdial (
                            category, city, company, area, address, pin, email, virtualnumber, whatsapp, number1, number2, number3, latitude, longitude, rating, reviews, website
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            category = VALUES(category),
                            city = VALUES(city),
                            area = VALUES(area),
                            pin = VALUES(pin),
                            email = VALUES(email),
                            virtualnumber = VALUES(virtualnumber),
                            whatsapp = VALUES(whatsapp),
                            number1 = VALUES(number1),
                            number2 = VALUES(number2),
                            number3 = VALUES(number3),
                            latitude = VALUES(latitude),
                            longitude = VALUES(longitude),
                            rating = VALUES(rating),
                            reviews = VALUES(reviews),
                            website = VALUES(website);
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