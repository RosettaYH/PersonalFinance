from app import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))  # 'expense' or 'income'
    note = db.Column(db.String(200))  # Optional note

    def __repr__(self):
        return f'<Category {self.name}>'
