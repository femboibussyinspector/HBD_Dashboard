from gevent import monkey
monkey.patch_all()
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request
from dotenv import load_dotenv

from config import Config
from extensions import db, jwt, cors, mail, migrate

# --- Import Models ---
from model.user import User
from model.scraper_task import ScraperTask
from model.amazon_product_model import AmazonProduct
from model.googlemap_data import GoogleMapData # Correct Import
from model.item_csv_model import ItemData
from model.master_table_model import MasterTable
from model.upload_master_reports_model import UploadReport
from model.listing_master import ListingMaster
from model.heyplaces import HeyPlaces
# Existing Models
from model.asklaila import Asklaila
from model.atm import ATM
from model.bank import Bank
from model.college_dunia import CollegeDunia

# --- Import Blueprints ---
from routes.auth_route import auth_bp
from routes.scraper_routes import scraper_bp
from routes.amazon_routes import amazon_api_bp
from routes.googlemap import googlemap_bp # Correct Import
from routes.master_table import master_table_bp
from routes.upload_product_csv import product_csv_bp
from routes.upload_item_csv import item_csv_bp
from routes.amazon_product import amazon_products_bp

# Listing & Product Blueprints imports
from routes.items_data import item_bp
from routes.item_csv_download import item_csv_bp as item_csv_download_bp
from routes.item_duplicate import item_duplicate_bp
from routes.upload_others_csv import upload_others_csv_bp
from routes.listing_master_route import listing_master_bp

from routes.listing_routes.upload_asklaila_route import asklaila_bp
from routes.listing_routes.upload_atm_route import atm_bp
from routes.listing_routes.upload_bank_route import bank_bp
from routes.listing_routes.upload_college_dunia_route import college_dunia_bp
from routes.listing_routes.upload_freelisting_route import freelisting_bp
from routes.listing_routes.upload_google_map_route import google_map_bp as gmap_upload_bp
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
from routes.product_routes.upload_amazon_products_route import amazon_bp as amazon_upload_bp
from routes.product_routes.upload_vivo_route import vivo_bp
from routes.product_routes.upload_big_basket_route import bigbasket_bp
from routes.product_routes.upload_blinkit_route import blinkit_bp
from routes.product_routes.upload_dmart_route import dmart_bp
from routes.product_routes.upload_flipkart_products_route import flipkart_bp
from routes.product_routes.upload_india_mart_route import indiamart_bp
from routes.product_routes.upload_jio_mart_route import jiomart_bp
from routes.gdrive_etl_routes.validation_dashboard import validation_dashboard_bp
# --- Initialize App ---
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
cors.init_app(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) # Allow all origins for dev
mail.init_app(app)

with app.app_context():
    db.create_all()

# --- GLOBAL JWT PROTECTION ---
PUBLIC_ROUTES = [
    "/",
    "/auth/signup",
    "/auth/login",
    "/auth/logout",
    "/auth/forgot-password",
    "/auth/verify-otp",
    "/auth/reset-password",
    "/health",
    "/api/master-dashboard-stats",
    # Listing/master data public fetch routes (all with /api prefix)
    "/api/atm/fetch-data",
    "/api/bank/fetch-data",
    "/api/asklaila/fetch-data",
    "/api/college-dunia/fetch-data",
    "/api/post-office/fetch-data",
    # Legacy listing endpoints kept public for compatibility
    "/google-listings",
    "/listing-master",
    "/complete-data",
    # Validation dashboard
    "/api/validation/dashboard",
]

@app.before_request
def protect_all_routes():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200
        
    normalized_path = request.path.rstrip('/')
    normalized_public_routes = [route.rstrip('/') for route in PUBLIC_ROUTES]
    
    if normalized_path in normalized_public_routes or request.path in PUBLIC_ROUTES:
        return None
    
    try:
        verify_jwt_in_request()
    except Exception as e:
        print(f"❌ JWT REJECTED for {request.path}: {str(e)}") 
        return jsonify({"message": "Missing or invalid token", "error": str(e)}), 401

# --- Register Main Blueprints ---
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(scraper_bp, url_prefix="/api")
app.register_blueprint(amazon_api_bp, url_prefix="/api")

# CORRECT REGISTRATION FOR GOOGLE MAPS
app.register_blueprint(googlemap_bp, url_prefix='/api') 

app.register_blueprint(master_table_bp)
app.register_blueprint(product_csv_bp)
app.register_blueprint(item_csv_bp)
app.register_blueprint(amazon_products_bp)
app.register_blueprint(item_bp, url_prefix="/items")
app.register_blueprint(item_csv_download_bp)
app.register_blueprint(item_duplicate_bp)
app.register_blueprint(upload_others_csv_bp)
app.register_blueprint(listing_master_bp, url_prefix="/api")
app.register_blueprint(validation_dashboard_bp)

# --- Register Listing & Product Blueprints (Batch) ---
blueprints_listing = [
    (asklaila_bp, "/asklaila"), (atm_bp, "/atm"), (bank_bp, "/bank"),
    (college_dunia_bp, "/college-dunia"), (freelisting_bp, "/freelisting"),
    (gmap_upload_bp, "/google-map"), (google_map_scrape_bp, "/google-map-scrape"),
    (heyplaces_bp, "/heyplaces"), (justdial_bp, "/justdial"), (magicpin_bp, "/magicpin"),
    (nearbuy_bp, "/nearbuy"), (pinda_bp, "/pinda"), (post_office_bp, "/post-office"),
    (schoolgis_bp, "/schoolgis"), (shiksha_bp, "/shiksha"), (yellow_pages_bp, "/yellow-pages"),
    (amazon_upload_bp, "/amazon"), (vivo_bp, "/vivo"), (blinkit_bp, "/blinkit"),
    (dmart_bp, "/dmart"), (flipkart_bp, "/flipkart"), (indiamart_bp, "/india-mart"),
    (jiomart_bp, "/jio-mart"), (bigbasket_bp, "/big-basket")
]

for bp, prefix in blueprints_listing:
    app.register_blueprint(bp, url_prefix=prefix)

@app.route('/')
def index():
    return jsonify({"message": "Flask API is running! Clean and Modular."})

