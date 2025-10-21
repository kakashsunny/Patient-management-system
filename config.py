import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
    
    # Payment Gateway Configuration
    PAYMENT_GATEWAY = os.getenv('PAYMENT_GATEWAY', 'razorpay')
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    
    # Email Configuration
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@hospital.com')
    
    # SMS Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    # Hospital Configuration
    HOSPITAL_NAME = os.getenv('HOSPITAL_NAME', 'City General Hospital')
    HOSPITAL_EMAIL = os.getenv('HOSPITAL_EMAIL', 'info@hospital.com')
    HOSPITAL_PHONE = os.getenv('HOSPITAL_PHONE', '+1-234-567-8900')
    HOSPITAL_ADDRESS = os.getenv('HOSPITAL_ADDRESS', '123 Medical Center Drive')
    TAX_RATE = float(os.getenv('TAX_RATE', '18'))
    CURRENCY = os.getenv('CURRENCY', 'INR')
    
    # Frontend URL
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5000')
    
    # Departments
    DEPARTMENTS = [
        'General Medicine',
        'Pediatrics',
        'Cardiology',
        'Orthopedics',
        'Neurology',
        'Dermatology',
        'ENT',
        'Ophthalmology',
        'Gynecology',
        'Psychiatry'
    ]
    
    # Consultation Modes
    CONSULTATION_MODES = ['In-person', 'Online']
    
    # User Roles
    ROLES = {
        'PATIENT': 'patient',
        'ADMIN': 'admin',
        'RECEPTIONIST': 'receptionist',
        'ACCOUNTANT': 'accountant',
        'LAB_STAFF': 'lab_staff',
        'DOCTOR': 'doctor'
    }
    
    # Appointment Status
    APPOINTMENT_STATUS = {
        'PENDING': 'pending',
        'APPROVED': 'approved',
        'COMPLETED': 'completed',
        'CANCELLED': 'cancelled'
    }
    
    # Payment Status
    PAYMENT_STATUS = {
        'PENDING': 'pending',
        'COMPLETED': 'completed',
        'FAILED': 'failed',
        'REFUNDED': 'refunded'
    }
