import os
import pandas as pd
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func
from model.master_table_model import MasterTable
from utils.safe_get import safe_get
from utils.drop_non_essential_indexes import drop_non_essential_indexes
from utils.create_non_essential_indexes import create_non_essential_indexes
from utils.clean_data_decimal import clean_data_decimal

CHUNK_SIZE = 2000
BATCH_SIZE = 100

def upload_master_csv(file_paths, session, report):
    inserted = 0
    total_processed = 0
    rows_since_commit = 0
    
    missing_phone = 0
    missing_email = 0
    missing_address = 0
    
    # City matching counters
    city_matched = 0
    city_unmatched = 0

    city_set = set()
    area_set = set()
    category_set = set()
    
    # Load valid cities from master_table (one-time query)
    valid_cities = _load_valid_cities(session)

    connection = session.connection()
    cursor = connection.connection.cursor()
    
    non_essential_indexes = ['business_category', 'area', 'city', 'email', 'data_source', 'created_at']
    
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
                    
                    if not primary_phone:
                        missing_phone += 1
                    if not email:
                        missing_email += 1
                    if not address:
                        missing_address += 1

                    city = safe_get(row, "city")
                    area = safe_get(row, "area")
                    category = safe_get(row, "business_category")
                    
                    # ✅ City matching check with in-memory update
                    if city:
                        city_lower = city.lower().strip()
                        
                        if city_lower in valid_cities:
                            city_matched += 1
                        else:
                            city_unmatched += 1
                            # Add new city to in-memory set for future matches
                            valid_cities.add(city_lower)
                        
                        city_set.add(city)
                    
                    if area:
                        area_set.add(area)
                    if category:
                        category_set.add(category)

                    batch.append({
                        "global_business_id": global_id,
                        "business_id": safe_get(row, "business_id"),
                        "business_name": safe_get(row, "business_name"),
                        "business_category": category,
                        "business_subcategory": safe_get(row, "business_subcategory"),
                        "ratings": clean_data_decimal(safe_get(row, "ratings")),
                        "primary_phone": primary_phone,
                        "secondary_phone": clean_data_decimal(safe_get(row, "secondary_phone")),
                        "other_phones": clean_data_decimal(safe_get(row, "other_phones")),
                        "virtual_phone": clean_data_decimal(safe_get(row, "virtual_phone")),
                        "whatsapp_phone": clean_data_decimal(safe_get(row, "whatsapp_phone")),
                        "email": email,
                        "website_url": safe_get(row, "website_url"),
                        "address": address,
                        "area": area,
                        "city": city,
                        "state": safe_get(row, "state") or "Unknown",
                        "pincode": clean_data_decimal(safe_get(row, "pincode")),
                        "country": safe_get(row, "country") or "India",
                        "data_source": "CSV"
                    })

                    if len(batch) >= BATCH_SIZE:
                        print(f"📝 Processing: {total_processed}")
                        ins = _commit_batch_upsert(batch, session)
                        inserted += ins
                        batch.clear()
                    
                    # Har 50K rows pe commit
                    if rows_since_commit >= 50000:
                        print(f"💾 Committing at {total_processed} rows...")
                        session.commit()
                        rows_since_commit = 0
                        
                        # Report update
                        _update_report(session, report, total_processed, inserted, 
                                     city_set, area_set, category_set, 
                                     missing_phone, missing_email, missing_address,
                                     city_matched, city_unmatched)

                if batch:
                    ins = _commit_batch_upsert(batch, session)
                    inserted += ins
        
        # Final commit
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
    """Load unique cities from master_table (one-time query)"""
    try:
        result = session.query(
            func.lower(MasterTable.city)
        ).distinct().all()
        
        return {city[0].strip() for city in result if city[0]}
    except Exception as e:
        print(f"⚠️ Error loading cities: {e}")
        return set()


def _commit_batch_upsert(batch, session):
    try:
        stmt = insert(MasterTable).values(batch)
        
        update_dict = {
            "business_name": stmt.inserted.business_name,
            "business_category": stmt.inserted.business_category,
            "ratings": stmt.inserted.ratings,
            "primary_phone": stmt.inserted.primary_phone,
            "email": stmt.inserted.email,
            "address": stmt.inserted.address,
            "city": stmt.inserted.city,
            "state": stmt.inserted.state,
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