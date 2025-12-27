from database.mysql_connection import get_mysql_connection
import pandas as pd
from utils.safe_get import safe_get
from utils.to_valid_json import to_valid_json
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_shiksha_data(file_paths):
    if not file_paths:
        raise ValueError("No files provided for upload.")
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 10000
    # upload_success = False
    try:
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:
                chunkFile_data = pd.read_csv(f,chunksize =batch_size )
                for chunk in chunkFile_data:
                    chunk = chunk.rename(columns = lambda c:c.replace(' ','_'))
                    chunk_data = []
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'Name'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'Area'),
                        safe_get(row, 'Latitude'),
                        safe_get(row, 'Longitude'),
                        safe_get(row, 'Admission_requirement'),
                        to_valid_json(safe_get(row, 'Courses')),
                        safe_get(row, 'Avg_Fees'),
                        safe_get(row, 'Salary'),
                        safe_get(row, 'Rating'),
                        safe_get(row, 'Number'),
                        safe_get(row, 'Website'),
                        to_valid_json(safe_get(row, 'Mail')),
                        safe_get(row, 'category'),
                        safe_get(row, 'country'),
                        )
                        chunk_data.append(row_tuple)

                # execute batch insert
                    insert_query = '''
                        INSERT INTO shiksha (
                            name, address, area, latitude, longitude, admission_requirement, courses, avg_fees, avg_salary, rating, number, website, email, category, country
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            area = VALUES(area),
                            latitude = VALUES(latitude),
                            longitude = VALUES(longitude),
                            admission_requirement = VALUES(admission_requirement),
                            courses = VALUES(courses),
                            avg_fees = VALUES(avg_fees),
                            avg_salary = VALUES(avg_salary),
                            rating = VALUES(rating),
                            number = VALUES(number),
                            website = VALUES(website),
                            email = VALUES(email),
                            category = VALUES(category),
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