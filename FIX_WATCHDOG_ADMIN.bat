@echo off
rem Right-click this file -> Run as administrator.
rem Applies the PF_Bridge_Watchdog settings that need elevation.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0fix_watchdog_admin.ps1"
echo.
echo Log written to: outbox\902_fix_watchdog_admin.out.txt
pause
