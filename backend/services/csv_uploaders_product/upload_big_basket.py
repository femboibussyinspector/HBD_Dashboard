import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_big_basket_data(file_paths):
    if not file_paths:
        print("logic error")
        raise ValueError("No file provided to upload")
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 10000
    upload_success = False
    try:
        drop_non_essential_indexes(cursor,'big_basket',['category','brand','rating'])
        connection.commit()
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:  
                chunkFile_data = pd.read_csv(file,chunksize=batch_size)
                for chunk in chunkFile_data:
                    chunk = chunk.rename(columns=lambda c:c.replace(' ','_'))
                    chunk_data=[]
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'product'),                             
                        safe_get(row, 'category'),
                        safe_get(row, 'sub_category'),
                        safe_get(row, 'brand'),
                        safe_get(row, 'sale_price'),
                        safe_get(row, 'market_price'),
                        safe_get(row, 'type'),
                        safe_get(row, 'rating'),
                        safe_get(row, 'description'),
                        )
                        chunk_data.append(row_tuple)

                    # storing the valus in the database
                    insert_query = '''
                    INSERT INTO big_basket (
                        product, category, sub_category, brand, sale_price, market_price, type, rating, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        category = VALUES(category),
                        sub_category = VALUES(sub_category),
                        sale_price = VALUES(sale_price),
                        market_price = VALUES(market_price),
                        type = VALUES(type),
                        rating = VALUES(rating),
                        description = VALUES(description);

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
            create_non_essential_indexes(cursor,'big_basket',['category','brand','rating'])
            connection.commit()
        cursor.close()
        connection.close()
