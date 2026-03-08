import re
import logging
from sqlalchemy import text, func
from model.master_table_model import MasterTable
from model.location_master import LocationMaster
from model.post_office import PostOffice
from extensions import db

logger = logging.getLogger(__name__)

# Common Indian State Name Mapping (Variations to Canonical)
STATE_SYNONYMS = {
    'andhra pradesh': 'Andhra Pradesh', 'ap': 'Andhra Pradesh',
    'arunachal pradesh': 'Arunachal Pradesh', 'ar': 'Arunachal Pradesh',
    'assam': 'Assam', 'as': 'Assam',
    'bihar': 'Bihar', 'br': 'Bihar',
    'chhattisgarh': 'Chhattisgarh', 'cg': 'Chhattisgarh',
    'goa': 'Goa', 'ga': 'Goa',
    'gujarat': 'Gujarat', 'gj': 'Gujarat', 'gujrat': 'Gujarat',
    'haryana': 'Haryana', 'hr': 'Haryana',
    'himachal pradesh': 'Himachal Pradesh', 'hp': 'Himachal Pradesh',
    'jharkhand': 'Jharkhand', 'jh': 'Jharkhand',
    'karnataka': 'Karnataka', 'ka': 'Karnataka',
    'kerala': 'Kerala', 'kl': 'Kerala',
    'madhya pradesh': 'Madhya Pradesh', 'mp': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra', 'mh': 'Maharashtra',
    'manipur': 'Manipur', 'mn': 'Manipur',
    'meghalaya': 'Meghalaya', 'ml': 'Meghalaya',
    'mizoram': 'Mizoram', 'mz': 'Mizoram',
    'nagaland': 'Nagaland', 'nl': 'Nagaland',
    'odisha': 'Odisha', 'or': 'Odisha',
    'punjab': 'Punjab', 'pb': 'Punjab',
    'rajasthan': 'Rajasthan', 'rj': 'Rajasthan',
    'sikkim': 'Sikkim', 'sk': 'Sikkim',
    'tamil nadu': 'Tamil Nadu', 'tn': 'Tamil Nadu',
    'telangana': 'Telangana', 'tg': 'Telangana', 'ts': 'Telangana',
    'tripura': 'Tripura', 'tr': 'Tripura',
    'uttar pradesh': 'Uttar Pradesh', 'up': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand', 'uk': 'Uttarakhand',
    'west bengal': 'West Bengal', 'wb': 'West Bengal',
    'delhi': 'Delhi', 'dl': 'Delhi', 'new delhi': 'Delhi', 'ncr': 'Delhi',
}

def extract_location_from_address(address):
    """
    Extracts pincode, city, and state from an address string using regex.
    """
    if not address:
        return None, None, None

    # 1. Extract Pincode (6 digits)
    pincode_match = re.search(r'\b(\d{6})\b', address)
    pincode = pincode_match.group(1) if pincode_match else None

    # 2. Extract State (Look for known state names/synonyms at the end)
    state = None
    address_lower = address.lower()
    for synonym, canonical in STATE_SYNONYMS.items():
        if re.search(rf'\b{synonym}\b', address_lower):
            state = canonical
            break

    # 3. Extract City (Heuristic: often before pincode or state)
    # This is a bit harder without a list of all cities, but we can try to find 
    # the word immediately preceding the pincode if it's not a state.
    city = None
    parts = [p.strip() for p in re.split(r'[,|\-\n]', address)]
    
    # Reverse search through parts to find something that looks like a city
    for part in reversed(parts):
        # Skip if it's just the pincode or state
        if pincode and pincode in part:
            part = part.replace(pincode, '').strip()
        if state and state.lower() in part.lower():
            part = re.sub(rf'\b{state}\b', '', part, flags=re.IGNORECASE).strip()
        
        if part and len(part) > 3 and not any(char.isdigit() for char in part):
            city = part
            break

    return area_cleanup(None), city_cleanup(city), state_cleanup(state), pincode

def area_cleanup(val):
    if not val: return None
    return val.strip().title()

def city_cleanup(val):
    if not val: return None
    return val.strip().title()

def state_cleanup(val):
    if not val: return None
    return val.strip().title()

def get_canonical_location(session, area=None, city=None, state=None, pincode=None):
    """
    Look up canonical location details from LocationMaster or PostOffice tables.
    """
    # 1. Try Pincode Lookup (PostOffice table is best for this)
    if pincode:
        po = session.query(PostOffice).filter(PostOffice.pincode == pincode).first()
        if po:
            return {
                'area': po.area or area,
                'city': po.city or city,
                'state': po.state or state,
                'pincode': pincode
            }

    # 2. Try Area + City Match in LocationMaster
    if area and city:
        lm = session.query(LocationMaster).filter(
            func.lower(LocationMaster.area_name) == area.lower(),
            func.lower(LocationMaster.city_name) == city.lower()
        ).first()
        if lm:
            return {
                'area': lm.area_name,
                'city': lm.city_name,
                'state': lm.state_full_name,
                'pincode': pincode
            }

    # 3. Try City Match in LocationMaster if area is unknown
    if city:
        lm = session.query(LocationMaster).filter(
            func.lower(LocationMaster.city_name) == city.lower()
        ).first()
        if lm:
            return {
                'area': area,
                'city': lm.city_name,
                'state': lm.state_full_name,
                'pincode': pincode
            }

    return {
        'area': area,
        'city': city,
        'state': state,
        'pincode': pincode
    }

def process_master_table_fixes(session, limit=1000):
    """
    Identifies rows with missing location data and applies fixes.
    """
    # Rows where area or city or pincode is missing
    # In master_table, state is NOT NULL, but it might be "Unknown" or "India" or generic
    rows = session.query(MasterTable).filter(
        (MasterTable.area == None) | (MasterTable.area == '') |
        (MasterTable.city == None) | (MasterTable.city == '') |
        (MasterTable.pincode == None) | (MasterTable.pincode == '')
    ).limit(limit).all()

    fixed_count = 0
    for row in rows:
        needs_fix = False
        
        # Initial extraction from address if missing
        ext_area, ext_city, ext_state, ext_pin = extract_location_from_address(row.address)
        
        current_area = row.area or ext_area
        current_city = row.city or ext_city
        current_state = row.state if row.state not in [None, '', 'Unknown', 'India'] else ext_state
        current_pin = row.pincode or ext_pin
        
        # Canonical lookup
        canonical = get_canonical_location(session, current_area, current_city, current_state, current_pin)
        
        if canonical['area'] and row.area != canonical['area']:
            row.area = canonical['area']
            needs_fix = True
        if canonical['city'] and row.city != canonical['city']:
            row.city = canonical['city']
            needs_fix = True
        if canonical['state'] and row.state != canonical['state']:
            row.state = canonical['state']
            needs_fix = True
        if canonical['pincode'] and row.pincode != canonical['pincode']:
            row.pincode = canonical['pincode']
            needs_fix = True
            
        if needs_fix:
            fixed_count += 1
            if fixed_count % 100 == 0:
                session.commit()
                logger.info(f"Fixed {fixed_count} records...")

    session.commit()
    return fixed_count
