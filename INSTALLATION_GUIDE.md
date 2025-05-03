# CODESYS REST API Installation Guide

This document provides detailed instructions for installing and setting up the CODESYS REST API wrapper service.

## Prerequisites

- Windows Operating System (Windows 10 or Windows Server 2016+)
- CODESYS 3.5 or later installed
- Python 3.x installed
  - Note: Only the script that runs inside CODESYS maintains Python 2.7 compatibility
  - All other server and client code requires Python 3.x
- Administrator privileges on the target system

## Required Python packages

The following Python packages are required:

```
pip install requests pywin32
```

## Installation Steps

### 1. Download and Extract Files

1. Download the CODESYS REST API package
2. Extract the contents to a directory of your choice (e.g., `C:\CODESYS-API`)

### 2. Configure the API Server

1. Open `HTTP_SERVER.py` in a text editor
2. Update the `CODESYS_PATH` variable to point to your CODESYS installation:
   ```python
   CODESYS_PATH = r"C:\Program Files\CODESYS 3.5\CODESYS\CODESYS.exe"  # Update this path
   ```
3. Optionally, change the `SERVER_HOST` and `SERVER_PORT` variables if you need the server to listen on a different interface or port
4. Save the changes

### 3. Set Up API Keys

By default, the system uses a single API key `admin`. For production use, you should create your own API keys:

1. Delete the `api_keys.json` file if it exists
2. The system will create a default API key on first run
3. To create additional keys or change the default key, modify the `api_keys.json` file:
   ```json
   {
     "your_api_key": {"name": "Your Key Name", "created": 1620000000.0}
   }
   ```

### 3. Install as a Windows Service

#### Using the Installation Script

The simplest way to install is to use the provided installation script:

```
install.bat
```

If you prefer not to install as a Windows service, you can simply run:
```
start_server.bat
```

#### Manual Service Installation

Alternatively, you can install the service manually:

1. Open a Command Prompt with Administrator privileges
2. Navigate to the directory where you extracted the files
3. Run the following command:
   ```
   python windows_service.py install
   ```
4. Start the service:
   ```
   python windows_service.py start
   ```

The service will now start automatically when the system boots.

### 4. Test the Installation

1. Open a Command Prompt or PowerShell window
2. Use curl or a similar tool to make a request to the API:
   ```
   curl -H "Authorization: ApiKey admin" http://localhost:8080/api/v1/system/info
   ```
3. If the API is functioning correctly, you should receive a JSON response with system information

Alternatively, you can use the provided example client script:

```
python example_client.py
```

## Running Manually (Without Service)

If you prefer to run the API server manually without installing it as a service:

1. Open a Command Prompt
2. Navigate to the directory where you extracted the files
3. Run the following command:
   ```
   python HTTP_SERVER.py
   ```
   
   Or use the provided script:
   ```
   start_server.bat
   ```
4. The server will start and display a message indicating it's running

Press Ctrl+C to stop the server when running manually.

## Directory Structure

The API server creates and uses the following directories:

- `requests/`: Directory for inter-process communication request files
- `results/`: Directory for inter-process communication result files
- Logs are stored in the root directory:
  - `codesys_api_server.log`: Main API server log
  - `session.log`: CODESYS session log
  - `codesys_api_service.log`: Windows service log (if running as a service)

## Troubleshooting

### Service Fails to Start

1. Check the `codesys_api_service.log` file for error messages
2. Verify the path to CODESYS.exe is correct in the server file (`HTTP_SERVER.py` or `HTTP_SERVER_PY3.py`)
3. Ensure all required Python packages are installed
4. Check Windows Event Viewer for service-related errors
5. Make sure you're using the correct Python version (2.7 or 3.x) with the appropriate scripts
6. If using Python 3.x, ensure you're using `windows_service_py3.py` instead of `windows_service.py`

### API Returns Errors

1. Check the `codesys_api_server.log` file for API server errors
2. Check the `session.log` file for CODESYS session errors
3. Verify CODESYS is installed and working correctly
4. Try running the server manually to see any console output
5. For Python 3.x compatibility issues, make sure you're using the correct version of files:
   - Use `HTTP_SERVER_PY3.py` instead of `HTTP_SERVER.py`
   - Use `example_client_py3.py` instead of `example_client.py`

### Authentication Issues

1. Verify you are using the correct API key in the Authorization header
2. Check the `api_keys.json` file to ensure your key is listed
3. Restart the API server after making changes to the API keys

## Uninstallation

To remove the Windows service:

1. Open a Command Prompt with Administrator privileges
2. Navigate to the directory where you extracted the files
3. Stop the service:
   ```
   python windows_service.py stop
   ```
4. Remove the service:
   ```
   python windows_service.py remove
   ```
   Or use the provided script:
   ```
   uninstall.bat
   ```

5. Delete the directory containing the API server files

## Security Considerations

- The API server does not use HTTPS by default. For production use, consider setting up a reverse proxy with HTTPS or implementing HTTPS support.
- API keys are stored in plain text. Ensure the `api_keys.json` file has appropriate file permissions.
- Consider running the service under a dedicated user account with minimal privileges.
- Review firewall settings to restrict access to the API server port.

## Updating

When updating to a new version:

1. Stop the service:
   ```
   python windows_service.py stop
   ```
2. Replace the files with the new version
3. Start the service:
   ```
   python windows_service.py start
   ```

## Additional Configuration

### Changing the Port

To change the port number:

1. Edit `HTTP_SERVER.py`
2. Change the `SERVER_PORT` variable to your preferred port
3. Restart the service

### Logging Configuration

To change logging settings:

1. Edit `HTTP_SERVER.py`
2. Modify the logging configuration at the top of the file
3. Restart the service

### Rate Limiting

Rate limiting is not implemented by default. Consider using a reverse proxy like Nginx or Apache for rate limiting in production environments.

## Python Version Compatibility

### Python Version Requirements

This API wrapper requires Python 3.x for all components except the script that runs inside CODESYS:

1. **CODESYS Internal Scripts**: The `PERSISTENT_SESSION.py` script maintains Python 2.7 compatibility to match CODESYS's IronPython 2.7 environment.
2. **Server Components**: All server components (HTTP server, Windows service) require Python 3.x.
3. **Client Components**: All client components require Python 3.x.

The project initially supported both Python 2.7 and 3.x, but has been consolidated to only support Python 3.x for simplicity and better maintainability.