@echo off
REM Simple CODESYS REST API Installation Script for Python 3
SETLOCAL EnableDelayedExpansion

echo Simple CODESYS REST API Installation (Python 3)
echo =============================================
echo.

REM Create directories
echo Creating directories...
mkdir requests 2>nul
mkdir results 2>nul

REM Install required packages
echo Installing required Python packages...
pip install requests
echo.

REM Update CODESYS path
echo Please enter the path to your CODESYS.exe:
echo (Example: C:\Program Files\CODESYS 3.5\CODESYS\CODESYS.exe)
set /p CODESYS_PATH=

REM Update the path in the server file
echo Updating CODESYS path in HTTP_SERVER_PY3.py...
powershell -Command "(Get-Content HTTP_SERVER_PY3.py) -replace 'CODESYS_PATH = r\".*\"', 'CODESYS_PATH = r\"%CODESYS_PATH:\=\\%\"' | Set-Content HTTP_SERVER_PY3.py"

echo.
echo Installation completed!
echo.
echo To start the server, run:
echo   python HTTP_SERVER_PY3.py
echo.
echo To test the API, run:
echo   python example_client_py3.py
echo.

ENDLOCAL