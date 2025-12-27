import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_yellow_pages_data(file_paths):
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
                    chunk = chunk.rename(columns=lambda c: c.replace(" ", "_"))
                    chunk_data = []
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                            safe_get(row, 'Name'),
                            safe_get(row, 'Address'),
                            safe_get(row, 'Area'),
                            safe_get(row, 'Number'),
                            safe_get(row, 'Mail'),
                            safe_get(row, 'Category'),
                            safe_get(row, 'Pincode'),
                            safe_get(row, 'City'),
                            safe_get(row, 'State'),
                            safe_get(row, 'Country')
                        )

                        chunk_data.append(row_tuple)

                    insert_query = """
                        INSERT INTO yellow_pages (
                            name, address, area, number, email, category,
                            pincode, city, state, country
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        area = VALUES(area),
                        number = VALUES(number),
                        email = VALUES(email),
                        category = VALUES(category),
                        pincode = VALUES(pincode),
                        city = VALUES(city),
                        state = VALUES(state),
                        country = VALUES(country);
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
