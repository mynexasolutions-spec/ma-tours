import uuid

from app.extensions import db


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(300), nullable=False)
    cta_text = db.Column(db.String(100), nullable=True)
    cta_link = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Announcement {self.text[:50]}>'
