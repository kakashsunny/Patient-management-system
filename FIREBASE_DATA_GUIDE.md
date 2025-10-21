# 🔍 How to View Login Data in Firebase

## 📊 Method 1: Firebase Console (Web Interface)

### Step 1: Access Firebase Console

1. Go to **[Firebase Console](https://console.firebase.google.com/)**
2. Click on your **hospital management project**
3. In the left sidebar, click **"Firestore Database"**

### Step 2: View Collections

You'll see these collections (after users start using the system):

#### 1️⃣ **users** Collection
**What it contains:** All registered users (patients, admins, staff)

**To view:**
- Click on "users" collection
- You'll see all user documents

**Each user document shows:**
```
Document ID: abc123xyz (unique user ID)
├── name: "John Doe"
├── email: "john@example.com"
├── phone: "+1234567890"
├── role: "patient" or "admin"
├── created_at: "2024-01-15T10:30:00"
├── last_login: "2024-01-20T14:25:00"  ← Last login time
├── last_login_ip: "192.168.1.1"       ← Last login IP
├── is_active: true
└── profile_photo: "url..."
```

#### 2️⃣ **login_history** Collection (NEW!)
**What it contains:** Every login attempt (successful and failed)

**To view:**
- Click on "login_history" collection
- You'll see all login records

**Each login record shows:**
```
Document ID: login_xyz789
├── user_id: "abc123xyz"
├── user_email: "john@example.com"
├── user_role: "patient"
├── status: "success" or "failed"
├── timestamp: "2024-01-20T14:25:00"
├── ip_address: "192.168.1.1"
├── browser: "Chrome"
├── os: "Windows"
└── user_agent: "Mozilla/5.0..."
```

#### 3️⃣ **appointments** Collection
**What it contains:** All appointment bookings

**To view:**
- Click on "appointments" collection
- See all appointments with patient details

#### 4️⃣ **staff** Collection
**What it contains:** Hospital staff information

#### 5️⃣ **invoices** Collection
**What it contains:** All billing records

#### 6️⃣ **inventory** Collection
**What it contains:** Medical supplies and equipment

---

## 🖥️ Method 2: Using Admin Dashboard

### View Login Activity in Admin Panel

1. **Start your application:**
   ```bash
   python app.py
   ```

2. **Login as admin:**
   - Go to: `http://localhost:5000/admin`
   - Login with your admin credentials

3. **View login activity:**
   - The system now tracks all logins automatically
   - You can access login data via API

### API Endpoints for Login Activity

**Get all login activity:**
```
GET /api/login-activity/all
Authorization: Bearer <admin-token>
```

**Get login history for specific user:**
```
GET /api/login-activity/user/<user_id>
Authorization: Bearer <admin-token>
```

---

## 🔍 Method 3: Check Specific Login Data

### Check if Anyone Has Logged In

**In Firebase Console:**

1. Go to Firestore Database
2. Click on **"users"** collection
3. **If you see documents** → Users have registered
4. Check **"last_login"** field → Shows when they last logged in
5. Click on **"login_history"** collection
6. **If you see documents** → Logins have occurred

### What Each Field Means

**In users collection:**
- `created_at` → When user registered
- `last_login` → Last successful login time
- `last_login_ip` → IP address of last login

**In login_history collection:**
- `timestamp` → Exact time of login attempt
- `status` → "success" or "failed"
- `ip_address` → User's IP address
- `browser` → Browser used (Chrome, Firefox, etc.)
- `os` → Operating system (Windows, macOS, etc.)

---

## 📱 Method 4: Real-Time Monitoring

### Enable Real-Time Updates in Firebase Console

1. In Firestore Database view
2. Click on a collection (e.g., "login_history")
3. Firebase automatically updates when new data is added
4. You'll see new logins appear in real-time!

---

## 🎯 Quick Check: Has Anyone Logged In?

### Fastest Way to Check:

1. **Open Firebase Console**
2. **Go to Firestore Database**
3. **Look for these signs:**

   ✅ **Users have registered if:**
   - "users" collection has documents
   - Each document = 1 registered user

   ✅ **Users have logged in if:**
   - "users" collection documents have "last_login" field
   - "login_history" collection exists and has documents

   ✅ **Recent activity if:**
   - "login_history" has recent timestamps
   - "appointments" collection has new bookings

---

## 📊 Example: What You'll See

### When Someone Registers:

**In "users" collection:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "role": "patient",
  "created_at": "2024-01-20T10:00:00",
  "is_active": true
}
```

### When Someone Logs In:

**In "login_history" collection:**
```json
{
  "user_id": "abc123",
  "user_email": "jane@example.com",
  "user_role": "patient",
  "status": "success",
  "timestamp": "2024-01-20T14:30:00",
  "ip_address": "192.168.1.100",
  "browser": "Chrome",
  "os": "Windows"
}
```

**Updated in "users" collection:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "last_login": "2024-01-20T14:30:00",  ← NEW!
  "last_login_ip": "192.168.1.100"      ← NEW!
}
```

---

## 🔔 What's New (Login Tracking Feature)

I've added automatic login tracking to your system:

### ✅ What's Tracked:
- Every login attempt (success and failed)
- User information (email, role)
- Device information (browser, OS)
- IP address
- Timestamp

### ✅ Where It's Stored:
- **Firestore Collection:** `login_history`
- **User Document:** Updated with `last_login` and `last_login_ip`

### ✅ How to Use:
1. Just run your application normally
2. When anyone logs in, it's automatically tracked
3. View in Firebase Console or via API

---

## 🎓 Step-by-Step Tutorial

### To See Login Data Right Now:

**Step 1:** Open Firebase Console
```
https://console.firebase.google.com/
```

**Step 2:** Select your project

**Step 3:** Click "Firestore Database" in left menu

**Step 4:** You'll see collections:
- Click "users" → See all registered users
- Click "login_history" → See all login attempts

**Step 5:** Click on any document to see details

**Step 6:** Look for:
- `timestamp` → When login happened
- `status` → Was it successful?
- `user_email` → Who logged in?

---

## 🚀 Testing Login Tracking

### Test It Yourself:

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Create a test account:**
   - Go to: `http://localhost:5000/signup`
   - Register with test email

3. **Login with test account:**
   - Go to: `http://localhost:5000/login`
   - Login with your test credentials

4. **Check Firebase:**
   - Open Firebase Console
   - Go to Firestore Database
   - Click "login_history" collection
   - **You'll see your login record!**

---

## 📈 Advanced: Query Login Data

### Using Firebase Console Filters:

1. In "login_history" collection
2. Click "Add filter"
3. Filter by:
   - `status` == "success" → See only successful logins
   - `user_email` == "specific@email.com" → See specific user
   - `timestamp` > "2024-01-20" → See recent logins

---

## 🔒 Security Note

**Login tracking includes:**
- ✅ IP addresses (for security)
- ✅ Browser and OS info
- ✅ Timestamps
- ✅ Success/failure status

**This helps you:**
- Detect suspicious login attempts
- Monitor user activity
- Troubleshoot login issues
- Track system usage

---

## 💡 Pro Tips

1. **Check daily:** Look at login_history to see system usage
2. **Monitor failed logins:** High failed attempts = potential security issue
3. **Track peak times:** See when most users login
4. **User analytics:** See which users are most active

---

## 🆘 Troubleshooting

**Q: I don't see any collections**
- A: No one has used the system yet. Create a test account first.

**Q: I see "users" but no "login_history"**
- A: Make sure you've updated the code with login tracking
- Restart your application
- Try logging in again

**Q: How do I export this data?**
- A: In Firebase Console, click "Export" button
- Or use the API endpoints to get JSON data

---

## ✅ Summary

**To view login data:**

1. **Firebase Console** → Firestore Database → "login_history" collection
2. **Check "users" collection** → Look at "last_login" field
3. **Use Admin API** → GET /api/login-activity/all

**What you'll see:**
- Who logged in
- When they logged in
- From where (IP address)
- Using what (browser, OS)
- Success or failed

---

**Your login tracking is now active! Every login is automatically recorded in Firebase.** 🎉
