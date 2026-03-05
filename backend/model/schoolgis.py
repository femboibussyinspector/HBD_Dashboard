from extensions import db

class SchoolGIS(db.Model):
    __tablename__ = 'schoolgis'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    pincode = db.Column(db.String(20))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    subcategory = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    category = db.Column(db.String(100))
    source = db.Column(db.String(100))
    name_long_lat_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "subcategory": self.subcategory,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "source": self.source
        }