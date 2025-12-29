// Booking specific JavaScript

// Calculate and update prices dynamically
function updatePriceCalculation() {
    const category = document.getElementById('category').value;
    const rentalType = document.querySelector('input[name="rental_type"]:checked')?.value;
    const days = parseInt(document.getElementById('days')?.value) || 1;
    
    if (!category) return;
    
    // Price mapping (should match server-side)
    const priceMap = {
        'commuter_bikes': { '12_hours': 550, '24_hours': 1000 },
        'adventure_bikes': { '12_hours': 650, '24_hours': 1200 },
        'royal_enfield_heritage': { '12_hours': 600, '24_hours': 1200 },
        'royal_enfield_adventure': { '12_hours': 700, '24_hours': 1400 },
        'royal_enfield_roadsters': { '12_hours': 850, '24_hours': 1800 },
        'scooters': { '12_hours': 500, '24_hours': 1100 },
        'hatchbacks': { '12_hours': 700, '24_hours': 1300 },
        'sedans': { '12_hours': 760, '24_hours': 1600 },
        'suvs': { '12_hours': 1000, '24_hours': 2000 },
        'minibus': { 'per_day': 1100 }
    };
    
    let price = 0;
    let description = '';
    
    if (category === 'minibus') {
        price = priceMap[category].per_day * days;
        description = `Mini Bus Rental for ${days} day(s)`;
    } else if (rentalType && priceMap[category]) {
        price = priceMap[category][rentalType];
        description = `${category.replace('_', ' ').toUpperCase()} - ${rentalType.replace('_', ' ')}`;
    }
    
    // Update UI
    const priceElement = document.getElementById('calculated-price');
    const descriptionElement = document.getElementById('price-description');
    
    if (priceElement) {
        priceElement.textContent = `₹${price}`;
    }
    
    if (descriptionElement) {
        descriptionElement.textContent = description;
    }
    
    // Update hidden input for form submission
    const priceInput = document.getElementById('final-price');
    if (priceInput) {
        priceInput.value = price;
    }
}

// Initialize booking page
function initBookingPage() {
    // Add event listeners for price calculation
    const categorySelect = document.getElementById('category');
    const rentalTypeRadios = document.querySelectorAll('input[name="rental_type"]');
    const daysInput = document.getElementById('days');
    
    if (categorySelect) {
        categorySelect.addEventListener('change', updatePriceCalculation);
    }
    
    if (rentalTypeRadios.length > 0) {
        rentalTypeRadios.forEach(radio => {
            radio.addEventListener('change', updatePriceCalculation);
        });
    }
    
    if (daysInput) {
        daysInput.addEventListener('input', updatePriceCalculation);
    }
    
    // Initialize with current calculation
    updatePriceCalculation();
    
    // Vehicle selection enhancement
    const vehicleSelect = document.getElementById('vehicle');
    if (vehicleSelect) {
        vehicleSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const vehicleInfo = selectedOption.dataset.info;
            
            if (vehicleInfo && document.getElementById('vehicle-info')) {
                document.getElementById('vehicle-info').textContent = vehicleInfo;
            }
        });
    }
}

// Generate PDF receipt
function generateReceipt(bookingData) {
    // This is a basic implementation - in production, use a proper PDF library
    const receiptWindow = window.open('', '_blank');
    receiptWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Booking Receipt - DriveEasy Rentals</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { text-align: center; margin-bottom: 30px; }
                .receipt { border: 2px solid #333; padding: 30px; max-width: 600px; margin: 0 auto; }
                .receipt h2 { color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }
                .detail { display: flex; justify-content: space-between; margin: 10px 0; }
                .total { font-weight: bold; font-size: 1.2em; margin-top: 20px; }
                .footer { margin-top: 30px; text-align: center; font-size: 0.9em; color: #666; }
            </style>
        </head>
        <body>
            <div class="receipt">
                <div class="header">
                    <h1>DriveEasy Rentals</h1>
                    <p>Booking Receipt</p>
                </div>
                <h2>Booking Details</h2>
                <div class="detail">
                    <span>Booking ID:</span>
                    <span>${bookingData.booking_id}</span>
                </div>
                <div class="detail">
                    <span>Vehicle:</span>
                    <span>${bookingData.vehicle_name}</span>
                </div>
                <div class="detail">
                    <span>Rental Type:</span>
                    <span>${bookingData.rental_type}</span>
                </div>
                <div class="detail">
                    <span>Start Date:</span>
                    <span>${bookingData.start_date}</span>
                </div>
                <div class="detail">
                    <span>Booking Date:</span>
                    <span>${bookingData.booking_date}</span>
                </div>
                <div class="detail total">
                    <span>Total Amount:</span>
                    <span>₹${bookingData.price}</span>
                </div>
                <div class="footer">
                    <p>Thank you for choosing DriveEasy Rentals!</p>
                    <p>For support: 1800-123-4567 | support@driveeasyrentals.com</p>
                </div>
            </div>
        </body>
        </html>
    `);
    receiptWindow.document.close();
}

// Initialize when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    initBookingPage();
    
    // Print receipt button
    const printBtn = document.getElementById('print-receipt');
    if (printBtn) {
        printBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get booking data from the page
            const bookingData = {
                booking_id: document.querySelector('[data-booking-id]')?.dataset.bookingId || 'N/A',
                vehicle_name: document.querySelector('[data-vehicle-name]')?.dataset.vehicleName || 'N/A',
                rental_type: document.querySelector('[data-rental-type]')?.dataset.rentalType || 'N/A',
                start_date: document.querySelector('[data-start-date]')?.dataset.startDate || 'N/A',
                booking_date: document.querySelector('[data-booking-date]')?.dataset.bookingDate || 'N/A',
                price: document.querySelector('[data-price]')?.dataset.price || '0'
            };
            
            generateReceipt(bookingData);
        });
    }
});