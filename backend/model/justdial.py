from extensions import db

class JustDial(db.Model):
    __tablename__ = 'justdial'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255)) # This is the 'name' in your DB
    address = db.Column(db.Text)
    number1 = db.Column(db.String(100)) # This is the 'phone' in your DB
    website = db.Column(db.String(512))
    category = db.Column(db.String(100))
    city = db.Column(db.String(100))
    source = db.Column(db.String(100))
    company_address_hash = db.Column(db.String(64)) # Match your screenshot

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.company,   # Maps 'company' to 'name' for the frontend
            "address": self.address,
            "number": self.number1, # Maps 'number1' to 'number' for the frontend
            "website": self.website,
            "category": self.category,
            "city": self.city,
            "source": self.source
        }