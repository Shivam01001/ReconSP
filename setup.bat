@echo off
setlocal

:: ReconSP - Windows Setup Script
:: Requirements: Go installed (https://go.dev/dl/)

echo [+] Checking Go Installation...
where go.exe >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Go NOT FOUND. Please install Go from https://go.dev/dl/
    pause
    exit /b 1
)

echo [+] Initializing Go project dependencies...
go mod tidy

echo [+] Building ReconSP for Windows...
go build -o reconsp.exe ./cmd/reconsp.go

if %errorlevel% neq 0 (
    echo [!] Build FAILED! Please check error messages above.
    pause
    exit /b 1
)

echo [✔] Build SUCCESSFUL!
echo [!] To use all features, ensure subfinder, httpx, and nuclei are in your PATH.
echo [!] Download from: https://github.com/projectdiscovery/

echo.
echo Run: .\reconsp.exe -u example.com -d 1
pause
