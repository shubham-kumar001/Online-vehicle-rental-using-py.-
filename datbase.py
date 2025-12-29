import sqlite3
import os

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