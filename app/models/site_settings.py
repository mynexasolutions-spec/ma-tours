import uuid

from app.extensions import db


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    facebook_url = db.Column(db.String(500), nullable=True)
    instagram_url = db.Column(db.String(500), nullable=True)
    youtube_url = db.Column(db.String(500), nullable=True)
    google_maps_url = db.Column(db.String(500), nullable=True)
    footer_text = db.Column(db.Text, nullable=True)
    
    # Hero Section Settings
    hero_text_mode = db.Column(db.String(20), default='per_slide')  # 'global' or 'per_slide'
    hero_title = db.Column(db.String(255), nullable=True)
    hero_subtitle = db.Column(db.String(255), nullable=True)
    hero_cta_text = db.Column(db.String(100), nullable=True)
    hero_cta_link = db.Column(db.String(255), nullable=True)
    
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<SiteSettings {self.business_name}>'
