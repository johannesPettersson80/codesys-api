@echo off
REM CODESYS REST API Installation Script for Python 3
SETLOCAL EnableDelayedExpansion

echo CODESYS REST API Installation (Python 3 Compatible)
echo ==============================================
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
    echo Please install Python and try again.
    goto :EOF
)

REM Check Python version
python -c "import sys; print('Python3' if sys.version_info[0] == 3 else 'Python2')" > temp.txt
SET /p PYTHON_VERSION=<temp.txt
DEL temp.txt
IF "%PYTHON_VERSION%" NEQ "Python3" (
    echo WARNING: You are using Python 2.x. This installation script is for Python 3.x.
    echo          Consider using the standard install.bat for Python 2.7 instead.
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
    echo Please enter the correct path to CODESYS.exe:
    set /p CUSTOM_PATH=
    
    IF EXIST "!CUSTOM_PATH!" (
        echo Updating CODESYS path in HTTP_SERVER_PY3.py...
        REM Use Python to update the file
        python -c "import re; content = open('HTTP_SERVER_PY3.py', 'r').read(); content = re.sub(r'CODESYS_PATH = r\".*\"', 'CODESYS_PATH = r\"!CUSTOM_PATH!\"', content); open('HTTP_SERVER_PY3.py', 'w').write(content)"
    ) ELSE (
        echo WARNING: The specified path does not exist. You will need to manually update
        echo          the CODESYS_PATH variable in HTTP_SERVER_PY3.py before using the API.
    )
)

REM Install Windows service
echo Installing Windows service...
python windows_service_py3.py install
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install Windows service.
    goto :EOF
)

REM Start the service
echo Starting CODESYS API service...
python windows_service_py3.py start
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