from extensions import db

class Pinda(db.Model):
    __tablename__ = 'pinda'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(512)) # Maps to the 'url' column in your schema
    address = db.Column(db.Text)
    number = db.Column(db.String(100))
    category = db.Column(db.String(100))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    source = db.Column(db.String(100))
    name_address_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "address": self.address,
            "number": self.number,
            "category": self.category,
            "city": self.city,
            "source": self.source
        }