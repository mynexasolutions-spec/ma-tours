import uuid

from app.extensions import db


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    package_taken = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Integer, nullable=True)  # 1-5
    review = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Testimonial {self.name}>'
