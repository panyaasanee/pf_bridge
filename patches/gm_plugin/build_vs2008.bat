@echo off
REM ===========================================================================
REM build_vs2008.bat -- build GameMaster.dll on the bridge machine.
REM
REM Target: x86, /MD. VS2008 (VC9) is preferred but NO LONGER REQUIRED: since
REM revision 2 the plug-in calls MSVCP90's exported wstring constructor instead
REM of inlining one from this compiler's headers, so our own std layout and
REM _SECURE_SCL setting no longer matter. /MD is still preferred so we share
REM the client's CRT by default.
REM
REM Run from a "Visual Studio 2008 Command Prompt", or just run this file: it
REM calls vcvars32.bat itself when VS90COMNTOOLS is set.
REM
REM To change build options WITHOUT editing the source (the README's A/B needs
REM this -- revision 1 documented rebuild flags that no one could actually
REM pass):
REM   set EXTRA_DEFS=/D PF_GM_KEY=L\"GMUI_BASIC\"
REM   set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=0
REM Then ALWAYS compare the SHA256 printed at the end against the previous
REM build. If it is unchanged, your flag did not reach the compiler and you are
REM about to re-test an identical DLL.
REM ===========================================================================
setlocal

if not "%VCINSTALLDIR%"=="" goto have_env
if "%VS90COMNTOOLS%"=="" (
  echo [FAIL] No VC environment. Open a "Visual Studio 2008 Command Prompt",
  echo        or set VS90COMNTOOLS to ...\Microsoft Visual Studio 9.0\Common7\Tools\
  exit /b 1
)
call "%VS90COMNTOOLS%..\..\VC\bin\vcvars32.bat"
if errorlevel 1 (
  echo [FAIL] vcvars32.bat did not initialise.
  exit /b 1
)
:have_env

if exist GameMaster.dll del /q GameMaster.dll
if exist GameMaster.obj del /q GameMaster.obj
if exist GameMaster.lib del /q GameMaster.lib
if exist GameMaster.exp del /q GameMaster.exp
if exist exports.txt    del /q exports.txt
if exist disasm.txt     del /q disasm.txt

echo.
echo === compiling and linking ===
echo EXTRA_DEFS=%EXTRA_DEFS%
cl /nologo /LD /MD /O2 /W4 /WX /EHsc ^
   /D WIN32 /D _WINDOWS /D NDEBUG /D _CRT_SECURE_NO_WARNINGS %EXTRA_DEFS% ^
   GameMaster.cpp ^
   /link /DEF:GameMaster.def /OUT:GameMaster.dll /MACHINE:X86
if errorlevel 1 (
  echo.
  echo [FAIL] build failed -- nothing to install.
  exit /b 1
)

REM ---------------------------------------------------------------------------
REM Check 1: the export name.
REM
REM A decorated name is the nastiest failure this project can produce: the
REM client's GetProcAddress returns NULL, GM-IMG-002 installs the 4-byte
REM fallback, and the result is observationally IDENTICAL to the six-day-old
REM bug -- button visible, click silent. Revision 1 "checked" this with
REM   findstr /i "CreateGameMaster"
REM which is a substring match, so it passed on _CreateGameMaster and on
REM CreateGameMaster@0: it green-lit precisely the failure it advertised
REM catching. Reject the decorations explicitly instead.
REM ---------------------------------------------------------------------------
echo.
echo === check 1/3: export name ===
dumpbin /nologo /exports GameMaster.dll > exports.txt
findstr /c:"_CreateGameMaster" exports.txt >nul
if not errorlevel 1 (
  echo [FAIL] exported as _CreateGameMaster -- leading underscore. GetProcAddress will miss it.
  exit /b 1
)
findstr /c:"CreateGameMaster@" exports.txt >nul
if not errorlevel 1 (
  echo [FAIL] exported with an @n stdcall decoration. GetProcAddress will miss it.
  exit /b 1
)
findstr /r /c:"[ ]CreateGameMaster$" exports.txt >nul
if errorlevel 1 (
  echo [FAIL] no export named exactly CreateGameMaster.
  exit /b 1
)
echo [ok] exported as exactly CreateGameMaster

REM ---------------------------------------------------------------------------
REM Check 2: CRT dependencies. Revision 1 printed a [WARN] here and then
REM printed [OK] anyway, which is not a check. A wrong CRT crashes at shutdown,
REM far from its cause; MSVCP90 must be present too, or our wstring ctor
REM resolution has nothing to bind to.
REM ---------------------------------------------------------------------------
echo.
echo === check 2/3: CRT dependencies ===
dumpbin /nologo /dependents GameMaster.dll | findstr /i "MSVCR90" >nul
if errorlevel 1 (
  echo [FAIL] MSVCR90.dll is not a dependency -- this is not a /MD VC9 build.
  exit /b 1
)
echo [ok] MSVCR90.dll present
dumpbin /nologo /dependents GameMaster.dll | findstr /i "MSVCP90" >nul
if errorlevel 1 (
  echo [WARN] MSVCP90.dll is not a dependency. Not fatal -- we resolve its
  echo        wstring ctor dynamically -- but confirm the client itself loads it,
  echo        or slots +0x00/+0x08 will skip construction. The plug-in prints
  echo        which of the two it did; read the debug output.
) else (
  echo [ok] MSVCP90.dll present
)

REM ---------------------------------------------------------------------------
REM Check 3: the vtable ABI. This is the only static evidence about THIS DLL
REM that can exist before it touches a live process, and revision 1 skipped it
REM while verifying two things that were easier. The three slots must clean 8,
REM 0 and 4 bytes of stack respectively [GM-IMG-012, -006, -014].
REM ---------------------------------------------------------------------------
echo.
echo === check 3/3: thiscall epilogues (expect ret 8, ret, ret 4) ===
dumpbin /nologo /disasm GameMaster.dll > disasm.txt
findstr /r /c:"ret[ ]*8$" disasm.txt >nul
if errorlevel 1 (
  echo [FAIL] no 'ret 8' found -- slot +0x00 does not clean two stack args.
  exit /b 1
)
findstr /r /c:"ret[ ]*4$" disasm.txt >nul
if errorlevel 1 (
  echo [FAIL] no 'ret 4' found -- slot +0x08 does not clean one stack arg.
  exit /b 1
)
echo [ok] ret 8 and ret 4 present
echo      Eyeball the three vtable slots by hand once, in disasm.txt: they must
echo      appear in declaration order and slot +0x04 must be a bare ret.

echo.
echo === sha256 (RECORD THIS, and compare it against your previous build) ===
certutil -hashfile GameMaster.dll SHA256

echo.
echo [OK] GameMaster.dll built and statically checked.
echo      Install with install.bat -- do NOT copy by hand: install.bat refuses
echo      to overwrite an existing GameMaster.dll, which would destroy a file
echo      nobody in this project has ever been able to obtain.
endlocal
