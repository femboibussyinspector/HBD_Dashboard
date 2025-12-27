import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_college_dunia_data(file_paths):

    if not file_paths:
        raise ValueError("No file paths provided to upload.")
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
                    chunk = chunk.rename(columns = lambda c: c.replace(' ','_'))
                    chunk_data = []
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'Name'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'Area'),
                        safe_get(row, 'Avg_Fees'),
                        safe_get(row, 'Rating'),
                        safe_get(row, 'Number'),
                        safe_get(row, 'Website'),
                        safe_get(row, 'Country'),
                        safe_get(row, 'Subcategory'),
                        safe_get(row, 'Category'),
                        safe_get(row, 'Course_Details'),
                        safe_get(row, 'Duration'),
                        safe_get(row, 'Mail'),
                        safe_get(row, 'Requirement'),
                        )
                        chunk_data.append(row_tuple)

                    # execute batch insert
                    insert_query = '''
                        INSERT INTO college_dunia (
                            name, address, area, avg_fees, rating, number, website, country, subcategory, category, course_details, duration, email, requirement
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            area = VALUES(area),
                            avg_fees = VALUES(avg_fees),
                            rating = VALUES(rating),
                            number = VALUES(number),
                            website = VALUES(website),
                            country = VALUES(country),
                            subcategory = VALUES(subcategory),
                            category = VALUES(category),
                            course_details = VALUES(course_details),
                            duration = VALUES(duration),
                            email = VALUES(email),
                            requirement = VALUES(requirement);
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