@echo off
REM CODESYS REST API Installation Script
SETLOCAL EnableDelayedExpansion

echo CODESYS REST API Installation
echo ============================
echo.

REM Check for administrative privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: This script requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    goto :EOF
)

REM Check for Python installation
python --version 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 2.7 and try again.
    goto :EOF
)

REM Check Python version
python -c "import sys; print('Good' if sys.version_info[0] == 2 else 'Bad')" > temp.txt
SET /p PYTHON_VERSION=<temp.txt
DEL temp.txt
IF "%PYTHON_VERSION%" NEQ "Good" (
    echo WARNING: You are using Python 3.x. This may not be compatible with CODESYS API.
    echo          The CODESYS scripting environment uses Python 2.7.
    echo.
    set /p CONTINUE=Do you want to continue anyway? [Y/N]: 
    IF /I "!CONTINUE!" NEQ "Y" goto :EOF
)

REM Install required packages
echo Installing required Python packages...
pip install requests pywin32
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install required packages.
    echo Please check your internet connection and try again.
    goto :EOF
)

REM Create directories
echo Creating directories...
mkdir requests 2>nul
mkdir results 2>nul

REM Check CODESYS path
set CODESYS_PATH="C:\Program Files\CODESYS 3.5\CODESYS\CODESYS.exe"
IF NOT EXIST %CODESYS_PATH% (
    echo WARNING: Default CODESYS path not found: %CODESYS_PATH%
    echo.
    echo You will need to update the CODESYS_PATH variable in HTTP_SERVER.py
    echo to point to your CODESYS installation.
    echo.
)

REM Install Windows service
echo Installing Windows service...
python windows_service.py install
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install Windows service.
    goto :EOF
)

REM Start the service
echo Starting CODESYS API service...
python windows_service.py start
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to start Windows service.
    goto :EOF
)

REM Success
echo.
echo Installation completed successfully!
echo.
echo CODESYS API server is now running as a Windows service.
echo To test, use the following command in a new command prompt:
echo   curl -H "Authorization: ApiKey admin" http://localhost:8080/api/v1/system/info
echo.
echo Or run the example client:
echo   python example_client.py
echo.
echo For more information, see the INSTALLATION_GUIDE.md file.
echo.

ENDLOCAL