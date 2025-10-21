# 🚀 Supabase Setup Guide (Much Easier than Firebase!)

## Why Supabase?
- ✅ **No billing required** - Completely free tier
- ✅ **Easier setup** - 5 minutes
- ✅ **PostgreSQL database** - More powerful than Firestore
- ✅ **Built-in authentication** - Ready to use
- ✅ **Real-time updates** - Like Firebase
- ✅ **Better free tier** - 500MB database, 2GB file storage

---

## 📋 Step-by-Step Setup

### Step 1: Create Supabase Account (1 minute)

1. Go to: **https://supabase.com/**
2. Click **"Start your project"** button
3. Sign in with:
   - **GitHub** (recommended)
   - Or **Google**
   - Or **Email**

---

### Step 2: Create New Project (2 minutes)

1. After logging in, click **"New Project"**
2. Fill in the details:
   - **Organization:** Select or create one
   - **Name:** `hospital-management`
   - **Database Password:** Create a strong password
     - Example: `Hospital@2024!Secure`
     - **⚠️ SAVE THIS PASSWORD!** You'll need it later
   - **Region:** Choose closest to you
     - India: `Southeast Asia (Singapore)`
     - US: `East US (North Virginia)`
     - Europe: `West EU (Ireland)`
   - **Pricing Plan:** Free (default)

3. Click **"Create new project"**
4. Wait 1-2 minutes while Supabase sets up your database

---

### Step 3: Get Your API Credentials (1 minute)

Once your project is ready:

1. In the left sidebar, click **"Settings"** (gear icon ⚙️)
2. Click **"API"** in the settings menu
3. You'll see two important values:

   **Project URL:**
   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```
   
   **API Key (anon public):**
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4...
   ```

4. **Copy both of these!**

---

### Step 4: Update Your .env File (1 minute)

1. Open your `.env` file in VS Code
2. Update these lines:

```env
SECRET_KEY=my-super-secret-key-12345

# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Replace with your actual URL and Key from Step 3.

3. Save the file (`Ctrl + S`)

---

### Step 5: Install Supabase Package

In terminal, run:

```bash
py -m pip install supabase
```

---

### Step 6: Create Database Tables

In Supabase dashboard:

1. Click **"SQL Editor"** in left sidebar
2. Click **"New query"**
3. Copy and paste this SQL:

```sql
-- Users table
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'patient',
    is_active BOOLEAN DEFAULT true,
    profile_photo TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    last_login_ip TEXT
);

-- Appointments table
CREATE TABLE appointments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    appointment_id TEXT UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id),
    patient_name TEXT NOT NULL,
    patient_email TEXT NOT NULL,
    patient_phone TEXT NOT NULL,
    department TEXT NOT NULL,
    date DATE NOT NULL,
    time TEXT NOT NULL,
    mode TEXT NOT NULL,
    symptoms TEXT,
    status TEXT DEFAULT 'pending',
    payment_status TEXT DEFAULT 'pending',
    consultation_fee DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Staff table
CREATE TABLE staff (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    role TEXT NOT NULL,
    department TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Login history table
CREATE TABLE login_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    user_role TEXT,
    status TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address TEXT,
    browser TEXT,
    os TEXT,
    user_agent TEXT
);
```

4. Click **"Run"** button
5. You should see "Success. No rows returned"

---

### Step 7: Run Your Application! 🎉

```bash
py app_no_firebase.py
```

Then open: **http://localhost:5000**

---

## ✅ Verification Checklist

- [ ] Supabase account created
- [ ] Project created and ready
- [ ] Got Project URL
- [ ] Got API Key (anon public)
- [ ] Updated `.env` file with credentials
- [ ] Installed supabase package: `py -m pip install supabase`
- [ ] Created database tables using SQL Editor
- [ ] Application runs successfully

---

## 🎯 What You Get with Supabase Free Tier

- ✅ **500 MB database** - Plenty for a hospital
- ✅ **2 GB file storage** - For medical reports, images
- ✅ **Unlimited API requests** - No limits!
- ✅ **50,000 monthly active users** - More than enough
- ✅ **Real-time subscriptions** - Live updates
- ✅ **Authentication** - Built-in user management

---

## 🔍 Supabase Dashboard Features

**Table Editor:**
- View all your data in tables
- Add/edit/delete records manually
- Like Excel but for your database

**SQL Editor:**
- Run custom SQL queries
- Create tables, views, functions

**Authentication:**
- Manage users
- See login history
- Configure auth providers

**Storage:**
- Upload files (prescriptions, reports)
- Manage medical documents

---

## 💡 Pro Tips

1. **Bookmark your project URL** - You'll use it often
2. **Save your database password** - Keep it secure
3. **Use Table Editor** - Easy way to view data
4. **Check logs** - See all database activity

---

## 🆘 Troubleshooting

**Q: Can't find API settings**
A: Settings (⚙️) → API → Scroll down to "Project API keys"

**Q: Which API key to use?**
A: Use **"anon public"** key (not the service_role key)

**Q: Database password forgotten?**
A: Settings → Database → Reset database password

**Q: Tables not created?**
A: SQL Editor → Copy SQL again → Make sure to click "Run"

---

## 🎉 You're Done!

Supabase is now set up and ready to use!

**Much easier than Firebase, right?** 😊

---

## 📚 Next Steps

1. Run your app: `py app_no_firebase.py`
2. Create a test account
3. Book an appointment
4. Check Supabase dashboard to see the data!

---

**Your Supabase Dashboard:** https://supabase.com/dashboard/project/YOUR-PROJECT-ID
