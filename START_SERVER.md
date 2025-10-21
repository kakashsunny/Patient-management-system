# 🚀 How to Start Your Hospital Management System

## ❌ Why "Go Live" Doesn't Work

**Live Server extension only works with static HTML files.**

Your project uses **Flask (Python)** which needs a Python server, not a file server.

---

## ✅ Correct Way to Run (3 Methods)

### Method 1: Using Terminal (Recommended)

**Step 1:** Open Terminal in VS Code
- Press `Ctrl + `` (backtick)
- Or: Menu → Terminal → New Terminal

**Step 2:** Run these commands:
```bash
cd c:\Users\LENOVO\jk\hospital-management
python app.py
```

**Step 3:** Open browser and go to:
```
http://localhost:5000
```

---

### Method 2: Double-Click run.bat (Easiest!)

**Step 1:** Find `run.bat` file in your project folder

**Step 2:** Double-click it

**Step 3:** Browser will show the server is running

**Step 4:** Open browser and go to:
```
http://localhost:5000
```

---

### Method 3: Using Python Directly

**Step 1:** Right-click on `app.py` in VS Code

**Step 2:** Select "Run Python File in Terminal"

**Step 3:** Open browser and go to:
```
http://localhost:5000
```

---

## 🎯 Quick Reference

### To Start Server:
```bash
python app.py
```

### To Stop Server:
Press `Ctrl + C` in terminal

### To Access Website:
```
Patient Portal: http://localhost:5000
Admin Dashboard: http://localhost:5000/admin
```

---

## 🔧 Troubleshooting

### Problem: "python is not recognized"

**Solution 1:** Use `py` instead:
```bash
py app.py
```

**Solution 2:** Add Python to PATH:
1. Search "Environment Variables" in Windows
2. Edit PATH
3. Add Python installation folder

---

### Problem: "No module named flask"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

Then run:
```bash
python app.py
```

---

### Problem: "Port 5000 already in use"

**Solution 1:** Kill existing process:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution 2:** Use different port:
Edit `app.py`, change last line to:
```python
app.run(debug=True, port=5001)
```

Then access: `http://localhost:5001`

---

### Problem: Shows folder structure instead of website

**Cause:** You're using Live Server or opening HTML files directly

**Solution:** 
- ❌ Don't use "Go Live" button
- ❌ Don't open HTML files directly
- ✅ Run `python app.py` in terminal
- ✅ Open `http://localhost:5000` in browser

---

## 📋 Complete Startup Checklist

Before running for the first time:

- [ ] Python installed (3.8+)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Firebase credentials: `firebase-credentials.json` in project root
- [ ] Environment file: `.env` created from `.env.example`
- [ ] Admin user created: `python setup_admin.py`

Then run:
```bash
python app.py
```

---

## 🎓 Understanding the Difference

### Live Server (Static Files)
```
HTML File → Browser
(No backend processing)
```
**Works for:** Plain HTML/CSS/JS websites

### Flask Server (Dynamic)
```
Browser → Flask (Python) → Database → Response
(Backend processing, templates, APIs)
```
**Works for:** Your Hospital Management System

---

## 💡 Pro Tips

1. **Keep terminal open** while using the website
2. **Don't close terminal** or server will stop
3. **Use Ctrl+C** to stop server properly
4. **Restart server** after changing Python code
5. **No restart needed** for HTML/CSS changes (just refresh browser)

---

## 🚀 Quick Start Commands

**First Time Setup:**
```bash
cd c:\Users\LENOVO\jk\hospital-management
pip install -r requirements.txt
python setup_admin.py
```

**Every Time You Want to Run:**
```bash
python app.py
```

**Then open in browser:**
```
http://localhost:5000
```

---

## ✅ Success Indicators

When server starts correctly, you'll see:

```
🏥 City General Hospital
🚀 Starting Hospital Management System...
📍 Server running at: http://localhost:5000
📊 Admin Dashboard: http://localhost:5000/admin
👤 Patient Portal: http://localhost:5000

 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

**This means it's working!** Open the URL in your browser.

---

## 🎉 You're Ready!

1. ✅ Run `python app.py` in terminal
2. ✅ Wait for "Running on http://localhost:5000"
3. ✅ Open browser to http://localhost:5000
4. ✅ Enjoy your Hospital Management System!

---

**Remember: Always use terminal to run Flask apps, not Live Server!** 🚀
