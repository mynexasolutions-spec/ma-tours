from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
import os
import uuid
from werkzeug.utils import secure_filename

from app.admin import admin_bp
from app.extensions import db
from app.models.package import (
    Package, PackageImage, PackageHighlight,
    PackageInclusion, PackageExclusion, PackageItinerary,
)
from app.models.inquiry import Inquiry
from app.models.destination import Destination
from app.models.category import Category
from app.models.testimonial import Testimonial
from app.models.hero_slide import HeroSlide
from app.models.announcement import Announcement
from app.models.gallery import GalleryCategory, GalleryImage
from app.models.faq import FAQ
from app.models.site_settings import SiteSettings
from app.models.activity import Activity
from app.models.departure import PackageDeparture
from app.utils import generate_slug


# ─── Image Upload Endpoint ────────────────────────────────────────

@admin_bp.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    """Upload an image and return its local URL."""
    if 'image' not in request.files:
        return {'success': False, 'error': 'No file part'}, 400
    
    file = request.files['image']
    if file.filename == '':
        return {'success': False, 'error': 'No selected file'}, 400
        
    if file:
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            return {'success': False, 'error': 'Invalid file type. Allowed: jpg, jpeg, png, webp, gif'}, 400
            
        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        return {
            'success': True, 
            'url': url_for('static', filename=f'uploads/{filename}')
        }


# ─── Dashboard ──────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
def dashboard():
    """Admin dashboard with summary widgets."""
    total_packages = Package.query.count()
    active_packages = Package.query.filter_by(is_active=True).count()
    featured_packages = Package.query.filter_by(is_featured=True).count()

    total_inquiries = Inquiry.query.count()
    new_inquiries = Inquiry.query.filter_by(status='new').count()

    recent_inquiries = Inquiry.query.order_by(
        Inquiry.created_at.desc()
    ).limit(10).all()

    total_destinations = Destination.query.count()
    total_testimonials = Testimonial.query.count()

    return render_template('admin/dashboard.html',
        total_packages=total_packages,
        active_packages=active_packages,
        featured_packages=featured_packages,
        total_inquiries=total_inquiries,
        new_inquiries=new_inquiries,
        recent_inquiries=recent_inquiries,
        total_destinations=total_destinations,
        total_testimonials=total_testimonials,
    )


# ─── Destinations ───────────────────────────────────────────────

@admin_bp.route('/destinations')
@login_required
def destinations_list():
    """List all destinations."""
    destinations = Destination.query.order_by(Destination.name).all()
    return render_template('admin/destinations/list.html', destinations=destinations)


@admin_bp.route('/destinations/add', methods=['GET', 'POST'])
@login_required
def destinations_add():
    """Add a new destination."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        hero_image_url = request.form.get('hero_image_url', '').strip()
        is_active = request.form.get('is_active') == 'on'

        if not name:
            flash('Destination name is required.', 'error')
            return render_template('admin/destinations/form.html', mode='add')

        slug = generate_slug(name)

        existing = Destination.query.filter_by(slug=slug).first()
        if existing:
            flash(f'A destination with slug "{slug}" already exists.', 'error')
            return render_template('admin/destinations/form.html', mode='add')

        destination = Destination(
            name=name, slug=slug, description=description,
            hero_image_url=hero_image_url or None, is_active=is_active,
        )
        db.session.add(destination)
        db.session.commit()

        flash(f'Destination "{name}" created successfully.', 'success')
        return redirect(url_for('admin.destinations_list'))

    return render_template('admin/destinations/form.html', mode='add')


@admin_bp.route('/destinations/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def destinations_edit(id):
    """Edit an existing destination."""
    destination = db.session.get(Destination, id)
    if not destination:
        flash('Destination not found.', 'error')
        return redirect(url_for('admin.destinations_list'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        hero_image_url = request.form.get('hero_image_url', '').strip()
        is_active = request.form.get('is_active') == 'on'

        if not name:
            flash('Destination name is required.', 'error')
            return render_template('admin/destinations/form.html', mode='edit', destination=destination)

        new_slug = generate_slug(name)
        if new_slug != destination.slug:
            existing = Destination.query.filter_by(slug=new_slug).first()
            if existing:
                flash(f'A destination with slug "{new_slug}" already exists.', 'error')
                return render_template('admin/destinations/form.html', mode='edit', destination=destination)
            destination.slug = new_slug

        destination.name = name
        destination.description = description
        destination.hero_image_url = hero_image_url or None
        destination.is_active = is_active

        db.session.commit()
        flash(f'Destination "{name}" updated successfully.', 'success')
        return redirect(url_for('admin.destinations_list'))

    return render_template('admin/destinations/form.html', mode='edit', destination=destination)


@admin_bp.route('/destinations/<string:id>/toggle', methods=['POST'])
@login_required
def destinations_toggle(id):
    """Toggle destination active status."""
    destination = db.session.get(Destination, id)
    if not destination:
        flash('Destination not found.', 'error')
        return redirect(url_for('admin.destinations_list'))

    destination.is_active = not destination.is_active
    db.session.commit()

    status = 'activated' if destination.is_active else 'deactivated'
    flash(f'Destination "{destination.name}" {status}.', 'success')
    return redirect(url_for('admin.destinations_list'))


# ─── Packages ───────────────────────────────────────────────────

@admin_bp.route('/packages')
@login_required
def packages_list():
    """List all packages."""
    packages = Package.query.order_by(Package.created_at.desc()).all()
    return render_template('admin/packages/list.html', packages=packages)


@admin_bp.route('/packages/add', methods=['GET', 'POST'])
@login_required
def packages_add():
    """Add a new package."""
    destinations = Destination.query.filter_by(is_active=True).order_by(Destination.name).all()
    categories = Category.query.order_by(Category.name).all()
    activities = Activity.query.filter_by(is_active=True).order_by(Activity.name).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        destination_id = request.form.get('destination_id', '').strip()
        category_ids = request.form.getlist('category_ids')
        activity_ids = request.form.getlist('activity_ids')
        short_description = request.form.get('short_description', '').strip()
        description = request.form.get('description', '').strip()
        price_from = request.form.get('price_from', '').strip()
        duration_days = request.form.get('duration_days', '').strip()
        duration_nights = request.form.get('duration_nights', '').strip()
        hotel_details = request.form.get('hotel_details', '').strip()
        seo_title = request.form.get('seo_title', '').strip()
        seo_description = request.form.get('seo_description', '').strip()
        is_featured = request.form.get('is_featured') == 'on'
        is_active = request.form.get('is_active') == 'on'

        if not title:
            flash('Package title is required.', 'error')
            return render_template('admin/packages/form.html', mode='add',
                                   destinations=destinations, categories=categories, activities=activities)

        slug = generate_slug(title)
        existing = Package.query.filter_by(slug=slug).first()
        if existing:
            flash(f'A package with slug "{slug}" already exists.', 'error')
            return render_template('admin/packages/form.html', mode='add',
                                   destinations=destinations, categories=categories, activities=activities)

        package = Package(
            title=title,
            slug=slug,
            destination_id=destination_id or None,
            short_description=short_description or None,
            description=description or None,
            price_from=float(price_from) if price_from else None,
            duration_days=int(duration_days) if duration_days else None,
            duration_nights=int(duration_nights) if duration_nights else None,
            hotel_details=hotel_details or None,
            seo_title=seo_title or None,
            seo_description=seo_description or None,
            is_featured=is_featured,
            is_active=is_active,
        )

        # Set categories
        for cid in category_ids:
            cat = db.session.get(Category, cid)
            if cat:
                package.categories.append(cat)
                
        # Set activities
        for aid in activity_ids:
            act = db.session.get(Activity, aid)
            if act:
                package.activities.append(act)

        db.session.add(package)
        db.session.commit()

        flash(f'Package "{title}" created. Now add highlights, itinerary, and images.', 'success')
        return redirect(url_for('admin.packages_edit', id=package.id))

    return render_template('admin/packages/form.html', mode='add',
                           destinations=destinations, categories=categories, activities=activities)


@admin_bp.route('/packages/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def packages_edit(id):
    """Edit package — full page with sub-item management."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    destinations = Destination.query.filter_by(is_active=True).order_by(Destination.name).all()
    categories = Category.query.order_by(Category.name).all()
    activities = Activity.query.filter_by(is_active=True).order_by(Activity.name).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        destination_id = request.form.get('destination_id', '').strip()
        category_ids = request.form.getlist('category_ids')
        activity_ids = request.form.getlist('activity_ids')
        short_description = request.form.get('short_description', '').strip()
        description = request.form.get('description', '').strip()
        price_from = request.form.get('price_from', '').strip()
        duration_days = request.form.get('duration_days', '').strip()
        duration_nights = request.form.get('duration_nights', '').strip()
        hotel_details = request.form.get('hotel_details', '').strip()
        seo_title = request.form.get('seo_title', '').strip()
        seo_description = request.form.get('seo_description', '').strip()
        is_featured = request.form.get('is_featured') == 'on'
        is_active = request.form.get('is_active') == 'on'

        if not title:
            flash('Package title is required.', 'error')
            return render_template('admin/packages/edit.html', package=package,
                                   destinations=destinations, categories=categories, activities=activities)

        new_slug = generate_slug(title)
        if new_slug != package.slug:
            existing = Package.query.filter_by(slug=new_slug).first()
            if existing:
                flash(f'A package with slug "{new_slug}" already exists.', 'error')
                return render_template('admin/packages/edit.html', package=package,
                                       destinations=destinations, categories=categories, activities=activities)
            package.slug = new_slug

        package.title = title
        package.destination_id = destination_id or None
        package.short_description = short_description or None
        package.description = description or None
        package.price_from = float(price_from) if price_from else None
        package.duration_days = int(duration_days) if duration_days else None
        package.duration_nights = int(duration_nights) if duration_nights else None
        package.hotel_details = hotel_details or None
        package.seo_title = seo_title or None
        package.seo_description = seo_description or None
        package.is_featured = is_featured
        package.is_active = is_active

        # Update categories
        package.categories.clear()
        for cid in category_ids:
            cat = db.session.get(Category, cid)
            if cat:
                package.categories.append(cat)
                
        # Update activities
        package.activities.clear()
        for aid in activity_ids:
            act = db.session.get(Activity, aid)
            if act:
                package.activities.append(act)

        db.session.commit()
        flash(f'Package "{title}" updated successfully.', 'success')
        return redirect(url_for('admin.packages_edit', id=package.id))

    return render_template('admin/packages/edit.html', package=package,
                           destinations=destinations, categories=categories)


@admin_bp.route('/packages/<string:id>/toggle', methods=['POST'])
@login_required
def packages_toggle(id):
    """Toggle package active status."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    package.is_active = not package.is_active
    db.session.commit()
    status = 'activated' if package.is_active else 'deactivated'
    flash(f'Package "{package.title}" {status}.', 'success')
    return redirect(url_for('admin.packages_list'))


@admin_bp.route('/packages/<string:id>/feature', methods=['POST'])
@login_required
def packages_feature(id):
    """Toggle package featured status."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    package.is_featured = not package.is_featured
    db.session.commit()
    status = 'featured' if package.is_featured else 'unfeatured'
    flash(f'Package "{package.title}" {status}.', 'success')
    return redirect(url_for('admin.packages_list'))


# ─── Package Highlights ─────────────────────────────────────────

@admin_bp.route('/packages/<string:id>/highlights/add', methods=['POST'])
@login_required
def package_highlight_add(id):
    """Add a highlight to a package."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    text = request.form.get('highlight', '').strip()
    if text:
        max_order = db.session.query(db.func.max(PackageHighlight.display_order)).filter_by(package_id=id).scalar() or 0
        highlight = PackageHighlight(package_id=id, highlight=text, display_order=max_order + 1)
        db.session.add(highlight)
        db.session.commit()
        flash('Highlight added.', 'success')
    else:
        flash('Highlight text is required.', 'error')

    return redirect(url_for('admin.packages_edit', id=id) + '#highlights')


@admin_bp.route('/packages/<string:pkg_id>/highlights/<string:h_id>/delete', methods=['POST'])
@login_required
def package_highlight_delete(pkg_id, h_id):
    """Delete a highlight."""
    highlight = db.session.get(PackageHighlight, h_id)
    if highlight and highlight.package_id == pkg_id:
        db.session.delete(highlight)
        db.session.commit()
        flash('Highlight removed.', 'success')

    return redirect(url_for('admin.packages_edit', id=pkg_id) + '#highlights')


# ─── Package Inclusions ─────────────────────────────────────────

@admin_bp.route('/packages/<string:id>/inclusions/add', methods=['POST'])
@login_required
def package_inclusion_add(id):
    """Add an inclusion to a package."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    text = request.form.get('inclusion', '').strip()
    if text:
        max_order = db.session.query(db.func.max(PackageInclusion.display_order)).filter_by(package_id=id).scalar() or 0
        inclusion = PackageInclusion(package_id=id, inclusion=text, display_order=max_order + 1)
        db.session.add(inclusion)
        db.session.commit()
        flash('Inclusion added.', 'success')
    else:
        flash('Inclusion text is required.', 'error')

    return redirect(url_for('admin.packages_edit', id=id) + '#inclusions')


@admin_bp.route('/packages/<string:pkg_id>/inclusions/<string:i_id>/delete', methods=['POST'])
@login_required
def package_inclusion_delete(pkg_id, i_id):
    """Delete an inclusion."""
    inclusion = db.session.get(PackageInclusion, i_id)
    if inclusion and inclusion.package_id == pkg_id:
        db.session.delete(inclusion)
        db.session.commit()
        flash('Inclusion removed.', 'success')

    return redirect(url_for('admin.packages_edit', id=pkg_id) + '#inclusions')


# ─── Package Exclusions ─────────────────────────────────────────

@admin_bp.route('/packages/<string:id>/exclusions/add', methods=['POST'])
@login_required
def package_exclusion_add(id):
    """Add an exclusion to a package."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    text = request.form.get('exclusion', '').strip()
    if text:
        max_order = db.session.query(db.func.max(PackageExclusion.display_order)).filter_by(package_id=id).scalar() or 0
        exclusion = PackageExclusion(package_id=id, exclusion=text, display_order=max_order + 1)
        db.session.add(exclusion)
        db.session.commit()
        flash('Exclusion added.', 'success')
    else:
        flash('Exclusion text is required.', 'error')

    return redirect(url_for('admin.packages_edit', id=id) + '#exclusions')


@admin_bp.route('/packages/<string:pkg_id>/exclusions/<string:e_id>/delete', methods=['POST'])
@login_required
def package_exclusion_delete(pkg_id, e_id):
    """Delete an exclusion."""
    exclusion = db.session.get(PackageExclusion, e_id)
    if exclusion and exclusion.package_id == pkg_id:
        db.session.delete(exclusion)
        db.session.commit()
        flash('Exclusion removed.', 'success')

    return redirect(url_for('admin.packages_edit', id=pkg_id) + '#exclusions')


# ─── Package Itinerary ──────────────────────────────────────────

@admin_bp.route('/packages/<string:id>/itinerary/add', methods=['POST'])
@login_required
def package_itinerary_add(id):
    """Add an itinerary day to a package."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    day_number = request.form.get('day_number', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if title and day_number:
        itinerary = PackageItinerary(
            package_id=id,
            day_number=int(day_number),
            title=title,
            description=description or None,
        )
        db.session.add(itinerary)
        db.session.commit()
        flash(f'Day {day_number} added to itinerary.', 'success')
    else:
        flash('Day number and title are required.', 'error')

    return redirect(url_for('admin.packages_edit', id=id) + '#itinerary')


@admin_bp.route('/packages/<string:pkg_id>/itinerary/<string:t_id>/delete', methods=['POST'])
@login_required
def package_itinerary_delete(pkg_id, t_id):
    """Delete an itinerary day."""
    itinerary = db.session.get(PackageItinerary, t_id)
    if itinerary and itinerary.package_id == pkg_id:
        db.session.delete(itinerary)
        db.session.commit()
        flash('Itinerary day removed.', 'success')

    return redirect(url_for('admin.packages_edit', id=pkg_id) + '#itinerary')


# ─── Package Images ─────────────────────────────────────────────

@admin_bp.route('/packages/<string:id>/images/add', methods=['POST'])
@login_required
def package_image_add(id):
    """Add an image to a package (URL-based for now)."""
    package = db.session.get(Package, id)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('admin.packages_list'))

    image_url = request.form.get('image_url', '').strip()
    if image_url:
        max_order = db.session.query(db.func.max(PackageImage.display_order)).filter_by(package_id=id).scalar() or 0
        image = PackageImage(package_id=id, image_url=image_url, display_order=max_order + 1)
        db.session.add(image)
        db.session.commit()
        flash('Image added.', 'success')
    else:
        flash('Image URL is required.', 'error')

    return redirect(url_for('admin.packages_edit', id=id) + '#images')


@admin_bp.route('/packages/<string:pkg_id>/images/<string:img_id>/delete', methods=['POST'])
@login_required
def package_image_delete(pkg_id, img_id):
    """Delete a package image."""
    image = db.session.get(PackageImage, img_id)
    if image and image.package_id == pkg_id:
        db.session.delete(image)
        db.session.commit()
        flash('Image removed.', 'success')

    return redirect(url_for('admin.packages_edit', id=pkg_id) + '#images')


# ─── Hero Slides ────────────────────────────────────────────────

@admin_bp.route('/hero/settings', methods=['GET', 'POST'])
@login_required
def hero_settings():
    """Manage global hero settings."""
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings(business_name='M.A. Tours & Travels')
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        settings.hero_text_mode = request.form.get('hero_text_mode', 'per_slide')
        settings.hero_title = request.form.get('hero_title', '').strip() or None
        settings.hero_subtitle = request.form.get('hero_subtitle', '').strip() or None
        settings.hero_cta_text = request.form.get('hero_cta_text', '').strip() or None
        settings.hero_cta_link = request.form.get('hero_cta_link', '').strip() or None
        
        db.session.commit()
        flash('Hero global settings updated.', 'success')
        return redirect(url_for('admin.hero_list'))
        
    return render_template('admin/hero/settings.html', settings=settings)


@admin_bp.route('/hero')
@login_required
def hero_list():
    """List all hero slides."""
    slides = HeroSlide.query.order_by(HeroSlide.display_order).all()
    settings = SiteSettings.query.first()
    return render_template('admin/hero/list.html', slides=slides, settings=settings)


@admin_bp.route('/hero/add', methods=['GET', 'POST'])
@login_required
def hero_add():
    """Add a hero slide."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subtitle = request.form.get('subtitle', '').strip()
        image_url = request.form.get('image_url', '').strip()
        cta_text = request.form.get('cta_text', '').strip()
        cta_link = request.form.get('cta_link', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        # Handle file upload
        if 'image_file' in request.files and request.files['image_file'].filename:
            file = request.files['image_file']
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'hero')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))
            image_url = url_for('static', filename=f'uploads/hero/{unique_filename}')
            
        if not title or not image_url:
            flash('Title and Image are required.', 'error')
            return render_template('admin/hero/form.html', mode='add')
            
        max_order = db.session.query(db.func.max(HeroSlide.display_order)).scalar() or 0
        slide = HeroSlide(
            title=title, subtitle=subtitle or None, image_url=image_url,
            cta_text=cta_text or None, cta_link=cta_link or None,
            display_order=max_order + 1, is_active=is_active
        )
        db.session.add(slide)
        db.session.commit()
        flash('Hero slide added.', 'success')
        return redirect(url_for('admin.hero_list'))
        
    return render_template('admin/hero/form.html', mode='add')


@admin_bp.route('/hero/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def hero_edit(id):
    """Edit a hero slide."""
    slide = db.session.get(HeroSlide, id)
    if not slide:
        flash('Slide not found.', 'error')
        return redirect(url_for('admin.hero_list'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subtitle = request.form.get('subtitle', '').strip()
        image_url = request.form.get('image_url', '').strip()
        cta_text = request.form.get('cta_text', '').strip()
        cta_link = request.form.get('cta_link', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        # Handle file upload
        if 'image_file' in request.files and request.files['image_file'].filename:
            file = request.files['image_file']
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'hero')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))
            image_url = url_for('static', filename=f'uploads/hero/{unique_filename}')
        if not image_url:
            image_url = slide.image_url
            
        if not title or not image_url:
            flash('Title and Image are required.', 'error')
            return render_template('admin/hero/form.html', mode='edit', slide=slide)
            
        slide.title = title
        slide.subtitle = subtitle or None
        slide.image_url = image_url
        slide.cta_text = cta_text or None
        slide.cta_link = cta_link or None
        slide.is_active = is_active
        
        db.session.commit()
        flash('Hero slide updated.', 'success')
        return redirect(url_for('admin.hero_list'))
        
    return render_template('admin/hero/form.html', mode='edit', slide=slide)


@admin_bp.route('/hero/<string:id>/delete', methods=['POST'])
@login_required
def hero_delete(id):
    """Delete a hero slide."""
    slide = db.session.get(HeroSlide, id)
    if slide:
        db.session.delete(slide)
        db.session.commit()
        flash('Hero slide deleted.', 'success')
    return redirect(url_for('admin.hero_list'))


# ─── Announcement ───────────────────────────────────────────────

@admin_bp.route('/announcement', methods=['GET', 'POST'])
@login_required
def announcement_manage():
    """Manage the top announcement bar."""
    # We'll just manage a single announcement for now
    announcement = Announcement.query.first()
    
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        cta_text = request.form.get('cta_text', '').strip()
        cta_link = request.form.get('cta_link', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        if not text and is_active:
            flash('Announcement text is required if active.', 'error')
            return render_template('admin/announcement/form.html', announcement=announcement)
            
        if not announcement:
            announcement = Announcement()
            db.session.add(announcement)
            
        announcement.text = text
        announcement.cta_text = cta_text or None
        announcement.cta_link = cta_link or None
        announcement.is_active = is_active
        
        db.session.commit()
        flash('Announcement updated successfully.', 'success')
        return redirect(url_for('admin.announcement_manage'))
        
    return render_template('admin/announcement/form.html', announcement=announcement)


# ─── Gallery ────────────────────────────────────────────────────

@admin_bp.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery_list():
    """List all gallery categories and handle category creation."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Category name is required.', 'error')
            return redirect(url_for('admin.gallery_list'))
            
        slug = generate_slug(name)
        existing = GalleryCategory.query.filter_by(slug=slug).first()
        if existing:
            flash(f'Category "{name}" already exists.', 'error')
            return redirect(url_for('admin.gallery_list'))
            
        category = GalleryCategory(name=name, slug=slug)
        db.session.add(category)
        db.session.commit()
        flash(f'Category "{name}" created.', 'success')
        return redirect(url_for('admin.gallery_list'))

    categories = GalleryCategory.query.order_by(GalleryCategory.name).all()
    return render_template('admin/gallery/list.html', categories=categories)


@admin_bp.route('/gallery/<string:id>/delete', methods=['POST'])
@login_required
def gallery_category_delete(id):
    """Delete a gallery category and its images."""
    category = db.session.get(GalleryCategory, id)
    if category:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted.', 'success')
    return redirect(url_for('admin.gallery_list'))


@admin_bp.route('/gallery/<string:id>', methods=['GET', 'POST'])
@login_required
def gallery_category(id):
    """View and manage images inside a category."""
    category = db.session.get(GalleryCategory, id)
    if not category:
        flash('Category not found.', 'error')
        return redirect(url_for('admin.gallery_list'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url', '').strip()
        caption = request.form.get('caption', '').strip()
        
        if not image_url:
            flash('Image URL is required.', 'error')
            return redirect(url_for('admin.gallery_category', id=category.id))
            
        max_order = db.session.query(db.func.max(GalleryImage.display_order)).filter_by(category_id=category.id).scalar() or 0
        image = GalleryImage(
            category_id=category.id,
            image_url=image_url,
            caption=caption or None,
            display_order=max_order + 1
        )
        db.session.add(image)
        db.session.commit()
        flash('Image added to gallery.', 'success')
        return redirect(url_for('admin.gallery_category', id=category.id))
        
    return render_template('admin/gallery/category.html', category=category)


@admin_bp.route('/gallery/image/<string:id>/delete', methods=['POST'])
@login_required
def gallery_image_delete(id):
    """Delete a gallery image."""
    image = db.session.get(GalleryImage, id)
    if not image:
        return redirect(url_for('admin.gallery_list'))
        
    category_id = image.category_id
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted.', 'success')
    return redirect(url_for('admin.gallery_category', id=category_id))


@admin_bp.route('/gallery/image/<string:id>/move/<string:direction>', methods=['POST'])
@login_required
def gallery_image_move(id, direction):
    """Move an image up or down in display order."""
    image = db.session.get(GalleryImage, id)
    if not image:
        return redirect(url_for('admin.gallery_list'))
        
    category_id = image.category_id
    current_order = image.display_order
    
    if direction == 'up':
        swap_img = GalleryImage.query.filter(
            GalleryImage.category_id == category_id,
            GalleryImage.display_order < current_order
        ).order_by(GalleryImage.display_order.desc()).first()
    elif direction == 'down':
        swap_img = GalleryImage.query.filter(
            GalleryImage.category_id == category_id,
            GalleryImage.display_order > current_order
        ).order_by(GalleryImage.display_order.asc()).first()
    else:
        swap_img = None
        
    if swap_img:
        image.display_order, swap_img.display_order = swap_img.display_order, image.display_order
        db.session.commit()
        
    return redirect(url_for('admin.gallery_category', id=category_id))


# ─── Testimonials ───────────────────────────────────────────────

@admin_bp.route('/testimonials')
@login_required
def testimonials_list():
    """List all testimonials."""
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials/list.html', testimonials=testimonials)


@admin_bp.route('/testimonials/add', methods=['GET', 'POST'])
@login_required
def testimonials_add():
    """Add a new testimonial."""
    packages = Package.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        package_taken = request.form.get('package_taken', '').strip()
        package_id = request.form.get('package_id') or None
        rating = request.form.get('rating')
        review = request.form.get('review', '').strip()
        image_url = request.form.get('image_url', '').strip()
        is_featured = request.form.get('is_featured') == 'on'
        is_active = request.form.get('is_active') == 'on'
        
        if not name or not review:
            flash('Name and review text are required.', 'error')
            return render_template('admin/testimonials/form.html', mode='add', packages=packages)
            
        testimonial = Testimonial(
            name=name,
            package_taken=package_taken or None,
            package_id=package_id,
            rating=int(rating) if rating else None,
            review=review,
            image_url=image_url or None,
            is_featured=is_featured,
            is_active=is_active
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added.', 'success')
        return redirect(url_for('admin.testimonials_list'))
        
    return render_template('admin/testimonials/form.html', mode='add', packages=packages)


@admin_bp.route('/testimonials/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def testimonials_edit(id):
    """Edit a testimonial."""
    testimonial = db.session.get(Testimonial, id)
    if not testimonial:
        flash('Testimonial not found.', 'error')
        return redirect(url_for('admin.testimonials_list'))

    packages = Package.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        package_taken = request.form.get('package_taken', '').strip()
        package_id = request.form.get('package_id') or None
        rating = request.form.get('rating')
        review = request.form.get('review', '').strip()
        image_url = request.form.get('image_url', '').strip()
        is_featured = request.form.get('is_featured') == 'on'
        is_active = request.form.get('is_active') == 'on'
        
        if not name or not review:
            flash('Name and review text are required.', 'error')
            return render_template('admin/testimonials/form.html', mode='edit', testimonial=testimonial, packages=packages)
            
        testimonial.name = name
        testimonial.package_taken = package_taken or None
        testimonial.package_id = package_id
        testimonial.rating = int(rating) if rating else None
        testimonial.review = review
        testimonial.image_url = image_url or None
        testimonial.is_featured = is_featured
        testimonial.is_active = is_active
        
        db.session.commit()
        flash('Testimonial updated.', 'success')
        return redirect(url_for('admin.testimonials_list'))
        
    return render_template('admin/testimonials/form.html', mode='edit', testimonial=testimonial, packages=packages)


@admin_bp.route('/testimonials/<string:id>/toggle', methods=['POST'])
@login_required
def testimonials_toggle(id):
    """Toggle testimonial active status."""
    testimonial = db.session.get(Testimonial, id)
    if testimonial:
        testimonial.is_active = not testimonial.is_active
        db.session.commit()
        flash('Testimonial status updated.', 'success')
    return redirect(url_for('admin.testimonials_list'))


@admin_bp.route('/testimonials/<string:id>/feature', methods=['POST'])
@login_required
def testimonials_feature(id):
    """Toggle testimonial featured status."""
    testimonial = db.session.get(Testimonial, id)
    if testimonial:
        testimonial.is_featured = not testimonial.is_featured
        db.session.commit()
        flash('Testimonial featured status updated.', 'success')
    return redirect(url_for('admin.testimonials_list'))


# ─── FAQs ───────────────────────────────────────────────────────

@admin_bp.route('/faqs')
@login_required
def faqs_list():
    """List all FAQs."""
    faqs = FAQ.query.order_by(FAQ.display_order).all()
    return render_template('admin/faqs/list.html', faqs=faqs)


@admin_bp.route('/faqs/add', methods=['GET', 'POST'])
@login_required
def faqs_add():
    """Add a new FAQ."""
    packages = Package.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()
        package_id = request.form.get('package_id') or None
        is_active = request.form.get('is_active') == 'on'
        
        if not question or not answer:
            flash('Question and answer are required.', 'error')
            return render_template('admin/faqs/form.html', mode='add', packages=packages)
            
        max_order = db.session.query(db.func.max(FAQ.display_order)).scalar() or 0
        faq = FAQ(
            question=question,
            answer=answer,
            package_id=package_id,
            display_order=max_order + 1,
            is_active=is_active
        )
        db.session.add(faq)
        db.session.commit()
        flash('FAQ added.', 'success')
        return redirect(url_for('admin.faqs_list'))
        
    return render_template('admin/faqs/form.html', mode='add', packages=packages)


@admin_bp.route('/faqs/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def faqs_edit(id):
    """Edit a FAQ."""
    faq = db.session.get(FAQ, id)
    if not faq:
        flash('FAQ not found.', 'error')
        return redirect(url_for('admin.faqs_list'))

    packages = Package.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()
        package_id = request.form.get('package_id') or None
        is_active = request.form.get('is_active') == 'on'
        
        if not question or not answer:
            flash('Question and answer are required.', 'error')
            return render_template('admin/faqs/form.html', mode='edit', faq=faq, packages=packages)
            
        faq.question = question
        faq.answer = answer
        faq.package_id = package_id
        faq.is_active = is_active
        
        db.session.commit()
        flash('FAQ updated.', 'success')
        return redirect(url_for('admin.faqs_list'))
        
    return render_template('admin/faqs/form.html', mode='edit', faq=faq, packages=packages)


@admin_bp.route('/faqs/<string:id>/toggle', methods=['POST'])
@login_required
def faqs_toggle(id):
    """Toggle FAQ active status."""
    faq = db.session.get(FAQ, id)
    if faq:
        faq.is_active = not faq.is_active
        db.session.commit()
        flash('FAQ status updated.', 'success')
    return redirect(url_for('admin.faqs_list'))


@admin_bp.route('/faqs/<string:id>/move/<string:direction>', methods=['POST'])
@login_required
def faqs_move(id, direction):
    """Move a FAQ up or down in display order."""
    faq = db.session.get(FAQ, id)
    if not faq:
        return redirect(url_for('admin.faqs_list'))
        
    current_order = faq.display_order
    
    if direction == 'up':
        swap_faq = FAQ.query.filter(FAQ.display_order < current_order).order_by(FAQ.display_order.desc()).first()
    elif direction == 'down':
        swap_faq = FAQ.query.filter(FAQ.display_order > current_order).order_by(FAQ.display_order.asc()).first()
    else:
        swap_faq = None
        
    if swap_faq:
        faq.display_order, swap_faq.display_order = swap_faq.display_order, faq.display_order
        db.session.commit()
        
    return redirect(url_for('admin.faqs_list'))


# ─── Inquiries (Mini CRM) ───────────────────────────────────────

@admin_bp.route('/inquiries')
@login_required
def inquiries_list():
    """List inquiries with optional status filtering."""
    status_filter = request.args.get('status')
    
    query = Inquiry.query
    if status_filter and status_filter in ['new', 'contacted', 'interested', 'booked', 'closed']:
        query = query.filter_by(status=status_filter)
        
    inquiries = query.order_by(Inquiry.created_at.desc()).all()
    
    # Get counts for tabs
    counts = {
        'all': Inquiry.query.count(),
        'new': Inquiry.query.filter_by(status='new').count(),
        'contacted': Inquiry.query.filter_by(status='contacted').count(),
        'interested': Inquiry.query.filter_by(status='interested').count(),
        'booked': Inquiry.query.filter_by(status='booked').count(),
        'closed': Inquiry.query.filter_by(status='closed').count(),
    }
    
    return render_template('admin/inquiries/list.html', 
                           inquiries=inquiries, 
                           current_status=status_filter,
                           counts=counts)


@admin_bp.route('/inquiries/<string:id>', methods=['GET', 'POST'])
@login_required
def inquiries_detail(id):
    """View and update an inquiry."""
    inquiry = db.session.get(Inquiry, id)
    if not inquiry:
        flash('Inquiry not found.', 'error')
        return redirect(url_for('admin.inquiries_list'))
        
    if request.method == 'POST':
        status = request.form.get('status')
        admin_notes = request.form.get('admin_notes', '').strip()
        
        if status in ['new', 'contacted', 'interested', 'booked', 'closed']:
            inquiry.status = status
            
        inquiry.admin_notes = admin_notes
        db.session.commit()
        
        flash('Inquiry updated.', 'success')
        return redirect(url_for('admin.inquiries_detail', id=inquiry.id))
        
    return render_template('admin/inquiries/detail.html', inquiry=inquiry)


# ─── Activities ─────────────────────────────────────────────────

@admin_bp.route('/activities')
@login_required
def activities_list():
    """List all activities."""
    activities = Activity.query.order_by(Activity.name).all()
    return render_template('admin/activities/list.html', activities=activities)


@admin_bp.route('/activities/add', methods=['GET', 'POST'])
@login_required
def activities_add():
    """Add a new activity."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        is_active = request.form.get('is_active') == 'on'

        if not name:
            flash('Activity name is required.', 'error')
            return render_template('admin/activities/form.html', mode='add')

        slug = generate_slug(name)
        existing = Activity.query.filter_by(slug=slug).first()
        if existing:
            flash(f'An activity with slug "{slug}" already exists.', 'error')
            return render_template('admin/activities/form.html', mode='add')

        activity = Activity(
            name=name,
            slug=slug,
            description=description or None,
            image_url=image_url or None,
            is_active=is_active
        )
        db.session.add(activity)
        db.session.commit()
        flash(f'Activity "{name}" added.', 'success')
        return redirect(url_for('admin.activities_list'))

    return render_template('admin/activities/form.html', mode='add')


@admin_bp.route('/activities/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def activities_edit(id):
    """Edit an activity."""
    activity = db.session.get(Activity, id)
    if not activity:
        flash('Activity not found.', 'error')
        return redirect(url_for('admin.activities_list'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        is_active = request.form.get('is_active') == 'on'

        if not name:
            flash('Activity name is required.', 'error')
            return render_template('admin/activities/form.html', mode='edit', activity=activity)

        new_slug = generate_slug(name)
        if new_slug != activity.slug:
            existing = Activity.query.filter_by(slug=new_slug).first()
            if existing:
                flash(f'An activity with slug "{new_slug}" already exists.', 'error')
                return render_template('admin/activities/form.html', mode='edit', activity=activity)
            activity.slug = new_slug

        activity.name = name
        activity.description = description or None
        activity.image_url = image_url or None
        activity.is_active = is_active

        db.session.commit()
        flash(f'Activity "{name}" updated.', 'success')
        return redirect(url_for('admin.activities_list'))

    return render_template('admin/activities/form.html', mode='edit', activity=activity)


@admin_bp.route('/activities/<string:id>/toggle', methods=['POST'])
@login_required
def activities_toggle(id):
    """Toggle activity active status."""
    activity = db.session.get(Activity, id)
    if activity:
        activity.is_active = not activity.is_active
        db.session.commit()
        flash('Activity status updated.', 'success')
    return redirect(url_for('admin.activities_list'))


# ─── Package Departures ─────────────────────────────────────────

@admin_bp.route('/packages/<string:package_id>/departures/add', methods=['POST'])
@login_required
def package_departures_add(package_id):
    """Add a departure to a package."""
    package = db.session.get(Package, package_id)
    if not package:
        return redirect(url_for('admin.packages_list'))

    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    price_override = request.form.get('price_override')
    available_seats = request.form.get('available_seats')
    status = request.form.get('status')

    if start_date and end_date:
        from datetime import datetime
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            departure = PackageDeparture(
                package_id=package.id,
                start_date=start_dt,
                end_date=end_dt,
                price_override=float(price_override) if price_override else None,
                available_seats=int(available_seats) if available_seats else None,
                status=status or 'Available'
            )
            db.session.add(departure)
            db.session.commit()
            flash('Departure added.', 'success')
        except ValueError:
            flash('Invalid date format.', 'error')

    return redirect(url_for('admin.packages_edit', id=package.id) + '#departures')


@admin_bp.route('/packages/<string:package_id>/departures/<string:departure_id>/delete', methods=['POST'])
@login_required
def package_departures_delete(package_id, departure_id):
    """Delete a departure from a package."""
    departure = db.session.get(PackageDeparture, departure_id)
    if departure and departure.package_id == package_id:
        db.session.delete(departure)
        db.session.commit()
        flash('Departure deleted.', 'success')
    return redirect(url_for('admin.packages_edit', id=package_id) + '#departures')


# ─── Site Settings ──────────────────────────────────────────────

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def site_settings():
    """Manage global business information."""
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings(business_name='M.A. Tours & Travels')
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        settings.business_name = request.form.get('business_name', '').strip()
        settings.phone = request.form.get('phone', '').strip() or None
        settings.whatsapp = request.form.get('whatsapp', '').strip() or None
        settings.email = request.form.get('email', '').strip() or None
        settings.address = request.form.get('address', '').strip() or None
        settings.facebook_url = request.form.get('facebook_url', '').strip() or None
        settings.instagram_url = request.form.get('instagram_url', '').strip() or None
        settings.youtube_url = request.form.get('youtube_url', '').strip() or None
        settings.google_maps_url = request.form.get('google_maps_url', '').strip() or None
        settings.footer_text = request.form.get('footer_text', '').strip() or None
        
        db.session.commit()
        flash('Site settings updated.', 'success')
        return redirect(url_for('admin.site_settings'))
        
    return render_template('admin/settings/form.html', settings=settings)
