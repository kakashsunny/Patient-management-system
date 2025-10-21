# 🚀 Quick Reference Guide - Authentication & Revenue

## 🔐 Authentication Quick Reference

### **Login Credentials**

**Admin:**
- Email: `admin@123`
- Password: `1234`

**Patient:**
- Any Gmail address (e.g., `patient@gmail.com`)
- Any password (auto-creates account)

### **Protected Routes**

| Route | Method | Auth Required | Role |
|-------|--------|---------------|------|
| `/api/reports/dashboard` | GET | ✅ | Admin |
| `/api/admin/patients` | GET | ✅ | Admin |
| `/api/appointments/all` | GET | ✅ | Admin |
| `/api/admin/messages` | GET | ✅ | Admin |
| `/api/admin/send-message` | POST | ✅ | Admin |
| `/api/login-activity/all` | GET | ✅ | Admin |
| `/api/appointments/book` | POST | ✅ | Patient/Admin |
| `/api/appointments/my-appointments` | GET | ✅ | Patient/Admin |
| `/api/appointments/<id>` | DELETE | ✅ | Patient/Admin |

### **Token Usage**

```javascript
// Store token after login
localStorage.setItem('token', response.token);

// Include in API requests
fetch('/api/appointments/my-appointments', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
```

---

## 💰 Revenue Calculation Quick Reference

### **Formula**
```
Revenue = (Consultation Fee × 1.18) × Completed Appointments
        - (Consultation Fee × 1.18) × Refunded Appointments
```

### **Constants**
- **Consultation Fee:** ₹500
- **Tax Rate:** 18% (GST)
- **Total per Appointment:** ₹590

### **Quick Calculations**

| Appointments | Base Revenue | With Tax (18%) | Final Amount |
|--------------|--------------|----------------|--------------|
| 1 | ₹500 | ₹590 | ₹590.00 |
| 5 | ₹2,500 | ₹2,950 | ₹2,950.00 |
| 10 | ₹5,000 | ₹5,900 | ₹5,900.00 |
| 20 | ₹10,000 | ₹11,800 | ₹11,800.00 |
| 50 | ₹25,000 | ₹29,500 | ₹29,500.00 |
| 100 | ₹50,000 | ₹59,000 | ₹59,000.00 |

### **Refund Impact**
```
1 Refund = -₹590
5 Refunds = -₹2,950
10 Refunds = -₹5,900
```

---

## 🧪 Testing Commands

### **Start Server**
```bash
python app_supabase.py
```

### **Run Tests**
```bash
python test_auth_revenue.py
```

### **Manual API Tests**

**1. Login as Admin:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@123","password":"1234"}'
```

**2. Get Dashboard (with token):**
```bash
curl http://localhost:5000/api/reports/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**3. Test Unauthorized Access:**
```bash
curl http://localhost:5000/api/reports/dashboard
# Should return 401
```

---

## 🔧 Configuration

### **Environment Variables (.env)**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### **App Configuration**
```python
# Token expiry: 30 days
# Tax rate: 18%
# Consultation fee: ₹500
```

---

## 📊 Dashboard Stats Explained

| Stat | Description | Calculation |
|------|-------------|-------------|
| **Total Patients** | Unique patients | Count of unique emails |
| **Today's Appointments** | Appointments today | Completed appointments for today |
| **Monthly Revenue** | Revenue this month | (Fee × 1.18) × Completed - Refunds |
| **Completed Appointments** | All completed | Count with payment_status='completed' |

---

## 🚨 Common Issues & Solutions

### **Issue: 401 Unauthorized**
**Solution:** Include valid token in Authorization header

### **Issue: 403 Forbidden**
**Solution:** Use admin token for admin routes

### **Issue: Revenue showing 0**
**Solution:** Ensure appointments have payment_status='completed'

### **Issue: Token expired**
**Solution:** Login again to get new token (expires after 30 days)

---

## 📝 Code Snippets

### **Frontend: Check Authentication**
```javascript
function isAuthenticated() {
  const token = localStorage.getItem('token');
  if (!token) return false;
  
  // Decode JWT to check expiry
  const payload = JSON.parse(atob(token.split('.')[1]));
  return payload.exp * 1000 > Date.now();
}
```

### **Frontend: Make Authenticated Request**
```javascript
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`/api${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
  
  if (response.status === 401) {
    // Token expired, redirect to login
    window.location.href = '/login';
  }
  
  return response.json();
}
```

### **Backend: Add New Protected Route**
```python
@app.route('/api/new-route', methods=['GET'])
@admin_required  # or @token_required
def new_route():
    # Access user info from decorator
    user_email = request.user_email
    user_role = request.user_role
    
    # Your logic here
    return jsonify({'message': 'Success'})
```

---

## ✅ Verification Checklist

Before deploying:

- [ ] Test admin login
- [ ] Test patient login
- [ ] Verify admin routes are protected
- [ ] Verify patient routes are protected
- [ ] Check revenue includes tax
- [ ] Test refund deduction
- [ ] Verify error messages
- [ ] Check token expiry handling

---

## 📞 Quick Help

**Server not starting?**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Install missing dependencies
pip install -r requirements.txt
```

**Database errors?**
```bash
# Check .env file exists
# Verify SUPABASE_URL and SUPABASE_KEY are set
```

**Authentication not working?**
```bash
# Check token is being sent in headers
# Verify token format: "Bearer <token>"
# Check token hasn't expired (30 days)
```

---

**🎉 System is ready to use!**
