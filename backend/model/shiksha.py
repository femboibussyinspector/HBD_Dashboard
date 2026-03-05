from extensions import db

class Shiksha(db.Model):
    __tablename__ = 'shiksha'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    area = db.Column(db.String(100))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    admission_requirement = db.Column(db.Text)
    courses = db.Column(db.Text)
    avg_fees = db.Column(db.String(100))
    avg_salary = db.Column(db.String(100))
    rating = db.Column(db.String(50))
    number = db.Column(db.String(100))
    website = db.Column(db.String(512))
    email = db.Column(db.String(255))
    category = db.Column(db.String(100))
    country = db.Column(db.String(100))
    source = db.Column(db.String(100))
    name_address_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.area,         # Mapping 'area' to 'city' for frontend consistency
            "courses": self.courses,
            "avg_fees": self.avg_fees,
            "avg_salary": self.avg_salary,
            "rating": self.rating,
            "number": self.number,
            "website": self.website,
            "email": self.email,
            "category": self.category,
            "country": self.country,
            "source": self.source
        }