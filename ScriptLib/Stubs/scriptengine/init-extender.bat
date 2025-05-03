@echo off
rem ----------------------------------------------------
rem   Appends the __init__-extension.py to __init__.py
rem ----------------------------------------------------

set START_DIR=%cd%
set THIS_DIR=%~dp0%
set PACKAGE_NAME=%1

cd /D %THIS_DIR%
echo. THIS_DIR=%THIS_DIR%

if exist __init__.py                goto target_exists
echo. "File __init__.py not found in current directory!"
exit 1

:target_exists
if exist __init__-extension.py      goto source_exists
echo. "File __init__-extension.py not found in current directory!"
exit 1

:source_exists
echo.>>                                        __init__.py
echo #>>                                       __init__.py
echo # Module "%PACKAGE_NAME%">>               __init__.py
echo #>>                                       __init__.py
copy /b __init__.py + __init__-extension.py    __init__.py
echo.>>                                        __init__.py

cd /D %START_DIR%

del /F %THIS_DIR%\__init__-extension.py
del /F %THIS_DIR%\init-extender.bat
