// Main JavaScript for Vehicle Rental System

// Load user bookings
function loadBookings() {
    const bookingsSection = document.getElementById('bookings-section');
    const bookingsList = document.getElementById('bookings-list');
    
    fetch('/api/user-bookings')
        .then(response => response.json())
        .then(bookings => {
            if (bookings.length > 0) {
                bookingsList.innerHTML = '';
                bookings.forEach(booking => {
                    const bookingElement = document.createElement('div');
                    bookingElement.className = 'booking-item';
                    bookingElement.innerHTML = `
                        <div class="booking-info">
                            <h4>${booking.vehicle_name}</h4>
                            <p>Booking ID: ${booking.booking_id}</p>
                            <p>${booking.rental_type} • ${new Date(booking.booking_date).toLocaleDateString()}</p>
                        </div>
                        <div class="booking-price">₹${booking.price}</div>
                    `;
                    bookingsList.appendChild(bookingElement);
                });
                bookingsSection.style.display = 'block';
            } else {
                bookingsList.innerHTML = '<p class="no-bookings">No bookings yet. Start by renting a vehicle!</p>';
                bookingsSection.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error loading bookings:', error);
            bookingsList.innerHTML = '<p class="error">Error loading bookings. Please try again.</p>';
            bookingsSection.style.display = 'block';
        });
}

// Form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = '#dc3545';
        } else {
            input.style.borderColor = '#e0e0e0';
        }
    });
    
    return isValid;
}

// Mobile menu toggle (for responsive design)
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('show');
    }
}

// Initialize date pickers
function initDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"], input[type="datetime-local"]');
    dateInputs.forEach(input => {
        if (!input.min) {
            const now = new Date();
            const minDate = now.toISOString().slice(0, 16);
            input.min = minDate;
        }
    });
}

// Format currency
function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN');
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add notification styles dynamically
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateX(100%);
        transition: transform 0.3s;
        z-index: 10000;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 5px solid #28a745;
    }
    
    .notification-error {
        border-left: 5px solid #dc3545;
    }
    
    .notification-info {
        border-left: 5px solid #17a2b8;
    }
    
    .notification i {
        font-size: 1.2rem;
    }
    
    .notification-success i {
        color: #28a745;
    }
    
    .notification-error i {
        color: #dc3545;
    }
    
    .notification-info i {
        color: #17a2b8;
    }
`;

document.head.appendChild(notificationStyles);

// Initialize when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    initDatePickers();
    
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Please fill all required fields', 'error');
            }
        });
    });
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Auto-hide notifications after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 300);
        }, 3000);
    });
});