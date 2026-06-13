from app import create_app
from app.extensions import db
from app.models.destination import Destination
from app.models.activity_category import ActivityCategory
from app.models.activity import Activity
from app.models.package import Package
from app.models.testimonial import Testimonial
from app.utils import generate_slug
import random

def seed_mock_data():
    app = create_app()
    with app.app_context():
        print("Seeding mock Destinations...")
        dests = [
            {'name': 'Srinagar', 'description': 'The summer capital of Jammu and Kashmir, known for its serene Dal Lake and Mughal Gardens.', 'hero_image_url': 'https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&q=80'},
            {'name': 'Gulmarg', 'description': 'A popular skiing destination and hill station surrounded by snow-capped mountains.', 'hero_image_url': 'https://images.unsplash.com/photo-1605640840605-14ac1855827b?auto=format&fit=crop&q=80'},
            {'name': 'Pahalgam', 'description': 'The Valley of Shepherds, a beautiful town located at the confluence of the Lidder River.', 'hero_image_url': 'https://images.unsplash.com/photo-1622308644420-b2fc1d0f5ec8?auto=format&fit=crop&q=80'},
            {'name': 'Sonamarg', 'description': 'The Meadow of Gold, known for its pristine lakes and majestic glaciers.', 'hero_image_url': 'https://images.unsplash.com/photo-1582455949175-99d81d27cb22?auto=format&fit=crop&q=80'}
        ]
        dest_objs = {}
        for d in dests:
            slug = generate_slug(d['name'])
            obj = Destination.query.filter_by(slug=slug).first()
            if not obj:
                obj = Destination(name=d['name'], slug=slug, description=d['description'], hero_image_url=d['hero_image_url'])
                db.session.add(obj)
            dest_objs[d['name']] = obj
        db.session.commit()

        print("Seeding mock Activity Categories...")
        cats = [
            {'name': 'Adventure', 'description': 'Thrilling activities for the brave hearted.', 'image_url': 'https://images.unsplash.com/photo-1533587851505-d119e131928F?auto=format&fit=crop&q=80'},
            {'name': 'Nature & Wildlife', 'description': 'Explore the beautiful flora and fauna of Kashmir.', 'image_url': 'https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&q=80'},
            {'name': 'Sightseeing', 'description': 'Visit the most popular tourist attractions.', 'image_url': 'https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&q=80'},
            {'name': 'Winter Sports', 'description': 'Skiing, snowboarding and more.', 'image_url': 'https://images.unsplash.com/photo-1605640840605-14ac1855827b?auto=format&fit=crop&q=80'}
        ]
        cat_objs = {}
        for c in cats:
            slug = generate_slug(c['name'])
            obj = ActivityCategory.query.filter_by(slug=slug).first()
            if not obj:
                obj = ActivityCategory(name=c['name'], slug=slug, description=c['description'], image_url=c['image_url'])
                db.session.add(obj)
            cat_objs[c['name']] = obj
        db.session.commit()

        print("Seeding mock Activities...")
        acts = [
            {'name': 'Shikara Ride', 'category': 'Nature & Wildlife', 'description': 'A relaxing ride on the Dal Lake.', 'image_url': 'https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&q=80'},
            {'name': 'Gondola Ride', 'category': 'Sightseeing', 'description': 'A breathtaking cable car ride in Gulmarg.', 'image_url': 'https://images.unsplash.com/photo-1605640840605-14ac1855827b?auto=format&fit=crop&q=80'},
            {'name': 'Skiing', 'category': 'Winter Sports', 'description': 'Glide down the snowy slopes of Gulmarg.', 'image_url': 'https://images.unsplash.com/photo-1551524164-687a55dd1126?auto=format&fit=crop&q=80'},
            {'name': 'River Rafting', 'category': 'Adventure', 'description': 'Tame the wild waters of the Lidder river.', 'image_url': 'https://images.unsplash.com/photo-1533587851505-d119e131928F?auto=format&fit=crop&q=80'},
            {'name': 'Trekking', 'category': 'Adventure', 'description': 'Hike through the beautiful trails of Pahalgam.', 'image_url': 'https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&q=80'}
        ]
        act_objs = []
        for a in acts:
            slug = generate_slug(a['name'])
            obj = Activity.query.filter_by(slug=slug).first()
            if not obj:
                obj = Activity(name=a['name'], slug=slug, description=a['description'], image_url=a['image_url'], category_id=cat_objs[a['category']].id)
                db.session.add(obj)
            act_objs.append(obj)
        db.session.commit()

        print("Seeding mock Packages...")
        pkgs = [
            {'title': 'Kashmir Paradise Tour', 'destination': 'Srinagar', 'price': 15000, 'days': 5, 'nights': 4, 'desc': 'A wonderful 5 day trip to Srinagar and Gulmarg.'},
            {'title': 'Romantic Honeymoon in Gulmarg', 'destination': 'Gulmarg', 'price': 25000, 'days': 6, 'nights': 5, 'desc': 'Spend your honeymoon in the romantic snowy peaks of Gulmarg.'},
            {'title': 'Family Vacation Package', 'destination': 'Pahalgam', 'price': 18000, 'days': 4, 'nights': 3, 'desc': 'A relaxing family vacation in the valley of shepherds.'}
        ]
        for p in pkgs:
            slug = generate_slug(p['title'])
            obj = Package.query.filter_by(slug=slug).first()
            if not obj:
                obj = Package(title=p['title'], slug=slug, destination_id=dest_objs[p['destination']].id, price_from=p['price'], duration_days=p['days'], duration_nights=p['nights'], short_description=p['desc'], is_featured=True)
                # add some random activities
                obj.activities = random.sample(act_objs, 2)
                db.session.add(obj)
        db.session.commit()

        print("Seeding mock Testimonials...")
        tests = [
            {'name': 'John Doe', 'package': 'Kashmir Paradise Tour', 'review': 'It was an amazing trip! The views were stunning and the service was excellent.', 'rating': 5},
            {'name': 'Jane Smith', 'package': 'Romantic Honeymoon in Gulmarg', 'review': 'We had the most romantic honeymoon. Thank you M.A. Tours!', 'rating': 5},
            {'name': 'Ahmed Khan', 'package': 'Family Vacation Package', 'review': 'Great family trip, the kids loved the Shikara ride.', 'rating': 4}
        ]
        for t in tests:
            obj = Testimonial.query.filter_by(name=t['name']).first()
            if not obj:
                pkg = Package.query.filter_by(title=t['package']).first()
                obj = Testimonial(name=t['name'], package_taken=t['package'], package_id=pkg.id if pkg else None, review=t['review'], rating=t['rating'], is_featured=True)
                db.session.add(obj)
        db.session.commit()

        print("Mock data seeded successfully!")

if __name__ == '__main__':
    seed_mock_data()
