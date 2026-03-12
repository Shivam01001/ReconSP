@echo off
echo [!] ReconSP Python Environment Setup
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed. Please install it from python.org
    exit /b 1
)

echo [+] Installing dependencies...
pip install -r requirements_py.txt

echo.
echo [+] Setup complete! 
echo [+] You can now run the tool using:
echo     python reconsp.py -u example.com -d 1
pause
