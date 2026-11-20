@echo off

set COMPONENT=%1

echo.
echo ========================================
echo SRAC IMPACT ANALYSIS
echo ========================================
echo.

if /I "%COMPONENT%"=="OpenSSL" (
    echo Component: OpenSSL
    echo.
    echo Impacted Mission Function:
    echo AUTH-CMD-001
    echo.
    echo Authority:
    echo MISSION_OWNER
    echo.
    echo Evidence:
    echo REQ-101
    echo HAZ-22
    echo TEST-15
    goto END
)

if /I "%COMPONENT%"=="CryptoLib" (
    echo Component: NASA CryptoLib
    echo.
    echo Impacted Mission Function:
    echo UPD-VER-002
    echo.
    echo Authority:
    echo MISSION_OWNER
    echo.
    echo Evidence:
    echo REQ-101
    echo TEST-15
    goto END
)

echo No SRAC relationship found.

:END
pause
