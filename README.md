# M.A. Tours & Travels

A comprehensive travel agency management system and public website built with Flask, SQLAlchemy, and Tailwind CSS.

## 🏗 System Architecture

This application is built as a **Flask Monolith**. It uses the Factory Pattern to initialize the application and is separated into distinct functional components using **Flask Blueprints**.

### 1. Blueprints
- **`app.auth`**: Handles authentication (login/logout) for the admin portal using `Flask-Login`.
- **`app.admin`**: The core CRM and Content Management System. It relies on server-side rendering (SSR) via Jinja2 templates, styled with Tailwind CSS (v4 via CDN). All routes here are protected and require an authenticated session.
- **`app.public`**: *(Upcoming)* The public-facing travel website built with Vue.js/Tailwind, which will consume data managed by the admin blueprint.

### 2. Tech Stack
- **Backend Framework**: Python / Flask 3.x
- **Database**: PostgreSQL (Hosted on Supabase)
- **ORM**: SQLAlchemy (via `Flask-SQLAlchemy`) & Alembic (via `Flask-Migrate`)
- **Authentication**: `Flask-Login` + `Werkzeug` security (Bcrypt under the hood)
- **Admin Frontend**: HTML5, Jinja2 Templating, Tailwind CSS v4 (CDN), Vanilla JavaScript
- **Environment**: Python `python-dotenv` for configuration management.

---

## 🗄 Database Models (Schema)

The database schema is highly relational, utilizing UUIDs (`String(36)`) for all primary keys to ensure scalability and security.

### Core CRM Models
- **`Admin`**: System administrators (email, hashed password, superadmin flag).
- **`Inquiry`**: A mini-CRM entity tracking customer leads. Linked to specific `Package` records. Features tracking for `status` (new, contacted, interested, booked, closed), `source`, and internal `admin_notes`.

### Travel Models
- **`Destination`**: Broad geographical locations (e.g., Kashmir, Ladakh) featuring images, descriptions, and SEO metadata.
- **`Category`**: High-level categorization tags (e.g., Honeymoon, Adventure).
- **`Package`**: The central model for travel offerings. It has a complex relationship with several sub-models:
  - **`PackageImage`**: Carousel images for the package.
  - **`PackageHighlight`**: Bullet points of key features.
  - **`PackageInclusion` / `PackageExclusion`**: Items included/excluded in the cost.
  - **`PackageItinerary`**: Day-by-day scheduling information.

### Content & Marketing Models
- **`HeroSlide`**: Homepage carousel management (Title, Image URL, CTA buttons).
- **`Announcement`**: Top-bar global announcements (Active toggle, text, CTA link).
- **`Testimonial`**: Customer social proof with star ratings (1-5) and featured toggles.
- **`FAQ`**: Frequently Asked Questions with display-order reordering logic.
- **`GalleryCategory` & `GalleryImage`**: Standalone image gallery management with categorical grouping.
- **`SiteSettings`**: Global KV store for social links, contact emails, and phone numbers.

---

## 🧭 Admin Panel Route Reference

The admin panel does not strictly expose a JSON REST API. Instead, it utilizes standard HTTP methods (GET/POST) to render templates and process form submissions (SSR pattern).

### Dashboard & Auth
- `GET /auth/login` - Admin login page.
- `POST /auth/login` - Authenticate session.
- `GET /auth/logout` - Terminate session.
- `GET /admin/` - Admin Dashboard (Summary stats & counts).

### CRM / Inquiries
- `GET /admin/inquiries?status=<filter>` - List inquiries (Filtered by: new, contacted, interested, booked, closed).
- `GET /admin/inquiries/<id>` - View inquiry detail and history.
- `POST /admin/inquiries/<id>` - Update lead status and admin notes.

### Package & Destination Management
- `GET|POST /admin/destinations` - List and add destinations.
- `GET|POST /admin/destinations/<id>/edit` - Update a destination.
- `GET|POST /admin/packages` - List and add travel packages.
- `GET|POST /admin/packages/<id>/edit` - Comprehensive package builder (General Info).
- `POST /admin/packages/<id>/<sub_item>/add` - Add itinerary, inclusion, highlight, etc.
- `POST /admin/packages/<id>/<sub_item>/<sub_id>/delete` - Remove specific package components.

### Marketing & Homepage Content
- `GET|POST /admin/hero` - List and add hero slides.
- `GET|POST /admin/hero/<id>/edit` - Edit a specific slide.
- `GET|POST /admin/announcement` - Manage the single global announcement bar.
- `GET|POST /admin/testimonials` - List and add testimonials.
- `POST /admin/testimonials/<id>/feature` - Toggle homepage visibility.
- `GET|POST /admin/faqs` - List and add FAQs.
- `POST /admin/faqs/<id>/move/<dir>` - Reorder FAQ display (`up` or `down`).

### Media / Gallery
- `GET|POST /admin/gallery` - List and create gallery categories.
- `GET|POST /admin/gallery/<id>` - View category images and upload new ones.
- `POST /admin/gallery/image/<id>/move/<dir>` - Reorder images inside a category.

---

## 🚀 Running the Project Locally

**1. Create a Virtual Environment:**
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Environment Variables (`.env`):**
Ensure your `.env` is configured with Supabase credentials:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secure_secret_key
DATABASE_URL=postgresql://user:password@aws-0-region.pooler.supabase.com:6543/postgres
```

**4. Run Migrations (If Schema Updates Occur):**
```bash
flask db migrate -m "message"
flask db upgrade
```

**5. Start the Server:**
```bash
python run.py
```

*The application will run at `http://127.0.0.1:5000`.*
