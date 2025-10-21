# 🚀 Quick Start Guide - Hospital Management System

Get your Hospital Management System running in **5 minutes**!

## ⚡ Fast Setup (Minimum Configuration)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Firebase Setup (Required)
1. Go to https://console.firebase.google.com/
2. Create a new project
3. Enable Firestore Database
4. Download service account key → Save as `firebase-credentials.json` in project root

### 3. Create .env File
```bash
# Copy example file
copy .env.example .env

# Edit .env and set minimum required:
SECRET_KEY=my-secret-key-12345
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

### 4. Create Admin User
```bash
python setup_admin.py
```
Enter your admin details when prompted.

### 5. Run Application
```bash
python app.py
```

### 6. Access the System
- **Patient Portal:** http://localhost:5000
- **Admin Dashboard:** http://localhost:5000/admin

## 🎯 What Works Out of the Box

✅ Patient registration and login  
✅ Appointment booking  
✅ Admin dashboard  
✅ Patient management  
✅ Appointment management  
✅ Basic billing  
✅ Inventory tracking  
✅ Reports  

## ⚠️ What Needs Additional Setup

❌ **Payment Gateway** - Appointments will be created but payment won't process  
❌ **Email Notifications** - No emails will be sent  
❌ **SMS Notifications** - No SMS will be sent  

## 🔧 Optional: Enable Payments (Razorpay)

1. Sign up at https://razorpay.com/
2. Get Test API Keys
3. Add to `.env`:
   ```
   PAYMENT_GATEWAY=razorpay
   RAZORPAY_KEY_ID=rzp_test_xxxxx
   RAZORPAY_KEY_SECRET=xxxxx
   ```
4. Restart the application

## 📧 Optional: Enable Email Notifications

1. Sign up at https://sendgrid.com/
2. Create API Key
3. Add to `.env`:
   ```
   SENDGRID_API_KEY=SG.xxxxx
   FROM_EMAIL=noreply@yourhospital.com
   ```
4. Restart the application

## 🎓 Test the System

### As a Patient:
1. Go to http://localhost:5000
2. Click "Sign Up"
3. Create an account
4. Book an appointment
5. View your dashboard

### As an Admin:
1. Go to http://localhost:5000/admin
2. Login with admin credentials
3. Explore dashboard
4. Manage appointments
5. View reports

## 📁 Project Structure

```
hospital-management/
├── app.py                  # Main application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── setup_admin.py        # Admin setup script
├── .env                  # Your configuration (create this)
├── firebase-credentials.json  # Firebase key (add this)
├── routes/               # API endpoints
├── utils/                # Helper functions
├── templates/            # HTML templates
└── static/              # CSS, JS, images
```

## 🐛 Common Issues

**Issue:** "Firebase credentials not found"  
**Fix:** Make sure `firebase-credentials.json` is in the project root

**Issue:** "Module not found"  
**Fix:** Run `pip install -r requirements.txt`

**Issue:** "Port 5000 in use"  
**Fix:** Change port in `app.py` or kill the process using port 5000

## 🎉 Next Steps

1. ✅ System is running
2. 📝 Customize hospital details in `.env`
3. 💳 Set up payment gateway (optional)
4. 📧 Configure email/SMS (optional)
5. 👥 Add staff members via admin panel
6. 🏥 Start managing your hospital!

## 📚 Full Documentation

For detailed setup and deployment instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 💡 Tips

- Use **test mode** for payment gateways during development
- Keep your `.env` file secure and never commit it to Git
- Backup your Firebase database regularly
- Test all features before going live

---

**Need Help?** Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions!
