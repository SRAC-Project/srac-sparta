@echo off
setlocal
set "PYTHONUTF8=1"
set "SRAC_ARGS="
pushd "%~dp0"
if not defined SRAC_PYTHON goto AUTO
set "SRAC_COMMAND=%SRAC_PYTHON%"
goto DISPATCH
:AUTO
where py >nul 2>nul
if errorlevel 1 goto TRY_PYTHON
set "SRAC_COMMAND=py"
set "SRAC_ARGS=-3"
goto DISPATCH
:TRY_PYTHON
where python >nul 2>nul
if errorlevel 1 goto NO_PYTHON
set "SRAC_COMMAND=python"
:DISPATCH
if /I "%~1"=="test" goto TEST
if /I "%~1"=="cve" goto LOOKUP
if /I "%~1"=="impact" goto LOOKUP
echo Usage: prototype.bat impact "Component Name" [--output-dir PATH]
echo        prototype.bat cve CVE-2026-1234 [--output-dir PATH]
echo        prototype.bat test
set "SRAC_EXIT=2"
goto DONE
:LOOKUP
"%SRAC_COMMAND%" %SRAC_ARGS% impact-analysis.py "%~2" %3 %4 %5 %6 %7 %8 %9
set "SRAC_EXIT=%ERRORLEVEL%"
goto DONE
:TEST
"%SRAC_COMMAND%" %SRAC_ARGS% -m unittest discover -s tests -v
set "SRAC_EXIT=%ERRORLEVEL%"
goto DONE
:NO_PYTHON
echo Python 3 is required. Install Python or set SRAC_PYTHON to its executable.
set "SRAC_EXIT=2"
:DONE
popd
exit /b %SRAC_EXIT%

