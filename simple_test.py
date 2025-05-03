"""
Simple CODESYS script test that shows a visible dialog

This script attempts to create a visible dialog in CODESYS to verify
script execution is working properly.
"""

# Try multiple methods to show a message box since different CODESYS versions
# might have different APIs

try:
    # First, try to print to stdout (this goes to console)
    print("TEST SCRIPT STARTED")
    
    # Try scriptengine method (3S CODESYS standard API)
    try:
        import scriptengine
        system = scriptengine.System()
        system.ui.info("Message from test script", "INFO")
        print("Displayed dialog using scriptengine.System UI")
    except Exception as e:
        print("Error using scriptengine.System UI:", str(e))
    
    # Try .NET MessageBox as a fallback
    try:
        import clr
        clr.AddReference("System.Windows.Forms")
        from System.Windows.Forms import MessageBox
        MessageBox.Show("Test message from Python script", "CODESYS Script Test")
        print("Displayed dialog using System.Windows.Forms.MessageBox")
    except Exception as e:
        print("Error using MessageBox:", str(e))
    
    # Try scriptengine.MessageBox if available
    try:
        from scriptengine import MessageBox
        MessageBox.Show("Test message from Python script", "CODESYS Script Test")
        print("Displayed dialog using scriptengine.MessageBox")
    except Exception as e:
        print("Error using scriptengine.MessageBox:", str(e))
    
    print("TEST SCRIPT COMPLETED")
    
except Exception as ex:
    print("GLOBAL ERROR:", str(ex))