from extensions import db

class BigBasket(db.Model):
    __tablename__ = 'big_basket' # Assuming this is your exact MySQL table name

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(512))
    category = db.Column(db.String(255))
    sub_category = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    sale_price = db.Column(db.String(100))
    market_price = db.Column(db.String(100))
    type = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.String(100))
    product_brand_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.product, # Mapped for frontend consistency
            "category": self.category,
            "sub_category": self.sub_category,
            "brand": self.brand,
            "sale_price": self.sale_price,
            "market_price": self.market_price,
            "type": self.type,
            "rating": self.rating
        }