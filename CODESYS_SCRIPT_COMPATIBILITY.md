# CODESYS Script Compatibility

This document explains the Python compatibility requirements for scripts that run inside CODESYS.

## CODESYS IronPython Environment

CODESYS uses IronPython 2.7 for its scripting environment. This means any script that runs directly inside CODESYS must use Python 2.7 syntax.

## Python Version Compatibility

The CODESYS API implementation uses the following approach:

1. **PERSISTENT_SESSION.py**: This script runs directly inside CODESYS and must use Python 2.7 syntax.
2. **Other Components**: All other components (HTTP server, Windows service, client) are written for Python 3.x.

## Key Differences Between Python 2.7 and 3.x

When modifying the PERSISTENT_SESSION.py script, be aware of these key syntax differences:

1. **Exception Handling**:
   - Python 2.7: `except Exception, e:`
   - Python 3.x: `except Exception as e:`

2. **Print Statements**:
   - Python 2.7: `print "Hello"` 
   - Python 3.x: `print("Hello")`

3. **String and Bytes Handling**:
   - Python 2.7 doesn't distinguish between strings and bytes
   - Python 3.x has explicit distinction between strings (unicode) and bytes

4. **Division Operator**:
   - Python 2.7: `5 / 2` results in `2` (integer division)
   - Python 3.x: `5 / 2` results in `2.5` (float division)

## Guidelines for Maintaining PERSISTENT_SESSION.py

When making changes to the PERSISTENT_SESSION.py script:

1. Always maintain Python 2.7 compatibility
2. Test the script in the CODESYS environment
3. Avoid using Python 3.x specific features or syntax
4. Remember that IronPython might have some limitations compared to CPython

## Testing PERSISTENT_SESSION.py

To test changes to PERSISTENT_SESSION.py:

1. Make your modifications
2. Run the script in CODESYS using the script execution feature
3. Verify that your script executes correctly without syntax errors
4. Test the functionality through the HTTP API

## Further Information

For more information on CODESYS scripting, refer to the CODESYS documentation on scripting and automation.