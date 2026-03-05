from extensions import db

class MagicPin(db.Model):
    __tablename__ = 'magicpin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    number = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    avg_spent = db.Column(db.String(100))
    address = db.Column(db.Text)
    area = db.Column(db.String(255))
    subcategory = db.Column(db.String(255))
    city = db.Column(db.String(100))
    category = db.Column(db.String(100))
    cost_for_two = db.Column(db.String(100))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    source = db.Column(db.String(100))
    name_address_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "rating": self.rating,
            "avg_spent": self.avg_spent,
            "address": self.address,
            "area": self.area,
            "subcategory": self.subcategory,
            "city": self.city,
            "category": self.category,
            "cost_for_two": self.cost_for_two,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "source": self.source
        }