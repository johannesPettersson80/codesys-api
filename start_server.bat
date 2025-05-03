@echo off
REM Start the CODESYS API server (Python 3 version)
SETLOCAL EnableDelayedExpansion

echo CODESYS API Server Launcher
echo ==========================
echo.

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

REM Check if required files exist
IF NOT EXIST HTTP_SERVER.py (
    echo ERROR: HTTP_SERVER.py not found.
    echo        Please make sure you are in the correct directory.
    goto :EOF
)

REM Check if required directories exist
IF NOT EXIST requests (
    echo Creating requests directory...
    mkdir requests
)

IF NOT EXIST results (
    echo Creating results directory...
    mkdir results
)

echo Starting CODESYS API server...
python HTTP_SERVER.py

ENDLOCAL