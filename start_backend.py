#!/usr/bin/env python3
# start_backend.py - Simple backend starter script

import os
import sys
import subprocess

# Change to Backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'Backend')
os.chdir(backend_dir)

print(f"Starting backend server from: {os.getcwd()}")
print("Backend server will run on http://localhost:8001")
print("Press Ctrl+C to stop the server")
print("-" * 50)

# Start the server
try:
    subprocess.run([sys.executable, 'main.py'], check=True)
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Error starting server: {e}")
    print("Make sure you have all required packages installed:")
    print("pip install fastapi uvicorn sqlalchemy python-jose[cryptography] python-multipart")
