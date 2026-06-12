from app import create_app
from app.extensions import db
from app.models.inquiry import Inquiry
from app.models.package import Package

app = create_app()

with app.app_context():
    package = Package.query.first()
    
    inquiries = [
        Inquiry(
            name="John Doe",
            phone="+91 9876543210",
            email="john@example.com",
            message="Looking for a honeymoon package next month.",
            source="homepage",
            status="new"
        ),
        Inquiry(
            name="Jane Smith",
            phone="+91 1234567890",
            message="Interested in the winter package.",
            source="package",
            package_id=package.id if package else None,
            status="new"
        ),
        Inquiry(
            name="Alice Brown",
            phone="+1 555 123 4567",
            email="alice@test.com",
            source="whatsapp",
            status="contacted",
            admin_notes="Called her on Tuesday, she wants to discuss budget."
        )
    ]
    
    db.session.add_all(inquiries)
    db.session.commit()
    print("Inquiries seeded.")
