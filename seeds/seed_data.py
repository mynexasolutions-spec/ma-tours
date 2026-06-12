"""
Seed script for M A Tours & Travels.

Seeds:
- 6 default categories
- 1 admin user
- 1 site_settings row with business info

Usage:
    flask seed
"""

from app.extensions import db
from app.models.admin import Admin
from app.models.category import Category
from app.models.site_settings import SiteSettings


def seed_categories():
    """Seed default package categories."""
    categories = [
        {'name': 'Domestic', 'slug': 'domestic'},
        {'name': 'International', 'slug': 'international'},
        {'name': 'Honeymoon', 'slug': 'honeymoon'},
        {'name': 'Family', 'slug': 'family'},
        {'name': 'Group Tour', 'slug': 'group-tour'},
        {'name': 'Umrah', 'slug': 'umrah'},
    ]

    for cat_data in categories:
        existing = Category.query.filter_by(slug=cat_data['slug']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
            print(f'  + Category: {cat_data["name"]}')
        else:
            print(f'  - Category already exists: {cat_data["name"]}')

    db.session.commit()


def seed_admin():
    """Seed default admin user."""
    email = 'admin@matoursandtravels.com'
    existing = Admin.query.filter_by(email=email).first()

    if not existing:
        admin = Admin(
            name='Admin',
            email=email,
        )
        admin.set_password('changeme123')
        db.session.add(admin)
        db.session.commit()
        print(f'  + Admin user: {email}')
    else:
        print(f'  - Admin already exists: {email}')


def seed_site_settings():
    """Seed default site settings with business information."""
    existing = SiteSettings.query.first()

    if not existing:
        settings = SiteSettings(
            business_name='M A Tours And Travels',
            phone='7304916310',
            whatsapp='7304916310',
            email='matoursandtravels193@gmail.com',
            address='',
            facebook_url='https://www.facebook.com/matoursandtravelsonline',
            instagram_url='https://www.instagram.com/matoursandtravelsonline',
            youtube_url='',
            google_maps_url='',
            footer_text='© M A Tours And Travels. All rights reserved.',
        )
        db.session.add(settings)
        db.session.commit()
        print('  + Site settings created')
    else:
        print('  - Site settings already exist')


def run_seeds():
    """Run all seed functions."""
    print('\n--- Seeding database ---\n')

    print('Categories:')
    seed_categories()

    print('\nAdmin:')
    seed_admin()

    print('\nSite Settings:')
    seed_site_settings()

    print('\n--- Seeding complete! ---\n')
