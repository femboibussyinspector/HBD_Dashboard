import sys
import warnings

# Suppress noisy library warnings
warnings.filterwarnings("ignore", message="urllib3.*charset_normalizer.*doesn't match")
warnings.filterwarnings("ignore", module="requests")

# Apply gevent monkey patching ONLY for production WSGI server, otherwise it breaks Ctrl+C in Flask dev server
if "--runserver" in sys.argv:
    from gevent import monkey
    monkey.patch_all()
import os
import sys

# Windows console encoding fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request
from dotenv import load_dotenv

from config import Config
from extensions import db, jwt, cors, mail, migrate

# --- Import Models ---
from model.user import User
from model.scraper_task import ScraperTask

from model.googlemap_data import GoogleMapData
from model.item_csv_model import ItemData
from model.master_table_model import MasterTable
from model.upload_master_reports_model import UploadReport
from model.listing_master import ListingMaster
from model.heyplaces import HeyPlaces
from model.location_master import LocationMaster

# Existing Models
from model.asklaila import Asklaila
from model.atm import ATM
from model.bank import Bank
from model.college_dunia import CollegeDunia
from model.justdial import JustDial
from model.magicpin import MagicPin
from model.nearbuy import NearBuy
from model.pinda import Pinda
from model.post_office import PostOffice
from model.schoolgis import SchoolGIS
from model.shiksha import Shiksha
from model.yellow_pages import YellowPages
from model.google_map_scrape import GoogleMapScrape

# --- Product Routes ---
from model.product_model.amazon_product import AmazonProduct
from model.product_model.bigbasket_product_model import BigBasket

# --- Import Blueprints ---
from routes.auth_route import auth_bp
from routes.scraper_routes import scraper_bp
from routes.amazon_routes import amazon_api_bp
from routes.googlemap import googlemap_bp
from routes.master_table import master_table_bp
from routes.upload_product_csv import product_csv_bp
from routes.upload_item_csv import item_csv_bp

# Listing & Product Blueprints imports
from routes.items_data import item_bp
from routes.item_csv_download import item_csv_bp as item_csv_download_bp
from routes.item_duplicate import item_duplicate_bp
from routes.upload_others_csv import upload_others_csv_bp
from routes.listing_master_route import listing_master_bp

from routes.location_master_route import location_master_bp

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
from routes.gdrive_etl_routes.dashboard_stats import dashboard_bp

# Load environment variables
_env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_env_path, override=True)
app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
cors.init_app(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
mail.init_app(app)

with app.app_context():
    db.create_all()
    from utils.db_migrations import run_pending_migrations
    print("🔄 Running Database Migrations...")
    run_pending_migrations(app)

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
    "/api/nearbuy/fetch-data",
    "/api/justdial/fetch-data",
    "/api/heyplaces/fetch-data",
    "/api/location-master/fetch-data",
    # Validation dashboard
    "/api/validation/dashboard",
    "/api/validation/errors",
    "/api/validation/clean",
    "/api/validation/report",
    "/api/model/stats",
    "/api/model/recent",
    "/api/model/all",
    "/api/model/files",
    "/api/model/state-summary",
    "/api/model/folder-status",
]

@app.before_request
def protect_all_routes():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200
        
    normalized_path = request.path.rstrip('/')
    normalized_public_routes = [route.rstrip('/') for route in PUBLIC_ROUTES]

    if normalized_path in normalized_public_routes or request.path in PUBLIC_ROUTES:
        return None

    if normalized_path.endswith('/fetch-data'):
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

app.register_blueprint(item_bp, url_prefix="/items")
app.register_blueprint(item_csv_download_bp)
app.register_blueprint(item_duplicate_bp)
app.register_blueprint(upload_others_csv_bp)
app.register_blueprint(listing_master_bp, url_prefix="/api")
app.register_blueprint(validation_dashboard_bp)
app.register_blueprint(dashboard_bp)

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
    (jiomart_bp, "/jio-mart"), (bigbasket_bp, "/big-basket"),
    (location_master_bp, "/location-master") # ✅ ADDED Location Master Blueprint
]

for bp, prefix in blueprints_listing:
    app.register_blueprint(bp, url_prefix=f"/api{prefix}")

@app.route('/')
def index():
    return jsonify({"message": "Flask API is running! Clean and Modular."})

if __name__ == '__main__':
    # Ensure env is loaded before anything else
    _env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(_env_path, override=True)
    print("🔗 Starting Flask API Server...")

    import sys
    # Handle the --runserver flag
    if "--runserver" in sys.argv:
        # Noisy 30-second terminal monitor removed. Use `python gdrive_status.py` instead.
        
        from gevent.pywsgi import WSGIServer
        print("🚀 Starting Gevent WSGI Server on http://0.0.0.0:5000")
        http_server = WSGIServer(('0.0.0.0', 5000), app)

        def shutdown():
            print('\n🛑 shutdown signal received. Stopping API server...')
            http_server.stop()
            print("✅ Shutdown complete.")
            sys.exit(0)

        # Optional handle for SIGINT if supported
        import signal
        import gevent
        try:
            gevent.signal_handler(signal.SIGINT, shutdown)
        except AttributeError:
            # Windows doesn't support gevent.signal_handler, fallback
            pass

        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            shutdown()
    else:
        # Fallback to standard Flask for local dev
        try:
            app.run(host='0.0.0.0', port=5000, debug=True)
        except KeyboardInterrupt:
            print('\n🛑 shutdown signal received. Stopping local dev server...')
            sys.exit(0)
