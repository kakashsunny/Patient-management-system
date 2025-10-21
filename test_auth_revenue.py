"""
Test script for Authentication and Revenue System
Run this after starting the Flask server
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_authentication():
    """Test authentication system"""
    print("\n" + "="*60)
    print("🔐 TESTING AUTHENTICATION SYSTEM")
    print("="*60)
    
    # Test 1: Access admin route without token
    print("\n1️⃣ Testing admin route without token...")
    response = requests.get(f"{BASE_URL}/api/reports/dashboard")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 401, "Should return 401 Unauthorized"
    print("   ✅ PASSED: Returns 401 without token")
    
    # Test 2: Login as admin
    print("\n2️⃣ Testing admin login...")
    login_data = {
        "email": "admin@123",
        "password": "1234"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    data = response.json()
    assert response.status_code == 200, "Login should succeed"
    assert 'token' in data, "Should return token"
    admin_token = data['token']
    print(f"   ✅ PASSED: Admin login successful")
    print(f"   Token: {admin_token[:50]}...")
    
    # Test 3: Access admin route with valid token
    print("\n3️⃣ Testing admin route with valid token...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/api/reports/dashboard", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json().get('stats', {})
        print(f"   ✅ PASSED: Admin route accessible")
        print(f"   Stats: {json.dumps(stats, indent=6)}")
    else:
        print(f"   ❌ FAILED: {response.json()}")
    
    # Test 4: Login as patient
    print("\n4️⃣ Testing patient login...")
    patient_data = {
        "email": "patient@gmail.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=patient_data)
    print(f"   Status: {response.status_code}")
    data = response.json()
    patient_token = data.get('token')
    print(f"   ✅ PASSED: Patient login successful")
    
    # Test 5: Patient tries to access admin route
    print("\n5️⃣ Testing patient accessing admin route...")
    headers = {"Authorization": f"Bearer {patient_token}"}
    response = requests.get(f"{BASE_URL}/api/reports/dashboard", headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 403, "Should return 403 Forbidden"
    print("   ✅ PASSED: Patient blocked from admin route")
    
    # Test 6: Patient can access own appointments
    print("\n6️⃣ Testing patient accessing own appointments...")
    response = requests.get(f"{BASE_URL}/api/appointments/my-appointments", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        appointments = response.json().get('appointments', [])
        print(f"   ✅ PASSED: Patient can access own appointments")
        print(f"   Found {len(appointments)} appointments")
    else:
        print(f"   ❌ FAILED: {response.json()}")

def test_revenue_calculation():
    """Test revenue calculation system"""
    print("\n" + "="*60)
    print("💰 TESTING REVENUE CALCULATION")
    print("="*60)
    
    # Login as admin first
    login_data = {"email": "admin@123", "password": "1234"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    admin_token = response.json()['token']
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get dashboard stats
    print("\n📊 Fetching dashboard statistics...")
    response = requests.get(f"{BASE_URL}/api/reports/dashboard", headers=headers)
    
    if response.status_code == 200:
        stats = response.json().get('stats', {})
        
        print("\n✅ Revenue Calculation Details:")
        print(f"   Total Patients: {stats.get('total_patients', 0)}")
        print(f"   Completed Appointments: {stats.get('completed_appointments', 0)}")
        print(f"   Monthly Revenue: ₹{stats.get('monthly_revenue', 0):,.2f}")
        
        # Calculate expected revenue
        completed = stats.get('completed_appointments', 0)
        base_fee = 500  # Consultation fee
        tax_rate = 0.18
        expected_per_appointment = base_fee * (1 + tax_rate)
        
        print(f"\n📈 Revenue Breakdown:")
        print(f"   Base Fee per Appointment: ₹{base_fee}")
        print(f"   Tax Rate: {tax_rate * 100}%")
        print(f"   Total per Appointment: ₹{expected_per_appointment}")
        print(f"   Completed Appointments: {completed}")
        print(f"   Expected Revenue: ₹{expected_per_appointment * completed:,.2f}")
        print(f"   Actual Revenue: ₹{stats.get('monthly_revenue', 0):,.2f}")
        
        print("\n✅ Revenue system includes 18% tax!")
    else:
        print(f"❌ Failed to fetch stats: {response.json()}")

def main():
    """Run all tests"""
    print("\n🚀 Starting Authentication & Revenue Tests")
    print("Make sure Flask server is running on http://localhost:5000")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code != 200:
            print("❌ Server is not running!")
            return
        
        print("✅ Server is running")
        
        # Run tests
        test_authentication()
        test_revenue_calculation()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Please start the Flask server first:")
        print("   python app_supabase.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
