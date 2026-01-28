import os
import re
import json
import threading
import argparse
import random
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request
from playwright.sync_api import sync_playwright
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

from config import Config
from extensions import db, jwt, cors, mail

# --- 1. Import Blueprints ---
from routes.auth_route import auth_bp
from routes.scraper_routes import scraper_bp
from routes.amazon_routes import amazon_api_bp
from routes.googlemap import googlemap_bp
from routes.master_table import master_table_bp
from routes.upload_product_csv import product_csv_bp
from routes.upload_item_csv import item_csv_bp
from routes.amazon_product import amazon_products_bp
from routes.items_data import item_bp
from routes.item_duplicate import item_duplicate_bp
from routes.upload_others_csv import upload_others_csv_bp

# Listing Blueprints
from routes.listing_routes.upload_asklaila_route import asklaila_bp
from routes.listing_routes.upload_atm_route import atm_bp
from routes.listing_routes.upload_bank_route import bank_bp
# ... (Import all other listing BPs here as seen in your code)

# --- 2. Initialize App ---
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

# Init Extensions
db.init_app(app)
jwt.init_app(app)
cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
mail.init_app(app)

# --- 3. Database Models & Creation ---
# Import models to ensure they are registered
from model.user import User
from model.scraper_task import ScraperTask
from model.amazon_product_model import AmazonProduct
from model.googlemap_data import GooglemapData
# ... (Import others)

with app.app_context():
    db.create_all()

# --- 4. Global JWT Protection ---
PUBLIC_ROUTES = [
    "/", "/auth/signup", "/auth/login", "/auth/logout",
    "/auth/forgot-password", "/auth/verify-otp", "/auth/reset-password", "/health"
]

@app.before_request
def protect_all_routes():
    if request.path in PUBLIC_ROUTES or request.method == "OPTIONS":
        return None
    try:
        verify_jwt_in_request()
    except Exception as e:
        return jsonify({"message": "Missing or invalid token", "error": str(e)}), 401

# --- 5. Register Blueprints ---
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(scraper_bp, url_prefix="/api")
app.register_blueprint(amazon_api_bp, url_prefix="/api")
app.register_blueprint(item_bp, url_prefix="/items")

# Register all other BPs using the loop logic from your teammate
listing_blueprints = [
    (asklaila_bp, "/asklaila"), (atm_bp, "/atm"), (bank_bp, "/bank"),
    (googlemap_bp, "/googlemap"), (master_table_bp, "/master-table")
    # ... add the rest of the list here
]
for bp, prefix in listing_blueprints:
    app.register_blueprint(bp, url_prefix=prefix)

@app.route('/')
def index():
    return jsonify({"message": "Flask API is running! Clean and Modular."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)