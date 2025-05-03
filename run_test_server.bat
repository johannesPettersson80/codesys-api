@echo off
echo Starting the test server...
echo This server does NOT connect to CODESYS
echo.
echo Use another command window to test with:
echo curl -H "Authorization: ApiKey admin" http://localhost:8080/api/v1/system/info
echo.
echo Press Ctrl+C to stop the server.
python test_server.py