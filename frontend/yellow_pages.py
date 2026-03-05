from extensions import db
class YellowPages(db.Model):
    __tablename__ = 'yellow_pages'
    id = db.Column(db.Integer, primary_key=True)
