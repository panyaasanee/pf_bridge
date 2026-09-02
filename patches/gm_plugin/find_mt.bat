@echo off
REM ===========================================================================
REM find_mt.bat -- locate the Windows SDK manifest tool, or fail loudly saying
REM where it looked.  Sets MT in the CALLER's environment (no setlocal here,
REM on purpose) and returns 1 when it finds nothing.
REM
REM   call find_mt.bat
REM   if %errorlevel% neq 0 exit /b 1     (NOT `if errorlevel 1`: that is a
REM                                        signed >= test and misses a crash)
REM   "%MT%" ...
REM
REM WHY IT IS ITS OWN FILE.  Two scripts need it -- build_vs2008.bat embeds the
REM manifest with it, install.bat reads the embedded one back out before
REM copying -- and a search this fiddly, copied twice, drifts.  The one thing
REM worse than not finding mt.exe is two scripts disagreeing about whether it
REM is there.
REM
REM WHY IT SEARCHES AT ALL, instead of a path in a comment (COO-DECISION
REM 2026-09-02T19:48+07:00: "find mt.exe without hardcoding a path -- look in
REM both the Windows SDK and VC\bin -- and if it is not there, FAIL LOUDLY
REM saying where you looked").  On the machine that measured this (ka1-A,
REM attended R304) it was NOT on the VC9 path, NOT in VC\bin, and NOT under
REM "Program Files (x86)" -- it was under plain "Program Files", at
REM   C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe
REM One machine, one version.  Nothing here assumes that layout.
REM
REM NOT ONE PARENTHESISED BLOCK BELOW, and that is a bug fix rather than a
REM style: `%ProgramFiles(x86)%` expands to a path containing `)`, and an
REM UNQUOTED one of those inside an `if (...)` block closes the block early --
REM cmd then runs the rest of the message as commands.  The report has to name
REM that folder, so this uses labels instead of blocks.
REM ===========================================================================
set "MT="
set "SDK64=%ProgramFiles%\Microsoft SDKs\Windows"
set "SDK32=%ProgramFiles(x86)%\Microsoft SDKs\Windows"

for /f "delims=" %%I in ('where mt.exe 2^>nul') do if not defined MT set "MT=%%I"
if not defined MT if defined WindowsSdkDir if exist "%WindowsSdkDir%bin\mt.exe" set "MT=%WindowsSdkDir%bin\mt.exe"
if defined MT goto found
if not exist "%SDK64%" goto try_sdk32
for /f "delims=" %%I in ('dir /b /s "%SDK64%\mt.exe" 2^>nul') do if not defined MT set "MT=%%I"
:try_sdk32
if defined MT goto found
if not exist "%SDK32%" goto try_vcbin
for /f "delims=" %%I in ('dir /b /s "%SDK32%\mt.exe" 2^>nul') do if not defined MT set "MT=%%I"
:try_vcbin
if not defined MT if defined VCINSTALLDIR if exist "%VCINSTALLDIR%bin\mt.exe" set "MT=%VCINSTALLDIR%bin\mt.exe"
if defined MT goto found

echo [FAIL] mt.exe (the Windows SDK manifest tool) was not found.
echo.
echo        Looked in, in this order:
echo          1. PATH (where mt.exe)
echo          2. %WindowsSdkDir%bin\mt.exe
echo          3. %SDK64%\ (recursive)
echo          4. %SDK32%\ (recursive)
echo          5. %VCINSTALLDIR%bin\mt.exe
echo        A line that still shows a %%NAME%% spelling above means that
echo        variable is not set on this machine, which is itself the answer
echo        for that line -- cmd leaves an undefined %%VAR%% as literal text
echo        rather than blanking it.
echo.
echo        On the machine that measured this it was at
echo          C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe
echo        If yours is somewhere else, put its folder on PATH and re-run.
exit /b 1

:found
echo [ok] mt.exe: %MT%
exit /b 0
