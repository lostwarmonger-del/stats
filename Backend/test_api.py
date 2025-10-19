#!/usr/bin/env python3
# test_api.py - Test script for the program 404640723 API

import requests
import json

BASE_URL = "http://localhost:8001"

def test_login():
    """Test login endpoint"""
    print("Testing login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful! Token: {data['access_token'][:20]}...")
        return data['access_token']
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_save_program_data(token):
    """Test saving program 404640723 data"""
    print("\nTesting save program data...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    test_data = {
        "row_number": "1",
        "page_channel_address": "https://example.com/page",
        "news_subject": "تست موضوع خبر",
        "naba_code": "NABA123",
        "naba_code_review": "بررسی شده",
        "naba_code_registration_date": "1403/01/15",
        "suspicion_classification": "کلاسه A",
        "suspicion_registration_date": "1403/01/16",
        "action_results": "اقدامات انجام شده",
        "identified_military_count": "5",
        "identified_military_dependents_count": "3",
        "honorary_police": "پلیس افتخاری تست"
    }
    
    response = requests.post(f"{BASE_URL}/programs/404640723", json=test_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Data saved successfully! Message: {data['message']}")
        return True
    else:
        print(f"❌ Save failed: {response.status_code} - {response.text}")
        return False

def test_get_program_data(token):
    """Test getting program 404640723 data"""
    print("\nTesting get program data...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/programs/404640723/1", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Data retrieved successfully!")
        print(f"   Row Number: {data.get('row_number')}")
        print(f"   News Subject: {data.get('news_subject')}")
        print(f"   NABA Code: {data.get('naba_code')}")
        return True
    else:
        print(f"❌ Get failed: {response.status_code} - {response.text}")
        return False

def main():
    print("🚀 Testing Program 404640723 API")
    print("=" * 50)
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test save data
    save_success = test_save_program_data(token)
    
    # Test get data
    get_success = test_get_program_data(token)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Login: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"Save Data: {'✅ PASS' if save_success else '❌ FAIL'}")
    print(f"Get Data: {'✅ PASS' if get_success else '❌ FAIL'}")
    
    if token and save_success and get_success:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the server logs.")

if __name__ == "__main__":
    main()
