#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS Diagnostic Script

This script tests the basic functionality of launching CODESYS and executing
a simple script inside it. It provides detailed output about what's happening
at each step to help diagnose issues.
"""

import os
import sys
import time
import subprocess
import tempfile
import json

# CODESYS path - update this to match your installation
CODESYS_PATH = r"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe"

# Test directories
TEMP_DIR = tempfile.gettempdir()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Test files
TEST_SCRIPT_PATH = os.path.join(TEMP_DIR, "codesys_test_script.py")
TEST_RESULT_PATH = os.path.join(TEMP_DIR, "codesys_test_result.json")
STATUS_FILE = os.path.join(SCRIPT_DIR, "session_status.json")

def print_separator():
    print("\n" + "="*80 + "\n")

def check_codesys_path():
    """Check if CODESYS executable exists."""
    print(f"Checking CODESYS path: {CODESYS_PATH}")
    
    if os.path.exists(CODESYS_PATH):
        print("✓ CODESYS executable found!")
    else:
        print("❌ CODESYS executable NOT found!")
        print(f"Please update the CODESYS_PATH in this script to point to your CODESYS installation.")
        return False
    
    return True

def create_test_script():
    """Create a simple test script for CODESYS."""
    print(f"Creating test script at: {TEST_SCRIPT_PATH}")
    
    script_content = """
import scriptengine
import json
import os
import sys
import time

# Create a status file to indicate script has started
status_path = r"{status_file}"
try:
    with open(status_path, 'w') as f:
        f.write(json.dumps({{"state": "running", "timestamp": time.time()}}))
    print("Created status file")
except Exception as e:
    print("Error creating status file:", str(e))

# Try to initialize the ScriptSystem
result = {{"success": False, "error": "Script did not complete"}}
try:
    print("Initializing ScriptSystem...")
    print("Python version:", sys.version)
    print("Working directory:", os.getcwd())
    
    # Initialize the system
    system = scriptengine.ScriptSystem()
    print("Successfully created ScriptSystem instance")
    
    # Get version info if available
    if hasattr(system, 'version'):
        version = system.version
        print("CODESYS version:", version)
    else:
        version = "Unknown"
        print("Version info not available in ScriptSystem")
    
    # Success result
    result = {{
        "success": True,
        "message": "Script executed successfully",
        "version": str(version),
        "timestamp": time.time()
    }}
except Exception as e:
    print("Error in script:", str(e))
    result = {{
        "success": False,
        "error": str(e),
        "timestamp": time.time()
    }}

# Save the result
try:
    result_path = r"{result_path}"
    with open(result_path, 'w') as f:
        f.write(json.dumps(result))
    print("Result saved to:", result_path)
except Exception as e:
    print("Error saving result:", str(e))
""".format(
    status_file=STATUS_FILE.replace("\\", "\\\\"),
    result_path=TEST_RESULT_PATH.replace("\\", "\\\\")
)
    
    try:
        with open(TEST_SCRIPT_PATH, 'w') as f:
            f.write(script_content)
        print("✓ Test script created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create test script: {str(e)}")
        return False

def clean_old_files():
    """Remove old test files if they exist."""
    print("Cleaning up old test files...")
    
    for path in [TEST_RESULT_PATH, STATUS_FILE]:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"✓ Removed old file: {path}")
            except Exception as e:
                print(f"❌ Failed to remove file {path}: {str(e)}")

def run_codesys_with_script():
    """Run CODESYS with the test script."""
    print_separator()
    print(f"Launching CODESYS with test script...")
    print(f"Command: {CODESYS_PATH} -script {TEST_SCRIPT_PATH}")
    
    try:
        # Remove any old status files
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)
            
        # Set up environment with PYTHONPATH pointing to ScriptLib
        script_lib_path = os.path.join(SCRIPT_DIR, "ScriptLib")
        env = os.environ.copy()
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = script_lib_path + os.pathsep + env["PYTHONPATH"]
        else:
            env["PYTHONPATH"] = script_lib_path
        
        print(f"Setting PYTHONPATH to: {env['PYTHONPATH']}")
        
        # Start CODESYS with the script using the correct --runscript parameter
        process = subprocess.Popen(
            [CODESYS_PATH, "--runscript", TEST_SCRIPT_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        
        print(f"✓ Process started with PID: {process.pid}")
        
        # Wait for status file to appear or process to exit
        print("Waiting for status file or process to complete...")
        max_wait = 30  # seconds
        wait_interval = 1
        total_waited = 0
        
        while total_waited < max_wait:
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                stderr_text = stderr.decode('utf-8', errors='replace') if stderr else "No error output"
                stdout_text = stdout.decode('utf-8', errors='replace') if stdout else "No standard output"
                
                print(f"❌ Process exited early with code: {process.returncode}")
                print("STDERR:")
                print(stderr_text)
                print("STDOUT:")
                print(stdout_text)
                break
            
            # Check if status file exists
            if os.path.exists(STATUS_FILE):
                try:
                    with open(STATUS_FILE, 'r') as f:
                        status = json.loads(f.read())
                    print(f"✓ Status file found! Status: {status.get('state')}")
                    break
                except Exception as e:
                    print(f"❌ Error reading status file: {str(e)}")
            
            time.sleep(wait_interval)
            total_waited += wait_interval
            sys.stdout.write(f"\rWaiting... {total_waited}s")
            sys.stdout.flush()
        
        if total_waited >= max_wait:
            print(f"\n⚠️ Timed out waiting for status file after {max_wait} seconds")
            print("CODESYS might be running but not creating the status file.")
        else:
            print(f"\nContinued after {total_waited} seconds")
        
        # Now wait for result file to appear
        print_separator()
        print("Waiting for script execution to complete and result file to appear...")
        max_wait = 30  # seconds
        total_waited = 0
        
        while total_waited < max_wait:
            # Check if result file exists
            if os.path.exists(TEST_RESULT_PATH):
                try:
                    with open(TEST_RESULT_PATH, 'r') as f:
                        result = json.loads(f.read())
                    print(f"✓ Result file found!")
                    print(f"Success: {result.get('success')}")
                    if result.get('success'):
                        print(f"Message: {result.get('message')}")
                        print(f"CODESYS Version: {result.get('version')}")
                    else:
                        print(f"Error: {result.get('error')}")
                    
                    # Try to terminate the process if it's still running
                    if process.poll() is None:
                        process.terminate()
                        print("Process terminated")
                    
                    return True
                except Exception as e:
                    print(f"❌ Error reading result file: {str(e)}")
            
            time.sleep(wait_interval)
            total_waited += wait_interval
            sys.stdout.write(f"\rWaiting for result... {total_waited}s")
            sys.stdout.flush()
        
        print(f"\n⚠️ Timed out waiting for result file after {max_wait} seconds")
        
        # Check if process is still running
        if process.poll() is None:
            print("CODESYS process is still running but not producing a result")
            print("Attempting to terminate the process...")
            process.terminate()
            time.sleep(2)
            
            if process.poll() is None:
                print("Process not responding to terminate, trying kill...")
                process.kill()
        else:
            stdout, stderr = process.communicate()
            stderr_text = stderr.decode('utf-8', errors='replace') if stderr else "No error output"
            stdout_text = stdout.decode('utf-8', errors='replace') if stdout else "No standard output"
            
            print(f"Process exited with code: {process.returncode}")
            if stdout_text.strip():
                print("STDOUT:")
                print(stdout_text)
            if stderr_text.strip():
                print("STDERR:")
                print(stderr_text)
        
        return False
        
    except Exception as e:
        print(f"❌ Error running CODESYS with script: {str(e)}")
        return False

def check_temp_directory():
    """Check if temp directory exists and is writable."""
    print(f"Checking temp directory: {TEMP_DIR}")
    
    if os.path.exists(TEMP_DIR):
        print(f"✓ Temp directory exists")
    else:
        print(f"❌ Temp directory doesn't exist!")
        try:
            os.makedirs(TEMP_DIR)
            print(f"✓ Created temp directory")
        except Exception as e:
            print(f"❌ Failed to create temp directory: {str(e)}")
            return False
    
    # Check if writable
    try:
        test_file = os.path.join(TEMP_DIR, "write_test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"✓ Temp directory is writable")
    except Exception as e:
        print(f"❌ Temp directory is not writable: {str(e)}")
        return False
    
    return True

def check_script_directory():
    """Check if script directory exists and is writable."""
    print(f"Checking script directory: {SCRIPT_DIR}")
    
    if os.path.exists(SCRIPT_DIR):
        print(f"✓ Script directory exists")
    else:
        print(f"❌ Script directory doesn't exist!")
        return False
    
    # Check if writable
    try:
        test_file = os.path.join(SCRIPT_DIR, "write_test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"✓ Script directory is writable")
    except Exception as e:
        print(f"❌ Script directory is not writable: {str(e)}")
        return False
    
    return True

def main():
    """Main function."""
    print_separator()
    print("CODESYS Diagnostic Script")
    print("This script will help diagnose issues with running scripts in CODESYS")
    print_separator()
    
    # Check environment
    if not check_codesys_path():
        return
    if not check_temp_directory():
        return
    if not check_script_directory():
        return
    
    # Clean up old files
    clean_old_files()
    
    # Create test script
    if not create_test_script():
        return
    
    # Run CODESYS with script
    success = run_codesys_with_script()
    
    print_separator()
    if success:
        print("✅ Test completed successfully!")
        print("CODESYS script execution is working correctly.")
    else:
        print("❌ Test failed!")
        print("CODESYS script execution is not working correctly.")
        print("\nPossible issues:")
        print("1. CODESYS might not be configured to run scripts properly")
        print("2. Permission issues with temp directory or script directory")
        print("3. The scriptengine module might not be available in CODESYS")
        print("4. CODESYS might be blocking script execution for security reasons")
        
        print("\nRecommendations:")
        print("1. Try running CODESYS manually and ensure it starts correctly")
        print("2. Check if CODESYS is configured to allow script execution")
        print("3. Verify that the CODESYS installation includes the scriptengine module")
        print("4. Check for any error logs in the CODESYS application")
    
    print_separator()
    print("Diagnostic script completed!")
    
if __name__ == "__main__":
    main()