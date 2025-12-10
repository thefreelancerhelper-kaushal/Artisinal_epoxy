"""
Flask application for Nova Scotia Epoxy Flooring Company
Features: Multi-page website with contact/quote forms, gallery, and responsive design
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from functools import wraps
import json
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

# Admin credentials
ADMIN_USERNAME = 'admin_sehaj'
ADMIN_PASSWORD = 'artisian'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize messages.json if it doesn't exist
MESSAGES_FILE = 'data/messages.json'
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)


def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number (basic validation)"""
    if not phone:
        return True  # Phone is optional in some forms
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10


def validate_contact_form(data):
    """Validate contact form data"""
    errors = []
    
    if not data.get('name', '').strip():
        errors.append('Name is required')
    
    if not data.get('email', '').strip():
        errors.append('Email is required')
    elif not validate_email(data['email']):
        errors.append('Invalid email format')
    
    if not data.get('message', '').strip():
        errors.append('Message is required')
    
    if data.get('phone') and not validate_phone(data['phone']):
        errors.append('Invalid phone number format')
    
    return errors


def validate_quote_form(data):
    """Validate quote form data"""
    errors = []
    
    if not data.get('name', '').strip():
        errors.append('Name is required')
    
    if not data.get('email', '').strip():
        errors.append('Email is required')
    elif not validate_email(data['email']):
        errors.append('Invalid email format')
    
    if not data.get('phone', '').strip():
        errors.append('Phone is required')
    elif not validate_phone(data['phone']):
        errors.append('Invalid phone number format')
    
    if not data.get('address', '').strip():
        errors.append('Address is required')
    
    if not data.get('project_type', '').strip():
        errors.append('Project type is required')
    
    if not data.get('flooring_type', '').strip():
        errors.append('Flooring type is required')
    
    # Validate square footage if provided
    sqft = data.get('square_footage', '').strip()
    if sqft:
        try:
            # Remove whitespace and try to parse as float
            sqft_value = float(sqft.replace(',', '').replace(' ', ''))
            if sqft_value <= 0:
                errors.append('Square footage must be a positive number')
        except (ValueError, TypeError):
            errors.append('Square footage must be a valid number')
    
    return errors


def save_message(message_data):
    """Save form submission to messages.json"""
    try:
        # Read existing messages
        with open(MESSAGES_FILE, 'r') as f:
            messages = json.load(f)
        
        # Add timestamp and ID
        message_data['timestamp'] = datetime.now().isoformat()
        message_data['id'] = len(messages) + 1
        
        # Append new message
        messages.append(message_data)
        
        # Save back to file
        with open(MESSAGES_FILE, 'w') as f:
            json.dump(messages, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving message: {e}")
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error=True)
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout from admin panel"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
def home():
    """Home page with hero banner and benefits sections"""
    return render_template('home.html')


@app.route('/about')
def about():
    """About page with company history and values"""
    return render_template('about.html')


@app.route('/services')
def services():
    """Services page listing all flooring options"""
    return render_template('services.html')


@app.route('/gallery')
def gallery():
    """Gallery page with project photos"""
    return render_template('gallery.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form submission"""
    if request.method == 'POST':
        # Collect form data
        form_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'message': request.form.get('message', '')
        }
        
        # Server-side validation
        errors = validate_contact_form(form_data)
        if errors:
            print(f"Contact form validation errors: {errors}")
            return redirect(url_for('contact_error'))
        
        # Save valid data
        message_data = {
            'type': 'contact',
            **form_data
        }
        
        if save_message(message_data):
            return redirect(url_for('contact_success'))
        else:
            return redirect(url_for('contact_error'))
    
    return render_template('contact.html')


@app.route('/contact/success')
def contact_success():
    """Contact form success page"""
    return render_template('contact.html', success=True)


@app.route('/contact/error')
def contact_error():
    """Contact form error page"""
    return render_template('contact.html', error=True)


@app.route('/quote', methods=['GET', 'POST'])
def quote():
    """Quote request page with detailed form"""
    if request.method == 'POST':
        # Collect form data
        form_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'project_type': request.form.get('project_type', ''),
            'flooring_type': request.form.get('flooring_type', ''),
            'square_footage': request.form.get('square_footage', ''),
            'timeline': request.form.get('timeline', ''),
            'details': request.form.get('details', '')
        }
        
        # Server-side validation
        errors = validate_quote_form(form_data)
        if errors:
            print(f"Quote form validation errors: {errors}")
            return redirect(url_for('quote_error'))
        
        # Save valid data
        message_data = {
            'type': 'quote',
            **form_data
        }
        
        if save_message(message_data):
            return redirect(url_for('quote_success'))
        else:
            return redirect(url_for('quote_error'))
    
    return render_template('quote.html')


@app.route('/quote/success')
def quote_success():
    """Quote form success page"""
    return render_template('quote.html', success=True)


@app.route('/quote/error')
def quote_error():
    """Quote form error page"""
    return render_template('quote.html', error=True)


@app.route('/admin')
@login_required
def admin():
    """Admin panel to view all messages and quotes"""
    try:
        with open(MESSAGES_FILE, 'r') as f:
            messages = json.load(f)
    except:
        messages = []
    
    # Separate contacts and quotes
    contacts = [m for m in messages if m.get('type') == 'contact']
    quotes = [m for m in messages if m.get('type') == 'quote']
    
    return render_template('admin.html', contacts=contacts, quotes=quotes, total_messages=len(messages))


if __name__ == '__main__':
    # Bind to 0.0.0.0:5000 for Replit environment
    app.run(host='0.0.0.0', port=5000, debug=True)
