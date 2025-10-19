#!/usr/bin/env python3
# test_notifications.py - Test notifications endpoint

import requests
import json

def test_notifications():
    try:
        print("Testing notifications endpoint...")
        response = requests.get('http://localhost:8001/notifications')
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Notifications endpoint is working!")
        else:
            print("❌ Notifications endpoint failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_notifications()
