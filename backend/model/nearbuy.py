from extensions import db

class NearBuy(db.Model):
    __tablename__ = 'nearbuy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    number = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    source = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "number": self.number,
            "rating": self.rating,
            "city": self.city,
            "country": self.country,
            "source": self.source
        }