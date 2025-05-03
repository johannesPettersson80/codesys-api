# CODESYS API Debugging Guide

This guide provides step-by-step instructions for troubleshooting connection issues with the CODESYS API HTTP server.

## Quick Start Debugging

1. **Verify CODESYS Path**
   ```
   python debug_codesys_path.py
   ```
   This confirms that the CODESYS executable can be found at the configured path.

2. **Test HTTP Server Only (No CODESYS)**
   ```
   run_test_server.bat
   ```
   This starts a simplified HTTP server that responds to API requests without connecting to CODESYS.
   Test with: `python example_client.py` in another window.

3. **Run Full Server**
   ```
   run_server.bat
   ```
   This starts the complete HTTP server that connects to CODESYS.
   Test with: `python example_client.py` in another window.

## Detailed Debugging Steps

If you're experiencing connection issues, follow these steps:

### 1. Check CODESYS Installation

Verify that CODESYS is correctly installed and that the path in `HTTP_SERVER.py` matches your installation:

```python
CODESYS_PATH = r"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe"
```

You can modify this path if your installation is different.

### 2. Check Permissions

Ensure that:
- The script has permission to execute CODESYS
- The temporary directories can be created and written to
- No firewalls are blocking HTTP connections

### 3. Test HTTP Functionality

Run the test server to isolate HTTP issues from CODESYS issues:
```
run_test_server.bat
```

In another command prompt, run:
```
python example_client.py
```

If this works, the issue is with CODESYS integration, not HTTP functionality.

### 4. Check Logs

Enable detailed logging in `HTTP_SERVER.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='codesys_api_server.log'
)
```

Then check the log file after running the server.

### 5. Common Issues and Solutions

#### "Connection aborted" / "RemoteDisconnected" Errors

**Cause**: The server is terminating connections unexpectedly.
**Solutions**:
- Increase timeout values in `HTTP_SERVER.py`
- Check if CODESYS is running correctly
- Verify script execution permissions

#### CODESYS Not Starting

**Cause**: Unable to start CODESYS process.
**Solutions**:
- Check the CODESYS path
- Run CODESYS manually to verify it works
- Check for permissions issues

#### Script Execution Timeouts

**Cause**: Scripts take too long to execute.
**Solution**: Increase the timeout value:
```python
# In HTTP_SERVER.py
SCRIPT_EXECUTION_TIMEOUT = 120  # seconds
```

## Advanced Debugging

For more detailed debugging:

```
debug.bat
```

This will present a menu with additional debugging options:
1. Check CODESYS path
2. Run HTTP server with debugging
3. Run test server
4. Full system test

## Getting Help

If you continue to experience issues after following these steps, please:
1. Collect all log files
2. Note the exact error messages
3. Document which debugging steps you've tried
4. Create a detailed issue in the GitHub repository