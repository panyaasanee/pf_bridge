@echo off
REM ===========================================================================
REM install.bat -- put GameMaster.dll next to the game client, refusing to
REM destroy anything.
REM
REM   install.bat "C:\path\to\client\folder"
REM
REM WHY THIS EXISTS RATHER THAN "just copy the file next to the exe":
REM
REM The owner's ruling is that the original plug-in never existed on our side.
REM That ruling is unpinned -- no repository artifact records it -- and this
REM lane's own most recent pinned note (notes_to_chief/20260901_2132_RE-164-
REM RESULT-...) says only that a bridge inventory did not FIND the file, and
REM explicitly nonclaims that it is truly absent. PF_GM_PLUGIN_GATE.md:14 flags
REM that same inventory as possibly stale.
REM
REM If the ruling is right, this script costs one extra keystroke.
REM If the inventory was stale, a plain copy would answer a "replace the
REM existing file?" prompt for you and permanently destroy a binary this
REM project spent 27 Aug - 1 Sep failing to obtain and has never disassembled.
REM Those outcomes are not symmetric, so this script never overwrites.
REM ===========================================================================
setlocal
REM Resolve GameMaster.dll relative to THIS script, never to the caller's cwd:
REM run from the repo root, a cwd-relative name could make the overwrite guard
REM inspect one file and the copy take another.
pushd "%~dp0"

if "%~1"=="" (
  echo Usage: install.bat "C:\path\to\client\folder"
  echo        ^(the folder containing the client executable^)
  exit /b 1
)

set "TARGET=%~1"

REM !! EVERY `%TARGET%` INSIDE A PARENTHESISED BLOCK BELOW IS QUOTED, and it
REM is a bug fix, not a style (pf-adversary, round `hj2cry`, D9).  Percent
REM expansion runs BEFORE parenthesis tokenising, so an unquoted
REM `C:\Program Files (x86)\PirateForce` puts a bare `)` inside the block and
REM closes it early: cmd then runs `\PirateForce` as a command and falls out
REM to the next line -- which in the second block is `exit /b 1`, i.e. an
REM unconditional `[STOP] a GameMaster.dll ALREADY EXISTS` about a folder that
REM has none.  The client is very plausibly installed under a path with
REM parentheses, so this was reachable on the first real use.
if not exist "%TARGET%\" (
  echo [FAIL] not a folder: "%TARGET%"
  exit /b 1
)

if not exist "GameMaster.dll" (
  echo [FAIL] GameMaster.dll not built yet. Run build_vs2008.bat first.
  exit /b 1
)

if exist "%TARGET%\GameMaster.dll" (
  echo.
  echo [STOP] A GameMaster.dll ALREADY EXISTS in the target folder.
  echo.
  echo         "%TARGET%\GameMaster.dll"
  echo.
  echo Nothing has been changed. This is important: if that file is the
  echo original plug-in, it is the artifact this project has been unable to
  echo obtain since 27 Aug, and overwriting it is not recoverable.
  echo.
  echo Its SHA256:
  certutil -hashfile "%TARGET%\GameMaster.dll" SHA256
  echo.
  echo Do this instead:
  echo   1. copy that file somewhere safe, outside the client folder;
  echo   2. report its SHA256 and size to chief/COO -- it changes the whole
  echo      premise of this work and RE-164 wants to disassemble it;
  echo   3. only then decide whether to install ours.
  exit /b 1
)

REM ===========================================================================
REM Revision 2: DO NOT INSTALL A DLL WINDOWS WILL NOT LOAD.
REM
REM COO-DECISION 2026-09-02T19:48+07:00 asked this script to "carry everything
REM the DLL needs, not the .dll on its own".  Measured answer, and it is worth
REM stating plainly because it is not what the phrasing suggests: once the
REM manifest is EMBEDDED (build_vs2008.bat revision 5), the .dll on its own IS
REM everything -- ka1-A's attended R304 loaded and ran exactly one file in the
REM client folder, with the CRT resolved out of the client's own side-by-side
REM assembly.  So this script does not gain a second file to copy.  What it
REM gains is a check that the ONE file is complete.
REM
REM WHY THAT IS THE FILE-COMPLETENESS PROBLEM AND NOT A SUBSTITUTE FOR IT: the
REM failure being prevented is precisely "a needed piece is missing when the
REM loader looks".  Before revision 5 that piece was a manifest sitting beside
REM the DLL, unread by anyone; the fix put it INSIDE the image.  A DLL built by
REM an older copy of the build script -- or by a build that stopped before the
REM embed -- still has the hole, and it is invisible: 13,824 bytes, all the old
REM checks [ok], and LoadLibraryW answers 14001 with no message on screen.
REM
REM !! IT RUNS **BELOW** THE [STOP] GUARD, and revision 2's first draft had it
REM above (pf-adversary, round `hj2cry`, D12).  The highest-value output this
REM script has is "there is ALREADY a GameMaster.dll in that folder" -- the
REM artifact this project has failed to obtain since 27 Aug.  A tool check
REM placed above it would swallow that discovery on exactly the machine most
REM likely to lack the tool: the GAME PC, which is not the build machine.
REM
REM !! AND A MISSING TOOL IS A WARNING, NOT A REFUSAL, for the same reason.
REM `dumpbin` ships with VC, not with the game.  Refusing to install a
REM verified-good DLL because the client machine has no compiler costs the
REM same attended round as installing a bad one -- so the two cases are split:
REM the tool SAYS the manifest is missing => refuse; the tool is ABSENT => say
REM so loudly and continue.  `build_vs2008.bat` gates hard on the machine that
REM has the tool, which is where the gate belongs.
REM
REM WHY `dumpbin` AND NOT `mt.exe` HERE: `mt.exe -inputresource:...;#2
REM -validate_manifest` has never been run by anyone on this project, so a
REM refusal built on it could be refusing a good file (pf-adversary D11).  The
REM `.rsrc` section IS measured: ka1-A's unloadable DLL had none.
REM
REM ~~a plain `GameMaster.dll.manifest` copied beside the DLL~~ -- NOT DONE,
REM and stated rather than silently skipped: an external manifest beside a DLL
REM is not what the loader read on the machine that measured this, and nobody
REM in this project has measured whether it would be read at all.  Copying an
REM extra file into the owner's client folder on an unmeasured guess is the
REM kind of change this script's whole design refuses to make.  Asked back in
REM `notes_to_chief/20260902_2038_LANE-GM-TO-COO-mt-exe-step-landed-and-the-
REM file-install-bat-does-not-copy.md`.
REM ===========================================================================
set "DUMPBIN="
for /f "delims=" %%I in ('where dumpbin 2^>nul') do if not defined DUMPBIN set "DUMPBIN=%%I"
if defined DUMPBIN goto have_dumpbin

echo [warn] dumpbin is not on PATH, so this script cannot look inside
echo        GameMaster.dll before copying it. That check is NOT the gate --
echo        build_vs2008.bat gates hard on the machine that builds the file --
echo        but it does mean nothing here has verified this particular file.
echo        If this DLL was built by build_vs2008.bat revision 5 or later, it
echo        was checked there. If you are not sure, stop and rebuild.
goto do_copy

:have_dumpbin
"%DUMPBIN%" /nologo /headers "GameMaster.dll" > "%TEMP%\pf_gm_headers.txt"
findstr /c:".rsrc" "%TEMP%\pf_gm_headers.txt" >nul
if %errorlevel% neq 0 (
  echo.
  echo [FAIL] GameMaster.dll has no .rsrc section, so it carries no embedded
  echo        manifest. Windows would answer LoadLibraryW with 14001 and no
  echo        plug-in code would ever run -- button visible, click silent,
  echo        exactly like the bug this plug-in exists to fix.
  echo        Nothing was copied. Rebuild with build_vs2008.bat, which embeds
  echo        the manifest and re-reads the image before it prints [OK].
  del /q "%TEMP%\pf_gm_headers.txt" 2>nul
  exit /b 1
)
del /q "%TEMP%\pf_gm_headers.txt" 2>nul
echo [ok] the file about to be copied carries an embedded resource

:do_copy
copy /y "GameMaster.dll" "%TARGET%\GameMaster.dll" >nul
if %errorlevel% neq 0 (
  echo [FAIL] copy failed. Check permissions on "%TARGET%"
  exit /b 1
)

echo [OK] installed: %TARGET%\GameMaster.dll
certutil -hashfile "%TARGET%\GameMaster.dll" SHA256
echo.
echo Rollback: delete that one file. Nothing else on the machine was touched --
echo no client byte was patched, no registry key written. The client then
echo returns to the fallback path it is on today [GM-IMG-002].
echo.
echo Before testing, attach a debug-output viewer (DebugView, or a debugger).
echo The plug-in prints [GM_PLUGIN] lines at load naming the build timestamp,
echo whether it found the client CRT, whether it resolved the wstring ctor, and
echo which key it will return. Without those lines you cannot tell "our DLL ran
echo and the key was wrong" from "our DLL never loaded" -- and those two look
echo identical on screen.
endlocal
