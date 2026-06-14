from flask import render_template, request, jsonify

from app.extensions import db
from app.frontend import public_bp
from app.models.hero_slide import HeroSlide
from app.models.announcement import Announcement
from app.models.package import Package
from app.models.destination import Destination
from app.models.travel_style import TravelStyle
from app.models.testimonial import Testimonial
from app.models.faq import FAQ
from app.models.gallery import GalleryImage, HomepageGalleryImage, GalleryCategory
from app.models.inquiry import Inquiry
from app.models.site_settings import SiteSettings
from app.models.activity import Activity
from app.models.activity_category import ActivityCategory

@public_bp.route('/')
def home():
    """Homepage."""
    hero_slides = HeroSlide.query.filter_by(is_active=True).order_by(HeroSlide.display_order).all()
    announcement = Announcement.query.filter_by(is_active=True).first()
    
    # Get top 3 featured/recent packages
    packages = Package.query.filter_by(is_active=True).order_by(Package.created_at.desc()).limit(3).all()
    
    # Get activity categories
    activity_categories = ActivityCategory.query.filter_by(is_active=True).order_by(ActivityCategory.display_order).all()
    
    # Get top 4 destinations
    destinations = Destination.query.filter_by(is_active=True).limit(4).all()
    
    # Get featured testimonials
    testimonials = Testimonial.query.filter_by(is_featured=True, is_active=True).all()
    
    # Get active FAQs
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.display_order).all()
    
    # Get recent gallery images (limit 6 for a nice grid)
    gallery_images = GalleryImage.query.order_by(GalleryImage.created_at.desc()).limit(6).all()
    
    # Get global site settings (for hero config)
    settings = SiteSettings.query.first()
    
    # Fetch top 8 homepage gallery images
    homepage_gallery = HomepageGalleryImage.query.filter_by(is_active=True).order_by(HomepageGalleryImage.display_order).limit(8).all()
    
    return render_template('frontend/home.html', 
                           hero_slides=hero_slides,
                           announcement=announcement,
                           packages=packages,
                           activity_categories=activity_categories,
                           destinations=destinations,
                           testimonials=testimonials,
                           faqs=faqs,
                           gallery_images=gallery_images,
                           homepage_gallery=homepage_gallery,
                           settings=settings)


@public_bp.route('/api/inquiry', methods=['POST'])
def submit_inquiry():
    """API endpoint to receive inquiry submissions from the frontend Vue components."""
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Invalid request data"}), 400
        
    try:
        from datetime import datetime
        
        # Parse travel_date properly if provided
        travel_date_str = data.get('travel_date')
        parsed_date = None
        if travel_date_str:
            try:
                parsed_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            except ValueError:
                # Fallback if the date string is in an unexpected format
                pass

        inquiry = Inquiry(
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            message=data.get('message'),
            travel_date=parsed_date,
            travelers_count=data.get('travelers_count') or None,
            source=data.get('source', 'homepage'),
            status='new',
            package_id=data.get('package_id') or None
        )
        db.session.add(inquiry)
        db.session.commit()
        return jsonify({"status": "success", "message": "Your inquiry has been received. Our team will contact you soon!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@public_bp.route('/about')
def about():
    """About Us page."""
    settings = SiteSettings.query.first()
    return render_template('frontend/about.html', settings=settings)


@public_bp.route('/packages')
def packages_list():
    """List all travel packages."""
    travel_style_slug = request.args.get('travel_style')
    destination_slug = request.args.get('destination')
    
    query = Package.query.filter_by(is_active=True)
    
    if travel_style_slug:
        query = query.join(Package.travel_styles).filter(TravelStyle.slug == travel_style_slug)
        
    if destination_slug:
        query = query.join(Destination).filter(Destination.slug == destination_slug)
        
    packages = query.order_by(Package.created_at.desc()).all()
    
    travel_styles = TravelStyle.query.all()
    destinations = Destination.query.filter_by(is_active=True).all()
    settings = SiteSettings.query.first()
    
    return render_template('frontend/packages/list.html', 
                           packages=packages, 
                           travel_styles=travel_styles, 
                           destinations=destinations,
                           current_travel_style=travel_style_slug,
                           current_destination=destination_slug,
                           settings=settings)


@public_bp.route('/packages/<slug>')
def package_detail(slug):
    """View details of a specific package."""
    package = Package.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    related_packages = Package.query.filter(
        Package.is_active == True,
        Package.id != package.id,
        Package.destination_id == package.destination_id
    ).limit(3).all()
    
    settings = SiteSettings.query.first()
    
    return render_template('frontend/packages/detail.html', 
                           package=package, 
                           related_packages=related_packages,
                           settings=settings)


@public_bp.route('/services')
def services():
    """Services page."""
    settings = SiteSettings.query.first()
    return render_template('frontend/services.html', settings=settings)


@public_bp.route('/gallery')
def gallery():
    """Gallery page."""
    categories = GalleryCategory.query.all()
    images = GalleryImage.query.filter_by(is_active=True).order_by(GalleryImage.display_order).all()
    settings = SiteSettings.query.first()
    return render_template('frontend/gallery.html', categories=categories, images=images, settings=settings)


@public_bp.route('/contact')
def contact():
    """Contact page."""
    settings = SiteSettings.query.first()
    return render_template('frontend/contact.html', settings=settings)


@public_bp.route('/privacy-policy')
def privacy_policy():
    """Privacy Policy page."""
    settings = SiteSettings.query.first()
    return render_template('frontend/legal/privacy.html', settings=settings)


@public_bp.route('/terms')
def terms():
    """Terms & Conditions page."""
    settings = SiteSettings.query.first()
    return render_template('frontend/legal/terms.html', settings=settings)


@public_bp.route('/destinations')
def destinations_list():
    """List all destinations."""
    domestic_destinations = Destination.query.filter_by(is_active=True, is_international=False).all()
    international_destinations = Destination.query.filter_by(is_active=True, is_international=True).all()
    settings = SiteSettings.query.first()
    return render_template('frontend/destinations/list.html', 
                           domestic_destinations=domestic_destinations, 
                           international_destinations=international_destinations, 
                           settings=settings)


@public_bp.route('/destinations/<slug>')
def destination_detail(slug):
    """View details of a specific destination and its packages."""
    destination = Destination.query.filter_by(slug=slug, is_active=True).first_or_404()
    packages = Package.query.filter_by(destination_id=destination.id, is_active=True).order_by(Package.created_at.desc()).all()
    settings = SiteSettings.query.first()
    return render_template('frontend/destinations/detail.html', destination=destination, packages=packages, settings=settings)


@public_bp.route('/activities')
def activities_list():
    """List all activities grouped by category."""
    categories = ActivityCategory.query.filter_by(is_active=True).order_by(ActivityCategory.display_order).all()
    # Uncategorized activities
    uncategorized = Activity.query.filter_by(is_active=True, category_id=None).all()
    settings = SiteSettings.query.first()
    return render_template('frontend/activities/list.html', categories=categories, uncategorized=uncategorized, settings=settings)


@public_bp.route('/activities/<slug>')
def activity_detail(slug):
    """View details of a specific activity and its packages."""
    activity = Activity.query.filter_by(slug=slug, is_active=True).first_or_404()
    packages = Package.query.join(Package.activities).filter(Activity.id == activity.id, Package.is_active == True).order_by(Package.created_at.desc()).all()
    settings = SiteSettings.query.first()
    return render_template('frontend/activities/detail.html', activity=activity, packages=packages, settings=settings)
