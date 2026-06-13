from app import create_app
from app.extensions import db
from app.models.faq import FAQ
from app.models.inquiry import Inquiry
import random
import datetime

def seed_more_data():
    app = create_app()
    with app.app_context():
        print("Seeding FAQs...")
        faqs = [
            {'question': 'When is the best time to visit Kashmir?', 'answer': 'The best time to visit Kashmir is from March to October when the weather is pleasant and the gardens are in full bloom. Winter is great for skiing.'},
            {'question': 'Do I need a special permit to visit border areas?', 'answer': 'Yes, for places like Gurez Valley or certain parts of Leh-Ladakh, you need an Inner Line Permit. We help arrange these for our guests.'},
            {'question': 'Is it safe to travel with family?', 'answer': 'Absolutely. Kashmir is extremely safe for tourists and locals are very welcoming to families.'},
            {'question': 'What kind of clothing should I pack?', 'answer': 'Pack light woolens for summer evenings, and heavy woolens, thermals, and snow-boots for winter trips.'}
        ]
        max_order = db.session.query(db.func.max(FAQ.display_order)).scalar() or 0
        for i, f in enumerate(faqs):
            obj = FAQ.query.filter_by(question=f['question']).first()
            if not obj:
                obj = FAQ(question=f['question'], answer=f['answer'], display_order=max_order + i + 1, is_active=True)
                db.session.add(obj)
        
        print("Seeding Inquiries...")
        inquiries = [
            {'name': 'Alex Johnson', 'email': 'alex.j@example.com', 'phone': '9876543210', 'message': 'I am looking for a 5-day family trip.', 'travelers_count': 4, 'status': 'new'},
            {'name': 'Sarah Smith', 'email': 'sarah.s@example.com', 'phone': '8765432109', 'message': 'Honeymoon package inquiry for December.', 'travelers_count': 2, 'status': 'contacted'},
            {'name': 'Michael Brown', 'email': 'mike.b@example.com', 'phone': '7654321098', 'message': 'Do you offer group discounts for college trips?', 'travelers_count': 15, 'status': 'interested'}
        ]
        for inq in inquiries:
            obj = Inquiry.query.filter_by(email=inq['email']).first()
            if not obj:
                obj = Inquiry(
                    name=inq['name'],
                    email=inq['email'],
                    phone=inq['phone'],
                    message=inq['message'],
                    travelers_count=inq['travelers_count'],
                    status=inq['status']
                )
                db.session.add(obj)
        
        db.session.commit()
        print("Successfully seeded FAQs and Inquiries.")

if __name__ == '__main__':
    seed_more_data()
