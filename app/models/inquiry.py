import uuid

from app.extensions import db


class Inquiry(db.Model):
    __tablename__ = 'inquiries'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='SET NULL'), nullable=True)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=True)

    travel_date = db.Column(db.Date, nullable=True)
    travelers_count = db.Column(db.Integer, nullable=True)

    message = db.Column(db.Text, nullable=True)

    source = db.Column(db.String(20), nullable=False, default='homepage')
    # source values: homepage, package, contact, whatsapp

    status = db.Column(db.String(20), nullable=False, default='new')
    # status values: new, contacted, interested, booked, closed

    admin_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Inquiry {self.name} - {self.status}>'
