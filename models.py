from app import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.String)