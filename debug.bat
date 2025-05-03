@echo off
REM CODESYS API Debug Batch File
SETLOCAL EnableDelayedExpansion

echo CODESYS API Debugging Tools
echo ==========================
echo.

REM Parse command line arguments
set DEBUG_MODE=%1
if "%DEBUG_MODE%"=="" set DEBUG_MODE=full

if /i "%DEBUG_MODE%"=="path" goto :debug_path
if /i "%DEBUG_MODE%"=="server" goto :debug_server
if /i "%DEBUG_MODE%"=="test" goto :debug_test
if /i "%DEBUG_MODE%"=="full" goto :debug_full

:debug_help
echo Usage: debug.bat [option]
echo.
echo Options:
echo   path   - Verify CODESYS executable path only
echo   server - Run debug server only
echo   test   - Run test server only
echo   full   - Run all debugging tools (default)
echo.
goto :end

:debug_path
echo === CHECKING CODESYS PATH ===
python debug_codesys_path.py
goto :end

:debug_server
echo === RUNNING DEBUG SERVER ===
echo CODESYS API server will start with debug output.
echo Press Ctrl+C to stop the server.
echo.
python debug_server.py
goto :end

:debug_test
echo === RUNNING TEST SERVER ===
echo Simple test server without CODESYS integration will start.
echo Press Ctrl+C to stop the server.
echo.
python test_server.py
goto :end

:debug_full
echo === FULL DEBUGGING SEQUENCE ===
echo.
echo Step 1: Checking CODESYS path
python debug_codesys_path.py
echo.
echo Press any key to continue to Step 2...
pause > nul

echo.
echo Step 2: Running test server (no CODESYS integration)
echo Press Ctrl+C after testing to continue...
start "CODESYS API Test Server" cmd /c "python test_server.py & pause"
echo.
echo Server is running in another window.
echo You can test it with: python example_client.py
echo.
echo Press any key to continue to Step 3...
pause > nul

echo.
echo Step 3: Running debug server (with CODESYS integration)
echo Press Ctrl+C to stop the server and exit debugging.
echo.
python debug_server.py

:end
ENDLOCAL