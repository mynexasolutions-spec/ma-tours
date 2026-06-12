import uuid
from app.extensions import db

class PackageDeparture(db.Model):
    __tablename__ = 'package_departures'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=False)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    price_override = db.Column(db.Numeric(10, 2), nullable=True) # Optional price for peak seasons
    available_seats = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), default='Available') # Available, Filling Fast, Sold Out
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<PackageDeparture {self.start_date} - {self.end_date}>'
