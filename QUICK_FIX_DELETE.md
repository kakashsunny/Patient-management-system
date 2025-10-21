# Quick Fix: Delete Not Working

## Most Likely Cause: Supabase Not Configured

The delete function needs Supabase credentials to work. Here's how to fix it:

## Solution 1: Configure Supabase (Recommended)

### Step 1: Check Your .env File
Open `.env` file in the project root and verify these lines exist:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key-here
```

### Step 2: If Missing, Add Supabase Credentials

#### Option A: You Have Supabase Account
1. Go to https://supabase.com/dashboard
2. Open your project
3. Go to Settings → API
4. Copy:
   - **Project URL** → Put in `SUPABASE_URL`
   - **anon public key** → Put in `SUPABASE_KEY`

#### Option B: Create New Supabase Project (5 minutes)
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New Project"
5. Fill in:
   - Name: `hospital-management`
   - Database Password: (create a strong password)
   - Region: Choose closest to you
6. Wait 2 minutes for setup
7. Go to Settings → API
8. Copy URL and anon key to `.env` file

### Step 3: Create Appointments Table in Supabase

Go to Supabase Dashboard → SQL Editor → New Query:

```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    appointment_id TEXT UNIQUE NOT NULL,
    patient_name TEXT NOT NULL,
    patient_email TEXT NOT NULL,
    patient_phone TEXT,
    department TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    mode TEXT,
    status TEXT DEFAULT 'pending',
    payment_status TEXT DEFAULT 'pending',
    consultation_fee NUMERIC DEFAULT 0,
    symptoms TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add index for faster queries
CREATE INDEX idx_appointment_id ON appointments(appointment_id);
CREATE INDEX idx_patient_email ON appointments(patient_email);
CREATE INDEX idx_status ON appointments(status);
```

Click "Run" to create the table.

### Step 4: Restart Server
```bash
# Stop server (Ctrl + C in terminal)
# Then restart:
python app_supabase.py
```

---

## Solution 2: Use Mock Data (For Testing Only)

If you just want to test without Supabase, I can create a version that uses in-memory storage.

---

## How to Test After Setup

### Step 1: Check Server Logs
When you restart the server, you should see:
```
[HOSPITAL] City General Hospital - SUPABASE MODE
============================================================
[STARTING] Hospital Management System...
[SUCCESS] Connected to Supabase Database
[SERVER] Running at: http://localhost:5000
```

### Step 2: Try Delete Again
1. Go to: `http://localhost:5000/admin/appointments`
2. Click delete (trash icon)
3. Watch the terminal for detailed logs:

**Success looks like:**
```
============================================================
[DELETE] Attempting to cancel appointment: APT123
[DELETE] Supabase URL: https://xxxxx.supabase.co...
[DELETE] Supabase KEY: Present
[DELETE] Found 1 appointments
[DELETE] Current status: pending, Payment: pending
[DELETE] Updating with data: {'status': 'cancelled', ...}
[DELETE] Making PATCH request to: https://...
[DELETE] Response status: 200
[SUCCESS] Cancelled appointment: APT123
============================================================
```

**Error looks like:**
```
============================================================
[DELETE] Attempting to cancel appointment: APT123
[DELETE] No Supabase URL!
[DELETE] Supabase KEY: MISSING!
[ERROR] Supabase credentials not configured!
============================================================
```

---

## Quick Checklist

- [ ] `.env` file exists in project root
- [ ] `SUPABASE_URL` is set in `.env`
- [ ] `SUPABASE_KEY` is set in `.env`
- [ ] Supabase project is created
- [ ] `appointments` table exists in Supabase
- [ ] Server restarted after adding credentials
- [ ] Browser cache cleared (Ctrl + Shift + Delete)

---

## Still Not Working?

### Check These:

1. **Server Terminal Output**
   - Look for the detailed logs when you click delete
   - Copy the exact error message

2. **Browser Console (F12)**
   - Check for JavaScript errors
   - Check Network tab for failed requests

3. **Supabase Dashboard**
   - Verify table exists
   - Check if data is there
   - Test API in Supabase dashboard

---

## Alternative: Use Firebase Instead

If Supabase is too complicated, you can use the Firebase version:

1. Set up Firebase (see `FIREBASE_SETUP.md`)
2. Run `python app.py` instead of `python app_supabase.py`

---

## Need Help?

Run this command and share the output:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('URL:', 'SET' if os.getenv('SUPABASE_URL') else 'MISSING'); print('KEY:', 'SET' if os.getenv('SUPABASE_KEY') else 'MISSING')"
```

This will tell us if your credentials are configured.

---

**Server Status:** ✓ Running with enhanced error logging  
**Next Step:** Configure Supabase credentials in `.env` file
