@echo off
REM CODESYS REST API Uninstallation Script
SETLOCAL

echo CODESYS REST API Uninstallation
echo ==============================
echo.

REM Check for administrative privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: This script requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    goto :EOF
)

REM Stop the service
echo Stopping CODESYS API service...
python windows_service.py stop
IF %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to stop service. It may already be stopped.
)

REM Uninstall the service
echo Removing Windows service...
python windows_service.py remove
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to remove Windows service.
    goto :EOF
)

REM Delete temporary directories
echo Cleaning up files...
IF EXIST requests (
    rmdir /S /Q requests
)
IF EXIST results (
    rmdir /S /Q results
)

REM Success
echo.
echo Uninstallation completed successfully!
echo.
echo The CODESYS API server has been removed as a Windows service.
echo If you wish to completely remove the application, you can now
echo delete this directory.
echo.

ENDLOCAL