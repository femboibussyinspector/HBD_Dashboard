import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_vivo_data(file_paths):
    if not file_paths:
        print("logic error")
        raise ValueError("No file provided to upload")
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 10000
    upload_success = False
    try:
        drop_non_essential_indexes(cursor,'vivo',['city','state'])
        connection.commit()
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:  
                chunkFile_data = pd.read_csv(file,chunksize=batch_size)
                for chunk in chunkFile_data:
                    chunk = chunk.rename(columns=lambda c:c.replace(' ','_'))
                    chunk_data=[]
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'POS_ID'),                             
                        safe_get(row, 'HARDWARE_ID'),
                        safe_get(row, 'STORE_ID'),
                        safe_get(row, 'MERCHANT_NAME'),
                        safe_get(row, 'STORE_NAME'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'City'),
                        safe_get(row, 'State'),
                        safe_get(row, 'Pin_code'),
                        )
                        chunk_data.append(row_tuple)

                    # storing the valus in the database
                    insert_query = '''
                    INSERT INTO vivo (
                        pos_id, hardware_id, store_id, merchant_name, store_name, address, city, state, pin_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        hardware_id = VALUES(hardware_id),
                        merchant_name = VALUES(merchant_name),
                        store_name = VALUES(store_name),
                        address = VALUES(address),
                        city = VALUES(city),
                        state = VALUES(state),
                        pin_code = VALUES(pin_code);

                '''
                    try:
                        cursor.executemany(insert_query,chunk_data)
                        connection.commit()
                        inserted+=len(chunk_data)
                    except Exception:
                        print("roll error")
                        connection.rollback()
                        raise 
        upload_success = True
        return inserted
    finally:
        if upload_success:
            create_non_essential_indexes(cursor,'vivo',['city','state'])
            connection.commit()
        cursor.close()
        connection.close()
