import os
import pandas as pd
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func
from model.master_table_model import MasterTable
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes
from utils.clean_data_decimal import clean_data_decimal
from services.location_validator_service import extract_location_from_address, get_canonical_location

CHUNK_SIZE = 2000
BATCH_SIZE = 100

def upload_master_csv(file_paths, session, report):
    inserted = 0
    total_processed = 0
    rows_since_commit = 0
    
    missing_phone = 0
    missing_email = 0
    missing_address = 0
    
    city_matched = 0
    city_unmatched = 0

    city_set = set()
    area_set = set()
    category_set = set()
    
    valid_cities = _load_valid_cities(session)

    connection = session.connection()
    cursor = connection.connection.cursor()
    
    # Updated non-essential indexes based on the new schema
    non_essential_indexes = ['business_category', 'area', 'city', 'district', 'email', 'data_source', 'asin', 'ifsc', 'created_at']
    
    try:
        print("🔧 Dropping indexes...")
        drop_non_essential_indexes(cursor, 'master_table', non_essential_indexes)

        for file in file_paths:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")

            for chunk in pd.read_csv(file, chunksize=CHUNK_SIZE):
                chunk = chunk.where(pd.notna(chunk), None)
                batch = []

                for row in chunk.itertuples(index=False):
                    total_processed += 1
                    rows_since_commit += 1

                    global_id = safe_get(row, "global_business_id")
                    if not global_id:
                        continue
                    
                    primary_phone = clean_data_decimal(safe_get(row, "primary_phone"))
                    email = safe_get(row, "email")
                    address = safe_get(row, "address")
                    
                    if not primary_phone: missing_phone += 1
                    if not email: missing_email += 1
                    if not address: missing_address += 1

                    city = safe_get(row, "city")
                    area = safe_get(row, "area")
                    category = safe_get(row, "business_category")
                    
                    if city:
                        city_lower = city.lower().strip()
                        if city_lower in valid_cities:
                            city_matched += 1
                        else:
                            city_unmatched += 1
                            valid_cities.add(city_lower)
                        city_set.add(city)
                    
                    if area: area_set.add(area)
                    if category: category_set.add(category)

                    # ✅ ADDED ALL NEW COLUMNS HERE
                    batch.append({
                        "global_business_id": global_id,
                        "business_id": safe_get(row, "business_id"),
                        "asin": safe_get(row, "asin"),
                        "ifsc": safe_get(row, "ifsc"),
                        "micr": safe_get(row, "micr"),
                        "branch_code": safe_get(row, "branch_code"),
                        "branch": safe_get(row, "branch"),
                        "price": clean_data_decimal(safe_get(row, "price")),
                        "listPrice": clean_data_decimal(safe_get(row, "listPrice")),
                        "isBestSeller": safe_get(row, "isBestSeller"),
                        "boughtInLastMonth": safe_get(row, "boughtInLastMonth"),
                        "ImgUrl": safe_get(row, "ImgUrl"),
                        "business_name": safe_get(row, "business_name"),
                        "business_category": category,
                        "business_subcategory": safe_get(row, "business_subcategory"),
                        "ratings": clean_data_decimal(safe_get(row, "ratings")),
                        "stars": safe_get(row, "stars"),
                        "reviews": clean_data_decimal(safe_get(row, "reviews")),
                        "primary_phone": primary_phone,
                        "secondary_phone": clean_data_decimal(safe_get(row, "secondary_phone")),
                        "other_phones": clean_data_decimal(safe_get(row, "other_phones")),
                        "virtual_phone": clean_data_decimal(safe_get(row, "virtual_phone")),
                        "whatsapp_phone": clean_data_decimal(safe_get(row, "whatsapp_phone")),
                        "email": email,
                        "website_url": safe_get(row, "website_url"),
                        "facebook_url": safe_get(row, "facebook_url"),
                        "linkedin_url": safe_get(row, "linkedin_url"),
                        "twitter_url": safe_get(row, "twitter_url"),
                        "address": address,
                        "area": area,
                        "city": city,
                        "district": safe_get(row, "district"),
                        "state": safe_get(row, "state") or "Unknown",
                        "pincode": clean_data_decimal(safe_get(row, "pincode")),
                    }
                    
                    # --- Location Validation & Fix ---
                    # 1. Initial extraction from address if missing
                    ext_area, ext_city, ext_state, ext_pin = extract_location_from_address(address)
                    
                    current_area = area or ext_area
                    current_city = city or ext_city
                    current_state = safe_get(row, "state") if safe_get(row, "state") not in [None, '', 'Unknown', 'India'] else ext_state
                    current_pin = clean_data_decimal(safe_get(row, "pincode")) or ext_pin
                    
                    # 2. Canonical lookup (pass session for DB access)
                    canonical = get_canonical_location(session, current_area, current_city, current_state, current_pin)
                    
                    # --- Prepare Batch Record ---
                    batch.append({
                        "global_business_id": global_id,
                        "business_id": safe_get(row, "business_id"),
                        "asin": safe_get(row, "asin"),
                        "ifsc": safe_get(row, "ifsc"),
                        "micr": safe_get(row, "micr"),
                        "branch_code": safe_get(row, "branch_code"),
                        "branch": safe_get(row, "branch"),
                        "price": clean_data_decimal(safe_get(row, "price")),
                        "listPrice": clean_data_decimal(safe_get(row, "listPrice")),
                        "isBestSeller": safe_get(row, "isBestSeller"),
                        "boughtInLastMonth": safe_get(row, "boughtInLastMonth"),
                        "ImgUrl": safe_get(row, "ImgUrl"),
                        "business_name": safe_get(row, "business_name"),
                        "business_category": category,
                        "business_subcategory": safe_get(row, "business_subcategory"),
                        "ratings": clean_data_decimal(safe_get(row, "ratings")),
                        "stars": safe_get(row, "stars"),
                        "reviews": clean_data_decimal(safe_get(row, "reviews")),
                        "primary_phone": primary_phone,
                        "secondary_phone": clean_data_decimal(safe_get(row, "secondary_phone")),
                        "other_phones": clean_data_decimal(safe_get(row, "other_phones")),
                        "virtual_phone": clean_data_decimal(safe_get(row, "virtual_phone")),
                        "whatsapp_phone": clean_data_decimal(safe_get(row, "whatsapp_phone")),
                        "email": email,
                        "website_url": safe_get(row, "website_url"),
                        "facebook_url": safe_get(row, "facebook_url"),
                        "linkedin_url": safe_get(row, "linkedin_url"),
                        "twitter_url": safe_get(row, "twitter_url"),
                        "address": address,
                        "area": canonical['area'] or area,
                        "city": canonical['city'] or city,
                        "district": safe_get(row, "district"),
                        "state": canonical['state'] or safe_get(row, "state") or "Unknown",
                        "pincode": canonical['pincode'] or clean_data_decimal(safe_get(row, "pincode")),
                        "country": safe_get(row, "country") or "India",
                        "data_source": safe_get(row, "data_source") or "CSV"
                    })

                    if len(batch) >= BATCH_SIZE:
                        ins = _commit_batch_upsert(batch, session)
                        inserted += ins
                        batch.clear()
                    
                    if rows_since_commit >= 50000:
                        session.commit()
                        rows_since_commit = 0
                        _update_report(session, report, total_processed, inserted, 
                                     city_set, area_set, category_set, 
                                     missing_phone, missing_email, missing_address,
                                     city_matched, city_unmatched)

                if batch:
                    ins = _commit_batch_upsert(batch, session)
                    inserted += ins
        
        session.commit()

    finally:
        print("🔧 Recreating indexes...")
        try:
            create_non_essential_indexes(cursor, 'master_table', non_essential_indexes)
            print("✅ Indexes recreated")
        except Exception as e:
            print(f"⚠️ Index error: {e}")
        finally:
            cursor.close()

    _update_report(session, report, total_processed, inserted, 
                 city_set, area_set, category_set, 
                 missing_phone, missing_email, missing_address,
                 city_matched, city_unmatched)

def _load_valid_cities(session):
    try:
        result = session.query(func.lower(MasterTable.city)).distinct().all()
        return {city[0].strip() for city in result if city[0]}
    except Exception as e:
        print(f"⚠️ Error loading cities: {e}")
        return set()

def _commit_batch_upsert(batch, session):
    try:
        stmt = insert(MasterTable).values(batch)
        
        # ✅ UPDATED DICT TO INCLUDE NEW FIELDS ON DUPLICATE UPDATE
        update_dict = {
            "business_name": stmt.inserted.business_name,
            "business_category": stmt.inserted.business_category,
            "business_subcategory": stmt.inserted.business_subcategory,
            "price": stmt.inserted.price,
            "ImgUrl": stmt.inserted.ImgUrl,
            "ratings": stmt.inserted.ratings,
            "reviews": stmt.inserted.reviews,
            "primary_phone": stmt.inserted.primary_phone,
            "secondary_phone": stmt.inserted.secondary_phone,
            "email": stmt.inserted.email,
            "website_url": stmt.inserted.website_url,
            "address": stmt.inserted.address,
            "area": stmt.inserted.area,
            "city": stmt.inserted.city,
            "district": stmt.inserted.district,
            "state": stmt.inserted.state,
            "pincode": stmt.inserted.pincode,
        }
        
        stmt = stmt.on_duplicate_key_update(**update_dict)
        session.execute(stmt)
        session.flush()
        
        return len(batch)
            
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {str(e)[:100]}")
        raise

def _update_report(session, report, total_processed, inserted, city_set, area_set, 
                  category_set, missing_phone, missing_email, missing_address,
                  city_matched, city_unmatched):
    try:
        report.total_processed = total_processed
        report.inserted = inserted
        report.total_cities = len(city_set)
        report.total_areas = len(area_set)
        report.total_categories = len(category_set)
        report.missing_primary_phone = missing_phone
        report.missing_email = missing_email
        report.missing_address = missing_address
        
        report.stats = {
            "city_match_status": {
                "matched": city_matched,
                "unmatched": city_unmatched
            }
        }
        
        session.commit()
    except:
        session.rollback()