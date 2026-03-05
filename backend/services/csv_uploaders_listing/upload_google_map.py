import csv
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get

def upload_google_map_data(file_paths):
    """
    Memory-safe streaming uploader for Google Map CSV data.
    Uses native csv module to avoid Pandas OOM risks for large files.
    """
    if not file_paths:
        raise ValueError("No file paths provided for upload.")
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    inserted = 0
    batch_size = 2000 # Optimized batch size for stability
    
    try:
        for file_path in file_paths:
            with open(file_path, newline='', encoding='utf-8') as f:
                # Use csv.DictReader for field-name based access
                reader = csv.DictReader(f)
                
                # Sanitize field names (handling spaces like the old Pandas renaming)
                fieldnames = [fn.replace(" ", "_") for fn in reader.fieldnames]
                reader.fieldnames = fieldnames
                
                chunk_data = []
                for row in reader:
                    row_tuple = (
                        safe_get(row, 'Business_Name'),
                        safe_get(row, 'Phone'),
                        safe_get(row, 'Email'),
                        safe_get(row, 'Website'),
                        safe_get(row, 'Address'),
                        safe_get(row, 'Latitude'),
                        safe_get(row, 'Longitude'),
                        safe_get(row, 'Rating'),
                        safe_get(row, 'Review'),
                        safe_get(row, 'Category'),
                        safe_get(row, 'Image1'),
                        safe_get(row, 'Image2'),
                        safe_get(row, 'Image3'),
                        safe_get(row, 'Image4'),
                        safe_get(row, 'Image5'),
                        safe_get(row, 'Image6'),
                        safe_get(row, 'Image7'),
                        safe_get(row, 'Image8'),
                        safe_get(row, 'Image9'),
                        safe_get(row, 'Image10'),
                        safe_get(row, 'WorkingHour'),
                        safe_get(row, 'Facebookprofile'),
                        safe_get(row, 'instagramprofile'),
                        safe_get(row, 'linkedinprofile'),
                        safe_get(row, 'Twitterprofile'),
                        safe_get(row, 'Source'),
                        safe_get(row, 'Id'),
                        safe_get(row, 'GMapsLink'),
                        safe_get(row, 'OrganizationName'),
                        safe_get(row, 'OrganizationId'),
                        safe_get(row, 'RateStars'),
                        safe_get(row, 'ReviewsTotalCount'),
                        safe_get(row, 'PricePolicy'),
                        safe_get(row, 'OrganizationCategory'),
                        safe_get(row, 'OrganizationAddress'),
                        safe_get(row, 'OrganizationLocatedInInformation'),
                        safe_get(row, 'OrganizationWebsite'),
                        safe_get(row, 'OrganizationPhoneNr'),
                        safe_get(row, 'OrganizationPlusCode'),
                        safe_get(row, 'OrganizationWorkTime'),
                        safe_get(row, 'OrganizationPopularLoadTimes'),
                        safe_get(row, 'OrganizationLatitude'),
                        safe_get(row, 'OrganizationLongitude'),
                        safe_get(row, 'OrganizationShortDescription'),
                        safe_get(row, 'OrganizationHeadPhotoFile'),
                        safe_get(row, 'OrganizationHeadPhotoURL'),
                        safe_get(row, 'OrganizationHeadPhotosFiles'),
                        safe_get(row, 'OrganizationHeadPhotosURLs'),
                        safe_get(row, 'OrganizationEmail'),
                        safe_get(row, 'OrganizationFacebook'),
                        safe_get(row, 'OrganizationInstagram'),
                        safe_get(row, 'OrganizationTwitter'),
                        safe_get(row, 'OrganizationLinkedIn'),
                        safe_get(row, 'OrganizationYouTube'),
                        safe_get(row, 'OrganizationContactsURL'),
                        safe_get(row, 'OrganizationYelp'),
                        safe_get(row, 'OrganizationTripAdvisor'),
                        safe_get(row, 'SearchRequest'),
                        safe_get(row, 'ShareLink'),
                        safe_get(row, 'ShareLinkOrganizationId'),
                        safe_get(row, 'EmbedMapCode'),
                    )
                    chunk_data.append(row_tuple)
                    
                    if len(chunk_data) >= batch_size:
                        _execute_batch(cursor, connection, chunk_data)
                        inserted += len(chunk_data)
                        chunk_data = []
                
                # Final chunk
                if chunk_data:
                    _execute_batch(cursor, connection, chunk_data)
                    inserted += len(chunk_data)
        
        return inserted
    finally:
        cursor.close()
        connection.close()

def _execute_batch(cursor, connection, chunk_data):
    """Internal helper for batch execution."""
    query = '''
        INSERT INTO google_map (
            business_name, number, email, website, address, 
            latitude, longitude, rating, review, category,
            image1, image2, image3, image4, image5, image6, image7, image8, image9, image10,
            working_hour, facebook_profile, instagram_profile, linkedin_profile, twitter_profile,
            source_name, g_id, gmaps_link, organization_name, organization_id,
            rate_stars, reviews_total_count, price_policy, organization_category, organization_address,
            organization_locatedin_information, organization_website, organization_phone_number,
            organization_pluscode, organization_work_time, organization_popular_load_times,
            organiztion_latitude, organization_longitude, organization_short_description,
            organization_head_photo_file, organization_head_photo_url, organization_photos_files,
            organizatiion_photos_urls, organization_email, organization_facebook,
            organization_instagram, organization_twitter, organization_linkedin,
            organization_youtube, organization_contacts_url, organization_yelp,
            organization_trip_advisor, search_request, share_link,
            share_link_organization_id, embed_map_code
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE 
            number = VALUES(number),
            email = VALUES(email),
            website = VALUES(website),
            latitude = VALUES(latitude),
            longitude = VALUES(longitude),
            rating = VALUES(rating),
            review = VALUES(review),
            category = VALUES(category),
            working_hour = VALUES(working_hour),
            organization_phone_number = VALUES(organization_phone_number),
            organization_website = VALUES(organization_website)
    '''
    try:
        cursor.executemany(query, chunk_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Batch Insert Failed: {e}")
        raise
