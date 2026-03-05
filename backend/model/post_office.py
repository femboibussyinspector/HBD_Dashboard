from extensions import db

class PostOffice(db.Model):
    __tablename__ = 'post_office' # Explicitly using your DB table name

    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.String(20))
    area = db.Column(db.String(255))
    taluka = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    source = db.Column(db.String(100))
    pin_area_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "pincode": self.pincode,
            "area": self.area,
            "taluka": self.taluka,
            "city": self.city,
            "state": self.state,
            "source": self.source
        }