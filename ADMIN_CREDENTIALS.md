# 🔐 Admin Login Credentials

## Admin Access

**Email:** `admin@123`  
**Password:** `1234`

---

## How to Login as Admin

### Step 1: Go to Login Page
http://localhost:5000/login

### Step 2: Select "Admin" Option
- Click on the **Admin** button (not Patient)

### Step 3: Enter Credentials
- **Email:** admin@123
- **Password:** 1234

### Step 4: Click Login
- You'll be redirected to: http://localhost:5000/admin

---

## Admin Features

### 📊 Dashboard
- View total appointments
- View total patients
- View statistics

### 👥 View Appointments
- See all patient appointments
- View patient details:
  - Name
  - Email
  - Phone number
  - Department
  - Date & Time
  - Status

### 💬 Send Messages to Patients
- Select patient from appointments list
- Send custom messages
- Track message history

### 📧 View Contact Messages
- See all "Get In Touch" form submissions
- View patient inquiries

### 📈 Login Activity
- Track all login attempts
- See user roles
- View timestamps

---

## Patient Login

**Any Gmail Account:**
- Email: `anything@gmail.com`
- Password: `any password`

**Example:**
- Email: `patient123@gmail.com`
- Password: `test123`

---

## Role-Based Access

### Admin Panel Access:
✅ Admin (`admin@123`)
❌ Regular patients

### Patient Dashboard Access:
✅ All Gmail users
❌ Admin (redirected to admin panel)

---

## Security Notes

⚠️ **Important:** In production, change these credentials!

Current setup is for **development/testing only**.

For production:
1. Use strong passwords
2. Hash passwords in database
3. Implement 2FA
4. Use environment variables
5. Add rate limiting

---

## Quick Test

1. **Login as Admin:**
   - Email: `admin@123`
   - Password: `1234`
   - Select: **Admin**
   - Result: Redirected to `/admin`

2. **Login as Patient:**
   - Email: `test@gmail.com`
   - Password: `anything`
   - Select: **Patient**
   - Result: Redirected to `/dashboard`

---

✅ **All set! Use these credentials to access the admin panel.**
