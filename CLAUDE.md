# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CODESYS REST API wrapper that provides HTTP endpoints for interacting with CODESYS automation software. The system maintains a persistent CODESYS session and exposes RESTful API endpoints for project management, POU operations, and script execution.

## Development Commands

### Starting the Server
- **Main server**: `python HTTP_SERVER.py` or `run_server.bat`
- **Test server** (no CODESYS): `python test_server.py` or `run_test_server.bat`
- **Debug mode**: Use `simple_test.bat` for interactive debugging and testing

### Testing
- **Example client**: `python example_client.py` (demonstrates full workflow)
- **Simple API client**: `python simple_api_client.py`
- **Debug scripts**: `python simplified_debug.py` (comprehensive diagnostics)

### Installation
- **Install as service**: `install.bat` (requires admin privileges)
- **Start manually**: `start_server.bat`
- **Uninstall service**: `uninstall.bat`

## Architecture

### Core Components

1. **HTTP_SERVER.py** - Main HTTP server (Python 3)
   - REST API endpoints (`/api/v1/`)
   - Authentication with API keys
   - CODESYS process management
   - Request/response handling

2. **PERSISTENT_SESSION.py** - CODESYS script runner (Python 2.7/IronPython)
   - Runs inside CODESYS environment
   - Maintains persistent session state
   - Executes CODESYS operations via scriptengine module
   - File-based communication with HTTP server

### Communication Pattern
- HTTP server writes request files to `requests/` directory
- PERSISTENT_SESSION.py monitors requests and processes them
- Results written to `results/` directory
- HTTP server reads results and returns to client

### Key Directories
- `requests/` - Incoming API requests (JSON files)
- `results/` - Operation results (JSON files)
- `ScriptLib/Stubs/scriptengine/` - CODESYS API type stubs and documentation

## Python Version Compatibility

- **HTTP_SERVER.py**: Python 3.x only
- **PERSISTENT_SESSION.py**: Python 2.7/IronPython (CODESYS requirement)
- **Client scripts**: Python 3.x compatible
- **Test/debug scripts**: Python 3.x

## Configuration

### Server Settings (HTTP_SERVER.py:44-47)
```python
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
CODESYS_PATH = r"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe"
```

### API Keys
- Stored in `api_keys.json`
- Default key: "admin"
- Header format: `Authorization: ApiKey YOUR_API_KEY`

## API Endpoints Structure

All endpoints prefixed with `/api/v1/`:

- **Session**: `/session/{start,stop,status,restart}`
- **Project**: `/project/{create,open,save,close,compile,list}`
- **POU**: `/pou/{create,code,list}`
- **Script**: `/script/execute`
- **System**: `/system/{info,logs}`

## Development Notes

### When Adding New Endpoints
1. Add handler in `HTTP_SERVER.py` route_request method
2. Add corresponding operation in `PERSISTENT_SESSION.py`
3. Update API documentation in README.md
4. Test with both `example_client.py` and direct HTTP calls

### CODESYS Script Development
- Use Python 2.7 syntax in PERSISTENT_SESSION.py
- Import `scriptengine` module for CODESYS operations
- Reference type stubs in `ScriptLib/Stubs/scriptengine/` for API documentation
- Test scripts with `debug_codesys_path.py` before integration

### File Communication Protocol
- Request files: UUID-named JSON files in `requests/`
- Result files: Corresponding UUID-named JSON files in `results/`
- Status tracking via `session_status.json`
- Termination via `terminate.signal` file

### Error Handling
- Server logs to `codesys_api_server.log`
- Session logs to `session.log`
- Use timeout of 120 seconds for script execution
- Check directory permissions before file operations