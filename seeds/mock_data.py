"""
Script to seed the database with rich mock data for demonstration.
Usage: flask mock-data
"""
import uuid
import random
from app.extensions import db
from app.models.destination import Destination
from app.models.activity_category import ActivityCategory
from app.models.activity import Activity
from app.models.package import Package
from app.models.hero_slide import HeroSlide
from app.models.testimonial import Testimonial
from app.models.faq import FAQ
from app.models.gallery import HomepageGalleryImage
from app.models.travel_style import TravelStyle

def run_mock_seeds():
    print("Seeding mock data...")
    
    # Hero Slides
    print("Adding Hero Slides...")
    slides = [
        {"title": "Discover the Magic of Kashmir", "subtitle": "Welcome to Paradise", "image_url": "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80", "display_order": 1, "cta_text": "Explore Packages", "cta_link": "/packages"},
        {"title": "Experience Winter Wonderland", "subtitle": "Gulmarg Awaits", "image_url": "https://images.unsplash.com/photo-1605640840469-60ef093848b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80", "display_order": 2, "cta_text": "View Ski Packages", "cta_link": "/packages"}
    ]
    for slide in slides:
        if not HeroSlide.query.filter_by(title=slide['title']).first():
            db.session.add(HeroSlide(**slide))

    # Destinations
    print("Adding Destinations...")
    dests = {
        "Srinagar": Destination(name="Srinagar", slug="srinagar", hero_image_url="https://images.unsplash.com/photo-1595815771614-ade9d652a65d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", description="The summer capital of Jammu and Kashmir, known for its serene lakes and houseboats.", is_international=False),
        "Gulmarg": Destination(name="Gulmarg", slug="gulmarg", hero_image_url="https://images.unsplash.com/photo-1605640840469-60ef093848b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", description="A popular skiing destination and a beautiful hill station.", is_international=False),
        "Pahalgam": Destination(name="Pahalgam", slug="pahalgam", hero_image_url="https://images.unsplash.com/photo-1626084620580-041490231846?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", description="The Valley of Shepherds, famous for its lush green meadows.", is_international=False)
    }
    for name, dest in dests.items():
        if not Destination.query.filter_by(slug=dest.slug).first():
            db.session.add(dest)
    db.session.commit()

    # Activity Categories
    print("Adding Activity Categories...")
    cats = {
        "Shikara Rides": ActivityCategory(name="Shikara Rides", slug="shikara-rides", image_url="https://images.unsplash.com/photo-1595815771614-ade9d652a65d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", display_order=1),
        "Skiing": ActivityCategory(name="Skiing & Snowboarding", slug="skiing", image_url="https://images.unsplash.com/photo-1605640840469-60ef093848b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", display_order=2),
        "Trekking": ActivityCategory(name="Trekking & Hiking", slug="trekking", image_url="https://images.unsplash.com/photo-1626084620580-041490231846?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", display_order=3)
    }
    for name, cat in cats.items():
        if not ActivityCategory.query.filter_by(slug=cat.slug).first():
            db.session.add(cat)
    db.session.commit()

    # Activities
    print("Adding Activities...")
    acts = [
        {"name": "Dal Lake Sunset Shikara Ride", "slug": "dal-lake-sunset", "category_id": cats["Shikara Rides"].id, "image_url": "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "description": "Experience the peaceful and enchanting sunset on the famous Dal Lake in a traditional Shikara."},
        {"name": "Gulmarg Gondola Ride", "slug": "gulmarg-gondola", "category_id": cats["Skiing"].id, "image_url": "https://images.unsplash.com/photo-1605640840469-60ef093848b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "description": "Ride one of the highest cable cars in the world, offering panoramic views of snow-clad mountains."}
    ]
    for act in acts:
        if not Activity.query.filter_by(slug=act['slug']).first():
            db.session.add(Activity(**act))

    # Packages
    print("Adding Packages...")
    srinagar_id = Destination.query.filter_by(slug='srinagar').first().id
    style_id = TravelStyle.query.filter_by(slug='domestic').first().id
    p1 = Package(title="Majestic Kashmir Tour", slug="majestic-kashmir", destination_id=srinagar_id, price_from=15000, duration_days=5, duration_nights=4, short_description="A beautiful 5-day tour covering Srinagar, Gulmarg, and Pahalgam with houseboat stays.", description="Detailed itinerary goes here.")
    
    if not Package.query.filter_by(slug=p1.slug).first():
        db.session.add(p1)
        db.session.commit()
        # Associate with travel style
        p1.travel_styles.append(TravelStyle.query.get(style_id))
        db.session.commit()

    # Testimonials
    print("Adding Testimonials...")
    tests = [
        {"name": "Aarav Sharma", "review": "The houseboat stay in Srinagar was a lifetime experience! Everything was perfectly organized by M A Tours.", "rating": 5, "is_featured": True, "package_taken": "Majestic Kashmir Tour"},
        {"name": "Priya Singh", "review": "Gulmarg was breathtaking. The driver was very polite and helpful. Excellent service overall.", "rating": 5, "is_featured": True, "package_taken": "Winter Wonderland Package"}
    ]
    for test in tests:
        if not Testimonial.query.filter_by(name=test['name']).first():
            db.session.add(Testimonial(**test))

    # FAQs
    print("Adding FAQs...")
    faqs = [
        {"question": "When is the best time to visit Kashmir?", "answer": "Kashmir is a year-round destination. Visit between March and October for pleasant weather and beautiful gardens, or between December and February for snow and winter sports in Gulmarg.", "display_order": 1},
        {"question": "Is it safe to travel to Kashmir?", "answer": "Yes, Kashmir is very safe for tourists. Locals are extremely welcoming and hospitable. Thousands of tourists visit the valley every year without any issues.", "display_order": 2}
    ]
    for faq in faqs:
        if not FAQ.query.filter_by(question=faq['question']).first():
            db.session.add(FAQ(**faq))

    # Homepage Gallery Images (Bento Grid)
    print("Adding Homepage Gallery Images...")
    bento_images = [
        {"image_url": "https://images.unsplash.com/photo-1598091383021-14ddee147322?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Dal Lake Reflections", "display_order": 1},
        {"image_url": "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Shikara at Sunset", "display_order": 2},
        {"image_url": "https://images.unsplash.com/photo-1605640840469-60ef093848b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Snowy Peaks of Gulmarg", "display_order": 3},
        {"image_url": "https://images.unsplash.com/photo-1626084620580-041490231846?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Pahalgam Valley", "display_order": 4},
        {"image_url": "https://images.unsplash.com/photo-1598091383021-14ddee147322?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Kashmiri Houseboat", "display_order": 5},
        {"image_url": "https://images.unsplash.com/photo-1605640840469-60ef093848b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Skiing Adventures", "display_order": 6},
        {"image_url": "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Traditional Shikara", "display_order": 7},
        {"image_url": "https://images.unsplash.com/photo-1626084620580-041490231846?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "caption": "Pine Forests", "display_order": 8}
    ]
    for img in bento_images:
        if not HomepageGalleryImage.query.filter_by(caption=img['caption']).first():
            db.session.add(HomepageGalleryImage(**img))

    db.session.commit()
    print("Mock data seeded successfully!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        run_mock_seeds()
