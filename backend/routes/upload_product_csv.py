# this code is for data csv upload for googlemap data and its complately working 

# from flask import Blueprint, request, jsonify
# import pandas as pd
# from io import StringIO
# import chardet
# from database.session import get_db_session
# from model.googlemap_data import GooglemapData

# product_csv_bp = Blueprint("upload_csv", __name__)

# @product_csv_bp.route("/upload_csv_product_data", methods=["POST"])
# def upload_csv():
#     session = None  #  Safe initialization
#     try:
#         # Check if file is present
#         if "file" not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400

#         file = request.files["file"]
#         if file.filename == "":
#             return jsonify({"error": "Empty file name"}), 400

#         #  Read CSV safely with encoding detection
#         raw_data = file.read()
#         detected = chardet.detect(raw_data)
#         encoding = detected["encoding"] or "utf-8"

#         try:
#             csv_data = StringIO(raw_data.decode(encoding, errors="ignore"))
#             df = pd.read_csv(csv_data)
#         except Exception as e:
#             print("CSV Read Error:", e)
#             return jsonify({"error": "Failed to read CSV file. Check encoding or format."}), 400

#         #  Optional rename (you can skip if already matches DB)
#         df.rename(columns={
#             "product_name": "product_name",
#             "affiliate_url": "affiliate_url",
#             "city_id": "city_id",
#             "area_id": "area_id",
#             "product_category": "product_category",
#             "product_description": "product_description",
#             "product_price": "product_price",
#             "product_slug": "product_slug",
#             "product_categories_string": "product_categories_string",
#             "product_image_small": "product_image_small",
#             "product_image_medium": "product_image_medium",
#             "product_image_large": "product_image_large",
#             "created_at": "created_at",
#             "updated_at": "updated_at",
#             "product_as_deal": "product_as_deal",
#             "product_type": "product_type",
#             "product_nature_type": "product_nature_type",
#             "product_original_price": "product_original_price",
#             "product_selling_price": "product_selling_price",
#             "product_brand_name": "product_brand_name",
#             "video_url": "video_url",
#             "product_featured_service": "product_featured_service",
#             "startdate": "startdate",
#             "enddate": "enddate",
#             "available": "available",
#             "online_image_url": "online_image_url"
#         }, inplace=True)

#         #  Create DB session
#         session = get_db_session()

#         #  Insert all rows from CSV
#         for _, row in df.iterrows():
#             record = GooglemapData(
#                 product_name=row.get("product_name"),
#                 affiliate_url=row.get("affiliate_url"),
#                 city_id=row.get("city_id"),
#                 area_id=row.get("area_id"),
#                 product_category=row.get("product_category"),
#                 product_description=row.get("product_description"),
#                 product_price=row.get("product_price"),
#                 product_slug=row.get("product_slug"),
#                 product_categories_string=row.get("product_categories_string"),
#                 product_image_small=row.get("product_image_small"),
#                 product_image_medium=row.get("product_image_medium"),
#                 product_image_large=row.get("product_image_large"),
#                 created_at=row.get("created_at"),
#                 updated_at=row.get("updated_at"),
#                 product_as_deal=row.get("product_as_deal"),
#                 product_type=row.get("product_type"),
#                 product_nature_type=row.get("product_nature_type"),
#                 product_original_price=row.get("product_original_price"),
#                 product_selling_price=row.get("product_selling_price"),
#                 product_brand_name=row.get("product_brand_name"),
#                 video_url=row.get("video_url"),
#                 product_featured_service=row.get("product_featured_service"),
#                 startdate=row.get("startdate"),
#                 enddate=row.get("enddate"),
#                 available=row.get("available"),
#                 online_image_url=row.get("online_image_url")
#             )
#             session.add(record)

#         session.commit()
#         return jsonify({"message": " CSV uploaded and saved to DB successfully"}), 201

#     except Exception as e:
#         if session:
#             session.rollback()
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500

#     finally:
#         if session:
#             session.close()

from flask import Blueprint, request, jsonify
import pandas as pd
from io import StringIO
import chardet
import json
from sqlalchemy.exc import SQLAlchemyError
from database.session import get_db_session
from model.product_model.amazon_product import AmazonProduct
import numpy as np
import traceback

product_csv_bp = Blueprint("upload_csv_product_data", __name__)

@product_csv_bp.route("/upload_csv_product_data", methods=["POST"])
def upload_csv_product_data():
    session = None
    try:
        #  File validation
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty file name"}), 400

        #  Detect encoding & read CSV
        raw_data = file.read()
        detected = chardet.detect(raw_data)
        encoding = detected.get("encoding") or "utf-8"

        try:
            csv_data = StringIO(raw_data.decode(encoding, errors="ignore"))
            df = pd.read_csv(csv_data)
        except Exception as e:
            print("CSV Read Error:", e)
            return jsonify({"error": "Failed to read CSV file. Check encoding or format."}), 400

        #  Replace all NaN, None, or "nan" with empty string
        df = df.replace({np.nan: None, "nan": None, "NaN": None})
        df = df.fillna("")  # ensures no NaN values remain at all

        session = get_db_session()

        #  Helper function to clean cell values
        def safe_val(value):
            if value is None or (isinstance(value, float) and np.isnan(value)):
                return ""
            if str(value).strip().lower() in ["nan", "none", "null"]:
                return ""
            return str(value).strip()

        inserted_count = 0
        skipped_count = 0

        for _, row in df.iterrows():
            try:
                # Clean and handle ASIN properly
                asin_value = safe_val(row.get("ASIN"))
                if asin_value == "":
                    asin_value = None  #  store NULL instead of empty string

                product = AmazonProduct(
                    ASIN=asin_value,
                    Product_name=safe_val(row.get("Product_name")),
                    price=safe_val(row.get("price")),
                    rating=float(row.get("rating")) if str(row.get("rating")).replace('.', '', 1).isdigit() else 0.0,
                    Number_of_ratings=int(row.get("Number_of_ratings")) if str(row.get("Number_of_ratings")).isdigit() else 0,
                    Brand=safe_val(row.get("Brand")),
                    Seller=safe_val(row.get("Seller")),
                    category=safe_val(row.get("category")),
                    subcategory=safe_val(row.get("subcategory")),
                    sub_sub_category=safe_val(row.get("sub_sub_category")),
                    category_sub_sub_sub=safe_val(row.get("category_sub_sub_sub")),
                    colour=safe_val(row.get("colour")),
                    size_options=safe_val(row.get("size_options")),
                    description=safe_val(row.get("description")),
                    link=safe_val(row.get("link")),
                    Image_URLs=safe_val(row.get("Image_URLs")),
                    About_the_items_bullet=safe_val(row.get("About_the_items_bullet")),
                    Product_details=(
                        json.loads(row.get("Product_details"))
                        if isinstance(row.get("Product_details"), str)
                        and row.get("Product_details").strip().startswith("{")
                        else {}
                    ),
                    Additional_Details=(
                        json.loads(row.get("Additional_Details"))
                        if isinstance(row.get("Additional_Details"), str)
                        and row.get("Additional_Details").strip().startswith("{")
                        else {}
                    ),
                    Manufacturer_Name=safe_val(row.get("Manufacturer_Name")),
                )

                session.add(product)
                inserted_count += 1

            except Exception as inner_e:
                skipped_count += 1
                print(f" Row skipped due to error: {inner_e}")
                continue

        session.commit()
        return jsonify({
            "message": " Amazon product CSV uploaded successfully.",
            "inserted_rows": inserted_count,
            "skipped_rows": skipped_count
        }), 201

    except SQLAlchemyError as e:
        if session:
            session.rollback()
        print("Database Error:", str(e))
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

    except Exception as e:
        if session:
            session.rollback()
        print("Unexpected Error:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        if session:
            session.close()
