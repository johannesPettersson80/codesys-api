#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS Path Debugging Tool

This script checks if the CODESYS executable is accessible and can be launched.
It helps diagnose issues with CODESYS integration.
"""

import os
import sys
import subprocess
import time

# Import the path from HTTP_SERVER.py
try:
    from HTTP_SERVER import CODESYS_PATH
    print(f"Imported CODESYS_PATH from HTTP_SERVER.py: {CODESYS_PATH}")
except ImportError:
    CODESYS_PATH = r"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe"
    print(f"Using default CODESYS_PATH: {CODESYS_PATH}")

def check_codesys_path():
    """Check if the CODESYS executable exists and can be accessed."""
    print("\n== CODESYS Path Check ==")
    
    # Check if path exists
    if os.path.exists(CODESYS_PATH):
        print(f"✓ CODESYS executable found at: {CODESYS_PATH}")
    else:
        print(f"✗ CODESYS executable NOT found at: {CODESYS_PATH}")
        print("\nPossible reasons:")
        print("1. The path is incorrect")
        print("2. CODESYS is not installed")
        print("3. CODESYS is installed in a different location")
        return False
    
    # Check if path is a file
    if os.path.isfile(CODESYS_PATH):
        print("✓ Path points to a file")
    else:
        print("✗ Path does not point to a file")
        return False
    
    # Check if file is executable
    try:
        # Get file info
        file_size = os.path.getsize(CODESYS_PATH) / (1024 * 1024)  # Size in MB
        print(f"✓ File size: {file_size:.2f} MB")
        
        # Try to get version info if on Windows
        if os.name == 'nt':
            try:
                import win32api
                info = win32api.GetFileVersionInfo(CODESYS_PATH, '\\')
                ms = info['FileVersionMS']
                ls = info['FileVersionLS']
                version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
                print(f"✓ File version: {version}")
            except:
                print("i Could not retrieve file version information")
    except Exception as e:
        print(f"✗ Error accessing file: {str(e)}")
        return False
    
    print("\n== CODESYS Execution Test ==")
    print("Attempting to launch CODESYS with --help option...")
    
    try:
        # Try to launch CODESYS with help flag (should exit quickly)
        start = time.time()
        process = subprocess.Popen(
            [CODESYS_PATH, "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for a few seconds
        try:
            stdout, stderr = process.communicate(timeout=5)
            stdout = stdout.decode('utf-8', errors='replace') if stdout else ""
            stderr = stderr.decode('utf-8', errors='replace') if stderr else ""
            
            # Check output
            if stdout:
                print(f"✓ CODESYS launched successfully with output")
                print("\nOutput excerpt:")
                lines = stdout.split('\n')
                for line in lines[:10]:  # Print first 10 lines
                    if line.strip():
                        print(f"  {line}")
                if len(lines) > 10:
                    print(f"  ... (total {len(lines)} lines)")
            elif stderr:
                print(f"✗ CODESYS launched but had errors")
                print("\nError output:")
                print(stderr)
            else:
                print("✓ CODESYS launched with no output")
                
            # Check exit code
            exit_code = process.returncode
            if exit_code == 0:
                print(f"✓ CODESYS exited with code 0 (success)")
            else:
                print(f"✗ CODESYS exited with code {exit_code}")
                
            print(f"✓ Total execution time: {time.time() - start:.2f} seconds")
            
        except subprocess.TimeoutExpired:
            process.kill()
            print("✗ CODESYS process did not exit within timeout period (5s)")
            print("  This might be normal for some CODESYS versions")
            
    except Exception as e:
        print(f"✗ Failed to launch CODESYS: {str(e)}")
        return False
    
    print("\n== Script Path Check ==")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PERSISTENT_SCRIPT = os.path.join(SCRIPT_DIR, "PERSISTENT_SESSION.py")
    
    if os.path.exists(PERSISTENT_SCRIPT):
        print(f"✓ PERSISTENT_SESSION.py found at: {PERSISTENT_SCRIPT}")
        
        # Check script size and content
        try:
            with open(PERSISTENT_SCRIPT, 'r') as f:
                content = f.read()
                print(f"✓ Script size: {len(content)} bytes")
                
                # Check for some key functions
                if "def initialize(self):" in content:
                    print("✓ initialize() function found in script")
                else:
                    print("✗ initialize() function NOT found in script")
                    
                if "def execute_script(self, script_path):" in content:
                    print("✓ execute_script() function found in script")
                else:
                    print("✗ execute_script() function NOT found in script")
        except Exception as e:
            print(f"✗ Error reading script: {str(e)}")
    else:
        print(f"✗ PERSISTENT_SESSION.py NOT found at: {PERSISTENT_SCRIPT}")
    
    print("\n== Summary ==")
    print("The CODESYS executable appears to be accessible.")
    print("If you're still experiencing issues, check:")
    print("1. CODESYS version compatibility")
    print("2. Script permissions")
    print("3. Network connectivity and firewall settings")
    print("4. Check logs for detailed error messages")
    
    return True

if __name__ == "__main__":
    print("=== CODESYS Integration Debug Tool ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    check_codesys_path()