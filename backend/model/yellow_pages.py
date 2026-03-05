from extensions import db

class YellowPages(db.Model):
    __tablename__ = 'yellow_pages' # Assuming your table name is yellow_pages. If it's yellowpages, change this.

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    area = db.Column(db.String(255))
    number = db.Column(db.String(100))
    email = db.Column(db.String(255))
    category = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    source = db.Column(db.String(100))
    name_address_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "area": self.area,
            "number": self.number,
            "email": self.email,
            "category": self.category,
            "pincode": self.pincode,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "source": self.source
        }