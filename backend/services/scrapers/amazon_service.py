import os
import time
import random
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import re
from urllib.parse import unquote
# --- App & DB Imports ---
from extensions import db
from model.scraper_task import ScraperTask
from model.product_model.amazon_product import AmazonProduct

# --- TEMPORARY: Keep this for amazon_routes.py compatibility if needed ---
DB_CONFIG_AMAZON = {
    'host': 'host.docker.internal',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT')
}

ua = UserAgent()
BASE_URL = 'https://www.amazon.in'

def get_headers():
    return {
        'User-Agent': ua.random,
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.amazon.in/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def get_product_details(url):
    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=get_headers())
        
        # Log if request failed
        if response.status_code != 200:
            print(f"xx Failed to fetch URL: {url} (Status: {response.status_code})")
            return None
        
        if 'captcha' in response.text.lower():
            print("xx Captcha encountered. Skipping.")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. ASIN (Required)
        asin = None
            
            # specific patterns for Amazon URLs
            # We unquote first to handle "sspa" (sponsored) links where the ASIN is encoded like %2Fdp%2F
        clean_url = unquote(url)
            
            # Regex: Look for /dp/ or /gp/product/ followed by exactly 10 alphanumeric chars
        match = re.search(r'(?:/dp/|/gp/product/)([A-Z0-9]{10})', clean_url)
            
        if match:
                asin = match.group(1)
        else:
                print(f"xx No ASIN found in URL: {url[:60]}...") # Print first 60 chars to debug
                return None

        # 2. Extract Fields (With Safe Defaults for Strict DB)
        name_elem = soup.select_one("#productTitle") or \
                soup.select_one("h1#title") or \
                soup.select_one("h1.a-size-large") or \
                soup.select_one("h1.a-size-medium") or \
                    soup.select_one("#titleSection h1")
        name = name_elem.get_text().strip() if name_elem else "Unknown Product"

        # Debugging: If still unknown, print the page title to see what Amazon served
        if name == "Unknown Product":
            page_title = soup.title.string.strip() if soup.title else "No Page Title"
        price_elem = soup.select_one('.a-price-whole')
        price = '₹' + price_elem.get_text().strip().replace(',', '') if price_elem else "₹0"

        rating_elem = soup.select_one('.a-icon-alt')
        rating_str = rating_elem.get_text().split()[0] if rating_elem else "0"
        try:
            rating = float(rating_str)
        except:
            rating = 0.0
            
        brand_elem = soup.select_one('#bylineInfo')
        brand = brand_elem.get_text().strip() if brand_elem else "Unknown Brand"

        # --- RETURN ALL FIELDS (No None Allowed) ---
        return {
            'ASIN': asin,
            'Product_name': name,
            'price': price,
            'rating': rating,
            'Number_of_ratings': 0, 
            'Brand': brand,
            'Seller': "Unknown",
            'category': "Uncategorized",
            'subcategory': "",
            'sub_sub_category': "",
            'category_sub_sub_sub': "",
            'colour': "",
            'size_options': "",
            'description': "",
            'link': url,
            'Image_URLs': "",
            'About_the_items_bullet': "",
            'Product_details': {},    # Empty JSON dict for Strict DB
            'Additional_Details': {}, 
            'Manufacturer_Name': "Unknown"
        }
    except Exception as e:
        print(f"xx Error scraping {url}: {e}")
        return None

def scrape_amazon_search(search_term, pages=1, limit=1000):
    from app import app 
    
    with app.app_context():
        try:
            # Initialize Task
            task = ScraperTask(
                platform="Amazon",
                search_query=search_term, 
                status="RUNNING",
                progress=0,
                total_found=0
            )
            db.session.add(task)
            db.session.commit()
            
            print(f"\n>>> TASK STARTED: ID {task.id} | Query: '{search_term}' | Pages: {pages}")
            
            all_products_count = 0
            
            for page in range(1, pages + 1):
                # Check for STOP
                db.session.refresh(task)
                if task.status in ["STOPPED", "CANCELLED"]:
                    print(f"!!! Task {task.id} Stopped by User !!!")
                    break

                search_url = f"{BASE_URL}/s?k={requests.utils.quote(search_term)}&page={page}"
                print(f"\n--- Scraping Page {page}/{pages} ---")
                
                try:
                    response = requests.get(search_url, headers=get_headers())
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = [urljoin(BASE_URL, a['href']) for a in soup.select('a.a-link-normal.s-no-outline') if a.get('href')]
                        
                        print(f"Found {len(links)} product links on Page {page}.")
                        
                        page_saved_count = 0
                        for link in links:
                            if all_products_count >= limit: break
                            
                            p_data = get_product_details(link)
                            if p_data:
                                # Save with SQLAlchemy
                                existing = AmazonProduct.query.filter_by(ASIN=p_data['ASIN']).first()
                                if not existing:
                                    new_prod = AmazonProduct(**p_data)
                                    db.session.add(new_prod)
                                    all_products_count += 1
                                    page_saved_count += 1
                                    print(f" [V] Saved: {p_data['Product_name'][:40]}...")
                                else:
                                    print(f" [!] Duplicate ASIN skipped: {p_data['ASIN']}")
                            
                        # Commit batch per page
                        task.progress = int((page / pages) * 100)
                        task.total_found = all_products_count
                        db.session.commit()
                        print(f"--- Page {page} Commit Success. Total Saved: {all_products_count} ---")
                    
                    else:
                        print(f"xx Failed to load Search Page {page}. Status: {response.status_code}")

                except Exception as e:
                    print(f"xx Critical Error on Page {page}: {e}")

                if all_products_count >= limit: 
                    print("--- Limit Reached ---")
                    break

            task.status = "COMPLETED"
            db.session.commit()
            print(f"\n>>> TASK COMPLETED: ID {task.id} | Total Products: {all_products_count} <<<\n")

        except Exception as e:
            db.session.rollback()
            print(f"\nxxx TASK FAILED: {e} xxx\n")
            task.status = "FAILED"
            task.error_message = str(e)
            db.session.commit()