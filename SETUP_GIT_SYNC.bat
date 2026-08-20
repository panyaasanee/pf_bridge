@echo off
rem Right-click this file -> Run as administrator.
rem One-time install of the PF_Git_Sync scheduled task: every 5 minutes,
rem plus catch-up triggers at logon and at screen-unlock. WakeToRun is left
rem OFF on purpose (opposite of PF_Bridge_Watchdog) - see the header comment
rem in setup_git_sync_admin.ps1 for why. Requested by Panya, 2026-08-20.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_git_sync_admin.ps1"
set RC=%ERRORLEVEL%
echo.
if %RC% EQU 0 (
    echo SUCCESS: PF_Git_Sync installed and verified - VERDICT=PASS in the log below.
) else (
    echo FAILED: verification did not pass, or the script could not run.
    echo Read the log below before assuming the task is safe. If it says
    echo NOT ELEVATED, right-click this file and choose "Run as administrator".
)
echo.
echo Log written to: pf_bridge\outbox\SETUP_GIT_SYNC.out.txt
pause
