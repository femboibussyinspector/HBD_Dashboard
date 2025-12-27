import pandas as pd
from database.mysql_connection import get_mysql_connection
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes

def upload_google_map_data(file_paths):
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
                currFile_chunks = pd.read_csv(file,chunksize = batch_size)
                for chunk in currFile_chunks:
                    chunk = chunk.rename(columns=lambda c: c.replace(" ", "_"))
                    chunk_data = []
                    for row in chunk.itertuples(index=False):
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

                # storing the valus in the database
                    upload_google_map_data_query = '''
                        INSERT INTO google_map (
                            business_name,
                            number,  
                            email ,
                            website ,
                            address , 
                            latitude ,
                            longitude ,
                            rating ,
                            review ,
                            category,
                            image1,
                            image2,
                            image3,
                            image4,
                            image5,
                            image6 ,
                            image7  ,
                            image8  ,
                            image9  ,
                            image10  ,
                            working_hour  ,
                            facebook_profile  ,
                            instagram_profile , 
                            linkedin_profile  ,
                            twitter_profile  ,
                            source_name,
                            g_id ,
                            gmaps_link  ,
                            organization_name ,
                            organization_id ,
                            rate_stars,
                            reviews_total_count  ,
                            price_policy  ,
                            organization_category ,
                            organization_address  ,
                            organization_locatedin_information  ,
                            organization_website  ,
                            organization_phone_number ,
                            organization_pluscode ,
                            organization_work_time  ,
                            organization_popular_load_times  ,
                            organiztion_latitude ,
                            organization_longitude ,
                            organization_short_description  ,
                            organization_head_photo_file  ,
                            organization_head_photo_url  ,
                            organization_photos_files  ,
                            organizatiion_photos_urls  ,
                            organization_email ,
                            organization_facebook  ,
                            organization_instagram  ,
                            organization_twitter  ,
                            organization_linkedin  ,
                            organization_youtube  ,
                            organization_contacts_url  ,
                            organization_yelp  ,
                            organization_trip_advisor  ,
                            search_request  ,
                            share_link  ,
                            share_link_organization_id  ,
                            embed_map_code ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
                            ON DUPLICATE KEY UPDATE 
                            number = VALUES(number),
                            email = VALUES(email),
                            website = VALUES(website),
                            latitude = VALUES(latitude),
                            longitude = VALUES(longitude) ,
                            rating = VALUES(rating),
                            review = VALUES(review),
                            category= VALUES(category),
                            image1= VALUES(image1),
                            image2= VALUES(image2),
                            image3= VALUES(image3),
                            image4= VALUES(image4),
                            image5= VALUES(image5),
                            image6 = VALUES(image6),
                            image7  = VALUES(image7),
                            image8 = VALUES(image8) ,
                            image9  = VALUES(image9),
                            image10 = VALUES(image10) ,
                            working_hour = VALUES(working_hour) ,
                            facebook_profile = VALUES(facebook_profile) ,
                            instagram_profile= VALUES(instagram_profile) , 
                            linkedin_profile = VALUES(linkedin_profile) ,
                            twitter_profile = VALUES(twitter_profile) ,
                            source_name= VALUES(source_name),
                            g_id = VALUES(g_id),
                            gmaps_link  = VALUES(gmaps_link),
                            organization_name= VALUES(organization_name) ,
                            organization_id = VALUES(organization_id),
                            rate_stars= VALUES(rate_stars),
                            reviews_total_count = VALUES(reviews_total_count) ,
                            price_policy = VALUES(price_policy) ,
                            organization_category = VALUES(organization_category),
                            organization_address = VALUES(organization_address) ,
                            organization_locatedin_information = VALUES(organization_locatedin_information) ,
                            organization_website = VALUES(organization_website) ,
                            organization_phone_number= VALUES(organization_phone_number) ,
                            organization_pluscode = VALUES(organization_pluscode),
                            organization_work_time = VALUES(organization_work_time) ,
                            organization_popular_load_times = VALUES(organization_popular_load_times) ,
                            organiztion_latitude = VALUES(organiztion_latitude),
                            organization_longitude = VALUES(organization_longitude),
                            organization_short_description = VALUES(organization_short_description) ,
                            organization_head_photo_file = VALUES(organization_head_photo_file) ,
                            organization_head_photo_url = VALUES(organization_head_photo_url) ,
                            organization_photos_files = VALUES(organization_photos_files) ,
                            organizatiion_photos_urls = VALUES(organizatiion_photos_urls) ,
                            organization_email = VALUES(organization_email),
                            organization_facebook = VALUES(organization_facebook) ,
                            organization_instagram = VALUES(organization_instagram) ,
                            organization_twitter = VALUES(organization_twitter) ,
                            organization_linkedin = VALUES(organization_linkedin) ,
                            organization_youtube = VALUES(organization_youtube) ,
                            organization_contacts_url = VALUES(organization_contacts_url) ,
                            organization_yelp = VALUES(organization_yelp) ,
                            organization_trip_advisor = VALUES(organization_trip_advisor) ,
                            search_request = VALUES(search_request) ,
                            share_link = VALUES(share_link) ,
                            share_link_organization_id = VALUES(share_link_organization_id) ,
                            embed_map_code = VALUES(embed_map_code)
                    '''
                    try:
                        cursor.executemany(upload_google_map_data_query,chunk_data)
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