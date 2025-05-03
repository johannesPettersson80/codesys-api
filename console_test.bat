@echo off
echo Testing CODESYS Script Execution in console mode
echo.

REM Create a minimal test script
echo import sys > console_test.py
echo print("Script test running") >> console_test.py
echo print("Python version:", sys.version) >> console_test.py
echo print("Arguments:", sys.argv) >> console_test.py

echo Running CODESYS with --noUI to see console output...
"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe" --runscript="%CD%\console_test.py" --noUI

echo.
echo If you saw any output above, the script executed.
echo If nothing appeared, there may be issues with script execution.
echo.
echo Press any key to exit...
pause > nul