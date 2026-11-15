@echo off
REM Double-click or run from cmd. Extra args are passed through, e.g.:
REM   build_windows.bat -Target portable
REM   build_windows.bat -InstallDeps
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_windows.ps1" %*
if errorlevel 1 (
  echo.
  echo Build failed.
)
pause
