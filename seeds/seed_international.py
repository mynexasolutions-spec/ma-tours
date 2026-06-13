from app import create_app
from app.extensions import db
from app.models.destination import Destination
from app.models.package import Package

def seed_international():
    app = create_app()
    with app.app_context():
        print("Seeding international destination...")
        dubai = Destination.query.filter_by(slug='dubai').first()
        if not dubai:
            dubai = Destination(
                name="Dubai",
                slug="dubai",
                description="Experience the luxury, shopping, and modern architecture of the UAE.",
                hero_image_url="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&q=80&w=2070",
                is_international=True,
                is_active=True
            )
            db.session.add(dubai)
            db.session.flush() # get ID
            
        # Add a package
        pkg = Package.query.filter_by(slug='dubai-luxury-escape').first()
        if not pkg:
            pkg = Package(
                title="Dubai Luxury Escape",
                slug="dubai-luxury-escape",
                destination_id=dubai.id,
                short_description="5 days of luxury in the heart of Dubai.",
                description="A fantastic tour covering Burj Khalifa, Desert Safari, and luxury shopping.",
                price_from=120000,
                duration_days=5,
                duration_nights=4,
                is_active=True,
                is_featured=True
            )
            db.session.add(pkg)
            
        db.session.commit()
        print("Successfully seeded Dubai!")

if __name__ == '__main__':
    seed_international()
