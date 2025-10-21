from flask import Flask, render_template, jsonify
from flask_cors import CORS
from config import Config
from utils.db import get_db

# Import blueprints
from routes.auth import auth_bp
from routes.appointments import appointments_bp
from routes.admin import admin_bp
from routes.billing import billing_bp
from routes.inventory import inventory_bp
from routes.reports import reports_bp
from routes.login_activity import login_activity_bp

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize database
db = get_db()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(billing_bp, url_prefix='/api/billing')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(reports_bp, url_prefix='/api/reports')
app.register_blueprint(login_activity_bp, url_prefix='/api/login-activity')

# ============ Frontend Routes ============

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

@app.route('/admin/staff')
def admin_staff():
    """Admin staff page"""
    return render_template('admin/staff.html')

@app.route('/admin/billing')
def admin_billing():
    """Admin billing page"""
    return render_template('admin/billing.html')

@app.route('/admin/inventory')
def admin_inventory():
    """Admin inventory page"""
    return render_template('admin/inventory.html')

@app.route('/admin/reports')
def admin_reports():
    """Admin reports page"""
    return render_template('admin/reports.html')

@app.route('/admin/settings')
def admin_settings():
    """Admin settings page"""
    return render_template('admin/settings.html')

# ============ API Health Check ============

@app.route('/api/health')
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'Hospital Management System API is running',
        'version': '1.0.0'
    }), 200

@app.route('/api/config')
def get_config():
    """Get public configuration"""
    return jsonify({
        'hospital_name': Config.HOSPITAL_NAME,
        'hospital_email': Config.HOSPITAL_EMAIL,
        'hospital_phone': Config.HOSPITAL_PHONE,
        'hospital_address': Config.HOSPITAL_ADDRESS,
        'departments': Config.DEPARTMENTS,
        'consultation_modes': Config.CONSULTATION_MODES,
        'currency': Config.CURRENCY,
        'payment_gateway': Config.PAYMENT_GATEWAY
    }), 200

# ============ Error Handlers ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print(f"[HOSPITAL] {Config.HOSPITAL_NAME}")
    print("=" * 60)
    print("[STARTING] Hospital Management System...")
    print(f"[SERVER] Running at: http://localhost:5000")
    print(f"[ADMIN] Dashboard: http://localhost:5000/admin")
    print(f"[PATIENT] Portal: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
