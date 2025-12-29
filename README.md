# 🚗 DriveEasy Vehicle Rental System

A complete online vehicle rental platform built with Python Flask, featuring user authentication, booking management, payment integration, and SQLite database.

## 🌟 Features

- **User Registration & Login** with Aadhar & Driving License verification
- **₹20 Entry Ticket System** for verified access
- **Multi-category Vehicles**: Bikes, Scooters, Cars, SUVs, Mini Buses
- **Real-time Booking System** with date/time selection
- **Secure Payment Gateway** (Credit/Debit, UPI, Net Banking, Cash)
- **Professional UI/UX** with responsive design
- **SQLite Database** for data persistence
- **Booking History** & confirmation system
- **Safety Guidelines** & rental cautions

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with Font Awesome icons
- **Authentication**: Session-based with passwordless login

## 🚀 Quick Start

1. **Install dependencies:**
```bash
pip install Flask
```

2. **Run the application:**
```bash
python app.py
```

3. **Open in browser:**
```
http://localhost:5000
```

## 📁 Project Structure

```
vehicle-rental/
├── app.py              # Main Flask application
├── database.py         # Database setup
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
│   ├── index.html     # Homepage
│   ├── login.html     # Login page
│   ├── register.html  # Registration
│   ├── dashboard.html # User dashboard
│   ├── vehicles.html  # Vehicle listings
│   ├── booking.html   # Booking form
│   ├── payment.html   # Payment page
│   ├── confirmation.html # Booking confirmation
│   └── thankyou.html  # Thank you page
├── static/            # Static assets
│   ├── css/          # Stylesheets
│   └── js/           # JavaScript files
└── vehicles.db       # SQLite database (auto-created)
```

## 📋 Database Schema

- **users**: Stores customer information
- **tickets**: Stores entry ticket purchases
- **bookings**: Stores all rental bookings

## 🎯 User Flow

1. **Registration** → Enter personal & document details
2. **Ticket Purchase** → Pay ₹20 entry fee
3. **Browse Vehicles** → Select from categories
4. **Book Vehicle** → Choose date/time & duration
5. **Make Payment** → Complete booking payment
6. **Confirmation** → Receive booking details & safety instructions

## 💼 Vehicle Categories & Pricing

- **Commuter Bikes**: ₹550/12hrs | ₹1000/24hrs
- **Adventure Bikes**: ₹650/12hrs | ₹1200/24hrs
- **Hatchbacks**: ₹700/12hrs | ₹1300/24hrs
- **SUVs**: ₹1000/12hrs | ₹2000/24hrs
- **Mini Buses**: ₹1100/day

## 🎨 Design Features

- Modern gradient-based UI
- Responsive layouts for all devices
- Interactive form validation
- Smooth animations & transitions
- Professional color scheme
- Intuitive navigation

## 📱 Responsive Design

- Mobile-first approach
- Flexbox & Grid layouts
- Media queries for different screen sizes
- Touch-friendly interfaces

## 🔒 Security Features

- Session management
- Form validation
- SQL injection prevention
- Secure payment simulation
- Input sanitization

## 🎓 For 3rd Semester Project

This project demonstrates:
- Full-stack web development
- Database integration
- User authentication
- Payment system simulation
- Professional UI design
- Complete business logic implementation

## 🤝 Contributing

Feel free to fork and modify for your college projects!

## 📄 License

Educational Purpose - Free to use for academic projects

---
**Developed with ❤️ for 3rd Semester Computer Science Project**
