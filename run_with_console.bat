@echo off
echo ========================================
echo  Attempting to run Button Wheel.py
echo ========================================
echo.
echo Using Python from PATH environment variable...
echo If this fails, ensure Python is installed and added to PATH,
echo or modify this script with the full path to python.exe.
echo.

REM Execute the Python script
python "Button Wheel.pyw"

REM The "%errorlevel%" variable holds the exit code of the last command
echo.
echo ========================================
echo  Script execution finished.
echo  Exit Code: %errorlevel% 
echo  (0 usually means success, non-zero often indicates an error)
echo ========================================
echo.
echo If the script crashed, error messages should be visible above.
echo Press any key to close this window...
pause >nul