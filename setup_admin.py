"""
Setup script to create the first admin user
Run this script after setting up Firebase credentials
"""

from utils.db import get_db
from werkzeug.security import generate_password_hash
from datetime import datetime
from config import Config

def create_admin():
    print("=" * 60)
    print("[HOSPITAL] Hospital Management System - Admin Setup")
    print("=" * 60)
    
    # Get admin details
    print("\nEnter admin details:")
    name = input("Name: ").strip()
    email = input("Email: ").strip().lower()
    phone = input("Phone: ").strip()
    password = input("Password: ").strip()
    
    if not all([name, email, phone, password]):
        print("[ERROR] All fields are required!")
        return
    
    try:
        db = get_db()
        
        # Check if admin already exists
        existing_admin = db.collection('users').where('email', '==', email).limit(1).get()
        
        if len(list(existing_admin)) > 0:
            print(f"[ERROR] User with email {email} already exists!")
            return
        
        # Create admin user
        admin_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'password': generate_password_hash(password),
            'role': Config.ROLES['ADMIN'],
            'is_active': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        user_ref = db.collection('users').add(admin_data)
        user_id = user_ref[1].id
        
        print("\n[SUCCESS] Admin user created successfully!")
        print(f"[EMAIL] Email: {email}")
        print(f"[ID] User ID: {user_id}")
        print("\nYou can now login to the admin dashboard.")
        
    except Exception as e:
        print(f"[ERROR] Error creating admin: {str(e)}")

if __name__ == '__main__':
    create_admin()
