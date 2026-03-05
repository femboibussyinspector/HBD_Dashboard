from extensions import db

class AmazonProduct(db.Model):
    __tablename__ = 'amazon_products' # Matches your DB table name

    id = db.Column(db.Integer, primary_key=True)
    ASIN = db.Column(db.String(100))
    Product_name = db.Column(db.Text)
    price = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    Number_of_ratings = db.Column(db.String(100))
    Brand = db.Column(db.String(255))
    Seller = db.Column(db.String(255))
    category = db.Column(db.String(255))
    subcategory = db.Column(db.String(255))
    sub_sub_category = db.Column(db.String(255))
    category_sub_sub_sub = db.Column(db.String(255))
    colour = db.Column(db.String(100))
    size_options = db.Column(db.Text)
    description = db.Column(db.Text)
    link = db.Column(db.Text)
    Image_URLs = db.Column(db.Text)
    About_the_items_bullet = db.Column(db.Text)
    Product_details = db.Column(db.Text)
    Additional_Details = db.Column(db.Text)
    Manufacturer_Name = db.Column(db.String(255))
    created_at = db.Column(db.String(100)) # Often stored as string in scraped DBs

    def to_dict(self):
        return {
            "id": self.id,
            "asin": self.ASIN,
            "name": self.Product_name, # Mapping for consistent frontend rendering
            "price": self.price,
            "rating": self.rating,
            "reviews": self.Number_of_ratings,
            "brand": self.Brand,
            "category": self.category,
            "link": self.link
        }