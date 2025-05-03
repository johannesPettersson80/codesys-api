@echo off
REM CODESYS REST API Installation Script (Python 3)
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
    echo Please install Python and try again.
    goto :EOF
)

REM Check Python version
python -c "import sys; print(sys.version_info[0])" > temp.txt
SET /p PYTHON_MAJOR_VERSION=<temp.txt
DEL temp.txt

IF %PYTHON_MAJOR_VERSION% LSS 3 (
    echo ERROR: This script requires Python 3.
    echo You are using Python 2.x.
    echo Please install Python 3 and try again.
    goto :EOF
)

echo Python %PYTHON_MAJOR_VERSION% detected.

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
set DEFAULT_CODESYS_PATH="C:\Program Files\CODESYS 3.5\CODESYS\CODESYS.exe"
IF NOT EXIST %DEFAULT_CODESYS_PATH% (
    echo WARNING: Default CODESYS path not found: %DEFAULT_CODESYS_PATH%
    echo.
    echo Please enter the correct path to CODESYS.exe:
    set /p CUSTOM_PATH=
    
    IF EXIST "!CUSTOM_PATH!" (
        echo Updating CODESYS path in HTTP_SERVER.py...
        REM Using PowerShell to safely handle the path
        powershell -Command "$content = Get-Content -Path 'HTTP_SERVER.py' -Raw; $pattern = 'CODESYS_PATH = r\\\".*\\\"'; $replacement = 'CODESYS_PATH = r\"!CUSTOM_PATH!\"'; $content = $content -replace $pattern, $replacement; Set-Content -Path 'HTTP_SERVER.py' -Value $content;"
    ) ELSE (
        echo WARNING: The specified path does not exist. You will need to manually update
        echo          the CODESYS_PATH variable in HTTP_SERVER.py before using the API.
    )
) ELSE (
    echo CODESYS path found at default location: %DEFAULT_CODESYS_PATH%
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