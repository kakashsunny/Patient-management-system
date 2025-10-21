# Hospital Management System - Complete Setup Guide

## 🎯 Overview

This is a comprehensive Hospital Management System built with Flask (Python) backend and modern HTML/CSS/JavaScript frontend, using Google Firestore as the database.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Google Firebase Account** - [Create Firebase Account](https://firebase.google.com/)

## 🚀 Step-by-Step Setup

### Step 1: Install Python Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all required Python packages including Flask, Firebase Admin SDK, payment gateways, etc.

### Step 2: Firebase Setup

1. **Create a Firebase Project:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add Project"
   - Enter project name (e.g., "hospital-management")
   - Follow the setup wizard

2. **Enable Firestore Database:**
   - In your Firebase project, go to "Firestore Database"
   - Click "Create Database"
   - Choose "Start in production mode"
   - Select a location close to your users

3. **Generate Service Account Key:**
   - Go to Project Settings (gear icon) → Service Accounts
   - Click "Generate New Private Key"
   - Save the downloaded JSON file as `firebase-credentials.json`
   - **Place this file in the project root directory**

### Step 3: Environment Configuration

1. **Create .env file:**
   ```bash
   copy .env.example .env
   ```
   (On Linux/Mac: `cp .env.example .env`)

2. **Edit the .env file** and configure the following:

   ```env
   # Flask Configuration
   SECRET_KEY=your-super-secret-key-change-this-in-production
   
   # Firebase
   FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
   
   # Payment Gateway (Choose one)
   PAYMENT_GATEWAY=razorpay
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_key_secret
   
   # Email Service (SendGrid)
   SENDGRID_API_KEY=your_sendgrid_api_key
   FROM_EMAIL=noreply@yourhospital.com
   
   # SMS Service (Twilio)
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   
   # Hospital Details
   HOSPITAL_NAME=City General Hospital
   HOSPITAL_EMAIL=info@cityhospital.com
   HOSPITAL_PHONE=+1-234-567-8900
   HOSPITAL_ADDRESS=123 Medical Center Drive, City, State 12345
   TAX_RATE=18
   CURRENCY=INR
   ```

### Step 4: Payment Gateway Setup (Razorpay)

1. **Sign up for Razorpay:**
   - Go to [Razorpay](https://razorpay.com/)
   - Create an account
   - Complete KYC verification

2. **Get API Keys:**
   - Go to Settings → API Keys
   - Generate Test/Live keys
   - Copy Key ID and Key Secret to your `.env` file

3. **Alternative: Stripe**
   - If using Stripe, change `PAYMENT_GATEWAY=stripe` in `.env`
   - Get keys from [Stripe Dashboard](https://dashboard.stripe.com/)

### Step 5: Email & SMS Setup (Optional but Recommended)

**SendGrid (Email):**
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key
3. Add to `.env` file

**Twilio (SMS):**
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get Account SID, Auth Token, and Phone Number
3. Add to `.env` file

> **Note:** The system will work without email/SMS, but notifications won't be sent.

### Step 6: Create Admin User

Run the setup script to create your first admin user:

```bash
python setup_admin.py
```

Follow the prompts to enter:
- Admin name
- Email address
- Phone number
- Password

### Step 7: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see:
```
🏥 City General Hospital
🚀 Starting Hospital Management System...
📍 Server running at: http://localhost:5000
📊 Admin Dashboard: http://localhost:5000/admin
👤 Patient Portal: http://localhost:5000
```

### Step 8: Access the Application

**Patient Portal:**
- URL: http://localhost:5000
- Features: Book appointments, view medical records, manage profile

**Admin Dashboard:**
- URL: http://localhost:5000/admin
- Login with the admin credentials you created
- Features: Manage patients, appointments, staff, billing, inventory, reports

## 📱 Features Overview

### User Side (Patient Portal)
✅ Patient registration and login  
✅ Appointment booking with payment  
✅ View appointment history  
✅ Download prescriptions and invoices  
✅ Manage profile  
✅ Contact form  

### Admin Side
✅ Dashboard with analytics  
✅ Patient management  
✅ Appointment management (approve/cancel)  
✅ Staff management  
✅ Billing and invoicing  
✅ Inventory management  
✅ Reports and analytics  
✅ Export to Excel  

## 🔧 Troubleshooting

### Issue: Firebase credentials not found
**Solution:** Ensure `firebase-credentials.json` is in the project root directory.

### Issue: Module not found errors
**Solution:** Run `pip install -r requirements.txt` again.

### Issue: Payment not working
**Solution:** 
- Check if Razorpay/Stripe keys are correct in `.env`
- Ensure you're using test keys for development
- Check browser console for errors

### Issue: Port 5000 already in use
**Solution:** 
- Change port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

## 🌐 Deployment to Production

### Option 1: Deploy to Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku create your-hospital-app
   git push heroku main
   ```

### Option 2: Deploy to PythonAnywhere

1. Upload files to PythonAnywhere
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Reload web app

### Option 3: Deploy to VPS (DigitalOcean, AWS, etc.)

1. Set up server with Python
2. Install Nginx and Gunicorn
3. Configure reverse proxy
4. Set up SSL certificate
5. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 🔒 Security Checklist for Production

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use production Firebase credentials
- [ ] Use live payment gateway keys
- [ ] Enable HTTPS/SSL
- [ ] Set `FLASK_ENV=production`
- [ ] Implement rate limiting
- [ ] Set up proper firewall rules
- [ ] Regular backups of Firestore database
- [ ] Monitor logs for suspicious activity

## 📊 Database Structure

The system uses Firestore with the following collections:

- **users** - Patient and admin user accounts
- **appointments** - All appointment records
- **staff** - Hospital staff information
- **invoices** - Billing and payment records
- **inventory** - Medical supplies and equipment
- **medical_records** - Patient medical history
- **attendance** - Staff attendance tracking
- **password_resets** - Password reset tokens

## 🆘 Support

For issues or questions:
1. Check this guide first
2. Review error messages in terminal
3. Check browser console for frontend errors
4. Verify all API keys and credentials

## 📝 License

MIT License - Feel free to use for personal or commercial projects.

## 🎉 You're All Set!

Your Hospital Management System is now ready to use. Start by:
1. Logging into the admin dashboard
2. Adding staff members
3. Configuring departments
4. Testing the appointment booking flow

Happy managing! 🏥
