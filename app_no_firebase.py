from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'
CORS(app)

# In-memory storage for appointments and reviews
appointments_storage = []
reviews_storage = [
    {
        'id': '1',
        'name': 'John Doe',
        'rating': 5,
        'review': 'Excellent service! The doctors are very professional and caring.',
        'date': '2024-01-15'
    },
    {
        'id': '2',
        'name': 'Sarah Johnson',
        'rating': 5,
        'review': 'Great hospital with modern facilities. Highly recommended!',
        'date': '2024-01-18'
    },
    {
        'id': '3',
        'name': 'Michael Chen',
        'rating': 4,
        'review': 'Good experience overall. Staff was helpful and friendly.',
        'date': '2024-01-20'
    }
]

# Frontend Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    """Signup page"""
    return render_template('signup.html')

@app.route('/booking')
def booking_page():
    """Appointment booking page"""
    return render_template('booking.html')

@app.route('/dashboard')
def patient_dashboard():
    """Patient dashboard"""
    return render_template('patient-dashboard.html')

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    return render_template('admin/dashboard.html')

@app.route('/admin/patients')
def admin_patients():
    """Admin patients page"""
    return render_template('admin/patients.html')

@app.route('/admin/appointments')
def admin_appointments():
    """Admin appointments page"""
    return render_template('admin/appointments.html')

# API Routes (Mock data for testing)
@app.route('/api/config')
def get_config():
    """Get public configuration"""
    return jsonify({
        'hospital_name': 'City General Hospital',
        'departments': ['General Medicine', 'Pediatrics', 'Cardiology', 'Orthopedics', 'Neurology'],
        'consultation_modes': ['In-person', 'Video Call', 'Phone Call'],
        'currency': 'INR',
        'tax_rate': 18,
        'razorpay_key': 'rzp_test_demo123456789',  # Demo key for testing
        'payment_gateway': 'razorpay'
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Hospital Management System is running (Test Mode - No Firebase)',
        'version': '1.0.0'
    })

# Authentication Routes (Working without database)
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Patient signup - accepts any Gmail and auto-login"""
    try:
        from flask import request
        import jwt
        from datetime import datetime, timedelta
        data = request.get_json()
        
        email = data.get('email', '')
        name = data.get('name', email.split('@')[0].title())
        
        # Check if email ends with @gmail.com
        if not email.endswith('@gmail.com'):
            return jsonify({'error': 'Please use a Gmail address'}), 400
        
        # Generate token for auto-login
        role = 'admin' if 'admin' in email.lower() else 'patient'
        token = jwt.encode({
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Return token so user is automatically logged in
        return jsonify({
            'message': 'Signup successful! You are now logged in.',
            'token': token,
            'user': {
                'id': f'user-{hash(email)}',
                'name': name,
                'email': email,
                'phone': '+1234567890',
                'role': role,
                'profile_photo': ''
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login - accepts any Gmail with any password"""
    try:
        from flask import request
        import jwt
        from datetime import datetime, timedelta
        
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        
        # Check if email ends with @gmail.com
        if not email.endswith('@gmail.com'):
            return jsonify({'error': 'Please use a Gmail address'}), 401
        
        # Check if password is provided
        if not password:
            return jsonify({'error': 'Password is required'}), 401
        
        # Generate token
        token = jwt.encode({
            'email': email,
            'role': 'admin' if 'admin' in email.lower() else 'patient',
            'exp': datetime.utcnow() + timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Determine role based on email
        role = 'admin' if 'admin' in email.lower() else 'patient'
        name = email.split('@')[0].title()
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': 'test-user-123',
                'name': name,
                'email': email,
                'phone': '+1234567890',
                'role': role,
                'profile_photo': ''
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Get user profile - Returns actual logged in user data"""
    from flask import request
    import jwt
    
    # Get token from header
    auth_header = request.headers.get('Authorization', '')
    
    # Default values
    email = 'guest@gmail.com'
    role = 'patient'
    name = 'Guest'
    
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            email = decoded.get('email', 'guest@gmail.com')
            role = decoded.get('role', 'patient')
            name = email.split('@')[0].title()
            
            print(f"✅ Profile loaded: {name} ({email})")  # Debug log
            
        except Exception as e:
            print(f"❌ Token decode error: {str(e)}")  # Debug log
            email = 'error@gmail.com'
            role = 'patient'
            name = 'Error User'
    else:
        print("⚠️ No Authorization header found")  # Debug log
    
    return jsonify({
        'user': {
            'id': f'user-{hash(email)}',
            'name': name,
            'email': email,
            'phone': '+1234567890',
            'role': role,
            'profile_photo': ''
        }
    }), 200

@app.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    """Book new appointment"""
    try:
        from flask import request
        import random
        from datetime import datetime
        import jwt
        data = request.get_json()
        
        # Get user info from token
        auth_header = request.headers.get('Authorization', '')
        user_email = 'patient@gmail.com'
        user_name = 'Patient'
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                user_email = decoded.get('email', 'patient@gmail.com')
                user_name = user_email.split('@')[0].title()
            except:
                pass
        
        # Generate appointment ID
        apt_id = f"APT{random.randint(1000, 9999)}"
        
        # Calculate fees
        consultation_fee = 500
        tax = consultation_fee * 0.18
        total = consultation_fee + tax
        
        # Generate mock payment order
        order_id = f"order_{random.randint(100000, 999999)}"
        invoice_no = f"INV-2024-{random.randint(1000, 9999)}"
        
        # Create appointment object with actual user data
        appointment = {
            'appointment_id': apt_id,
            'patient_name': user_name,
            'patient_email': user_email,
            'patient_phone': '+1234567890',
            'department': data.get('department'),
            'date': data.get('date'),
            'time': data.get('time'),
            'mode': data.get('mode'),
            'symptoms': data.get('symptoms', ''),
            'consultation_fee': consultation_fee,
            'tax': tax,
            'total': total,
            'status': 'pending',
            'payment_status': 'pending',
            'invoice_no': invoice_no,
            'order_id': order_id,
            'created_at': datetime.now().isoformat()
        }
        
        # Store in memory
        appointments_storage.append(appointment)
        
        return jsonify({
            'message': 'Appointment created! Please proceed with payment.',
            'appointment': appointment,
            'payment': {
                'order_id': order_id,
                'amount': int(total * 100),  # Convert to paise
                'currency': 'INR',
                'razorpay_key': 'rzp_test_demo123456789'
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/verify-payment', methods=['POST'])
def verify_payment():
    """Verify payment (mock) - Always succeeds in test mode"""
    try:
        from flask import request
        data = request.get_json()
        
        appointment_id = data.get('appointment_id')
        
        # Find and update appointment in storage
        for apt in appointments_storage:
            if apt['appointment_id'] == appointment_id:
                apt['status'] = 'confirmed'
                apt['payment_status'] = 'completed'
                apt['doctor'] = 'Dr. Smith'  # Assign doctor
                
                return jsonify({
                    'success': True,
                    'message': 'Payment successful! Your appointment is confirmed.',
                    'payment_status': 'completed',
                    'invoice_id': apt['invoice_no'],
                    'appointment': apt
                }), 200
        
        # If not found in storage, return success anyway
        return jsonify({
            'success': True,
            'message': 'Payment successful! Your appointment is confirmed.',
            'payment_status': 'completed',
            'invoice_id': f"INV-2024-{appointment_id}",
            'appointment': {
                'appointment_id': appointment_id,
                'status': 'confirmed',
                'payment_status': 'completed'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/my-appointments', methods=['GET'])
def my_appointments():
    """Get user appointments - Returns stored appointments"""
    # Return only confirmed/paid appointments
    confirmed_appointments = [apt for apt in appointments_storage if apt.get('payment_status') == 'completed']
    
    # Sort by date (newest first)
    confirmed_appointments.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return jsonify({
        'appointments': confirmed_appointments
    }), 200

@app.route('/api/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get single appointment details - Returns actual booked appointment"""
    # Find appointment in storage
    for apt in appointments_storage:
        if apt['appointment_id'] == appointment_id:
            return jsonify({
                'appointment': apt
            }), 200
    
    # If not found, return error
    return jsonify({
        'error': 'Appointment not found'
    }), 404

# Admin Routes
@app.route('/api/admin/patients', methods=['GET'])
def get_admin_patients():
    """Get all patients (Admin only)"""
    return jsonify({
        'patients': [
            {
                'id': '1',
                'name': 'John Doe',
                'email': 'john@gmail.com',
                'phone': '+1234567890',
                'created_at': '2024-01-15T10:30:00'
            },
            {
                'id': '2',
                'name': 'Jane Smith',
                'email': 'jane@gmail.com',
                'phone': '+1234567891',
                'created_at': '2024-01-16T11:00:00'
            }
        ],
        'count': 2
    }), 200

@app.route('/api/appointments/all', methods=['GET'])
def all_appointments():
    """Get all appointments (Admin only)"""
    return jsonify({
        'appointments': [
            {
                'appointment_id': 'APT001',
                'patient_name': 'John Doe',
                'patient_email': 'john@gmail.com',
                'patient_phone': '+1234567890',
                'department': 'General Medicine',
                'date': '2024-01-25',
                'time': '10:00 AM',
                'mode': 'In-person',
                'status': 'approved',
                'payment_status': 'completed',
                'consultation_fee': 500
            },
            {
                'appointment_id': 'APT002',
                'patient_name': 'Jane Smith',
                'patient_email': 'jane@gmail.com',
                'patient_phone': '+1234567891',
                'department': 'Cardiology',
                'date': '2024-01-28',
                'time': '2:00 PM',
                'mode': 'Video Call',
                'status': 'pending',
                'payment_status': 'pending',
                'consultation_fee': 800
            }
        ],
        'count': 2
    }), 200

@app.route('/api/billing/invoices', methods=['GET'])
def get_invoices():
    """Get all invoices"""
    return jsonify({
        'invoices': [
            {
                'id': 'INV001',
                'invoice_no': 'INV-2024-001',
                'patient_name': 'John Doe',
                'date': '2024-01-25',
                'total': 590,
                'payment_status': 'completed',
                'items': [
                    {'description': 'Consultation Fee', 'amount': 500},
                    {'description': 'Tax (18%)', 'amount': 90}
                ]
            },
            {
                'id': 'INV002',
                'invoice_no': 'INV-2024-002',
                'patient_name': 'Jane Smith',
                'date': '2024-01-28',
                'total': 944,
                'payment_status': 'pending',
                'items': [
                    {'description': 'Consultation Fee', 'amount': 800},
                    {'description': 'Tax (18%)', 'amount': 144}
                ]
            }
        ],
        'count': 2
    }), 200

@app.route('/api/billing/summary', methods=['GET'])
def billing_summary():
    """Get billing summary"""
    return jsonify({
        'summary': {
            'total_revenue': 1534,
            'paid_amount': 590,
            'pending_amount': 944,
            'total_invoices': 2
        }
    }), 200

@app.route('/api/billing/invoices/<invoice_id>/download', methods=['GET'])
def download_invoice(invoice_id):
    """Download invoice as HTML (mock)"""
    from datetime import datetime
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice - {invoice_id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .invoice-details {{ margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #2196F3; color: white; }}
            .total {{ font-size: 18px; font-weight: bold; text-align: right; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏥 City General Hospital</h1>
            <p>123 Medical Center Drive, City, State 12345</p>
            <p>Phone: +1-234-567-8900 | Email: info@cityhospital.com</p>
        </div>
        
        <h2>INVOICE</h2>
        
        <div class="invoice-details">
            <p><strong>Invoice No:</strong> {invoice_id}</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            <p><strong>Patient Name:</strong> Test Patient</p>
            <p><strong>Appointment ID:</strong> APT001</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Description</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Consultation Fee - General Medicine</td>
                    <td>₹500.00</td>
                </tr>
                <tr>
                    <td>Tax (18%)</td>
                    <td>₹90.00</td>
                </tr>
            </tbody>
        </table>
        
        <p class="total">Total Amount: ₹590.00</p>
        <p class="total">Payment Status: <span style="color: green;">PAID</span></p>
        
        <div style="margin-top: 40px; text-align: center; color: #666;">
            <p>Thank you for choosing City General Hospital!</p>
            <p>For any queries, please contact us at info@cityhospital.com</p>
        </div>
        
        <script>
            // Auto print on load
            window.onload = function() {{ window.print(); }}
        </script>
    </body>
    </html>
    """
    
    from flask import Response
    return Response(html, mimetype='text/html')

@app.route('/api/login-activity/all', methods=['GET'])
def login_activity():
    """Get all login activity (Admin only)"""
    return jsonify({
        'login_activity': [
            {
                'user_email': 'john@gmail.com',
                'user_role': 'patient',
                'status': 'success',
                'timestamp': '2024-01-20T14:30:00',
                'ip_address': '192.168.1.100',
                'browser': 'Chrome',
                'os': 'Windows'
            },
            {
                'user_email': 'admin@gmail.com',
                'user_role': 'admin',
                'status': 'success',
                'timestamp': '2024-01-20T15:00:00',
                'ip_address': '192.168.1.101',
                'browser': 'Firefox',
                'os': 'Windows'
            },
            {
                'user_email': 'jane@gmail.com',
                'user_role': 'patient',
                'status': 'failed',
                'timestamp': '2024-01-20T15:30:00',
                'ip_address': '192.168.1.102',
                'browser': 'Chrome',
                'os': 'macOS'
            }
        ],
        'count': 3
    }), 200

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """Handle contact form submissions"""
    try:
        from flask import request
        data = request.get_json()
        
        return jsonify({
            'message': 'Thank you for contacting us! We will get back to you soon.',
            'data': {
                'name': data.get('name'),
                'email': data.get('email'),
                'subject': data.get('subject'),
                'message': data.get('message'),
                'timestamp': '2024-01-20T16:00:00'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/messages', methods=['GET'])
def admin_messages():
    """Get all contact messages (Admin only)"""
    return jsonify({
        'messages': [
            {
                'id': '1',
                'name': 'John Doe',
                'email': 'john@gmail.com',
                'subject': 'Appointment Query',
                'message': 'I would like to know about appointment availability.',
                'timestamp': '2024-01-20T10:00:00',
                'status': 'unread'
            },
            {
                'id': '2',
                'name': 'Jane Smith',
                'email': 'jane@gmail.com',
                'subject': 'Billing Question',
                'message': 'Can I get a copy of my invoice?',
                'timestamp': '2024-01-20T11:30:00',
                'status': 'read'
            }
        ],
        'count': 2
    }), 200

@app.route('/api/reports/dashboard', methods=['GET'])
def dashboard_stats():
    """Get dashboard statistics"""
    return jsonify({
        'stats': {
            'total_patients': 25,
            'todays_appointments': 8,
            'monthly_revenue': 45000,
            'low_stock_items': 3,
            'pending_appointments': 5,
            'total_appointments': 50,
            'total_staff': 12,
            'total_revenue': 125000
        }
    }), 200

# Reviews API
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Get all reviews for homepage"""
    # Return only 5-star and 4-star reviews for homepage
    top_reviews = [r for r in reviews_storage if r['rating'] >= 4]
    return jsonify({
        'reviews': top_reviews[:6],  # Show top 6 reviews
        'count': len(reviews_storage),
        'average_rating': sum(r['rating'] for r in reviews_storage) / len(reviews_storage) if reviews_storage else 0
    }), 200

@app.route('/api/reviews', methods=['POST'])
def add_review():
    """Add a new review"""
    try:
        from flask import request
        from datetime import datetime
        import random
        data = request.get_json()
        
        review = {
            'id': str(random.randint(1000, 9999)),
            'name': data.get('name', 'Anonymous'),
            'rating': int(data.get('rating', 5)),
            'review': data.get('review', ''),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        reviews_storage.append(review)
        
        return jsonify({
            'message': 'Thank you for your review!',
            'review': review
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 City General Hospital - TEST MODE")
    print("="*60)
    print("🚀 Starting Hospital Management System...")
    print("⚠️  Running WITHOUT Firebase (Frontend Only)")
    print("📍 Server running at: http://localhost:5000")
    print("📊 Admin Dashboard: http://localhost:5000/admin")
    print("👤 Patient Portal: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
