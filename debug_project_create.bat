@echo off
echo CODESYS API Debug Project Creation
echo ==================================
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

REM Run the debug project creation script
echo.
echo Starting debug script...
echo This will create a log file with detailed information.
echo.
python debug_project_creation.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo Debug completed successfully!
) else (
    echo.
    echo Debug completed with errors. Check the log file for details.
)

echo.
echo A detailed log has been saved to: debug_project_creation.log
echo.
echo Press any key to exit...
pause >nul