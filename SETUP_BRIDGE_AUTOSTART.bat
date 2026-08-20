@echo off
rem One-time setup: register PF Bridge watchdog in Task Scheduler.
rem After this, the bridge starts itself and revives itself every 5 minutes.
rem You never need to open START_PF_BRIDGE.bat manually again.

schtasks /Create /F /TN "PF_Bridge_Watchdog" /SC MINUTE /MO 5 /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"C:\Users\Panya\Desktop\Pirate Force\pf_bridge\pf_bridge_watchdog.ps1\""

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo FAILED to register task. Try right-click this file - Run as administrator.
    pause
    exit /b 1
)

schtasks /Run /TN "PF_Bridge_Watchdog"

echo.
echo Done! Bridge watchdog registered (checks every 5 minutes, starts bridge hidden if missing).
echo Log file: pf_bridge\watchdog.log
pause
