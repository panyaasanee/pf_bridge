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
REM the tool SAYS the manifest is missing == refuse; the tool is ABSENT == say
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
goto pfgm_image_check

:have_dumpbin
REM !! `2>&1`, and the emptiness check below, are a FALSE-RED fix
REM (pf-adversary, round `b8xrod`, M4).  A `dumpbin.exe` that `where` finds on
REM PATH but that runs outside a VS command prompt dies looking for `mspdb*.dll`
REM and says so on STDERR.  With stdout alone redirected, the headers file came
REM out EMPTY, `findstr` failed, and this block then printed
REM `[FAIL] GameMaster.dll has no .rsrc section` -- a failure of the TOOL,
REM reported as a finding about the DLL, refusing a good file permanently while
REM telling the owner to "rebuild", which fails again identically.  The gate
REM itself is unchanged: an image that really has no `.rsrc` still produces
REM headers output and is still refused.
"%DUMPBIN%" /nologo /headers "GameMaster.dll" > "%TEMP%\pf_gm_headers.txt" 2>&1
set "PFGM_HDRSIZE="
for %%S in ("%TEMP%\pf_gm_headers.txt") do set "PFGM_HDRSIZE=%%~zS"
if not defined PFGM_HDRSIZE set "PFGM_HDRSIZE=0"
if "%PFGM_HDRSIZE%"=="0" (
  echo [warn] dumpbin produced no output at all, so it did not read this file.
  echo        That is the tool failing, not a finding about GameMaster.dll --
  echo        the usual cause is dumpbin on PATH outside a VS command prompt,
  echo        which cannot load mspdb80/mspdb100.dll. Nothing here has checked
  echo        the image; continuing to the resource-tree check below.
  del /q "%TEMP%\pf_gm_headers.txt" 2>nul
  goto pfgm_image_check
)
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

REM ===========================================================================
REM Revision 3: RUN the image checker, do not merely recommend it.
REM
REM COO-DECISION 2026-09-02T23:42+07:00 item 3.  Until this revision the only
REM thing between a DLL whose manifest sits at the WRONG resource id and the
REM owner's client folder was a printed suggestion in README.md ("step 0"),
REM which nobody on this project has ever been observed running.
REM
REM `dumpbin /headers` above cannot close that hole, and this is the whole
REM reason revision 3 exists: it sees the `.rsrc` SECTION.  A manifest
REM embedded at `;#1` -- the EXE id, one keystroke from the right command --
REM puts an `.rsrc` section in the image while leaving the DLL exactly as
REM unloadable as one with no manifest at all (14001, silent, button visible,
REM click dead).  `pirateforce_foundation.gm.plugin_image_check` parses the
REM resource tree and requires id 2, so it is the check that decides here.
REM
REM THE THREE BRANCHES, AND WHY THEY ARE NOT ONE BRANCH:
REM
REM   no interpreter, or no checkout of the checker on this machine
REM       -- WARN AND CONTINUE.  Fail-open is explicit in the decision: the
REM          game PC is not the build PC and nobody has measured whether it
REM          has Python.  Refusing a good DLL there costs the same attended
REM          round as installing a bad one, and build_vs2008.bat already gates
REM          hard on the machine that does have the tools.
REM   the checker ran and answered
REM       -- ITS VERDICT DECIDES.  `verdict=image_ok` installs; anything else
REM          refuses and copies nothing (fail-closed).
REM   the checker was found and started, but printed no verdict line
REM       -- WARN AND CONTINUE, in different words from branch 1.
REM          [ASSUMPTION OF LANE-GM - AWAITING COO] the decision does not name
REM          this case.  It is read as "no working tool here" and not as a
REM          finding about the DLL, because a bad DLL cannot reach it: every
REM          parse error inside the checker is caught and turned INTO a
REM          verdict (`PluginImageError` carries one, `inspect_plugin_file`
REM          never lets one escape, and a truncated or non-PE file reports
REM          `not_pe`).  A run with no verdict line is therefore a broken
REM          environment -- a Python 2 `python.exe`, a half-synced checkout --
REM          and never a statement about these bytes.  Asked back in
REM          notes_to_chief/20260903_0034_LANE-GM-ASK-COO-the-checker-that-
REM          starts-and-says-nothing.md.
REM
REM !! WHERE THIS STEP ACTUALLY RUNS, said plainly because the sentence
REM "install.bat now runs the checker" is only true on some machines
REM (pf-adversary, round `b8xrod`, H3).  On the GAME PC -- which this same
REM script says at the top is not the build machine -- there is normally no
REM `pirate-force-server` checkout and no Python, so control reaches
REM `:pfgm_no_tool` and this whole step warns and copies.  It bites on the
REM BRIDGE, where both repositories sit side by side and where a DLL is
REM normally built and installed.  That is a real gap, not a hidden one: it
REM is the price of the fail-open COO-DECISION `20260902_2342` item 3
REM required, and closing it means putting a checker on the game PC, not
REM tightening this branch.  Do not read a clean install on a bare game PC as
REM "the image was checked".
REM
REM !! `--dll` ONLY, NEVER `--client-dir`, AND IT IS LOAD-BEARING.  Control
REM only reaches this line once the [STOP] guard above has proved the target
REM folder holds NO GameMaster.dll, so `--client-dir "%TARGET%"` would report
REM `verdict=missing` and exit 1 EVERY SINGLE TIME -- a permanent refusal to
REM install, on precisely the clean folder an install is for.  The build/
REM install comparison that flag exists for belongs to step 0 AFTER an
REM install, not to the install itself.
REM ===========================================================================
:pfgm_image_check
set "PFGM_SRC="
REM `set PF_SERVER_REPO="C:\..."` is how most people set a path with a space,
REM and the quotes then land INSIDE the value: `if exist "%VAR%\src\..."`
REM becomes a broken token and is false forever, sending a machine that has
REM every tool down the warn-and-copy branch (pf-adversary, round `b8xrod`, L2).
set "PFGM_REPO=%PF_SERVER_REPO%"
if defined PFGM_REPO set "PFGM_REPO=%PFGM_REPO:"=%"
if defined PFGM_REPO if exist "%PFGM_REPO%\src\pirateforce_foundation\gm\plugin_image_check.py" set "PFGM_SRC=%PFGM_REPO%\src"
if not defined PFGM_SRC if exist "%~dp0..\..\..\Pirate Force ServerProject\src\pirateforce_foundation\gm\plugin_image_check.py" set "PFGM_SRC=%~dp0..\..\..\Pirate Force ServerProject\src"
if not defined PFGM_SRC if exist "%~dp0..\..\..\pirate-force-server\src\pirateforce_foundation\gm\plugin_image_check.py" set "PFGM_SRC=%~dp0..\..\..\pirate-force-server\src"
if not defined PFGM_SRC goto pfgm_no_tool

REM A `py` launcher can be installed with no 3.x runtime behind it, and a
REM `python.exe` on PATH can still be a Python 2, which cannot even import
REM this module (`from __future__ import annotations`).  So each candidate is
REM asked to RUN something before it is believed.
set "PFGM_PY="
REM `if %errorlevel%==0`, not `if not errorlevel 1`: the latter means
REM "errorlevel is less than 1", which is TRUE for a negative code -- an
REM interpreter that dies with 0xC0000005 would be believed (round `b8xrod`, L1).
py -3 -c "pass" >nul 2>nul
if %errorlevel%==0 set "PFGM_PY=py -3"
if defined PFGM_PY goto pfgm_run
python -c "import sys; raise SystemExit(0 if sys.version_info[0] == 3 else 1)" >nul 2>nul
if %errorlevel%==0 set "PFGM_PY=python"
if defined PFGM_PY goto pfgm_run
python3 -c "pass" >nul 2>nul
if %errorlevel%==0 set "PFGM_PY=python3"
if not defined PFGM_PY goto pfgm_no_tool

:pfgm_run
set "PFGM_OUT=%TEMP%\pf_gm_image_check.txt"
del /q "%PFGM_OUT%" 2>nul
set "PYTHONPATH=%PFGM_SRC%"
echo [..] plugin_image_check ^(%PFGM_PY%^) is reading the file about to be copied
%PFGM_PY% -m pirateforce_foundation.gm.plugin_image_check --dll "%~dp0GameMaster.dll" > "%PFGM_OUT%" 2>&1
set "PFGM_RC=%errorlevel%"
if exist "%PFGM_OUT%" type "%PFGM_OUT%"
findstr /c:"GM_PLUGIN_IMAGE build verdict=" "%PFGM_OUT%" >nul 2>nul
if errorlevel 1 goto pfgm_no_verdict

REM !! WHICH COPY ANSWERED (pf-adversary, round `b8xrod`, H2).  The module is
REM located by GUESSING FOLDER NAMES above, and any checkout older than round
REM `selrsl` prints `verdict=image_ok` and exits 0 for a manifest embedded at
REM resource id 1 -- the exact shape this gate exists to catch.  The verdict
REM token cannot tell those two copies apart.  The `rules=` line can: the old
REM copy does not print it.  A stale checkout is therefore treated as no tool
REM at all, not as a pass.
findstr /c:"GM_PLUGIN_IMAGE build rules=" "%PFGM_OUT%" >nul 2>nul
if errorlevel 1 goto pfgm_stale_tool
findstr /c:"manifest_id2" "%PFGM_OUT%" >nul 2>nul
if errorlevel 1 goto pfgm_stale_tool
REM Both, not either: the exit code alone can be clobbered by anything that
REM runs between here and the test, and the verdict line alone would miss a
REM future check that fails the run without changing that token.
if not "%PFGM_RC%"=="0" goto pfgm_refuse
findstr /c:"GM_PLUGIN_IMAGE build verdict=image_ok" "%PFGM_OUT%" >nul 2>nul
if errorlevel 1 goto pfgm_refuse
del /q "%PFGM_OUT%" 2>nul
echo [ok] plugin_image_check: verdict=image_ok
echo      NONCLAIM: file-level only, and narrower than it sounds. It does NOT
echo      say the GM window opens (only a person at the screen decides that),
echo      and it does NOT say the manifest at id 2 CONTAINS a usable assembly
echo      reference -- an empty or wrong-version manifest reads image_ok here
echo      and still answers 14001. It says the id is right, not the contents.
goto do_copy

:pfgm_no_tool
echo.
echo [warn] plugin_image_check did NOT run on this machine, so nothing here
echo        has read the resource tree of the file about to be copied.
echo        Reason: no Python 3 on PATH, or no pirate-force-server checkout
echo        found. Looked at %%PF_SERVER_REPO%%\src, then, beside the folder
echo        that holds pf_bridge, "Pirate Force ServerProject\src" and
echo        "pirate-force-server\src".
echo        The .rsrc check above is NOT the same check: a manifest embedded
echo        at resource id 1 leaves an .rsrc section behind and the DLL still
echo        never loads.
echo        If this DLL came from build_vs2008.bat revision 5 or later it was
echo        checked on the build machine. If you are not sure, stop and run
echo        step 0 by hand from the server checkout:
echo            set PYTHONPATH=src
echo            py -3 -m pirateforce_foundation.gm.plugin_image_check --dll "%~dp0GameMaster.dll"
echo        Set PF_SERVER_REPO to that checkout to make this automatic.
goto do_copy

:pfgm_no_verdict
echo.
echo [warn] plugin_image_check started but printed no verdict line, so it has
echo        neither passed nor failed this file. Its output is above.
echo        That is a broken tool environment -- a Python 2 interpreter, a
echo        half-synced checkout -- and never a finding about these bytes: the
echo        checker turns every parse error into a verdict instead of raising,
echo        so a bad DLL cannot land here.
echo        Continuing, for the same reason a missing interpreter continues.
if exist "%PFGM_OUT%" del /q "%PFGM_OUT%" 2>nul
goto do_copy

:pfgm_refuse
REM ===========================================================================
REM Revision 4: PFGM_FORCE=1 -- a way past THIS refusal that leaves evidence.
REM
REM COO-DECISION 2026-09-03T01:48+07:00 item 7, revising the same COO's
REM `20260902_2342`: the id-2 rule still blocks, but a rule that has never
REM read a real DLL must not be the only thing between the owner and an
REM attended round. The DLL that GT-207 proved LOADS (R304, the GM window
REM opened on screen) has never been through this checker. If it were refused
REM at two in the morning with no way past, P-3 would be blocked by us, by
REM hand, and no lane could help until the next round.
REM
REM WHY THIS IS NOT FAIL-OPEN, said plainly because it looks like it:
REM   - the variable has NO default.  Nothing in this repository sets it,
REM     build_vs2008.bat does not set it, and an unset or empty PFGM_FORCE
REM     leaves the refusal exactly as it was.  The owner types it.
REM   - only the literal `1` counts, so `PFGM_FORCE=0` and `PFGM_FORCE=no`
REM     force nothing.
REM   - it is scoped to THIS refusal -- the checker's verdict about the file
REM     being installed.  It does NOT reach the [STOP] guard on an existing
REM     GameMaster.dll, which is about destroying an artifact this project has
REM     failed to obtain since 27 Aug and stays unforceable, and it does not
REM     reach the `.rsrc` [FAIL] above.
REM   - it prints the real verdict and the failing rule names in capitals,
REM     keeps the full report on disk, and repeats the line under the [OK], so
REM     a forced install cannot later be remembered as a checked one.
REM
REM The two tokens are READ FROM THE CHECKER'S OWN OUTPUT, never guessed here:
REM `verdict=` and `failed_rules=` are printed by
REM `pirateforce_foundation.gm.plugin_image_check.console_lines`, and
REM `failed_rules` names EVERY rule the image breaks, not only the one the
REM verdict happens to be.  A checker older than round `p7q74c` prints no such
REM line; that case says so instead of printing an empty `rules=`.
REM ===========================================================================
set "PFGM_VERDICT="
for /f "tokens=3" %%V in ('findstr /c:"GM_PLUGIN_IMAGE build verdict=" "%PFGM_OUT%"') do if not defined PFGM_VERDICT set "PFGM_VERDICT=%%V"
if not defined PFGM_VERDICT set "PFGM_VERDICT=verdict=unparsed_read_the_report_above"
set "PFGM_RULES="
for /f "tokens=3" %%R in ('findstr /c:"GM_PLUGIN_IMAGE build failed_rules=" "%PFGM_OUT%"') do if not defined PFGM_RULES set "PFGM_RULES=%%R"
REM `failed_rules=manifest_id2` -> `rules=manifest_id2`: the decision asked for
REM `rules=`, and re-typing the value into a second literal is how a printed
REM token and the token a test greps for drift apart.
REM !! NO ANGLE BRACKETS IN THESE VALUES, and that is a bug fix waiting to
REM happen rather than a style: `echo %VAR%` where the value holds a `<` is a
REM REDIRECTION, so the one line the owner has to report would be swallowed
REM into a file instead of printed.
if defined PFGM_RULES set "PFGM_RULES=%PFGM_RULES:failed_=%"
if not defined PFGM_RULES set "PFGM_RULES=rules=not_printed_this_checker_predates_round_p7q74c"
REM Same de-quoting as PF_SERVER_REPO above: `set PFGM_FORCE="1"` is how a
REM person who has been fighting paths with spaces all evening will type it.
set "PFGM_FORCE_FLAG=%PFGM_FORCE%"
if defined PFGM_FORCE_FLAG set "PFGM_FORCE_FLAG=%PFGM_FORCE_FLAG:"=%"
if "%PFGM_FORCE_FLAG%"=="1" goto pfgm_forced
echo.
echo [FAIL] plugin_image_check refused this file. Its verdict and EVERY
echo        blocking problem it found are printed above -- read all of them.
echo        One attended round is not worth spending one rebuild at a time.
echo        Nothing was copied. "%TARGET%" is untouched.
echo        The likeliest cause of a refusal that the .rsrc check let through
echo        is verdict=manifest_missing with a manifest at resource id 1
echo        instead of 2. Rebuild with build_vs2008.bat revision 5 or later,
echo        which embeds at ;#2.
echo.
echo        The full report is KEPT, not deleted, so it can be pasted into a
echo        letter instead of retyped off the screen:
echo            "%PFGM_OUT%"
echo.
echo        If you have a DLL you have SEEN load -- the GM window opened with
echo        it -- and this refusal is the only thing between you and a test
echo        session, install it anyway and tell us what was refused:
echo            set PFGM_FORCE=1
echo            install.bat "%TARGET%"
echo        That prints the real verdict and the failing rule names in
echo        capitals, keeps the report above, and asks you to send both to
echo        LANE-GM. It does not make the file good -- it makes the refusal
echo        reportable instead of final. It does NOT apply to the [STOP] guard
echo        about an existing GameMaster.dll: nothing forces that one.
exit /b 1

:pfgm_forced
set "PFGM_FORCED=1"
echo.
echo [FORCED] %PFGM_VERDICT% %PFGM_RULES%
echo [FORCED] PFGM_FORCE=1 IS SET, SO A FILE THIS CHECKER REFUSED IS BEING
echo [FORCED] COPIED ANYWAY. NOTHING HERE HAS VERIFIED IT. THE VERDICT ON THE
echo [FORCED] LINE ABOVE IS A FINDING ABOUT THESE BYTES, NOT A WARNING ABOUT A
echo [FORCED] MISSING TOOL.
echo [FORCED] TELL LANE-GM TWO THINGS: THE TOKENS ABOVE, AND WHETHER THE GM
echo [FORCED] WINDOW OPENED AFTERWARDS. EITHER ANSWER IS EVIDENCE -- IF IT
echo [FORCED] OPENED, A RULE OF OURS IS WRONG ABOUT REAL FILES AND WE OWE YOU
echo [FORCED] A FIX; IF IT DID NOT, THE RULE JUST SAVED THE SESSION.
echo [FORCED] THE FULL REPORT IS KEPT AT:
echo [FORCED]     "%PFGM_OUT%"
echo [FORCED] ROLLBACK IS ONE FILE: DELETE THE COPY IN THE CLIENT FOLDER.
goto do_copy

:pfgm_stale_tool
echo.
echo [warn] the plugin_image_check that answered is an OLD COPY: it printed a
echo        verdict but no "rules=" line naming manifest_id2, and copies from
echo        before 2026-09-02 answered verdict=image_ok for a manifest embedded
echo        at resource id 1 -- the exact failure this step exists to catch.
echo        Its answer is therefore NOT trusted, and this is treated like
echo        having no checker at all: nothing here has read the image.
echo        Fix by pulling the pirate-force-server checkout it used:
echo            "%PFGM_SRC%"
echo        or by pointing PF_SERVER_REPO at an up-to-date one.
if exist "%PFGM_OUT%" del /q "%PFGM_OUT%" 2>nul
goto do_copy

:do_copy
copy /y "GameMaster.dll" "%TARGET%\GameMaster.dll" >nul
if %errorlevel% neq 0 (
  echo [FAIL] copy failed. Check permissions on "%TARGET%"
  exit /b 1
)

echo [OK] installed: %TARGET%\GameMaster.dll
certutil -hashfile "%TARGET%\GameMaster.dll" SHA256
REM Said a second time, and the second time is the load-bearing one: the [OK]
REM and the SHA256 above are what a person screenshots, and a refusal that has
REM scrolled off the top would otherwise be remembered as "install.bat said OK".
if "%PFGM_FORCED%"=="1" (
  echo.
  echo [FORCED] THAT [OK] MEANS COPIED, NOT CHECKED. %PFGM_VERDICT% %PFGM_RULES%
  echo [FORCED] IF THE GM BUTTON STAYS DEAD, THIS LINE IS THE FIRST THING TO
  echo [FORCED] REPORT TO LANE-GM.
)
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
