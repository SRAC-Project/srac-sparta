@echo off

echo ========================================
echo TEST 1 - OpenSSL
echo ========================================
call 04-run-impact-analysis.bat OpenSSL

echo.
echo ========================================
echo TEST 2 - NASA CryptoLib
echo ========================================
call 04-run-impact-analysis.bat CryptoLib

echo.
echo ========================================
echo TEST 3 - Logging Service
echo ========================================
call 04-run-impact-analysis.bat "Logging Service"

echo.
echo ========================================
echo ALL TESTS COMPLETED
echo ========================================

pause