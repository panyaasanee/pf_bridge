@echo off
rem ===========================================================================
rem Right-click this file -> Run as administrator.
rem
rem WHY THIS FILE EXISTS: SETUP_GIT_SYNC.bat failed at 2026-08-20 19:14 in two
rem places at once. (1) Register-ScheduledTask rejected the trigger XML because
rem RepetitionDuration was TimeSpan.MaxValue, which serialises to
rem P99999999DT23H59M59S and Task Scheduler refuses it. (2) The schtasks
rem fallback passed its arguments from PowerShell as an array, and the -File
rem path broke at the space in "Pirate Force" - the error names the fragment
rem 'Force\pf_bridge\pf_git_sync.ps1'.
rem
rem This file avoids both by NOT using PowerShell to register anything. The
rem schtasks line below is copied from SETUP_BRIDGE_AUTOSTART.bat, which
rem registered PF_Bridge_Watchdog with the same space in the same path and has
rem worked for days. /SC MINUTE /MO 5 also repeats indefinitely with no
rem duration value at all, so bug (1) cannot come back.
rem
rem The task is created as the logged-on user on purpose: git push needs the
rem credentials Windows Credential Manager stores in Panya's profile. A task
rem running as SYSTEM would have none of them and every push would fail.
rem ===========================================================================

echo === STEP 1: register the task (schtasks, cmd quoting) ===
schtasks /Create /F /TN "PF_Git_Sync" /SC MINUTE /MO 5 /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"C:\Users\Panya\Desktop\Pirate Force\pf_bridge\pf_git_sync.ps1\""

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo STEP 1 FAILED to register the task. Nothing else was attempted.
    echo If it says access denied, right-click this file - Run as administrator.
    pause
    exit /b 1
)
echo STEP 1 OK

echo.
echo === STEP 2: apply settings that need elevation ===
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0fix_git_sync_settings.ps1"

echo.
echo ===========================================================================
echo Read the VERDICT line above. PASS means the task is installed and set.
echo This file did NOT run the sync even once - nothing has been pulled or
echo pushed yet. To watch the first run by hand:  schtasks /Run /TN PF_Git_Sync
echo ===========================================================================
pause
