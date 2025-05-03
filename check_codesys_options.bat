@echo off
echo Checking CODESYS command line options
echo.

echo Attempting to run CODESYS with /? to see help
"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe" /?

echo.
echo If no help was displayed, trying with -help
"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe" -help

echo.
echo If no help was displayed, the correct command line options might be different
echo Press any key to continue...
pause