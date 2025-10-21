# Delete Error: "Failed to cancel appointment" - SOLUTION

## Status Check ✓

✓ **Server is running** on port 5000  
✓ **Supabase credentials are configured**  
✓ **Enhanced logging is active**

## What to Do Now

### Step 1: Try Deleting an Appointment Again

1. Open: `http://localhost:5000/admin/appointments`
2. Click the **trash icon** on any appointment
3. Confirm the deletion

### Step 2: Check the Server Terminal

**Look at the terminal where you ran `python app_supabase.py`**

You will see detailed logs like this:

#### If Supabase Table Doesn't Exist:
```
============================================================
[DELETE] Attempting to cancel appointment: APT123
[DELETE] Supabase URL: https://xxxxx.supabase.co...
[DELETE] Supabase KEY: Present
[DELETE] Found 0 appointments
[ERROR] Appointment APT123 not found in database
============================================================
```
**Solution:** Create the appointments table in Supabase (see below)

#### If Update Fails:
```
============================================================
[DELETE] Attempting to cancel appointment: APT123
[DELETE] Found 1 appointments
[DELETE] Current status: pending, Payment: pending
[DELETE] Updating with data: {'status': 'cancelled', ...}
[DELETE] Making PATCH request to: https://...
[DELETE] Response status: 400
[ERROR] Update failed with status 400
[ERROR] Response: {"message":"..."}
============================================================
```
**Solution:** Check the error message in the response

#### If It Works:
```
============================================================
[DELETE] Attempting to cancel appointment: APT123
[DELETE] Found 1 appointments
[DELETE] Current status: pending, Payment: pending
[DELETE] Updating with data: {'status': 'cancelled', ...}
[DELETE] Making PATCH request to: https://...
[DELETE] Response status: 200
[SUCCESS] Cancelled appointment: APT123
============================================================
```
**Result:** Appointment disappears from list ✓

---

## Common Issues & Solutions

### Issue 1: "Appointment not found in database"

**Cause:** No appointments exist in Supabase table

**Solution:** Create a test appointment first:
1. Go to patient portal: `http://localhost:5000/booking`
2. Book an appointment
3. Then try deleting it from admin panel

### Issue 2: "Database update failed: 400"

**Cause:** Table structure issue or column doesn't exist

**Solution:** Check Supabase table structure:
1. Go to Supabase Dashboard
2. Click "Table Editor"
3. Find "appointments" table
4. Verify these columns exist:
   - `appointment_id` (text)
   - `status` (text)
   - `payment_status` (text)

### Issue 3: "Network error"

**Cause:** Can't connect to Supabase

**Solution:**
1. Check internet connection
2. Verify Supabase URL is correct
3. Check Supabase project is active (not paused)

---

## Create Appointments Table in Supabase

If the table doesn't exist:

### Step 1: Go to Supabase Dashboard
https://supabase.com/dashboard

### Step 2: Select Your Project

### Step 3: Go to SQL Editor
Click "SQL Editor" in left sidebar

### Step 4: Run This SQL
```sql
-- Create appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    appointment_id TEXT UNIQUE NOT NULL,
    patient_name TEXT NOT NULL,
    patient_email TEXT NOT NULL,
    patient_phone TEXT,
    department TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    mode TEXT DEFAULT 'In-person',
    status TEXT DEFAULT 'pending',
    payment_status TEXT DEFAULT 'pending',
    consultation_fee NUMERIC DEFAULT 500,
    symptoms TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_appointment_id ON appointments(appointment_id);
CREATE INDEX IF NOT EXISTS idx_patient_email ON appointments(patient_email);
CREATE INDEX IF NOT EXISTS idx_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_date ON appointments(date);

-- Insert a test appointment
INSERT INTO appointments (
    appointment_id, 
    patient_name, 
    patient_email, 
    patient_phone,
    department, 
    date, 
    time, 
    status, 
    payment_status,
    consultation_fee
) VALUES (
    'APT' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0'),
    'Test Patient',
    'test@example.com',
    '+1234567890',
    'General Medicine',
    CURRENT_DATE::TEXT,
    '10:00 AM',
    'pending',
    'completed',
    500
);
```

Click **"Run"** button

### Step 5: Verify
Go to "Table Editor" → "appointments" → You should see the test appointment

---

## Test the Delete Function

### Method 1: Via Admin Panel
1. `http://localhost:5000/admin/appointments`
2. Click delete on the test appointment
3. Check terminal for logs

### Method 2: Via API (Direct Test)
```bash
# Replace APT0001 with actual appointment_id
curl -X DELETE http://localhost:5000/api/appointments/APT0001
```

---

## What the Logs Tell You

### Log Line 1: Credentials Check
```
[DELETE] Supabase URL: https://xxxxx.supabase.co...
[DELETE] Supabase KEY: Present
```
✓ Credentials are loaded

### Log Line 2: Finding Appointment
```
[DELETE] Found 1 appointments
```
✓ Appointment exists in database

### Log Line 3: Current State
```
[DELETE] Current status: pending, Payment: pending
```
✓ Shows current appointment state

### Log Line 4: Update Request
```
[DELETE] Making PATCH request to: https://...
[DELETE] Response status: 200
```
✓ Update successful

### Log Line 5: Result
```
[SUCCESS] Cancelled appointment: APT123
```
✓ Operation completed

---

## Next Steps

1. **Try deleting again** and watch the terminal
2. **Copy the exact error** from terminal (all lines between the `====` bars)
3. **Share the error** so I can provide specific solution

Or if you see:
- "Appointment not found" → Create test appointment first
- "Database update failed: 400" → Check table structure
- "Network error" → Check Supabase connection

---

## Quick Commands

### Check if table exists:
Go to Supabase Dashboard → Table Editor → Look for "appointments"

### View all appointments:
Go to Supabase Dashboard → Table Editor → "appointments" → View data

### Test API directly:
```bash
# Get all appointments
curl http://localhost:5000/api/appointments/all

# Delete specific appointment
curl -X DELETE http://localhost:5000/api/appointments/APT0001
```

---

**Current Status:**
- ✓ Server running with enhanced logging
- ✓ Supabase credentials configured
- ⏳ Waiting for you to try delete and check terminal logs

**What to do:** Try deleting an appointment and share the terminal output!
