# Import all models so Alembic and SQLAlchemy can discover them
from app.models.admin import Admin
from app.models.destination import Destination
from app.models.travel_style import TravelStyle
from app.models.package import (
    Package, PackageImage, PackageHighlight,
    PackageInclusion, PackageExclusion, PackageItinerary,
    package_travel_styles, package_activities,
)
from app.models.inquiry import Inquiry
from app.models.testimonial import Testimonial
from app.models.faq import FAQ
from app.models.gallery import GalleryCategory, GalleryImage
from app.models.hero_slide import HeroSlide
from app.models.announcement import Announcement
from app.models.site_settings import SiteSettings
from app.models.activity_category import ActivityCategory
from app.models.activity import Activity
from app.models.departure import PackageDeparture

__all__ = [
    'Admin',
    'Destination',
    'TravelStyle',
    'Package', 'PackageImage', 'PackageHighlight',
    'PackageInclusion', 'PackageExclusion', 'PackageItinerary',
    'package_travel_styles', 'package_activities',
    'Inquiry',
    'Testimonial',
    'FAQ',
    'GalleryCategory', 'GalleryImage',
    'HeroSlide',
    'Announcement',
    'SiteSettings',
    'ActivityCategory',
    'Activity',
    'PackageDeparture',
]
