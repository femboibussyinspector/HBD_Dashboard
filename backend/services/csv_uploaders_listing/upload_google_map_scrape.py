import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes


def upload_google_map_scrape_data(file_paths):
    if not file_paths:
        raise ValueError("No files provided for upload.")
    inserted = 0
    batch_size = 10000
    connection = get_mysql_connection()
    cursor = connection.cursor()
    upload_success = False
    try:
        for file in file_paths:
            with open(file,newline='',encoding='utf-8') as f:
                chunkFile_data = pd.read_csv(file,chunksize = batch_size)
                for chunk in chunkFile_data:
                    chunk_data = []
                    chunk = chunk.rename(columns = lambda c: c.replace(' ','_'))
                    for row in chunk.itertuples(index=False):
                        row_tuple = (
                        safe_get(row, 'Name'),
                        safe_get(row, 'Mobile_Number'),
                        safe_get(row, 'Review_Count'),
                        safe_get(row, 'Rating'),
                        safe_get(row, 'Catagory'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'Website'),
                        safe_get(row, 'Email_Id'),
                        safe_get(row, 'PlusCode'),
                        safe_get(row, 'Closing_Hours'),
                        safe_get(row, 'latitude'),
                        safe_get(row, 'latitude.1'),
                        safe_get(row, 'Instagram_Profile'),
                        safe_get(row, 'Facebook_Profile'),
                        safe_get(row, 'Linkedin_Profile'),
                        safe_get(row, 'Twitter_Profile'),
                        safe_get(row, 'Images_Folder'),
                        )
                        chunk_data.append(row_tuple)

                    # execute batch insert
                    insert_query = '''
                        INSERT INTO google_map_scrape (
                            name, number, review_count, rating, category, address, website, email, pluscode, closing_hours, latitude, longitude, instagram_profile, facebook_profile, linkedin_profile, twitter_profile, images_folder
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            number = VALUES(number),
                            review_count = VALUES(review_count),
                            rating = VALUES(rating),
                            category = VALUES(category),
                            website = VALUES(website),
                            email = VALUES(email),
                            pluscode = VALUES(pluscode),
                            closing_hours = VALUES(closing_hours),
                            latitude = VALUES(latitude),
                            longitude = VALUES(longitude),
                            instagram_profile = VALUES(instagram_profile),
                            facebook_profile = VALUES(facebook_profile),
                            linkedin_profile = VALUES(linkedin_profile),
                            twitter_profile = VALUES(twitter_profile),
                            images_folder = VALUES(images_folder);
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
            