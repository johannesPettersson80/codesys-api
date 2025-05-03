"""
Alternative approach to test CODESYS automation

Instead of launching CODESYS with a script, this attempts to use
the CODESYS Automation Interface if available.
"""

import os
import sys
import time
import subprocess

def main():
    print("Testing CODESYS Automation Interface")
    print("-" * 50)
    
    # Try to use the COM interface if available
    try:
        import win32com.client
        
        print("Attempting to connect to CODESYS via COM interface...")
        
        # Try to create the CODESYS application object
        app = win32com.client.Dispatch("CODESYS.Application")
        print("Successfully created CODESYS application object")
        
        # Get version information
        version = app.Version
        print(f"CODESYS version: {version}")
        
        # Try to execute a simple operation
        print("Attempting to execute a simple operation...")
        # Depending on the COM interface, you might need to use different methods
        # This is just a generic attempt
        if hasattr(app, 'ShowMessage'):
            app.ShowMessage("Test message from automation script")
            print("Message displayed successfully")
        else:
            print("ShowMessage method not available")
            
        # List available methods
        print("\nAvailable methods and properties:")
        for item in dir(app):
            if not item.startswith('_'):
                print(f"- {item}")
                
        print("\nCOM interface test completed successfully")
        
    except ImportError:
        print("Error: win32com.client not available. Please install pywin32.")
        print("You can install it with: pip install pywin32")
        
    except Exception as e:
        print(f"Error accessing CODESYS COM interface: {str(e)}")
        print("This might indicate that CODESYS doesn't expose a COM automation interface")
    
    print("\nTrying alternative approach - executing a script directly with IronPython...")
    
    # Look for IronPython installation that might have been installed with CODESYS
    ironpython_paths = [
        r"C:\Program Files\IronPython 2.7",
        r"C:\Program Files (x86)\IronPython 2.7",
        r"C:\Program Files\CODESYS 3.5.21.0\IronPython",
        r"C:\Program Files\CODESYS 3.5.21.0\CODESYS\IronPython",
        r"C:\Program Files\CODESYS 3.5.21.0\Common\IronPython",
    ]
    
    for path in ironpython_paths:
        ipy_exe = os.path.join(path, "ipy.exe")
        if os.path.exists(ipy_exe):
            print(f"Found IronPython at: {ipy_exe}")
            
            # Create a simple test script
            test_script = os.path.join(os.getcwd(), "ipy_test.py")
            with open(test_script, 'w') as f:
                f.write("""
print("IronPython test script running")
print("Python version:", sys.version)

# Try to import CODESYS modules
try:
    import scriptengine
    print("Successfully imported scriptengine")
    
    # Try to create system object
    system = scriptengine.System()
    print("Successfully created system object")
    
    # Display version if available
    if hasattr(system, 'version'):
        print("CODESYS version:", system.version)
    
except ImportError as ie:
    print("Error importing scriptengine:", str(ie))
    
except Exception as e:
    print("Error:", str(e))
""")
            
            # Run the test script with IronPython
            print(f"Running test script with IronPython: {ipy_exe}")
            try:
                result = subprocess.run([ipy_exe, test_script], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE,
                                       timeout=30)
                
                stdout = result.stdout.decode('utf-8', errors='replace')
                stderr = result.stderr.decode('utf-8', errors='replace')
                
                print("\nOutput from IronPython script:")
                print("-" * 30)
                print(stdout)
                
                if stderr:
                    print("\nErrors from IronPython script:")
                    print("-" * 30)
                    print(stderr)
                    
                print("-" * 30)
                
            except subprocess.TimeoutExpired:
                print("IronPython script execution timed out")
                
            except Exception as e:
                print(f"Error running IronPython script: {str(e)}")
                
            # Clean up
            if os.path.exists(test_script):
                os.remove(test_script)
                
            break
    else:
        print("Could not find IronPython installation")
    
    print("\nTest completed")
    
if __name__ == "__main__":
    main()