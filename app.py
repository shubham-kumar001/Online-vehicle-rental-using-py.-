from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime, timedelta
import sqlite3
import uuid
import os

app = Flask(__name__)
app.secret_key = 'driveeasy-rental-secret-key-2024'
app.config['DATABASE'] = 'vehicles.db'

# Database functions
def get_db():
    conn = sqlite3.connect('vehicles.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('vehicles.db'):
        conn = sqlite3.connect('vehicles.db')
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mobile TEXT UNIQUE NOT NULL,
                aadhar TEXT UNIQUE NOT NULL,
                driving_license TEXT UNIQUE NOT NULL,
                gender TEXT NOT NULL,
                location TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tickets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ticket_id TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                purchase_date TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                booking_id TEXT UNIQUE NOT NULL,
                vehicle_category TEXT NOT NULL,
                vehicle_name TEXT NOT NULL,
                rental_type TEXT NOT NULL,
                start_date TEXT NOT NULL,
                price REAL NOT NULL,
                payment_method TEXT NOT NULL,
                booking_date TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'confirmed',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

# Initialize database
init_db()

# Vehicle categories with rental prices
VEHICLE_CATEGORIES = {
    'commuter_bikes': {'12_hours': 550, '24_hours': 1000, 'name': 'Commuter Bikes'},
    'adventure_bikes': {'12_hours': 650, '24_hours': 1200, 'name': 'Adventure & Performance Bikes'},
    'royal_enfield_heritage': {'12_hours': 600, '24_hours': 1200, 'name': 'Royal Enfield Heritage & Classic'},
    'royal_enfield_adventure': {'12_hours': 700, '24_hours': 1400, 'name': 'Royal Enfield Adventure & Scrambler'},
    'royal_enfield_roadsters': {'12_hours': 850, '24_hours': 1800, 'name': 'Royal Enfield Roadsters & Sport'},
    'scooters': {'12_hours': 500, '24_hours': 1100, 'name': 'Scooters'},
    'hatchbacks': {'12_hours': 700, '24_hours': 1300, 'name': 'Hatchback Cars'},
    'sedans': {'12_hours': 760, '24_hours': 1600, 'name': 'Sedan Cars'},
    'suvs': {'12_hours': 1000, '24_hours': 2000, 'name': 'SUV Cars'},
    'minibus': {'per_day': 1100, 'name': 'Mini Bus'}
}

# Vehicle lists
VEHICLES = {
    'commuter_bikes': [
        'Hero Splendor Plus Xtec',
        'Hero HF Deluxe',
        'Hero HF 100',
        'Hero Passion Pro Plus',
        'Hero Glamour Xtec',
        'Hero Super Splendor Xtec'
    ],
    'adventure_bikes': [
        'Hero Xtreme 125R',
        'Hero Xtreme 160R 4V',
        'Hero XPulse 200 4V',
        'Hero XPulse 210',
        'Hero Karizma XMR',
        'Hero Mavrick 440',
        'Hero Xtreme 250R'
    ],
    'royal_enfield_heritage': [
        'Classic 350',
        'Bullet 350',
        'Classic 650'
    ],
    'royal_enfield_adventure': [
        'Meteor 350',
        'Super Meteor 650',
        'Himalayan 450',
        'Scram 411'
    ],
    'royal_enfield_roadsters': [
        'Hunter 350',
        'Interceptor 650',
        'Continental GT 650',
        'Guerrilla 450'
    ],
    'scooters': [
        'Hero Pleasure Plus',
        'Hero Maestro Edge 110',
        'Hero Maestro Edge 125',
        'Hero Xoom 125',
        'Hero Xoom 160'
    ],
    'hatchbacks': [
        'Maruti Suzuki Swift',
        'Maruti Suzuki Dzire',
        'Hyundai i10',
        'Hyundai i20',
        'Maruti Wagon R',
        'Maruti Celerio'
    ],
    'sedans': [
        'Honda City',
        'Hyundai Verna',
        'Hyundai Aura',
        'Toyota Etios',
        'Maruti Ciaz'
    ],
    'suvs': [
        'Hyundai Creta',
        'Mahindra Scorpio-N',
        'Mahindra XUV500',
        'Toyota Innova Crysta'
    ],
    'minibus': [
        'Ford Transit',
        'Mercedes-Benz Sprinter',
        'Toyota Coaster',
        'Force Traveller',
        'Tata Winger',
        'Tata Starbus',
        'Mahindra Tourister',
        'Mahindra Cruzio'
    ]
}

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        aadhar = request.form['aadhar']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE mobile = ? AND aadhar = ?', (mobile, aadhar))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            # Check if user has ticket
            cursor.execute('SELECT * FROM tickets WHERE user_id = ?', (user[0],))
            ticket = cursor.fetchone()
            if ticket:
                session['has_ticket'] = True
                session['ticket_id'] = ticket[2]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please register first.', 'error')
            return redirect(url_for('register'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        aadhar = request.form['aadhar']
        driving_license = request.form['driving_license']
        gender = request.form['gender']
        location = request.form['location']
        
        # Check if user already exists
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE mobile = ? OR aadhar = ?', (mobile, aadhar))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('User already exists. Please login.', 'error')
            return redirect(url_for('login'))
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (name, mobile, aadhar, driving_license, gender, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, mobile, aadhar, driving_license, gender, location))
        db.commit()
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE mobile = ?', (mobile,))
        user = cursor.fetchone()
        
        session['user_id'] = user[0]
        session['name'] = name
        return redirect(url_for('ticket'))
    
    return render_template('register.html')

@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Process ticket payment
        payment_method = request.form['payment_method']
        ticket_id = str(uuid.uuid4())[:8].upper()
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO tickets (user_id, ticket_id, amount, payment_method, purchase_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], ticket_id, 20, payment_method, datetime.now()))
        db.commit()
        
        session['has_ticket'] = True
        session['ticket_id'] = ticket_id
        return redirect(url_for('dashboard'))
    
    return render_template('payment.html', amount=20, description="Entry Ticket", ticket=True)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not session.get('has_ticket'):
        return redirect(url_for('ticket'))
    
    return render_template('dashboard.html', name=session.get('name'))

@app.route('/vehicles')
def vehicles():
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    return render_template('vehicles.html', 
                         categories=VEHICLE_CATEGORIES,
                         vehicles=VEHICLES)

@app.route('/book/<category>', methods=['GET', 'POST'])
def book_vehicle(category):
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    if category not in VEHICLE_CATEGORIES:
        return redirect(url_for('vehicles'))
    
    if request.method == 'POST':
        vehicle_name = request.form['vehicle']
        rental_type = request.form.get('rental_type', '12_hours')
        start_date = request.form['start_date']
        
        # Calculate price
        price = 0
        if category == 'minibus':
            days = int(request.form.get('days', 1))
            price = VEHICLE_CATEGORIES[category]['per_day'] * days
            rental_type = f"{days} day(s)"
        else:
            if rental_type == '12_hours':
                price = VEHICLE_CATEGORIES[category]['12_hours']
            else:
                price = VEHICLE_CATEGORIES[category]['24_hours']
        
        # Save booking to session
        session['booking'] = {
            'category': category,
            'vehicle': vehicle_name,
            'rental_type': rental_type,
            'start_date': start_date,
            'price': price
        }
        
        return redirect(url_for('booking_payment'))
    
    return render_template('booking.html',
                         category=category,
                         category_name=VEHICLE_CATEGORIES[category]['name'],
                         vehicles=VEHICLES[category],
                         is_minibus=(category == 'minibus'),
                         categories=VEHICLE_CATEGORIES)

@app.route('/booking-payment', methods=['GET', 'POST'])
def booking_payment():
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    if 'booking' not in session:
        return redirect(url_for('vehicles'))
    
    booking = session['booking']
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        
        # Generate booking ID
        booking_id = str(uuid.uuid4())[:8].upper()
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, booking_id, vehicle_category, vehicle_name, 
                                rental_type, start_date, price, payment_method, booking_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], booking_id, booking['category'], booking['vehicle'],
              booking['rental_type'], booking['start_date'], booking['price'],
              payment_method, datetime.now()))
        db.commit()
        
        session['booking_id'] = booking_id
        return redirect(url_for('confirmation'))
    
    return render_template('payment.html', 
                         amount=booking['price'],
                         description=f"Booking for {booking['vehicle']}",
                         ticket=False)

@app.route('/confirmation')
def confirmation():
    if 'user_id' not in session or 'booking_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM bookings WHERE booking_id = ? AND user_id = ?
    ''', (session['booking_id'], session['user_id']))
    booking = cursor.fetchone()
    
    if not booking:
        return redirect(url_for('dashboard'))
    
    return render_template('confirmation.html', booking=booking)

@app.route('/thankyou')
def thankyou():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Clear booking session
    session.pop('booking', None)
    session.pop('booking_id', None)
    
    return render_template('thankyou.html')

@app.route('/api/user-bookings')
def user_bookings():
    if 'user_id' not in session:
        return jsonify([])
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT booking_id, vehicle_name, rental_type, price, booking_date
        FROM bookings WHERE user_id = ? ORDER BY booking_date DESC
    ''', (session['user_id'],))
    bookings = cursor.fetchall()
    
    result = []
    for booking in bookings:
        result.append({
            'booking_id': booking[0],
            'vehicle_name': booking[1],
            'rental_type': booking[2],
            'price': booking[3],
            'booking_date': booking[4]
        })
    
    return jsonify(result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Process ticket payment
        payment_method = request.form['payment_method']
        ticket_id = str(uuid.uuid4())[:8].upper()
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO tickets (user_id, ticket_id, amount, payment_method, purchase_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], ticket_id, 20, payment_method, datetime.now()))
        db.commit()
        
        session['has_ticket'] = True
        session['ticket_id'] = ticket_id
        return redirect(url_for('dashboard'))
    
    # Get today's date in YYYYMMDD format
    today = datetime.now().strftime('%Y%m%d')
    
    return render_template('payment.html', amount=20, description="Entry Ticket", ticket=True, today=today)
@app.route('/booking-payment', methods=['GET', 'POST'])
def booking_payment():
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    if 'booking' not in session:
        return redirect(url_for('vehicles'))
    
    booking = session['booking']
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        
        # Generate booking ID
        booking_id = str(uuid.uuid4())[:8].upper()
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, booking_id, vehicle_category, vehicle_name, 
                                rental_type, start_date, price, payment_method, booking_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], booking_id, booking['category'], booking['vehicle'],
              booking['rental_type'], booking['start_date'], booking['price'],
              payment_method, datetime.now()))
        db.commit()
        
        session['booking_id'] = booking_id
        return redirect(url_for('confirmation'))
    
    # Get today's date
    today = datetime.now().strftime('%Y%m%d')
    
    return render_template('payment.html', 
                         amount=booking['price'],
                         description=f"Booking for {booking['vehicle']}",
                         ticket=False,
                         today=today)