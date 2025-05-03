@echo off
echo CODESYS API Project Creation Test
echo ================================
echo.

REM Check Python is available
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)

REM Install required packages if not already installed
echo Checking required packages...
python -c "import requests" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing required packages...
    pip install requests
)

REM Run the project creation test
echo.
echo Starting test...
echo.
python test_project_creation.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo Test completed successfully!
) else (
    echo.
    echo Test failed with error code %ERRORLEVEL%
)

echo.
echo Press any key to exit...
pause >nul