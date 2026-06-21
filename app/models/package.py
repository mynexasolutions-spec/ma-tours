import uuid

from app.extensions import db


# --- Association table for Package <-> TravelStyle (many-to-many) ---
package_travel_styles = db.Table(
    'package_travel_styles',
    db.Column('package_id', db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), primary_key=True),
    db.Column('travel_style_id', db.String(36), db.ForeignKey('travel_styles.id', ondelete='CASCADE'), primary_key=True),
)

# --- Association table for Package <-> Activity (many-to-many) ---
package_activities = db.Table(
    'package_activities',
    db.Column('package_id', db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), primary_key=True),
    db.Column('activity_id', db.String(36), db.ForeignKey('activities.id', ondelete='CASCADE'), primary_key=True),
)

class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id = db.Column(db.String(36), db.ForeignKey('destinations.id', ondelete='SET NULL'), nullable=True)

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)

    short_description = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)

    price_from = db.Column(db.Numeric(10, 2), nullable=True)

    duration_days = db.Column(db.Integer, nullable=True)
    duration_nights = db.Column(db.Integer, nullable=True)

    hotel_details = db.Column(db.Text, nullable=True)

    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    seo_title = db.Column(db.String(200), nullable=True)
    seo_description = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    travel_styles = db.relationship('TravelStyle', secondary=package_travel_styles, backref='packages', lazy='joined')
    activities = db.relationship('Activity', secondary=package_activities, backref='packages', lazy='joined')
    departures = db.relationship('PackageDeparture', backref='package', lazy='dynamic',
                                 order_by='PackageDeparture.start_date', cascade='all, delete-orphan')
    images = db.relationship('PackageImage', backref='package', lazy='dynamic',
                             order_by='PackageImage.display_order', cascade='all, delete-orphan')
    highlights = db.relationship('PackageHighlight', backref='package', lazy='dynamic',
                                 order_by='PackageHighlight.display_order', cascade='all, delete-orphan')
    inclusions = db.relationship('PackageInclusion', backref='package', lazy='dynamic',
                                 order_by='PackageInclusion.display_order', cascade='all, delete-orphan')
    exclusions = db.relationship('PackageExclusion', backref='package', lazy='dynamic',
                                 order_by='PackageExclusion.display_order', cascade='all, delete-orphan')
    itinerary = db.relationship('PackageItinerary', backref='package', lazy='dynamic',
                                order_by='PackageItinerary.day_number', cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', backref='package', lazy='dynamic')
    faqs = db.relationship('FAQ', backref='package', lazy='dynamic', cascade='all, delete-orphan')
    testimonials = db.relationship('Testimonial', backref='package', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def hero_image_url(self):
        """Returns the first image URL associated with the package, or None."""
        first_image = self.images.first()
        return first_image.image_url if first_image else None

    def __repr__(self):
        return f'<Package {self.title}>'


class PackageImage(db.Model):
    __tablename__ = 'package_images'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<PackageImage {self.id}>'


class PackageHighlight(db.Model):
    __tablename__ = 'package_highlights'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=False)
    highlight = db.Column(db.String(300), nullable=False)
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<PackageHighlight {self.highlight}>'


class PackageInclusion(db.Model):
    __tablename__ = 'package_inclusions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=False)
    inclusion = db.Column(db.String(300), nullable=False)
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<PackageInclusion {self.inclusion}>'


class PackageExclusion(db.Model):
    __tablename__ = 'package_exclusions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=False)
    exclusion = db.Column(db.String(300), nullable=False)
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<PackageExclusion {self.exclusion}>'


class PackageItinerary(db.Model):
    __tablename__ = 'package_itinerary'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    package_id = db.Column(db.String(36), db.ForeignKey('packages.id', ondelete='CASCADE'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<PackageItinerary Day {self.day_number}: {self.title}>'
