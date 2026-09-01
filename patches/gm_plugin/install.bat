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

if "%~1"=="" (
  echo Usage: install.bat "C:\path\to\client\folder"
  echo        ^(the folder containing the client executable^)
  exit /b 1
)

set "TARGET=%~1"

if not exist "%TARGET%\" (
  echo [FAIL] not a folder: %TARGET%
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
  echo         %TARGET%\GameMaster.dll
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

copy /y "GameMaster.dll" "%TARGET%\GameMaster.dll" >nul
if errorlevel 1 (
  echo [FAIL] copy failed. Check permissions on %TARGET%
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
