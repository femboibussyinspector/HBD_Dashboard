import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_india_mart_data(file_paths):
    if not file_paths:
        print("logic error")
        raise ValueError("No file provided to upload")
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 10000
    upload_success = False
    try:
        drop_non_essential_indexes(cursor,'india_mart',['stars','Price','categoryName'])
        connection.commit()
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:  
                chunkFile_data = pd.read_csv(file,chunksize=batch_size)
                for chunk in chunkFile_data:
                    chunk = chunk.rename(columns=lambda c:c.replace(' ','_'))
                    chunk_data=[]
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'asin'),                             
                        safe_get(row, 'title'),
                        safe_get(row, 'imgUrl'),
                        safe_get(row, 'productURL'),
                        safe_get(row, 'stars'),
                        safe_get(row, 'reviews'),
                        safe_get(row, 'price'),
                        safe_get(row, 'listPrice'),
                        safe_get(row, 'categoryName'),
                        safe_get(row, 'isBestSeller'),
                        safe_get(row, 'boughtInLastMonth'),
                        )
                        chunk_data.append(row_tuple)

                    # storing the valus in the database
                    upload_india_mart_data_query = '''
                    INSERT INTO india_mart (
                        asin, title, imgUrl, productUrl, stars, reviews, price, listPrice, categoryName, isBestSeller, boughtInLastMonth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        title = VALUES(title),
                        imgUrl = VALUES(imgUrl),
                        productUrl = VALUES(productUrl),
                        stars = VALUES(stars),
                        reviews = VALUES(reviews),
                        price = VALUES(price),
                        listPrice = VALUES(listPrice),
                        categoryName = VALUES(categoryName),
                        isBestSeller = VALUES(isBestSeller);

                '''
                    try:
                        cursor.executemany(upload_india_mart_data_query,chunk_data)
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
            create_non_essential_indexes(cursor,'india_mart',['stars','price','categoryName'])
            connection.commit()
        cursor.close()
        connection.close()
