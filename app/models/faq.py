import uuid

from app.extensions import db


class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<FAQ {self.question[:50]}>'
