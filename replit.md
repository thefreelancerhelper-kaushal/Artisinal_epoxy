# Nova Scotia Epoxy Flooring Website

## Overview
Professional Flask-based website for a Nova Scotia epoxy flooring company. Features a modern design with blurred glass navigation, responsive layouts, and comprehensive service information.

## Recent Changes (November 26, 2025)
- Created complete multi-page Flask application
- Implemented all page templates (Home, About, Services, Gallery, Contact, Quote)
- Added responsive CSS with blurred glass navigation and yellow accent branding
- Integrated contact and quote forms with JSON storage
- Created placeholder images for all website sections
- Configured Flask workflow on port 5000

## Project Architecture

### Backend (Flask)
- **app.py**: Main Flask application with routes for all pages
- **Form handling**: Contact and quote submissions saved to `data/messages.json`
- **Routes**: Home, About, Services, Gallery, Contact, Quote

### Frontend
- **Templates** (Jinja2): 
  - base.html: Sticky navigation with blurred glass effect, footer, WhatsApp button
  - home.html: Hero with yellow sidebar accent, benefits section, featured projects
  - about.html: Company history (est. 2019), Soprema/ALSAN details, values
  - services.html: Metallic epoxy, flake flooring, commercial coatings
  - gallery.html: Filterable image grid with hover effects
  - contact.html: Contact form with business info
  - quote.html: Detailed quote request form

- **Static Assets**:
  - CSS: Responsive design, max-width 1100px, mobile navigation collapse
  - JavaScript: Mobile menu toggle, smooth scrolling, form validation
  - Images: Placeholder images for logo, hero, gallery (15 total)

### Key Features
- Sticky navigation with blurred glass background (backdrop-filter)
- Yellow (#FFD700) brand accent color throughout
- 3D button effects with shadow layering
- Responsive grid layouts for all sections
- Mobile-first navigation with hamburger menu
- Floating WhatsApp chat button (bottom-right)
- Form submissions stored in JSON format
- Smooth scrolling and animations

### Design Specifications
- Max content width: 1100px
- Primary color: #FFD700 (yellow/gold)
- Font stack: Inter (body), Poppins (headings)
- Mobile breakpoints: 768px, 480px
- Section spacing: 4rem (desktop), 3rem (mobile)

## Technology Stack
- Python 3.11
- Flask 3.1.2
- Jinja2 templating
- Vanilla JavaScript
- CSS3 (Grid, Flexbox, backdrop-filter)
- Font Awesome icons
- Google Fonts (Inter, Poppins)

## Running the Application
The Flask server runs on port 5000 (configured in workflow).
Access the site through the Replit webview.

## Form Data Storage
Contact and quote submissions are stored in `data/messages.json` with timestamps and unique IDs.

## Future Enhancements
- Email notifications for form submissions
- Admin dashboard for viewing messages
- Dynamic gallery management
- Testimonials section
- Google Maps integration
