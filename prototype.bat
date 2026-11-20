@echo off

if /I "%1"=="impact" (
    "C:\Users\devashrid\AppData\Local\Programs\Python\Python313\python.exe" impact-analysis.py %2 %3 %4
    goto END
)

if /I "%1"=="cve" (
    "C:\Users\devashrid\AppData\Local\Programs\Python\Python313\python.exe" impact-analysis.py %2
    goto END
)

if /I "%1"=="test" (

    echo ========================================
    echo TEST 1 - OpenSSL
    echo ========================================
    call prototype.bat impact OpenSSL

    echo.

    echo ========================================
    echo TEST 2 - NASA CryptoLib
    echo ========================================
    call prototype.bat impact "NASA CryptoLib"

    echo.

    echo ========================================
    echo TEST 3 - Telemetry Library
    echo ========================================
    call prototype.bat impact "Telemetry Library"

    goto END
)

echo.
echo Usage:
echo.
echo prototype.bat impact OpenSSL
echo prototype.bat impact "NASA CryptoLib"
echo prototype.bat impact "Telemetry Library"
echo prototype.bat test
echo prototype.bat cve CVE-2026-1234

:END
