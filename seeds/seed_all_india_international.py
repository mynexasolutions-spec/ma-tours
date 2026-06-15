import sys
import os
import random
import datetime
from decimal import Decimal

# Add the workspace root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.destination import Destination
from app.models.activity_category import ActivityCategory
from app.models.activity import Activity
from app.models.package import Package, PackageHighlight, PackageInclusion, PackageExclusion, PackageItinerary
from app.models.testimonial import Testimonial
from app.models.faq import FAQ
from app.models.inquiry import Inquiry
from app.models.departure import PackageDeparture
from app.utils import generate_slug

def seed_all():
    app = create_app()
    with app.app_context():
        print("--- Seeding All India & International Tours Data ---")

        # 1. Seed Destinations
        destinations_data = [
            {'name': 'Goa', 'description': 'India\'s ultimate beach destination, famous for its golden sand beaches, historic Portuguese architecture, and vibrant nightlife.', 'is_international': False},
            {'name': 'Kerala', 'description': 'Known as "God\'s Own Country", Kerala is famous for its serene backwaters, traditional houseboats, spices, and misty hill stations like Munnar.', 'is_international': False},
            {'name': 'Rajasthan', 'description': 'The land of royalty, palaces, forts, and rich heritage. Experience the culture of Jaipur, Udaipur, and Jaisalmer.', 'is_international': False},
            {'name': 'Andaman Islands', 'description': 'A tropical paradise in the Bay of Bengal, known for its pristine beaches, turquoise waters, and world-class scuba diving spots.', 'is_international': False},
            {'name': 'Himachal Pradesh', 'description': 'Breathtaking hill stations surrounded by snow-capped Himalayan peaks. Ideal for adventure lovers in Manali, Shimla, and Dharamshala.', 'is_international': False},
            {'name': 'Dubai', 'description': 'Experience the futuristic city of Dubai with its iconic skyscrapers like Burj Khalifa, luxury shopping malls, and thrilling desert safaris.', 'is_international': True},
            {'name': 'Thailand', 'description': 'The Land of Smiles, famous for its tropical beaches, ornate royal temples, active street markets, and islands like Phuket and Krabi.', 'is_international': True},
            {'name': 'Bali', 'description': 'The Island of the Gods, renowned for its forested volcanic mountains, iconic rice paddies, beaches, coral reefs, and spiritual heritage.', 'is_international': True},
            {'name': 'Maldives', 'description': 'A luxurious tropical getaway featuring crystal-clear blue lagoons, vibrant coral reefs, and premium overwater villas.', 'is_international': True},
            {'name': 'Switzerland', 'description': 'Experience the magical Swiss Alps, pristine lakes, charming villages, and high-altitude adventures in Jungfraujoch and Zermatt.', 'is_international': True}
        ]

        dest_objs = {}
        for d in destinations_data:
            slug = generate_slug(d['name'])
            obj = Destination.query.filter_by(slug=slug).first()
            if not obj:
                obj = Destination(
                    name=d['name'],
                    slug=slug,
                    description=d['description'],
                    is_international=d['is_international'],
                    hero_image_url=None, # User wants to upload manually
                    is_active=True
                )
                db.session.add(obj)
                db.session.flush()
                print(f"  + Destination: {d['name']}")
            else:
                print(f"  - Destination already exists: {d['name']}")
            dest_objs[d['name']] = obj

        # 2. Seed Activity Categories
        categories_data = [
            {'name': 'Water Sports', 'description': 'Thrilling water-based activities like scuba diving, snorkeling, and parasailing.'},
            {'name': 'Adventure', 'description': 'High energy activities including trekking, desert safaris, and mountaineering.'},
            {'name': 'Cultural & Heritage', 'description': 'Explore historic monuments, ancient forts, temples, and local traditions.'},
            {'name': 'Sightseeing', 'description': 'Guided tours to the most scenic viewpoints, landmarks, and city attractions.'},
            {'name': 'Nature & Wildlife', 'description': 'National park safaris, scenic boat cruises, and close encounters with wildlife.'}
        ]

        cat_objs = {}
        for c in categories_data:
            slug = generate_slug(c['name'])
            obj = ActivityCategory.query.filter_by(slug=slug).first()
            if not obj:
                obj = ActivityCategory(
                    name=c['name'],
                    slug=slug,
                    description=c['description'],
                    image_url=None
                )
                db.session.add(obj)
                db.session.flush()
                print(f"  + Activity Category: {c['name']}")
            else:
                print(f"  - Activity Category already exists: {c['name']}")
            cat_objs[c['name']] = obj

        # 3. Seed Activities
        activities_data = [
            {'name': 'Scuba Diving', 'category': 'Water Sports', 'description': 'Explore underwater marine life and beautiful coral reefs.'},
            {'name': 'Snorkeling', 'category': 'Water Sports', 'description': 'Swim on the surface of crystal-clear water and view shallow corals.'},
            {'name': 'Parasailing', 'category': 'Water Sports', 'description': 'Soar high above the ocean and get a bird\'s eye view of the coast.'},
            {'name': 'Desert Safari', 'category': 'Adventure', 'description': 'Thrilling dune bashing, camel rides, and traditional dinner in a desert camp.'},
            {'name': 'Mountain Trekking', 'category': 'Adventure', 'description': 'Guided treks through scenic mountain trails and green valleys.'},
            {'name': 'Fort Exploring', 'category': 'Cultural & Heritage', 'description': 'Visit massive historic palaces, battlements, and museums.'},
            {'name': 'Temple Sightseeing', 'category': 'Cultural & Heritage', 'description': 'Explore magnificent ancient temples and cultural sites.'},
            {'name': 'Houseboat Cruise', 'category': 'Nature & Wildlife', 'description': 'Spend a relaxing night on a traditional houseboat cruising through palm-fringed canals.'},
            {'name': 'Elephant Safari', 'category': 'Nature & Wildlife', 'description': 'Ride through spice gardens or national forests on an elephant.'},
            {'name': 'Cable Car Ride', 'category': 'Sightseeing', 'description': 'Enjoy panoramic aerial views of mountains and valleys.'},
            {'name': 'City Sightseeing Tour', 'category': 'Sightseeing', 'description': 'A guided tour of local landmarks, markets, and tourist hubs.'}
        ]

        act_objs = {}
        for a in activities_data:
            slug = generate_slug(a['name'])
            obj = Activity.query.filter_by(slug=slug).first()
            if not obj:
                obj = Activity(
                    name=a['name'],
                    slug=slug,
                    description=a['description'],
                    image_url=None,
                    category_id=cat_objs[a['category']].id,
                    is_active=True
                )
                db.session.add(obj)
                db.session.flush()
                print(f"  + Activity: {a['name']}")
            else:
                print(f"  - Activity already exists: {a['name']}")
            act_objs[a['name']] = obj

        # 4. Seed Packages with detailed high-quality data
        packages_data = [
            {
                'title': 'Goa Beach Escape & Water Sports',
                'dest_name': 'Goa',
                'price': 12500,
                'days': 4,
                'nights': 3,
                'short': 'Relax on Goa\'s sun-kissed beaches and experience high-adrenaline water sports.',
                'desc': '<p>Goa is the beach capital of India. This tour takes you through North Goa\'s popular beaches (Calangute, Baga) and South Goa\'s historic churches.</p><p>Includes a full day of water sports adventure (Scuba diving, Jet Ski, Banana ride, Parasailing) and cozy beachside stays.</p>',
                'acts': ['Scuba Diving', 'Parasailing', 'City Sightseeing Tour'],
                'highlights': [
                    "Parasailing, Jet Ski, Banana Ride, and Bumper Ride at Baga Beach",
                    "Fascinating Scuba Diving experience with underwater photos/videos",
                    "Guided sightseeing of historic churches and temples in Old Goa",
                    "Romantic sunset cruise on the Mandovi River"
                ],
                'inclusions': [
                    "3 Nights accommodation in a 3-star beachside resort",
                    "Daily breakfast at the resort",
                    "Full day North Goa sightseeing by private AC sedan",
                    "Full day South Goa sightseeing by private AC sedan",
                    "Scuba Diving & Water Sports activity package with transfers",
                    "Airport pick-up and drop-off"
                ],
                'exclusions': [
                    "Airfare or train tickets",
                    "Lunch and dinner (unless specified)",
                    "Personal expenses (laundry, telephone, tips)",
                    "Any monument entry fees"
                ],
                'itinerary': [
                    {"title": "Arrival in Goa & Sunset Cruise", "description": "On arrival at Goa Airport/Railway Station, meet our representative and transfer to your resort. Check-in and relax. In the evening, enjoy a romantic sunset cruise on the Mandovi River with music and dance performances. Overnight stay in Goa."},
                    {"title": "North Goa Sightseeing & Baga Beach", "description": "After breakfast, proceed for a full-day tour of North Goa. Visit Fort Aguada, Coco Beach, Calangute Beach, Baga Beach, and Anjuna Beach. Indulge in shopping at local flea markets. Overnight stay in Goa."},
                    {"title": "Scuba Diving & Water Sports Adventure", "description": "Early morning, head to the scuba diving site. Enjoy a boat ride, briefing, and a thrilling dive to witness marine life. Follow this with a combo of water sports including Jet Ski, Parasailing, Banana ride, and Bumper ride. Return to resort in the evening. Overnight stay in Goa."},
                    {"title": "South Goa Tour & Departure", "description": "Check out after breakfast. Visit Old Goa Churches (Basilica of Bom Jesus, Se Cathedral), Mangueshi Temple, and Miramar Beach. Later, transfer to the airport or railway station for your onward journey."}
                ],
                'departures': [
                    {'start_offset': 10, 'end_offset': 13, 'seats': 15, 'status': 'Available'},
                    {'start_offset': 20, 'end_offset': 23, 'seats': 10, 'status': 'Filling Fast'}
                ]
            },
            {
                'title': 'Kerala Backwater Serenade',
                'dest_name': 'Kerala',
                'price': 18000,
                'days': 5,
                'nights': 4,
                'short': 'Cruise the tranquil backwaters on a private houseboat and tour the tea gardens of Munnar.',
                'desc': '<p>Unwind in God\'s Own Country. Spend your first two days exploring the lush tea plantations and waterfalls of Munnar.</p><p>Experience a magical overnight stay on a premium houseboat in Alleppey, floating along palm-fringed backwaters with freshly cooked Keralite meals served on board.</p>',
                'acts': ['Houseboat Cruise', 'Elephant Safari', 'City Sightseeing Tour'],
                'highlights': [
                    "Overnight stay in a private traditional Kettuvallam houseboat",
                    "Explore lush green tea plantations and estates in Munnar",
                    "Scenic waterfalls: Cheeyappara and Valara",
                    "Boating on Periyar Lake in Thekkady wildlife sanctuary"
                ],
                'inclusions': [
                    "2 Nights in Munnar (premium hill resort), 1 Night in Thekkady, 1 Night in Houseboat",
                    "Houseboat stay includes all meals (Breakfast, Lunch, Dinner)",
                    "Breakfast at Munnar and Thekkady hotels",
                    "All transfers and sightseeing by private AC Cab",
                    "Spice plantation tour in Thekkady"
                ],
                'exclusions': [
                    "Airfare or train tickets",
                    "Entry tickets to national parks, spice gardens, and boating",
                    "Any personal expenses, tips, and drinks"
                ],
                'itinerary': [
                    {"title": "Cochin to Munnar (Lush Hill Station)", "description": "Arrive at Cochin Airport/Railway Station. Drive to Munnar, enjoying scenic views, waterfalls (Cheeyappara & Valara), and tea gardens along the way. Check-in to your resort in Munnar and spend the evening at leisure. Overnight in Munnar."},
                    {"title": "Munnar Sightseeing Tour", "description": "After breakfast, visit Eravikulam National Park (home to Nilgiri Tahr), Mattupetty Dam, Echo Point, Kundala Lake, and the Tea Museum. Return to the resort for overnight stay."},
                    {"title": "Munnar to Thekkady (Wildlife & Spices)", "description": "Drive to Thekkady. Check-in and proceed for a guided spice plantation tour. In the evening, enjoy boating on Periyar Lake to spot wild animals or watch a traditional Kathakali show. Overnight in Thekkady."},
                    {"title": "Houseboat Experience in Alleppey", "description": "Check out and drive to Alleppey. Embark on your private houseboat at noon. Cruise through the scenic backwaters, canals, and villages. Enjoy traditional Kerala lunch, evening tea with snacks, and dinner on board. Overnight on the houseboat."},
                    {"title": "Houseboat to Cochin & Departure", "description": "After breakfast, check out from the houseboat in Alleppey. Drive back to Cochin, visit Fort Cochin, Chinese Fishing Nets, and Jewish Synagogue (if time permits). Transfer to airport/railway station."}
                ],
                'departures': [
                    {'start_offset': 12, 'end_offset': 16, 'seats': 12, 'status': 'Available'},
                    {'start_offset': 25, 'end_offset': 29, 'seats': 8, 'status': 'Filling Fast'}
                ]
            },
            {
                'title': 'Royal Rajasthan Heritage Tour',
                'dest_name': 'Rajasthan',
                'price': 22000,
                'days': 6,
                'nights': 5,
                'short': 'Explore massive desert forts, royal palaces, and vibrant markets in Jaipur and Udaipur.',
                'desc': '<p>Step back in time to the era of Maharajas. This cultural trip covers the Pink City (Jaipur) and the City of Lakes (Udaipur).</p><p>Walk through the corridors of Amber Fort, click photos at Hawa Mahal, enjoy a scenic boat ride on Lake Pichola, and explore royal museums.</p>',
                'acts': ['Fort Exploring', 'Temple Sightseeing', 'City Sightseeing Tour'],
                'highlights': [
                    "Relish the grandeur of Jaipur's Amber Fort and City Palace",
                    "Boating at Lake Pichola with sunset view of Jag Mandir",
                    "Enchanting puppet shows and traditional Rajasthani dinner",
                    "Explore Chittorgarh Fort - India's largest fort complex"
                ],
                'inclusions': [
                    "3 Nights in Jaipur, 2 Nights in Udaipur in heritage style hotels",
                    "Daily breakfast at hotels",
                    "Full sightseeing and transfers by private AC Sedan",
                    "Elephant or Jeep ride at Amber Fort",
                    "Boat ride on Lake Pichola"
                ],
                'exclusions': [
                    "Monument entrance fees and camera guides",
                    "Lunch and dinner (unless specified)",
                    "Flights or train tickets to Jaipur/Udaipur"
                ],
                'itinerary': [
                    {"title": "Arrival in Jaipur (The Pink City)", "description": "Arrive in Jaipur. Check-in to your hotel. Evening visit to Chokhi Dhani for an immersive Rajasthani cultural experience and dinner. Overnight in Jaipur."},
                    {"title": "Jaipur Forts & Palaces Sightseeing", "description": "After breakfast, explore Amber Fort (jeep/elephant ride included), Hawa Mahal, City Palace, Jantar Mantar, and Jal Mahal. Overnight in Jaipur."},
                    {"title": "Jaipur to Udaipur via Chittorgarh", "description": "Drive to Udaipur. En-route, visit the historic Chittorgarh Fort, listening to tales of Rajput bravery. Arrive in Udaipur, check-in, and relax. Overnight in Udaipur."},
                    {"title": "Udaipur - The Venice of the East", "description": "Sightseeing in Udaipur. Visit City Palace, Jagdish Temple, Saheliyon-ki-Bari, and enjoy a romantic sunset boat ride on Lake Pichola. Overnight in Udaipur."},
                    {"title": "Udaipur Excursion to Kumbhalgarh Fort", "description": "Take a day-trip to Kumbhalgarh Fort, famous for having the second-longest wall in the world. Return to Udaipur in the evening for shopping. Overnight in Udaipur."},
                    {"title": "Departure from Udaipur", "description": "After breakfast, checkout and transfer to Udaipur Airport or Railway Station for your departure."}
                ],
                'departures': [
                    {'start_offset': 15, 'end_offset': 20, 'seats': 10, 'status': 'Available'},
                    {'start_offset': 30, 'end_offset': 35, 'seats': 15, 'status': 'Available'}
                ]
            },
            {
                'title': 'Andaman Island Tropical Paradise',
                'dest_name': 'Andaman Islands',
                'price': 32000,
                'days': 6,
                'nights': 5,
                'short': 'Immerse yourself in tropical beaches and snorkel or dive in crystal-clear waters.',
                'desc': '<p>Escape to the exotic Andaman Islands. Visit Port Blair\'s historic Cellular Jail and watch the light and sound show.</p><p>Cruise to Havelock Island to spend time on the world-famous Radhanagar Beach (Asia\'s best beach) and snorkel/dive among colorful coral reefs at Elephant Beach.</p>',
                'acts': ['Scuba Diving', 'Snorkeling', 'Parasailing'],
                'highlights': [
                    "Watch the Light and Sound Show at Cellular Jail, Port Blair",
                    "Sunbathe at Radhanagar Beach on Havelock Island (Asia's Best Beach)",
                    "Snorkeling at Elephant Beach amongst vibrant coral reefs",
                    "Scenic private cruise ferry between Port Blair and Havelock"
                ],
                'inclusions': [
                    "3 Nights in Port Blair, 2 Nights in Havelock Island in beach resorts",
                    "Daily breakfast",
                    "Private cruise ferry tickets (Makruzz/Green Ocean) for inter-island transfers",
                    "All land transfers by private AC vehicle",
                    "Snorkeling gear and guide at Elephant Beach"
                ],
                'exclusions': [
                    "Flights to Port Blair",
                    "Scuba diving and other optional water activities",
                    "Meals not mentioned in inclusions"
                ],
                'itinerary': [
                    {"title": "Arrival in Port Blair & Cellular Jail", "description": "Arrive in Port Blair. Check-in to your hotel. Visit the historic Cellular Jail followed by the evening Light & Sound Show detailing the freedom struggle. Overnight in Port Blair."},
                    {"title": "Port Blair to Havelock Island", "description": "Take the morning private luxury cruise ferry to Havelock Island. Check-in to your beach resort. Spend the afternoon at leisure. In the evening, visit Radhanagar Beach (Beach No. 7) for a spectacular sunset. Overnight in Havelock."},
                    {"title": "Elephant Beach Excursion & Water Activities", "description": "Head to Elephant Beach by speed boat. Enjoy snorkeling (included) to view corals. Try optional activities like Sea Walk, Parasailing, or Jet Skiing. Return to resort. Overnight in Havelock."},
                    {"title": "Havelock to Port Blair & shopping", "description": "Return to Port Blair via cruise ferry. Check-in to your hotel. Afternoon visit to Sagarika Cottage Industries Emporium for local handicraft shopping. Overnight in Port Blair."},
                    {"title": "Ross Island & North Bay Coral Island", "description": "Full day excursion to Ross Island (the former British administrative capital) and North Bay Island (famous for coral viewing and glass-bottom boat rides). Overnight in Port Blair."},
                    {"title": "Departure from Port Blair", "description": "Checkout after breakfast and transfer to the airport."}
                ],
                'departures': [
                    {'start_offset': 8, 'end_offset': 13, 'seats': 15, 'status': 'Available'},
                    {'start_offset': 22, 'end_offset': 27, 'seats': 12, 'status': 'Available'}
                ]
            },
            {
                'title': 'Himachal Adventure (Manali & Shimla)',
                'dest_name': 'Himachal Pradesh',
                'price': 16500,
                'days': 6,
                'nights': 5,
                'short': 'Breathtaking valleys, snow-capped mountains, and adventure sports in Solang Valley.',
                'desc': '<p>Discover the snowy peaks of Himachal. Explore the colonial charm of Shimla\'s Mall Road, and take in the natural beauty of Manali.</p><p>Take a cable car ride in Solang Valley, try paragliding, and visit the snow fields at Rohtang Pass (subject to permit).</p>',
                'acts': ['Mountain Trekking', 'Cable Car Ride', 'City Sightseeing Tour'],
                'highlights': [
                    "Stroll down Mall Road and shop in Shimla",
                    "Thrilling snow activities at Rohtang Pass",
                    "Paragliding and Zorbing in Solang Valley",
                    "Visit the sacred Hadimba Temple in Manali"
                ],
                'inclusions': [
                    "2 Nights in Shimla, 3 Nights in Manali in scenic valley hotels",
                    "Daily Breakfast and Dinner (MAP Plan)",
                    "Private AC Cab for the entire trip (Delhi/Chandigarh pick-up & drop)",
                    "Local sightseeing of Shimla and Manali"
                ],
                'exclusions': [
                    "Rohtang Pass permit and local electric bus fare",
                    "Adventure sports charges (paragliding, rafting)",
                    "Lunch, tips, laundry"
                ],
                'itinerary': [
                    {"title": "Delhi to Shimla (Gateway to Hills)", "description": "Drive from Delhi/Chandigarh to Shimla. Check-in to hotel, enjoy the pleasant weather, and stroll around Mall Road, Ridge, and Christ Church in the evening. Overnight in Shimla."},
                    {"title": "Kufri Excursion & Shimla Tour", "description": "After breakfast, visit Kufri (famous for snow views and adventure park). Later visit Jakhoo Temple. Overnight in Shimla."},
                    {"title": "Shimla to Manali via Kullu Valley", "description": "Drive to Manali. En-route, visit Kullu valley, enjoy river rafting in Beas River, and visit a shawl factory. Arrive in Manali, check-in. Overnight in Manali."},
                    {"title": "Manali Local Sightseeing", "description": "Explore Manali. Visit Hadimba Temple, Vashisht Hot Water Springs, Tibetan Monastery, and Club House. Overnight in Manali."},
                    {"title": "Solang Valley & Rohtang Pass", "description": "Proceed to Solang Valley for paragliding, quad biking, and cable car rides. If permit is available, proceed to Rohtang Pass to play in the snow. Overnight in Manali."},
                    {"title": "Manali to Delhi Departure", "description": "Check out after breakfast. Drive back to Delhi/Chandigarh for your departure flight or train."}
                ],
                'departures': [
                    {'start_offset': 18, 'end_offset': 23, 'seats': 14, 'status': 'Available'},
                    {'start_offset': 35, 'end_offset': 40, 'seats': 10, 'status': 'Available'}
                ]
            },
            {
                'title': 'Dubai Highlights & Desert Safari',
                'dest_name': 'Dubai',
                'price': 45000,
                'days': 5,
                'nights': 4,
                'short': 'Ascend the Burj Khalifa, cruise Dubai Marina, and bash the dunes on a Desert Safari.',
                'desc': '<p>An ultra-modern escape to the UAE. Visit the Burj Khalifa observation deck on the 124th floor, explore the Dubai Mall, and watch the dancing fountains.</p><p>Enjoy a thrilling 4x4 desert dune bashing ride, followed by camel riding, henna painting, belly dance shows, and a buffet dinner in a bedouin camp.</p>',
                'acts': ['Desert Safari', 'City Sightseeing Tour'],
                'highlights': [
                    "Burj Khalifa Observation Deck (124th Floor) entry ticket",
                    "Thrilling 4x4 Desert Safari with BBQ Buffet Dinner & Tanoura Show",
                    "Romantic Dhow Cruise Dinner at Dubai Marina",
                    "Explore the futuristic Museum of the Future"
                ],
                'inclusions': [
                    "4 Nights stay in a 4-star hotel in Dubai",
                    "Daily breakfast",
                    "Burj Khalifa 124th Floor non-peak hours ticket",
                    "Desert Safari with BBQ Dinner & transfers",
                    "Dubai Marina Dhow Cruise Dinner",
                    "Half-day Dubai city tour by AC coach",
                    "Airport transfers on private basis"
                ],
                'exclusions': [
                    "Visa fee and Travel Insurance",
                    "Tourism Dirham tax (payable directly at hotel)",
                    "Lunch and other personal expenses"
                ],
                'itinerary': [
                    {"title": "Arrival in Dubai & Marina Dhow Cruise", "description": "Arrive in Dubai. Transfer to your hotel. In the evening, head for a luxury Marina Dhow Cruise. Enjoy a buffet dinner, soft drinks, and live music with Dubai Marina views. Overnight in Dubai."},
                    {"title": "City Tour & Burj Khalifa", "description": "After breakfast, enjoy a half-day Dubai City Tour (Gold Souk, Spice Souk, Jumeirah Mosque, Burj Al Arab photo point). In the afternoon, visit the Dubai Mall and go up to the 124th floor of Burj Khalifa. Watch the Fountain Show. Overnight in Dubai."},
                    {"title": "Desert Safari Adventure", "description": "Morning at leisure for shopping. Around 3:00 PM, depart for a thrilling 4x4 Desert Safari. Experience dune bashing, camel riding, henna art, belly dancing, and a BBQ dinner. Overnight in Dubai."},
                    {"title": "Museum of the Future & Miracle Garden", "description": "Visit the iconic Museum of the Future. Later, visit the Dubai Miracle Garden (seasonal) or Global Village. Overnight in Dubai."},
                    {"title": "Departure from Dubai", "description": "Checkout after breakfast. Spend time shopping. Transfer to Dubai International Airport for your departure flight."}
                ],
                'departures': [
                    {'start_offset': 14, 'end_offset': 18, 'seats': 20, 'status': 'Available'},
                    {'start_offset': 28, 'end_offset': 32, 'seats': 12, 'status': 'Filling Fast'}
                ]
            },
            {
                'title': 'Thailand Island Hopper (Bangkok & Phuket)',
                'dest_name': 'Thailand',
                'price': 38000,
                'days': 5,
                'nights': 4,
                'short': 'Discover historic Buddhist temples in Bangkok and pristine tropical beaches in Phuket.',
                'desc': '<p>Get the best of both city life and islands in Thailand. Explore the Grand Palace and Wat Pho (Reclining Buddha temple) in Bangkok.</p><p>Fly to Phuket to relax on Patong beach, and take a premium speedboat cruise to the Phi Phi Islands for snorkeling and swimming in Maya Bay.</p>',
                'acts': ['Snorkeling', 'Temple Sightseeing', 'City Sightseeing Tour'],
                'highlights': [
                    "Speedboat tour to Phi Phi Islands with buffet lunch",
                    "Explore Bangkok's Grand Palace and temple of Reclining Buddha",
                    "Phuket city tour with Karon View Point and Wat Chalong",
                    "Vibrant nightlife at Patong's Bangla Road"
                ],
                'inclusions': [
                    "2 Nights in Phuket (beach resort), 2 Nights in Bangkok (city center hotel)",
                    "Daily breakfast at hotels",
                    "Internal flight ticket from Phuket to Bangkok",
                    "Phi Phi Island tour by speedboat with lunch and snorkeling gear",
                    "Phuket & Bangkok city tours with temple entry fees",
                    "All airport and land transfers"
                ],
                'exclusions': [
                    "International flights to/from Thailand",
                    "Thailand Visa fee (on-arrival or pre-visa)",
                    "National Park entrance fee at Phi Phi (400 THB)"
                ],
                'itinerary': [
                    {"title": "Arrival in Phuket & Bangla Road Nightlife", "description": "Fly into Phuket. Meet our representative and transfer to your resort near Patong Beach. In the evening, explore the vibrant Bangla Road nightlife. Overnight in Phuket."},
                    {"title": "Phi Phi Islands Tour by Speedboat", "description": "After breakfast, board a premium speedboat. Visit Maya Bay (where 'The Beach' was filmed), Pileh Lagoon, Monkey Beach, and Viking Cave. Enjoy buffet lunch and snorkeling. Overnight in Phuket."},
                    {"title": "Phuket Tour & Flight to Bangkok", "description": "Check out. Take a half-day Phuket city tour visiting Karon View Point, Big Buddha, and Wat Chalong. Later, transfer to airport for your flight to Bangkok. Check-in to Bangkok hotel. Overnight in Bangkok."},
                    {"title": "Bangkok Temples & Shopping", "description": "Tour Bangkok's famous temples: Wat Pho (Reclining Buddha) and Wat Traimit (Golden Buddha). Afternoon free for shopping at MBK Center or Siam Paragon. Overnight in Bangkok."},
                    {"title": "Departure from Bangkok", "description": "Checkout after breakfast. Transfer to Suvarnabhumi or Don Mueang Airport for your international return flight."}
                ],
                'departures': [
                    {'start_offset': 11, 'end_offset': 15, 'seats': 18, 'status': 'Available'},
                    {'start_offset': 26, 'end_offset': 30, 'seats': 14, 'status': 'Available'}
                ]
            },
            {
                'title': 'Bali Culture & Beach Escape',
                'dest_name': 'Bali',
                'price': 42000,
                'days': 6,
                'nights': 5,
                'short': 'Explore scenic rice terraces, sacred temples, and beautiful beaches in Ubud and Kuta.',
                'desc': '<p>A perfect blend of spirituality, culture, and nature. Stay in Ubud, the cultural heart of Bali, surrounded by lush rice fields.</p><p>Visit the famous Uluwatu Temple perched on a cliff edge, watch a traditional Kecak fire dance, and take a sunset stroll along Seminyak beach.</p>',
                'acts': ['Snorkeling', 'Temple Sightseeing', 'City Sightseeing Tour'],
                'highlights': [
                    "Spectacular sunset view at Uluwatu Temple with Kecak dance",
                    "Explore Tegalalang Rice Terraces and Ubud Art Market",
                    "Exciting swing adventure over the Ubud forest valley",
                    "Snorkeling at Nusa Penida's Crystal Bay"
                ],
                'inclusions': [
                    "3 Nights in Ubud (boutique resort), 2 Nights in Seminyak (beach pool villa)",
                    "Daily breakfast",
                    "Ubud Swing ticket and forest entry",
                    "Day trip to Nusa Penida island by speed boat with lunch",
                    "Uluwatu Temple tour with Kecak Dance ticket",
                    "Private airport and hotel transfers"
                ],
                'exclusions': [
                    "International flight tickets",
                    "Bali Visa on Arrival fee (500,000 IDR) and tourist tax",
                    "Personal expenses and guide tips"
                ],
                'itinerary': [
                    {"title": "Arrival in Bali & Ubud Transfer", "description": "Arrive at Denpasar Airport. Transfer to your boutique resort in Ubud. Check-in, relax, and explore Ubud center or Art Market. Overnight in Ubud."},
                    {"title": "Ubud Rice Terraces & Jungle Swing", "description": "Visit Tegalalang Rice Terraces, try the famous Bali Swing, and visit the Sacred Monkey Forest Sanctuary. Enjoy dinner overlooking the jungle. Overnight in Ubud."},
                    {"title": "Nusa Penida Island Tour", "description": "Early morning transfer to Sanur harbor. Take a fast boat to Nusa Penida. Visit Kelingking Beach (T-Rex Cliff), Broken Beach, Angel's Billabong, and snorkel at Crystal Bay. Return to Ubud. Overnight in Ubud."},
                    {"title": "Ubud to Seminyak & Uluwatu Temple", "description": "Checkout and drive to your pool villa in Seminyak. In the afternoon, visit Uluwatu Temple on the cliff edge. Watch the Kecak Fire Dance during sunset. Overnight in Seminyak."},
                    {"title": "Water Sports & Beach Club", "description": "Morning water activities at Tanjung Benoa (Banana boat, Jet Ski). Afternoon at leisure to relax at a premium beach club in Seminyak. Overnight in Seminyak."},
                    {"title": "Departure from Bali", "description": "Checkout from your villa. Transfer to Denpasar Airport for your departure flight."}
                ],
                'departures': [
                    {'start_offset': 15, 'end_offset': 20, 'seats': 10, 'status': 'Available'},
                    {'start_offset': 30, 'end_offset': 35, 'seats': 15, 'status': 'Available'}
                ]
            },
            {
                'title': 'Maldives Luxury Overwater Escape',
                'dest_name': 'Maldives',
                'price': 85000,
                'days': 5,
                'nights': 4,
                'short': 'Stay in a premium overwater villa with direct access to private lagoons and marine life.',
                'desc': '<p>Pure, unadulterated luxury. Wake up to panoramic ocean views from your overwater bungalow.</p><p>Snorkel directly from your villa deck, swim with sea turtles, indulge in couples spa treatments, and enjoy candlelight dinners on private sandy shores.</p>',
                'acts': ['Scuba Diving', 'Snorkeling'],
                'highlights': [
                    "Stay in an ultra-luxurious Overwater Villa with direct lagoon access",
                    "Exciting speedboat transfers to/from Male Airport",
                    "Complimentary snorkeling gear to explore house reefs",
                    "Candlelight beachside dinner under the stars"
                ],
                'inclusions': [
                    "4 Nights in a 5-star resort in Maldives (Water Villa)",
                    "Full Board meal plan (Breakfast, Lunch, Dinner)",
                    "Roundtrip airport transfers by Speedboat",
                    "Complimentary non-motorized water sports (kayaking, paddleboarding)"
                ],
                'exclusions': [
                    "International flights to Male",
                    "Premium alcoholic beverages (unless specified)",
                    "Spa treatments and motorized water sports"
                ],
                'itinerary': [
                    {"title": "Arrival & Speedboat to Luxury Resort", "description": "Arrive at Velana International Airport, Male. Meet the resort representative and take a thrilling speedboat ride to your island resort. Check-in to your Overwater Villa. Overnight in Maldives."},
                    {"title": "Water Villa Living & House Reef Snorkeling", "description": "Enjoy breakfast with ocean views. Step directly from your villa deck into the turquoise lagoon. Collect your snorkeling gear and explore the house reef. Overnight in Maldives."},
                    {"title": "Spa & Sunset Cruise", "description": "Pamper yourself with a relaxing spa massage. In the evening, enjoy a sunset dolphin cruise with drinks and snacks. Overnight in Maldives."},
                    {"title": "Beach Dinner & Leisure", "description": "Spend the day kayaking or relaxing on white sand beaches. In the evening, enjoy a private beachside candlelight dinner. Overnight in Maldives."},
                    {"title": "Departure from Maldives", "description": "Checkout. Take the speedboat transfer back to Male Airport for your return flight."}
                ],
                'departures': [
                    {'start_offset': 20, 'end_offset': 24, 'seats': 12, 'status': 'Available'},
                    {'start_offset': 40, 'end_offset': 44, 'seats': 12, 'status': 'Available'}
                ]
            },
            {
                'title': 'Swiss Alps Scenic Explorer',
                'dest_name': 'Switzerland',
                'price': 145000,
                'days': 7,
                'nights': 6,
                'short': 'Explore snow-capped peaks, scenic mountain train journeys, and lakeside Swiss cities.',
                'desc': '<p>A fairytale trip through Switzerland. Take the cogwheel train to Jungfraujoch - the Top of Europe, standing at 3,454 meters.</p><p>Explore the charming lakeside town of Lucerne, take a cable car up Mt. Titlis for panoramic views, and cruise Lake Geneva.</p>',
                'acts': ['Cable Car Ride', 'City Sightseeing Tour'],
                'highlights': [
                    "Jungfraujoch excursion - the Top of Europe cogwheel train",
                    "Cable car ride up Mt. Titlis with ice cave explorer",
                    "Scenic boat cruise on beautiful Lake Lucerne",
                    "Scenic train journey through the Swiss countryside"
                ],
                'inclusions': [
                    "3 Nights in Lucerne, 3 Nights in Interlaken in boutique hotels",
                    "Daily Swiss breakfast",
                    "8-Day Swiss Travel Pass (2nd Class) for unlimited train, bus, and boat travel",
                    "Jungfraujoch excursion ticket with seat reservations",
                    "Mt. Titlis cable car ticket"
                ],
                'exclusions': [
                    "Flights to/from Switzerland",
                    "Lunch and dinner",
                    "Schengen Visa fee and travel insurance"
                ],
                'itinerary': [
                    {"title": "Arrival in Zurich & Transfer to Lucerne", "description": "Arrive at Zurich Airport. Activate your Swiss Travel Pass and board the direct train to Lucerne. Check-in to your hotel. Stroll across the Chapel Bridge. Overnight in Lucerne."},
                    {"title": "Mt. Titlis Excursion", "description": "Travel to Engelberg. Take the Rotair rotating cable car to the summit of Mt. Titlis (3,020m). Explore the glacier cave and walk the Cliff Walk bridge. Return to Lucerne. Overnight in Lucerne."},
                    {"title": "Lake Lucerne Cruise & Interlaken Transfer", "description": "Enjoy a morning boat cruise on Lake Lucerne. In the afternoon, board the scenic Luzern-Interlaken Express train. Check-in to Interlaken hotel. Overnight in Interlaken."},
                    {"title": "Jungfraujoch - Top of Europe", "description": "Board the cogwheel train from Interlaken to Jungfraujoch (3,454m). Visit the Sphinx Observatory and the Ice Palace. Marvel at the Aletsch Glacier. Return to Interlaken. Overnight in Interlaken."},
                    {"title": "Interlaken Lake Cruise & Harder Kulm", "description": "Take a cruise on Lake Thun or Lake Brienz. In the afternoon, ride the funicular to Harder Kulm for sunset views. Overnight in Interlaken."},
                    {"title": "Interlaken to Zurich", "description": "Return to Zurich by train. Spend the afternoon exploring Bahnhofstrasse and the old town. Overnight in Zurich."},
                    {"title": "Departure from Switzerland", "description": "Transfer to Zurich Airport for your return flight."}
                ],
                'departures': [
                    {'start_offset': 30, 'end_offset': 36, 'seats': 10, 'status': 'Available'},
                    {'start_offset': 60, 'end_offset': 66, 'seats': 10, 'status': 'Available'}
                ]
            }
        ]

        pkg_objs = {}
        for p in packages_data:
            slug = generate_slug(p['title'])
            obj = Package.query.filter_by(slug=slug).first()
            dest = dest_objs[p['dest_name']]
            
            if not obj:
                obj = Package(
                    title=p['title'],
                    slug=slug,
                    destination_id=dest.id,
                    price_from=Decimal(p['price']),
                    duration_days=p['days'],
                    duration_nights=p['nights'],
                    short_description=p['short'],
                    description=p['desc'],
                    is_featured=True,
                    is_active=True
                )
                db.session.add(obj)
                db.session.flush()
                print(f"  + Package: {p['title']}")
            else:
                print(f"  - Package already exists: {p['title']}")
            
            # Link activities
            associated_acts = [act_objs[name] for name in p['acts'] if name in act_objs]
            obj.activities = associated_acts

            # Clear old related details
            PackageHighlight.query.filter_by(package_id=obj.id).delete()
            PackageInclusion.query.filter_by(package_id=obj.id).delete()
            PackageExclusion.query.filter_by(package_id=obj.id).delete()
            PackageItinerary.query.filter_by(package_id=obj.id).delete()
            PackageDeparture.query.filter_by(package_id=obj.id).delete()
            db.session.flush()

            # Seed Highlights
            for idx, h in enumerate(p.get('highlights', [])):
                db.session.add(PackageHighlight(package_id=obj.id, highlight=h, display_order=idx))

            # Seed Inclusions
            for idx, inc in enumerate(p.get('inclusions', [])):
                db.session.add(PackageInclusion(package_id=obj.id, inclusion=inc, display_order=idx))

            # Seed Exclusions
            for idx, exc in enumerate(p.get('exclusions', [])):
                db.session.add(PackageExclusion(package_id=obj.id, exclusion=exc, display_order=idx))

            # Seed Itinerary
            for idx, day in enumerate(p.get('itinerary', [])):
                db.session.add(PackageItinerary(
                    package_id=obj.id,
                    day_number=idx + 1,
                    title=day['title'],
                    description=day['description']
                ))

            # Seed Departures
            for dep in p.get('departures', []):
                start = datetime.date.today() + datetime.timedelta(days=dep['start_offset'])
                end = datetime.date.today() + datetime.timedelta(days=dep['end_offset'])
                db.session.add(PackageDeparture(
                    package_id=obj.id,
                    start_date=start,
                    end_date=end,
                    available_seats=dep.get('seats', 15),
                    status=dep.get('status', 'Available')
                ))

            db.session.flush()
            pkg_objs[p['title']] = obj

        # 5. Seed Testimonials/Reviews
        reviews_data = [
            {'name': 'Rohan Sharma', 'package': 'Goa Beach Escape & Water Sports', 'rating': 5, 'review': 'Awesome arrangement! The water sports day in Goa was the highlight of the trip. Highly recommended.'},
            {'name': 'Priyanka Patel', 'package': 'Kerala Backwater Serenade', 'rating': 5, 'review': 'The houseboat cruise in Alleppey was magical. Munnar hills were so refreshing. Thank you for this beautiful memory!'},
            {'name': 'Sanjay Singh', 'package': 'Royal Rajasthan Heritage Tour', 'rating': 5, 'review': 'Perfect cultural itinerary. The tour guide in Jaipur was very knowledgeable and the heritage stays in Udaipur were royal.'},
            {'name': 'Vikram Malhotra', 'package': 'Andaman Island Tropical Paradise', 'rating': 5, 'review': 'Radhanagar beach is stunning. The scuba diving experience at Havelock was very safe and beautiful.'},
            {'name': 'Ananya Sen', 'package': 'Bali Culture & Beach Escape', 'rating': 4, 'review': 'Ubud was so serene. Uluwatu sunset view is simply spectacular. Had a smooth trip altogether.'},
            {'name': 'Deepak Gupta', 'package': 'Maldives Luxury Overwater Escape', 'rating': 5, 'review': 'Absolutely premium! Worth every rupee. The lagoon was so clear and we saw baby sharks right near our villa.'}
        ]

        for r in reviews_data:
            existing = Testimonial.query.filter_by(name=r['name'], package_taken=r['package']).first()
            if not existing:
                pkg = pkg_objs.get(r['package'])
                obj = Testimonial(
                    name=r['name'],
                    package_taken=r['package'],
                    package_id=pkg.id if pkg else None,
                    rating=r['rating'],
                    review=r['review'],
                    image_url=None,
                    is_featured=True,
                    is_active=True
                )
                db.session.add(obj)
                print(f"  + Review: {r['name']} for {r['package']}")

        # 6. Seed General FAQs
        faqs_data = [
            {'question': 'How do I book an international tour package?', 'answer': 'You can submit an inquiry through our tour details page, contact us directly via phone, or drop us a message on WhatsApp. Our travel experts will connect with you, plan the customized itinerary, and share quotes. Once approved, we will assist you with flight booking, visas, hotels, and sightseeing.'},
            {'question': 'Are flight tickets included in the display price?', 'answer': 'No, our display package prices are standard "Land Only" rates. They cover ground hotel stays, transfers, sightseeing entry fees, and activities as listed. Flight ticketing is dynamic, but we can arrange tickets from your departure city as an add-on during booking.'},
            {'question': 'Do you offer customization on itineraries?', 'answer': 'Yes, absolutely! All our holiday packages are 100% customizable. You can add more days, swap hotel categories, select specific sightseeing excursions, or change activities depending on your preferences and budget.'},
            {'question': 'Is travel insurance included in packages?', 'answer': 'We strongly recommend travel insurance for all domestic and international trips. Standard packages do not include insurance, but our sales executives can help you purchase comprehensive travel insurance plans at a minimal cost.'},
            {'question': 'What are your booking and cancellation terms?', 'answer': 'To confirm a booking, a standard deposit (usually 30-50% of the land cost + 100% of flights) is required. The cancellation fee depends on the destination and timeline. Generally, cancellations 30+ days before travel incur minimal administrative fees, whereas cancellations within 15 days of departure are non-refundable.'}
        ]

        max_order = db.session.query(db.func.max(FAQ.display_order)).scalar() or 0
        for i, f in enumerate(faqs_data):
            existing = FAQ.query.filter_by(question=f['question']).first()
            if not existing:
                obj = FAQ(
                    question=f['question'],
                    answer=f['answer'],
                    display_order=max_order + i + 1,
                    is_active=True
                )
                db.session.add(obj)
                print(f"  + FAQ: {f['question'][:50]}...")

        # 7. Seed Enquiries
        enquiries_data = [
            {'name': 'Amit Deshmukh', 'phone': '9819203040', 'email': 'amit.d@example.com', 'message': 'Looking for a Honeymoon trip to Maldives in August. Budget around 1.5 Lakhs.', 'travelers': 2, 'package': 'Maldives Luxury Overwater Escape'},
            {'name': 'Sneha Rao', 'phone': '9122334455', 'email': 'sneha.rao@example.com', 'message': 'Plan a family vacation to Himachal (Shimla & Manali) for 6 adults and 2 children.', 'travelers': 8, 'package': 'Himachal Adventure (Manali & Shimla)'},
            {'name': 'Rajesh Iyer', 'phone': '9820011223', 'email': 'rajesh.iyer@example.com', 'message': 'Need customized Bali package for corporate group tour of 15 members. Require conference facilities.', 'travelers': 15, 'package': 'Bali Culture & Beach Escape'}
        ]

        for e in enquiries_data:
            existing = Inquiry.query.filter_by(name=e['name'], phone=e['phone']).first()
            if not existing:
                pkg = pkg_objs.get(e['package'])
                obj = Inquiry(
                    name=e['name'],
                    phone=e['phone'],
                    email=e['email'],
                    travel_date=datetime.date.today() + datetime.timedelta(days=60),
                    travelers_count=e['travelers'],
                    message=e['message'],
                    package_id=pkg.id if pkg else None,
                    source='package',
                    status='new'
                )
                db.session.add(obj)
                print(f"  + Enquiry: {e['name']} for {e['package']}")

        db.session.commit()
        print("--- Database Seeding Completed Successfully ---")

if __name__ == '__main__':
    seed_all()
