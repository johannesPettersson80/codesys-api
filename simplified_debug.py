#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simplified debugging script for CODESYS API
This is a standalone script that performs all necessary debugging
"""

import sys
import os
import time
import subprocess
import threading
import json

# Configure basic logging to console
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('debug.log')
    ]
)

# Print startup information
print("=" * 60)
print("CODESYS API Simplified Debugger")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print()

# Step 1: Check CODESYS path
print("STEP 1: Checking CODESYS executable path")
print("-" * 60)

try:
    from HTTP_SERVER import CODESYS_PATH, PERSISTENT_SCRIPT
    print(f"CODESYS_PATH: {CODESYS_PATH}")
    print(f"PERSISTENT_SCRIPT: {PERSISTENT_SCRIPT}")
    
    if os.path.exists(CODESYS_PATH):
        print("✓ CODESYS executable exists")
        file_size = os.path.getsize(CODESYS_PATH) / (1024 * 1024)  # Size in MB
        print(f"✓ File size: {file_size:.2f} MB")
    else:
        print("✗ CODESYS executable NOT found at this path")
        print("This is likely the cause of your issues.")
        
    if os.path.exists(PERSISTENT_SCRIPT):
        print("✓ PERSISTENT_SESSION.py script exists")
        file_size = os.path.getsize(PERSISTENT_SCRIPT) / 1024  # Size in KB
        print(f"✓ File size: {file_size:.2f} KB")
    else:
        print("✗ PERSISTENT_SESSION.py script NOT found")
        print("This is likely the cause of your issues.")
except Exception as e:
    print(f"Error checking paths: {str(e)}")
    
print()

# Step 2: Check directory structure
print("STEP 2: Checking directory structure")
print("-" * 60)

try:
    dirs_to_check = ['requests', 'results']
    for dir_name in dirs_to_check:
        dir_path = os.path.join(os.getcwd(), dir_name)
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"Creating directory: {dir_path}")
            os.makedirs(dir_path)
            print(f"✓ Directory created: {dir_path}")
except Exception as e:
    print(f"Error checking directories: {str(e)}")
    
print()

# Step 3: Test simple HTTP server
print("STEP 3: Testing basic HTTP functionality")
print("-" * 60)
print("Starting a basic HTTP server on port 8081...")

# Define a simple HTTP server
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received request for: {self.path}")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Simple server is working')
        
    def log_message(self, format, *args):
        # Override to prevent default logging to stderr
        print(f"HTTP: {self.address_string()} - {format % args}")

def run_simple_server():
    try:
        server = HTTPServer(('127.0.0.1', 8081), SimpleHandler)
        print("Simple server started on port 8081")
        server.serve_forever()
    except Exception as e:
        print(f"Error in simple server: {str(e)}")

# Start the server in a thread
server_thread = threading.Thread(target=run_simple_server)
server_thread.daemon = True
server_thread.start()

# Test the server
time.sleep(2)  # Give server time to start
print("Testing simple server with a request...")
try:
    import urllib.request
    with urllib.request.urlopen('http://127.0.0.1:8081/test') as response:
        content = response.read().decode('utf-8')
        print(f"✓ Server response: {content}")
except Exception as e:
    print(f"✗ Error testing server: {str(e)}")
    
print()

# Step 4: Test CODESYS process
print("STEP 4: Testing CODESYS process launch")
print("-" * 60)

def test_codesys_process():
    try:
        print(f"Attempting to launch CODESYS: {CODESYS_PATH}")
        
        # Create a simple test script
        test_script_path = os.path.join(os.getcwd(), "test_script.py")
        with open(test_script_path, 'w') as f:
            f.write("""
print("Test script running!")
import sys
print("Python version:", sys.version)
try:
    import scriptengine
    print("Successfully imported scriptengine")
except Exception as e:
    print("Error importing scriptengine:", str(e))
""")
        
        print(f"Created test script: {test_script_path}")
        
        # Try to launch CODESYS with the test script
        print("Starting CODESYS process...")
        process = subprocess.Popen(
            [CODESYS_PATH, "-script", test_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        print("Waiting for process to complete...")
        try:
            stdout, stderr = process.communicate(timeout=10)
            
            print("Process completed!")
            if stdout:
                print("=== STDOUT ===")
                print(stdout)
            if stderr:
                print("=== STDERR ===")
                print(stderr)
                
            print(f"Exit code: {process.returncode}")
        except subprocess.TimeoutExpired:
            process.kill()
            print("Process did not complete within timeout (10 seconds)")
            print("This might be normal if CODESYS is starting up properly")
            
    except Exception as e:
        print(f"Error testing CODESYS process: {str(e)}")
    finally:
        # Clean up
        if os.path.exists(test_script_path):
            os.remove(test_script_path)

test_codesys_process()
print()

# Step 5: Suggest next steps
print("STEP 5: Diagnosis and recommendations")
print("-" * 60)

print("""
Based on the tests, here are some potential issues and solutions:

1. If CODESYS executable was not found:
   - Check the path in HTTP_SERVER.py
   - Make sure CODESYS is installed

2. If the simple HTTP server test failed:
   - Check if another program is using port 8080
   - Verify network settings and firewall rules

3. If CODESYS process launch failed:
   - Verify CODESYS installation
   - Check permissions to run CODESYS

4. Next steps for testing the API:
   a. First try the test_server without CODESYS integration:
      python test_server.py
   
   b. Then try the API with:
      curl -H "Authorization: ApiKey admin" http://localhost:8080/api/v1/system/info
   
   c. Finally try the real server with:
      python HTTP_SERVER.py
      
For any errors you encounter, check:
- debug.log for detailed log messages
- codesys_api_server.log for server errors
- session.log for CODESYS session errors
""")

print("\nDebugging complete. See debug.log for detailed output.")