@echo off
REM Simple Test Batch File for CODESYS API
SETLOCAL EnableDelayedExpansion

echo CODESYS API Simple Test Script
echo =============================
echo.

REM Step 1: Run the simple debug script
echo Running simplified debugger...
python simplified_debug.py
echo.
echo Debugging complete.
echo.

REM Step 2: Prompt for next action
echo What would you like to do next?
echo.
echo 1. Run test server (no CODESYS integration)
echo 2. Run actual HTTP_SERVER
echo 3. Exit
echo.
SET /p CHOICE=Enter choice (1, 2, or 3): 

IF "%CHOICE%"=="1" (
    echo Starting test server...
    echo Use another command window to test with:
    echo curl -H "Authorization: ApiKey admin" http://localhost:8080/api/v1/system/info
    echo.
    echo Press Ctrl+C to stop the server when done.
    python test_server.py
    goto :end
)

IF "%CHOICE%"=="2" (
    echo Starting HTTP server (with CODESYS integration)...
    echo Use another command window to test with:
    echo python example_client.py
    echo.
    echo Press Ctrl+C to stop the server when done.
    python HTTP_SERVER.py
    goto :end
)

:end
ENDLOCAL