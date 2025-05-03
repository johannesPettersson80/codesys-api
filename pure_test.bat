@echo off
echo Testing CODESYS Script Execution with pure command line
echo.

REM Create a minimal test script
echo import sys > test.py
echo print("Script test running") >> test.py
echo print("Python version:", sys.version) >> test.py
echo print("Arguments:", sys.argv) >> test.py

echo Running CODESYS with explicit script path and quotes...
"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe" --runscript="%CD%\test.py" --scriptargs:"test_arg"

echo.
echo If CODESYS started but nothing else happened, then there may be permissions issues
echo or configuration issues with script execution in your CODESYS installation.
echo.
echo Press any key to exit...
pause > nul