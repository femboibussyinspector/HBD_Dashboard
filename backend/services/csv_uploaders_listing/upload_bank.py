import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_bank_data(file_paths):
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
                        safe_get(row, 'Bank'),
                        safe_get(row, 'IFSC'),
                        safe_get(row, 'MICR'),
                        safe_get(row, 'Branch_Code'),
                        safe_get(row, 'Branch'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'City'),
                        safe_get(row, 'District'),
                        safe_get(row, 'State'),
                        safe_get(row, 'Contact'),
                        )
                        chunk_data.append(row_tuple)

                    # execute batch insert
                    insert_query = '''
                        INSERT INTO bank_data (
                            bank, ifsc, micr, branch_code, branch, address, city, district, state, contact
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE
                            ifsc = VALUES(ifsc),
                            micr = VALUES(micr),
                            branch = VALUES(branch),
                            address = VALUES(address),
                            city = VALUES(city),
                            district = VALUES(district),
                            state = VALUES(state),
                            contact = VALUES(contact);
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
