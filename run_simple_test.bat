@echo off
echo Testing CODESYS Script Execution
echo This will launch CODESYS with a simple test script that should display a dialog
echo.
echo Press any key to continue...
pause > nul

echo Starting CODESYS with the test script...
"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe" -script simple_test.py

echo.
echo Did you see a dialog box? If not, script execution isn't working properly.
echo Press any key to exit...
pause > nul