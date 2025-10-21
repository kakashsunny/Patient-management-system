from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import random
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'
CORS(app)

# Import Supabase - Simple HTTP version
import os
from dotenv import load_dotenv
import requests

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def supabase_insert(table, data):
    """Insert data into Supabase table"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"[SUCCESS] Inserted into {table}: {data.get('email', data.get('name', 'data'))}")
            return response.json()
        else:
            print(f"[ERROR] Insert failed for {table}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Insert error for {table}: {e}")
        return None

def supabase_select(table, filters=None):
    """Select data from Supabase table"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        if filters:
            url += f"?{filters}"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}'
        }
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Select error: {e}")
        return []

def supabase_update(table, data, filter_col, filter_val):
    """Update data in Supabase table"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table}?{filter_col}=eq.{filter_val}"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        response = requests.patch(url, json=data, headers=headers)
        
        # Check for successful status codes (200, 201, 204)
        if response.status_code in [200, 201, 204]:
            try:
                return response.json() if response.text else {'success': True}
            except:
                return {'success': True}
        else:
            print(f"[ERROR] Update failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Update error: {e}")
        return None

# Authentication Decorators
def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_email = decoded.get('email')
            request.user_role = decoded.get('role')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_email = decoded.get('email')
            request.user_role = decoded.get('role')
            
            if request.user_role != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

# Frontend Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/booking')
def booking_page():
    return render_template('booking.html')

@app.route('/dashboard')
def patient_dashboard():
    return render_template('patient-dashboard.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/patients')
def admin_patients():
    return render_template('admin/patients.html')

@app.route('/admin/appointments')
def admin_appointments():
    return render_template('admin/appointments.html')

@app.route('/admin/messages')
def admin_messages_page():
    return render_template('admin/messages.html')

# API Routes
@app.route('/api/config')
def get_config():
    return jsonify({
        'hospital_name': 'City General Hospital',
        'departments': ['General Medicine', 'Pediatrics', 'Cardiology', 'Orthopedics', 'Neurology'],
        'consultation_modes': ['In-person', 'Video Call', 'Phone Call'],
        'currency': 'INR',
        'tax_rate': 18,
        'razorpay_key': 'rzp_test_demo123456789',
        'payment_gateway': 'razorpay'
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Hospital Management System with Supabase',
        'version': '1.0.0'
    })

# Authentication Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        email = data.get('email', '')
        name = data.get('name', email.split('@')[0].title())
        password = data.get('password', '')
        
        if not email.endswith('@gmail.com'):
            return jsonify({'error': 'Please use a Gmail address'}), 400
        
        # Save to Supabase users table
        role = 'admin' if 'admin' in email.lower() else 'patient'
        user_data = {
            'name': name,
            'email': email,
            'password': password,  # In production, hash this!
            'role': role,
            'is_active': True,
            'created_at': datetime.now().isoformat()
        }
        
        result = supabase_insert('users', user_data)
        
        # Generate token
        token = jwt.encode({
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Signup successful! You are now logged in.',
            'token': token,
            'user': {
                'id': result[0]['id'] if result and len(result) > 0 else 'new-user',
                'name': name,
                'email': email,
                'role': role
            }
        }), 201
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        email = data.get('email', '')
        password = data.get('password', '')
        
        # Check for admin credentials
        if email == 'admin@123' and password == '1234':
            token = jwt.encode({
                'email': email,
                'role': 'admin',
                'exp': datetime.utcnow() + timedelta(days=30)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'message': 'Admin login successful',
                'token': token,
                'user': {
                    'id': 'admin-001',
                    'name': 'Administrator',
                    'email': email,
                    'role': 'admin'
                }
            }), 200
        
        if not email.endswith('@gmail.com'):
            return jsonify({'error': 'Please use a Gmail address'}), 401
        
        # Check if user exists in Supabase
        result = supabase_select('users', f'email=eq.{email}')
        
        if result and len(result) > 0:
            user = result[0]
            role = user.get('role', 'patient')
            name = user.get('name', email.split('@')[0].title())
        else:
            # Auto-create user if doesn't exist
            role = 'admin' if 'admin' in email.lower() else 'patient'
            name = email.split('@')[0].title()
            
            user_data = {
                'name': name,
                'email': email,
                'password': password,
                'role': role,
                'is_active': True,
                'created_at': datetime.now().isoformat()
            }
            supabase_insert('users', user_data)
        
        # Save login history
        login_data = {
            'user_email': email,
            'user_role': role,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr,
            'browser': request.headers.get('User-Agent', 'Unknown')[:100],
            'os': 'Windows'
        }
        supabase_insert('login_history', login_data)
        
        # Generate token
        token = jwt.encode({
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.get('id', 'user-123') if result and len(result) > 0 else 'new-user',
                'name': name,
                'email': email,
                'role': role
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = decoded.get('email')
        
        # Get user from Supabase
        result = supabase_select('users', f'email=eq.{email}')
        
        if result and len(result) > 0:
            user = result[0]
            return jsonify({
                'user': {
                    'id': user.get('id', ''),
                    'name': user.get('name', email.split('@')[0].title()),
                    'email': email,
                    'phone': user.get('phone', '+1234567890'),
                    'role': user.get('role', 'patient')
                }
            }), 200
        else:
            # Return basic info if user not in database
            return jsonify({
                'user': {
                    'id': f'user-{hash(email)}',
                    'name': email.split('@')[0].title(),
                    'email': email,
                    'phone': '+1234567890',
                    'role': 'patient'
                }
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/auth/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = decoded.get('email')
        
        data = request.get_json()
        
        # Prepare update data
        update_data = {}
        if data.get('name'):
            update_data['name'] = data.get('name')
        if data.get('phone'):
            update_data['phone'] = data.get('phone')
        if data.get('password'):
            update_data['password'] = data.get('password')
        
        # Update in Supabase
        result = supabase_update('users', update_data, 'email', email)
        
        if result:
            print(f"✅ Profile updated for: {email}")
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            }), 200
        else:
            # If user doesn't exist, create them
            user_data = {
                'email': email,
                'name': data.get('name', email.split('@')[0].title()),
                'phone': data.get('phone', '+1234567890'),
                'role': 'patient',
                'created_at': datetime.now().isoformat()
            }
            if data.get('password'):
                user_data['password'] = data.get('password')
            
            supabase_insert('users', user_data)
            print(f"✅ Profile created for: {email}")
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            }), 200
        
    except Exception as e:
        print(f"❌ Profile update error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Contact Form
@app.route('/api/contact', methods=['POST'])
def contact_form():
    try:
        data = request.get_json()
        
        contact_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'subject': data.get('subject', 'General Inquiry'),
            'message': data.get('message'),
            'status': 'unread',
            'created_at': datetime.now().isoformat()
        }
        
        supabase_insert('contact_messages', contact_data)
        
        return jsonify({
            'message': 'Thank you for contacting us! We will get back to you soon.'
        }), 200
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Appointments
@app.route('/api/appointments/book', methods=['POST'])
@token_required
def book_appointment():
    try:
        data = request.get_json()
        
        # Get user from decorator (already validated)
        user_email = request.user_email
        user_name = user_email.split('@')[0].title()
        
        booking_date = data.get('date')
        booking_time = data.get('time')
        
        # Validate working hours (8:00 AM to 8:00 PM)
        try:
            time_obj = datetime.strptime(booking_time, '%H:%M').time()
            start_time = datetime.strptime('08:00', '%H:%M').time()
            end_time = datetime.strptime('20:00', '%H:%M').time()
            
            if not (start_time <= time_obj <= end_time):
                return jsonify({
                    'error': 'Appointments can only be booked between 8:00 AM and 8:00 PM.'
                }), 400
        except:
            return jsonify({'error': 'Invalid time format'}), 400
        
        # Check if slot is already booked (exact time)
        existing = supabase_select('appointments', f'date=eq.{booking_date}&time=eq.{booking_time}')
        if existing and len(existing) > 0:
            return jsonify({
                'error': 'This time slot is already allotted to another person.'
            }), 400
        
        # Check 20-minute gap rule
        all_appointments = supabase_select('appointments', f'date=eq.{booking_date}')
        if all_appointments:
            booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", '%Y-%m-%d %H:%M')
            
            for apt in all_appointments:
                apt_time = apt.get('time')
                if apt_time:
                    apt_datetime = datetime.strptime(f"{booking_date} {apt_time}", '%Y-%m-%d %H:%M')
                    time_diff = abs((booking_datetime - apt_datetime).total_seconds() / 60)
                    
                    if time_diff < 20:
                        return jsonify({
                            'error': f'Please maintain a 20-minute gap. Slot at {apt_time} is already booked.'
                        }), 400
        
        # Generate IDs
        apt_id = f"APT{random.randint(1000, 9999)}"
        invoice_no = f"INV-2024-{random.randint(1000, 9999)}"
        
        # Calculate fees
        consultation_fee = 500
        tax = consultation_fee * 0.18
        total = consultation_fee + tax
        
        # Save to Supabase
        appointment_data = {
            'appointment_id': apt_id,
            'patient_name': user_name,
            'patient_email': user_email,
            'patient_phone': '+1234567890',
            'department': data.get('department'),
            'date': booking_date,
            'time': booking_time,
            'mode': data.get('mode'),
            'symptoms': data.get('symptoms', ''),
            'status': 'pending',
            'payment_status': 'pending',
            'consultation_fee': consultation_fee,
            'created_at': datetime.now().isoformat()
        }
        
        result = supabase_insert('appointments', appointment_data)
        
        return jsonify({
            'message': 'Appointment created! Please proceed with payment.',
            'appointment': appointment_data,
            'payment': {
                'order_id': f"order_{random.randint(100000, 999999)}",
                'amount': int(total * 100),
                'currency': 'INR',
                'razorpay_key': 'rzp_test_demo123456789'
            }
        }), 201
        
    except Exception as e:
        print(f"Booking error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/verify-payment', methods=['POST'])
def verify_payment():
    try:
        data = request.get_json()
        
        appointment_id = data.get('appointment_id')
        
        # Update appointment status
        update_data = {
            'status': 'confirmed',
            'payment_status': 'completed'
        }
        
        supabase_update('appointments', update_data, 'appointment_id', appointment_id)
        
        return jsonify({
            'success': True,
            'message': 'Payment successful! Your appointment is confirmed.'
        }), 200
        
    except Exception as e:
        print(f"Payment verification error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/my-appointments', methods=['GET'])
@token_required
def my_appointments():
    try:
        # Get user from decorator (already validated)
        user_email = request.user_email
        
        # Get appointments from Supabase (exclude cancelled)
        result = supabase_select('appointments', f'patient_email=eq.{user_email}&payment_status=eq.completed')
        
        # Filter out cancelled appointments
        active_appointments = [apt for apt in result if apt.get('status') != 'cancelled']
        
        return jsonify({
            'appointments': active_appointments
        }), 200
        
    except Exception as e:
        print(f"Get appointments error: {str(e)}")
        return jsonify({'appointments': []}), 200

@app.route('/api/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get single appointment details"""
    try:
        # Get appointment from Supabase
        result = supabase_select('appointments', f'appointment_id=eq.{appointment_id}')
        
        if result and len(result) > 0:
            return jsonify({
                'appointment': result[0]
            }), 200
        else:
            return jsonify({
                'error': 'Appointment not found'
            }), 404
        
    except Exception as e:
        print(f"Get appointment error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments/<appointment_id>', methods=['DELETE'])
@token_required
def delete_appointment(appointment_id):
    """Delete/Cancel appointment"""
    try:
        print(f"\n{'='*60}")
        print(f"[DELETE] Attempting to cancel appointment: {appointment_id}")
        print(f"[DELETE] Supabase URL: {SUPABASE_URL[:30]}..." if SUPABASE_URL else "[DELETE] No Supabase URL!")
        print(f"[DELETE] Supabase KEY: {'Present' if SUPABASE_KEY else 'MISSING!'}")
        
        # Check if Supabase is configured
        if not SUPABASE_URL or not SUPABASE_KEY:
            print(f"[ERROR] Supabase credentials not configured!")
            return jsonify({
                'error': 'Database not configured. Please check .env file.'
            }), 500
        
        # First, get the appointment to check its current payment status
        appointments = supabase_select('appointments', f'appointment_id=eq.{appointment_id}')
        
        print(f"[DELETE] Found {len(appointments) if appointments else 0} appointments")
        
        if not appointments or len(appointments) == 0:
            print(f"[ERROR] Appointment not found: {appointment_id}")
            return jsonify({
                'error': f'Appointment {appointment_id} not found in database'
            }), 404
        
        appointment = appointments[0]
        print(f"[DELETE] Current status: {appointment.get('status')}, Payment: {appointment.get('payment_status')}")
        
        # Update appointment status to cancelled
        update_data = {
            'status': 'cancelled',
            'payment_status': 'refunded' if appointment.get('payment_status') == 'completed' else 'cancelled'
        }
        
        print(f"[DELETE] Updating with data: {update_data}")
        
        # Direct HTTP request to Supabase
        try:
            url = f"{SUPABASE_URL}/rest/v1/appointments?appointment_id=eq.{appointment_id}"
            headers = {
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
            }
            
            print(f"[DELETE] Making PATCH request to: {url}")
            response = requests.patch(url, json=update_data, headers=headers)
            print(f"[DELETE] Response status: {response.status_code}")
            print(f"[DELETE] Response text: {response.text[:200]}")
            
            if response.status_code in [200, 201, 204]:
                print(f"[SUCCESS] Cancelled appointment: {appointment_id}")
                print(f"{'='*60}\n")
                return jsonify({
                    'success': True,
                    'message': 'Appointment cancelled successfully'
                }), 200
            else:
                print(f"[ERROR] Update failed with status {response.status_code}")
                print(f"[ERROR] Response: {response.text}")
                print(f"{'='*60}\n")
                return jsonify({
                    'error': f'Database update failed: {response.status_code}'
                }), 400
                
        except requests.exceptions.RequestException as req_err:
            print(f"[ERROR] Request exception: {str(req_err)}")
            print(f"{'='*60}\n")
            return jsonify({
                'error': f'Network error: {str(req_err)}'
            }), 500
        
    except Exception as e:
        print(f"[ERROR] Delete appointment exception: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Admin Routes
@app.route('/api/login-activity/all', methods=['GET'])
@admin_required
def login_activity():
    try:
        result = supabase_select('login_history', 'order=timestamp.desc&limit=50')
        
        return jsonify({
            'login_activity': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        print(f"Login activity error: {str(e)}")
        return jsonify({'login_activity': []}), 200

@app.route('/api/admin/messages', methods=['GET'])
@admin_required
def admin_messages():
    try:
        result = supabase_select('contact_messages', 'order=created_at.desc')
        
        return jsonify({
            'messages': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        print(f"Get messages error: {str(e)}")
        return jsonify({'messages': []}), 200

@app.route('/api/appointments/all', methods=['GET'])
@admin_required
def all_appointments():
    try:
        result = supabase_select('appointments', 'order=created_at.desc')
        
        # Filter out cancelled appointments - they should not appear in the list
        active_appointments = [apt for apt in result if apt.get('status') != 'cancelled']
        
        return jsonify({
            'appointments': active_appointments,
            'count': len(active_appointments),
            'total_patients': len(set(apt.get('patient_email') for apt in active_appointments if apt.get('patient_email')))
        }), 200
        
    except Exception as e:
        print(f"Get all appointments error: {str(e)}")
        return jsonify({'appointments': []}), 200

@app.route('/api/admin/send-message', methods=['POST'])
@admin_required
def send_admin_message():
    """Admin sends message to patient"""
    try:
        data = request.get_json()
        
        message_data = {
            'recipient_email': data.get('recipient_email'),
            'recipient_name': data.get('recipient_name'),
            'message': data.get('message'),
            'sent_by': 'admin',
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        }
        
        result = supabase_insert('admin_messages', message_data)
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully!'
        }), 200
        
    except Exception as e:
        print(f"Send message error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/dashboard', methods=['GET'])
@admin_required
def dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get all appointments (exclude cancelled)
        all_appointments = supabase_select('appointments')
        active_appointments = [a for a in all_appointments if a.get('status') != 'cancelled']
        
        # Get today's date and current month
        today = datetime.now().date().isoformat()
        current_month = datetime.now().strftime('%Y-%m')
        
        # Calculate stats (exclude cancelled)
        total_appointments = len(active_appointments)
        todays_appointments = len([a for a in active_appointments 
                                   if a.get('date') == today and a.get('payment_status') == 'completed'])
        pending_appointments = len([a for a in active_appointments if a.get('status') == 'pending'])
        completed_appointments = len([a for a in active_appointments if a.get('payment_status') == 'completed'])
        
        # Calculate MONTHLY revenue (only completed appointments in current month, not cancelled or refunded)
        # Revenue includes consultation fee + 18% tax
        TAX_RATE = 0.18
        
        monthly_revenue_base = sum(
            float(a.get('consultation_fee', 0)) 
            for a in active_appointments 
            if a.get('payment_status') == 'completed' 
            and a.get('date', '').startswith(current_month)
        )
        
        # Add tax to revenue
        monthly_revenue = monthly_revenue_base * (1 + TAX_RATE)
        
        # Subtract refunded amounts (with tax) from revenue
        refunded_base = sum(
            float(a.get('consultation_fee', 0))
            for a in all_appointments
            if a.get('payment_status') == 'refunded'
            and a.get('date', '').startswith(current_month)
        )
        
        refunded_amount = refunded_base * (1 + TAX_RATE)
        monthly_revenue = monthly_revenue - refunded_amount
        
        # Round to 2 decimal places
        monthly_revenue = round(monthly_revenue, 2)
        
        # Get unique patients (exclude cancelled)
        unique_patients = len(set(a.get('patient_email') for a in active_appointments if a.get('patient_email')))
        
        print(f"[STATS] Dashboard Stats: Patients={unique_patients}, Today={todays_appointments}, Monthly Revenue={monthly_revenue}")
        
        return jsonify({
            'stats': {
                'total_patients': unique_patients,
                'todays_appointments': todays_appointments,
                'monthly_revenue': monthly_revenue,
                'low_stock_items': 0,  # Not implemented
                'pending_appointments': pending_appointments,
                'total_appointments': total_appointments,
                'total_staff': 0,  # Not implemented
                'completed_appointments': completed_appointments
            }
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Dashboard stats error: {str(e)}")
        return jsonify({'stats': {
            'total_patients': 0,
            'todays_appointments': 0,
            'monthly_revenue': 0,
            'low_stock_items': 0,
            'pending_appointments': 0,
            'total_appointments': 0,
            'total_staff': 0
        }}), 200

@app.route('/api/admin/patients', methods=['GET'])
@admin_required
def get_admin_patients():
    """Get all patients from appointments"""
    try:
        all_appointments = supabase_select('appointments')
        
        # Get unique patients
        patients_dict = {}
        for apt in all_appointments:
            email = apt.get('patient_email')
            if email and email not in patients_dict:
                patients_dict[email] = {
                    'id': apt.get('id', ''),
                    'name': apt.get('patient_name', 'Unknown'),
                    'email': email,
                    'phone': apt.get('patient_phone', '+1234567890'),
                    'total_appointments': 0,
                    'last_visit': apt.get('date', '')
                }
            
            if email:
                patients_dict[email]['total_appointments'] += 1
                # Update last visit if this appointment is more recent
                if apt.get('date', '') > patients_dict[email]['last_visit']:
                    patients_dict[email]['last_visit'] = apt.get('date', '')
        
        patients = list(patients_dict.values())
        
        return jsonify({
            'patients': patients,
            'count': len(patients)
        }), 200
        
    except Exception as e:
        print(f"Get patients error: {str(e)}")
        return jsonify({'patients': []}), 200

# Reviews API
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Get all reviews for homepage"""
    try:
        result = supabase_select('reviews', 'rating=gte.4&order=created_at.desc&limit=6')
        
        # Calculate average rating
        all_reviews = supabase_select('reviews')
        avg_rating = sum(r.get('rating', 0) for r in all_reviews) / len(all_reviews) if all_reviews else 0
        
        return jsonify({
            'reviews': result,
            'count': len(all_reviews),
            'average_rating': round(avg_rating, 1)
        }), 200
        
    except Exception as e:
        print(f"Get reviews error: {str(e)}")
        # Return default reviews if Supabase fails
        return jsonify({
            'reviews': [
                {
                    'id': '1',
                    'name': 'John Doe',
                    'rating': 5,
                    'review': 'Excellent service! The doctors are very professional.',
                    'created_at': '2024-01-15'
                },
                {
                    'id': '2',
                    'name': 'Sarah Johnson',
                    'rating': 5,
                    'review': 'Great hospital with modern facilities.',
                    'created_at': '2024-01-18'
                }
            ],
            'count': 2,
            'average_rating': 5.0
        }), 200

@app.route('/api/reviews', methods=['POST'])
def add_review():
    """Add a new review"""
    try:
        data = request.get_json()
        
        review_data = {
            'name': data.get('name', 'Anonymous'),
            'rating': int(data.get('rating', 5)),
            'review': data.get('review', ''),
            'created_at': datetime.now().isoformat()
        }
        
        result = supabase_insert('reviews', review_data)
        
        return jsonify({
            'message': 'Thank you for your review!',
            'review': result[0] if result else review_data
        }), 201
        
    except Exception as e:
        print(f"Add review error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("[HOSPITAL] City General Hospital - SUPABASE MODE")
    print("="*60)
    print("[STARTING] Hospital Management System...")
    print("[SUCCESS] Connected to Supabase Database")
    print("[SERVER] Running at: http://localhost:5000")
    print("[ADMIN] Dashboard: http://localhost:5000/admin")
    print("[PATIENT] Portal: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
