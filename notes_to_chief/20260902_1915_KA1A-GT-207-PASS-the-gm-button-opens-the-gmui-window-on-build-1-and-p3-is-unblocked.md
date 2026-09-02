# GT-207 GM-PLUGIN-THREE-CELL-BUTTON-001 -> **[PASS]** on build 1

OBSERVER_CONFIRMED: 2026-09-02T18:54+07:00

- who: ka1-A (attended), owner **Panya** at the keyboard, she clicked the button herself
- when: 2026-09-02 18:30 -> 19:07 (+07:00), approximate
- head: 2fa4b589558783e79bf1cb9fc7c601c1cf5e2ae1 · BOOT_COMMIT: 379bf766d72816007a6e2241ccd846e670874fe5
- canonical sha 4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454 - UNCHANGED before and after
- jobs: 1455 preflight · 1456 build (failed, env) · 1457 build 1 · 1458 embed+install+step 0 · 1459 boot (aborted, code delta) · 1460 boot · 1461 teardown + rollback
- **builds used: 1 of the 3 the ticket allows.** Build 2 and build 3 were never needed.

**The ticket's own decisive line came back the best of its five:**

```
[GM_PLUGIN] alive, returning interface
```

**and the window opened.**

---

## RE-164, answered BEFORE anything was touched (the ticket's precondition)

**No.** There was no `GameMaster.dll` beside the client. Measured twice, at 18:15 and
again in job 1455 at 18:24, in
`C:\Users\Panya\Desktop\Pirate Force\GameClient`:
the only DLL present was `dbghelp.dll` (1,061,944 bytes, dated 2013-09-24), and a
case-insensitive search for `*gamemaster*` three levels deep returned zero files.

nonclaim: three levels from `GameClient\`, not the whole disk, not the registry, and
no import-table inspection. "Not in the folder" is not "never loaded".

---

## 🔴 DEVIATION FROM THE TICKET - read this before using this result

The ticket says `verdict=manifest_missing` means **stop the build, report LANE-GM, do
not boot**, on the stated ground that `build_vs2008.bat` has no `mt.exe` step and
VS2008 has no `/MANIFEST:EMBED`.

The build did produce a DLL with **no embedded manifest** (measured), and it imports
`MSVCR90.dll`, so step 0 would have returned exactly that verdict.

**But `mt.exe` exists on this machine** - at
`C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe`, under `Program Files`,
not `Program Files (x86)`, which is why an earlier search missed it - and the linker
had already written `GameMaster.dll.manifest` beside the DLL.

The owner was shown the choice in plain language and **chose to embed it** (her word:
"kho" / option 2, ~18:40 +07:00). So job 1458 ran, in its own job, without editing any
file belonging to LANE-GM:

```
mt.exe -manifest GameMaster.dll.manifest -outputresource:GameMaster.dll;#2
```

- nothing in `patches/gm_plugin/` was edited
- no compiler flag changed, no cell of the BUILD table changed, no fourth cell created
- the compiled code is byte-identical apart from the added resource
- sha256 13,824 bytes `67501F7E...F496` -> 14,848 bytes `4A0ECB58...D743B`
- the embedded manifest is the linker's own, declaring
  `Microsoft.VC90.CRT 9.0.21022.8 x86 publicKeyToken=1fc8b3b9a1e18e3b`

Reasoning offered to the owner, recorded here so anyone can disagree with it: the
purpose of that STOP is "do not boot a DLL that cannot load"; a side-by-side CRT
binding with no manifest is refused by the loader with 14001 and the plug-in never
runs. Embedding the manifest is what makes it loadable, so the purpose of the stop is
served rather than bypassed. The clause was written when nobody knew this machine had
`mt.exe`.

**If chief or LANE-GM judges this deviation unacceptable, this whole result should be
treated as INCONCLUSIVE and re-run after `build_vs2008.bat` gains its own `mt.exe`
step.** I would rather lose the result than have it quietly used on a basis someone
disputes. A separate letter to LANE-GM (filed 1920 today) asks for that step.

---

## Step 0 - the mandatory gate

```
GM_PLUGIN_IMAGE build   verdict=image_ok
GM_PLUGIN_IMAGE build   sha256=4a0ecb5817c15b0bf08964bc16972bc7340666357c494e9d0308ee9ce72d743b size=14848
GM_PLUGIN_IMAGE build   exports=CreateGameMaster
GM_PLUGIN_IMAGE build   imports=MSVCR90.dll,KERNEL32.dll
GM_PLUGIN_IMAGE build   embedded_manifest=yes
GM_PLUGIN_IMAGE install verdict=image_ok   (same sha256, same size)
GM_PLUGIN_IMAGE compare same_bytes=yes
STEP0_EXIT=0
```

`install.bat` was used, never a hand copy. It reported
`[OK] installed: ...\GameClient\GameMaster.dll` and its own sha256 matched.

---

## BUILD 1 - what the build itself said

```
EXTRA_DEFS=                          <- empty, which IS cell 1
check 1/3 export name      [ok] exported as exactly CreateGameMaster
                                1    0 00001570 CreateGameMaster
check 2/3 CRT dependencies [ok] MSVCR90.dll present
                           [info] MSVCP90.dll is not a dependency of THIS DLL (expected)
check 3/3 thiscall epilogues [ok] ret 8 and ret 4 present
sha256 (pre-manifest) 67501f7e2c74648473316ff5661433eaebf810f848c2958fb99998db72b5f496
```

---

## Every `[GM_PLUGIN]` line, verbatim, with the boot/click split

**ALL TEN LINES APPEARED AT BOOT.** Client pid 2496, DebugView rows 536-545, spanning
134.60008 to 134.60074 - **0.7 milliseconds**, and **before the owner touched anything.**

```
536  [GM_PLUGIN] loaded build=Sep  2 2026 18:30:33
537  [GM_PLUGIN] key=GMUI_1
538  [GM_PLUGIN] slot +0x00 +4 init: off (cell 1/2 default)
539  [GM_PLUGIN] CRT / msvcp90 lookups are deferred to the first CreateGameMaster call,
                 off the loader lock -- their result lines appear then, not now
540  [GM_PLUGIN] self-pin: ok (FreeLibrary cannot unmap us)
541  [GM_PLUGIN] client CRT: msvcr90.dll instance taken from the client's own operator
                 delete import, and ??2@YAPAXI@Z resolved in it
542  [GM_PLUGIN] msvcp90 wstring ctor: resolved from the client's own msvcp90.dll import
                 binding (that exact instance)
543  [GM_PLUGIN] key=GMUI_1
544  [GM_PLUGIN] slot +0x00 +4 init: off (cell 1/2 default -- writes the -1 and leaves +4
                 as the caller left it)
545  [GM_PLUGIN] alive, returning interface
```

**On the click: no new `[GM_PLUGIN]` line at all** (owner-observed, DebugView open the
whole time). That is consistent, not a defect - see the corrected assumption below.

`loaded build=Sep 2 2026 18:30:33` matches the build finishing at 18:30:34 in job 1457,
so the loaded image is this build.

---

## RECHECK, item by item

1. `loaded` at boot - **YES**, and it names this build's timestamp.
2. Result line - **`alive, returning interface`**. The best of the five. No `FAIL`.
3. `client CRT:` / `msvcp90 wstring ctor:` / `self-pin:` - all three present, all three
   succeeded. No `REFUSING`, no `NOT FOUND`.
4. `key=GMUI_1` and `slot +0x00 +4 init: off` - **matches BUILD table row 1 exactly**,
   read from the boot occurrence as the ticket requires.
5. **The window opened.** Title bar reads **`GMUI`**. Three tabs.
6. **No crash on close.** Job 1461 found **zero** crash dumps written in the previous two
   hours in the client folder, and the teardown closed with ports free and integrity ok.
   No crash on click either.
7. `slot +0x08 called with no MSVCP90 ctor` - **not seen, and this is a NO-RESULT, not a
   negative.** Read by LANE-GM's second gate exactly as instructed: line 542 says
   `resolved from the client's own msvcp90.dll import binding`, and it contains
   **no `NOT RESOLVED`** (`:662`/`:674`) and **no `degraded: no MSVCP90 wstring ctor`**
   (`:750`). The ctor therefore works, so a slot-8 call default-constructs and returns
   **silently by design**.
   🔴 **This round must NOT be used to close or to confirm `GM-IMG-014`'s blocker
   `NO_PINNED_CALL_ROUTE_FOR_SLOT8`.** That is exactly the mistake RECHECK 7's second
   gate was added to prevent.

---

## What is in the window (client-observable, recorded, nothing was executed)

The owner switched tabs and photographed each. **The `apply` button was never pressed**
- outside this ticket by its own nonclaim (1).

- **tab 1** - character hide / show / appear · a scene field with X, Y, Z boxes · an NPC
  field · two player fields · a "latest data" field
- **tab 2** - monster fields · a general ban control (ban all / unban) with a duration in
  minutes · a per-account ban with account name, reason and duration ("0 = permanent")
- **tab 3** - item drop with a drop-rate box · a BUFF field · a level field · an
  on/off toggle · an event field with a count

Screenshots are with the owner and in
`GameClient\Data\ScreenShot\` (the client wrote `ScreenShot20260902_185434.png` among
others while the window was open).

---

## Two things the ticket marked "[proposed, nobody has measured it]" - both now MEASURED

1. The ticket says the `client CRT:` / `msvcp90 wstring ctor:` / `self-pin:` lines
   "appear on the FIRST CLICK, not at boot", citing that `ResolveOnce()` is called only
   from `CreateGameMaster`, and separately proposed that **the click** is what reaches
   `CreateGameMaster` - "that is the question of the whole ticket, nobody has measured
   it".
   **Measured: the client calls `CreateGameMaster` at LOAD.** All three lines, plus the
   second `key=`/`slot` pair and `alive`, landed within 0.7 ms of `loaded`, with no
   input from the owner. The click reaches slot `+0x04`, which prints nothing.
2. Consequently the ticket's STOP - "`loaded` but no `client CRT:` on click means the
   client never called `CreateGameMaster`" - cannot be read the way it is written, since
   `client CRT:` now arrives at boot. Whoever owns the ticket should restate that stop
   in terms of the boot lines.

---

## What this closes and what it does NOT

**Closes:** the suspect the plug-in was built to eliminate. Before today the client
found no `GameMaster.dll`, built the 4-byte fallback object, slot `+0x04` returned NULL,
and the dispatcher returned immediately with no log and no frame (`GM-IMG-002/003/006/007`).
With a real DLL returning a real interface, **the button opens its window**. P-3's
headline question - open or not - is answered: **open**.

**Does NOT close, and nobody should say otherwise:**
- nonclaim (1) of the ticket stands: a window opening is **not** proof that any GM
  command works, and is not a milestone.
- nonclaim (3) stands: one suspect eliminated, not a root cause proved. `GM-IMG-005`
  (`GMModule_Client+0x19`) was never tested and is still an independent producer of the
  same silence.
- this says nothing whatsoever about the server. The plug-in touches no vital, no DB,
  and never opened the canonical DB. `gm_accounts` is a JSON allowlist, not a DB.
- the tab labels are the client's own localized strings. I did **not** verify that the
  tab reached is the one the ticket calls `GMUI_BASIC`; I recorded what is on screen.

---

## Rollback

**Done.** Job 1461 deleted `...\GameClient\GameMaster.dll` (sha256 `4A0ECB58...D743B`
recorded first) and verified it is gone: the only DLL beside the client is
`dbghelp.dll` again. The built copy stays at
`pf_bridge\patches\gm_plugin\GameMaster.dll`, same sha256, **not installed**.

No client byte was patched, no registry key written, no DB touched.

---

## Housekeeping found on the way

- The **boot** template inherited from job 1410 guards "pad busy" with
  `Get-Process -Name 'GameClient.local'`. The real process name is
  **`GameClient.local.bin`**, so the guard sees 0 clients while one is running. I used
  `Where-Object { $_.ProcessName -like 'GameClient*' }` in jobs 1459-1461 and it reported
  correctly. Same wrong name sits at lines 316 and 698 of
  `staged\TEMPLATE_teardown_generic.ps1` (reporting only there).
- Job 1456 failed with `[FAIL] No VC environment` although `VS90COMNTOOLS` **is** set at
  Machine scope. Cause: the bridge console process started before VS2008 was installed
  and never inherited it. Fix used: read the Machine value and assign
  `$env:VS90COMNTOOLS` inside the job. Worth putting in any future build job.
- Job 1459 aborted on `CODE_DELTA_vs_main=2` because `origin/main` moved between the
  resolve and the boot. Re-running two minutes later resolved `379bf766` cleanly. The
  guard behaved correctly; no change requested.
