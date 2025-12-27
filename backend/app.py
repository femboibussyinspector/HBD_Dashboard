from flask import request, jsonify, render_template, redirect,Flask
from flask_cors import CORS
import os, sys, re, time, random, json, argparse, threading, csv, hashlib
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from fake_useragent import UserAgent    
from config import Config
from extensions import db, jwt, cors
import pandas as pd
import ast

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config.from_object(Config)

# Init extensions
db.init_app(app)
jwt.init_app(app)
cors(app)

# Import all SQLAlchemy models so that db.create_all() works
from model.user import User
from model.amazon_product_model import AmazonProduct
from model.googlemap_data import GooglemapData
from model.item_csv_model import ItemData

with app.app_context():
    db.create_all()


# Load environment variables
load_dotenv()

# google map scrapper 
def safe_filename(name: str) -> str:
    """Sanitize filename to remove/replace invalid characters."""
    name = name.strip().replace(' ', '_')
    return re.sub(r'[^\w\-]', '_', name)

class Business(BaseModel):
    """Pydantic model for business data validation"""
    name: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    phone_number: Optional[str] = None
    reviews_count: Optional[int] = None
    reviews_average: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    area: Optional[str] = None

    @field_validator('reviews_average')
    @classmethod
    def validate_rating(cls, v):
        if v is not None and (v < 0 or v > 5):
            raise ValueError('Rating must be between 0 and 5')
        return v

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    save_at: str = 'output'

    def dataframe(self):
        return pd.DataFrame([b.model_dump() for b in self.business_list])

    def save_to_excel(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)

    def save_to_mysql(self):
        """Save data to MySQL database using credentials from .env"""
        connection = None
        try:
            print("Saving to DB:", os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_NAME'))
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                port=os.getenv('DB_PORT')
            )

            if connection.is_connected():
                cursor = connection.cursor()
                
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS google_Map (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(500),
                    address TEXT,
                    website VARCHAR(500),
                    phone_number VARCHAR(100),
                    reviews_count INT,
                    reviews_average FLOAT,
                    category VARCHAR(255),
                    subcategory VARCHAR(500),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    area VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_business (name,address)
                )""")

                # Creating or inserting data for the incomplete entries
                
                # cursor.execute("""
                # CREATE TABLE IF NOT EXISTS businesses_incomplete (
                #     id INT AUTO_INCREMENT PRIMARY KEY,
                #     name VARCHAR(500),
                #     address TEXT,
                #     website VARCHAR(500),
                #     phone_number VARCHAR(100),
                #     reviews_count INT,
                #     reviews_average FLOAT,
                #     category VARCHAR(255),
                #     subcategory VARCHAR(500),
                #     city VARCHAR(100),
                #     state VARCHAR(100),
                #     area VARCHAR(500),
                #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                # )
                # """)

                # Creating or inserting data for the duplicate entries

                # cursor.execute("""
                # CREATE TABLE IF NOT EXISTS businesses_duplicates (
                #     id INT AUTO_INCREMENT PRIMARY KEY,
                #     name VARCHAR(500),
                #     address TEXT,
                #     website VARCHAR(500),
                #     phone_number VARCHAR(100),
                #     reviews_count INT,
                #     reviews_average FLOAT,
                #     category VARCHAR(255),
                #     subcategory VARCHAR(500),
                #     city VARCHAR(100),
                #     state VARCHAR(100),
                #     area VARCHAR(500),
                #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                # )
                # """)

                insert_query_complete_entries = """
                INSERT INTO google_Map (
                    name, address, website, phone_number,
                    reviews_count, reviews_average, category,
                    subcategory, city, state, area
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    website = VALUES(website),
                    phone_number = VALUES(phone_number),
                    reviews_count = VALUES(reviews_count),
                    reviews_average = VALUES(reviews_average),
                    subcategory = VALUES(subcategory),
                    area = VALUES(area)
                """

                # this will be used during the handling of duplicate entries
                # ON DUPLICATE KEY UPDATE
                #     website = VALUES(website),
                #     phone_number = VALUES(phone_number),
                #     reviews_count = VALUES(reviews_count),
                #     reviews_average = VALUES(reviews_average),
                #     subcategory = VALUES(subcategory),
                #     area = VALUES(area)

                insert_query_incomplete_entries = """
                INSERT INTO businesses_incomplete (
                    name, address, website, phone_number,
                    reviews_count, reviews_average, category,
                    subcategory, city, state, area
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                insert_query_duplicate_entries = """
                INSERT INTO businesses_duplicates (
                    name, address, website, phone_number,
                    reviews_count, reviews_average, category,
                    subcategory, city, state, area
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                for business in self.business_list:
                    cursor.execute(insert_query_complete_entries, (
                        business.name,
                        business.address,
                        business.website,
                        business.phone_number,
                        business.reviews_count,
                        business.reviews_average,
                        business.category,
                        business.subcategory,
                        business.city,
                        business.state,
                        business.area
                    ))

                connection.commit()
                print(f"✅ Successfully saved {len(self.business_list)} businesses to MySQL")

        except Error as e:
            print(f" MySQL Error: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

def run_scraper(search_list):
    """Run the scraper with the provided search list"""
    with sync_playwright() as p:
        print("playwright is running")
        browser = p.chromium.launch(headless=False)
        print("completed playwright")
        
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)

        for search_for_index, search_item in enumerate(search_list):
            category = search_item['category']
            city = search_item['city']
            state = search_item['state']

            search_query = f"{category}, {city}, {state}"
            print(f"-----\n{search_for_index} - {search_query}")

            page.locator('//input[@id="searchboxinput"]').fill(search_query)
            page.wait_for_timeout(3000)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)

                current_count = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()

                if current_count >= 1000:  # Default limit for API usage
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()[:1000]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                elif current_count == previously_counted:
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = current_count
                    print(f"Currently Scraped: {current_count}")

            business_list = BusinessList()

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(5000)

                    name_attr = 'aria-label'
                    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                    website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                    phone_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                    review_count_xpath = '//button[@jsaction="pane.reviewChart.moreReviews"]//span'
                    reviews_avg_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'
                    subcategory_xpath = '//div[contains(@aria-label, "stars")]/following-sibling::div[contains(@class, "fontBodyMedium")]'

                    business_data = {
                        'name': listing.get_attribute(name_attr) or "",
                        'address': page.locator(address_xpath).nth(0).inner_text() if page.locator(address_xpath).count() > 0 else "",
                        'website': page.locator(website_xpath).nth(0).inner_text() if page.locator(website_xpath).count() > 0 else "",
                        'phone_number': page.locator(phone_xpath).nth(0).inner_text() if page.locator(phone_xpath).count() > 0 else "",
                        'subcategory': page.locator(subcategory_xpath).nth(0).inner_text() if page.locator(subcategory_xpath).count() > 0 else "",
                        'category': category,
                        'city': city,
                        'state': state
                    }

                    if page.locator(review_count_xpath).count() > 0:
                        business_data['reviews_count'] = int(
                            page.locator(review_count_xpath).inner_text()
                            .split()[0]
                            .replace(',', '')
                            .strip()
                        )
                    else:
                        business_data['reviews_count'] = None

                    if page.locator(reviews_avg_xpath).count() > 0:
                        business_data['reviews_average'] = float(
                            page.locator(reviews_avg_xpath)
                            .get_attribute(name_attr)
                            .split()[0]
                            .replace(',', '.')
                            .strip()
                        )
                    else:
                        business_data['reviews_average'] = None

                    if business_data['address']:
                        addr_parts = business_data['address'].split(',')
                        business_data['area'] = ','.join(addr_parts[:2]).strip() if len(addr_parts) >= 2 else addr_parts[0].strip()
                    else:
                        business_data['area'] = ""

                    business = Business(**business_data)
                    business_list.business_list.append(business)

                except Exception as e:
                    print(f'Error occurred: {e}')

            print("Preparing to save files...")
            print("Businesses collected:", len(business_list.business_list))

            safe_name = safe_filename(f"google_maps_data_{category}_{city}_{state}")

            try:
                business_list.save_to_csv(safe_name)
                print("CSV saved successfully")
            except Exception as e:
                print("CSV Save Error:", e)

            try:
                business_list.save_to_mysql()
                print("MySQL Save Done")
            except Exception as e:
                print("MySQL Save Error:", e)


        browser.close()


@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    data = request.json
    if not data or 'queries' not in data:
        return jsonify({'error': 'Missing queries'}), 400
    
    search_list = []
    for line in data['queries']:
        parts = [part.strip() for part in line.split(',')]
        if len(parts) == 3:
            search_list.append({
                "category": parts[0],
                "city": parts[1],
                "state": parts[2]
            })
    
    if not search_list:
        return jsonify({'error': 'No valid queries provided'}), 400

    thread = threading.Thread(target=run_scraper, args=(search_list,))
    thread.start()
    
    return jsonify({
        'status': 'Scraping started',
        'searches': len(search_list)
    }), 202

@app.route('/api/results', methods=['GET'])
def api_results():
    connection = None
    try:
        print("Connecting with:", os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_NAME'))
        connection = mysql.connector.connect(
           host=os.getenv('DB_HOST'),
           user=os.getenv('DB_USER'),
           password=os.getenv('DB_PASSWORD'),
           database=os.getenv('DB_NAME'),
           port=os.getenv('DB_PORT')
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM google_Map LIMIT 1000")
        results = cursor.fetchall()
        return jsonify(results)
    except Error as e:
        print("Error connecting to database:", e)
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()

def main():
    """Original command-line functionality"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    if args.total:
        total = args.total
    else:
        total = 1_000_000

    search_list = []

    if args.search:
        search_list = [{"category": args.search, "city": "", "state": ""}]
    else:
        input_file_path = os.path.join(os.getcwd(), 'input.txt')
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                for line in file.readlines():
                    parts = [part.strip() for part in line.strip().split(',')]
                    if len(parts) == 3:
                        search_list.append({
                            "category": parts[0],
                            "city": parts[1],
                            "state": parts[2]
                        })
        if len(search_list) == 0:
            print("Error: You must either pass the -s search argument, or add searches to input.txt in the format: category,city,state")
            sys.exit()

    run_scraper(search_list)      
            
# amazone scrapper 
# MySQL connection config (use environment variables or hardcode for local)
DB_CONFIG_AMAZON = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD_PLAIN'),
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
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }

def get_product_details(url):
    print("Inside get_product_details:", url)
    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        if 'captcha' in response.text.lower():
            raise Exception("Captcha page encountered")
        soup = BeautifulSoup(response.text, 'html.parser')
        asin = url.split('/dp/')[1].split('/')[0] if '/dp/' in url else None
        title_selectors = [
            "#productTitle",
            "span.a-size-large.product-title-word-break",
            "h1.a-size-large.a-spacing-none",
            "span#title",
            "h1#title",
        ]

        name = None
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                name = elem.get_text().strip()
                break

        if not name:
            print("Title not found for:", url)
        price = soup.select_one('.a-price-whole')
        price = price.get_text().strip() if price else None
        if price:
            price = '₹' + price.replace(',', '')
        rating = soup.select_one('span[data-asin][class*="a-icon-alt"]')
        if not rating:
            rating = soup.select_one('.a-icon-alt')
        rating = rating.get_text().split()[0] if rating else None
        num_ratings = soup.select_one('#acrCustomerReviewText')
        num_ratings = num_ratings.get_text().split()[0].replace(',', '') if num_ratings else 0
        brand = soup.select_one('#bylineInfo')
        brand = brand.get_text().strip() if brand else None
        seller = None  # Seller info extraction can be added if needed
        category = None
        subcategory = None
        sub_sub_category = None
        category_sub_sub_sub = None
        colour = None
        size_options = None
        description = None
        link = url
        image_urls = []
        about_bullet = []
        product_details = {}
        additional_details = {}
        manufacturer_name = None
        # Add more extraction logic as needed
        return {
            'ASIN': asin,
            'Product_name': name,
            'price': price,
            'rating': float(rating) if rating else None,
            'Number_of_ratings': int(num_ratings) if num_ratings else 0,
            'Brand': brand,
            'Seller': seller,
            'category': category,
            'subcategory': subcategory,
            'sub_sub_category': sub_sub_category,
            'category_sub_sub_sub': category_sub_sub_sub,
            'colour': colour,
            'size_options': size_options,
            'description': description,
            'link': link,
            'Image_URLs': ' | '.join(image_urls) if image_urls else None,
            'About_the_items_bullet': ' | '.join(about_bullet) if about_bullet else None,
            'Product_details': json.dumps(product_details),
            'Additional_Details': json.dumps(additional_details),
            'Manufacturer_Name': manufacturer_name
        }
    except Exception as e:
        print(f"Error scraping product details: {e}")
        return None


def insert_products_to_db(products):
    if not products:
        return 0
    connection = None
    inserted = 0
    try:
        connection = mysql.connector.connect(**DB_CONFIG_AMAZON)
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS amazon_products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ASIN VARCHAR(20) UNIQUE,
            Product_name TEXT,
            price VARCHAR(50),
            rating FLOAT,
            Number_of_ratings INT,
            Brand VARCHAR(255),
            Seller VARCHAR(255),
            category VARCHAR(255),
            subcategory VARCHAR(255),
            sub_sub_category VARCHAR(255),
            category_sub_sub_sub VARCHAR(255),
            colour VARCHAR(255),
            size_options TEXT,
            description TEXT,
            link TEXT,
            Image_URLs TEXT,
            About_the_items_bullet TEXT,
            Product_details JSON,
            Additional_Details JSON,
            Manufacturer_Name VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
        cursor.execute(create_table_query)
        insert_query = '''
        INSERT INTO amazon_products (
            ASIN, Product_name, price, rating, Number_of_ratings, Brand, Seller, category, subcategory, sub_sub_category, category_sub_sub_sub, colour, size_options, description, link, Image_URLs, About_the_items_bullet, Product_details, Additional_Details, Manufacturer_Name
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Product_name=VALUES(Product_name),
            price=VALUES(price),
            rating=VALUES(rating),
            Number_of_ratings=VALUES(Number_of_ratings),
            Brand=VALUES(Brand),
            Seller=VALUES(Seller),
            category=VALUES(category),
            subcategory=VALUES(subcategory),
            sub_sub_category=VALUES(sub_sub_category),
            category_sub_sub_sub=VALUES(category_sub_sub_sub),
            colour=VALUES(colour),
            size_options=VALUES(size_options),
            description=VALUES(description),
            link=VALUES(link),
            Image_URLs=VALUES(Image_URLs),
            About_the_items_bullet=VALUES(About_the_items_bullet),
            Product_details=VALUES(Product_details),
            Additional_Details=VALUES(Additional_Details),
            Manufacturer_Name=VALUES(Manufacturer_Name)
        '''
        for product in products:
            cursor.execute(insert_query, (
                product['ASIN'],
                product['Product_name'],
                product['price'],
                product['rating'],
                product['Number_of_ratings'],
                product['Brand'],
                product['Seller'],
                product['category'],
                product['subcategory'],
                product['sub_sub_category'],
                product['category_sub_sub_sub'],
                product['colour'],
                product['size_options'],
                product['description'],
                product['link'],
                product['Image_URLs'],
                product['About_the_items_bullet'],
                product['Product_details'],
                product['Additional_Details'],
                product['Manufacturer_Name']
            ))
            inserted += 1
        connection.commit()
    except Error as e:
        print(f"Error inserting products: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
    return inserted

    
def scrape_amazon_search(search_term, pages=1, limit=1000):
    products = []
    previous_count = 0   # track number of links seen before

    for page in range(1, pages + 1):
        try:
            print(f"\n----- Scraping Page {page} -----")

            search_url = f"{BASE_URL}/s?k={requests.utils.quote(search_term)}&page={page}"
            time.sleep(random.uniform(1, 2))

            response = requests.get(search_url, headers=get_headers())
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            product_links = [
                urljoin(BASE_URL, a['href'])
                for a in soup.select('a.a-link-normal.s-no-outline')
                if a.get('href')
            ]

            print("Found links on this page:", len(product_links))

            # Stop condition when no links are found
            if len(product_links) == previous_count:
                print("No new product links appearing… stopping scraping.")
                break

            previous_count = len(product_links)

            # collect product details
            for link in product_links:
                if len(products) >= limit:
                    print(f"Reached the scraping limit of {limit} products.")
                    break

                print("Fetching product:", link)
                product_data = get_product_details(link)

                if product_data:
                    products.append(product_data)

                time.sleep(random.uniform(1.5, 4))

            if len(products) >= limit:
                break

        except Exception as e:
            print(f"Error on page {page}: {str(e)}")
            time.sleep(random.uniform(5, 10))
            continue

    # Save to CSV
    print("Saving to CSV...")

    # make output folder if not exists
    if not os.path.exists("output"):
        os.makedirs("output")

    filename = f"output/amazon_data_{search_term.replace(' ', '_')}.csv"

    # save list of dicts to CSV
    if products:
        keys = products[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(products)

        print(f"CSV saved successfully: {filename}")
    else:
        print("No products scraped. CSV not created.")

    # saving the data to db

    print("Saving data to MySQL…")
    inserted = insert_products_to_db(products)
    if inserted:
        print(f"Inserted {inserted} rows into DB.")
    else:
        print("No data inserted into DB.")

    print("Total products scraped:", len(products))
    return products


@app.route('/api/amazon_products', methods=['GET'])
def get_amazon_products():
    connection = None
    try:
        print("DEBUG → GET API using:", 
        os.getenv('DB_HOST'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')),
        os.getenv('DB_PORT')

        connection = mysql.connector.connect(**DB_CONFIG_AMAZON)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM amazon_products LIMIT 1000")
        results = cursor.fetchall()
        return jsonify(results)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection and connection.is_connected():
            connection.close()

@app.route('/api/scrape_amazon', methods=['POST'])
def scrape_and_insert():
    data = request.get_json()
    search_term = data.get('search_term')
    pages = int(data.get('pages', 1))
    if not search_term:
        return jsonify({'error': 'search_term is required'}), 400
    thread = threading.Thread(target=scrape_amazon_search, args=(search_term, pages))
    thread.start()
    return jsonify({"status": "started"}), 202


# uploader for amazon_products bulk data
@app.route('/upload_amazon_products_data', methods=["POST"])
def upload_amazon_products_data():

    connection = None
    inserted = 0
    try:
        connection = mysql.connector.connect(**DB_CONFIG_AMAZON)
        cursor = connection.cursor()
        if request.files:
            files = request.files.getlist("file")
            total_row_data = []
            
    except Error as e:
        print(f"Error uploading data inside the amazon_products table: {e}")
        return jsonify({
            "status": "error",
            "message": "Invalid CSV format"
        }), 400
    finally:
        if connection and connection.is_connected():
            connection.close()
    return jsonify({
    "status": "success"
})


# ROOT
@app.route('/')
def index():
   return jsonify({"message": "Flask API is running!"})

# Register blueprints
from routes.auth_route import auth_bp
app.register_blueprint(auth_bp)

# googlemapdata endpoint
from routes.googlemap import googlemap_bp
app.register_blueprint(googlemap_bp)

# upload product csv 
from routes.upload_product_csv import product_csv_bp
app.register_blueprint(product_csv_bp)

# upload item csv 
from routes.upload_item_csv import item_csv_bp
app.register_blueprint(item_csv_bp)

# complate incomplate data
from routes.amazon_product import amazon_products_bp
app.register_blueprint(amazon_products_bp)

# items data complate/incomplate
from routes.items_data import item_bp
app.register_blueprint(item_bp, url_prefix="/items")

# items data csv download
from routes.item_csv_download import item_csv_bp
app.register_blueprint(item_csv_bp)

# duplicate item
from routes.item_duplicate import item_duplicate_bp
app.register_blueprint(item_duplicate_bp)

# upload others csv
from routes.upload_others_csv import upload_others_csv_bp
app.register_blueprint(upload_others_csv_bp)

# Listing data routes
from routes.listing_routes.upload_asklaila_route import asklaila_bp
from routes.listing_routes.upload_atm_route import atm_bp
from routes.listing_routes.upload_bank_route import bank_bp
from routes.listing_routes.upload_college_dunia_route import college_dunia_bp
from routes.listing_routes.upload_freelisting_route import freelisting_bp
from routes.listing_routes.upload_google_map_route import google_map_bp
from routes.listing_routes.upload_google_map_scrape_route import google_map_scrape_bp
from routes.listing_routes.upload_heyplaces_route import heyplaces_bp
from routes.listing_routes.upload_justdial_route import justdial_bp
from routes.listing_routes.upload_magicpin_route import magicpin_bp
from routes.listing_routes.upload_nearbuy_route import nearbuy_bp
from routes.listing_routes.upload_pinda_route import pinda_bp
from routes.listing_routes.upload_post_office_route import post_office_bp
from routes.listing_routes.upload_schoolgis_route import schoolgis_bp
from routes.listing_routes.upload_shiksha_route import shiksha_bp
from routes.listing_routes.upload_yellow_pages_route import yellow_pages_bp
from routes.product_routes.upload_amazon_products_route import amazon_bp
from routes.product_routes.upload_vivo_route import vivo_bp
from routes.product_routes.upload_big_basket_route import upload_big_basket_route

blueprints_listing = [(asklaila_bp, "/asklaila"),
    (atm_bp, "/atm"),
    (bank_bp, "/bank"),
    (college_dunia_bp, "/college-dunia"),
    (freelisting_bp, "/freelisting"),
    (google_map_bp, "/google-map"),
    (google_map_scrape_bp, "/google-map-scrape"),
    (heyplaces_bp, "/heyplaces"),
    (justdial_bp, "/justdial"),
    (magicpin_bp, "/magicpin"),
    (nearbuy_bp, "/nearbuy"),
    (pinda_bp, "/pinda"),
    (post_office_bp, "/post-office"),
    (schoolgis_bp, "/schoolgis"),
    (shiksha_bp, "/shiksha"),
    (yellow_pages_bp, "/yellow-pages"),
    (amazon_bp,"/amazon"),
    (vivo_bp,"/vivo"),
    ]

for bp,prefix in blueprints_listing:
    app.register_blueprint(bp,url_prefix=prefix)

if __name__ == '__main__':
    import argparse
    import pandas as pd
    parser = argparse.ArgumentParser(description='Amazon Scraper API & CLI')
    parser.add_argument('--runserver', action='store_true', help='Run the Flask API server')
    parser.add_argument('--scrape', type=str, help='Search term to scrape from Amazon')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape (default: 1)')
    parser.add_argument('--show', action='store_true', help='Show product data as a table after scraping')
    args = parser.parse_args()

    if args.runserver:
        app.run(debug=True)
    elif args.scrape:
        print(f"Scraping Amazon for '{args.scrape}' ({args.pages} pages)...")
        scraped_products = scrape_amazon_search(args.scrape, args.pages)
        inserted = insert_products_to_db(scraped_products)
        print(f"Scraped: {len(scraped_products)} | Inserted/Updated: {inserted}")
        if args.show:
            # Fetch and display as table
            connection = None
            try:
                connection = mysql.connector.connect(**DB_CONFIG_AMAZON)
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM amazon_products ORDER BY created_at DESC LIMIT 20")
                results = cursor.fetchall()
                if results:
                    df = pd.DataFrame(results)
                    print(df.to_string(index=False))
                else:
                    print("No products found in the database.")
            except Error as e:
                print(f"Error fetching products: {e}")
            finally:
                if connection and connection.is_connected():
                    connection.close()
    else:
        parser.print_help()
print("Loaded DB:", os.getenv("DB_USER"), os.getenv("DB_NAME"))


