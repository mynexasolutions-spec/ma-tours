import uuid

from app.extensions import db


class HeroSlide(db.Model):
    __tablename__ = 'hero_slides'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300), nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    cta_text = db.Column(db.String(100), nullable=True)
    cta_link = db.Column(db.String(500), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<HeroSlide {self.title}>'
