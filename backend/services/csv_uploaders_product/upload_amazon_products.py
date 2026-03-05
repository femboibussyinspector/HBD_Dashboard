import csv
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_amazon_products_data(file_paths):
    """
    Memory-safe streaming uploader for Amazon product CSV data.
    Uses native csv module to avoid Pandas OOM risks for large files.
    """
    if not file_paths:
        raise ValueError("No file provided to upload")
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 2000
    upload_success = False
    
    try:
        drop_non_essential_indexes(cursor, 'amazon_products', ['stars', 'price', 'categoryName'])
        connection.commit()
        
        for file_path in file_paths:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Sanitize field names
                fieldnames = [fn.replace(" ", "_") for fn in reader.fieldnames]
                reader.fieldnames = fieldnames
                
                chunk_data = []
                for row in reader:
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
                    
                    if len(chunk_data) >= batch_size:
                        _execute_amazon_batch(cursor, connection, chunk_data)
                        inserted += len(chunk_data)
                        chunk_data = []
                
                if chunk_data:
                    _execute_amazon_batch(cursor, connection, chunk_data)
                    inserted += len(chunk_data)
                    
        upload_success = True
        return inserted
    finally:
        if upload_success:
            create_non_essential_indexes(cursor, 'amazon_products', ['stars', 'price', 'categoryName'])
            connection.commit()
        cursor.close()
        connection.close()

def _execute_amazon_batch(cursor, connection, chunk_data):
    """Internal helper for Amazon batch execution."""
    query = '''
        INSERT INTO amazon_products (
            asin, title, imgUrl, productUrl, stars, reviews, price, listPrice, categoryName, isBestSeller, boughtInLastMonth
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            imgUrl = VALUES(imgUrl),
            productUrl = VALUES(productUrl),
            stars = VALUES(stars),
            reviews = VALUES(reviews),
            price = VALUES(price),
            listPrice = VALUES(listPrice),
            categoryName = VALUES(categoryName),
            isBestSeller = VALUES(isBestSeller)
    '''
    try:
        cursor.executemany(query, chunk_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Amazon Batch Insert Failed: {e}")
        raise
