# CODESYS Script Compatibility

This document explains the Python compatibility requirements for scripts that run inside CODESYS.

## CODESYS IronPython Environment

CODESYS uses IronPython for its scripting environment. This means any script that runs directly inside CODESYS must maintain compatibility with this environment.

## Python Version Compatibility

The CODESYS API implementation uses the following approach:

1. **PERSISTENT_SESSION.py**: This script runs directly inside CODESYS and must maintain compatibility with the CODESYS IronPython environment.
2. **Other Components**: All other components (HTTP server, Windows service, client) require Python 3.x.

## Key CODESYS Script Syntax Requirements

When modifying the PERSISTENT_SESSION.py script, be aware of these syntax requirements:

1. **Exception Handling**:
   - Use the syntax: `except Exception, e:`

2. **Print Statements**:
   - Use the syntax: `print "Hello"`

3. **String Handling**:
   - Be aware that IronPython handles strings differently than modern Python

4. **Division Operator**:
   - Integer division: `5 / 2` results in `2`

## Guidelines for Maintaining PERSISTENT_SESSION.py

When making changes to the PERSISTENT_SESSION.py script:

1. Always maintain compatibility with the CODESYS IronPython environment
2. Test the script in the CODESYS environment
3. Avoid using modern Python features not supported by CODESYS
4. Remember that IronPython might have some limitations compared to CPython

## Testing PERSISTENT_SESSION.py

To test changes to PERSISTENT_SESSION.py:

1. Make your modifications
2. Run the script in CODESYS using the script execution feature
3. Verify that your script executes correctly without syntax errors
4. Test the functionality through the HTTP API

## Further Information

For more information on CODESYS scripting, refer to the CODESYS documentation on scripting and automation.