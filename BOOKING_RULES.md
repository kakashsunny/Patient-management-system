# 📅 Appointment Booking Rules

## ✅ Implemented Features

### 1. **Working Hours Restriction**
- ⏰ Appointments can only be booked between **8:00 AM and 8:00 PM**
- ❌ Any time outside this range will be rejected
- Error message: "Appointments can only be booked between 8:00 AM and 8:00 PM."

### 2. **Unique Time Slot Rule**
- 🚫 No two patients can book the same date and time
- ✅ System checks if slot is already taken before booking
- Error message: "This time slot is already allotted to another person."

### 3. **20-Minute Gap Between Appointments**
- ⏱️ Minimum 20-minute gap between consecutive appointments
- 📊 System checks all appointments on the selected date
- ✅ Prevents overbooking and ensures proper scheduling
- Error message: "Please maintain a 20-minute gap. Slot at [TIME] is already booked."

### 4. **Time Slot Generation**
- 🕐 Time slots generated in 20-minute intervals
- 📋 Available slots: 8:00 AM, 8:20 AM, 8:40 AM, ... 7:40 PM, 8:00 PM
- 🎯 Total of 37 time slots per day

---

## 🎯 How It Works

### Backend Validation (`app_supabase.py`)

```python
# 1. Check working hours (8 AM - 8 PM)
if not (start_time <= time_obj <= end_time):
    return error

# 2. Check if exact slot is taken
existing = supabase_select('appointments', f'date=eq.{date}&time=eq.{time}')
if existing:
    return "This time slot is already allotted to another person."

# 3. Check 20-minute gap
for each appointment on same date:
    if time_difference < 20 minutes:
        return "Please maintain a 20-minute gap."
```

### Frontend (`booking.html`)

```javascript
// Generate time slots in 20-minute intervals
8:00 AM, 8:20 AM, 8:40 AM, 9:00 AM, ...
```

---

## 📊 Example Scenarios

### ✅ Valid Bookings:
- Patient A books: **Jan 15, 10:00 AM** ✓
- Patient B books: **Jan 15, 10:20 AM** ✓ (20-min gap)
- Patient C books: **Jan 15, 11:00 AM** ✓ (60-min gap)

### ❌ Invalid Bookings:
- Patient A books: **Jan 15, 10:00 AM** ✓
- Patient B tries: **Jan 15, 10:00 AM** ✗ (Same slot)
- Patient C tries: **Jan 15, 10:10 AM** ✗ (Less than 20-min gap)
- Patient D tries: **Jan 15, 7:00 AM** ✗ (Before working hours)
- Patient E tries: **Jan 15, 9:00 PM** ✗ (After working hours)

---

## 🚀 Testing Instructions

### Test 1: Working Hours
1. Try booking at **7:00 AM** → Should fail
2. Try booking at **9:00 PM** → Should fail
3. Try booking at **10:00 AM** → Should succeed

### Test 2: Unique Slot
1. Book appointment at **Jan 15, 2:00 PM**
2. Try booking same slot again → Should fail with message

### Test 3: 20-Minute Gap
1. Book appointment at **10:00 AM**
2. Try booking at **10:10 AM** → Should fail
3. Try booking at **10:20 AM** → Should succeed

---

## 📝 Notes

- All validations happen on the **backend** (secure)
- Frontend shows only valid time slots (better UX)
- Error messages are user-friendly
- System checks Supabase database for existing appointments
- Works in real-time with multiple users

---

## 🔧 Technical Details

**Database Table:** `appointments`
**Key Fields:**
- `date` (DATE)
- `time` (TEXT in HH:MM format)
- `status` (pending/confirmed)
- `payment_status` (pending/completed)

**Validation Order:**
1. Check working hours
2. Check exact slot availability
3. Check 20-minute gap rule
4. Create appointment if all pass

---

✅ **All rules implemented and tested!**
