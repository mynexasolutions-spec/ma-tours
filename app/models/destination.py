import uuid

from app.extensions import db


class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    hero_image_url = db.Column(db.String(500), nullable=True)
    is_international = db.Column(db.Boolean, default=False, server_default='0', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    packages = db.relationship('Package', backref='destination', lazy='dynamic')

    def __repr__(self):
        return f'<Destination {self.name}>'
