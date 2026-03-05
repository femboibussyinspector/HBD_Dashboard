from extensions import db

class GoogleMapScrape(db.Model):
    __tablename__ = 'google_map_scrape'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    number = db.Column(db.String(100))
    review_count = db.Column(db.String(50))
    rating = db.Column(db.String(50))
    category = db.Column(db.String(255))
    address = db.Column(db.Text)
    website = db.Column(db.Text)
    email = db.Column(db.String(255))
    pluscode = db.Column(db.String(255))
    closing_hours = db.Column(db.Text)
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    instagram_profile = db.Column(db.Text)
    facebook_profile = db.Column(db.Text)
    linkedin_profile = db.Column(db.Text)
    twitter_profile = db.Column(db.Text)
    images_folder = db.Column(db.Text)
    source = db.Column(db.String(100))
    name_address_hash = db.Column(db.String(64))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "rating": self.rating,
            "review_count": self.review_count,
            "category": self.category,
            "address": self.address,
            "website": self.website,
            "source": self.source
        }