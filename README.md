# 🏥 Hospital Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A comprehensive, production-ready Hospital Management System with patient portal and admin dashboard**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Demo](#-demo)

</div>

---

## 🌟 Features

### 👥 Patient Portal
- ✅ **User Authentication** - Secure signup/login with JWT
- ✅ **Appointment Booking** - Online booking with payment integration
- ✅ **Patient Dashboard** - View appointments, medical records, invoices
- ✅ **Payment Integration** - Razorpay/Stripe for online payments
- ✅ **Medical Records** - Upload and download medical documents
- ✅ **Notifications** - Email/SMS confirmations

### 🔧 Admin Dashboard
- ✅ **Analytics Dashboard** - Real-time statistics and charts
- ✅ **Patient Management** - Complete patient records and history
- ✅ **Appointment Management** - Approve, reschedule, cancel appointments
- ✅ **Staff Management** - Add/manage doctors, nurses, staff with attendance
- ✅ **Billing System** - Generate invoices with PDF export
- ✅ **Inventory Management** - Track medicines, equipment with low-stock alerts
- ✅ **Reports & Analytics** - Export to Excel, revenue reports
- ✅ **Role-Based Access** - Admin, Receptionist, Accountant, Lab Staff

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Firebase account
- (Optional) Razorpay/Stripe account for payments

### Installation

1. **Clone or download the project**
   ```bash
   cd hospital-management
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Firebase Setup**
   - Create project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Firestore Database
   - Download service account key → Save as `firebase-credentials.json`

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

5. **Create admin user**
   ```bash
   python setup_admin.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the system**
   - Patient Portal: http://localhost:5000
   - Admin Dashboard: http://localhost:5000/admin

📖 **Detailed setup guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)  
⚡ **5-minute setup:** [QUICKSTART.md](QUICKSTART.md)

## 📁 Project Structure

```
hospital-management/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── setup_admin.py             # Admin user setup script
├── routes/                     # API routes
│   ├── auth.py                # Authentication
│   ├── appointments.py        # Appointments
│   ├── admin.py               # Admin operations
│   ├── billing.py             # Billing & invoices
│   ├── inventory.py           # Inventory management
│   └── reports.py             # Reports & analytics
├── utils/                      # Utility functions
│   ├── db.py                  # Firestore connection
│   ├── auth_middleware.py     # JWT authentication
│   ├── payment.py             # Payment gateway
│   ├── notifications.py       # Email/SMS
│   ├── pdf_generator.py       # PDF generation
│   └── validators.py          # Input validation
└── templates/                  # HTML templates
    ├── index.html             # Landing page
    ├── login.html             # Login page
    ├── signup.html            # Signup page
    ├── booking.html           # Appointment booking
    ├── patient-dashboard.html # Patient dashboard
    └── admin/                 # Admin templates
        ├── dashboard.html
        ├── patients.html
        ├── appointments.html
        ├── staff.html
        ├── billing.html
        ├── inventory.html
        ├── reports.html
        └── settings.html
```

## 📸 Screenshots

### Patient Portal
- Modern landing page with hospital information
- Easy appointment booking with payment
- Comprehensive patient dashboard

### Admin Dashboard
- Real-time analytics and statistics
- Complete patient and appointment management
- Billing, inventory, and staff management
- Detailed reports and Excel exports

## 🔌 API Documentation

The system provides 40+ RESTful API endpoints:

- **Authentication:** Signup, Login, Password Reset, Profile Management
- **Appointments:** Book, View, Cancel, Reschedule, Approve
- **Admin:** Patient/Staff/Inventory Management
- **Billing:** Invoice Generation, Payment Processing
- **Reports:** Analytics, Excel Exports

📚 Full API documentation: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 💳 Payment Gateway Setup

**Razorpay (Recommended for India):**
1. Sign up at [Razorpay](https://razorpay.com/)
2. Get test/live API keys
3. Add to `.env`: `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`

**Stripe (International):**
1. Sign up at [Stripe](https://stripe.com/)
2. Get API keys from dashboard
3. Set `PAYMENT_GATEWAY=stripe` in `.env`

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask (Python) |
| Database | Google Firestore |
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Material Design Bootstrap |
| Authentication | JWT (JSON Web Tokens) |
| Payment | Razorpay / Stripe |
| Email | SendGrid |
| SMS | Twilio |
| PDF Generation | ReportLab |
| Charts | Chart.js |

## 📊 Database Schema

Firestore collections:
- `users` - Patient and admin accounts
- `appointments` - Appointment records
- `staff` - Hospital staff information
- `invoices` - Billing records
- `inventory` - Medical supplies
- `medical_records` - Patient medical history
- `attendance` - Staff attendance
- `password_resets` - Reset tokens

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing (Werkzeug)
- ✅ Role-based access control
- ✅ Input validation and sanitization
- ✅ XSS protection
- ✅ Secure payment processing
- ✅ Environment variable configuration

## 🚀 Deployment

The system is production-ready and can be deployed to:
- **Heroku** - Quick deployment with Procfile
- **PythonAnywhere** - Python-specific hosting
- **AWS/GCP/Azure** - Cloud platforms
- **VPS** - DigitalOcean, Linode, etc.

📖 Deployment guide: [SETUP_GUIDE.md](SETUP_GUIDE.md#deployment-to-production)

## 📝 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete feature list and API docs

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - Free for personal and commercial use

## 🙏 Acknowledgments

Built with Flask, Firebase, Material Design Bootstrap, and other amazing open-source technologies.

---

<div align="center">

**Made with ❤️ for better healthcare management**

⭐ Star this repo if you find it helpful!

</div>
