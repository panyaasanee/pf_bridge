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
REM   set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=1   (revision 3 default is 0)
REM Then ALWAYS compare the SHA256 printed at the end against the previous
REM build. If it is unchanged, your flag did not reach the compiler and you are
REM about to re-test an identical DLL.
REM ===========================================================================
setlocal
REM Operate on THIS script's folder, not the caller's cwd, so a forgotten cd
REM cannot make us build or check some other GameMaster.dll.
pushd "%~dp0"

REM ---------------------------------------------------------------------------
REM EVERY GATE BELOW IS `if %errorlevel% neq 0`, NEVER `if errorlevel 1`, and
REM revision 5 converted all of them (pf-adversary, round `hj2cry`, D10).
REM `if errorlevel 1` is a signed GREATER-THAN-OR-EQUAL test, so it is FALSE
REM for a negative exit code -- and a tool launched from a folder that is not
REM on PATH is exactly how you get one: `STATUS_DLL_NOT_FOUND` is
REM -1073741515 and an access violation is -1073741819. `find_mt.bat` finds
REM mt.exe in the SDK folder without putting that folder on PATH, so a crashed
REM mt.exe would have printed `[ok] manifest embedded`, then `[ok] RT_MANIFEST
REM #2 reads back out`, then `[OK] built and statically checked` -- and handed
REM the operator the unloadable DLL this whole revision exists to prevent,
REM through the checks added to prevent it.
REM ---------------------------------------------------------------------------

if not "%VCINSTALLDIR%"=="" goto have_env
if "%VS90COMNTOOLS%"=="" (
  echo [FAIL] No VC environment. Open a "Visual Studio 2008 Command Prompt",
  echo        or set VS90COMNTOOLS to ...\Microsoft Visual Studio 9.0\Common7\Tools\
  exit /b 1
)
call "%VS90COMNTOOLS%..\..\VC\bin\vcvars32.bat"
if %errorlevel% neq 0 (
  echo [FAIL] vcvars32.bat did not initialise.
  exit /b 1
)
:have_env

REM !! REFUSE TO DELETE A GameMaster.dll THIS FOLDER DID NOT BUILD.
REM
REM pf-adversary (round `hj2cry`, D16) named the asymmetry: `install.bat`
REM spends its whole header refusing to overwrite a GameMaster.dll because it
REM might be the original plug-in "nobody in this project has ever been able to
REM obtain" -- and this script, in the same directory, deleted one on sight.
REM If the original is ever recovered and dropped in here to be disassembled,
REM the next build destroys it, and a failed build destroys the previous good
REM DLL as a bonus.
REM
REM THE TEST IS THE .obj, not a guess: a successful build of this script leaves
REM GameMaster.obj beside GameMaster.dll and never cleans up afterwards, so a
REM .dll with no .obj beside it did not come out of a build in this folder.
REM False alarms (you deleted the .obj by hand) cost one `del GameMaster.dll`
REM typed deliberately, which is the point.
if not exist GameMaster.dll goto no_stale_dll
if exist GameMaster.obj goto stale_dll_is_ours
echo [STOP] A GameMaster.dll is here with no GameMaster.obj beside it, so it
echo        did not come out of a build in this folder. This script deletes
echo        GameMaster.dll before compiling, and if that file is the ORIGINAL
echo        plug-in the deletion is not recoverable -- RE-164 still wants to
echo        disassemble it.
echo.
echo        Its SHA256:
certutil -hashfile GameMaster.dll SHA256
echo.
echo        Move it somewhere safe (or delete it yourself if you know what it
echo        is), then re-run. Nothing has been changed.
exit /b 1
:stale_dll_is_ours
del /q GameMaster.dll
:no_stale_dll
if exist GameMaster.obj del /q GameMaster.obj
if exist GameMaster.lib del /q GameMaster.lib
if exist GameMaster.exp del /q GameMaster.exp
if exist exports.txt    del /q exports.txt
if exist disasm.txt     del /q disasm.txt
if exist headers.txt    del /q headers.txt
REM Revision 5: the linker's manifest is deleted with the rest, and that is a
REM SAFETY step, not tidiness. The embed below takes whatever
REM GameMaster.dll.manifest is sitting here; a stale one left by an earlier
REM build would be embedded into a new DLL without a word, and the result
REM loads -- against the wrong CRT assembly. Deleting it first means the embed
REM either finds THIS build's manifest or fails loudly.
if exist GameMaster.dll.manifest del /q GameMaster.dll.manifest

echo.
echo === compiling and linking ===
echo EXTRA_DEFS=%EXTRA_DEFS%
REM /W4 without /WX on purpose: VC9's own Platform SDK headers emit W4-level
REM warnings (C4201 nameless struct/union among them), so /WX would abort the
REM build over a warning in Microsoft's headers, on a machine that cannot
REM iterate quickly. Read the warnings; do not let them stop the build.
cl /nologo /LD /MD /O2 /W4 /EHsc ^
   /D WIN32 /D _WINDOWS /D NDEBUG /D _CRT_SECURE_NO_WARNINGS %EXTRA_DEFS% ^
   GameMaster.cpp ^
   /link /DEF:GameMaster.def /OUT:GameMaster.dll /MACHINE:X86
if %errorlevel% neq 0 (
  echo.
  echo [FAIL] build failed -- nothing to install.
  exit /b 1
)

REM ===========================================================================
REM Revision 5, the step whose absence made every DLL this script produced
REM UNLOADABLE: embed the linker's manifest as RT_MANIFEST #2.
REM
REM MEASURED, NOT REASONED (ka1-A, attended round R304, 2026-09-02 ~19:20,
REM letter `notes_to_chief/20260902_1920_KA1A-TO-LANE-GM-build_vs2008-produces-
REM a-dll-the-loader-refuses-add-the-mt-exe-step.md`): this script's own output,
REM all three checks [ok], had NO .rsrc section and no embedded manifest, while
REM importing MSVCR90.dll. Windows answers LoadLibraryW with 14001 for that
REM combination and NOTHING in the plug-in runs -- indistinguishable on screen
REM from the bug the plug-in exists to fix. One `mt.exe` command turned the same
REM DLL into one that loaded, ran, and opened the GM window.
REM
REM THE EMBED RUNS BEFORE THE CHECKS BELOW, on purpose: adding a resource
REM changes the file, and every check -- the export table, the dependents, the
REM disassembly, the SHA256 the installer compares against -- must describe the
REM image that will actually be installed, not the one that existed for a
REM moment before the embed.
REM
REM NOT HARDCODED, because mt.exe is not where a reader expects. It is NOT on
REM the VC9 path (vcvars32.bat does not add the SDK bin), NOT in VC\bin on the
REM machine that measured this, and NOT under "Program Files (x86)" there --
REM it was under plain "Program Files". So this searches, in order, and NAMES
REM EVERY PLACE IT LOOKED if it comes up empty.
REM
REM AND IT FAILS LOUDLY. COO-DECISION 2026-09-02T19:48+07:00: "if it cannot be
REM found, fail loudly and say where you looked -- never fail quietly and let
REM an unloadable DLL out." A build that skipped this step and printed [OK]
REM would cost a whole attended round before the game is even started.
REM ===========================================================================
echo.
echo === embedding the manifest (RT_MANIFEST #2) ===

if not exist GameMaster.dll.manifest (
  echo [FAIL] the linker produced no GameMaster.dll.manifest beside the DLL.
  echo        A /MD VC9 link always writes one, so this is not a "nothing to
  echo        embed" case -- something is wrong with the link step above.
  echo        Refusing to ship a DLL that imports MSVCR90 with no manifest:
  echo        LoadLibraryW would answer 14001 and no plug-in code would run.
  exit /b 1
)

REM The search lives in `find_mt.bat` -- install.bat needs the same one to
REM read the embedded manifest back out before it copies anything, and a
REM search this fiddly, copied twice, drifts.  It sets MT or fails loudly
REM naming every place it looked.
call "%~dp0find_mt.bat"
if %errorlevel% neq 0 (
  echo.
  echo        THIS IS FATAL HERE: the DLL above imports MSVCR90.dll and has no
  echo        embedded manifest, so Windows would refuse to load it with error
  echo        14001 and nothing in the plug-in would ever run. That failure
  echo        looks EXACTLY like the bug this plug-in fixes, so this script
  echo        stops instead of handing you one. Do NOT hand-copy the DLL out
  echo        of here.
  exit /b 1
)

"%MT%" -nologo -manifest GameMaster.dll.manifest -outputresource:GameMaster.dll;#2
if %errorlevel% neq 0 (
  echo [FAIL] mt.exe could not embed the manifest ^(exit code above^).
  echo        Nothing is installable from this build. A common cause is the
  echo        DLL being open in another process ^(the game, DebugView holding a
  echo        handle, an antivirus scan^): close it and re-run.
  exit /b 1
)
echo [ok] manifest embedded

REM ---------------------------------------------------------------------------
REM Check 0: the embed is real, read back out of the SHIPPED IMAGE.
REM
REM `mt.exe` exiting 0 is not the claim that matters -- "the resource is in the
REM file" is.  This check reads the built DLL itself.
REM
REM !! THE HARD GATE IS THE `.rsrc` SECTION, NOT THE mt.exe READ-BACK, and the
REM difference is which of the two anybody has actually run (pf-adversary,
REM round `hj2cry`, D11).  ka1-A's measurement names the failing state
REM precisely: the unloadable 13,824-byte DLL had **no .rsrc section at all**,
REM and the embed took it to 14,848.  `dumpbin` is already this script's tool
REM and is in the same VC installation the compile step needs, so the gate
REM rests on a measured state and a tool that is certainly present.
REM
REM The mt.exe read-back below it is the STRICTER question -- an RT_MANIFEST at
REM id #2 specifically, which is the id a DLL's activation context comes from
REM -- and it is deliberately ADVISORY, because `mt.exe -inputresource:...
REM -validate_manifest` has never been run on this project's SDK build
REM (version 5.2.3790.2075).  Making an unrun invocation a hard gate risks the
REM opposite failure: refusing a GOOD build on the one machine we have any
REM evidence about, which costs the same attended round from the other side.
REM Whoever runs this first: point check 0 at ka1-A's known-bad DLL
REM (sha256 67501F7E...F496) once and see it go red -- that promotes the
REM advisory to a gate, and until then it is a warning that names itself.
REM
REM WHAT `.rsrc` DOES NOT PROVE, said plainly: it proves the image has A
REM resource directory, not that the resource is a manifest at id #2.  For
REM THIS DLL that gap is narrow (GameMaster.cpp declares no resources of any
REM kind, so the only thing that can put an .rsrc here is the embed above),
REM and the two lines below close the rest of it between them.
REM ---------------------------------------------------------------------------
echo.
echo === check 0/4: the manifest is really in the image ===
dumpbin /nologo /headers GameMaster.dll > headers.txt
findstr /c:".rsrc" headers.txt >nul
if %errorlevel% neq 0 (
  echo [FAIL] GameMaster.dll has no .rsrc section, so nothing was embedded --
  echo        this is byte-for-byte the state ka1-A measured on the build that
  echo        Windows refused with 14001. mt.exe may have reported success
  echo        above; the image says otherwise, and the image is what ships.
  exit /b 1
)
echo [ok] .rsrc section present (it was ABSENT on the unloadable build)
"%MT%" -nologo -inputresource:GameMaster.dll;#2 -validate_manifest
if %errorlevel% neq 0 (
  echo [warn] mt.exe could not read RT_MANIFEST #2 back out of the DLL.
  echo        TWO CAUSES ARE POSSIBLE AND THIS SCRIPT CANNOT TELL THEM APART:
  echo          ^(a^) the manifest really is not at id #2 -- the DLL will fail
  echo              to load with 14001; or
  echo          ^(b^) this mt.exe build does not accept -inputresource with
  echo              -validate_manifest. Nobody has run that combination.
  echo        The .rsrc gate above passed, so this is NOT treated as fatal.
  echo        Settle it before booting the game, with the tool that measured
  echo        the fix in the first place:
  echo          py -3 -m pirateforce_foundation.gm.plugin_image_check --dll ...
  echo        and report which cause it was, so this line can become a gate.
) else (
  echo [ok] RT_MANIFEST #2 reads back out of the built DLL
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
echo === check 1/4: export name ===
dumpbin /nologo /exports GameMaster.dll > exports.txt

REM One word-boundary test does all three jobs, and survives either output
REM format dumpbin may use (a bare "CreateGameMaster" column, or the
REM "CreateGameMaster = _CreateGameMaster" form some versions print for a
REM .def-renamed export -- the exported token still matches there):
REM   _CreateGameMaster    -> '_' is a word character, so \< does not match
REM   CreateGameMaster@0   -> \> does not match before '@'
REM   CreateGameMaster     -> matches
REM An earlier revision used a plain substring match here, which passed on both
REM decorated spellings: it green-lit the exact failure it existed to catch.
findstr /r /c:"\<CreateGameMaster\>" exports.txt >nul
if %errorlevel% neq 0 (
  echo [FAIL] no export named exactly CreateGameMaster.
  echo        GetProcAddress would return NULL and the client would silently
  echo        keep its own fallback -- indistinguishable on screen from the bug
  echo        this plug-in exists to fix. Export table was:
  type exports.txt
  exit /b 1
)
echo [ok] exported as exactly CreateGameMaster
echo      (read these lines yourself once, do not just trust the check:)
findstr /i "CreateGameMaster" exports.txt

REM ---------------------------------------------------------------------------
REM Check 2: CRT dependency. Revision 1 printed a [WARN] here and then printed
REM [OK] anyway, which is not a check. A wrong CRT crashes at shutdown, far
REM from its cause, so the MSVCR90 half below is a real FAIL.
REM
REM The MSVCP90 half is NOT a check and revision 4 stops pretending it is:
REM this DLL includes only <windows.h> and <new> (placement new only, no
REM import), and catch(...) pulls __CxxFrameHandler3 from MSVCR90, so the
REM built image NEVER depends on MSVCP90 and the warning below is permanent.
REM It also would not mean what it said: we bind to the CLIENT's msvcp90
REM instance, not to ours. It is printed as information, not as a gate.
REM ---------------------------------------------------------------------------
echo.
echo === check 2/4: CRT dependencies ===
dumpbin /nologo /dependents GameMaster.dll | findstr /i "MSVCR90" >nul
if %errorlevel% neq 0 (
  echo [FAIL] MSVCR90.dll is not a dependency -- this is not a /MD VC9 build.
  exit /b 1
)
echo [ok] MSVCR90.dll present
dumpbin /nologo /dependents GameMaster.dll | findstr /i "MSVCP90" >nul
if %errorlevel% neq 0 (
  echo [info] MSVCP90.dll is not a dependency of THIS DLL, which is expected
  echo        and not a finding: we resolve the wstring ctor inside the
  echo        CLIENT's own msvcp90 instance at run time. What matters is the
  echo        [GM_PLUGIN] 'msvcp90 wstring ctor:' line in DebugView, which is
  echo        printed at the first CreateGameMaster call, not at load.
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
echo === check 3/4: thiscall epilogues (expect ret 8, ret, ret 4) ===
dumpbin /nologo /disasm GameMaster.dll > disasm.txt
findstr /r /c:"ret[ ]*8$" disasm.txt >nul
if %errorlevel% neq 0 (
  echo [FAIL] no 'ret 8' found -- slot +0x00 does not clean two stack args.
  exit /b 1
)
findstr /r /c:"ret[ ]*4$" disasm.txt >nul
if %errorlevel% neq 0 (
  echo [FAIL] no 'ret 4' found -- slot +0x08 does not clean one stack arg.
  exit /b 1
)
echo [ok] ret 8 and ret 4 present
echo      Eyeball the three vtable slots by hand once, in disasm.txt: they must
echo      appear in declaration order and slot +0x04 must be a bare ret.

echo.
echo === EXTRA_DEFS this build actually saw ===
echo      EXTRA_DEFS=%EXTRA_DEFS%
echo      Empty here means cell 1.  If you meant cell 2 or 3 and this is
echo      empty, the flag did NOT reach the compiler - stop and set it.

echo.
echo === sha256 (RECORD THIS; it is NOT a flag-arrival check) ===
echo      The DLL embeds __DATE__/__TIME__ and the PE header carries a
echo      link timestamp, so EVERY rebuild changes this hash whether or
echo      not your flag arrived.  Record it to prove the INSTALLED file is
echo      this build (plugin_image_check compares them).  The real control
echo      that the flag arrived is the line above plus the [GM_PLUGIN]
echo      'key=' and 'slot +0x00 +4 init:' lines in DebugView.
certutil -hashfile GameMaster.dll SHA256

echo.
echo [OK] GameMaster.dll built and statically checked.
echo      Install with install.bat -- do NOT copy by hand: install.bat refuses
echo      to overwrite an existing GameMaster.dll, which would destroy a file
echo      nobody in this project has ever been able to obtain.
echo.
echo === next step 0, BEFORE booting the game (pirate-force-server checkout) ===
echo      set PYTHONPATH=src
echo      py -3 -m pirateforce_foundation.gm.plugin_image_check --dll "%CD%\GameMaster.dll" --client-dir "^<client folder^>"
echo      It names every file-level failure at once (missing / not_pe /
echo      wrong_machine / no_exports / export_decorated / manifest_missing ...)
echo      and exit code 0 also means the INSTALLED file is this build, byte for
echo      byte.  One attended round: do not spend it discovering these one at a
echo      time.
endlocal
