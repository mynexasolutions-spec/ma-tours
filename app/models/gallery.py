import uuid

from app.extensions import db


class GalleryCategory(db.Model):
    __tablename__ = 'gallery_categories'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)

    # Relationships
    images = db.relationship('GalleryImage', backref='category', lazy='dynamic',
                             order_by='GalleryImage.display_order', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<GalleryCategory {self.name}>'


class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = db.Column(db.String(36), db.ForeignKey('gallery_categories.id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(300), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<GalleryImage {self.id}>'
