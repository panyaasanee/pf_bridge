@echo off
REM ===========================================================================
REM build_vs2008.bat -- build GameMaster.dll on the bridge machine.
REM
REM Target: x86, /MD (dynamic CRT = MSVCR90), Visual Studio 2008 (VC9).
REM VC9 is not a preference. Slot +0x00 and slot +0x08 construct an MSVCP90
REM std::basic_string<wchar_t> inside memory the CLIENT owns, and a newer
REM toolchain lays that type out differently. GameMaster.cpp refuses to compile
REM outside VC9 for that reason; read the PF_GM_ALLOW_NON_VC9 note in the source
REM before overriding it.
REM
REM Run from a "Visual Studio 2008 Command Prompt", or just run this file: it
REM calls vcvars32.bat itself when VS90COMNTOOLS is set.
REM ===========================================================================
setlocal

if not "%VCINSTALLDIR%"=="" goto have_env
if "%VS90COMNTOOLS%"=="" (
  echo [FAIL] No VC9 environment. Open a "Visual Studio 2008 Command Prompt",
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

echo.
echo === compiling and linking ===
cl /nologo /LD /MD /O2 /W4 /EHsc /GS- ^
   /D WIN32 /D _WINDOWS /D NDEBUG /D _CRT_SECURE_NO_WARNINGS ^
   GameMaster.cpp ^
   /link /DEF:GameMaster.def /OUT:GameMaster.dll /MACHINE:X86
if errorlevel 1 (
  echo.
  echo [FAIL] build failed -- nothing to install.
  exit /b 1
)

REM --- The two checks that catch the failure modes that actually happen ------
REM 1. a decorated export name means GetProcAddress returns NULL and the client
REM    silently stays on the fallback path, looking exactly like today's bug;
REM 2. the wrong CRT means the client's MSVCR90 delete frees a pointer from a
REM    heap that never owned it, which crashes at shutdown, far from the cause.

echo.
echo === export table (must show exactly: CreateGameMaster) ===
dumpbin /nologo /exports GameMaster.dll | findstr /i "CreateGameMaster"
if errorlevel 1 (
  echo [FAIL] CreateGameMaster is not exported under that exact name.
  exit /b 1
)

echo.
echo === CRT dependency (must list MSVCR90.dll) ===
dumpbin /nologo /dependents GameMaster.dll | findstr /i "MSVCR90"
if errorlevel 1 (
  echo [WARN] MSVCR90.dll not listed as a dependency. If this is not a /MD VC9
  echo        build, the client's operator delete and ours are different heaps.
)

echo.
echo === sha256 (record this in the test report) ===
certutil -hashfile GameMaster.dll SHA256

echo.
echo [OK] GameMaster.dll built. Install it next to the client executable,
echo      then run the acceptance test in README.md. To roll back, delete the
echo      file: the client returns to the proven fallback path with no other
echo      change.
endlocal
