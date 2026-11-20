@echo off

echo 1. Create Demo Data
echo 2. Generate SBOM
echo 3. Load SRAC
echo 4. Run Impact Analysis
echo 5. Run All Tests

set /p choice=Enter choice:

if "%choice%"=="1" goto DATA
if "%choice%"=="2" goto SBOM
if "%choice%"=="3" goto SRAC
if "%choice%"=="4" goto IMPACT
if "%choice%"=="5" goto TESTS

goto END

:DATA
echo Creating Demo Data...
goto END

:SBOM
echo Generating SBOM...
goto END

:SRAC
echo Loading SRAC...
goto END

:IMPACT
echo Running Impact Analysis...
goto END

:TESTS
echo Running Tests...
goto END

:END
pause
