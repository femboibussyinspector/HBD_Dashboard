from extensions import db

class LocationMaster(db.Model):
    __tablename__ = 'Location_Master_India'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Column names must match your MySQL table exactly
    area_name = db.Column(db.String(255))
    city_name = db.Column(db.String(255))
    state_full_name = db.Column(db.String(255))
    state_short_code = db.Column(db.String(10))
    country_name = db.Column(db.String(100))

    def to_dict(self):
        """
        Returns a dictionary representation for the frontend.
        We merge the state name and code for a cleaner UI display.
        """
        return {
            "id": self.id,
            "area": self.area_name,
            "city": self.city_name,
            "state": f"{self.state_full_name} ({self.state_short_code})",
            "country": self.country_name
        }