# GAME TEST QUEUE -- ARCHIVE 20260906 (closed tickets moved verbatim from `GAME_TEST_QUEUE.md` per AGENTS.md §7 file-size gate; each has a one-line stub left in place; nothing here is deleted)

## GT-244 LIVE-WARP-SCENE-PERSISTS-ACROSS-LOGIN-001  [🚫 CLOSED -- CANCELLED - covered by 20260904_1911 R310 ข้อ 3 -- ห้ามบูตใบนี้ · คำถามของใบถูกตอบบนจอไปแล้วในรอบ R310 ก่อนที่ใครจะเรียกใบ: `/warp 2` → `GM_WARP_SCENE_PERSISTED scene=2` ทันที · `character_positions` = (2, 26905, 21185, 1680) โดยผู้เล่นไม่ขยับ → ปิด X → relaunch → ล็อกอินโผล่เกาะคุก (ภาพ `185526.png`) · `GM_WARP_SCENE_PERSIST_FAILED` = 0 ⇒ `PANYA-DECISION 20260904_1430` ปิด · ยกเลิกโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 2 (`PANYA 1934`) · ไม่แตะ F-1/F-2 ของ `GT-172` ที่ยังเปิดอยู่]

> Closes finding F-3 under `GT-172` (live warp changes the on-screen scene immediately but
> historically did not update the `character_positions` row used at next login -- a player who
> live-warped and logged out/in could land back in the old scene). This is a new, separate
> entry; it does not edit `GT-172`'s own PASS verdict and does not touch its still-open F-1/F-2.
> Opened per `COO-DECISION 20260904_1746` (chief opens this ticket, round 18:21) following
> `COO-DECISION 20260904_1646` (accepts LANE-GM's finding: a failed write must not block the
> warp itself, but must print console token `GM_WARP_SCENE_PERSIST_FAILED` alongside the
> existing `GM_WARP_SCENE_PERSISTED`) and `PANYA-DECISION 20260904_1430` ("a live warp must
> persist the scene immediately, even if the player never walks" -- her own measured repro:
> `/warp 2` live from Port Royal changed the screen and printed `WORLD_SCENE scene_id=2`, but
> closing the client with X and relogging without ever taking a step landed back at Port Royal;
> taking one step first before closing DID persist correctly, proving the write only fired on
> the movement frame, never on the warp frame itself).
>
> 🔴 **CAVEAT -- do not boot early:** `pirate-force-server#745` (`c2610cc`, merged onto `main`
> 2026-09-04T17:24+07:00) carries the base fix for the above PLUS a second commit (code
> `q3cde9`) fixing two CRITICAL findings LANE-GM's own first adversary pass caught in the same
> round: D1 (a `FoundationSession.checkpoint` write at frame-assembly time was overwriting
> `selected`, so the destination scene's census never composed) and D2 (`/warp <n> <x> <y>` was
> briefly wired to roll its own login-attribute assembly, which could leave a character
> permanently unable to log back in). Per `COO-DECISION 20260904_1744`, that second commit has
> NOT yet been through its required SECOND adversary pass as of this writing. **Nobody boots
> this ticket until that second-pass result has come back clean.** See RECHECK below.

- objective: single claim -- a GM issues a live `/warp <n>` (no coordinates; see note below)
  mid-session to move character X from scene A into scene N. Without the character taking one
  single further step, does the `character_positions` row for X get written with `scene_id = N`
  and a position matching where `TeleportVital` placed them, at the moment the warp frame itself
  is sent -- not waiting for a subsequent movement frame?
- note on command form: `/warp <n> <x> <y>` (explicit coordinates, cross-scene) is currently
  WITHDRAWN and refused with a console line, no bytes out (`COO-DECISION 20260904_1744` item 3;
  R306 measured that frame shape, a 45-byte ForcePos, kills the client with `ErrorData=28317`)
  -- do not attempt it. Use `/warp <n>` with no coordinates, landing at scene N's registered
  spawn point; this branch already PASSED as a live cross-scene teleport in `GT-182`
  (2026-09-01), and separately for same-scene warps per `PANYA-DECISION 20260903_1800`. This
  entry is not about whether the teleport itself happens (already proven) -- only whether the DB
  row updates in the same beat as that teleport.
- db: fresh copy of `state\pirateforce.sqlite3` only, never the canonical file. Record the
  copy's filename and sha256 of the canonical file before and after; `PRAGMA integrity_check` =
  `ok` both times.
- server args: standard boot, no `--*-scenario` flag, GM account from `gm_accounts.json`.
  Capture stdout+stderr to one combined console file.
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt243_<stamp>.sqlite3
  ```
- RECHECK (run before every boot; any item failing = stay BLOCKED, do not boot):
  1. Confirm a result exists (`rounds/` or `notes_to_chief/`, addressed LANE-GM or COO) stating
     the SECOND pf-adversary pass on code `q3cde9` (server#745's D1/D2 commit) returned clean on
     `origin/main`. Absence, or a result reporting new findings, = stay BLOCKED.
  2. `git -C ../pirate-force-server grep -c "GM_WARP_SCENE_PERSIST_FAILED" origin/main -- src/`
     -- must be >= 1 (the paired failure token from `COO-DECISION 20260904_1646` item 2 must be
     on `main`, not just opened as a PR -- as of round `ydlvtt` it was pushed but not yet
     confirmed merged). If 0, stay BLOCKED.
  3. `git -C ../pirate-force-server log --oneline origin/main -1 -- src/pirateforce_foundation/gm/warp_scene_persist.py`
     -- confirm the commit reachable is at or after `q3cde9`'s second commit (`c2610cc` alone is
     not sufficient -- items 1-2 above must also pass).
- steps: (server first, then client; if a client is ever killed, restart the server before the
  next client boot or it hangs on "connecting" forever)
  1. RECHECK passes fully. `LOCK_GAME`. Boot stamp. sha canonical (before). Copy DB.
  2. Boot fresh server, then client. Log in with the GM account into scene A (any starting
     scene). Confirm HUD.
  3. Right-click-drag the camera only (never `Q`/`E`, never `W/A/S/D` -- those turn the
     character and emit `TargetPosVital`, which would confound this test) for a clean baseline
     view. Screenshot S0, full resolution: scene name, HUD X/Y/Z, and the colour of every name
     label in frame (one line per label; write "none" if empty).
  4. Click the chat input box, confirm the cursor/focus is in it (typing while unfocused becomes
     hotkeys, not chat). Type `/warp <n>` once, for a destination scene N known to
     `scene_catalog.is_known_scene_id` and != A. Press Enter.
  5. Immediately after the scene visibly changes (do not wait, do not move): screenshot S1, full
     resolution: scene name/background/minimap now showing N, HUD X/Y/Z, label colours. Note
     whether the console printed `GM_WARP_SCENE_PERSISTED scene=<n>` or
     `GM_WARP_SCENE_PERSIST_FAILED scene=<n> reason=<...>` for this warp -- secondary signal
     only, not a substitute for the DB read in step 10.
  6. 🔴 **STOP-on-HP-0**: if HP reaches 0 at any point, stop immediately, capture screenshot +
     console, record as the result -- do not retry.
  7. WITHOUT taking one single step (no `W/A/S/D`, no `Q`/`E`; camera drag only), exit to the
     character-select screen via the normal exit path (not force-killing the client), leaving
     the server running. Note the exact wall-clock time.
  8. Log back in with the SAME character. Screenshot S2, full resolution: scene
     name/background/minimap on arrival, HUD X/Y/Z, label colours.
  9. NO-CRASH check: right-click-drag camera only, then exit with the normal exit path.
  10. Stop the server. sha256 all evidence files. `integrity_check`. sha canonical (after) --
      must match the before value. Open the DB copy directly and read the `character_positions`
      row for this character as it stood immediately after step 5 (compare its `scene_id`/x/y/z
      against N's spawn point / the destination `TeleportVital` target). Run teardown regardless
      of how the round ended (teardown template refuses a boot stamp older than 420 minutes).
- pass criteria (two layers, never mixed):
    wire/DB (console + DB copy; headless-provable, no human required):
      (1) the console prints `GM_WARP_SCENE_PERSISTED scene=<n>` (or, as a valid negative
          result, `GM_WARP_SCENE_PERSIST_FAILED scene=<n> reason=<...>`) for this warp, in the
          same request/response cycle as the `TeleportVital` frame -- no intervening
          `TargetPosVital` frame between the warp and this token.
      (2) the `character_positions` row for character X, read from the DB copy, shows
          `scene_id = N` with position fields matching the destination's spawn point / the
          `TeleportVital` target, at a point BEFORE any subsequent movement frame appears in the
          console -- this is the row that must exist even though the character never took a
          step (per `PANYA-DECISION 20260904_1430`).
      (3) if the console instead shows `GM_WARP_SCENE_PERSIST_FAILED`, that is a valid, useful
          negative result for this layer: the write did not happen, and per
          `COO-DECISION 20260904_1646` item 2 this must NOT have blocked the on-screen warp (S1
          in the client-observable layer should still show the scene change) -- record both
          facts; this is a finding, not a wasted round.
      (4) `integrity_check` = `ok` both times; canonical sha unchanged.
      This layer alone cannot say what the tester saw on screen.
    client-observable (needs a human at the screen; never inferred from the console/DB):
      (5) S1 shows the scene visibly changed to N immediately, mid-session, no relog.
      (6) S2 (after logout and a fresh login, with zero movement in between) shows scene N on
          arrival -- not scene A, the pre-warp scene.
      (7) name label colours recorded for every label in S0, S1, and S2, one line per label per
          image, "none" where empty, read from full-resolution stills only (never a contact
          sheet, downscaled image, or video). Record colour only -- do not infer a cause
          (`RE-067` owns that question). Any divergence from the original server's screenshots
          goes to `REAL_SERVER_DIVERGENCE.tsv`, one row each.
      This layer alone cannot say what the DB row held before the human looked.
    Close only with `OBSERVER_CONFIRMED: <ISO+07:00>` once both layers have evidence (`G-OBS`).
    Evidence with no observer signature is `AWAITING-OBSERVER`, not PASS.
- nonclaims:
  1. Does not test `/warp <n> <x> <y>` with explicit coordinates -- that branch is withdrawn
     (see note above); nothing here reopens it.
  2. Does not test census/actor population of the destination scene (`GT-172` F-1, still open,
     separate).
  3. Does not test the geometry the character lands on (`GT-172` F-2, still open, separate) --
     if S1/S2 shows the character stuck in geometry, log it as data, not a FAIL of this claim.
  4. Does not close, retest, or overturn D8 (LANE-GM's own still-open follow-ups: first-warp-
     in-same-dispatch census ordering, and the write-then-socket-send gap) -- separate
     CORE-REQUEST, not this ticket.
  5. Does not itself certify server#745's second commit passed adversary review -- that is a
     fact this ticket's RECHECK reads, not one it produces.
  6. Not a combat test; STOP-on-HP-0 exists only because a GM account is in a live session and
     any hostile contact must halt the round, per house convention on GM-warp tickets.
- links: `GT-172` (F-3 origin, PASS overall, F-1/F-2 still open) -- `GT-182` (PASS, proves
  `/warp <n>` no-coords live cross-scene teleport itself already lands correctly) --
  `notes_to_chief/20260904_1430_PANYA-DECISION-a-live-warp-must-persist-the-scene-immediately-even-if-the-player-never-walks.md`
  -- `notes_to_chief/20260904_1646_COO-DECISION-lane-gm-1430-landed-accepted-write-failure-does-not-block-the-warp-but-must-print-a-console-line-three-deviations-accepted.md`
  -- `notes_to_chief/20260904_1744_COO-DECISION-lane-gm-745-is-on-main-second-adversary-pass-on-the-fix-is-your-first-task-warp-with-coordinates-stays-withdrawn.md`
  -- `notes_to_chief/20260904_1746_COO-DECISION-chief-745-landed-open-the-gt172-f3-closing-ticket-and-answer-gm-0435-in-one-line.md`
  -- `notes_to_chief/20260904_1652_LANE-GM-TO-COO-adversary-caught-two-criticals-in-745-fixed-same-round.md`
  (D1/D2 detail) -- `rounds/GM_20260904_1754_ydlvtt_the-console-line-that-tells-persisted-from-failed.md`
  (`GM_WARP_SCENE_PERSIST_FAILED` implementation, PR push not yet confirmed merged as of that
  round's own end) -- `pirate-force-server#745` (`c2610cc`) --
  `src/pirateforce_foundation/gm/warp_scene_persist.py`
- numbering: originally drafted as `GT-243` after grepping `GT-24[0-9]` across the working tree
  and finding no existing `GT-243` -- but that check ran against a stale local clone. LANE-CS
  independently opened `GT-243` (`HOTBAR-SKILL-99-VS-WIELD-Z-SAME-SESSION-HEX-DIFF-001`) around
  the same time and it landed on `main` first (`git show origin/main:GAME_TEST_QUEUE.md` confirms
  it). Per prompt section 4 ("เลขชนกับที่มีอยู่ ห้ามทับ ให้ +1"): renumbered to `244` by chief
  round `ub8svt` before merging main into this branch, no other change.
- result: (tester fills in: PASS/FAIL/still-BLOCKED, evidence for both layers separately,
  console lines verbatim, DB row read verbatim, sha256, boot stamp, `OBSERVER_CONFIRMED`
  timestamp)

**ผู้เปิดใบ: chief (LANE-E) ตาม `COO-DECISION 20260904_1746` -- ผู้บริโภคผล: chief (LANE-E)**

---


## GT-121 CORE-REQUEST-026 BG0002-ARRIVAL-CENSUS-NO-WASD-001: after CORE-REQUEST-026 makes the Bg0002 (Prison Exile Island) census fire on `teleport_sent + runtime_ack_sent` (arrival) instead of waiting for the first `TargetPosVital`, does a real client actually show NPCs/monsters standing on screen the moment the loading screen clears -- **before the player presses any movement key at all** -- closing gap ① from M1-P's own PASS result (`20260828_0150_M1P-RESULT-PASS-*.md`: "เข้าฉากแล้วไม่มีอะไรเกิดขึ้นจนกว่าจะกด Q/E/A/S/D/W หนึ่งครั้ง")  [✅ PASS -- ปิดโดยสาย A (LANE-A) รอบ `kr1kme` (2026-08-28T10:2x+07:00) จากผล attended กะ1-A `20260828_0925_GT116-121-120-RESULT-*.md` · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (BOOT_COMMIT `98307ae` = main HEAD) · claim เดียว (สำมะโนมาก่อนขยับ) เท่านั้น: wire `WORLD_CENSUS assembled=97/97 source=bg0002_full_roster` พิมพ์ที่ HB#5 ก่อน first `TargetPosVital` ที่ HB#15 (10 heartbeat ต่อมา) · จอเจ้าของ: "เข้าแมพมา NPC ทุกตัวเกิดมารออยู่แล้ว ผ่าน" -- ช่องว่างข้อ ① ของ M1-P ปิด · [ไม่อ้าง] เรื่อง facing/สี/ความหนาแน่นของ actor (คนละเรื่อง, gap ②/③/④/⑥ ของ M1-P ยังเปิดอยู่ -- ไม่รวมข้อ ⑤ ที่แยกเรื่อง Mirage Reel/RE-123 ซึ่งก็ยังเปิดเช่นกัน)]

> NUMBERING NOTE: grep confirmed before reserving (2026-08-28T06:38+07:00, this round) -- `GT-121`/`RE-120` = 0
> hits in `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and `archive/`. Highest number in use anywhere in the
> shared counter is `120` (`GT-120`, above) -- => this entry is `121`. `GT-101`-`GT-120` and `RE-085`-`RE-119`
> stay exactly where they are, unchanged -- this is a new entry, not a replacement for any of them.

### source (links only -- see cited files for full detail, not re-derived here)
- `notes_to_chief/20260828_0150_M1P-RESULT-PASS-owner-confirms-Prison-Exile-identities-6-gaps-map-window-lead.md`
  gap ①: the owner's own M1-P session (00:2x-00:5x+07:00, boot commit `6406a05`, BEFORE this fix existed)
  measured the census arriving only after the client's first `TargetPosVital` (console L260 -> L264-265) --
  the scene sat empty from load until the player's first WASD press. This entry is the first attended shot at
  the fix for exactly that gap.
- `archive/rounds_2026-08-27_to_28/R207_confident-ride-sf9kel_core-request-026-bg0002-census-arrival-trigger.md` /
  `notes_to_chief/consumed/20260828_0234_LANE-A-CORE-REQUEST-024-bg0002-census-trigger-on-arrival.md` (the
  build request, filed under the shadow-collided number `024`, re-registered `026` per
  `CHIEF_CONTINUATION.md` row 026): chief wired `pirate-force-server@13fe3aa` same round -- confirmed on
  `origin/main` ancestry as of this entry (`git log origin/main --oneline | grep 13fe3aa`, merged via
  `pirate-force-server#177`). WORLD-CENSUS-001's bg0002 branch now triggers on
  `teleport_sent and runtime_ack_sent` alone, anchored on
  `world_scene_travel.spawn_position(world_scene_travel.destination(scene_id, scene_entry_registry))`
  when no `TargetPosVital` has arrived yet; a real `TargetPosVital` that does arrive first still wins as the
  anchor, unchanged. bg0001 (Port Royal) is untouched -- still waits for `TargetPosVital` exactly as before,
  not in scope of this entry.
- `notes_to_chief/consumed/20260827_2240_KA1A-NOTE-GT110-unsafe-until-0x5A19-payload-fixed-plus-M1P-jobs-staged.md`
  and the M1-P result above: the run-DB-copy seed procedure this entry reuses (`character_positions.scene_id`
  1->2 on a throwaway copy, never canonical) is not new -- it is the exact procedure M1-P's own jobs
  `1311`-`1314` already ran successfully once today. This entry does not invent a new seed method.

### objective (single claim -- identity/roster correctness is a separate, already-PASSED claim from M1-P)
On a character whose stored position row names `scene_id=2` (seeded the same way M1-P seeded it), does the
Prison Exile Island census (NPCs, monsters) appear on screen **before the player has pressed any movement
key** -- specifically, does the very first `RuntimeProtocolReq` poll after arrival already carry the full
roster, rather than the roster appearing only after the first WASD-triggered `TargetPosVital`. The wire/DB
layer of this claim (does the dispatcher's guard actually admit an arrival with `last_target_pos is None`) is
already proven headless this round in `tests/test_bg0002_census_wiring.py::
test_the_scene2_census_arrives_with_no_target_pos_vital_ever_sent` (cited above, NOT re-proven here). This
entry is the client-observable layer only: the first human eyes on this specific fix, and specifically the
first time anyone tests it WITHOUT pressing a movement key first (M1-P's own PASS session did press WASD,
which is exactly why it could see gap ① at all).

### predictions (a wrong prediction is a finding, not a failure)
- P1 [primary, proposed]: NPCs/monsters are visible standing on the ground the moment the loading screen
  clears and the HUD becomes interactive, with the character standing still and no key pressed yet -- not the
  empty scene M1-P's own PASS session described for the first few seconds.
- P2 [expected non-event, explicitly NOT a requirement]: the actors' facing direction is still the same
  cosmetic four-way round-robin RE-116 already bounded as synthetic (not real client data) -- do not treat
  uniform facing as a new finding, it is gap ② from the same M1-P letter and already understood, unrelated to
  this fix.
- P3 [falsifier]: the scene is still empty until the first movement key is pressed -- a real negative, not a
  failure. It would mean either this client build never received `pirate-force-server@13fe3aa`, the seed did
  not actually land on `scene_id=2` before boot, or the arrival trigger's own anchor fallback
  (`world_scene_travel.spawn_position`) failed silently and latched `world_census_refused` -- redirect to a
  new RE/GT entry naming which of those three (check the console for `world_census_bg0002_arrival_anchor_
  refused_*` specifically -- its presence points at the third), do not re-run this one guessing.

### ก่อนบูต -- ด่าน 0 (merge status, MUST clear first), ด่าน 1 (green boot), ด่าน 2 (grep confirms the branch)
**ด่าน 0 -- merge status:** commit `pirate-force-server@13fe3aa` is confirmed on `origin/main` ancestry as of
this entry's writing (`git log origin/main --oneline` lists it, merged via `pirate-force-server#177`) --
unlike GT-120 at the time it was opened, this fix does not need a fresh re-check before ด่าน 1, but
`pf_resolve_green_boot.py` still follows `origin/main` at boot time, not this entry's writing time, so
re-confirm anyway.

**ด่าน 1:**
```
py -3 pf_resolve_green_boot.py --repo "C:\path\to\pirate-force-server" --fetch
```
Only `exit 0` + printed `BOOT_COMMIT: <sha>` means bootable.

**ด่าน 2 (need at least 1 line from every command; missing any one = BLOCKED, do not boot):**
```
git grep -n "CORE-REQUEST-026" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "world_census_bg0002_arrival_anchor_refused" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "SCENE2_N_ID" <SHA> -- src/pirateforce_foundation/world_population_bg0002.py
git grep -n "test_the_scene2_census_arrives_with_no_target_pos_vital_ever_sent" <SHA> -- tests/test_bg0002_census_wiring.py
```

### db -- seed procedure reused from M1-P jobs 1311-1314, not new
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to
`pf_bridge\backup\pirateforce_before_GT-121_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt121.sqlite3`. sha256
vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

Seed, on the working copy only, before first boot:
```
UPDATE character_positions
   SET scene_id=2, scene_seq=0, x=26905, y=21185, z=1680
 WHERE character_id=<the test character's id>;
```
(`26905,21185,1680` is `scenarios/world_scene_registry_001.json`'s own pinned scene-2 spawn -- the same value
`world_scene_travel.spawn_position` reads as the arrival-trigger's anchor fallback, and the same coordinate
M1-P's own seed used.) Print the row before and after the UPDATE as the SEED_BEFORE/SEED_AFTER receipt, the
same convention M1-P's job `1312_m1p_boot_video` used.

### server args (flagless -- the dispatch branch is unconditional/production, no `--*-scenario` of any kind)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt121.sqlite3
```
No scenario flag, no other entry piggybacked onto this boot.

### steps (click by click -- record continuous video for the whole LOCK_GAME window)
Before start: hold `LOCK_GAME`, note boot stamp (+07:00, must be under 420 min old at teardown), compare
canonical sha, copy DB per the db block above, run the seed UPDATE and print SEED_BEFORE/AFTER, stage
`TEMPLATE_teardown_generic.ps1`, confirm ด่าน 0-2 all cleared (record the resolved SHA).
1. Start the server first (ports 10188/10189 must show 0 established connections before opening the client).
2. Open client, log in to the seeded character. **Start continuous recording BEFORE the loading screen
   clears** -- the whole point of this entry is what is on screen in the first few seconds, before any input.
3. **Do not press any key and do not move the mouse over the game viewport** from the moment the loading
   screen clears until step 5 is done. No W/A/S/D, no Q/E, no camera drag -- any of those can emit a
   `TargetPosVital` and would make this test indistinguishable from what M1-P already ran once.
4. Photograph full-res the instant the HUD becomes interactive (T0), and again at +1s, +2s, +5s -- record
   whether any actor (NPC or monster) is visible at each still, and if visible only starting at some later
   still than T0, record which one.
5. Once step 4's stills are captured, THEN it is safe to do the normal M1-P-style tour (WASD to Navy
   Transfer/Sebastian/Pike/etc.) if useful corroboration, but that part is not required for this entry's own
   pass/fail -- it is already what M1-P proved once.
6. If the server console is visible, copy verbatim the first `WORLD_SCENE scene_id=2` line and the first
   `WORLD_CENSUS assembled=.../...` line, and note whether either appears before or after step 3's first
   possible player input (there should be none) -- supplementary corroboration only, not a substitute for the
   client-observable answer.
7. Log out, teardown via `TEMPLATE_teardown_generic.ps1` (stamp still under 420 min), recheck canonical
   sha256, sha256 every capture.

### pass criteria (two layers, never mixed)

wire/DB: the actual claim this layer answers -- "does the dispatcher admit an arrival census with
`last_target_pos is None`" -- is already CLOSED headless this round by
`tests/test_bg0002_census_wiring.py`'s 4 new tests (cited above, not reproduced by this entry). This entry's
own wire/DB obligations are only: canonical sha256 matches `CANON_SHA.txt` before/after; `PRAGMA
integrity_check` = `ok` on the working copy both times; the seed UPDATE's before/after row is printed.

client-observable (a human at the screen only, never inferred from the console):
- Primary reading: are NPCs/monsters visible at T0 (the instant the HUD becomes interactive, before any
  player input) -- P1 vs P3, both are complete, valid answers; write whichever actually happened, and if
  P3, record exactly how many seconds/inputs elapsed before actors did appear (if they ever did).
- Secondary: record which specific NPC(s) are visible at T0 by name/title if legible (does not need to match
  every one of the 97 -- a handful visible near spawn is enough to answer this entry's own question).
- No crash, no stuck loading screen, no error dialog during the no-input observation window (steps 3-4).

### nonclaims
- Does not re-test M1-P's own identity/roster-correctness claim (already PASSED, see the source letter) --
  this entry only tests WHEN the roster appears, not WHETHER it is the right roster.
- Does not test bg0001 (Port Royal) -- CORE-REQUEST-026 deliberately left that branch untouched, still
  requiring `TargetPosVital` exactly as before; a separate entry would be needed if that behavior is ever
  wanted there too.
- Does not prove the arrival-trigger's anchor fallback is correct for any scene OTHER than 2 -- it is scoped
  to `SCENE2_N_ID` only, by the runtime.py branch structure itself, not by anything this entry checks.
- Does not attempt to close gaps ②-⑦ from the M1-P letter (heading, name colour, density, Mirage Reel, pose,
  Attr completeness) -- separate, already-tracked items, out of scope here.
- Single account, single login, single session -- no reconnect/relogin, no second character.
- If ด่าน 0/1/2 don't clear (functions not found at the resolved SHA) -> the entire entry is **BLOCKED**, not
  NO-RESULT/FAIL -- record it as "รอ merge" and stop.

### result (ผู้เทสกรอก)
```

```

---

## GT-143 BG0002-SET103-FIVE-PLACEMENTS-001 [attended, in-game]: ยืนไปดูพิกัดห้าจุดใน Prison Exile -- ตรงนั้นมี Orc Chief หรือไม่มีอะไรเลย  [~~OPEN~~ **ANSWERED (บูตจริง, กะ1-A 2026-08-30T15:4x+07:00) — ทั้งสองกฎที่ใบนี้ทำนายไว้ผิดทั้งคู่**
· อัปเดตโดย LANE-B รอบ `qb1ytr` 2026-08-30T16:4x+07:00 บริโภคจดหมาย `20260830_1554_GT143-GT132-GT149-RESULT-*.md`:
เจ้าของเดินครบทั้งห้าจุด พบ actor จริงแค่ตัวเดียวในย่านนั้น (`Carle`/`Nautilus Leader` n_ID 40) ซึ่ง**ไม่ใช่
หนึ่งในห้าพิกัดที่ใบนี้ถาม** · wire ยืนยันตรงกัน: สำมะโน 97/97 แถว มี `n_ID` แค่ 1-41 เท่านั้น **ไม่มี `103`
และไม่มี `917` เลยสักแถว** ⇒ คำตอบไม่ใช่ "setnum ถูก" และไม่ใช่ "cline ถูก (ล่องหน)" แต่คือ**ห้าแถวนี้ไม่ถูก
ส่งลงฉากเลยไม่ว่ากฎไหน** — คนละคำทำนายกับทั้งสองทางที่ใบนี้ตั้งไว้แต่แรก 🔴 **ข้อบกพร่องที่เจ้าของชี้เอง
ของการออกแบบใบนี้:** "เห็นว่างเปล่า" กับ "cline ล่องหนทำงานแล้ว" แยกกันด้วยตาไม่ได้ ถ้าไม่มีชั้นสายคู่กัน
รอบนี้มีชั้นสาย จึงจับได้ว่าอ่านผลด้วยตาอย่างเดียวจะสรุปผิด · **หาว่าห้าแถวหายไปที่ขั้นไหนของท่อเป็นคำถาม
ของสาย A/chief ไม่ใช่ของสาย B** (ระบุไว้แล้วในจดหมายผลข้อ 4 cc สาย A/chief โดยตรง — สาย B ไม่เปิดใบซ้ำ)
· nonclaim เดิมของใบนี้ (เรื่องกฎตัวตนของโปรเจกต์ ไม่ใช่หน้าที่ใบนี้ตัดสิน) ยังใช้ได้ทุกตัวอักษร**]

> ทำไมถึงมีใบนี้: `COO-DECISION 20260829_0345` ให้ `cline` เป็นกฎตัวตนกฎเดียว โดยมีเงื่อนไขว่า `Bg0002` ต้องออกมาเหมือนเดิม รอบ `ua236k` วัดแล้วว่า **ต่าง 5 แถวจาก 17** ⇒ เงื่อนไขหยุดทำงาน ใบถามเจ้าของคือ `notes_to_chief/20260829_0549_LANE-B-ASK-COO-cline-deletes-five-prison-exile-rows.md` · ใบนี้คือหลักฐานชั้น client-observable ที่จะทำให้เจ้าของเคาะจากของที่เห็น ไม่ใช่จากความจำ

**คำถามเดียว:** ตรงห้าพิกัดนี้ใน Prison Exile (`Bg0002`) มี actor อยู่หรือไม่มี — ถ้ามี ชื่ออะไร

| # | placement | x | y | z |
|---|---|---|---|---|
| 1 | 92 | 17870.70 | 6142.27 | 946.08 |
| 2 | 93 | 17646.61 | 5751.74 | 1472.73 |
| 3 | 94 | 17927.32 | 5449.72 | 920.73 |
| 4 | 95 | 17194.11 | 6104.93 | 1016.14 |
| 5 | 96 | 17243.01 | 5434.12 | 979.53 |

**สองกฎทำนายคนละอย่าง จึงแยกกันด้วยตา:**

| กฎ | `MOBS.n_ID` | สิ่งที่ควรเห็น |
|---|---|---|
| `setnum` (ที่ ship อยู่วันนี้) | `103` | Orc Chief เลเวล 58 ชื่อขึ้นสีแดง คลิกเปิด target panel ได้ |
| `cline` (`CLINE[2,103]`) | `917` | rank 0 / AI 0 / outfit `INVISIBLE` ⇒ **ไม่มีอะไรให้เห็นตรงนั้นเลย** |

**วิธีทำ (ไม่ต้องแก้โค้ด ไม่ต้องเปิดแฟล็ก):**
1. บูตเซิร์ฟเวอร์ปกติ เข้า `Bg0002` ด้วยตัวละครที่มีอยู่ — วันนี้เซิร์ฟเวอร์ ship ห้าแถวนี้อยู่ ⇒ ถ้าเห็น Orc Chief คือของที่เซิร์ฟเวอร์ส่งเอง
2. เดินไปห้าจุดด้านบน จุดละหนึ่งจอ ถ่ายหน้าจอไว้ทั้งห้าจุด
3. ถ้ามี actor: คลิกหนึ่งครั้ง จดชื่อที่ขึ้นใน target panel และสีของชื่อ (แดง/เหลือง/ขาว)
4. ถ้าไม่มี: จดว่าไม่มี — การไม่มีคือคำตอบที่มีค่าเท่ากัน ไม่ใช่ FAIL

**เกณฑ์สองชั้น:**
- client-observable: ห้าจุด มี actor กี่จุด ชื่ออะไร สีอะไร (สกรีนชอตทุกจุด ลง `evidence_screens/`)
- wire/DB: `WORLD_CENSUS` ของบูตเดียวกัน — นับแถว template `103` ที่ส่งจริง (คาดว่า 5)

**คำตอบที่ใบนี้กำลังหา และมันแปลว่าอะไร:**
- **เห็น Orc Chief ห้าตัว** ⇒ `setnum` อ่านถูกสำหรับเลขนี้ และการพลิกเป็น `cline` จะลบมอนจริงออกจากสนาม
- **ไม่มีอะไรเลย** ⇒ ที่ ship อยู่วันนี้ถูกสร้างขึ้นเอง และ `cline` ถูกทั้งฉาก ⇒ พลิกได้ทันที
- **เห็นอย่างอื่น** ⇒ ทั้งสองกฎผิด เปิดใบ RE ใหม่

> **เพิ่มหลัง pf-adversary:** ทางเลือกของเจ้าของมี **สามทาง ไม่ใช่สอง** — `tools/pf_mine_scene_mob_roster.py --keep-withdrawn-rows` ship แถวที่กฎใหม่ถอน โดยติดป้ายรายแถวว่าเป็นการอ่านแบบเก่ารอ migrate (`bg0001` เคย ship แบบนั้นจนถึงรอบ `8ftmbx`) ⇒ **"มอนหายห้าตัว" เป็นผลของแฟล็ก ไม่ใช่ของกฎ** · ใบนี้ยังตอบคำถามเดิม (ตรงนั้นมีอะไร) ซึ่งจำเป็นกับทั้งสามทาง
> **เบาะแสที่ไม่ใช่หลักฐาน:** `MOBS 917` คือตัวล่องหนคู่แฝดของ `MOBS 916` "Training Iron Man" ที่ Port Royal ship เป็นหุ่นซ้อม และห้าจุดนี้อยู่รวมกันเป็นกระจุก (x 17194-17927, y 5434-6142) ⇒ อ่านได้ว่าเป็น**ลานฝึก** · ถ้าผู้เทสเห็นว่าบริเวณนั้นมีรูปร่างแบบลานฝึก ให้จดไว้ด้วย

**nonclaim:** ใบนี้ไม่ได้ตัดสินกฎตัวตนของโปรเจกต์ — มันตอบคำถามเดียวว่าพิกัดห้าจุดนี้มีอะไร · คนตัดสินคือเจ้าของ · และ `Bg0002` จะไม่ถูกแก้จนกว่าจะมีคำเคาะ


---

## GT-149 DROP-LIFETIME-MEASURE-001 [attended, in-game · แนบไปกับรอบถ่ายวิดีโอของเจ้าของ · ~10 นาที]: ฆ่ามอนแล้ว **จงใจไม่เก็บ** -- ของบนพื้นอยู่ได้กี่วินาทีก่อนหาย  [~~PENDING~~ **ANSWERED-DIFFERENTLY (บูตจริง, กะ1-A 2026-08-30T15:4x+07:00)**
· อัปเดตโดย LANE-B รอบ `qb1ytr` 2026-08-30T16:4x+07:00 บริโภคจดหมาย `20260830_1554_GT143-GT132-GT149-RESULT-*.md`:
ผู้เทสจับเวลาที่ใบถามไม่ได้เพราะ**ไม่เคยเห็นของบนพื้นเลยสักชิ้นทั้งสี่ครั้ง** ⇒ คำถามเดิม ("อยู่กี่วินาที
ก่อนหาย") ไม่มีคำตอบชั้น client-observable แต่ชั้นสายให้ตัวเลขสองตัวที่ใบไม่ได้ถามและมีค่ามากกว่า:
`MOB_DROP_PRESENCE ... declared_lifetime=120.0s oldest_left=120.0s newest_left=120.0s label_life=0.2`
— **บัญชีพื้นดิน (ledger) อยู่รอด 120 วิ ตามที่ตั้งไว้จริง แต่ป้ายที่ตาเห็นอยู่แค่ 0.2 วิ** สองค่านี้
วัดคนละชั้น ไม่ขัดกัน · เฟรม `MOB_LOOT_DROP` เองยังมาถึงช้า (`late=351-949 ms` จากคอนโซล) ซึ่งกินเวลา
มากกว่าอายุป้ายทั้งช่วง (สมมติฐาน ไม่ใช่ข้อสรุป — ยังไม่วัดฝั่ง client ตรง ๆ ว่าป้ายหมดอายุก่อนเฟรมถึงจอ
จริงหรือไม่) · `REEMISSION_REDRAWS_THE_LABEL` ยังเป็น `None` เหมือนเดิม รอบนี้ไม่ได้วัดเพิ่ม (ไม่มีการส่งซ้ำ
เกิดขึ้นเลยภายใต้ cadence ปัจจุบัน ป้ายจึงไม่มีโอกาสถูก redraw ให้วัด) · 🔴 **`DROP_LIFETIME_SECONDS=120.0`
ไม่ใช่ตัวบล็อกอีกต่อไป — `label_life` ต่างหากที่เป็นตัวบล็อกจริงของ `GT-146`** ดู ASK-COO ใบใหม่รอบนี้
(`notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md`) ที่เปิดคำถามว่า
จะแก้ที่ไหนได้บ้างในเมื่อ `label_life` เป็นพฤติกรรมของไคลเอนต์เดิม ไม่ใช่ตัวแปรฝั่งเซิร์ฟเวอร์]

> NUMBERING: เลขสูงสุดที่ใช้ไป = 148 (`GT-148` · `RE-` สูงสุด = 132) ⇒ ใบนี้ = `GT-149` · ตัวนับเดียวร่วม `CLIENT_RE_QUEUE.md`
> ที่มา: `DROP_LIFETIME_SECONDS = 120.0` ใน `mob_loot.py` เป็นเลขที่สาย B **เลือกเอง** ไม่ได้วัด · COO รับเป็นค่าตั้งต้นชั่วคราว (`20260829_1444` ข้อ 1) และสั่งเปิดใบวัดนี้ (ข้อ 2)
> 🔴 **ไม่ block M5** — เข้าคิวรอบที่เจ้าของสะดวก ไม่มีเส้นตาย · ค่าที่วัดได้จะแทนที่เลข 120 หรือยืนยันมัน ทั้งสองอย่างใช้ได้
> 🔴 ใบนี้วัด **ค่า** ไม่ได้วัด **กลไก** — กลไก (ของหมดอายุแล้วคลิกไม่ได้) ถูกเคาะแล้วและมีเทสคุมอยู่ ห้ามอ่านผลใบนี้เป็นคำตัดสินเรื่องกลไก

- objective: (ข้ออ้างเดียว) หลังมอนตาย ของตกลงพื้น และ **ไม่มีใครเก็บ** -- เวลาตั้งแต่ของปรากฏจนของหายจากจอ **เป็นกี่วินาที** (เลขเดียว บวกความคลาดเคลื่อนของวิธีจับเวลา)
- db: สำเนา throwaway `state\run_gt149.sqlite3` · 🔴 ห้ามเปิด canonical `state\pirateforce.sqlite3` · sha256 canonical ก่อน-หลังต้องเท่ากัน
- server args: `py -3 -u -m pirateforce_foundation.app --db state\run_gt149.sqlite3` · **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** (เลนนี้ต้องทำงานโดยไม่ต้องมีแฟล็ก)
- steps:
    0. มาตรฐานบ้าน: LOCK · sha canonical · copy DB · บูตเซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ
    1. เข้าเกม เดินไปหามอนที่ตีได้ · **เริ่มอัดวิดีโอก่อนตีนัดแรก** (วิดีโอคือนาฬิกา ไม่ใช่มือกดจับเวลา)
    2. ตีจนตาย · ของตกลงพื้น · 🔴 **อย่าเข้าใกล้ อย่าคลิกของ** ยืนดูเฉย ๆ ในระยะที่ยังเห็นของ
    3. อัดต่อจนของหายจากจอ · อัดต่ออีก ~15 วินาทีหลังของหาย (กันเคส "หายแล้วกลับมา")
    4. **อย่าออกจากแมพ อย่าล็อกเอาต์** -- ออกจากฉากแล้วเป็นคนละใบ
    5. ปิดไคลเอนต์ → ปิดเซิร์ฟเวอร์ → teardown · เก็บ console `.err` · sha canonical ซ้ำ · ห้าม commit เอง
- pass criteria: 🔴 สองชั้นแยกกัน ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น
    wire/DB (headless ไม่ต้องมีคนหน้าจอ):
      (ก) console มีบรรทัดที่ประกาศ `DROP_LIFETIME_SECONDS` ที่ **บังคับใช้จริงในบูตนั้น** -- คัดดิบ ไม่ใช่คัดจากซอร์ส
      (ข) มีโทเคนตอนของเกิด และโทเคนตอนของถูก prune/หมดอายุ พร้อม timestamp ทั้งคู่ -- ผลต่างสองค่านี้คือคำตอบชั้น wire
      (ค) โทเคนใดขาด ⇒ นั่นคือผลของใบนี้ ⇒ redirect เป็นใบเติม G-OBS ไม่ใช่ FAIL
      ชั้นนี้ตอบไม่ได้: ผู้เล่นเห็นของหายตอนไหน
    client-observable (ต้องมีตาคน):
      เลขวินาทีอ่านจาก **timestamp ของเฟรมวิดีโอ**: เฟรมแรกที่เห็นของบนพื้น → เฟรมแรกที่ไม่เห็นของแล้ว · จดสองค่าและผลต่าง · จด fps ของวิดีโอ (ความคลาดเคลื่อน = 1/fps)
      🔴 จด **สิ่งที่เห็น** ห้ามเดาสาเหตุ · ถ้าของหายเป็นขั้น (จาง → หาย) จดทั้งสองเฟรม
      🔴 G-OBS: จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ไม่มี = chief ไม่บริโภค
      ชั้นนี้ตอบไม่ได้: เซิร์ฟเวอร์ถือว่าของหมดอายุตอนไหน (คนละนาฬิกากับตา)
- nonclaims:
    1. ไม่วัดว่า "คลิกตอนของใกล้หมดอายุแล้วได้ของไหม" -- นั่นคือกลไก มีเทสคุมแล้ว และเป็นคนละใบ
    2. ไม่วัดเคสสองผู้เล่น · ออกจากฉากแล้วกลับ · ของดรอปหลายชิ้น -- เจอเมื่อไรเปิดใบใหม่
    3. **ผลลบมีค่าเท่าผลบวก:** ของไม่หายเลยภายใน 5 นาที ⇒ finding ว่า prune ไม่เดินในบูตไร้แฟล็ก (แพงกว่าเลขที่ผิด) ⇒ redirect เป็นใบแก้ ไม่ใช่ FAIL
    4. เลขที่วัดได้ **ไม่ผูก** ให้ต้องเท่ากับของเซิร์ฟเวอร์ต้นฉบับ -- ใบนี้วัดของเรา
- links: `notes_to_chief/20260829_1347_LANE-B-ASK-COO-how-long-a-drop-stays-pickable.md` · `notes_to_chief/20260829_1444_COO-DECISION-drop-lifetime-120s-interim-approved.md` · `pirate-force-server` `src/pirateforce_foundation/mob_loot.py` (`DROP_LIFETIME_SECONDS`)

### RIDER-149-A [เติมโดย LANE-B รอบ `m0vp7m` 2026-08-29T22:5x+07:00 · ใบเดิมทั้งใบยังใช้ได้ ไม่มีอะไรถูกลบ]

🔴 **ด่านบิลด์ก่อนบูต (ถ้าไม่ผ่าน ห้ามรัน จดว่า NO-RESULT แล้วคืนใบ):** คอนโซลตอนฆ่ามอนต้องมีบรรทัด
ขึ้นต้น `MOB_DROP_PRESENCE` — ถ้าไม่มี แปลว่าสามบรรทัดของใบ `20260829_2246_LANE-B-CORE-REQUEST-*`
ยังไม่ลง main และของยังหายทันทีที่ประกาศเหมือนเดิม

**บรรทัดนั้นตอบ pass criteria ข้อ (ก) ให้เลย** (ประกาศอายุที่บังคับใช้จริงในบูตนั้น คัดดิบ):
`MOB_DROP_PRESENCE state=... live=N announced=N carried=N ... declared_lifetime=120.0s oldest_left=..s label_life=0.2-0.4s redraw=unmeasured`

**ขั้นที่เติม (ดูอย่างเดียว ห้ามคลิกอะไรทั้งนั้น — PANYA-ORDER persist-first ยังเกตใบคลิกอยู่):**
- 2b. หลังมอนตัวแรกตกของแล้ว **นับ ~10 วินาที** แล้วไป **ฆ่ามอนตัวที่สอง** ในระยะที่ยังเห็นจุดที่ของตัวแรกตก
- 2c. จ้องตำแหน่งของ**ตัวแรก**ตอนตัวที่สองตาย: **ป้ายของตัวแรกกลับมาไหม**
- 2d. ทำต่อจากขั้น 3 ของใบเดิมตามปกติ (ยืนดูจนของหายหมด แล้วอัดต่ออีก 15 วิ)

🔴 **ข้อ 2c คือของที่มีค่าที่สุดในใบนี้ตอนนี้** และมันตัดสินข้อที่ยังไม่มีใครวัดเลย:
"การส่งซ้ำวาดป้ายใหม่จริงไหม" (`REEMISSION_REDRAWS_THE_LABEL` ยังเป็น `None` ในซอร์ส)
· **ป้ายกลับมา = ของค้างได้จริงด้วยวิธีนี้** · **ป้ายไม่กลับมา = ผลลบที่มีค่าเท่ากัน** ⇒ แปลว่า
ทางเดียวที่เหลือคือส่งซ้ำถี่กว่านั้น ซึ่งต้องให้ COO เคาะใหม่ ⇒ อย่าเดา ให้จดสิ่งที่เห็น
· ทั้งสองอย่างไม่ใช่ FAIL ของใบนี้

### result (ผู้เทสกรอก)
```
บรรทัด DROP_LIFETIME_SECONDS จากคอนโซล (คัดดิบ) :
บรรทัด MOB_DROP_PRESENCE ของคิลที่ 1 (คัดดิบ) :
บรรทัด MOB_DROP_PRESENCE ของคิลที่ 2 (คัดดิบ · ดู carried= ว่ามากกว่า 0 ไหม) :
โทเคนตอนของเกิด + timestamp :
โทเคนตอนของหมดอายุ + timestamp · ผลต่าง (วินาที) :
วิดีโอ: fps · timestamp เฟรมแรกที่เห็นของ · เฟรมแรกที่ไม่เห็นของ · ผลต่าง (วินาที) :
ป้ายของมอนตัวแรก "กลับมา" ตอนตัวที่สองตายหรือไม่ (เห็น/ไม่เห็น · timestamp เฟรม) :
ของหายเป็นขั้นหรือหายทันที (จดสิ่งที่เห็น) :
path + sha256 ของวิดีโอ/console/DB :
CANON_SHA ก่อน/หลัง · NO-CRASH/CRASH :
OBSERVER_CONFIRMED  :
```

## 🆕 GT-175 SPICE-PARADISE-FIRST-EYES-001 [attended, in-game]: ฉาก 3 (Bg0003, Spice Paradise Island) มีสิ่งมีชีวิตขึ้นจอจริงหรือไม่ -- ตาคู่แรกของโปรเจกต์ในฉากนี้  [~~READY~~ 🟢 **PASS ทั้งสองชั้น — LANE-A รอบ `20260901_1334` 2026-09-01T13:34+07:00 ปิดหัวใบ ตามผล `notes_to_chief/consumed/20260901_1040_GT182-RESULT-PASS-and-GT175-PASS-but-the-first-eyes-batch-still-cannot-close.md`: เจ้าของเข้าฉาก 3 จริง (ผ่าน `/warp 3` ใบแรกของ login, GT-182) เดินสำรวจแล้วชี้ชื่อได้ตรงจอ Sand dragon x3, Columbus, Spice Merchant Reyna, Wizards, Plato — ไม่ใช่เกาะว่างเปล่า; wire ตรงเกณฑ์เป๊ะ `WORLD_CENSUS_BG0003 assembled=62/72 shippable=62 bodies=ok` (10 unresolved เป็นช่องว่างที่รู้อยู่แล้ว ไม่ใช่ FAIL ของใบนี้) · chief ไม่ปิดแทนตามสัญญาผู้บริโภคของใบนี้เอง (broadcast `20260901_1114_FROM_CHIEF_R285_TO_ALL`) → LANE-A ปิดเอง**]

> เปิดโดย LANE-A (สาย A · WORLD) รอบ `p7wm17`, 2026-08-31T20:07+07:00 · `login_entry_allowed` ของฉาก 3
> พลิกเป็น `true` รอบนี้ (`COO-DECISION 20260830_1441`, ประตูที่หกในคิวเดียวกับฉาก 4/5/6/8/10; composer
> `world_population_bg0003.py`/`world_bg0003_identity.py` **สร้าง ผูก และเปิดประตูในรอบเดียวกัน** เหมือน
> ฉาก 5/6/8 (รอบ `l03cgh`/`fx0007`/`p4wire`) -- เหตุผลเดียวกัน: เทสทั่วไป (`tests/test_lane_a_scene_census.py::
> ComposerContractTests`) สมมติไว้แล้วว่าทุกฉากที่ lane นี้ผูก census ให้ต้องเปิดด้วย เพราะฉาก 4/5/6/8/10/14
> เปิดหมดแล้วตอนรอบนี้เริ่ม) -- ไม่ใช่สำเนาของ `GT-166` เพราะฉากนี้**ไม่มี**ความเสี่ยงแบบ `GT-166`: ทะเบียนเอง
> ไม่ระบุฉากนี้ใน `table_row_differences.the_two_interiors` (ตรวจแล้ว ไม่ใช่สมมติ) -- รูปแบบเดียวกับ `GT-165`
> (ฉาก 4) / `GT-171` (ฉาก 5) / `GT-173` (ฉาก 6) / `GT-174` (ฉาก 8)

### objective (claim เดียว)
ล็อกอินเข้าฉาก 3 จริงแล้ว **เห็นตัวละคร/มอนสเตอร์ยืนอยู่บนเกาะเครื่องเทศ** (ไม่ใช่เกาะว่างเปล่า) ใช่หรือไม่ --
คำถามคือ "มีสิ่งมีชีวิตขึ้นจอไหม" ไม่ใช่ "มันโจมตีไหม": composer ของฉากนี้**ตั้งใจไม่ส่ง faction bit เลย** (ดู
`world_population_bg0003.py` docstring -- เป็นคำตัดสินของสาย B ที่ยังไม่ทำ) จึงไม่มีความเสี่ยงแบบ `GT-134`
ที่มอนไม่ก้าวร้าว -- นั่นเป็นพฤติกรรมที่คาดไว้ ไม่ใช่ FAIL ของใบนี้

### ทางเข้า
ไม่มี production path ใดเขียนแถว character ให้ชื่อฉาก 3 เอง (ดู `login_entry_allowed_because` ในทะเบียน) --
เข้าได้เฉพาะ staged GM account (`config/gm_login_scene.json`, scene_id=3) หรือ GM `/warp 3`

### สิ่งที่ยังไม่วัด (บันทึกไว้ล่วงหน้า ไม่ใช่คำทำนายว่าจะพัง)
1. จุดเกิด `MARKER[3]` ยังเป็นชั้นหลักฐาน `authored` เท่านั้น -- ไม่เคยมีไคลเอนต์ยืนจริง, ห่างจาก placement
   ที่ใกล้ที่สุด 405.0 หน่วย (`table_row_differences.marker_geometry_measured_not_enforced`) -- ถ้าตกในหิน/
   หลุดพื้น ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL ของใบนี้ (คำถามของใบนี้คือมี actor ไหม ไม่ใช่พื้นดีไหม)
2. ฉากนี้ไม่มี leader ที่ถูกตัดเพราะชื่อไม่ใช่ ASCII (ต่างจากฉาก 6) -- ตัวที่ถูกตัด 10 ตัวทั้งหมดเป็นเหตุผล
   "ไม่มีแถว MOBS" (1 ตัว) หรือ "s_OUTFIT ว่าง" (9 ตัว) เท่านั้น (ดู `world_bg0003_identity.py` docstring) --
   ไม่ใช่ FAIL ของใบนี้เช่นกัน (composer ข้ามไปแล้วตั้งแต่ต้น ไม่ใช่สิ่งที่ผู้เทสจะเห็นหายไปกลางจอ)
3. ฉากนี้มี 9 sets ที่ multi-variant outfit และ 1 ใน 9 มีเก้าตัวแปร (กว้างที่สุดที่ lane นี้เคยบันทึก) --
   ส่งตัวแปรแรกเสมอตามกติกาเดิม ถ้าตัวละครดูแปลกตาไม่ตรงกับที่คาด ให้บันทึกเป็นข้อมูลแยก ไม่ใช่ FAIL

### pass criteria — สองชั้น
**wire/DB (ปิดแล้วโดยเทส):** console line `WORLD_CENSUS_BG0003 assembled=62/72 ...` ปรากฏหลังล็อกอินเข้าฉาก 3
-- pin ไว้แล้ว `tests/test_lane_a_scene_census.py::SpiceParadiseRegistrationTests::
test_the_real_registry_now_composes_and_that_is_the_round` และ `tests/test_world_population_bg0003.py`
(เทสระดับ composer ตรง)
**client-observable (ยังไม่มีใครยืนดู -- นี่คือสิ่งที่ใบนี้ต้องการ):** ผู้เทสเข้าฉาก 3 จริงแล้วรายงานว่าเห็น
actor ขึ้นจอหรือไม่ (นับคร่าว ๆ พอ ไม่ต้องนับให้ครบ 62)

### สัญญาผู้บริโภค
เปิดโดย LANE-A -- LANE-A บริโภคผลเอง ปิดหัวใบเมื่อผู้เทสยืนยันด้วยตา

### links
`scenarios/world_scene_registry_001.json` แถว `n_id: 3` (`login_entry_allowed_because`) ·
`src/pirateforce_foundation/world_population_bg0003.py`, `world_bg0003_identity.py` ·
`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md` · `GT-165` (scene 4, same
shape) · `GT-171` (scene 5, same shape) · `GT-173` (scene 6, same shape) · `GT-174` (scene 8, same shape) ·
`GT-166` (scene 10, same shape plus the geometry risk this scene does not carry) · `GT-134` (scene 14, same
shape)

**หมายเหตุผู้เขียนใบนี้:** ควรเขียนผ่านเอเจนต์ `pf-queue-author` ตามกติกาของโปรเจกต์ แต่ในสภาพแวดล้อม
รอบนี้ไม่มีเครื่องมือสำหรับ spawn subagent ชนิดนั้น จึงเขียนเองตามรูปแบบของใบ `GT-174`/`GT-173` ให้ใกล้เคียง
ที่สุด -- ถ้ารูปแบบผิดจากมาตรฐานให้แก้ได้ตามที่ `pf-queue-author` เห็นสมควรในรอบถัดไป

## GT-219 GM-IMAGE-CHECKER-MEETS-TWO-REAL-DLLS-001  [✅ PASS ทั้งสองขั้น -- ปิดใบ · ขั้น A `20260904_1508` (ชิ้น (ก) ผ่านครบ · ชิ้น (ข) `A2 NO-RESULT` ปิดถาวร ไม่ rebuild) · ขั้น B `20260904_1911` ข้อ 1 R310: `install.bat` จริง → `image_ok` → `[OK] installed` sha `4a0ecb58…d743b` 14,848 B · DebugView จับ `[GM_PLUGIN] alive` 10 บรรทัด × 2 การเปิด · หน้าต่าง `GMUI` เปิด 3 แท็บ (ภาพ `184909.png`) · NO-CRASH · rollback ครบ · `OBSERVER_CONFIRMED: 2026-09-04T18:49+07:00` · ปิดโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 1 · nonclaim คงเดิม: หน้าต่างเปิด ≠ ปุ่มใน GMUI ทำงาน (P-3 ขั้นถัดไป · LANE-GM)]

> 🔢 **ป้ายเปลี่ยนโดย chief (LANE-E) รอบ `oi2r2n`/R340** ตาม `COO-DECISION 20260904_1648` ข้อ 1 · ผลที่ปลดป้าย: `notes_to_chief/20260904_1508_KA1A-GT219-STEP-A-RESULT-*` (ka1-A · jobs `1497` + `1497b` · ไม่มีเซิร์ฟเวอร์ ไม่มีเกม ไม่แตะ DB)
> **RECHECK 1 = PASS**: `patches\gm_plugin\GameMaster.dll` size=`14848` sha256=`4a0ecb5817c15b0bf08964bc16972bc7340666357c494e9d0308ee9ce72d743b` (certutil + Get-FileHash ตรงกันสองเครื่องมือ) · บรรทัด `RECHECK1=FAIL` ใน log ของ job 1497 **ผิดเพราะฟังก์ชัน `H` ถูก alias `Get-History` บัง** = บทเรียนเครื่องมือ ไม่ใช่ผลวัด
> **RECHECK 2 = NOT FOUND ตามคำทำนาย**: `GameMaster*.dll` ทั้งโฟลเดอร์ (recursive) มีไฟล์เดียวคือ (ก) · ไม่มีตัว 13,824/`67501f7e…f496` ⇒ ตาม `COO 20260903_0213` **เดินต่อด้วย (ก) อย่างเดียว ห้าม rebuild** — negative control ตัวนั้นถูก `mt.exe -outputresource` เขียนทับไปตั้งแต่ R304 และจะไม่กลับมา
> ขั้น A1 `image_ok` `EXIT=0` · `find_mt.bat` เจอ `mt.exe` · `install.bat` ติดตั้งแล้ว rollback แล้ว (โฟลเดอร์ไคลเอนต์กลับเป็น `dir` = 0)
> 🔴 **สิ่งที่ป้ายนี้ไม่ได้พูด (nonclaim ของตัวเครื่องเอง)**: `image_ok` เป็นผลระดับไฟล์ล้วน — **ไม่ได้บอกว่าหน้าต่าง GM เปิด** และไม่ได้บอกว่า manifest ที่ id 2 มี assembly reference ที่ใช้ได้จริง (manifest ว่างหรือผิดเวอร์ชันก็ยังตอบ 14001) · ขั้น B คือสิ่งเดียวที่ตอบข้อนั้น
> ~~เดิม: `[BLOCKED -- ขาดของจริงชิ้น (ข): สำเนา GameMaster.dll 13,824 ไบต์ sha256 67501f7e...f496 ยังไม่มีจดหมายฉบับใดบันทึกว่าถูกเก็บไว้ · RECHECK 2 เป็นตัวปลดป้าย]`~~ — RECHECK 2 ตอบแล้วว่า "ไม่มี" ซึ่ง**คือ**คำตอบของใบ ไม่ใช่การขาดคำตอบ

RECHECK: `certutil -hashfile "<pf_bridge>\patches\gm_plugin\GameMaster.dll" SHA256` ต้องได้ `4a0ecb58...d743b` (14,848 ไบต์) **และ** `dir /b /s "<pf_bridge>\GameMaster*.dll"` ต้องเจอตัวที่ hash เป็น `67501f7e...f496` (13,824 ไบต์) — เจอทั้งคู่ = ปลดเป็น `[🟢 READY]` · ไม่เจอตัวที่สอง = ป้ายคงเดิม เขียนผลบรรทัดเดียวแล้วหยุด

> เปิดตามคำสั่ง `COO 20260903_0148` ข้อ 7 (บรรทัดท้าย: "การวัดสอง DLL ผมสั่ง chief เปิดเป็นใบเทสแล้ว") · ทวงซ้ำถึง chief ใน `COO 20260903_0446` · ทรงของใบมาจาก `COO 20260902_2148` ใบที่ 2 (negative control ของ `check 0/4`) · คำขอต้นเรื่อง: `LANE-GM 20260903_0034` และ `LANE-GM 20260902_2038`
>
> 🔴 **ตัวบล็อกมีข้อเดียว และเป็นเรื่องของ "ของ" ไม่ใช่ของโค้ด**: คำสั่งที่ ka1-A ใช้ในรอบ R304 คือ
> `mt.exe -manifest GameMaster.dll.manifest -outputresource:GameMaster.dll;#2` (ใบ `20260902_1920`)
> ซึ่ง **เขียนทับไฟล์เดิมที่พาธเดียวกัน** 13,824 -> 14,848 ไบต์ ⇒ ตัว 13,824 (negative control) อาจไม่มีอยู่บนเครื่องแล้ว
> 🔴 **ห้าม build ใหม่เพื่อผลิตของชิ้น (ข)** ใบนี้ไม่มีสิทธิ์สั่ง rebuild — ไม่เจอ = ให้ COO/LANE-GM ตัดสินว่าจะทำอย่างไรต่อ
>
> 🔴 **รอบนี้คือการรันครั้งแรกของจริง**: `install.bat` / `find_mt.bat` / `build_vs2008.bat` rev.5 **ยังไม่เคยถูกรันเลยแม้แต่ครั้งเดียว** (คลาวด์ไม่มี Windows ไม่มี cmd ไม่มี `mt.exe` — `LANE-GM 20260902_2038` nonclaim 2 · `20260903_0345` NONCLAIM)
> ⇒ **ถ้าสคริปต์หรือคำสั่งใดตายตั้งแต่บรรทัดแรก ให้คัดข้อความทั้งบรรทัด + `EXIT=` แล้วรายงาน ห้ามแก้สคริปต์ ห้ามไล่ดีบั๊กเอง** สคริปต์ตายบรรทัดแรก = ผลการวัดของใบนี้ ไม่ใช่รอบเสีย

### RECHECK เต็ม (รันตามลำดับ ก่อนแตะอะไรทั้งสิ้น · ไม่ผ่าน = ไม่เดินขั้นถัดไป)
1. ของชิ้น (ก) ยังอยู่และเป็นไบต์เดิม: `certutil -hashfile "<pf_bridge>\patches\gm_plugin\GameMaster.dll" SHA256`
   ต้องได้ `4a0ecb5817c15b0bf08964bc16972bc7340666357c494e9d0308ee9ce72d743b` และ `dir` ต้องได้ **14,848**
   (ที่อยู่ของไฟล์มาจากใบผล `GT-207` หัวข้อ Rollback) · ไม่ตรง = **นี่ไม่ใช่ DLL ตัวที่ `GT-207` โหลดได้** หยุดทั้งใบ ห้ามเดาว่าเป็นตัวเดียวกัน
2. ของชิ้น (ข) มีอยู่ไหม: `dir /b /s "<pf_bridge>\GameMaster*.dll"` แล้ว `certutil -hashfile "<ทุกตัวที่เจอ>" SHA256`
   ต้องหาตัวที่ได้ `67501f7e2c74648473316ff5661433eaebf810f848c2958fb99998db72b5f496` (13,824 ไบต์)
   **คำทำนาย: ไม่เจอ** (เพราะการฝัง manifest เขียนทับที่เดิม) — ทำนายผิดคือข่าวดี
3. สำเนาของตัวตรวจใหม่พอไหม — ตัดสินจากผลของขั้น A1: ต้องมีบรรทัด `GM_PLUGIN_IMAGE ... rules=` ที่มีคำว่า `manifest_id2`
   ไม่มี = checkout เก่ากว่ารอบ `selrsl` ซึ่ง `install.bat` ปฏิบัติเหมือน **ไม่มีเครื่องมือ** ⇒ คำตอบใช้ไม่ได้ทั้งใบ หยุด รายงาน

- objective: (ข้ออ้างเดียว) กฎ `RT_MANIFEST id 2` ของ `pirateforce_foundation.gm.plugin_image_check`
  **แยกแยะ DLL จริงสองตัวได้ถูกต้องหรือไม่** — รับตัวที่คนเห็นกับตาว่าโหลดได้ (ก) และปฏิเสธตัวที่ loader ปฏิเสธ (ข)
  วันนี้กฎนี้ **ยังไม่เคยถูกชี้ไปที่ DLL จริงสักไฟล์** (เทสทั้งชุดเป็น synthetic โดยเจตนา) แต่มันยืนขวางโฟลเดอร์ไคลเอนต์ของเจ้าของอยู่
  · (ก) = `pf_bridge\patches\gm_plugin\GameMaster.dll` 14,848 ไบต์ sha `4A0ECB58...D743B` (ตัวที่ `GT-207` build 1 โหลดได้ หน้าต่าง GMUI เปิด)
  · (ข) = สำเนา 13,824 ไบต์ sha `67501F7E...F496` (ไม่มีเซกชัน `.rsrc` · `LoadLibraryW` ตอบ 14001)
- db: ขั้น A **ไม่แตะ DB เลย** (ตัวตรวจอ่านไบต์อย่างเดียว ไม่ copy ไม่เขียน) · ขั้น B ใช้ `default_state\pirateforce.sqlite3`
  **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ `state\run_gt219.sqlite3` · จด sha256 สำเนาก่อน/หลัง · sha256 canonical เทียบ `CANON_SHA.txt` **ก่อนและหลัง ต้องเท่ากัน** · `PRAGMA integrity_check` = `ok` สองครั้ง
- server args: ขั้น A **ไม่ต้องมีเซิร์ฟเวอร์และไม่ต้องเปิดเกม** · ขั้น B บูตปกติบน `main` ไม่มีแฟล็ก `--*-scenario`:
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt219.sqlite3`
- steps: (playbook: `ATTENDED_SESSION_RUNBOOK.md` · ขั้น B อัดวิดีโอตลอด `LOCK_GAME`)

  **ขั้น A -- ตัวตรวจ อ่านอย่างเดียว ไม่มีการ copy ไม่ต้องบูตอะไร (< 2 นาที)** จาก checkout ของ `pirate-force-server`:
  ```
  cd /d "<pirate-force-server checkout>"
  set PYTHONPATH=src
  py -3 -m pirateforce_foundation.gm.plugin_image_check --dll "<pf_bridge>\patches\gm_plugin\GameMaster.dll"
  echo EXIT=%errorlevel%
  ```
  A1 = คำสั่งข้างบน (ของชิ้น ก) · A2 = คำสั่งเดียวกันแต่ `--dll "<สำเนา 13,824 ไบต์>"` (ของชิ้น ข)
  🔴 **ห้ามเติม `--client-dir` ในขั้นนี้เด็ดขาด** — โฟลเดอร์ไคลเอนต์ตอนนี้ไม่มี `GameMaster.dll` (rollback ของ `GT-207` ลบไปแล้ว) ⇒ `--client-dir` จะได้ `verdict=missing` exit 1 **ทุกครั้ง** แล้วใบนี้จะรายงานผิดเรื่อง
  🔴 **ใส่เครื่องหมายคำพูดทุกพาธ** (พาธของเจ้าของมีช่องว่าง) · คัด **ทุกบรรทัดที่ขึ้นต้นด้วย `GM_PLUGIN_IMAGE` แบบคำต่อคำ** + `EXIT=` ห้ามสรุปเอง ห้ามพิมพ์ใหม่จากความจำ
  A2 รันไม่ได้เพราะหาไฟล์ (ข) ไม่เจอ = เขียน `NO-RESULT (ข)` บรรทัดเดียว **แล้วหยุดทั้งใบตามป้าย BLOCKED**

  **ขั้น B -- attended หนึ่งครั้ง (ทำเมื่อ RECHECK 2 เจอไฟล์เท่านั้น)**
  1. LOCK_GAME · boot stamp (teardown ปฏิเสธ stamp เก่ากว่า **420 นาที**) · sha canonical · copy DB
  2. **เปิด DebugView ค้างไว้ก่อนบูตทุกครั้ง** — ไม่มีตัวจับ `[GM_PLUGIN]` = อ่านผลไม่ได้เลย
  3. ติดตั้งของชิ้น (ก): `install.bat "C:\Users\Panya\Desktop\Pirate Force\GameClient"` **ห้าม copy เอง**
     · ถ้าขึ้น `[FAIL] plugin_image_check refused this file.` ⇒ คัดบล็อกทั้งหมด แล้วรันซ้ำแบบทิ้งหลักฐาน:
       `set PFGM_FORCE=1` แล้ว `install.bat "C:\Users\Panya\Desktop\Pirate Force\GameClient"`
       คัดบรรทัด `[FORCED] verdict=... rules=...` **ทั้งสองที่** + พาธ `%TEMP%\pf_gm_forced_installs.log`
     · 🔴 ถ้าขึ้น `[STOP] A GameMaster.dll ALREADY EXISTS` = **หยุดทั้งใบ** เก็บ sha256 ที่มันพิมพ์ แล้วรายงานทันที (นั่นคือของที่ตามหามาตั้งแต่ 27 ส.ค.) · `PFGM_FORCE` **ไม่มีผลกับด่านนี้** โดยการออกแบบ
  4. **เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ** · ล็อกอินบัญชีที่ยืนยันแล้วว่าอยู่ใน `config/gm_accounts.json`
  5. **กดปุ่ม GM หนึ่งครั้ง** (ปุ่มเดียวกับ `GT-207`) · ถ่าย **full-res S1** ตอนกด และ **S2** สภาพหลังกด (เปิดหรือไม่เปิดก็ถ่าย)
     🔴 **ห้ามพิมพ์ตัวอักษรตลอดรอบ** (ตัวอักษรตอนช่องแชทไม่โฟกัส = ฮอตคีย์) · ไม่ต้องเดินไปไหน
  6. NO-CRASH ด้วย **คลิกขวาค้างลาก** เท่านั้น (หมุน **กล้อง** อย่างเดียว ไม่เปลี่ยน facing ไม่มีไบต์ขึ้นไวร์)
     🔴 **ห้ามใช้ `Q`/`E` หรือ `W/A/S/D` เป็นตัวเช็ค** — มันเปลี่ยน facing และยิง `TargetPosVital`
  7. ออกเกมด้วย X มุมขวาบน · ปิดเซิร์ฟเวอร์ (**ฆ่าไคลเอนต์แล้วต้อง restart เซิร์ฟเวอร์ก่อนบูตหน้า ไม่งั้นค้าง "connecting" ตลอดกาล**)
  8. **rollback เสมอ ไม่ว่าผลจะเป็นอะไร**: ลบ `GameMaster.dll` ที่ติดตั้งออกจากข้างไคลเอนต์ แล้วยืนยันว่าหายจริง · teardown เสมอ · sha canonical ซ้ำ · `integrity_check` · ห้าม commit เอง

- pass criteria: (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB          : ผลิตได้โดยไม่ต้องมีคนอยู่หน้าจอ --
      (1) **A1**: `verdict=` + `failed_rules=` + `rules=` + `sha256=`/`size=` + `EXIT=` ครบทุกบรรทัดคำต่อคำ (คาด `sha256=4a0ecb58...` `size=14848`)
      (2) **A2**: ชุดเดียวกันของไฟล์ 13,824 (คาด `sha256=67501f7e...` `size=13824`)
      (3) ขั้น A **ต้องไม่มีการ copy ใด ๆ เกิดขึ้น** — โฟลเดอร์ไคลเอนต์ยังไม่มี `GameMaster.dll` หลัง A1/A2 (`dir` ยืนยัน)
      (4) ขั้น B: บรรทัดที่ `install.bat` พิมพ์เองทั้งชุด (`[ok]`/`[warn]`/`[FAIL]`/`[FORCED]`/`[OK] installed:` + sha256 ของ certutil)
          · ไฟล์ที่ติดตั้ง sha256 = `4a0ecb58...` · หลัง rollback ไฟล์หายจริง
      (5) sha256 canonical ตรง `CANON_SHA.txt` ก่อน/หลัง · `integrity_check` = `ok` สองครั้ง · ไม่มี traceback ที่ไม่ถูกจับ
      ชั้นนี้ **ตอบไม่ได้**: หน้าต่าง GMUI เปิดหรือไม่ · บนจอเห็นอะไร · สีป้ายชื่อ
    client-observable: **ต้องมีคนอยู่หน้าจอเท่านั้น ห้ามอนุมานจากคอนโซลหรือจาก verdict**
      (1) หลังติดตั้ง (ก) แล้ว **กดปุ่ม GM แล้วหน้าต่างชื่อ `GMUI` เปิดหรือไม่** (เปิด/ไม่เปิด อย่างเดียว ไม่ตีความ)
      (2) NO-CRASH/CRASH ตอนกด และตอนปิดเกม · มีข้อความระบบขึ้นไหม (คัดเป๊ะ + สี)
      (3) 🔴 **จดสีป้ายชื่อทุกป้ายในทุกภาพ หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** อ่านจาก **full-res เท่านั้น** · ไม่มีป้ายให้เขียน `none` ห้ามเว้นว่าง
          **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (เจ้าของคำถามคือ `RE-067`) · ต่างจากภาพของเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ
      ชั้นนี้ **ตอบไม่ได้**: ตัวตรวจว่าอะไร · exit code เท่าไร · มีการ copy เกิดขึ้นหรือไม่
      🔴 **G-OBS**: จดหมายผลต้องมีบรรทัด `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · ไม่มี = `AWAITING-OBSERVER` ไม่ใช่ `PASS`

- คำทำนาย (**เป็นคำทำนาย** · ทำนายผิด = ผลการวัด ไม่ใช่ความล้มเหลว · **ผลลบมีค่าเท่าผลบวก**):
    P1 A1 = `image_ok` exit 0 · A2 = ปฏิเสธ (คาด `manifest_missing`, `failed_rules` มี `manifest_id2`) exit ไม่เป็น 0 ⇒ กฎ id 2 แยกของจริงได้ถูกทั้งสองทาง
    P2 🔴 **A1 ถูกปฏิเสธ** = ผลลบที่มีค่าที่สุดของใบนี้: กฎ id 2 ปฏิเสธ DLL ที่คนเห็นกับตาว่าโหลดได้ ⇒ **เราบล็อก P-3 ด้วยมือเราเอง**
       ⇒ คำสั่งยืนของ COO: **ลดกิ่ง id 2 เป็น advisory ทันที ไม่ต้องถาม** (คนลงมือคือ LANE-GM ไม่ใช่ผู้เทส) · ผู้เทสเดินขั้น B ต่อด้วย `PFGM_FORCE=1`
    P3 **A2 = `image_ok`** ⇒ เกตนี้ไม่เคยกันอะไรได้เลย · ตั้งแต่จุดนั้น `check 0/4` และ verdict **ห้ามถูกอ้างเป็นหลักฐานว่า DLL ครบ** เหลือเกต `.rsrc` (`dumpbin`) ตัวเดียว
    P4 ตัวตรวจรันแล้วไม่พิมพ์บรรทัด verdict เลย = **สภาพแวดล้อมพัง** (Python 2 · checkout ไม่ครบ) ไม่ใช่คำพูดเกี่ยวกับไบต์ชุดนั้น ⇒ จดคำต่อคำแล้วรายงาน

- nonclaims:
  1. **ไม่พิสูจน์ว่า `install.bat` ทั้งไฟล์ถูกต้อง** — ใบนี้แตะเฉพาะกิ่งตัวตรวจภาพ ไม่แตะกิ่ง `dumpbin`/`find_mt`/`build_vs2008.bat`
  2. `image_ok` แปลว่า **id ถูก** ไม่ได้แปลว่า **เนื้อ manifest ใช้ได้** — manifest ที่ id 2 แต่ว่างหรือเวอร์ชัน CRT ผิด ยังตอบ 14001 อยู่ดี
  3. ไม่พิสูจน์ว่า loader ยอมรับ/ปฏิเสธ manifest ที่ id 1 (นั่นคือขั้น `0N-b` ของ `GT-207` คนละคำถาม)
  4. หน้าต่างเปิด **ไม่ใช่** ข้อพิสูจน์ว่าคำสั่ง GM ใดทำงาน และไม่ใช่ไมล์สโตน · ใบนี้ไม่ให้สถานะ GM กับใคร
  5. ไม่แตะฝั่งเซิร์ฟเวอร์เลย — ไม่มีเฟรม GM ใหม่ ไม่มี vital ไม่แตะ `runtime.py` · ผลของใบนี้ **ไม่ย้าย NOW.md P-3** ด้วยตัวมันเอง
  6. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ (`RE-067`) · ไม่พิสูจน์ว่าเครื่องอื่นนอกจากเครื่องเจ้าของมี `mt.exe`/Python/`dumpbin`
  7. ผลของ (ข) ไม่พูดถึงคุณภาพของ DLL ที่จะ build ในอนาคต — พูดถึง **เครื่องมือวัด** ว่าขยับหรือไม่ขยับเมื่อชี้ไปที่ของที่รู้ว่าเสีย

- result: (ผู้เทสกรอก) ผล RECHECK สามข้อ · บรรทัด `GM_PLUGIN_IMAGE` + `EXIT=` ของ A1 และ A2 ครบคำต่อคำ ·
  บรรทัดทั้งชุดที่ `install.bat` พิมพ์ (รวม `[FORCED]` ถ้ามี) · sha256 ก่อน/หลังติดตั้ง · เปิด/ไม่เปิดหน้าต่าง GMUI ·
  ตารางสีป้ายชื่อทุกภาพ · rollback ทำแล้วหรือยัง · ผลเต็มไปที่ round file + จดหมายผล ไม่ใช่ในใบนี้

- links: `COO 20260903_0148` · `COO 20260903_0446` · `COO 20260902_2148` · `LANE-GM 20260903_0345` · `LANE-GM 20260903_0034` · `LANE-GM 20260902_2038` · `KA1A 20260902_1915` (ผล `GT-207`) · `KA1A 20260902_1920` · `GT-207` · `patches/gm_plugin/install.bat`

**ผู้เปิดใบ: chief (สาย E) รอบ R314 `bbm6xn` ตาม `COO-DECISION 20260903_0148` ข้อ 7 และ `20260903_0446` -- ผู้บริโภคผล: chief (สาย E)**

## GT-228 ISLAND-CONTACT-TRIGGER-FRAME-CAPTURE-001  [🟢 **PASS (กล่อง B) — ปิดโดย chief (LANE-E) รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00**] ~~[OPEN -- เจ้าของใบ LANE-A · ร่างตาม `COO-DECISION 20260904_0409` ข้อ 2 · 🔴 **ใบนี้เป็นใบ "เก็บ hex" ไม่ใช่ใบตัดสินการเทียบท่า**]~~

> 🟢 **ผล PASS — R308 (Panya นั่งหน้าจอทั้งใบ) · `OBSERVER_CONFIRMED: 2026-09-04T13:22+07:00`**
> 🔴 **บิลด์ที่บูต = `pirate-force-server` commit `d8969729bcdf7f6880d1b18595ea8aea77e4a7f7` ไม่ใช่หัว `main`** (deviation 1 ของใบผล: resolver เลือกคอมมิตเขียวล่าสุด · main ขยับทุก ~10 นาที) — ใครก็ตามที่เอา XYZ/id จากใบนี้ไปใช้ต้องรู้ว่ามันวัดบนบิลด์นี้ ไม่ใช่บน main
> ผลเต็ม: `notes_to_chief/20260904_1331_KA1A-R308-RESULTS-gt228-pass-box-B-island-contact-fires-triggervital-id-2-at-prison-exile-and-id-3-at-spice-paradise-not-153-154.md`
> รับเป็นคำตัดสิน: `notes_to_chief/20260904_1345_COO-DECISION-lane-a-gt228-pass-*` (COO 13:45)
> เกณฑ์ของใบนี้คือ "ได้ hex ครบสองเกาะ" ไม่ใช่ "หน้าต่างเด้ง" — ครบตามนั้น: ชนเกาะ = ไคลเอนต์ยิง `TriggerVital 0x1FB2` id **2** (Prison Exile, 3/3) และ id **3** (Spice Paradise, 2/2) · คำทำนาย id 153/154 **ตกไป** · XYZ วัดจากเฟรมจริง (rx152 `-5613.8, 4162.5, 186.0` = เกาะ 2 · rx433 `-1563.5, -5275.1, 186.0` = เกาะ 3)
> 🔴 ใบนี้ **ไม่** ตัดสินว่าเทียบท่าได้ และ **ไม่** พิสูจน์ว่า id = เลขฉากปลายทาง (นั่นเป็นสมมติฐานหลักที่ COO รับไว้ ยังไม่พิสูจน์) — ใบที่จะตัดสินคือ `GT-233` (M2 provisioning trial) · ทางสำรองคือ `RE-234`
> ผู้บริโภคผลคือ **LANE-A** ตามกฎ "ใครเปิดใบคนนั้นบริโภค" — chief ปิดหัวใบให้ตามคำสั่ง `COO 20260904_1346` ข้อ 2(จ) เท่านั้น

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `3kwnnr`/R332 2026-09-04T05:2x+07:00 ตาม `COO-DECISION 20260904_0344` ข้อ 3** — ตัวนับร่วมสองคิว + archive คืน `226` (ใบ `GT-226` ของรอบเดียวกัน) ⇒ ใบนี้ `GT-228` · `GT-228` = 0 hit ทั้งสามที่ก่อนวาง · เนื้อใบวางทั้งก้อนตามที่ LANE-A ร่าง ไม่แก้ถ้อยคำใด ๆ นอกจากเติมเลขใบ · **เจ้าของใบและผู้บริโภคผล = LANE-A**


> เปิดโดย LANE-A · ผลกลับมาที่ LANE-A · numbering: ตัวนับร่วมกับ `CLIENT_RE_QUEUE.md` — **chief เป็นคนตั้งเลข ผู้เทสห้ามตั้งเอง**
> บูต/DB/teardown ตาม `BRIDGE_BOOT_PROCEDURE.md` + `ATTENDED_SESSION_RUNBOOK.md` · **รัน teardown เสมอ** แม้รอบจบเพราะเลิกเล่นเฉย ๆ (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที)
> เวลาบนจอ ~20-25 นาที · ต้องมีคนนั่งหน้าจอทั้งใบ

- objective: ข้อพิสูจน์เดียว -- **เรามี hex ดิบของทุกเฟรมที่ไคลเอนต์ส่งออก ณ จังหวะที่เรือ "ชน/เข้าเขต" เกาะ 2 (Prison Exile Island) และเกาะ 3 (Spice Paradise Island) ในฉาก 126 ครบทั้งสองเกาะ**
  🔴 **เกณฑ์ผ่านคือ "ได้ hex ของเฟรมตอนชน ครบสองเกาะ" ไม่ใช่ "มีหน้าต่างเด้ง"** · หน้าต่างจะเด้งหรือไม่เด้ง ใบนี้ผ่านได้ทั้งคู่ ขอแค่ไบต์ครบและมีคนยืนยันว่าจอเป็นอย่างไรตอนนั้น
  ~~สมมุติฐานที่ใบนี้ไปทดสอบ (เป็นคำทำนาย ไม่ใช่ผลวัด): ตอนชนเกาะ ไคลเอนต์ยิง opcode เดิม `TriggerVital 0x1FB2` แต่ถือ trigger id ของแถวเกาะ = `153` Prison Exile Island · `154` Spice Paradise Island~~
  🆕 **คำทำนายใหม่ (LANE-A รอบ 09:51 ตาม `RE-227`/`COO-DECISION 20260904_0747` ข้อ 3(ค) — แทนคำทำนาย `0x1FB2` ข้างบน)**: RE-227 (static ครบ CFG) พินแล้วว่าเส้นทาง NavigationEx contact tick **ไม่มี direct call ไปยัง outbound submit, TriggerVital allocator หรือ TriggerVital serializer เลย** ⇒ **คาดว่าตอนเรือชน/เข้าเขตเกาะจะไม่มีเฟรมใดออกจากไคลเอนต์เลย** (หน้าต่างรายงานกัปตัน ถ้าเด้ง เป็น local proximity check ล้วนของไคลเอนต์ ไม่ผูกกับไบต์ออกสาย) — **หน้าต่างว่างเปล่าในช่วงชนคือผลที่คาดไว้ ไม่ใช่รอบล่ม** สิ่งเดียวที่ยังไม่รู้และใบนี้ต้องวัดคือ **XYZ จริงของเกาะ 2/3** (อ่านจาก HUD ตามข้อ 🆕 ในขั้น 9-11 ข้างล่าง) เพื่อให้ `LANE-A` ประกอบ encoder `NavigationEx_AddSurveyDataVtial` ได้โดยไม่ต้องเดา
  ที่มาของสองเลขนี้: รอบ `xv20xj` ไล่จากตารางของไคลเอนต์เอง -- `TEXTDATA_TH__Trigger_TIP` แถว `152..167` เป็นบล็อกปลายทางการเดินทางติดกันทั้งบล็อก ชื่อตรงตัวกับตารางชื่อฉาก และเพดานเลเวลตรงกับ `n_SCENE_LV` ครบ 10 แถว ⇒ **เป็นความเข้ากันได้ ยังไม่ใช่การพิสูจน์** ไม่เคยมีใครเห็นไบต์ของ `0x1FB2` ที่ถือ id `153`/`154` เลยสักครั้ง

- ของที่รู้แล้วจากรอบก่อน (R307 · `notes_to_chief/20260903_1901_KA1A-R307-RESULTS-*.md`) -- อ่านตรงนี้พอ ไม่ต้องไปเปิดไฟล์:
  ฉากมหาสมุทรคือ `scene_id 126` (model `Bg3001` ชื่อบนจอ "Atlantic Ocean: Rising Sun Sea") · ในฉากนี้ **ตัวละครคือเรือ** HUD เป็นเข็มทิศแทนมินิแมป · จุดเกิด HUD อ่านได้ `X 3,050 Y 232`
  ระหว่างแล่นเรือ ไคลเอนต์ส่ง `TriggerVital 0x1FB2` **5 ครั้ง ครั้งละ 69 ไบต์** รูปเฟรม:
  `12 B2 1F 0B 01 0F <u16 trigger> 00 0B 04 2A <x> 2A <y> 2A <z=186.0>` แล้วต่อด้วย position vital
  trigger id ที่เห็นคือ `40 / 51 / 3 / 57 / 36` = **prop ทะเลทั้งห้า** (Black Braid Landmine · Magic Egg · Seafood Cargo · Black Charm Demon Flower · Offer Altar) · **เซิร์ฟเวอร์ไม่ตอบสักเฟรม** (5 ส่ง 0 ตอบ)
  ผู้เทสรอบนั้น **เห็นเกาะ Spice Paradise และ Prison Exile ในฉากนี้จริง** และบนเซิร์ฟเวอร์จริงการแล่นเข้าใกล้จะเด้งหน้า "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]" -- ของเรายังไม่เด้ง

- 🔴 PRECONDITION ที่ต้องเช็คจริงก่อนขั้น 1 (ไม่ใช่หมายเหตุ):
  P1. **ตัวพิมพ์คอนโซลของใบนี้อาจยังไม่ทำงาน**: รอบนี้มี log-only hook ชื่อ `pirateforce_foundation.lane_hooks.lane_a_island_trigger_log` ที่พิมพ์หนึ่งบรรทัดต่อหนึ่งเฟรม `0x1FB2` ขาเข้า
      ~~แต่ **มันถูกลงทะเบียนแล้วยังไม่มีใครยิง** -- `runtime.py` ยังไม่มีจุดเรียกจนกว่า chief จะลง CORE-REQUEST หนึ่งบรรทัด~~
      🆕 **แก้โดยเจ้าของใบ (LANE-A) รอบ `azhl15` 2026-09-04T07:5x+07:00 ตามจดหมาย chief `20260904_0638`**: จุดเรียกลง `main` แล้ว -- `runtime.py` กิ่ง `nested_id == legacy.TRIGGER_VITAL` เรียก `lane_hooks.fire("vital_inbound_trigger_vital", ...)` ทุกเฟรมขาเข้า (commit `5efb55d` R333 · วัดด้วย `git merge-base --is-ancestor` = ancestor ของ `origin/main` จริง รอบ `azhl15`)
      ⇒ **คาดว่าจะเห็นบรรทัด `LANE_A_TRIGGER_VITAL ...` หนึ่งบรรทัดต่อหนึ่งเฟรม `0x1FB2` ขาเข้า** (รอบ `azhl15` ขับ **เฟรมจับจริงของ R307 หนึ่งเฟรม (60 ไบต์ที่จดหมายยกมา · เฟรมบนสาย 69 ไบต์)** ผ่าน dispatcher จริงแบบ headless แล้วได้บรรทัดทุกครั้ง ไม่มีไบต์ออก · แก้ถ้อยคำรอบ `azhl15b` ตามผล `pf-adversary` — ของเดิมเขียนว่า "ครบทุกเฟรม" ซึ่งเกินจริง)
      🆕 **P1-a (รอบ `azhl15b` · precondition ที่ต้องรันจริงก่อนบูต ไม่ใช่หมายเหตุ)**: `git -C <โคลนที่จะบูต> merge-base --is-ancestor 5efb55d HEAD; echo $?` **ต้องได้ `0`**
      ไม่ได้ `0` = โคลนยังไม่มีจุดยิง ⇒ `git pull` ก่อน แล้วค่อยบูต · **ห้ามเดินใบด้วยโคลนที่ตอบไม่ใช่ `0`** แล้วไปสรุปว่า "hook ไม่ทำงาน" (บรรทัดฐานเดียวกับ `GT-045` v2 ข้อ (ข))
      🆕 **P1-b (รอบ `azhl15b`)**: บรรทัด `UNPARSED` ที่ hex **มี `0f9900` หรือ `0f9a00` อยู่ข้างใน = สัญญาณเกาะ ให้คัดมาด้วยทุกบรรทัด**
      (แปลว่า walker เดินไปไม่ถึงฟิลด์ ไม่ได้แปลว่าเฟรมไม่มี id เกาะ) · 🔴 อย่ารายงานว่า "ไม่เจอสตริง คำทำนายผิด" ถ้ายังไม่ได้ไล่ดู hex ของบรรทัด `UNPARSED`
      🆕 **P1-c (รอบ `azhl15b` · วัดแล้วในเทส)**: `parse_outer` ของเซิร์ฟเวอร์อ่าน **nested vital ตัวแรกตัวเดียว** ⇒ ถ้าเฟรมตอนชนเกาะส่ง `TriggerVital` มาเป็น **vital ตัวที่สอง** กิ่งจะไม่ถูกเลือก **คอนโซลจะเงียบสนิท**
      ⇒ **คอนโซลเงียบ + capture มี `12 B2 1F` อยู่จริง = เคสนี้ ไม่ใช่ "hook พัง" และไม่ใช่ FAIL** · บันทึกไว้ตรง ๆ แล้วเดินใบต่อ (R307 ได้ TriggerVital เป็นตัวแรกทั้งห้าเฟรม ซึ่งยังไม่มีใครพิสูจน์ว่าเฟรมชนเกาะจะเรียงแบบเดียวกัน)
      ⇒ ตอนบูต ให้มองหาโทเคนนี้ใน **stderr**: `LANE_HOOK_REGISTERED pirateforce_foundation.lane_hooks.lane_a_island_trigger_log vital_inbound_trigger_vital`
      **ไม่เจอ** (ไม่ว่าโทเคนลงทะเบียน หรือบรรทัดต่อเฟรม) ⇒ เขียนในผลว่า "ครึ่งคอนโซลของใบนี้ผลิตอะไรไม่ได้ในบิลด์นี้" พร้อมระบุว่าบิลด์ที่บูตเป็น commit ไหน แล้ว **เดินใบต่อตามปกติ** · 🔴 **ห้ามรายงานเป็น FAIL** และ **ห้ามแก้โค้ดเองเพื่อให้มันยิง**
      **ครึ่งจับแพ็กเก็ตทำงานได้เสมอ ไม่ขึ้นกับ hook นี้** -- ครึ่งนั้นคือครึ่งที่ตัดสินใบ · 🔴 **บรรทัดคอนโซลไม่ใช่ตัวตัดสินใบ และไม่ใช่หลักฐานว่าเทียบท่าได้** -- ใบนี้ยังเป็นใบ "เก็บ hex" เหมือนเดิมทุกประการ (ดูหัวใบ) · บรรทัด `ISLAND` แปลว่า "ไคลเอนต์ยิง trigger id ที่ตารางของไคลเอนต์เองเรียกว่าเกาะ" เท่านั้น ไม่ได้แปลว่าเซิร์ฟเวอร์เข้าใจหรือตอบอะไร
  P2. **เกาะ 3 มีเกตเลเวล Lv.25** (ตารางของไคลเอนต์เองสองตารางตรงกัน) · **เกาะ 2 ไม่มีเกต**
      ตัวละครเทสเลเวล 1 อาจได้ **ข้อความปฏิเสธ "เลเวลของท่านไม่เพียงพอ"** ที่เกาะ 3 แทนหน้ารายงานกัปตัน
      🔴 **นั่นคือ RESULT ไม่ใช่รอบล่ม** -- การถูกปฏิเสธแปลว่า **มีการตรวจจับการชนเกิดขึ้นแล้ว** ซึ่งเป็นข้อมูลที่ใบนี้ต้องการ · คัดข้อความตามตัวอักษรที่เห็น + ภาพนิ่ง
  P3. **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** · ไคลเอนต์ที่ถูกฆ่า = เซิร์ฟเวอร์ยังถือเซสชันไว้ ตัวถัดไปจะค้าง "connecting" ตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเปิดไคลเอนต์ใหม่ทุกครั้ง**
      และ **ห้ามเปิดไคลเอนต์ทิ้งไว้โดยไม่มีเซิร์ฟเวอร์** (ตายเองใน ~3.5 นาที)
  P4. ใบนี้ **ต้องปิดไคลเอนต์แล้วเปิดใหม่หนึ่งรอบ** ตามเส้นทางเข้าฉาก ⇒ ตอนเปิดใหม่ให้ **รีสตาร์ตเซิร์ฟเวอร์ก่อนตาม P3**

- db: canonical = `state\pirateforce.sqlite3` -- 🔴 **สำเนาเท่านั้น ห้ามเปิดไฟล์ canonical** ⇒ คัดลอกเป็น `state\run_gt228_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา
  จด sha256 ของสำเนาก่อน/หลัง · จด sha256 ของ canonical ก่อน/หลัง แล้วยืนยันว่า **ไม่เปลี่ยน** · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง
  (รอบคัดลอก DB ⇒ ตำแหน่งตัวละครกลับไปจุดเกิดทุกบูต **เป็นเรื่องปกติ ไม่ใช่ผลวัด**)

- server args: บูตมาตรฐาน · **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` · บัญชี GM ใน `config/gm_accounts.json`
  🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)** -- โทเคนของเลนนี้ออกทาง stderr ล้วน
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt228_<stamp>.sqlite3 2>&1
  ```
  ต้องมีตัวจับแพ็กเก็ตเปิดอยู่ตลอดใบ: `capture_v141\GAME_LIVE.txt` (hex ดิบ) และ `GAME_EVENTS_LIVE.txt`

- steps: (คลิกตามลำดับ · **จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา"** -- เวลาเหล่านี้คือสิ่งที่ใช้ตัดหน้าต่าง hex ทีหลัง ถ้าไม่จด ไบต์ที่จับได้จะตัดไม่ออก)
  1. PRECONDITION P1-P4 ผ่านก่อน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB เป็น run copy
  2. บูตเซิร์ฟเวอร์ใหม่สด · คัดบรรทัด `LANE_HOOK_REGISTERED ...` (หรือเขียนว่า "ไม่มี") · เปิดตัวจับแพ็กเก็ต
  3. บูตไคลเอนต์ · ล็อกอิน · ภาพนิ่ง `S00-HOME` เต็มความละเอียด
  4. คลิกช่องแชท **ยืนยันว่า focus จริงก่อนพิมพ์** (พิมพ์ตอนไม่ focus = ตัวอักษรกลายเป็นฮอตคีย์) · พิมพ์ `/warp 126` · Enter
     🔴 `/warp` เป็นคำสั่ง GM **ไม่ใช่** ตัวยิงแชทที่ต้องยาว **12 ตัวอักษร ASCII พอดี** ของใบอื่น ⇒ **ห้ามเติมตัวอักษรให้ครบ 12**
  5. **จอไม่เปลี่ยนฉาก = ผลที่คาดไว้** (`/warp 126` สเตจไว้ให้ล็อกอินครั้งถัดไป ไม่วาปสด) · คัดบรรทัดคอนโซลที่ตอบกลับ
  6. **ปิดไคลเอนต์ด้วยปุ่ม X** -> **รีสตาร์ตเซิร์ฟเวอร์ (P3)** -> เปิดไคลเอนต์ใหม่ -> ล็อกอินตัวละครเดิม -> รอโหลดจนจบ
  7. ภาพนิ่ง `S126-SPAWN` ทันทีที่โหลดเสร็จ **ยังไม่กดอะไรเลย** · **จดเวลา** · ยืนยันว่าเห็น HUD เข็มทิศและตัวเองเป็นเรือ
  8. หาเกาะด้วยการหมุน **กล้อง** อย่างเดียวก่อน: **คลิกขวาลาก** (หมุนกล้องล้วน ตัวละครไม่หัน ไม่มีไบต์ออกสาย ปลอดภัยทุกจังหวะ) · ภาพนิ่ง `S126-LOOK1..3`
  9. **แล่นเข้าชนเกาะ 2 (Prison Exile Island) ก่อน** (ไม่มีเกตเลเวล) ด้วย `W/A/S/D` และ `Q`/`E`
     🔴 ใบนี้ **ต้องการ** ให้ตัวละครขยับและหันจริง (`W/A/S/D` และ `Q`/`E` หัน **ตัวละคร** และยิง `TargetPosVital` ออกสาย -- นั่นคือสิ่งที่ต้องการ ไม่ใช่ของต้องห้ามในใบนี้)
     🔴 **ห้ามคลิกซ้ายใส่เกาะ** -- คลิกเป็นคนละเส้นทาง (R307 เห็นเกาะ "หันหน้าเข้าหาเรา" เมื่อคลิก) · ใบนี้พิสูจน์ **การชน** เท่านั้น
     ภาพนิ่ง `S126-ISL2-APPROACH` ตอนเข้าใกล้ · **จดเวลา** วินาทีที่เรือแตะเกาะ · ภาพนิ่ง `S126-ISL2-CONTACT` ภายใน ~2 วิ · ค้างนิ่ง ~10 วิ · ภาพ `S126-ISL2-AFTER`
     🆕 **(LANE-A รอบ 09:51 ตาม `COO-DECISION 20260904_0747` ข้อ 3(ค)) ทุกครั้งที่เรือแตะเกาะ: อ่านและจด HUD พิกัด `X Y` ของเรือ ณ จังหวะสัมผัสจากภาพ `S126-ISL2-CONTACT`** (HUD เข็มทิศของฉากนี้แสดงพิกัดแบบเดียวกับที่จดไว้ตอน spawn `X 3,050 Y 232`) — **ใบนี้กลายเป็นแหล่ง XYZ ของเกาะ ที่ `NavigationEx_AddSurveyDataVtial` encoder ของ LANE-A ต้องใช้ ห้ามเดา**
  10. ถอยออกมา ~5 วิ แล้ว **แล่นเข้าชนเกาะ 2 ซ้ำอีกครั้งที่สอง** (จดเวลาใหม่ · ภาพ `S126-ISL2-CONTACT-B` · 🆕 จด HUD `X Y` ซ้ำจากภาพนี้ด้วย) -- ซ้ำเพื่อพิสูจน์ว่าสิ่งที่จับได้ทำซ้ำได้ ไม่ใช่ของบังเอิญ
  11. **ทำขั้น 9-10 ซ้ำทั้งชุดกับเกาะ 3 (Spice Paradise Island)** · ภาพ `S126-ISL3-APPROACH` / `-CONTACT` / `-AFTER` / `-CONTACT-B` · **จดเวลาทุกครั้ง** · 🆕 **จด HUD `X Y` จากภาพ `S126-ISL3-CONTACT` และ `S126-ISL3-CONTACT-B` เช่นเดียวกับเกาะ 2**
      ถ้าเจอข้อความปฏิเสธเรื่องเลเวล ⇒ **คัดข้อความตามตัวอักษร** + ภาพนิ่ง + จดเวลา แล้ว **เดินใบต่อจนจบ** (ดู P2)
  11ก. 🆕 **อ่านคู่พิกัด HUD ตอนเกิด แล้วเทียบกับตารางของไคลเอนต์ (LANE-A รอบ `npbdgr` 2026-09-04T10:58+07:00 · เจ้าของใบแก้เอง) — 10 วินาที ไม่มีความเสี่ยง**
      ตอนอยู่ที่จุดเกิดของฉาก 126 (ก่อนเริ่มขั้น 9 ก็ได้ หรือย้อนมาทำตอนจบก็ได้) **จดเลข HUD `X Y` ตามตัวอักษร + ภาพนิ่ง `S126-SPAWN-HUD`**
      🔴 **ทำไม**: `gamedata/tables/CONSTDATA_TH__MARKER.tsv` (sha256 `723c713a...67dc`) แถว `n_ID 17` ของฉาก 126 คือ
      `n_X 3050 · n_Y 232 · n_Z 90` — **ตรงกับเลข HUD ตอนเกิดที่ R307 จดไว้ (`X 3,050 Y 232`) ทั้งสองตัวพอดี**
      ⇒ คู่เลขบน HUD คือ `x`/`y` ของโลกในกรอบเดียวกับตาราง marker · การอ่านซ้ำในบูตนี้คือการยืนยันว่าบูตนี้ก็ยังเป็นกรอบเดิม
      **ต่างจากที่จดไว้ = finding ชิ้นใหญ่ เขียนแยกทันที** (แปลว่ากรอบพิกัดของ HUD ไม่คงที่ และเลขจากขั้น 9-11 แปลงไม่ได้)
      🔴 **ไม่ต้องหาเลขที่สามจาก HUD**: ตาราง marker ให้ระนาบของผู้เล่นในฉากนี้ = `n_Z 90` (10 ใน 11 แถว) ส่วนเกาะสี่ก้อน
      ที่ไคลเอนต์วางไว้ในฉากเดียวกันอยู่ที่ `z` 123.57-123.64 ⇒ **ต่างกัน ~33.6** และเพราะไคลเอนต์เช็กด้วยระยะ **กำลังสอง**
      เทียบ 500 (`RE-227`) ระยะแนวราบที่ยังชนได้ = `sqrt(500^2 - 33.6^2)` = **498.9**
      🔴 **บรรทัดนี้เป็นการคำนวณบน `z` ที่ยัง "สมมติ" (ไม่มีอะไรพิสูจน์ว่าเกาะ 2/3 ถูกวางในฉากนี้เลย) ไม่ใช่ผลการวัด**
      — ที่ **วัดจริง** คือเลขในสองตารางข้างบน ส่วนตัวเลข 498.9 คือเลขคณิตบนสมมติฐาน (`pf-adversary` รอบ `npbdgr` D3)
      ⚠️ **ห้ามเอาเรือไปจอดชิดเกาะที่ไม่ใช่เป้าเพื่อ "สอบเทียบ"** — ร่างแรกของขั้นนี้สั่งอย่างนั้น แล้วมันไปชนกฎ `STOP` ของใบนี้เอง
      (ถ้าหน้าต่างยืนยันเด้งแล้วเผลอกด ใบล่มทั้งใบ) และตอนนี้ก็ไม่จำเป็นแล้วเพราะตาราง marker ตอบให้แล้ว
  12. ตัวเช็ค NO-CRASH ตอนจบ: **คลิกขวาลากหมุนกล้อง** เท่านั้น (พิสูจน์ว่าไคลเอนต์ยังมีชีวิตโดยไม่ต้องมีไบต์ออกสาย) · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้** · ออกด้วยปุ่ม X
  13. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ**
  🔴 **STOP:** ฉากเปลี่ยนไปเกาะจริง หรือมีหน้าต่างยืนยันโผล่แล้วเผลอกด ⇒ หยุดทั้งใบ ปิดไคลเอนต์ รายงานทันที (ใบนี้ **ไม่มีสิทธิ์กดยืนยัน** เข้าเกาะ)

- pass criteria (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน):
      (ก) 🔴 **นี่คือเกณฑ์ผ่านของใบ**: ตัด hex ดิบจาก `GAME_LIVE.txt` **หน้าต่าง +/- 5 วินาที รอบเวลาที่จดไว้ของทุกจังหวะชน** (เกาะ 2 สองครั้ง · เกาะ 3 สองครั้ง)
          **คัดทุกเฟรมในหน้าต่างนั้น ทุก opcode ไม่กรองอะไรทิ้ง** พร้อม index เฟรม + จำนวนไบต์ต่อเฟรม · `TargetPosVital` รัว ๆ ต้องอยู่ในนั้นด้วย **ห้ามตัดออกเพราะดูน่าเบื่อ**
          **ครบทั้งสองเกาะ = ผ่าน** · ได้เกาะเดียว = ผลบางส่วน รายงานว่าได้เกาะไหน
      (ข) ตัวช่วยค้น (ไม่ใช่ตัวตัดสิน): เฟรมที่ตรงสมมุติฐานจะมีรูป `12 B2 1F 0B 01 0F <u16> 00 0B 04 ...` ยาว 69 ไบต์
          id `153` = ไบต์ `99 00` ⇒ ค้น `0F 99 00 0B 04` · id `154` = `9A 00` ⇒ ค้น `0F 9A 00 0B 04`
          🔴 **ไม่เจอสองสตริงนี้ ไม่ได้แปลว่าใบตก** -- แปลว่าคำทำนายผิด ซึ่งเป็น finding (ดูหัวข้อผลลัพธ์)
      (ค) ถ้า P1 ผ่าน (hook ยิงจริง): บรรทัดคอนโซลรูป
          `LANE_A_TRIGGER_VITAL id=<n> name=<ชื่อจากตารางของไคลเอนต์เอง> ISLAND scene=<n> min_level=<n> wire=<PROVEN|CANDIDATE> no_responder bytes_out=0`
          (`... PROP ...` เมื่อเป็น prop · `... UNPARSED len=.. hex=..` เมื่อ payload เดินไม่ผ่าน) ⇒ **คัดทุกบรรทัดที่เห็น ดิบ ๆ**
          🔴 **จำนวนบรรทัดที่ผู้เทสนับเองด้วยตา ไม่ใช่หลักฐานเดี่ยว** ต้องมี hex ของ (ก) คู่เสมอ
      (ง) `integrity_check` = `ok` ทั้งสองครั้ง · sha256 ของ canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      🔴 **ชั้นนี้ตอบไม่ได้เลยว่ามีอะไรขึ้นบนจอ**
    client-observable (🔴 **ต้องมีคนนั่งหน้าจอ ห้ามอนุมานจากคอนโซล**):
      (จ) **ตอนชนแต่ละครั้ง จอเป็นอย่างไร** -- เขียนหนึ่งในสี่คำตรง ๆ ต่อหนึ่งครั้ง: `หน้าต่างรายงานกัปตัน` / `ข้อความปฏิเสธ (คัดตามตัวอักษร)` / `ข้อความอื่น (คัด)` / `ไม่มีอะไรเลย` · **แนบภาพนิ่งของจังหวะนั้น**
      (ฉ) เรือ **หยุด/เด้ง/ทะลุผ่านเกาะ** หรือไม่ -- บรรยายตามที่เห็น **ห้ามเดาสาเหตุ**
      (ช) 🔴 **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ ทุกภาพ** · เขียนคำว่า `none` ออกมาแทนการเว้นว่าง
          อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** (ห้าม contact sheet / ภาพย่อ / วิดีโอ) · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุของสี** (`RE-067` เป็นเจ้าของคำถามนั้น) · ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 **ชั้นนี้ตอบไม่ได้ว่าไบต์ใดออกจากไคลเอนต์**
    🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` เท่านั้น (G-OBS) · หลักฐานครบแต่ไม่มีลายเซ็นคน = `AWAITING-OBSERVER` ซึ่งไม่ใช่ PASS และไม่ใช่ FAIL

- ทำอย่างไรกับผลแต่ละแบบ (🔴 **ผู้เทสไม่ต้องตัดสินสมมุติฐาน แค่เลือกกล่องแล้วรายงาน**):
  A. **ได้เฟรมที่ถือ id `153` และ/หรือ `154`** ⇒ ใบ **PASS** · คำทำนายถูก · ครึ่ง (ก) ของใบ `RE-` เรื่องรายงานกัปตันปิดได้โดยไม่ต้องเปิดอิมเมจ · ผลไปที่ LANE-A
     🔴 **ยังห้ามเขียนว่า "การเทียบท่าทำงานแล้ว"** -- ยังไม่มีใครเห็นเฟรมขาเข้าและปุ่มยืนยัน
  B. **ได้เฟรมตอนชน แต่ id เป็นเลขอื่น** (prop เดิม 40/51/3/57/36 หรือเลขที่ไม่รู้จัก หรือคนละ opcode) ⇒ ใบ **ยัง PASS** เพราะเกณฑ์คือ hex ไม่ใช่ id · เขียนเลขที่เห็นตรง ๆ · redirect: ใบ `RE-` ต้องเลิกสมมุติ 153/154 แล้วไปไล่จาก opcode ที่จับได้จริง
  C. **ไม่มีเฟรมใด ๆ ออกในหน้าต่าง +/- 5 วิ ของทั้งสองเกาะ** ⇒ 🔴 **นี่คือผลที่ใช้ได้และมีค่าเท่าผลบวก และมัน "หักล้าง" สมมุติฐานของใบนี้**
     รายงานเป็น **PASS พร้อมคำตัดสิน `NO-FRAME`** (ไม่ใช่ FAIL ไม่ใช่ NO-RESULT) แนบหน้าต่าง hex ที่ว่างเปล่านั้นมาเป็นหลักฐาน
     redirect: แปลว่าหน้าต่างรายงานกัปตัน **น่าจะเป็นของไคลเอนต์ล้วน** (เช็คระยะเอง ไม่มีไบต์ออกจนกดยืนยัน) หรือรอเฟรม **ขาเข้า** จากเซิร์ฟเวอร์ก่อน ⇒ ใบ `RE-` ต้องย้ายไปทาง static RE บนอิมเมจ และ LANE-A ต้องเลิกแผนเขียน responder ฝั่งขาเข้าไปก่อน
  D. **เกาะ 3 ตอบด้วยข้อความปฏิเสธเรื่องเลเวล** ⇒ **RESULT ไม่ใช่รอบล่ม** (P2) · ถ้ามีเฟรมมาด้วย = ยืนยันว่าเช็คเลเวลอยู่ฝั่งเซิร์ฟเวอร์/สาย · ถ้าปฏิเสธแต่ **ไม่มีไบต์ออกเลย** = หลักฐานว่าเช็คอยู่ในไคลเอนต์ล้วน (finding ชิ้นใหญ่ เขียนให้ชัด) · เกาะ 2 ยังต้องเก็บให้ครบตามเดิม
  E. **หาเกาะไม่เจอ / ไคลเอนต์ตาย / ตัวจับแพ็กเก็ตไม่ได้เขียนไฟล์** ⇒ **NO-RESULT** พร้อมเหตุผลหนึ่งบรรทัด · ห้ามเดาแทนไบต์ที่ไม่มี

- ที่รู้อยู่แล้วและ **ไม่ใช่ FAIL** (เห็นแล้วอย่าหยุดใบ อย่าเปิดใบซ้ำ ให้จดไว้เฉย ๆ): เรือของผู้เล่นขึ้น **HP -1/1** และตัวเรือไหม้ไฟตลอดเวลา · ฉากนี้ **ไม่มีเฟรม `PLAYER_FACTION`** (`n_SAVE = 0`) · เกาะและวัตถุนิ่ง "หันหน้าเข้าหาเรา" เมื่อถูกคลิก · ตำแหน่งกลับไปจุดเกิดทุกบูต

- nonclaims:
  1. 🔴 **ไม่ใช่ใบตัดสิน PASS/FAIL ของการเทียบท่า** -- ใบนั้นยัง **ปิดค้างไว้** จนกว่าผล RE จะลง (`COO-DECISION 20260904_0343` ข้อ 5) · ผลใบนี้ไม่ใช่ใบอนุญาตให้ใครเปิดใบนั้น
  2. ไม่พิสูจน์ว่า `0x1FB2` คือ "เฟรมเทียบท่า" · การอ้างแบบนั้นต้องมี hex **บวก** `span_sha256` จากอิมเมจ ซึ่งใบนี้ไม่ผลิต
  3. ไม่พิสูจน์เฟรม **ขาเข้า** จากเซิร์ฟเวอร์ ไม่พิสูจน์ปุ่ม "ยืนยัน" ไม่พิสูจน์เส้นทางเปลี่ยนฉากเข้าเกาะ
  4. ไม่พิสูจน์ว่าเซิร์ฟเวอร์ **ควร** ตอบอะไร และ **ไม่อนุญาต** ให้ใครเขียน responder จากผลใบนี้เพียงใบเดียว
  5. ไม่ตัดสินความหมายของสีป้ายชื่อ (`RE-067`) · ไม่แตะ HP/vitals ของเรือ (`GT-109` VEHICLE-BIND) · ไม่แตะคอมแบต/ดรอป · ไม่พิสูจน์กลไก `/warp` เอง
  6. ไม่พิสูจน์อะไรที่ต้องรอดข้าม relog (บูตบนสำเนา DB)

- links: `notes_to_chief/20260903_1901_KA1A-R307-RESULTS-*.md` · `notes_to_chief/20260904_0434_LANE-A-TO-CHIEF-RE-TICKET-captain-report-frame-on-island-contact.md` ·
  `lane_hooks/lane_a_island_trigger_log.py` · `external/PF_PROTOCOL_REGISTRY.tsv` · `gamedata/tables/TEXTDATA_TH__Trigger_TIP.tsv` ·
  `COO 20260904_0343` ข้อ 5 · `COO 20260904_0409` ข้อ 2 · `GT-217` · `RE-067`
- result: (ผู้เทสกรอก: PASS / PASS+`NO-FRAME` / NO-RESULT · branch+commit ที่บูต · มี/ไม่มี `LANE_HOOK_REGISTERED` ·
  hex ดิบของหน้าต่าง +/-5 วิ ทั้งสี่จังหวะชน (เกาะ 2 x2 · เกาะ 3 x2) · บรรทัด `LANE_A_TRIGGER_VITAL` ทุกบรรทัดถ้ามี ·
  เวลา `HH:MM:SS+07:00` ของทุกจังหวะชน · ภาพ `S00-HOME`/`S126-SPAWN`/`S126-LOOK1..3`/`S126-ISL2-*`/`S126-ISL3-*` ·
  สิ่งที่เห็นบนจอตอนชนทีละครั้ง + ข้อความที่คัดตามตัวอักษร · บรรทัดสีป้ายครบทุกป้ายทุกภาพ ·
  sha256 ทั้งสี่ค่า · `integrity_check` สองครั้ง · NO-CRASH/CRASH · 🆕 **ขั้น 11ก: เลข HUD `X Y` ตอนเกิด ตามตัวอักษร + ภาพ `S126-SPAWN-HUD` (ตรง/ไม่ตรงกับ `3050 232`)** ·
  🆕 **ถ้าเห็นบรรทัด `LANE_A_ENTER_INSTANCE ...` ในคอนโซล ให้คัดมาดิบ ๆ** — ใบนี้ห้ามกดยืนยัน ⇒ บรรทัดนั้น **ไม่ควรมี** ถ้ามีแปลว่าเฟรมยืนยันไปถึงเซิร์ฟเวอร์โดยไม่มีใครกด = finding ชิ้นใหญ่ ·
  `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: LANE-A -- LANE-A บริโภคผลใบนี้เอง**

---

## GT-246 AUTO-WALK-CLICK-DIFFERENTIAL-001  [ANSWERED -- วัดครบแล้วในรอบ attended R310 (2026-09-04 18:45-19:07 +07:00) ตั้งแต่ก่อนใบนี้มีเลข -- ห้ามบูตซ้ำ ไม่มีขั้นตอนเหลือให้รัน -- เลขใบตั้งโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 4 ("ตั้งเลขใบ differential auto-walk แล้วเขียนผลจาก `1911` ข้อ 2 ลงใบเลย ... ผู้บริโภค = LANE-UI ไม่ต้องบูตซ้ำ") -- เจ้าของใบ/ผู้บริโภคผล = **LANE-UI**]

> ใบนี้ตั้งเลขย้อนหลัง: การวัดเกิดก่อนเลขใบ ผู้ขับ = Panya ผู้วัด/เขียน = ka1-A
> ทุกค่าในหัวข้อ result คัดจาก `notes_to_chief/20260904_1911_KA1A-R310-RESULTS-*.md` ข้อ 2 คำต่อคำ
> chief ไม่ได้วัดใหม่ ไม่ได้ตีความเพิ่ม ไม่ได้เติมค่าที่จดหมายไม่มี

## GT-247 ATTACK-POSE-ONE-FIELD-AB-001  [🟢 **PASS -- R315 2026-09-05 10:11-10:2x** · `OBSERVER_CONFIRMED 2026-09-05T10:24+07:00` · ปิดหัวโดย chief (LANE-E) รอบ `pv4zg1`/R352 2026-09-05T11:0x+07:00 ตามผล `notes_to_chief/20260905_1031_KA1A-R315-RESULTS-*.md` + `COO-DECISION 20260905_1045` · ผล: `+0x30` ของเฟรม echo = **BEHAVIOR id** — 5 ค่าให้ 5 ท่าต่างกัน 1 ท่าต่อ 1 คลิก · 🔴 **[เสนอ ไม่ใช่ [วัดแล้ว]] ตาราง id↔ท่า และ "ตัวที่ไม่ออกท่าคือ `286` กับ echo `60029`"** — pf-adversary (D9) ชี้ว่าการหมุนค่า 7 ตัวต่อ hit ในบูตเดียว ทำให้ข้อสรุปรายค่าขึ้นกับการจับคู่ "คลิกที่คนเห็น" กับ "hit ที่เซิร์ฟนับ" และจดหมายผลเองบันทึกว่า 41 hits มาจาก 33 เฟรม (คลิกรัว + cadence ตัดทิ้ง) ⇒ ถ้ามี offset คงที่ ±1 ตัวที่เงียบจะกลายเป็นคู่ที่อยู่ติดกันในวงหมุนแทน และการ "ซ้ำได้ 3 รอบ" ตรวจ offset คงที่ไม่ได้ · **สิ่งที่รอดทุกกรณี = ฟิลด์ `+0x30` เป็นตัวเลือกท่า · 5 ค่าให้ 5 ท่า · 1 ท่าต่อ 1 คลิก (นี่คือสิ่งที่ปิดใบนี้)** · **คำถามค้างถึง ka1-A/LANE-B: การจับคู่ id↔ท่าอ่านสดจาก `POSE_TRIAL sent=<id> hit=<n>` ขณะ Panya บอกท่าหรือไม่** — ถ้าใช่ เขียนหนึ่งบรรทัดแล้วข้อสงสัยนี้ปิดทันที · บูตไร้ธง `BOOT_COMMIT 987edc55` = หัว main code_delta 0 · สวิตช์เป็น env `PF_POSE_TRIAL=<list>` ผ่าน production `_dispatch_mob_combat` (server `#787`) · 41 hits · ทางเบี่ยง "ลิสต์เดียว 7 ค่าแทน 7 บูต" Panya เคาะเอง 10:05 · **ผู้บริโภคผล = LANE-B** (ท่าโจมตี production จาก equip type ตกคิวหลัง PR ฉาก 4 ตาม `1045`) · 🔴 ห้ามบูตใบนี้ซ้ำ · เดิม: 🟢 **READY** -- ปลดหัวโดย chief (LANE-E) รอบ `5e00uw`/R348 2026-09-05T04:5x+07:00 ตาม `NOW.md` 04:45 (COO) · **หลักฐานที่ chief วัดเอง ไม่ได้เชื่อบรรทัดเดียว:** สวิตช์อยู่ใน production `_dispatch_mob_combat` จริง (`runtime.py:5131` เรียก `make_production_hit_pose_echo`, commit `0abde7aa` "LANE-B round yqbwri: GT-247 pose-trial into production dispatch", อยู่บน `main` ผ่าน server `#787` -- `git merge-base --is-ancestor` ยืนยัน · หมายเหตุ: commit ยอดของกิ่ง `#787` คือ latch ของ mob_loot ตัวสวิตช์เป็น commit ก่อนหน้าในกิ่งเดียวกัน) · `pytest tests/test_pose_trial.py tests/test_action_ack.py -q` = **48 passed, 79 subtests** · `test_an_unarmed_boot_is_byte_and_line_identical_to_production` ยังตรึงอยู่ · 🔴🔴 **อ่านกับดักในขั้นตอนที่ 1 ก่อนบูต** (chief วัดเอง R348 -- ดู `notes_to_chief/20260905_0451_CHIEF-TO-LANE-B-pose-trial-boot-banner-refuses-a-list.md`) · ⚠️ ที่ยังไม่ตรึง: จุดเรียกใน `runtime.py:5131` ไม่มีเทสตรึง call site (มีแต่เทสของฟังก์ชัน) = ถ้าใครลบบรรทัดนั้น เทสไม่แดง -- ของ LANE-B แจ้งแล้วไม่แก้ในรอบนี้ · เดิม: 🔴 BLOCKED-ON-WIRING -- แก้หัวโดย chief (LANE-E) รอบ `s5uz94` 2026-09-05T03:3x+07:00 ตาม `COO-DECISION 20260905_0248`(บริบท `NOW.md` "รอเครื่องคุณ" ข้อ 3)/ผล `R314 02:31` (`notes_to_chief/20260905_0233_KA1A-R314-RESULTS-*.md`): รันแล้วจริง = **NOT-EXERCISED** ไม่ใช่ READY อีกต่อไป -- สวิตช์ `#771` อ่านได้เฉพาะใต้ `--scene-load-scenario` และเกต `is_scene_remote_hostile_target` ต้อง `vital_count==1` แต่ไคลเอนต์พ่วง TargetPos ทุกเฟรม ⇒ เซิร์ฟไม่เคยตอบ -- Panya คลิกแล้วไม่มีท่า (ไม่ใช่ NEGATIVE ตัวจริง เพราะการทดลองไม่เคยถูกเรียกเลย) ⇒ **ห้ามบูตซ้ำจนกว่า LANE-B ย้ายสวิตช์ไป production `_dispatch_mob_combat` (echo ต่อ hit ผ่าน `PF_POSE_TRIAL=<list>`) แล้วขึ้น main** (`0248` งานแรก) แล้ว chief ปลดหัวใหม่ · เดิม: 🟢 **READY** -- ปลดโดย chief (LANE-E) รอบ `zwxuuk` ตาม `COO-DECISION 20260904_2347`: แฟล็กของ **LANE-B** อยู่บน `main` จริง (server `#771`, `be725d4`, merged 23:37) และ `RECHECK` ด้านล่างผ่านครบ · เลขใบตั้งโดย chief (LANE-E) รอบ `epkucn`/R344 ตาม `COO-DECISION 20260904_2142` ข้อ 1 · เนื้อใบ = `notes_to_chief/20260904_2133_KA1A-TO-COO-attack-pose-*` §1 (ผู้ร่าง ka1-A) · **เจ้าของใบ/ผู้บริโภคผล = LANE-B** · ผู้รัน = Panya (attended) ~10-15 นาที · 🔴 **Panya ยกเว้นกฎ "ห้ามใบตีมอนจนกว่า P-2 จะปิด" ให้ใบนี้ใบเดียว** (คำสั่งสด 2026-09-04 21:15 · `NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด") -- ใบนี้วัด **ท่า** ไม่วัดสี ไม่วัดดาเมจ · **บูตเดี่ยว ไม่พ่วง `GT-114`** (`GT-114` ยกเลิกแล้วตาม `COO-DECISION 20260904_2158`) · ไม่ออกท่าทั้ง 6 ค่า = **NEGATIVE** (ผลลบที่มีค่า) ไม่ใช่ FAIL (`COO-DECISION 20260904_2346`)]

**คำถามเดียว:** เมื่อ reply ต่อ `ActionVital` ใส่ `+0x30` = behavior id ของอาวุธที่ถือจริง (ไม่ใช่ echo `0xEA7D`) ไคลเอนต์เล่นอนิเมชันโจมตีของ performer ซ้ำได้ทุกครั้งหรือไม่

**ที่มา:** `RE-110-RESULT` 2026-08-27 18:32 (archive) ข้อ "one-field A/B เท่านั้น" + `BUILD_IMPACT` ของมัน · chief `1405` ยืนยัน [PROVEN] crosswalk `EQUIP_VALUE.n_EQUIPTYPE -> n_ATTACK_SKILL -> BEHAVIOR.n_ID` = 280/282/284/286/288/290

**สวิตช์จริง = ตัวแปรแวดล้อม ไม่ใช่แฟล็กบรรทัดคำสั่ง** (`COO-DECISION 20260904_2346`: `app.py` เป็นของ chief, LANE-B แก้ไม่ได้ จึงเลือกอ่าน process environment แบบเดียวกับ `PF_SPEED_TRIAL`) -- ก่อนบูตแต่ละครั้ง พิมพ์ **`set PF_POSE_TRIAL=<id>`** ใน cmd.exe ของสะพาน (**ห้ามใช้ `setx`** -- `setx` เขียนลง registry ติดค้างทุกบูตในอนาคตแบบมองไม่เห็น ส่วน `set` เป็นของหน้าต่างนั้นบานเดียว) แล้วค่อยบูตเซิร์ฟเวอร์ · **ต้องเห็นบรรทัดคอนโซล `POSE_TRIAL_BOOT armed=<id>` ก่อนคลิกทุกครั้ง** -- ไม่เห็น = ตัวแปรไม่ติด อย่าคลิกต่อ · ไม่ตั้งตัวแปร/ตั้งว่าง/พิมพ์ผิด/`auto` ที่ไม่มี provenance = production เดิมทุกไบต์ (fail-closed) · แฟล็กบรรทัดคำสั่ง `--pose-trial <id>` เป็นแค่ alias สะดวกมือหนึ่งบรรทัดที่ยังไม่มีใครเขียน ไม่ใช่ตัวบล็อกใบนี้
**ระยะยืน:** ตัวกรอง range gate ที่ `0x44EB1D -> 0x4758D0` ใช้ `n_RANGE = 75` (ระยะยกกำลังสอง) -- **ยืนให้ชิดมอนกว่าค่านี้ก่อนคลิก** ไม่งั้นค่าที่ resolve ได้จริงอาจโดนเกตนี้ปฏิเสธจนดูเหมือนไม่ออกท่าทั้งที่ id ถูก

**RECHECK (ก่อนปลด READY) -- ผ่านครบแล้ว รอบ `5e00uw`/R348:** ✅ ตัวแปร `PF_POSE_TRIAL` + โทเคน `POSE_TRIAL_BOOT`/`POSE_TRIAL` อยู่บน `main` · ✅ **สวิตช์อยู่บนทางเดิน production แล้ว ไม่ใช่ scenario gate**: `runtime.py:5131` (ใน `def _dispatch_mob_combat`, เริ่มบรรทัด 4920) เรียก `action_ack.make_production_hit_pose_echo` -- commit `0abde7aa` บน `main` ผ่าน server `#787` · ✅ `pytest tests/test_pose_trial.py tests/test_action_ack.py -q` เขียว (**48 passed, 79 subtests** -- เดิม 33/69 ก่อนย้ายลง production) · ✅ ไม่ตั้งตัวแปร = byte-identical กับ production (`test_an_unarmed_boot_is_byte_and_line_identical_to_production` ตรึงอยู่) · ⚠️ ที่ **ไม่** ผ่าน: จุดเรียกใน `runtime.py:5131` ไม่มีเทสตรึง call site -- ลบบรรทัดนั้นแล้วเทสไม่แดง (ของ LANE-B แจ้งแล้ว)

**steps (~10-15 นาทีหน้าจอ · ฉาก 2 มอน Fighting Fish soldier ที่ตีได้อยู่แล้ว · ยืนชิดมอน <75 ทุกครั้งก่อนคลิก):**
🔴🔴 **กับดักที่ต้องอ่านก่อนขั้นที่ 1 (chief วัดเอง R348 2026-09-05T04:5x+07:00 · `PYTHONPATH=src python3 -c` เรียก `pose_trial.boot_banner` ตรง ๆ):**
**ตั้งค่าเป็น "หนึ่งค่าต่อหนึ่งบูต" เท่านั้น ห้ามตั้งเป็นลิสต์คั่นจุลภาคในรอบนี้**
`set PF_POSE_TRIAL=280` -> บรรทัดบูตพิมพ์ `POSE_TRIAL_BOOT armed=280` (ถูก) แต่
`set PF_POSE_TRIAL=280,284,288,282,290,286` -> บรรทัดบูตพิมพ์ **`POSE_TRIAL_BOOT refused=malformed`** ทั้งที่ทางเดิน per-hit ใน production **รับลิสต์ได้ปกติ** (`parse_trial_list` คืน `(280,284,288,282,290,286)`)
เพราะ `boot_banner` ยังอ่านผ่าน `trial_opening`/`_parse_selector` ซึ่งรับค่าเดียว ยังไม่ถูกอัปเดตตาม `COO-DECISION 20260905_0248`
⇒ ถ้าตั้งเป็นลิสต์ ผู้เทสจะเห็นคำว่า `refused` แล้วเข้าใจว่า "ไม่ได้อาร์ม" และเลิกรอบทิ้งไปทั้งที่การทดลองทำงานอยู่ · เป็นของ **LANE-B** (`pose_trial.py`) แจ้งแล้ว ยังไม่แก้ ⇒ **รอบนี้ใช้หนึ่งค่าต่อหนึ่งบูตตามขั้นที่ 1-2 ข้างล่างตามเดิม**

1. `LOCK_GAME` · สำเนา DB · ปิด cmd.exe เดิม เปิดใหม่ พิมพ์ `set PF_POSE_TRIAL=60029` (ค่า echo เดิม = **control**) -> บูต -> เห็น `POSE_TRIAL_BOOT armed=60029` แล้วค่อยคลิกตีมอน 1 ครั้ง -> เห็น `POSE_TRIAL sent=60029 hit=1` ในคอนโซล -> Panya ดูว่าออกท่าไหม (คาด: ไม่) · ถ่าย 1 ใบ
2. teardown แล้วเปิด cmd.exe ใหม่ทุกรอบ พิมพ์ `set PF_POSE_TRIAL=<id>` ทีละค่า **280 -> 284 -> 288 -> 282 -> 290 -> 286** -> บูต -> เห็น `POSE_TRIAL_BOOT armed=<id>` -> คลิกตีมอน 1 ครั้งต่อค่า -> เห็น `POSE_TRIAL sent=<id> hit=<n>` ทุกครั้งที่ตีติด (ไม่เห็นบรรทัดนี้ = การตีไม่ถูกนับเป็น hit ไม่ใช่ "ค่าผิด" -- บันทึกแยก) -> Panya บอก "ออกท่า / ไม่ออก / ท่าอะไร" · ถ่ายเฉพาะค่าที่ออกท่า
3. ค่าที่ออกท่า: **ไม่กดอะไรต่อ 10 วินาที** -- ดูว่าไคลเอนต์ตีซ้ำเอง (auto-repeat) ไหม (ตอบ objective 1 ของ `RE-110` ที่ static ตัน) · สายจดเวลาเฟรม `ActionVital` ขาเข้าเทียบ
4. teardown ตามปกติ

**pass criteria (สองชั้น ห้ามใช้ชั้นเดียวอ้างอีกชั้น):**
- wire/DB: โทเคน `POSE_TRIAL` ครบทุกค่า + hex ของ reply แต่ละค่า ต่างกัน**เฉพาะ** `+0x30`
- client-observable: ตารางค่า -> ท่า (ออก/ไม่ออก) จาก Panya + ภาพของค่าที่ออกท่า · ต้องมี `OBSERVER_CONFIRMED: <ISO+07:00>`
- **PASS = อย่างน้อยหนึ่งค่าออกท่าซ้ำได้** · ทุกค่าไม่ออกท่า = ผลลบที่มีค่า (field map ผิด -> กลับไป RE) ไม่ใช่รอบเสีย

**STOP:** ไคลเอนต์ปิดตัว / `ErrorData` ใด ๆ -> หยุดทันที บันทึกค่าที่ส่งล่าสุด

**nonclaims:** ไม่ตัดสิน cadence (ค่า 600 ms ชั่วคราวคงเดิม) · ไม่ตัดสินดาเมจ/สูตร (LANE-CS/LANE-B) · ไม่ใช่ M4 (มอนตีกลับ) · ไม่แตะ production ถ้าไม่มีแฟล็ก · ไม่ยืนยัน equip type ของ Arena01 (ยังไม่มี provenance = เหตุผลที่ต้องไล่ทั้งหกค่า)

## GT-141 GM-003 CHAT-WARP-STAGED-LOGIN-SCENE-001 [attended]: GM พิมพ์ `/warp <ฉากที่พินไว้>` ลงกล่องแชท แล้วล็อกเอาต์-ล็อกอินใหม่ -- โผล่ที่ฉากนั้นไหม  [❌ **CANCELLED - covered by GT-217** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — `GT-217` เดินเส้นทางเดียวกันนี้จบแล้วบนจอเจ้าของรอบ R307 (`/warp 126` จอง -> ปิดด้วย X -> เปิดใหม่ -> โผล่ที่ spawn ของทะเบียน · จดหมายผล `notes_to_chief/20260903_1901_KA1A-R307-RESULTS-*.md`) ⇒ ไม่ต้องเผาบูตอีกใบเพื่อคำตอบเดิม · **ยกเลิกไม่ใช่ลบ** เนื้อใบและด่านก่อนบูตทั้งหมดคงไว้ข้างล่างเพื่อเป็นบริบทของ `GT-217` · เปิดใหม่ได้ถ้ามีใครแสดงว่าเส้นทางของสองใบต่างกันจริง · สถานะเดิม: **READY (เงื่อนไขโค้ดปลดแล้ว) · 🔴 อ่านสองข้อล่างก่อนบูต ไม่งั้นเกรดผิด** · ~~BLOCKED — โค้ดที่ใบนี้เทสยังไม่อยู่บน main~~ ~~READY เมื่อ `pirate-force-server#224` merge~~ -- LANE-GM รอบ `gejldf` · **อัปเดตรอบ `ank2vl` 2026-08-29T05:2x+07:00 (LANE-GM เจ้าของใบ) วัดด้วย GitHub API ไม่ใช่จดหมาย:** `#224` เอง `state=closed merged=false` — เกต Windows แดงแล้ว `merge-claude-pr.yml` ปิดให้เอง (run `33210364835`) แต่ **งานนั้นขึ้น main แล้วทาง `#232`** (merge `b229269` จาก branch `claude/sleepy-sagan-gejldf`) ⇒ `/warp <ฉากอื่น>` มีอยู่จริงบน main แล้ว ใบนี้บูตได้ · **(1) ฉากที่จองได้มีสี่ฉากเท่านั้น** `stageable_scene_ids() == (1, 2, 278, 997)` — ฉากนอกรายการถูกปฏิเสธ**ตอนเขียน** ไม่ใช่ตอนล็อกอิน (`login_entry_is_pinned`, `COO-DECISION 20260829_0441` ข้อ 3) ⇒ พิมพ์ `/warp 126` แล้วได้ refusal **คือพฤติกรรมที่ถูก ไม่ใช่ FAIL** · **(2) single-use ยังไม่มีผลบน main** `COO-DECISION 20260829_0441` ข้อ 2 สั่งว่า override ต้องถูกใช้แล้วหายไปเอง · โมดูล `gm/login_scene_consume.py` + เทสอยู่ใน `pirate-force-server#230` **แต่จุดเรียกใน `runtime.py` ยังไม่เปลี่ยน** (`CORE-REQUEST-GM-033` ถึง chief, ใบ `20260829_0515`) ⇒ **วันนี้ entry ยังค้างอยู่หลังล็อกอิน** ขั้นเก็บกวาดของใบนี้ยัง**ต้องทำด้วยมือ** (ลบบรรทัดบัญชีตัวเองใน `config/gm_login_scene.json` ก่อนคืนเครื่อง) · เมื่อ GM-033 ลง main ขั้นนั้นเปลี่ยนเป็น "ยืนยันว่าไฟล์หายไปเอง" และ**ล็อกอินครั้งที่สองต้องได้ฉากปกติ** · **อัปเดตรอบ `tp8mq6` 2026-08-29T06:4x+07:00 (LANE-GM เจ้าของใบ) สองข้อ:** (ก) บล็อกของ chief หมดแล้ว วัดด้วย GitHub API: `#230` `merged_at 2026-08-28T21:56:49Z` และ `#233` merge แล้ว ⇒ chief เดินใบ `CHIEF-DECISION 20260829_0520` ข้อ ② ได้ครบ ไม่ต้องแยก PR · (ข) 🔴 **ก่อนหน้ารอบนี้ single-use ไม่ได้ถือจริงแม้จะเรียกจาก runtime แล้วก็ตาม** — pf-adversary วัดได้ว่า ถ้าสองล็อกอินของบัญชีเดียวกันซ้อนกัน **ผู้แพ้ได้ฉากที่ stage ไว้ไปด้วย** (4/4 ตอนโหลดขนาน) แก้แล้วในรอบ `tp8mq6` ⇒ **ห้ามเกรดใบนี้ด้วยรอบที่เปิดสองหน้าต่างพร้อมกัน จนกว่า PR ของรอบ `tp8mq6` จะ merge** และผลเก่าที่รันแบบซ้อนกันให้ถือว่าอ่านไม่ได้ · **อัปเดตรอบ `qq0i9u` 2026-08-29T09:2x+07:00 (LANE-GM เจ้าของใบ) — ไม่ปลดและไม่เพิ่มบล็อก เปลี่ยนเฉพาะข้อ (1) ให้กว้างขึ้น:** ข้อ (1) เดิมพูดถึงการปฏิเสธ**ตอนเขียน** (`/warp`) เท่านั้น · ตอนนี้ **ไฟล์ config ที่แก้ด้วยมือก็ถูกปฏิเสธด้วย ตอนอ่าน** — `gm/login_scene_admission.py` ใช้เพรดิเคตตัวเดียวกันทั้งฝั่งเขียนและฝั่งอ่าน ทั้ง `gm_login_scene.json` และแฟ้ม standalone ⇒ ผลต่อผู้เทสใบนี้: (ก) ถ้าเผลอใส่ฉากนอก `(1, 2, 278, 997)` ลงไฟล์เอง **ล็อกอินไม่ตายอีกแล้ว** ได้ฉาก 1 แทน และ stderr พิมพ์ `GM_LOGIN_SCENE_CONFIG_REFUSED ... stageable=(1, 2, 278, 997)` (ข) 🔴 fail-closed ทั้งแฟ้ม: บรรทัดเดียวผิด = override ทุกบัญชีในแฟ้มนั้นหยุดทำงาน ⇒ ถ้าใบนี้ได้ฉาก 1 ทั้งที่ stage ฉาก 2 ไว้ **ให้ grep โทเคนข้างบนใน stderr ก่อนสรุปว่า FAIL** (ค) เกณฑ์ของใบนี้ไม่เปลี่ยน — สี่ฉากเดิม ไม่มีฉากไหนหายไป (เทสตรึงค่าเป็น literal) · วัดในชุดเทสผ่าน dispatcher จริง **ยังไม่เคยวัดกับ client จริง** · 🔴 (ง) **ด่านก่อนบูตข้อใหม่ ไม่ปลดและไม่เพิ่มบล็อก:** ห้ามแก้ `scenarios/world_scene_registry_001.json` ระหว่างที่เซิร์ฟเวอร์รันอยู่ — `runtime.py:527` ถือ snapshot ตั้งแต่บูต ส่วนด่านรับเข้าอ่านดิสก์ ⇒ แก้ให้กว้างขึ้นกลางคัน = ล็อกอินถูกปฏิเสธไม่มี reply และโทเคนไม่พิมพ์ (`pf-adversary` รอบ `qq0i9u` วัดซ้ำได้ · `CORE-REQUEST-GM-034` ขอทางแก้จาก chief) ⇒ แก้ทะเบียนแล้วต้องรีสตาร์ตเซิร์ฟเวอร์ก่อนบูตเกม · 🔴 **อัปเดตรอบ `7gplcy` 2026-08-29T10:4x+07:00 (LANE-GM เจ้าของใบ) — แก้คำของตัวเองรอบก่อน ไม่ปลดและไม่เพิ่มบล็อก:** อัปเดตรอบ `qq0i9u` ข้างบนเขียนไว้เหมือนว่าด่านรับเข้าตอนอ่าน (`gm/login_scene_admission.py`) อยู่บน main แล้ว 🔴 **ไม่จริง ขอถอน** — จดหมายของรอบนั้นขึ้น main จริง (`pf_bridge#389` merged) แต่ **โค้ดไม่ขึ้น**: `pirate-force-server#249` `state=closed merged=false` — เกต Windows แดงที่เทสเดียว (run `33229946448`) แล้ว `merge-claude-pr.yml` ปิด PR ทิ้งทั้งใบ ⇒ **จนกว่า PR ของรอบ `7gplcy` จะ merge ให้อ่านข้อ (ก) (ข) ของย่อหน้านั้นเหมือนยังไม่มี** (พิมพ์ฉากนอกรายการลงไฟล์เอง = ล็อกอินถูกปฏิเสธเงียบ ไม่มีโทเคน `GM_LOGIN_SCENE_CONFIG_REFUSED` ให้ grep) · ข้อ (ง) ห้ามแก้ทะเบียนกลางคัน **ยังใช้ได้ตามเดิมทุกตัวอักษร** เพราะมันเป็นพฤติกรรมของ `runtime.py` ไม่ใช่ของโค้ดที่หายไป · เกณฑ์ของใบไม่เปลี่ยน สี่ฉากเดิม · วัดด้วย GitHub API `merged_at` ไม่ใช่ด้วย `rounds/` หรือจดหมาย · 🔴 **อัปเดตรอบ `7hfrt0` 2026-08-29T13:3x+07:00 (LANE-GM เจ้าของใบ) — ขีดฆ่าไม่ลบ · ไม่ปลดและไม่เพิ่มบล็อก เปลี่ยนเฉพาะโทษของข้อ (ง):** ~~"แก้ทะเบียนกลางคันให้กว้างขึ้น ⇒ ล็อกอินถูกปฏิเสธไม่มี reply และโทเคนไม่พิมพ์"~~ **ไม่จริงแล้ว** — `pirate-force-server#253` `merged_at 2026-08-29T05:45:42Z` พาเกตของ chief ขึ้น main: `runtime.py` ทดลอง `resolve_entry` กับ snapshot ของโปรเซสก่อนใช้ override ถ้าปฏิเสธ ⇒ **ไม่ใช้ override** ตัวละคร**เข้าเกมได้ที่แถวของตัวเอง** พิมพ์ `GM_LOGIN_SCENE_OVERRIDE_REFUSED ... source=boot_snapshot` และคืนใบที่บริโภคแล้วกลับดิสก์ ⇒ โทษเปลี่ยนจาก **ล็อกเอาต์ถาวรเงียบ** เป็น **override ไม่ทำงาน แต่ grep เจอ** · 🔴 **ข้อห้ามยังอยู่ทุกตัวอักษร** ใบนี้เกรด "โผล่ที่ฉากที่ `/warp` จองไว้ไหม" — override ที่ไม่ทำงาน = เกรดไม่ได้ ⇒ แก้ทะเบียนแล้ว**รีสตาร์ตก่อนบูตเกม** และถ้าได้ฉากผิดให้ grep โทเคนนี้**ก่อน**สรุป FAIL (มีสองโทเคนที่ต้องแยกกัน: `GM_LOGIN_SCENE_OVERRIDE_REFUSED` = snapshot ปฏิเสธปลายทาง · `GM_LOGIN_SCENE_CONFIG_REFUSED` = แฟ้ม config มีบรรทัดผิด) · ทิศตรงข้าม (ทะเบียนถูกแก้ให้**แคบลง**หลังบูต ⇒ override ของทุกบัญชีในแฟ้มดับพร้อมกัน) เกตนี้เอื้อมไม่ถึง พารามิเตอร์ `scene_registry=` ลงเขตสาย GM แล้วรอบนี้ แต่ **ยังไม่มีผล** จนกว่า `CORE-REQUEST-GM-036` (ใบ `20260829_1330`) จะทำให้ `runtime.py` ส่ง snapshot เข้ามา ⇒ วันนี้ถือว่าทิศนี้ยังเปิด · **ยังไม่เคยวัดกับ client จริง** · **อัปเดตรอบ `znb56z` 2026-08-30T00:3x+07:00 (LANE-GM เจ้าของใบ) — ไม่ปลดและไม่เพิ่มบล็อก เกณฑ์ของใบไม่เปลี่ยน:** `CORE-REQUEST-GM-038` ลงครบทั้งสองครึ่งแล้ว (chief `#281` · สายนี้รอบนี้) ⇒ ตั้งแต่นี้ **แมพที่ถูกใช้แล้วหมดไป (`gm_login_scene`) รับฉากที่มีใบ chief สั่งไว้ได้** แม้ฉากนั้นจะพิน `login_entry_allowed: false` (วันนี้มีใบเดียว: ฉาก 126) · 🔴 **แต่วันนี้ยังไม่มีผลกับใบนี้เลย** [วัดบน main รอบนี้ ไม่ได้เชื่อจดหมาย]: `sanctioned_barred_blocker(126) == lane_a_registry_row_missing` — แถวทะเบียนของสาย A (ครึ่งที่ 1 ของ `CHIEF-DECISION 20260829_1603`) ยังไม่ลง main ⇒ `stageable_scene_ids()` **ยังเป็น `(1, 2, 278, 997)` เท่าเดิม** และ `/warp 126` ยังได้ refusal ซึ่งยัง**ถูก ไม่ใช่ FAIL** ตามข้อ (1) เดิมทุกตัวอักษร · สิ่งที่ผู้เทสจะเห็นต่างจริงคือ**คำในโทเคน**: `blocker=` ข้าง `GM_CHAT_WARP_REFUSED` เปลี่ยนจาก `login_path_bars_it_needs_core_request_gm_038` เป็น `lane_a_registry_row_missing` (คนละใบที่ต้องไปตาม) · 🔴 **ด่านก่อนบูตข้อใหม่:** วันที่สาย A ลงแถว 126 แล้ว `stageable=` ในโทเคนจะกลายเป็น `(1, 2, 126, 278, 997)` **เอง โดยไม่มี PR ของสายนี้คั่น** ⇒ ถ้าเห็น 126 ในรายการ **อย่าถือว่าใบพัง** ให้ถือว่าสาย A merge แล้ว และเลข 126 ใช้ได้จริงกับ `/warp` · เลขสี่ตัวในข้อ (1) จึงต้องอ่านว่า "รายการที่โทเคนพิมพ์ ณ วันบูต" ไม่ใช่ค่าคงที่ · **ยังไม่เคยวัดกับ client จริง**]

> NUMBERING: grep ก่อนจอง 03:33+07:00 -- `GT-141`/`RE-141` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า `GT-140`

ไม่ซ้ำกับ `GT-127` (ตัดสินที่ ndjson) และ `GT-128` (ตัดสินที่จอ **ระหว่างล็อกอินเดียวกัน** ผ่าน `ForcePos`, ยัง BLOCKED)

🔴 **แก้ก่อนใครจะบูต (รอบ `gejldf` เดียวกัน หลังผล pf-adversary):** ฉากที่ **จองได้** มีแค่ฉากที่
lane A พินไว้ว่าเข้าได้ตอนล็อกอิน = **1, 2, 278, 997 เท่านั้น** (สั่ง `/warp <อื่น>` ⇒ ปฏิเสธด้วย
`refused_stage_scene_has_no_login_entry` ไม่เขียนไฟล์)
(เหตุผลที่รายชื่อสั้น: `rounds/GM_20260829_0336_*.md`)

🟡 **ตั้งแต่รอบ `c48x1n`: คนเฝ้าคอนโซลไม่ต้องเปิดใบนี้มาดูรายชื่อ** (เมื่อ `pirate-force-server#254` merge)
`/warp <ฉากผิดที่เป็นตัวเลข>` ⇒ stderr ของเซิร์ฟเวอร์ได้หนึ่งบรรทัด:
`GM_CHAT_WARP_REFUSED account='<ชื่อ>' scene_id=<n> reason=scene_has_no_login_entry stageable=(...)`
grep `GM_CHAT_WARP_REFUSED` (คนละโทเคนกับ `GM_LOGIN_SCENE_CONFIG_REFUSED` ซึ่งแปลว่าไฟล์ config เสีย ไม่ใช่พิมพ์ผิด)

🔴 **ผู้เทสหน้าจอยังต้องอ่านรายชื่อ `1, 2, 278, 997` จากใบนี้เหมือนเดิม** — บรรทัดนั้นอยู่บน stderr ของเครื่องเซิร์ฟเวอร์
ไม่ใช่บนจอเกม และไม่มีอะไรตอบกลับไปที่ไคลเอนต์ (pf-adversary D7 รอบ `c48x1n` จับได้ว่าฉบับแรกของบรรทัดนี้อ้างเกิน)
~~🔴 **และพิมพ์ผิดที่ไม่ใช่ตัวเลข (`/warp island` · `/warp` เปล่า ๆ · `/warp 3 100`) ยังเงียบสนิททั้งสองฝั่ง** (D8 เปิดอยู่)~~
🟡 **อัปเดตรอบ `9wy444` 2026-08-29T15:2x+07:00 (LANE-GM เจ้าของใบ) — ขีดฆ่าไม่ลบ · ไม่ปลดและไม่เพิ่มบล็อก · เปลี่ยนเฉพาะสิ่งที่คนเฝ้าคอนโซล grep ได้:** D8 ปิดแล้วตาม `COO-DECISION 20260829_1344` (ทาง (ก) คนเฝ้าคอนโซล) ⇒ **เมื่อ `pirate-force-server#265` merge** (วัดด้วย GitHub API `merged_at` ไม่ใช่ด้วยใบนี้) พิมพ์ผิดที่ตายก่อนถึงไวยากรณ์ จะได้หนึ่งบรรทัดบน stderr ของเครื่องเซิร์ฟเวอร์:
`GM_CHAT_COMMAND_REFUSED account='<ชื่อ>' reason=command_parse_error_<Type> usage='<ไวยากรณ์ที่ถูก>'`
🔴 **บรรทัดนี้ไม่พิมพ์คำที่คุณพิมพ์ผิดกลับมาให้ ตั้งใจ** — `session.token` เป็น `--token` ระดับโปรเซส ไม่ใช่ล็อกอินต่อคอนเนกชัน (`runtime.py:5140-5150`) ⇒ ถ้าพิมพ์กลับมา ประโยคของผู้เล่นคนอื่นจะไปโผล่ในคอนโซล ใต้ชื่อบัญชี GM ของคุณ (pf-adversary รอบ `9wy444` D1) · สิ่งที่ได้คือ**ไวยากรณ์ที่ถูกของคำสั่งที่พิมพ์**
ครอบ `/warp island` · `/warp` เปล่า · `/warp 3 100` · `/warp 3 x y` · `/nonsense` · `/` เปล่า (`/nonsense` และ `/` ได้คลังคำสั่งทั้งหกบรรทัด) · grep `GM_CHAT_COMMAND_REFUSED` — **โทเคนที่สาม แยกจาก `GM_CHAT_WARP_REFUSED` (ฉากที่ล็อกอินเข้าไม่ได้) และ `GM_LOGIN_SCENE_CONFIG_REFUSED` (ไฟล์ config เสีย)**
🔴 **ฝั่งจอเกมยังเงียบเหมือนเดิมทุกตัวอักษร และเกณฑ์ของใบนี้ไม่เปลี่ยน** — บรรทัดนี้อยู่บนเครื่องเซิร์ฟเวอร์ ผู้เทสหน้าจอยังต้องอ่านรายชื่อ `1, 2, 278, 997` จากใบนี้เหมือนเดิม · 🔴 และยังมีความเงียบที่**ไม่ได้ปิด**: คำสั่งที่ **ถูกไวยากรณ์** แต่โดน rate limit หรือเขียน audit log ไม่ได้ (`rate_limited` · `command_log_quota_exceeded` · `command_log_write_failed_*`) **ยังไม่มีบรรทัดคอนโซลเลย** ⇒ ถ้าพิมพ์คำสั่งที่ถูกทุกอย่างแล้วเงียบสนิท อย่าเพิ่งสรุปว่า client ไม่ส่ง ให้ดู ndjson และดิสก์ก่อน
🔴 ไม่ใช่หลักฐานว่า `/warp` ทำงาน และ **ไม่เปลี่ยนเกณฑ์ของใบนี้เลย**

🟢 **อัปเดตรอบ `2q9lxx` 2026-08-30T10:2x+07:00 (LANE-GM เจ้าของใบ) — ไม่ปลดและไม่เพิ่มบล็อก เกณฑ์ของใบไม่เปลี่ยน:**
รายชื่อ `1, 2, 278, 997` ที่พูดซ้ำหลายจุดข้างบน (รวมในบรรทัดคอนโซล
`GM_CHAT_WARP_REFUSED ... stageable=(...)`) **โตเป็นห้าค่าแล้วบนคอมมิตปัจจุบัน**
[วัดสดรอบนี้ ไม่ใช่จากจดหมาย]: `login_scene_admission.stageable_scene_ids() ==
(1, 2, 14, 278, 997)` — ฉาก **14** (Hell Volcano Island) เข้าชุดจากคนละทางกับที่ใบนี้
เคยเตือนไว้เรื่องฉาก 126: ไม่ใช่ทาง `CORE-REQUEST-GM-038`/sanctioned-bypass แต่มาจาก
สาย A พลิก `login_entry_allowed(14)` เป็น `true` ตรง ๆ (`COO-DECISION 20260829_2342`,
PR `pirate-force-server#290`, จดหมาย
`notes_to_chief/20260830_0045_LANE-A-TO-LANE-GM-scene-14-is-stageable-now.md`
ซึ่งบริโภคจบแล้วรอบ `kmdln4` — ห้าไฟล์เทสของสายนี้ปักค่าใหม่ไว้ครบแล้ว ไม่มีอะไรค้าง)
**ถ้าคอนโซล grep เจอ `stageable=(1, 2, 14, 278, 997)` แทนสี่ค่าเดิม อย่าถือว่าใบนี้พัง**
— เหมือนคำเตือนเดิมของใบนี้เรื่องฉาก 126 ("อ่านว่ารายการที่โทเคนพิมพ์ ณ วันบูต ไม่ใช่ค่าคงที่")
เพียงแต่รอบนี้ทางที่ทำให้มันโตเป็นคนละทาง · **`/warp 14` เองใช้ได้ตามกฎเดิมแล้ว** (เป็นฉากที่จองได้
เพิ่มอีกหนึ่งฉาก) แต่ใบนี้ยังแนะนำ **278**/คู่เทียบ **2** เหมือนเดิม เพราะเกณฑ์ผ่านของใบนี้ไม่ได้ผูกกับ
ฉากใดฉากหนึ่งเป็นการเฉพาะ · nonclaim: ไม่มีการเปลี่ยนโค้ดของสายนี้ในรอบนี้ ค่าที่โตมาจากสาย A ล้วน ๆ

### objective (claim เดียว)
บนบูตไร้แฟล็ก บัญชีใน `gm_accounts` พิมพ์ `/warp <scene_id ที่ lane A พินไว้ และไม่ใช่ฉากปัจจุบัน>`
ลงกล่องแชทธรรมดา แล้ว **ล็อกเอาต์และล็อกอินใหม่** -- ตัวละครปรากฏที่ฉากนั้นจริงหรือไม่
(ฉากที่แนะนำให้ใช้: **278** = test stage · คู่เทียบ: **2** = Prison Exile)

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1 [wire/DB]** ทันทีที่พิมพ์: stderr `LANE_GM_CHAT_ACTION warp route=action` +
  `gm_chat_action_warp_staged_login_scene_<scene_id>` · ndjson สองแถว `record_id` เดียวกัน
  แถวที่สอง `"outcome":"staged_login_scene"` (`"executed": false` ถูกต้องแล้ว) ·
  `config/gm_login_scene.json` มี `{"gm_login_scene": {"<บัญชี GM>": <scene_id>}}`
- **P2 [บนจอ ระหว่างล็อกอินเดิม]** **ไม่มีอะไรเกิดขึ้นเลย** (คำทำนาย ไม่ใช่ความล้มเหลว -- ประตูนี้ไม่ส่งอะไรถึงไคลเอนต์)
- **P3 [หัวใจของใบ]** ล็อกเอาต์ ล็อกอินด้วยบัญชี GM เดิม ⇒ โผล่ที่ฉากที่สั่ง · บันทึกภาพหน้าจอ +
  คอนโซล `gm_login_scene_override_applied_<scene_id>`
- **P4 [คู่ควบคุม]** บัญชีนอก `gm_accounts` พิมพ์คำสั่งเดียวกัน ⇒ ไม่มีแถว ndjson ไม่มีบรรทัดในคอนฟิก
  และล็อกอินครั้งถัดไปของบัญชีนั้นอยู่ที่เดิม
- **P5 [ตัวหักล้าง]** `/warp 999999` ⇒ `refused_stage_unknown_scene` · `/warp 3` (มีชื่อ แต่ไม่ถูกพิน) ⇒
  `refused_stage_scene_has_no_login_entry` · ทั้งคู่คอนฟิกไม่เปลี่ยนแม้แต่ไบต์เดียว
  🔴 เห็น `staged_login_scene` จาก `/warp 3` = **หยุดทันที** ด่านกันล็อกเอาต์ไม่อยู่บนคอมมิตนั้น
- **P6 [ข้อบังคับ ไม่ใช่คำทำนาย]** หลังล็อกอินใหม่ **อย่าพิมพ์ `/warp` ซ้ำในเซสชันเดียวกัน** --
  เซิร์ฟเวอร์ยังจำว่าตัวละครอยู่ฉากเดิม (`CORE-REQUEST-GM-033`) · จะจองใหม่ให้ล็อกเอาต์ก่อน

### ก่อนบูต
- **ด่าน 0:** ใช้ซ้ำการอนุมัติบัญชีเดิม (`notes_to_chief/20260827_1200_CHIEF-REPLY-GT101-*`) -- GM หนึ่ง + นอกลิสต์หนึ่ง
- **ด่าน 1:** `py -3 pf_resolve_green_boot.py --repo "<path>" --fetch` เฉพาะ exit 0
- **ด่าน 2 (grep ที่ `<SHA>` จริง):**
```
git grep -n "make_gm_chat_command_action" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "staged_login_scene" <SHA> -- src/pirateforce_foundation/gm/commands.py
git grep -n "def stage_login_scene" <SHA> -- src/pirateforce_foundation/gm/login_scene_stage.py
git grep -n "get_login_scene_override" <SHA> -- src/pirateforce_foundation/runtime.py
git grep -n "def login_entry_is_pinned" <SHA> -- src/pirateforce_foundation/gm/login_scene_stage.py
```
🔴 บรรทัดสุดท้าย **0 hit = ห้ามบูตใบนี้** -- คอมมิตนั้นยังไม่มีด่านที่กันการจองฉากที่ล็อกอินเข้าไม่ได้
(ดูคำเตือนหัวใบ) ไม่ใช่ FAIL ของใบ แต่เป็นคอมมิตที่ไม่ปลอดภัยกับบัญชีเทส
  บรรทัดที่ 2-3 ⇒ 0 hit = `<SHA>` เก่ากว่า merge ของ `#224` ⇒ **ยังไม่ใช่ FAIL** บูตไม่ได้ รัน `--fetch` ใหม่

### pass criteria (สองชั้นแยกกัน ห้ามใช้ชั้นหนึ่งแทนอีกชั้น)
- **wire/DB:** P1 ครบสามอย่าง (สองอีเวนต์ + แถว `outcome` + บรรทัดในไฟล์คอนฟิก) และ P5 ปฏิเสธจริงทั้งสองกรณี
- **client-observable:** P3 เห็นฉากใหม่บนจอหลังล็อกอินใหม่ + `OBSERVER_CONFIRMED: <เวลา +07:00>`
- ขาดชั้นใดชั้นหนึ่ง = PARTIAL ไม่ใช่ PASS

### ขั้นเก็บกวาดหลังจบใบ (บังคับ)
ลบ `config/gm_login_scene.json` (ไม่ใช่ canonical DB ลบได้ปลอดภัย ค่าเริ่มต้น = ไม่มีใครมี override)
ไม่ลบ = บัญชี GM เข้าฉากนั้นทุกครั้งไปเรื่อย ๆ · บันทึกว่าทำอะไร

### nonclaims
1. 🔴 **ผ่านใบนี้ ไม่ได้แปลว่า warp ทำงาน** -- ไม่มีไบต์ออกสาย ตัวละครไม่เคยข้ามฉากขณะออนไลน์
   พิสูจน์แค่ "คำสั่งในแชทจองฉากล็อกอินได้"
2. 🔴 **ห้ามอ้าง M2 หรือ milestone ใด ๆ** -- เห็นเกาะเพราะ GM จองฉากไว้ ไม่ใช่เพราะเส้นทางเดินเรือทำงาน
3. ไม่อ้างว่า `TeleportVital`/`ForcePos` ถูกพิสูจน์เพิ่ม และไม่อ้างว่าฉากนั้นเล่นได้ครบ

**ผู้เปิดใบ: LANE-GM (รอบ `gejldf`)** -- ผลกลับมาที่สาย GM บริโภค

### result (ผู้เทสกรอก)
```

```

---

## GT-183 GM-B-SPEED-COMMAND-001  [❌ **CANCELLED - refuted by GT-218 (`/speed 400` killed the client in one frame, R306); open question carried by GT-231 and the (b'') gate in NOW** · ปิดโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 1 · ไม่ขัด `PANYA-ORDER 20260830_0215` §3 เพราะเจตนา ("คำสั่ง speed ใช้ได้") ยังเดินอยู่ใน `GT-231` และเกต (b'') ใน `NOW.md` · **Panya กลับคำได้ = เปิดใหม่ด้วยการลบวงเล็บนี้หนึ่งบรรทัด**]

> 🔴 **chief (LANE-E) รอบ `8nh6q5`/R334 2026-09-04T08:4x+07:00 — ไม่ปิดใบนี้ และนี่คือเหตุผล**
> LANE-GM (`notes_to_chief/20260904_0735`) เสนอให้ปิดด้วย `CANCELLED - covered by <ใบใหม่>` ตาม
> `PANYA-DECISION 20260903_1934` **ผมไม่ทำ และส่งขึ้น COO แทน**: ใบนี้ถูกเปิดตาม **`PANYA-ORDER`
> `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` §3 โดยตรง** ⇒ การยกเลิกมันคือการขัดคำสั่งที่เจ้าของ
> เคาะเอง ซึ่งอยู่นอกอำนาจ chief · **ใบยัง BLOCKED ตามเดิม ไม่มีใครลบ ไม่มีใครย้าย**
> สิ่งที่เปลี่ยนคือ **ป้ายชี้ทาง ไม่ใช่สถานะ**:
> - `GT-218` **FAIL** (`OBSERVER_CONFIRMED 2026-09-03T16:32+07:00`): `/speed 400` — ค่าที่ล็อกอินส่งอยู่แล้ว —
>   ฆ่าไคลเอนต์ในเฟรมเดียว ⇒ `/speed 800` ของใบนี้ **อันตรายกว่าอย่างเคร่งครัด** และ `NOW.md` ห้ามทุกค่าที่ไม่ใช่
>   `400` ที่ล็อกอินส่ง ⇒ **ห้ามบูตใบนี้ด้วยค่า `800` ไม่ว่าสถานะจะเป็นอะไร**
> - คำถามที่ยังเปิดอยู่จริง (เฟรมหรือการสร้าง actor เป็นตัวทำให้บิตที่ไม่ตั้ง = ศูนย์) ย้ายไปอยู่ใบใหม่ของ LANE-GM
>   ตาม `COO-DECISION 20260904_0545` ข้อ 3 — ดูจดหมาย `20260904_0844_CHIEF-TO-LANE-GM-*`
> **ขอ COO เคาะ**: ปิด `GT-183` ด้วย `CANCELLED - refuted by GT-218` หรือคงไว้ · ผมทำให้ทันทีที่มีคำตัดสิน

> Opened by chief this round, directly per Panya's order, same provenance as `GT-182`
> above. Source: PANYA-ORDER `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` section 3
> (GM-B). Build-owner lane: **LANE-GM** per chief's broadcast letter this round.

- objective: single claim -- on a NORMAL boot of `pirate-force-server` `main` (no
  `PF_ADHOC_ATTR_PROBE` environment variable, no external fork, no reference-only code from
  `notes_to_chief/reference_adhoc_probe/`), a GM account types `/speed <value>` as a real
  GM chat command and a human watching the screen sees the character's own movement speed
  visibly change to match. The owner's own justification for asking for this ("already
  proven doable via PF_ADHOC_ATTR_PROBE") refers to an informal, one-off, un-reviewed,
  external-fork round the owner ran personally on 2026-08-27 -- this entry tests whether
  the SAME wire mechanism, once written as a real, tested, in-tree GM command, still
  produces the same visible effect on an ordinary client and boot.
- background (read before building or running):
  - `notes_to_chief/reference_adhoc_probe/ADHOC_PROBE_ROUND1_FINDINGS_20260827.md` row
    "7 f32_54": values `1`, `999`, `99999` sent via the probe's field x7 made the
    character visibly "walk fast/slow" on the owner's own screen. The owner's own estimate
    of the table-normal value is **400** -- explicitly flagged in that same file as
    "ยังไม่ได้ยืนยันกับตาราง/ไบนารี" (not yet confirmed against the stats table or the
    binary) -- treat 400 as a starting guess, not a confirmed constant.
  - `notes_to_chief/reference_adhoc_probe/adhoc_attr_probe.py`: the mechanism is
    `BasicAttr` field x7, offset `+0x54`, kind `f32`, mask bit `0x0040`, sent as part of a
    FULL 55-field `UpdateAttrVital` (`0x309A`) block -- the module's own docstring states
    the client's ActorAttr apply "copies the incoming object whole", so a sparse delta
    that omits other fields would zero them. Any real implementation of `/speed` must
    follow the same whole-block-send discipline, not invent a smaller delta frame.
  - `notes_to_chief/reference_adhoc_probe/README_WHAT_THIS_IS.md`: this reference folder is
    explicitly **read-only**, has never passed `pf-adversary`, has no tests, and "if you
    want to use this for real you must rewrite it in your own lane's territory, with
    tests, not copy-paste". This entry cannot be closed by pointing at that folder; it
    requires new, tested, in-tree code.
- db: fresh copy of `state\pirateforce.sqlite3` for this boot (never the canonical file) --
  record the copy's filename and sha256 before/after; verify the canonical file's own
  sha256 is unchanged before and after.
- server args: standard boot, `-SecondPasswordMode bypass`, GM account from
  `config/gm_accounts.json` (or a test copy via `PF_GM_ACCOUNTS_CONFIG`). Requires whatever
  PR wires a real `/speed` GM chat command to be merged to `main` first (see RECHECK).
- steps:
  1. Boot per standard playbook; confirm server up before client connects and confirm this
     is a fresh server (not reused after a prior client was killed).
  2. Log in with the GM account. Right-click-drag camera only for a clean baseline view.
     Screenshot BASELINE, full resolution. Record every name label's colour in frame (one
     line each, "none" if nothing else visible), and note a fixed walking reference (e.g.
     distance between two landmarks, or time to cross a known gap) so "faster" is not
     purely subjective.
  3. Click into the chat box, confirm focus, type exactly `/speed 800` (double the owner's
     estimated normal 400) and press Enter.
  4. Walk the character a fixed distance (same path as any baseline walk timing done in
     step 2) using normal WASD movement. Screenshot STEP-A. Record whether the character
     visibly moves faster than baseline, and every name label's colour again.
  5. Click into chat again, type exactly `/speed 100` (well below owner's estimated
     normal), press Enter. Walk the same fixed distance. Screenshot STEP-B. Record whether
     the character visibly moves slower than baseline.
  6. Click into chat again, type exactly `/speed 400` (owner's estimated normal), press
     Enter, walk the same distance, screenshot STEP-C, and record whether it looks like
     baseline again (this is a visual comparison only, not a confirmation against the
     stats table).
- pass criteria (two layers, kept separate):
    wire/DB: server console/capture log for this boot shows, after each `/speed <value>`
      line, an `UpdateAttrVital 0x309A` frame whose decoded `BasicAttr` block has bit
      `0x0040` set and the `+0x54` field (f32) equal to the value typed, with the rest of
      the 55-field block populated (not zeroed) per the whole-block-send rule above.
    client-observable: what the human at the screen reports for STEP-A/B/C -- does the
      character visibly move faster after `/speed 800`, visibly slower after `/speed 100`,
      and does `/speed 400` look like the untouched baseline. A result where the character
      does NOT change speed at all is a valid, useful negative.
- nonclaims:
  1. Does not confirm 400 is the table-correct default walking speed -- it remains the
     owner's own estimate from one round, explicitly unconfirmed against
     `STANDARD_STATUS`/binary per the source finding itself.
  2. Does not test negative, zero, or extreme values beyond what round-1 already tried
     (1/999/99999) -- if new edge values are wanted, that is a new, separate probe
     request, per the one-entry-one-claim rule.
  3. Does not claim the whole-block-send discipline used by the ad-hoc probe is safe to
     relax for a real `/speed` command.
  4. Does not test `/speed` interacting with the movement-lock fields (x41/x42) --
     out of scope.
  5. Does not test any other ActorAttr field from the probe table -- this entry is scoped
     to field x7 / move speed only.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="GM-B" --grep="/speed" --grep="GT-183" | head -5`
  (empty output = the real `/speed` command has not landed on `main` yet and BLOCKED is
  still accurate).
- links: `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` (section 3, GM-B) --
  `notes_to_chief/reference_adhoc_probe/README_WHAT_THIS_IS.md`,
  `ADHOC_PROBE_ROUND1_FINDINGS_20260827.md`, `ACTORATTR_PROBE_TABLE_x_y.md`,
  `adhoc_attr_probe.py` -- `PROCESS_GATES.md` rule #18.
- numbering: see `GT-182`'s numbering note. This entry is `183`.
- result: (tester/build lane fills in: PASS/FAIL/BLOCKED, evidence, timestamp,
  OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## GT-200 CENSUS-NPC-LEVEL-LABEL-MULTI-SCENE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS (R307 2026-09-03 — เดินครบ 11 ฉากตามใบ arrival census ตรงเกณฑ์ทุกฉาก) · regression เสริมยืนยัน R321 2026-09-06 (Columbus LV10/Martin LV35/Fighting Fish Sergeant LV35 ตรงเดิม) · จาก notes_to_chief/20260903_1901_KA1A-R307-*.md + notes_to_chief/20260906_1255_KA1A-R321-*.md §8 · 🟢 READY -- RECHECK **ผ่าน วัดเองโดย LANE-A (เจ้าของใบ) รอบ `mcf4qp` 2026-09-03T08:4x+07:00** บน `origin/main` (เซิร์ฟเวอร์ `f240ab4`): `git show origin/main:src/pirateforce_foundation/world_population_bg0006.py` มี `level=placement.identity.level` จริง (บรรทัด 210 · ตัวห่อคือ `world_census_level.leveled_npc_attr` บรรทัด 200) · ~~[PENDING -- โค้ดยังไม่ขึ้น `main`: PR #524 branch `claude/dazzling-volta-7ste68`]~~ · 🔴 ผู้เทสยังต้องรัน RECHECK เองก่อนบูตทุกครั้ง (ตัดสินด้วยเนื้อโค้ด ห้ามเทียบเลข commit)
🟢 **บูตเดียวกับ `GT-210`/`GT-212` ได้และควรทำ** -- ทั้งสามใบเดินด้วย `/warp` เส้นทางเดียวกัน · 🔴 **กติกาลำดับข้อเดียว: ที่แต่ละฉาก ถ่ายภาพของใบนี้ให้เสร็จ "ก่อน" คลิกใคร** เพราะคำตอบของ `GT-210`/`GT-212` ส่ง roster ทับของเดิม]

ATTENDED: RECHECK ผ่านก่อน -> บูตปกติ ไม่มีแฟล็ก scenario -> ล็อกอิน GM -> จัดมุมด้วย **คลิกขวาลาก** เท่านั้น (ห้าม Q/E) เป็นตัวเช็ค NO-CRASH -> คลิกช่องแชทยืนยัน focus -> `/warp 3` Enter รอ ~3 วิ เดินเข้าใกล้ NPC ถ่ายภาพนิ่งเต็มความละเอียด -> ซ้ำกับ `/warp 6` และ `/warp 14` (เหลือเวลาค่อยทำ `/warp 130` และฉาก 1)
ATTENDED: แต่ละฉากบันทึก >= 4 ตัว ตัวละบรรทัด: ชื่อ · `LV` · สีป้าย (อ่านจากภาพเต็มความละเอียดเท่านั้น "none" ถ้าไม่มี) -- ฉาก 14 เพิ่มอีกหนึ่งบรรทัดเป็นตัวควบคุม: `LV` ของมอนสเตอร์ศัตรูหนึ่งตัว (Glaucoma/Lava shakers/Carlos) คาดว่าเป็น LV 105/115 ไม่ใช่ 1
ATTENDED: ชั้น client-observable เท่านั้นที่ตัดสินใบ -- PASS ต้องเห็น `LV` ไม่ใช่ 1 และต่างกันรายตัวในฉากเดียวกัน ครบ >= 3 ฉาก โดยมีอย่างน้อยหนึ่งฉากช่วงกว้าง (3/4/5/6/14) -- ยังเห็น `LV 1` ทั้งที่ wire ผ่านแล้ว = ผลลบ/finding ไม่ใช่ FAIL ของใบนี้ (เปิด RE ใหม่พร้อมภาพนิ่ง) ระบุชื่อฉากที่พลาด -- `/warp` พังกลางทาง = NO-RESULT ของใบนี้ (เป็นหลักฐานของ GT-192)
ATTENDED: ไม่มีแฟล็ก บูตปกติ ไม่ต้องตั้ง env หรือ tree ใด ๆ เพิ่ม
ATTENDED: 🔴 บูตร่วมกับ GT-210/GT-212 ได้ แต่ต้องถ่ายภาพของใบนี้ให้เสร็จ "ก่อน" คลิกใครในแต่ละฉาก (คำตอบของ GT-210/GT-212 ส่ง roster ทับของเดิม) -- ถ้ารันก่อนรอบ `2p4n3h` ขึ้น main ห้ามคลิก NPC ก่อนถ่ายภาพ (เฟรมหลังคลิกไม่มีฟิลด์เลเวลจะย้อนเป็น LV 1) ถ้ารันหลังจากนั้นคลิกได้ตามปกติแต่บันทึกไว้ว่ารันบน main รุ่นไหน

> เปิดโดย LANE-A รอบ `7ste68` 2026-09-02T02:55+07:00 ตามใบมอบหมาย `notes_to_chief/
> 20260901_2358_CHIEF-TO-LANE-A-codex-gt192-lv1-census-level-encode-assigned.md`
> · **LANE-A บริโภคผลเอง** · numbering: คำสั่งค้นหาคืน `199` ⇒ ใบนี้ `200` · บูต/DB/teardown ตาม
> `ATTENDED_SESSION_RUNBOOK.md` · ที่มาเต็มใน `rounds/A_20260902_0155_7ste68_*.md`

- objective: ข้อพิสูจน์เดียว -- ป้าย `LV` เหนือหัว **NPC สำมะโนธรรมดา** แสดงเลขจริงและ **ต่างกันรายตัว**
  ไม่ใช่ `LV 1` ทุกตัวอย่างที่ `GT-192` เห็น ในอย่างน้อย **3 ฉาก** ที่ไปถึงด้วย `/warp <mapnum>`
  ภายในการล็อกอินครั้งเดียว
- background: census ปกติไม่เคยเข้ารหัสเลเวลเลย (helper แช่แข็ง `v141:1139-1195` ไม่มีพารามิเตอร์
  level, mask ไม่เคยเซ็ตบิต `0x0002`) · รอบ `7ste68` เพิ่ม `world_census_level.py` (splice บิต
  `0x0002` + u16 tag `0x12` ตาม `RE-117`) ต่อเข้า **ทุก census source ที่มีชีวิต 13 ตัว รวมฉาก 1**
  · **ไม่มีแฟล็ก ติดทุกบูต** · 🔴 ฉาก 1 ยังขึ้น `LV 1` = **finding ไม่ใช่ผลที่คาดไว้**
- steps:
  1. RECHECK ผ่านก่อน · บูตปกติ **ไม่มีแฟล็ก scenario** · ล็อกอิน GM
  2. จัดมุมด้วย **คลิกขวาลาก** เท่านั้น = ตัวเช็ค NO-CRASH (ห้ามใช้ `Q`/`E`)
  3. คลิกช่องแชท **ยืนยัน focus** · `/warp 3` · Enter · รอ ~3 วินาที
  4. เดินเข้าใกล้ NPC · ภาพนิ่ง **เต็มความละเอียด** ชื่อ SCENE-3 · บันทึก >= 4 ตัว ตัวละบรรทัด:
     ชื่อ · `LV` · **สีป้าย** ("none" ถ้าไม่มี) อ่านสีจากภาพเต็มเท่านั้น
  5. ซ้ำข้อ 3-4 กับ `/warp 6` ("Columbus") และ `/warp 14` ("Hell King Kong") ·
     ถ้าเหลือเวลา: `/warp 130` และฉาก 1 (จุดล็อกอินปกติ) ซึ่งรอบนี้ต่อสายแล้วเหมือนกัน
  6. **[คำทำนาย ไม่ใช่ผลวัด]** ช่วงที่ mine ไว้: ฉาก 1 = 10..125 · 3 = 10..105 · 6 = 71..105 ·
     14 = 1..115 · ฉาก 9 แค่ 93/98 · ฉาก 130 แค่ 10/150 · หลุดช่วง = finding
  7. 🔴 **ตัวควบคุมที่สำคัญกว่าข้อ 1-6 รวมกัน (pf-adversary สั่งให้ถาม)** -- ในฉาก 14 บันทึก `LV` ของ
     **มอนสเตอร์ศัตรู** หนึ่งตัว (`Glaucoma` / `Lava shakers` / `Carlos` · รายชื่อครบในไฟล์รอบ)
     ตัวเหล่านี้ **ส่งเลเวลมาตั้งแต่ `RE-117`** (105 · `Carlos` 115) คนละเส้นทางกับ census ปกติ ⇒
     ขึ้น `LV 105`/`115` = ยืนยันการวินิจฉัย · **ขึ้น `LV 1` ด้วย** = ไคลเอนต์ไม่ได้วาดจากฟิลด์นี้
     และรอบ `7ste68` แก้ผิดจุด
- pass criteria (สองชั้น แยกกันเด็ดขาด):
    wire/DB -- **ทำแล้วในรอบ `7ste68`**: เทสอ่านเลเวลกลับออกจาก `generation.pc` รายตัวครบทั้ง
      13 census source · สวีท 6628 passed / 327 skipped / 14240 subtests · พิสูจน์แค่ว่า
      **เซิร์ฟเวอร์ส่งไบต์ออกไป** ไม่พิสูจน์สิ่งที่ไคลเอนต์วาด
    client-observable -- **ชั้นนี้เท่านั้นที่ตัดสินใบ**: ใน >= 3 ฉากที่ warp ถึงใน login เดียว ป้าย `LV`
      แสดงเลข **ไม่ใช่ 1** และ **ต่างกันระหว่างตัวในฉากเดียวกัน** · อย่างน้อยหนึ่งฉากต้องช่วงกว้าง
      (3, 4, 5, 6, 14) -- ฉากค่าเดียวลำพังไม่พิสูจน์ว่าเป็นฟิลด์รายตัว
      · **ผลลบมีค่าเท่าผลบวก**: ยังเห็น `LV 1` ทั้งที่ชั้น wire ผ่าน ⇒ ไคลเอนต์อ่านจากที่อื่น
      ⇒ เปิดใบ RE ใหม่พร้อมภาพนิ่ง ไม่ใช่ FAIL ของใบนี้ · ผิดบางฉาก ⇒ ระบุ **ชื่อฉาก** ที่พลาด
- nonclaims:
  1. ไม่พูดเรื่อง **สี/faction/ชนิด actor** -- P-2 ยังเปิด บันทึกสีอย่างเดียว **ห้ามอนุมานสาเหตุ**
  2. ไม่แก้ไขอะไรเรื่องมอนสเตอร์ศัตรู -- lane B ส่งเลเวลของมันมาตั้งแต่ `RE-117` แล้ว ใบนี้แค่**อ่าน**
     ค่าของมันเป็นตัวควบคุม (ข้อ 7) · ไม่พิสูจน์ HP/ชื่อ/พิกัด · ไม่พิสูจน์ว่า `n_LEVEL_MIN` คือเลเวล
     จริงต่อ spawn (เป็น min ของช่วง หลายแถวมี max สูงกว่า)
  3. ไม่ทดสอบกลไก `/warp` เอง -- ร่วมกับ `GT-192` ซึ่ง **ยังเปิดอยู่และใบนี้ห้ามแก้** · warp พังกลางทาง
     = `NO-RESULT` ของใบนี้ และเป็นหลักฐานของ `GT-192`
  4. ความต่างจากเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` · ไม่อ้างว่า PR merge แล้ว
- RECHECK (ตัดสินด้วยเนื้อโค้ด ห้ามเทียบเลข commit) -- ต้องได้ hit จริง:
  ```
  git -C pirate-force-server fetch origin
  git -C pirate-force-server show origin/main:src/pirateforce_foundation/world_population_bg0006.py | findstr /C:"level=placement.identity.level"
  ```
  🔴 **แก้รอบ `mcf4qp` (pf-adversary D3):** ฉบับเดิมเป็น `cd ... && ... | grep -n ...` ซึ่ง **รันบนเครื่องเจ้าของไม่ได้เลย**
  -- PS 5.1 ไม่รับ `&&` และ `grep` ไม่มีบน Windows ⇒ ผู้เทสจะได้ error แล้วอ่านตามกฎของใบว่า "ยังไม่ merge ห้ามบูต"
  ทั้งที่โค้ดอยู่บน `main` แล้ว · หนึ่งบรรทัด = หนึ่งคำสั่ง · รันจากโฟลเดอร์แม่ที่มี `pirate-force-server` อยู่ข้างใน
  ว่าง/พัง = PR #524 ยังไม่ merge ⇒ คง `PENDING` **ห้ามบูต** (เทส branch ก่อน merge ได้ ถ้าเปลี่ยน
  `origin/main` เป็น `origin/claude/dazzling-volta-7ste68` แล้วเขียนในผลว่าใช้ตัวไหน)
  🔴 **แก้คำสั่ง RECHECK 2026-09-02T04:5x+07:00 (LANE-A รอบ `2p4n3h`, เจ้าของใบเอง)**: เดิมค้นหา
  ~~`world_census_level.leveled_npc_attr`~~ ซึ่ง**เลิกปรากฏในไฟล์นั้นแล้ว**หลังรอบ `2p4n3h` ย้าย
  call site ไปเป็น `world_census_gait.census_npc_attr` (ห่อ `leveled_npc_attr` อีกที ระดับยังส่ง
  เหมือนเดิมทุกไบต์บวกฟิลด์ gait) ถ้าไม่แก้ คำสั่งเดิมจะคืนค่าว่างและอ่านผิดว่า "PR #524 ยังไม่ merge"
  ทั้งที่ merge แล้ว · คำสั่งใหม่ค้นหาอาร์กิวเมนต์ระดับซึ่งอยู่ในทั้งสองรูปแบบ
  🔴 **คำเตือนที่สำคัญกว่าคำสั่ง RECHECK (LANE-A รอบ `2p4n3h`, วัดแล้วผ่าน dispatcher จริง)**:
  ก่อนรอบ `2p4n3h` การ **คลิก NPC หนึ่งครั้ง** ทำให้เซิร์ฟเวอร์ส่ง actor ทั้ง 108 ตัวของฉาก 1 ใหม่
  **โดยไม่มีฟิลด์เลเวลเลย** (`world_face_frame.build_face_state` เรียก `make_npc_attr` เปล่า ๆ
  ซึ่งไม่มีพารามิเตอร์ level) ⇒ ภาพที่ถ่ายหลังคลิกใครสักคน **เป็นเฟรมที่ถูกย้อนแล้ว** และจะขึ้น
  `LV 1` แม้โค้ดของ `7ste68` จะอยู่บน main · ฉาก 14 เป็นแบบเดียวกันเฉพาะ NPC พลเรือน
  ⇒ **ถ้ารัน `GT-200` ก่อนรอบ `2p4n3h` ขึ้น main: ห้ามคลิก NPC ก่อนถ่ายภาพ**
  ถ้ารันหลังจากนั้น: คลิกได้ตามปกติ และให้บันทึกไว้ในผลว่ารันบน main รุ่นไหน
- links: `pirate-force-server#524` · `RE-117` · `RE-201` (ปิดแล้ว) · `GT-192` (ห้ามแก้)
- result: (ผู้เทสกรอก: PASS/FAIL/BLOCKED/NO-RESULT · หลักฐาน · timestamp · `OBSERVER_CONFIRMED`)

**ผู้เปิดใบ: LANE-A รอบ `7ste68` 2026-09-02T01:55+07:00 -- LANE-A บริโภคผลใบนี้เอง**

## GT-214 CHOOSE-NPC-SCENE2-CLICK-ANSWER-AND-HOSTILE-SAFETY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS-AGAIN (regression ยืนยันซ้ำ R321 2026-09-06 11:52 · ผลแรก PASS ที่ R307 2026-09-03) · จาก notes_to_chief/20260906_1255_KA1A-R321-*.md §RESULT · 🟢 READY -- โค้ดขึ้น `main` แล้ว (`server#591` merge 2026-09-02T11:31Z) วัดเองโดย LANE-A รอบ `4uztfj` · ~~[BLOCKED -- โค้ดยังไม่ขึ้น main]~~ · 🔴 **RECHECK ยังต้องรันก่อนบูตทุกครั้ง** และข้อ 2 **เปลี่ยนสตริง** ในรอบ `4uztfj`: โทเคน `dead_monster_needs_a_mob_death_body` ถูกแทนด้วย `clicked_body_is_dead_needs_a_mob_death_body` (COO-DECISION 20260902_1945 ย่อการ์ด 'ตายแล้ว' ให้ตัดสินเฉพาะร่างที่ถูกคลิก) ⇒ สตริงใหม่ขึ้น main พร้อม PR รอบ `4uztfj` เท่านั้น · ถ้า RECHECK ข้อ 2 ยังไม่เจอสตริงใหม่ **ยังบูตได้ตามปกติ** ผลไม่เปลี่ยน แต่ให้จดว่าบูตบนคอมมิตก่อนรอบนั้น · 🔴 **แก้ข้อ (ข) และคำทำนายข้อ 10 ในรอบ `qa86im`** (ใบ chief `20260903_0300`): จุดเรียกส่ง ledger แล้วตั้งแต่ `server#619` ⇒ บรรทัด `..._ANSWERED` เปลี่ยนสองช่องเอง และรอบ `qa86im` เพิ่มช่องที่สาม `dead_as_corpse=` · **เกณฑ์ตัดสินไม่เปลี่ยนสักข้อ** ใบนี้ยังห้ามฆ่ามอน ⇒ สามช่องท้ายยังต้องเป็น 0]

ATTENDED: บูต DB สำเนา `state\run_gt214_<stamp>.sqlite3` เท่านั้น (ห้ามเปิด canonical) เซิร์ฟก่อนไคลเอนต์ทีหลัง ไม่มีแฟล็ก scenario ใด ๆ, เก็บคอนโซล `2>&1` ทั้ง stdout+stderr -> โฟกัสช่องแชทจริง พิมพ์ `/warp 2` Enter รอ ~3 วิ -> ถ่าย `S02-BEFORE` (คลิกขวาลากจัดกล้องได้ ไม่ยิงอะไร) -> คลิกซ้าย actor **หนึ่งครั้งก่อนเดิน** (คาดว่าเงียบ = ผลที่ถูกต้อง ไม่ใช่ FAIL) แล้วเดินหนึ่งก้าว (`W`/`S`) หลังจากนั้นห้ามเปลี่ยน facing อีกนอกจากก้าวที่สั่ง
ATTENDED: หาโทเคนคอนโซล -- คลิกก่อนเดิน: ต้องเจอ `LANE_A_CHOOSE_NPC_SCENE2_DECLINED reason=no_player_position_walk_one_step` และไม่มี `..._ANSWERED` คู่กัน · คลิกหลังเดิน (สามครั้งคนละ actor): ต้องเจอ `LANE_A_CHOOSE_NPC_SCENE2_ANSWERED placement=<n> visible=<n> hostile=<n> ...` ทุกครั้ง โดยช่อง `wounded=` `dead_at_ceiling=` `dead_as_corpse=` ต้องเป็น `0` ทั้งสาม (ใบนี้ห้ามตีมอน) · 🔴 `visible=97` `hostile=12` เป็น **คำทำนาย ไม่ใช่เงื่อนไขผ่าน** (ข้อ 10 ของใบ) -- เลขต่างจากนี้ = finding จดดิบ ๆ ไม่ใช่ FAIL · ถ่าย `S02-AFTER` x3, `S02-MOB-BEFORE/AFTER`, `S02-COL+2s/+30s` เต็มความละเอียด พร้อมจดสีป้ายชื่อทุกป้ายทุกภาพ (เขียน `none` ถ้าไม่มีสี ห้ามอนุมานสาเหตุ)
ATTENDED: ตัดสิน PASS/FAIL ที่ **ชั้น client-observable เท่านั้น**: `S02-BEFORE` เห็นฝูง actor ยืนจริง, `S02-AFTER` ตัวที่ถูกคลิกหันมาหาเราและมีชื่อ/แถบ HP ขึ้น (ชื่อว่าง = บันทึกไม่ใช่ FAIL อัตโนมัติ), `S02-MOB-AFTER` มอนยังเป็นมอนไม่กลายเป็นชาวบ้านไม่หาย, `S02-COL+30s` ครบ 30 วิไม่มีหน้าต่างบทสนทนา/เควสต์และยังอยู่ฉาก 2 -- ชั้น wire/DB (grep คอนโซล, sha256, integrity_check) พิสูจน์ได้แต่ **ตอบไม่ได้ว่าเห็นอะไรบนจอ** ห้ามใช้แทนกัน · มี `..._ANSWERED` ครบแต่จอไม่ขยับ = ผลลบที่ถูกต้อง ไม่ใช่ FAIL · ไม่มี `LANE_HOOK_FIRED` เลยตอนคลิก = `NO-RESULT`
ATTENDED: RECHECK สามข้อบน `origin/main` ก่อนบูตทุกครั้ง -- ข้อ 1 (`production_allowed = True`) และข้อ 3 (`pytest tests/test_lane_a_choose_npc_scene2.py` เขียวทั้งชุด) ว่าง/แดง = คง `[BLOCKED]` ห้ามบูต · ข้อ 2 ต้องเจอ `no_player_position_walk_one_step` (ไม่เจอ = ห้ามบูตเช่นกัน) ส่วนสตริงใหม่ `clicked_body_is_dead_needs_a_mob_death_body` **ไม่เจอก็ยังบูตได้ตามปกติ ผลไม่เปลี่ยน** ให้จด branch/commit ที่บูตแทน (หัวใบรอบ `4uztfj`) · จดสตริงเวอร์ชันที่เจอจริง (`hp=ceiling`/`from_ledger=0` ของคอมมิตเก่า หรือ `hp=ledger from_ledger=12 dead_as_corpse=0` ของ `server#619`/รอบ `qa86im`) พร้อม branch/commit ที่บูต ทั้งสองไม่ใช่ FAIL
ATTENDED: 🔴 STOP ทันทีถ้ามีหน้าต่างบทสนทนา/เควสต์โผล่ หรือรู้ตัวว่าอยู่คนละแมพหลังคลิก -- ปิดไคลเอนต์ รายงานทันทีเป็น FAIL, ห้ามใช้ `Q`/`E` เป็นตัวเช็ค NO-CRASH ให้ใช้คลิกขวาลากกล้องเท่านั้น

> เปิดโดย LANE-A (WORLD) รอบ `cu1il6` 2026-09-02T17:40+07:00 · **LANE-A บริโภคผลเอง**
> numbering: ตัวนับร่วมกับ `CLIENT_RE_QUEUE.md` -- สูงสุดตอนเปิด = `GT-213` (`RE` สูงสุด = 210) ⇒ ใบนี้ `214` · รันคำสั่งกฎ ② ซ้ำตอน rebase
> 🔴 **ใบนี้ไม่แซงคิวบูต** ของ `FROM_CHIEF_R305`: `GT-207` -> `GT-193` -> `GT-205` -> `GT-204` (ท้ายสุด) · ใบนี้ต่อ **หลัง** สี่ใบนั้น
> บูต/DB/teardown ตาม `ATTENDED_SESSION_RUNBOOK.md` · teardown ต้องรันเสมอ แม้รอบจบเพราะเลิกเล่นเฉย ๆ (ปฏิเสธ boot stamp เก่ากว่า 420 นาที)

- objective: ข้อพิสูจน์เดียว -- **คลิกซ้ายบน actor ในฉาก 2 (Prison Exile Island · `Bg0002` · 97 actor) แล้วไคลเอนต์วาดคำตอบจริงบนจอ**
  ที่เมื่อก่อนคลิกแล้วเซิร์ฟเวอร์เงียบสนิท · ครึ่งความปลอดภัยอยู่ในข้อพิสูจน์เดียวกัน **ไม่แยกใบ**: คำตอบส่ง actor ทั้ง 97 ใหม่ทุกครั้ง
  ⇒ มอน 12 ตัวที่สำมะโนขาเข้าเสียบเป็นศัตรู (placement 50,58,59,60,61,77,78,79,80,86,87,88) **ต้องยังเป็นมอนบนจอ ไม่กลายเป็นชาวบ้าน**
  (ทรงเสียแบบเดียวกับฉาก 14 รอบ R274 แต่คนละชุดตัวเลข)
- RECHECK (ตัดสินด้วย **เนื้อโค้ดบน `origin/main`** ห้ามเทียบเลข commit · ผ่านครบสามข้อ = เลื่อนเป็น `READY` ได้เอง):
  ```
  (cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene2.py | findstr /C:"production_allowed = True")
  (cd pirate-force-server && git show origin/main:src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene2.py | findstr /C:"no_player_position_walk_one_step" /C:"clicked_body_is_dead_needs_a_mob_death_body")
  (cd pirate-force-server && py -3 -m pytest tests/test_lane_a_choose_npc_scene2.py -q)
  ```
  ข้อ 1-2 ต้องเจอจริงทั้งสองสตริง (เลือกสตริงที่เป็น **เนื้อโค้ด** ไม่ใช่ข้อความใน docstring:
  `hp=ceiling` ที่คอนโซลพิมพ์ตอนรันเป็นผลของ f-string จึง **ไม่มีในไฟล์** ห้าม grep คำนั้น -- วัดแล้วรอบ `cu1il6`) · ข้อ 3 ต้องเขียวทั้งชุด · ว่าง/แดง = ยังไม่ merge ⇒ คง `[BLOCKED]` **ห้ามบูต ไม่เสียเวลาผู้เทสแม้แต่นาทีเดียว**
  ทดสอบก่อน merge ได้ถ้าเปลี่ยน `origin/main` เป็น branch ของรอบ `cu1il6` แล้ว **เขียนในผลว่าใช้ branch/commit ไหน**
- db: `state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิดไฟล์ canonical** ⇒ `state\run_gt214_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา
  จด sha256 สำเนาก่อน/หลัง · sha256 canonical ก่อน/หลัง ต้อง **ไม่เปลี่ยน** · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง
  (รอบคัดลอก DB ⇒ ตัวละครกลับไป spawn ทุกบูต เป็นเรื่องปกติ ไม่ใช่ผลวัด)
- server args: บูตมาตรฐาน `BRIDGE_BOOT_PROCEDURE.md` · 🔴 **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` · GM ใน `config/gm_accounts.json`
  🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)** -- โทเคนของเลนออกทาง **stderr** ล้วน ถ้าเก็บแต่ stdout จะไม่เห็นอะไรเลย
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt214_<stamp>.sqlite3
  ```
- เส้นทาง: `/warp 2` เปล่า **ไม่ใส่พิกัด** (เส้นทางของ `GT-192` ห้ามคิดใหม่) · สำมะโนประกอบตอนไปถึงแล้ว (chief รอบ `4w5j25` ขยายทริกเกอร์ครบทุกฉากยกเว้นบ้าน) ⇒ **ไม่ต้องเดินหาฝูงชน**
- steps: (เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ)
  1. RECHECK ผ่านก่อน · LOCK_GAME · จด boot stamp · sha canonical · คัดลอก DB
  2. บูตเซิร์ฟเวอร์ **ใหม่สด** ก่อน แล้วค่อยบูตไคลเอนต์ (ไคลเอนต์ที่ถูกฆ่า = เซิร์ฟเวอร์ยังถือเซสชัน ตัวถัดไปค้าง "connecting" ตลอดกาล ⇒ **รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ**) · ห้ามทิ้งไคลเอนต์ไว้โดยไม่มีเซิร์ฟเวอร์ (ตายใน ~3.5 นาที) · ล็อกอิน GM ให้เข้าฉากจริงก่อน
  3. คลิกช่องแชท **ยืนยัน focus จริง** (พิมพ์ตอนไม่ focus = ฮอตคีย์) · พิมพ์ `/warp 2` · Enter · รอ ~3 วิ
     (`/warp` คือคำสั่ง GM **ไม่ใช่** ตัวยิงแชทที่ต้องยาว 12 ตัวอักษรพอดี -- ห้ามเติมตัวอักษรให้ครบ 12)
  4. ภาพนิ่ง **เต็มความละเอียด** `S02-BEFORE` -- ยังไม่คลิกใคร · จัดมุมกล้องด้วย **คลิกขวาลาก** เท่านั้น
     (คลิกขวาลากหมุน **กล้องอย่างเดียว** facing ไม่ขยับ ไม่ยิงอะไร ปลอดภัยทุกจังหวะ)
  5. 🔴 **คลิกทดสอบครั้งแรก ก่อนเดิน -- คาดว่าเงียบ และนั่นคือสิ่งที่ถูกต้อง**: คลิกซ้าย actor หนึ่งตัวหนึ่งครั้ง
     responder คำนวณทิศหันจาก `last_target_pos` ของผู้เล่นเอง ซึ่งยังเป็น `None` ก่อนก้าวแรก ⇒ **ปฏิเสธโดยตั้งใจ**
     คอนโซลต้องมี `LANE_A_CHOOSE_NPC_SCENE2_DECLINED reason=no_player_position_walk_one_step` · **จอไม่ขยับ = ผลที่คาดไว้ ไม่ใช่ FAIL** · จดบรรทัดดิบไว้แล้วไปข้อ 6
  6. **เดินหนึ่งก้าว** (`W` หรือ `S`) · หลังจากนี้ 🔴 **ห้ามเปลี่ยน facing ของตัวละครอีก** นอกจากก้าวเดินที่ใบสั่ง (`W/A/S/D` และ `Q`/`E` ยิง `TargetPosVital`)
  7. **คลิกซ้ายหนึ่งครั้ง** บน actor หนึ่งตัว โดยมีตัวอื่นในเฟรมอย่างน้อยสองตัว · `S02-AFTER` ภายใน ~3 วิ · จดบรรทัด `..._ANSWERED` ดิบทุกครั้ง
  8. ทำซ้ำข้อ 7 อีกสองครั้งกับ actor คนละตัว (รวมสามคลิกที่ได้คำตอบ)
  9. **ครึ่งความปลอดภัย:** จัดเฟรมให้มี actor ที่ **หน้าตาเป็นมอน** อย่างน้อยหนึ่งตัวอยู่ในภาพ · `S02-MOB-BEFORE` ⇒ คลิก actor ตัวใดก็ได้หนึ่งครั้ง ⇒ `S02-MOB-AFTER` ภายใน ~3 วิ · เทียบว่ามอนตัวนั้น **ยังเป็นมอนตัวเดิม** (โมเดลเดิม ไม่กลายเป็นชาวบ้าน ไม่หายไป)
  10. **[ขั้นสังเกต ไม่ใช่เกณฑ์ตัดสิน]** ทำ **ก็ต่อเมื่อ** มีมอนที่ **บาดเจ็บอยู่แล้ว** จากใบอื่นในเซสชันเดียวกัน · 🔴 **ห้ามตีมอนเพื่อทำขั้นนี้** (`NOW.md` ห้ามใบตีมอนจนกว่า P-1 และ P-2 ปิด) · ถ้าไม่มี ให้ **ข้าม** แล้วเขียนว่า "ไม่มีมอนบาดเจ็บ ข้าม"
      ถ้ามี: `S02-HP-BEFORE` (เห็นแถบ HP พร่อง) ⇒ คลิก actor ตัวใดก็ได้หนึ่งครั้ง ⇒ `S02-HP-AFTER` · จดว่าแถบ HP **เต็มกลับ** หรือ **ยังพร่อง**
      ~~**[คำทำนาย]** เต็มกลับ เพราะ responder ไม่มี combat ledger (`hp=ceiling` ในคอนโซลบอกไว้ตรง ๆ)~~ **คำทำนายใหม่ (แก้รอบ `qa86im` ตามใบ chief `20260903_0300`): ยังพร่องอยู่** ถ้ามอนตัวนั้นบาดเจ็บจริงใน ledger — `server#619` ลง `mob_combat_ledger=` ที่จุดเรียกแล้ว ⇒ `CORE-REQUEST 20260902_1735` ปิดที่ชั้นโค้ด และรอบนั้นคอนโซลจะพิมพ์ `wounded=` **ไม่ใช่ 0**
      · **ทั้งสองผลไม่ใช่ FAIL ของใบนี้** เป็นการวัดที่ใบนี้ถูกขอให้ยืนยันด้วยตา · จดสิ่งที่เห็นตรง ๆ พร้อมบรรทัดคอนโซลดิบของคลิกนั้น
  11. **ครึ่งความปลอดภัยที่สอง:** ฉาก 2 มี actor ชื่อ `Columbus` (`n_ID 360`) ซึ่ง **ไม่ใช่ Columbus ของพอร์ตรอยัล** · คลิกมันหนึ่งครั้ง แล้ว **จ้องจอ 30 วินาที ไม่คลิกอะไรเลย** · `S02-COL+2s` `S02-COL+30s` · หาไม่เจอให้คลิกทีละตัวแล้วอ่าน `placement=` ย้อนจากคอนโซล
  11b. **[ขั้นสังเกต ไม่ใช่เกณฑ์ตัดสิน · pf-adversary D2]** ทำ **ก็ต่อเมื่อ** มีของวางอยู่บนพื้นในฉาก 2 จากใบอื่นในเซสชันเดียวกัน · 🔴 **ห้ามฆ่ามอนเพื่อสร้างเงื่อนไขนี้**
      เฟรมตอบคลิกประกอบผ่าน `make_runtime_remote_actors` ซึ่ง derived mask บอกว่า **ไม่มี ground list** (`0x02` วัดแล้ว บิต `0x08` ไม่ติด)
      ถ้ามีของบนพื้น: `S02-GROUND-BEFORE` ⇒ คลิก actor หนึ่งครั้ง ⇒ `S02-GROUND-AFTER` · จดว่าของ **ยังอยู่** หรือ **หายไป**
      **[ยังไม่วัด]** ผลของบิตนี้กับไคลเอนต์เป็นการอ่านแบบ static ของสาย B เท่านั้น · ใบ `20260902_1806_LANE-A-TO-LANE-B-*`
  11c. **[ขั้นสังเกต · pf-adversary D6]** ในภาพ `S02-AFTER` ให้ดู actor **ตัวอื่น** ที่ไม่ได้ถูกคลิกด้วย: **ยังยืนที่เดิม** หรือขยับ/หันไปทางอื่น
      (เฟรมส่ง NPCAttr ให้ 96 ตัวโดย **ไม่มี** MovementAttr ซึ่งไม่มีตำแหน่งอยู่ในนั้น — ยังไม่มีใครวัดว่าไคลเอนต์ "คงของเดิม" หรือไม่)
  12. ตัวเช็ค NO-CRASH: **คลิกขวาลากหมุนกล้อง** เท่านั้น · 🔴 **ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้** · ออกด้วย X
  13. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err`, `capture_v141\GAME_LIVE.txt`, `GAME_EVENTS_LIVE.txt` + sha256 · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ**
  🔴 **ขอบเขต:** คลิกเพื่อ **เลือก** เท่านั้น -- ห้ามตีมอน ห้ามใช้สกิล ห้ามคลิกโจมตี · เผลอตี = จดไว้ในผล
  🔴 **STOP:** มีหน้าต่างบทสนทนา/เควสต์โผล่ หรือรู้ตัวว่าอยู่คนละแมพหลังคลิก ⇒ **หยุดทั้งใบทันที ปิดไคลเอนต์ รายงานทันที = FAIL**
- pass criteria (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน · grep คอนโซลรวม `2>&1`):
      (ก) คลิกข้อ 5: มี `LANE_A_CHOOSE_NPC_SCENE2_DECLINED reason=no_player_position_walk_one_step` และ **ไม่มี** `..._ANSWERED` คู่กัน
      (ข) ทุกคลิกหลังก้าวเดิน: ~~`LANE_A_CHOOSE_NPC_SCENE2_ANSWERED placement=<n> visible=97 hostile=12 hp=ceiling from_ledger=0 wounded=0 dead_at_ceiling=0`~~ **สตริงใหม่ (แก้รอบ `qa86im` ตามใบ chief `20260903_0300`)**:
          `LANE_A_CHOOSE_NPC_SCENE2_ANSWERED placement=<n> visible=97 hostile=12 hp=ledger from_ledger=12 wounded=0 dead_at_ceiling=0 dead_as_corpse=0` และ label ที่ส่ง `LANE_A_CHOOSE_NPC_SCENE2_FACE_P<n>`
          🔴 **ทำไมเปลี่ยน:** `server#619` (R313) ลง `mob_combat_ledger=` ที่จุดเรียก ⇒ `hp=ceiling from_ledger=0` กลายเป็น `hp=ledger from_ledger=12` **แม้ผู้เทสไม่ได้ฆ่าอะไรเลย** (chief วัดผ่าน dispatcher จริง) · ช่อง `dead_as_corpse=` เพิ่มในรอบ `qa86im`
          🔴 **บูตบนคอมมิตก่อน `server#619` จะได้ `hp=ceiling from_ledger=0` และก่อน `4uztfj` จะจบที่ `from_ledger=0` เฉย ๆ — ทั้งสองกรณี ไม่ใช่ FAIL** ให้จดบรรทัดดิบตามที่เห็น พร้อมคอมมิตที่บูต
          🔴 **`hp=ledger from_ledger=12` ยกเป็นหลักฐานว่า HP มาจาก ledger ไม่ได้** (`COO-DECISION 20260902_1945` ข้อ 4.3): ledger ที่เพิ่งเปิดและไม่มีการรบเลยก็พิมพ์เลขนี้ · ช่องที่ยกเป็นหลักฐานได้คือ `wounded=` เท่านั้น
          · `wounded=` `dead_at_ceiling=` `dead_as_corpse=` **ต้องเป็น `0` ทั้งสามช่องในใบนี้** เพราะใบนี้ไม่มีขั้นตอนฆ่า (ค่าอื่นที่ไม่ใช่ 0 = มีคนตีมอนในเซสชันเดียวกัน ⇒ จดดิบ ๆ แล้วรายงาน ไม่ต้องตัดสินเอง)
          **[คำทำนาย ไม่ใช่ผลวัด]** `visible=97` และ `hostile=12` เท่ากันทุกคลิก · เลขต่างจากนี้ = finding ให้จดดิบ ๆ ไม่ต้องตีความ
      (ค) ตลอดเวลาที่อยู่ฉาก 2: **ไม่มี** event `core_request_014_columbus_npc_conversation_sent_once` และ **ไม่มี** label `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` และ **ไม่มี** `core_request_014_columbus_scene17_teleport_sent`
      (ง) `integrity_check` = `ok` ทั้งสองครั้ง · sha canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      🔴 **ชั้นนี้ตอบไม่ได้เลยว่ามีอะไรถูกวาดบนจอ หรือผู้เล่นยืนอยู่ที่ไหน**
    client-observable (ต้องมีคนนั่งหน้าจอ · **ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (จ) `S02-BEFORE`: หลัง `/warp 2` **เห็นฝูง actor ยืนอยู่จริง** ก่อนคลิกใคร (ไม่ต้องเดินไปหา)
      (ฉ) `S02-AFTER`: ตัวที่ถูกคลิก **หันมาหาตัวละครเรา** และมี **ชื่อ และ/หรือ แถบ HP** ขึ้น -- บันทึกสิ่งที่แสดงตรง ๆ · **ช่องชื่อว่าง = การบันทึก ไม่ใช่ FAIL อัตโนมัติ** (`GT-030-R3`)
      (ช) `S02-MOB-AFTER` เทียบ `S02-MOB-BEFORE`: มอนในเฟรม **ยังเป็นมอน** ไม่กลายเป็นชาวบ้าน ไม่หายไป · actor อื่นอยู่ครบ หน้าตาเดิม ป้าย `LV` ไม่หายและไม่กลายเป็น `1`
      (ซ) `S02-COL+30s`: หลังคลิก `Columbus` ครบ 30 วินาที **ไม่มีหน้าต่างบทสนทนา/เควสต์ใด ๆ** และ **ยังอยู่ฉาก 2** (พื้นหลังเดิม HUD เดิม ฝูงเดิม)
      (ฌ) 🔴 **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ ทุกภาพ** · เขียนคำว่า `none` ออกมาแทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** (ห้าม contact sheet/ภาพย่อ/วิดีโอ) · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067`) · ความต่างจากภาพเซิร์ฟเวอร์จริงลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 **ชั้นนี้ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์**
- **ผลลบมีค่าเท่าผลบวก:** มี `..._ANSWERED` ครบแต่จอไม่ขยับ ⇒ คำตอบคือ **เซิร์ฟเวอร์ตอบแล้ว ไคลเอนต์ไม่วาด** ⇒ ไม่ใช่ความผิดของ lane hook · **ห้ามถอน `production_allowed` ด้วยเหตุนี้** ให้เปิดใบ `RE-` ใหม่พร้อมภาพและเลข `visible=` ·
  มี `LANE_HOOK_FIRED` แต่ไม่มี `..._ANSWERED` ⇒ เช็คก่อนว่าเดินหนึ่งก้าวจริง (ข้อ 6) · ไม่มี `LANE_HOOK_FIRED` เลยตอนคลิก ⇒ คลิกไม่ถึงสาขานี้ = `NO-RESULT`
- nonclaims:
  1. ไม่พิสูจน์ว่าสำมะโนขาเข้าถูก/ครบ (`GT-192` ห้ามแก้) · ไม่พิสูจน์เลข `LV` (`GT-200` ห้ามแก้) · ไม่พิสูจน์กลไก `/warp` เอง
  2. ไม่ตัดสินฉาก 3 (`GT-210`) · ฉากโรสเตอร์เก้าเกาะ (`GT-212`) · ฉาก 14 (`GT-134`/`GT-213`) · ฉาก 1 · ฉาก 17
  3b. **ไม่พิสูจน์ว่าเฟรมนี้ทำอะไรกับของบนพื้น หรือกับตำแหน่งของ 96 ตัวที่ไม่ได้ถูกคลิก** -- ข้อ 11b/11c เป็นการ **สังเกต** ล้วน · `RE-092` พิสูจน์ replace-by-omission **ระดับชุด actor** ไม่ใช่ระดับ attribute และไม่ใช่ ground list
  3. **ไม่พิสูจน์คอมแบต/aggro/HP** -- ข้อ 10 เป็น **การสังเกต** ของช่องว่างที่รู้อยู่แล้ว (`hp=ceiling`) **ไม่ใช่เกณฑ์ผ่าน/ตก** และใบนี้ **ไม่ได้แก้** อะไรเรื่องนั้น (`CORE-REQUEST 20260902_1735`)
  4. ไม่พูดเรื่องความหมายของสีป้าย -- `RE-067` ยังเปิด · จดสีอย่างเดียว
  5. ไม่พิสูจน์ว่า index space เป็น scene-aware แล้ว · ไม่พิสูจน์ว่าอะไรรอดข้าม relog · ไม่แซงลำดับบูตของ `FROM_CHIEF_R305`
- links: `lane_hooks/lane_a_choose_npc_scene2.py` · `lane_hooks/lane_a_scene_census.py` · `GT-210` · `GT-212` · `GT-213` · `GT-192` · `GT-200` · `RE-067` · `notes_to_chief/20260902_1735_LANE-A-CORE-REQUEST-*.md`
- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · branch/commit ที่บูต · ภาพ `S02-BEFORE`/`S02-AFTER` (สามคลิก)/`S02-MOB-BEFORE`/`S02-MOB-AFTER`/`S02-HP-*` (หรือ "ข้าม")/`S02-COL+2s`/`S02-COL+30s` · บรรทัดคอนโซลดิบทุกบรรทัด (`..._DECLINED` และ `..._ANSWERED` ทุกคลิก) · บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 ทั้งสี่ค่า · timestamp +07:00 · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `cu1il6` 2026-09-02T17:40+07:00 -- LANE-A บริโภคผลใบนี้เอง**

## GT-220 GROUND-DROP-SURVIVES-A-CLICK-ON-A-TOWNSPERSON-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS (R307 2026-09-03 — killed mobs, 2 drops on floor survived NPC clicks, picked with 1 click) · ความพยายามซ้ำ R321 2026-09-06 ถูก BLOCKED ด้วยเหตุไม่เกี่ยวกับเกณฑ์ใบนี้เอง (มอนฉาก 2 เขียว/ตีไม่ได้จากบั๊ก §1 login-126-no-faction) — ไม่ใช่การพลิกผล PASS เดิม · RESULT: GT-220 BLOCKED R321 2026-09-06 (no attackable mob; original PASS stands from R307) · จาก notes_to_chief/20260903_1901_KA1A-R307-*.md + notes_to_chief/20260906_1255_KA1A-R321-*.md §8 · 🟢 READY -- เงื่อนไขข้อ 1 ของใบสั่ง chief (`20260903_0505` ข้อ ④) ผ่านแล้ว: RECHECK 1 วัดเองโดย LANE-A รอบ `umlyof` บน `origin/main` (`server#625`) ⇒ เปิดเป็น READY · ผู้เทสรัน RECHECK เองก่อนบูตทุกครั้ง]

ATTENDED: 🔴 ขั้น 0: LOCK_GAME · boot stamp · sha canonical · copy DB · RECHECK สองข้อบน `origin/main` ไม่ผ่าน = ไม่บูต (BLOCKED) -> บูตปกติบน `main` ไม่มีแฟล็ก `--*-scenario` ใด ๆ ด้วย `-SecondPasswordMode bypass` + บัญชี GM -> เข้าเกม พิมพ์ `/warp 2` เปล่า (คลิกช่องแชทยืนยัน focus จริงก่อน) -> ฆ่ามอนให้ของตก >=3 ชิ้น ห้ามเก็บ ถ่าย S0 ทันที -> คลิกซ้ายชาวเมือง/NPC (ไม่ใช่ของที่ตก) 1 ครั้ง รอ 3 วิ ถ่าย S1 · ทำซ้ำ 2 ครั้งกับ NPC คนละตัวถ้ามี ถ่าย S2 หลังคลิกสุดท้าย ทั้งหมดต้องจบภายใน 90 วินาทีจาก S0 (ของมีอายุ 120 วิ)
ATTENDED: หาโทเคนคอนโซล (stdout+stderr รวม `2>&1`): `GROUND_UNDER_PUBLICATION_REACHED lane_hooks.choose_npc_response.scene_2` ต้องมี · ต้องไม่มี `GROUND_ACTORS_LIVENESS_UNKNOWN` ของฉาก 2 เลย · `GROUND_ROWS_SWEPT_BY_READ` >0 ใน 90 วิแรก = FAIL ชั้น wire · `LANE_A_CHOOSE_NPC_SCENE2_ANSWERED` ต้องมีหนึ่งบรรทัดต่อคลิก (สามคลิก)
ATTENDED: ตัวตัดสินจริงคือชั้น client-observable เท่านั้น (ห้ามอนุมานจากคอนโซล): ของทุกชิ้นที่เห็นใน S0 ต้องยังเห็นใน S1 และ S2 จากมุมกล้องเดิม แบบนับทีละชิ้นแบบ full-res -- หายแม้ชิ้นเดียวหลังคลิกใด = FAIL ชั้นนี้ (จดว่าหายกี่ชิ้นหลังคลิกที่เท่าไร) · ของครบ = PASS ชั้นนี้ · ถ้ามี `GROUND_ACTORS_LIVENESS_UNKNOWN` ของฉาก 2 แม้บรรทัดเดียว (wire ชั้น 2 ตก) หรือของหมดอายุเกิน 90/120 วิ หรือไม่มีของตกเลยตั้งแต่แรก = NO-RESULT ไม่ใช่ FAIL
ATTENDED: ไม่มีแฟล็ก `--*-scenario` ใด ๆ ใช้ DB สำเนา (`state\run_gt220.sqlite3`) เท่านั้น ห้ามเปิด canonical -- ต้องมี `-SecondPasswordMode bypass` + บัญชี GM ใน `config/gm_accounts.json`
ATTENDED: 🔴 ห้ามพิมพ์ตัวอักษรตลอดรอบยกเว้น `/warp 2` ในขั้นที่ 1 ขั้นเดียว (ไม่โฟกัส = ฮอตคีย์) · กล้องและ NO-CRASH ใช้คลิกขวาค้างลากเท่านั้น ห้าม Q/E · จดสีป้ายทุกป้ายทุกภาพจาก full-res (ไม่มี = `none`)

RECHECK (ทั้งสองข้อต้องผ่าน ไม่ผ่านข้อใดข้อหนึ่ง = ไม่บูต ตีกลับเป็น `BLOCKED` แล้วเขียนถึง chief)
`git -C pirate-force-server fetch` ก่อน · สองคำสั่งนี้ต้องพิมพ์บรรทัดที่ลงท้ายด้วย `:1`
1. `git -C pirate-force-server grep -c "mob_loot_cell=self.mob_loot_cell" origin/main -- src/pirateforce_foundation/runtime.py` ⇒ `...runtime.py:1` (จุดเรียกส่ง cell จริง)
2. `git -C pirate-force-server grep -c "def remote_actors_preserving_the_ground_under_publication" origin/main -- src/pirateforce_foundation/mob_combat.py` ⇒ `...mob_combat.py:1` (ตัวประกอบที่ถือล็อก)
🔴 ไม่เจอ = คำสั่ง **ไม่พิมพ์อะไรเลย และ exit 1** (ไม่ใช่พิมพ์ `0`) = สายขาด ใบนี้วัดอะไรไม่ได้
รันจบแต่ยังไม่มีลายเซ็นตาคน = **`AWAITING-OBSERVER`** · **G-OBS บังคับ**: จดหมายผลต้องมี `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` ไม่มี = chief ไม่ปิดใบ

- objective: (ข้ออ้างเดียว) **ฆ่ามอนให้ของตกพื้น แล้ว "คลิกอย่างอื่นก่อนเก็บ" (ชาวเมือง/NPC ที่ไม่ใช่ของที่ตก) ของบนพื้นต้องยังอยู่บนจอ**
  ไม่ทับ `GT-204` · 🔴 **ใบเดียวที่แยก "ไคลเอนต์เก็บ ground pool ไว้จริง" ออกจาก "ไคลเอนต์เมินสามไบต์ที่มันไม่พาร์ส" ได้** (สามไบต์ = **มาร์กเกอร์ ไม่ใช่รายการของ**: เดลตาเท่ากันสำหรับ 1 แถวกับ 255 แถว)
- db: `default_state\pirateforce.sqlite3` -- **สำเนาเท่านั้น ห้ามเปิด canonical** · `backup\pirateforce_before_GT-220_<yyyyMMdd_HHmmss>.sqlite3` แล้ว `state\run_gt220.sqlite3`
  · sha256 สำเนาก่อน/หลัง · sha256 canonical เทียบ `CANON_SHA.txt` ก่อน/หลัง ต้องเท่ากัน · `PRAGMA integrity_check` = `ok` สองครั้ง
- server args: บูตปกติบน `main` **ไม่มีแฟล็ก `--*-scenario` ใด ๆ**: `py -3 -u -m pirateforce_foundation.app --db state\run_gt220.sqlite3`
  · 🔴 ต้องมี `-SecondPasswordMode bypass` + บัญชี GM ใน `config/gm_accounts.json` (เหมือน `GT-214` — ประตูเดียวเข้าฉาก 2 คือ `/warp 2`)
  · 🔴 **เก็บคอนโซลรวม stdout+stderr (`2>&1`)**: `LANE_A_..._ANSWERED` ออก **stderr** · `GROUND_UNDER_PUBLICATION_*` ออก **stdout** ⇒ เก็บทางเดียวเห็นครึ่งเดียว (teardown template อ่านแต่ `.out.txt`)
- steps: (playbook: `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME`)
    0. LOCK_GAME · boot stamp · sha canonical · copy DB · รัน RECHECK ทั้งสองข้อ ไม่ผ่าน = ไม่บูต
    1. **server ก่อน client เสมอ** · เข้าเกม · **เส้นทางเดียวไปฉาก 2 คือ `/warp 2` เปล่า ไม่ใส่พิกัด** (เหมือน `GT-214`):
       คลิกช่องแชท **ยืนยัน focus จริง** → พิมพ์ `/warp 2` → Enter → รอ ~3 วิ · จด `T0` และ X/Y/Z ของตัวละครเมื่อถึงฉาก
    2. จัดกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น · `W/A/S/D` ใช้ได้เฉพาะขั้นที่สั่งให้เดิน
       🔴 **ห้ามพิมพ์ตัวอักษรตลอดรอบ ยกเว้น `/warp 2` ในขั้นที่ 1 ขั้นเดียว** (ตัวอักษรตอนช่องแชทไม่โฟกัส = ฮอตคีย์)
    3. ฆ่ามอนจนมีของบนพื้น **อย่างน้อย 3 ชิ้น** · **ห้ามเดินไปเก็บ** · ถ่าย **S0** ทันที · จด `t(S0)` + ระยะตัวละครถึงจุดของตก (G-FRAME)
       🔴 **ของบนพื้นมีอายุ 120 วินาที** (`mob_loot.DROP_LIFETIME_SECONDS`) ⇒ **ขั้น 3-5 ต้องจบใน 90 วินาที** · เกินแล้วของหาย = อายุหมดตามออกแบบ **ไม่ใช่ FAIL** ⇒ NO-RESULT (`GT-188`)
    4. **คลิกซ้ายที่ "ชาวเมือง/NPC ที่ไม่ใช่ของที่ตก" หนึ่งครั้ง** (ขั้นเดียวที่ใบนี้วัด) · จด `t(click)` · รอ 3 วิ · ถ่าย **S1** จากมุมกล้องเดิม
    5. ทำซ้ำขั้น 4 อีกสองครั้ง กับ NPC คนละตัวถ้ามี (รวมสามคลิก) · ถ่าย **S2** หลังคลิกสุดท้าย
    6. เดินเข้าไปติดของชิ้นหนึ่ง **แล้วคลิกซ้ายเก็บ** · จดจำนวนคลิก · เปิดกระเป๋าถ่าย **S3**
       🔴 ขั้นนี้ **ไม่ใช่ตัวตัดสินหลัก** เก็บไม่ขึ้นเพราะประตูอื่น (`vital_count_not_one`) = P3 ไม่ใช่ FAIL
    7. NO-CRASH ด้วย **คลิกขวาค้างลาก** · **S4** · ออกเกมด้วย X มุมขวาบน · ปิดเซิร์ฟเวอร์ (ฆ่าไคลเอนต์แล้ว **ต้อง restart เซิร์ฟเวอร์** ก่อนบูตหน้า)
    8. เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · **teardown เสมอ** · sha canonical ซ้ำ · ห้าม commit เอง
    9. คัดดิบ ห้ามตีความ:
       `findstr /N /C:"GROUND_UNDER_PUBLICATION_REACHED" /C:"GROUND_UNDER_PUBLICATION_CALL_SITE" /C:"GROUND_ACTORS_LIVENESS_UNKNOWN" /C:"GROUND_ROWS_SWEPT_BY_READ" /C:"GROUND_ROWS_RACE_WINDOW_OPEN" /C:"LANE_A_CHOOSE_NPC_SCENE2_ANSWERED" server_console_live.*.txt`

- pass criteria: (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด** -- G5)
    wire            : (1) `GROUND_UNDER_PUBLICATION_REACHED lane_hooks.choose_npc_response.scene_2` ปรากฏ (พิมพ์ครั้งเดียวต่อ site ⇒ หนึ่งบรรทัด = ครบ) ·
      (2) 🔴 **ไม่มีบรรทัด `GROUND_ACTORS_LIVENESS_UNKNOWN lane_hooks.choose_npc_response.scene_2` เลย ไม่ว่าเหตุผลท้ายบรรทัดจะเป็นอะไร**
        (`no_cell` · `another_scenes_cell` · `cell_has_no_scene` · `caller_scene_id_unaddressed` · `cell_refused` ...) — **มีแม้บรรทัดเดียว = เกตปฏิเสธ = ไม่เคยติดอาวุธเฟรม ⇒ ทั้งใบ NO-RESULT และ 🔴 ห้ามสรุป P2**
        (เหตุผล: `..._REACHED` พิมพ์ตอน **เข้า** ตัวประกอบ ก่อนเกตตัดสิน ⇒ ข้อ 1 ผ่านได้ทั้งที่ยังไม่มีอะไรถูกติดอาวุธ · วัดโดย pf-adversary รอบ `umlyof`) ·
      (2ก) `GROUND_ROWS_RACE_WINDOW_OPEN ...scene_2 <reason>` ถ้ามี = ทางเปิดหน้าต่าง race ⇒ **ไม่ FAIL แต่จดลง result ทุกบรรทัด** ·
      (3) `GROUND_ROWS_SWEPT_BY_READ` ที่ site นี้ = **ไม่มีบรรทัด** (ตัวพิมพ์คืนก่อนเมื่อจำนวน <= 0 ⇒ "บรรทัดที่บอกว่า 0" ไม่มีทางมี)
        มีบรรทัดพร้อมจำนวน > 0 **ภายใน 90 วินาทีแรก** = การอ่านกวาดแถวทิ้ง = FAIL ชั้น wire · เกิน 120 วินาที = อายุหมด ⇒ NO-RESULT (ดูขั้น 3) ·
      (4) `LANE_A_CHOOSE_NPC_SCENE2_ANSWERED` มีหนึ่งบรรทัดต่อคลิก (สามคลิก = สามบรรทัด) ·
      (5) `integrity_check` = `ok` · sha canonical ตรง `CANON_SHA.txt` ก่อน/หลัง · ไม่มี traceback ที่ไม่ถูกจับ
      🔴 **ชั้นนี้ตอบไม่ได้ว่าของบนพื้นรอด** เฟรมที่ยาวขึ้นแปลว่า "มีมาร์กเกอร์" เท่านั้น ห้ามเขียนว่า "เฟรมยาวขึ้น = แถวรอด"
      🔴 **ห้ามใช้โทเคน `composed_not_called` เป็นหลักฐานใด ๆ** — สแกนของมันมองไม่เห็นการเรียกแบบ name lookup ของสาย A (`..._CALL_SITE wired_by_name_lookup` คือค่าที่ถูกบน main วันนี้)
    client-observable: **ต้องมีคนอยู่หน้าจอเท่านั้น ห้ามอนุมานจากคอนโซล** --
      (1) **ของทุกชิ้นใน `S0` ยังเห็นใน `S1` และ `S2`** (นับทีละชิ้นจาก full-res มุมกล้องเดิม · หายแม้ชิ้นเดียว = FAIL ชั้นนี้ จดว่าหายกี่ชิ้นหลังคลิกที่เท่าไร) ·
      (2) เก็บของที่เหลือขึ้นได้จริงหลังคลิก NPC (ขั้น 6) เทียบ `S3` ·
      (3) NO-CRASH/CRASH · มีข้อความระบบขึ้นไหม (คัดเป๊ะ + สี) ·
      🔴 **จดสีป้ายชื่อทุกป้ายทุกภาพ** (หนึ่งบรรทัด/ป้าย/ภาพ · full-res · ไม่มีป้าย = `none` · **ห้ามเดาสาเหตุ** `RE-067`)
      ชั้นนี้ตอบไม่ได้: มีบรรทัดคอนโซลไหน กี่ไบต์ กวาดแถวหรือเปล่า

- คำทำนาย (**เป็นคำทำนาย** · ทำนายผิด = ผลการวัด ไม่ใช่ความล้มเหลว):
    P1 wire ผ่านทุกข้อ + ของยังอยู่ครบใน `S1`/`S2` ⇒ ผ่านสองชั้น = **`RE-130` ได้หลักฐานฝั่งไคลเอนต์ครั้งแรก**
    P2 wire ผ่านทุกข้อ **รวมข้อ 2** แต่ของหายจากจอ ⇒ **ผลลบที่มีค่าที่สุดของใบนี้**: มาร์กเกอร์สามไบต์ไม่พอ ไคลเอนต์ไม่ได้อ่านมันเป็น ground pool ⇒ redirect กลับสาย A/B ว่าต้องส่งรายการจริง
       🔴 สรุปข้อนี้ได้ **ก็ต่อเมื่อไม่มีบรรทัด `GROUND_ACTORS_LIVENESS_UNKNOWN` ของฉาก 2 เลย** มิฉะนั้นคือ NO-RESULT ตามข้อ 2
    P3 ของยังอยู่ แต่ขั้น 6 เก็บไม่ขึ้น (`vital_count_not_one`) ⇒ ชั้นหลักยัง PASS ได้ ให้จดเลขคลิกไว้ให้ `GT-216`
    P4 ไม่มีของตกเลย / ของหายก่อนคลิกครั้งแรก ⇒ **NO-RESULT (ประตู `GT-188`)** ไม่ใช่ FAIL
- nonclaims:
  1. ไม่พิสูจน์ว่าของรอดข้าม relog (`GT-142`) · ไม่พิสูจน์ว่าอยู่บนพื้นนานเท่าไร (`GT-188`) · ไม่วัดคลิกซ้ายเก็บของเป็นตัวหลัก (`GT-204`/`GT-216`)
  2. ไม่ตัดสินว่าสามไบต์นั้นคืออะไรในเชิงโปรโตคอล · ใบนี้ตัดสิน **สิ่งที่เห็นบนจอ** เท่านั้น
  3. ไม่ตัดสินสาเหตุของสีป้าย (`RE-067`) · ไม่ใช่เทสสองผู้เล่นแย่งของ / กระเป๋าเต็ม · ครอบเฉพาะฉาก 2
- result: (ผู้เทสกรอก · `OBSERVER_CONFIRMED` · `T0`/`t` ทุกภาพ + ระยะถึงจุดของตก (G-FRAME) · จำนวนชิ้นใน `S0`/`S1`/`S2` + ตารางสีป้าย · ผลเต็มไป round file และจดหมายผล)

- links: `CHIEF 20260903_0505` (ใบสั่ง ผู้ทำ = สาย A) · `LANE-B 20260903_0455` · `GT-204` · `GT-216` · `GT-188` · `RE-130` · `COO-DECISION 20260902_1946` · `server#625`

**ผู้เปิดใบ: LANE-A (WORLD) รอบ `umlyof` ตามใบสั่ง chief `20260903_0505` ข้อ ④ -- ผู้บริโภคผล: LANE-A (WORLD)**

## GT-230 NPC-SHOP-SELL-SLOT-FRAME-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS ตามเกณฑ์ใบ (เก็บ hex ลากไอเทมลงช่องขาย 2 ครั้งซ้ำได้ NPC 'Chalais') — R320 2026-09-06 §GT-230 · nonclaims: server ไม่ตอบ cmd=1 (ขาย)/cmd=12 (ปิดร้าน) เลย ไอเทมไม่เคยวางสำเร็จจริง · จาก notes_to_chief/20260906_0155_KA1A-R320-*.md · OPEN -- เจ้าของใบ LANE-UI · 🔴 **ใบนี้เป็นใบ "เก็บ hex" ไม่ใช่ใบตัดสินว่าขายสำเร็จ** · 🆕 เนื้อใบเต็มลงแล้วรอบ `ziuhft` — บูตได้จริง]

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `8nh6q5`/R334 2026-09-04T08:3x+07:00** ตามคำขอใน
> `notes_to_chief/20260904_0752_LANE-UI-RE-TICKET-npc-sell-grid-wire-command-never-captured.md`
> ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน `229` (ใบ `RE-229` ของรอบเดียวกัน) ⇒ ใบนี้ `230`
> · `GT-230`/`RE-230` = 0 hit ทั้งสามที่ก่อนวาง · **เจ้าของใบและผู้บริโภคผล = LANE-UI**
>
> 🔴 **ทำไมเป็น `GT-` ไม่ใช่ `RE-` ทั้งที่ `COO-DECISION 20260904_0644` ข้อ 2 เรียกว่า "ใบ RE ใบแรก"**
> เพราะ LANE-UI วัดมาแล้วว่า **grep/static ปิดคำถามนี้ไม่ได้** และตัวเขาเองขอมาเป็น "ใบ capture"
> รูปแบบเดียวกับใบเกาะของ LANE-A (`GT-228`) ⇒ chief ตั้งเป็นใบ attended capture ตามเนื้องานจริง
> ไม่ใช่ตามชื่อที่ใบสั่งใช้ · ถ้า COO เห็นว่าควรเป็น `RE-` บอกมาบรรทัดเดียว ผมย้ายให้และเก็บเลขเดิมไว้

- **คำถามที่ใบนี้ตอบ (บรรทัดแรก)**: ลากไอเทมเข้า **ช่อง sell** ของแผงร้าน NPC แล้ว **ไคลเอนต์ส่งไบต์อะไรออกสาย**
  (`TradeCmdVital 0x23B5` ด้วย cmd เลขใหม่ · หรือ opcode อื่นทั้งดุ้น · หรือไม่ส่งอะไรเลย)
- **ผ่าน** = ได้ hex ของเฟรมที่ออกตอนลากเข้าช่อง sell ครบหนึ่งเฟรม · **ไม่ต้องตัดสินว่า "ขายสำเร็จ"**
- **"ไบต์ว่าง" ก็เป็นผลที่ใช้ได้** และ **"หาไอเทมขายได้ไม่เจอ / เปิดร้านนั้นไม่ได้อีกแล้ว" ก็เป็นผลที่ใช้ได้**
  (แปลว่าใบต้องหาร้าน/ไอเทมทดแทนก่อน ไม่ใช่ใบล้ม)

- **สถานะที่วัดมาแล้ว (LANE-UI `0752` — ทำให้ใบนี้จำเป็น)**: คำตอบวันนี้คือ **undetermined** ไม่ใช่ "มี" และไม่ใช่ "ไม่มี"
  · ฝั่งจอ **มีช่อง sell จริง** (`reports/PF_RE_V111_to_V115_Inventory_Monster_Shop_20260814.md:55`)
  · ฝั่งสาย **ไม่เคยมีแคปเจอร์ไหนลากของเข้าช่องนั้นเลย** ⇒ ไม่มีเลขคำสั่งขายที่จับได้สักตัว
  (ทราฟฟิกร้านค้าที่เคยจับได้ทั้งหมดคือ `TradeCmdVital` cmd `6`/`8`/`12` = ฝั่งซื้อล้วน)
  · ฝั่ง static สืบ caller ของ `UpdateConditionalStoreItemVital` (`0xC84A`) **ไม่ถึง** — `CALL_UNCLASSIFIED: 0x0064F2D0`
  ไม่มี e8-call-site walk ของ vital นี้ในคลังเลย

- 🔴 **nonclaim บังคับ (ห้ามตัด — ~~ยกจาก `0752` ทั้งดุ้น~~ 🆕 แก้ LANE-UI รอบ `09q9jw2`: เป็นการสรุปความ+เรียงเลข
  ใหม่ ไม่ใช่คำต่อคำ · ดู `0752:72-85` เทียบต้นฉบับ)**
  ① ไม่อ้างว่า `UpdateConditionalStoreItemVital` คือคำตอบ หรือไม่ใช่คำตอบ — caller ยังไม่ถูกเดินสาย
  ② ไม่อ้างว่าช่อง sell ใน V111-115 **ทำงานได้จริง** — เห็นแค่บนจอ (คำเตือนเดียวกับที่ V116 ให้กับช่อง buy ของ V115
     ซึ่งถอนคำอ้าง "Buy grid insertion" ว่าเป็น drag-follow artifact ไม่ใช่ cart จริง)
  ③ ป้าย "ร้าน NPC" ของ vital ตัวนี้ใน `PF_USE_DROP_SELL001:157` เป็น **ป้าย registration/role ไม่ใช่ผลเดินสาย caller**
     ⇒ **ไม่ตอบว่าซื้อหรือขาย** (= ข้อ⑦ของจดหมาย `0752`)
  ④ `span_sha256` ของแถวใน `PF_SERIALIZER_FIELDS.tsv` **ยังไม่ verify กับอิมเมจ** (คลาวด์ไม่มี client image) (= ข้อ③ของจดหมาย)
  ⑤ **🆕 คืนเข้าลิสต์ (= ข้อ④ตัวจริงของจดหมาย ที่เคยหายไปจากที่นี่)**: ไม่ได้ไล่ทุกแถวของ `TEXTDATA_TH__MESSAGE.tsv`
     (908 บรรทัดจริง วัดด้วย `wc -l` — แก้จาก "~2,900" ที่ผิด) ทีละแถว — grep คำเดาไม่เจอ ไม่ใช่พิสูจน์ว่าไม่มี

- **เกณฑ์สองชั้น (ห้ามรวมข้ามชั้น)**
  ① **wire/DB**: hex ของเฟรมที่ออกตอนลากเข้าช่อง sell + เลข `[G< #N]` ของมัน · แถว DB ก่อน/หลังของกระเป๋าและเงิน
  ② **client-observable**: ภาพนิ่งของแผงร้านตอนไอเทมอยู่ในช่อง sell · ปิดใบด้วย `OBSERVER_CONFIRMED: <ISO+07:00>`

> 🆕 **เนื้อใบเต็มร่างโดยเจ้าของใบ (LANE-UI) รอบ `ziuhft` 2026-09-04T09:23+07:00 ตามจดหมาย chief `20260904_0835`**
> (chief สั่งไว้ตรง ๆ ว่า "คุณเติมได้เลย ไม่ต้องขออีก" — รูปแบบเดียวกับที่ LANE-A แก้ P1 ของ `GT-228` เอง)
> สถานะเปลี่ยนจาก `PENDING` → `OPEN` เพราะใบนี้บูตได้จริงแล้ว (ไม่ต้องรอโค้ด/RE ใดอีก)

- 🔴 **สองสิ่งที่ยังไม่รู้จริง (ห้ามอ้างว่ารู้แล้ว) — ใบนี้คือใบสำรวจของทั้งสองข้อ**:
  ① **ไม่มีใครในโปรเจกต์นี้เคยเปิดร้าน NPC สำเร็จบนเซิร์ฟเวอร์ของเราเอง (`pirateforce_foundation.app`)** — `TradeZoomVital`/`TradeCmdVital`/`CheckSecondPwdVital` ทุกตัวที่อ้างใน V111-V122 มาจาก**เซิร์ฟเวอร์จริงของค่าย** ไม่ใช่บิลด์นี้ ⇒ ขั้น 4-6 ข้างล่างคือการทดลองว่าร้านเปิดบนบิลด์นี้ได้เลยหรือไม่ ไม่ใช่ขั้นที่ยืนยันแล้ว
  ② **ไม่มีพิกัด/ชื่อ NPC ร้านค้าตัวไหนถูก pin ไว้ในคลังเลยสักตัว** — ใบนี้จึงเป็นใบ**ไล่คลิก** ไม่ใช่ใบที่บอกพิกัดตายตัว

- 🔴 PRECONDITION ที่ต้องเช็คจริงก่อนขั้น 1:
  P1. **ไอเทมที่ขายได้ไม่ต้องหา — ตัวละครใหม่มีอยู่แล้ว**: `SQLiteStore._insert_initial_backpack`
      (นิยามฟังก์ชันที่ `pirate-force-server/src/pirateforce_foundation/store.py:674` เรียกจริงที่ `store.py:575`
      ตอนสร้างตัวละคร) ใส่ของ 4 ชิ้นจากค่าคงที่ `INITIAL_BACKPACK` (นิยามอยู่คนละไฟล์ —
      `pirate-force-server/src/pirateforce_foundation/inventory.py:39-49`) ให้ทุกตัวละครใหม่เสมอ
      (`template_id 2600001` x2 ช่อง 0/2 · `2400901` ช่อง 1 · `2200002` ช่อง 3) ⇒ **สร้างตัวละครใหม่หนึ่งตัวสำหรับใบนี้ ไม่ใช้ตัวเก่าที่เคยเทสอย่างอื่นมาก่อน** จะได้กระเป๋าที่รู้ต้นทางแน่ชัด · ถ้ากระเป๋าตัวใหม่ว่างเปล่าผิดจากนี้ ⇒ **นี่คือ finding ของใบนี้เอง** เขียนไว้ตรง ๆ แล้วลองตัวละครใหม่อีกตัว
  P2. **การคลิก NPC หนึ่งครั้ง (ซ้าย) ปกติเปิด "หน้าต่างบทสนทนาเปล่า" ไม่ใช่ร้านค้า — [ทำนายจาก `GT-104` ยังไม่ใช่ผลวัดตรงกับ NPC ร้านค้า]**:
      `GT-104` **วัดพฤติกรรมนี้กับ hostile field-mob placement (P33/P58) เท่านั้น** ("คลิกซ้ายบน hostile placement
      ถูกตอบด้วยเลนคุย NPC (`V98_NPC_FACE_PLAYER_POSITION_HEADING_P<n>` + `V98_NPC_CONVERSATION_DEFAULT_P<n>`)")
      ไม่เคยมีการคลิก NPC ค้าขายจริงในใบนั้นเลย · ที่ยกมาใช้ทำนายพฤติกรรมกับ NPC ทั่วไปเพราะ `GT-104` เองบันทึกไว้ว่า
      "v141 ตอบทุก index ที่อยู่ในสำมะโน ไม่มีตัวแยก mob/NPC" (dispatch ไม่แยกชนิด placement) — เป็นเหตุผลที่สมเหตุสมผล
      แต่ **ยังไม่มีใครวัดการคลิก NPC ร้านค้าจริงสักครั้ง** ⇒ **ไม่ใช่ NPC ทุกตัวเป็นร้านค้า** ต้องไล่คลิกหลายตัวจนกว่าจะเจอตัวที่หน้าต่างเปิดเป็นแผงร้าน (มีช่อง buy/sell) แทนกล่องสนทนาเปล่า · เจอกล่องสนทนาเปล่า = ปกติ ไม่ใช่ผลลบ ให้ปิดแล้วคลิกตัวถัดไป · เจอพฤติกรรมอื่นนอกสองแบบนี้ (เช่น กล่องสนทนามีตัวเลือก) = finding แยก บันทึกไว้ตรง ๆ
  P3. **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** (กฎเดียวกับ `GT-228` P3) · ห้ามเปิดไคลเอนต์ทิ้งไว้โดยไม่มีเซิร์ฟเวอร์ (ตายเองใน ~3.5 นาที)
  P4. `-SecondPasswordMode bypass` (กฎเดียวกับ `GT-228`) กันไว้ล่วงหน้าเพื่อไม่ให้กล่องรหัสผ่านที่สองขวางถ้าร้านเรียกมัน — **ใบนี้ไม่ตัดสินพฤติกรรมรหัสผ่านที่สอง** ถ้าเห็นกล่องนั้นโผล่มาทั้งที่ตั้ง bypass ไว้ ให้บันทึกเป็น finding แยก ไม่ใช่ทำให้ใบนี้ล้ม

- db: canonical = `state\pirateforce.sqlite3` — 🔴 **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ คัดลอกเป็น
  `state\run_gt230_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · sha256 canonical ก่อน/หลังต้องตรง ·
  `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง · จด sha256 ของสำเนาก่อน/หลังด้วย

- server args: บูตมาตรฐาน · **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` · บัญชี GM ใน `config/gm_accounts.json`
  🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt230_<stamp>.sqlite3 2>&1
  ```
  ต้องมีตัวจับแพ็กเก็ตเปิดอยู่ตลอดใบ: `capture_v141\GAME_LIVE.txt` (hex ดิบ) และ `GAME_EVENTS_LIVE.txt`

- steps: (**จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา"** — ใช้ตัดหน้าต่าง hex ทีหลัง)
  1. PRECONDITION P1-P4 ผ่านก่อน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB เป็น run copy
  2. บูตเซิร์ฟเวอร์ใหม่สด · เปิดตัวจับแพ็กเก็ต
  3. บูตไคลเอนต์ · **สร้างตัวละครใหม่หนึ่งตัว** (ตามชื่อ/คลาสอะไรก็ได้) · ล็อกอิน · ภาพนิ่ง `S00-HOME`
  4. เปิดหน้าต่างกระเป๋า (Backpack) ยืนยันด้วยตา + ภาพนิ่ง `S00-BACKPACK-INITIAL` ว่ามี 4 ช่องตาม P1 จริง — **ถ้าไม่ตรง ให้บันทึกของจริงที่เห็นแทน ไม่เดา**
  5. เดินไปยังกลุ่ม NPC ที่ใกล้ที่สุดจากจุดเกิด · **คลิกซ้ายทีละตัว** จนกว่าจะเจอตัวที่เปิดแผงร้าน (มีช่อง buy/sell) · **จดเวลา** ทุกครั้งที่คลิก + ชื่อ/คำอธิบาย NPC ที่เห็นบนจอ + ผลลัพธ์ (กล่องสนทนาเปล่า / แผงร้าน / อื่น ๆ)
     🔴 **เพดานการไล่คลิก: ไม่เกิน 15 นาทีนาฬิกาจริงหรือ 20 ตัว แล้วแต่ถึงก่อน** — เกินแล้วยังไม่เจอ ⇒ ไปข้อ 9 (ผลลัพธ์ C)
  6. เจอแผงร้านแล้ว ภาพนิ่ง `S-SHOP-OPEN` เต็มความละเอียด · **จดเวลา** · ถ้าเจอกล่องรหัสผ่านที่สอง (`CheckSecondPwdVital`) ให้บันทึกไว้ (ดู P4) แล้วเดินต่อ
  7. ถ้าแผงร้านมีช่อง **sell** จริง (ไม่ใช่ buy อย่างเดียว): **ลากไอเทมหนึ่งชิ้นจากกระเป๋า (ช่องไหนก็ได้จาก P1) เข้าช่อง sell** · **จดเวลา** ทันทีก่อนปล่อยเมาส์ · ภาพนิ่ง `S-SELL-DRAG` ระหว่างลาก และ `S-SELL-DROPPED` หลังปล่อย
     🔴 **ห้ามกดยืนยันขายถ้ามีปุ่มยืนยันแยก** — ใบนี้หยุดที่ "ของอยู่ในช่อง sell" เท่านั้น ถ้ามีปุ่ม "ขาย/OK" ให้ถ่ายภาพปุ่มไว้เฉย ๆ **ไม่กด** (กันไม่ให้ไอเทมเริ่มต้นหายไปจากตัวละครทดสอบชุดต่อไปโดยไม่จำเป็น)
  8. ปิดแผงร้าน (ปุ่ม X หรือคลิกออกนอกแผง) · ภาพนิ่ง `S-SHOP-CLOSE` · เช็ก NO-CRASH ด้วยคลิกขวาลากหมุนกล้องเท่านั้น
  9. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ**
  🔴 **STOP:** เจอปุ่มยืนยันการขายแล้วเผลอกด ⇒ หยุดทั้งใบ บันทึกทันทีว่ากดไปแล้ว (ไม่ปิดบัง) แล้วเดินขั้น 8-9 ต่อให้จบเพื่อเก็บ teardown ให้ครบ

- ทำอย่างไรกับผลแต่ละแบบ:
  A. **เจอแผงร้านที่มีช่อง sell + ลากของเข้าสำเร็จ** ⇒ **PASS** · เกณฑ์ทั้งสองชั้นข้างบน (①②) ตัดสิน · นี่คือผลที่ใบนี้ต้องการที่สุด
  B. **เจอแผงร้าน แต่มีแค่ buy ไม่มีช่อง sell** ⇒ **PASS พร้อมคำตัดสิน `BUY-ONLY-SHOP`** (ไม่ใช่ FAIL) · บันทึกชื่อ/คำอธิบาย NPC ไว้ แล้วถ้ายังมีเวลาในเพดาน 15 นาที ให้ลองตัวถัดไป
  C. **ไล่คลิกจนครบเพดานแล้วไม่เจอแผงร้านเลยสักตัว (เจอแต่กล่องสนทนาเปล่า)** ⇒ **PASS พร้อมคำตัดสิน `NO-SHOP-FOUND`** (มีค่าเท่าผลบวก เหมือน `NO-FRAME` ของ `GT-228`) · redirect: แปลว่า NPC ร้านค้าอยู่นอกระยะเดินจากจุดเกิด หรือบิลด์นี้ยังไม่มี NPC ที่ประกาศเป็นร้านค้าเลย ⇒ ใบถัดไปต้องขยายรัศมีค้นหาหรือขอพิกัดจากฝั่ง static RE
  D. **เจอแผงร้านที่มีช่อง sell แต่ลากไม่ติด/ไอเทมเด้งกลับ** ⇒ **PASS พร้อมคำตัดสิน `SELL-SLOT-REJECTED`** · จดข้อความปฏิเสธถ้ามีตามตัวอักษร + hex ของหน้าต่างเวลาที่ลาก (ถ้าไม่มีเฟรมออกเลย = สอดคล้องกับ nonclaim ④ เดิม ไม่ใช่ผลแปลก)
  E. **ไคลเอนต์ตาย/ตัวจับแพ็กเก็ตไม่เขียนไฟล์** ⇒ **NO-RESULT** พร้อมเหตุผลหนึ่งบรรทัด

- nonclaims — 🆕 **แก้โดย LANE-UI รอบ `09q9jw`**: ตัด ①-④ เดิมตรงนี้ออก (เคยเขียนว่า "ยกจาก `0752` ทั้งดุ้น" แต่
  จริง ๆ เป็นแค่ paraphrase ซ้ำของ ①-④ ที่หัวใบด้านบนอยู่แล้วด้วยถ้อยคำต่างกัน — อ่านที่หัวใบที่เดียวพอ รวมส่วนแก้
  เลขต่อท้าย) เหลือเฉพาะ nonclaim ที่เป็นของใบ `GT-230` เองจริง (ไม่มีในจดหมาย `0752`):
  ① **ใหม่**: ไม่อ้างว่า NPC ตัวใดตัวหนึ่งเป็น "ร้านค้าตัวจริง" ของโปรเจกต์ก่อนใบนี้รัน — ยังไม่มีพิกัดที่ pin ไว้ในคลัง (ดูข้อ ② ของ "สองสิ่งที่ยังไม่รู้จริง" ด้านบน)
  ② **ใหม่**: ไม่ตัดสินว่าเซิร์ฟเวอร์เราเอง (`pirateforce_foundation.app`) จำลองพฤติกรรมร้านของเซิร์ฟเวอร์ค่ายได้ถูกต้อง — ใบนี้แค่จับสิ่งที่บิลด์นี้ทำจริงตอนนี้
  ③ **ใหม่**: P2 ที่ทำนายว่าคลิก NPC เดียวเปิดกล่องสนทนาเปล่า **มาจาก `GT-104` ที่วัดกับ hostile field-mob เท่านั้น
     ไม่ใช่ผลวัดตรงกับ NPC ค้าขาย** (ดูส่วนแก้ของ P2 ด้านบน) — ยังไม่มีใครคลิก NPC ร้านค้าจริงมาก่อนใบนี้เลย

- links: `notes_to_chief/20260904_0752_LANE-UI-RE-TICKET-npc-sell-grid-wire-command-never-captured.md` ·
  `notes_to_chief/20260904_0835_CHIEF-TO-LANE-UI-npc-sell-capture-is-gt-230-not-an-re-ticket.md` ·
  `pirate-force-server/src/pirateforce_foundation/inventory.py:39-49` (`INITIAL_BACKPACK`) ·
  `pirate-force-server/src/pirateforce_foundation/trade_session_membership.py` (RE-157 job 1, ทำไมเฟรม `TradeCmdVital` ไปถึง `current/pf_login_game_server_v141.py` ได้อยู่แล้ววันนี้) ·
  `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md:190-206` (ลำดับ V111-V122 shop ฝั่งค่าย) · `GT-228` (ใบต้นแบบของรูปแบบ)
- result: (ผู้เทสกรอก: PASS `A`/`BUY-ONLY-SHOP`/`NO-SHOP-FOUND`/`SELL-SLOT-REJECTED` · branch+commit ที่บูต ·
  ชื่อ/คำอธิบาย NPC ทุกตัวที่คลิกพร้อมเวลาและผลลัพธ์ · hex ดิบของหน้าต่าง +/-5 วิ รอบจังหวะเปิดร้าน + จังหวะลากเข้า sell (ถ้ามี) ·
  ภาพ `S00-HOME`/`S00-BACKPACK-INITIAL`/`S-SHOP-OPEN`/`S-SELL-DRAG`/`S-SELL-DROPPED`/`S-SHOP-CLOSE` · sha256 ทั้งสี่ค่า ·
  `integrity_check` สองครั้ง · NO-CRASH/CRASH · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

- **ลำดับ**: ต่อท้าย "รอเครื่องคุณ" ของ `NOW.md` · **ไม่แซง** `GT-223` / `GT-219` / P-2 / `GT-228`
- **ผู้เปิดใบ: LANE-UI — LANE-UI บริโภคผลใบนี้เอง และปิดหัวใบเอง**

---

## 🔴 GT-231 SPEED-ONE-LOGIN-SHAPED-FRAME-DOES-NOT-ZERO-THE-REST-001  [BLOCKED -- RECHECK เป็นตัวปลดป้าย · ใบเปิด ยังไม่เคยรัน ห้ามลบ ห้ามย้าย · เจ้าของใบ/ผู้บริโภคผล = LANE-GM]

> **คำถามที่ใบนี้ตอบ (คำถามที่ยังค้างของ `RE-222`)**: "บิตที่ไม่ตั้ง = ศูนย์" เป็นสมบัติของ **เฟรม `0x309A`**
> หรือของ **การสร้าง actor**? — เฟรม `0x309A` หนึ่งใบที่ถือ mask **เท่ากับ mask ที่ล็อกอินของคอนเนกชันนั้นส่ง**
> ทำให้ค่าที่ไม่ได้อยู่ในเฟรมกลายเป็นศูนย์บนจอหรือไม่
> **ผ่าน** = เป็นสมบัติของ **การสร้าง actor** ไม่ใช่ของเฟรม ⇒ (b'') เดินต่อ ·
> **ไม่ผ่าน** = (b'') ถอยไปทางเลือก (ข) แล้ว **เปิดใบ RE ตอนนั้น** (`COO-DECISION 20260904_0545` ข้อ 3)
> 🔴 ใบนี้ **ไม่ supersede `GT-183`** และ **ไม่เปิด `GT-218` ใหม่** (`GT-218` FAIL ไปแล้ว คงไว้เป็นประวัติ ห้ามลบ) —
> มันถามคนละคำถาม · ใบนี้ **ไม่ปิดใบอื่นใดทั้งสิ้น** · ใบนี้เป็น **การทดลอง** ไม่ใช่การยืนยันฟีเจอร์
>
> 🔢 เลขใบตั้งโดย chief (LANE-E) รอบ `8nh6q5`/R334 · **ถ้อยคำเนื้อใบเป็นของ LANE-GM chief ไม่แก้สาระ**
> 🔴 **`GT-183` chief ไม่ปิดเอง** (เปิดตาม `PANYA-ORDER 20260901_0215` §3 = นอกอำนาจ chief) ⇒ ส่งขึ้น COO เคาะ
> ดูบล็อกในหัว `GT-183` · ระหว่างนี้ `GT-183` **ยัง BLOCKED ไม่มีใครลบ ไม่มีใครย้าย**

- objective: (ข้ออ้างเดียว) เฟรม `0x309A` **หนึ่งใบ** ที่ mask เท่ากับ mask ล็อกอินของเซสชันนั้น
  **ไม่ทำให้** ค่าที่ไม่ได้อยู่ในเฟรมกลายเป็นศูนย์บนจอ
- RECHECK: (รันก่อนเชื่อหัวใบเสมอ · **ไม่ผ่าน = ยัง BLOCKED ห้ามบูต**)
  ```
  (cd pirate-force-server && git show origin/main:src/pirateforce_foundation/lane_hooks/__init__.py | findstr /C:"current_login_attr_bytes")
  ```
  เจอ = จุดอ่านที่สองลง `main` แล้ว ⇒ ใบนี้เกรดได้ (ปลดเป็น PENDING) · ไม่เจอ = ยัง BLOCKED
  (วันนี้กำแพงที่ `gm/attr_wire.make_update_attr_frame` ยังปฏิเสธพร้อมบรรทัดคอนโซล ไม่มีไบต์ออก **ตามที่ควรเป็น**)
- db: canonical = `state\pirateforce.sqlite3` — **สำเนาเท่านั้น ห้ามเปิด canonical** · คัดลอกเป็น
  `state\run_gt231_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา · sha256 canonical ก่อน/หลังต้องตรง ·
  `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง · สำรองแถวตัวละครก่อนบูต ·
  (คัดลอก DB ⇒ ตัวละครกลับจุด spawn ทุกบูต **ปกติ ไม่ใช่ผลวัด**)
- server args: บูตมาตรฐาน · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** · เก็บคอนโซลรวม stdout+stderr ไฟล์เดียว (`2>&1`)
  · เปิดประตูด้วย `PF_SPEED_TRIAL=400` **ในเซสชันผู้เทสเท่านั้น**
  ```
  set PF_SPEED_TRIAL=400
  py -3 -u -m pirateforce_foundation.app --db state\run_gt231_<stamp>.sqlite3
  ```
- steps: (~10 นาทีหน้าจอ · ต้องมีคนนั่งหน้าจอทั้งใบ)
  1. RECHECK ผ่าน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB
  2. **BEFORE** (เซิร์ฟเวอร์ยังไม่เปิด · `mode=ro` ห้ามตัดออก · ห้ามชี้ canonical): คัดแถวตัวละครทั้งแถว
     (เงิน · HP · HP สูงสุด · MP · ช่องความเร็ว) เป็นบล็อกดิบ
  3. บูต **เซิร์ฟเวอร์ใหม่สดก่อน** แล้วค่อยบูตไคลเอนต์ (เคยฆ่าไคลเอนต์ = เซิร์ฟเวอร์ยังถือเซสชัน ตัวถัดไปค้าง
     "connecting" ตลอดกาล ⇒ รีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ) · ห้ามเปิดไคลเอนต์ทิ้งโดยไม่มีเซิร์ฟเวอร์ (ตายเองใน ~3.5 นาที)
  4. ล็อกอินเข้าฉาก **ยืนนิ่ง** · `S0` เต็มความละเอียด เห็น HUD ครบ (เงิน · แถบ HP · HP สูงสุด · MP)
     🔴 **ห้ามเปลี่ยน facing ของตัวละคร** — ห้าม `W/A/S/D` ห้าม `Q`/`E` (สองอย่างนี้ยิง `TargetPosVital` ออกสาย)
     · หมุนกล้องด้วยคลิกขวาค้างลากได้ตลอดใบ (ไม่เปลี่ยน facing · ไม่มีไบต์ออก)
  5. **คลิกช่องแชทให้ขึ้น cursor ก่อน** แล้วพิมพ์คำสั่ง `/speed` ด้วยค่า **400 เท่านั้น** **หนึ่งครั้ง** ·
     จดสตริงที่พิมพ์ **คำต่อคำ + นับจำนวนอักขระ** · 🔴 นอกช่องแชท ทุกตัวอักษรกลายเป็นฮอตคีย์ ·
     🔴 predicate ของ trigger คือ **12 อักขระ printable ASCII พอดี** — สตริงที่สั้นกว่าถึงเซิร์ฟเวอร์แล้ว
     **เงียบ ๆ ไม่เข้าเงื่อนไข** ⇒ "ไม่มีอะไรเกิดขึ้น" ไม่ใช่หลักฐานว่ากำแพงปฏิเสธ
  6. `S1` ทันที มุมกล้องเดิม เห็น HUD ชุดเดียวกับ `S0`
  7. 🔴 **STOP-on-HP-0**: HP แตะ 0 เมื่อไร **หยุดทันที** เก็บภาพ+คอนโซล บันทึกเป็นผล **ไม่ต้องลองซ้ำ**
  8. ตัวเช็ค NO-CRASH: **คลิกขวาค้างลากหมุนกล้องเท่านั้น** · ออกเกมด้วยปุ่ม X
  9. ปิดเซิร์ฟเวอร์ให้สนิท · รันคำสั่งข้อ 2 ซ้ำคำต่อคำเป็นบล็อก `AFTER` · เก็บคอนโซลรวม + วิดีโอ/ภาพก่อน-หลัง +
     sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ** แม้รอบจบเพราะเลิกเล่นเฉย ๆ
     (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที)
- pass criteria: (สองชั้น · 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB (อ่านจากคอนโซล + สำเนา DB · ไม่ต้องมีตาคน):
      (1) คอนโซลของบูตนั้นพิมพ์เฟรม `0x309A` ออก **หนึ่งใบเท่านั้น** (มากกว่าหนึ่ง = ชั้นนี้ไม่ผ่าน)
      (2) `basic_mask`/`actor_mask` ของเฟรมนั้น **เท่ากับ** mask ที่ล็อกอินของเซสชันนั้นประกอบ — วันนี้คือ
          `0x074F` / `0x0000000000000801` ในฉากที่ `world_faction_admission` admit ·
          `0x034F` / `0x0000000000000801` ในฉากที่ไม่ admit · mask อื่น = ชั้นนี้ไม่ผ่าน
      (3) ไม่มี `x=30` ในเฟรมเลย
      (4) `AFTER`: แถวตัวละคร **ไม่เปลี่ยนนอกจากช่องความเร็ว**
      (5) `integrity_check` = `ok` · sha canonical ตรง · ไม่มี traceback หลุด
      **ชั้นนี้ตอบไม่ได้เลยว่า:** ไคลเอนต์วาดอะไรบนจอ
    client-observable (**ต้องมีตาคน ห้ามอนุมานจากคอนโซล/DB**):
      (6) หลังส่งหนึ่งเฟรม **เงิน · HP สูงสุด · MP · และแถบ HP ไม่เปลี่ยน** ระหว่าง `S0` กับ `S1`
          — **ทั้งสี่ต้องครบ ขาดข้อเดียว = ไม่ผ่าน**
      (7) ตัวละครยังยืนอยู่ ไม่มีไดอะล็อกตาย ไม่หลุดการเชื่อมต่อ
      (8) 🔴 บันทึก **สีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** ครบทุกภาพ · เขียน `none`
          แทนการเว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียดเท่านั้น** ห้าม contact sheet/ภาพย่อ/วิดีโอ ·
          **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น) · ต่างจากภาพเซิร์ฟเวอร์จริง ⇒
          `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      **ชั้นนี้ตอบไม่ได้เลยว่า:** mask อะไรออกไปบนสาย
- prediction: (**คำทำนาย ไม่ใช่ผลวัด** · ทำนายผิด = finding ไม่ใช่ความล้มเหลว)
    P1 เฟรมใบเดียว mask ตรง + สี่ค่าบนจอไม่เปลี่ยน + ตัวละครยังยืน ⇒ **PASS** = สมบัติของการสร้าง actor ⇒ (b'') เดินต่อ
    P2 ค่าใดค่าหนึ่งในสี่กลายเป็นศูนย์/เปลี่ยน ⇒ **FAIL** = สมบัติของเฟรม ⇒ (b'') ถอยไป (ข) + LANE-GM เปิดใบ RE ตอนนั้น
    P3 กำแพงปฏิเสธ มีบรรทัดคอนโซล ไม่มีไบต์ออก ⇒ **NOT MEASURED ไม่ใช่ FAIL** · รันใหม่เมื่อจุดอ่านครบ
    P4 HP ถึง 0 ⇒ หยุดตามข้อ 7 · เป็น **ผลวัด** ที่ต้องส่งพร้อมคอนโซลคำต่อคำ
    🔴 **ผลลบมีค่าเท่าผลบวก** — P2 เปลี่ยนทิศ (b'') ทั้งเส้น · P3 ชี้ว่าตัวบล็อกยังเป็นแหล่งค่า ไม่ใช่คำถามนี้
- กติกาความปลอดภัย (ยกมาจากใบเดิม ไม่ใช่ของใหม่ · ทุกข้อบังคับ):
    - ค่าเดียว: ค่าที่ล็อกอินส่งอยู่แล้ว (`400`) **ห้ามค่าอื่น ห้าม `800` ห้าม `1e40`**
    - **STOP-on-HP-0**: HP แตะ 0 หยุดทันที บันทึกเป็นผล ไม่ต้องลองซ้ำ
    - **ล็อก `/speed` ทุกตัวคงปิด** ยกเว้นเฟรมทดลองของใบนี้ใบเดียว · `PF_SPEED_TRIAL` เปิดได้เฉพาะเฟรมที่
      **ผ่านนิยาม (b'') ใหม่** (mask เฟรม = mask ล็อกอิน · `COO-DECISION 20260904_0545` ข้อ 2)
    - 🔴 **`x=30` ห้ามออกจากเซิร์ฟเวอร์ตลอดกาล** — เฟรมมี `x=30` = หยุด ไม่ส่ง
    - `/warp <n> <x> <y>` (มีพิกัด) **ปิดอยู่ ห้ามพิมพ์ในใบนี้**
    - ต้องมีวิดีโอ/ภาพก่อน-หลัง · backup แถว DB ก่อนบูต · ห้ามเปิด canonical DB
- nonclaims: (อ่านก่อนอ้างผลใบนี้)
  1. ไม่พิสูจน์ว่า `/speed` "ทำงาน" · ไม่พิสูจน์ว่าตัวละครเดินเร็วขึ้น — **ห้ามเดินเพื่อทดสอบความเร็ว**
     (เดิน = เปลี่ยน facing = ยิงเฟรมออกสาย และไม่ใช่คำถามของใบนี้)
  2. ไม่พิสูจน์อะไรกับชุด mask อื่นนอกจาก mask ล็อกอินของคอนเนกชันนั้น · ไม่พิสูจน์ครบ 55/27 แถว
  3. ไม่อธิบาย `GT-218` และไม่กลับคำ `GT-218` · ไม่ปิด `GT-183`
  4. ไม่พิสูจน์อะไรบน canonical — บูตบน **สำเนา**
  5. ไม่ตัดสินสาเหตุของสีป้ายชื่อใด ๆ (`RE-067`) · จดสีอย่างเดียว
  6. ไม่ใช่ใบตีมอน — ห้ามตี ห้ามคลิกมอนสเตอร์ ห้ามเข้าใกล้จนโดนตี (`NOW.md` P-1/P-2 ยังไม่ปิด)
- links: `gm/attr_wire.py` (`make_update_attr_frame` = กำแพงที่ทางออกเฟรม) ·
  `lane_hooks.current_named_attr_values` / `current_login_attr_bytes` (แหล่งค่าสองแหล่ง) ·
  `RE-222` (คำถามที่ใบนี้ตอบ) · `GT-183` · `GT-218` (ประวัติ FAIL ห้ามลบ) · `COO-DECISION 20260904_0545` ·
  `notes_to_chief/20260904_0735_LANE-GM-TO-CHIEF-*` · `BRIDGE_BOOT_PROCEDURE.md` +
  `ATTENDED_SESSION_RUNBOOK.md` + `TEMPLATE_teardown_generic.ps1`
- numbering: ตัวนับร่วมสองคิว + archive คืน `230` (หลัง `RE-229`/`GT-230` รอบเดียวกัน) ⇒ `231` · 0 hit ก่อนวาง
- result: (ผู้รันกรอกแยกสองชั้น · ชั้นไหนไม่ได้วัดเขียน `NOT MEASURED` · บรรทัดคอนโซลของเฟรมและของกำแพง
  ดิบ ๆ ทุกบรรทัด · สตริงที่พิมพ์ในแชทคำต่อคำ + จำนวนอักขระ · บล็อก `BEFORE`/`AFTER` · ภาพ `S0`/`S1` เต็ม
  ความละเอียด · บรรทัดสีป้ายครบทุกป้ายทุกภาพ · sha256 · branch/commit ที่บูต · timestamp +07:00)

**ผู้เปิดใบ: chief (LANE-E) รอบ `8nh6q5` (R334) ตาม `COO-DECISION 20260904_0545` ข้อ 3 -- ผู้บริโภคผล: LANE-GM**

---

## GT-245 CHARACTER-SELECT-SCREEN-SHOWS-THE-REAL-SCENE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ครึ่งหลัง PASS — R317 2026-09-05 §1: หลัง /warp 1 (persist R316) → relaunch → หน้าเลือกตัวพิมพ์ 'Port Royal' ตรงเกณฑ์แยกแยะที่ COO/pf-adversary กำหนดไว้ (ครึ่งแรกเห็น 'Prison Exile Island' มาก่อนใน R315 แล้ว) ⇒ **ใบนี้ PASS เต็มสองครึ่งแล้ว** (PANYA-DECISION 20260903_1857 ปิดได้) · จาก notes_to_chief/20260905_1125_KA1A-R317-*.md · 🟡 **PARTIAL -- ครึ่งแรก PASS R315 · ครึ่งหลังยังไม่รัน** (🔴 ป้ายต้องเป็น PARTIAL ไม่ใช่ PASS: `tools_bridge/pf_queue_status.py` อ่านคำแรกในวงเล็บเป็นสถานะ และ PASS จะทำให้รอบ attended ข้ามครึ่งหลังทั้งที่ยังไม่รัน [วัดแล้ว chief `pv4zg1` 11:10]) -- แก้หัวโดย chief (LANE-E) รอบ `pv4zg1`/R352 2026-09-05T11:0x+07:00 ตามผล `notes_to_chief/20260905_1031_KA1A-R315-RESULTS-*.md` §4 · **ครึ่งแรกผ่านแล้ว**: `/warp 2` → relaunch → หน้าเลือกตัวพิมพ์ "Prison Exile Island" (`OBSERVER_CONFIRMED 2026-09-05T10:24+07:00`) · **เหลือครึ่งหลัง**: `/warp 1` → relaunch → ต้องขึ้น "Port Royal" ⇒ นัดบูตถัดไป (R317) · 🔴🔴 **แก้หลัง pf-adversary (D3) ในรอบเดียวกัน — ฉบับก่อนหน้าเขียนว่า "รันเฉพาะครึ่งหลัง ไม่ต้องรันครึ่งแรกซ้ำ" ซึ่งทำให้ครึ่งหลังผ่านได้ด้วยบิลด์ที่ย้อนทั้งหมด**: อาการของบั๊กเดิมคือหน้าเลือกตัวละครพิมพ์ "Port Royal" **เสมอ** (`PANYA-DECISION 20260904_1857` · R310) ⇒ "จอขึ้น Port Royal" คือผลของบิลด์ก่อนแก้ด้วย · ครึ่งหลังแยกแยะได้ต่อเมื่อ **ตัวละครถูก persist ไว้ที่ฉาก 2 ก่อนเริ่ม** และ DB ของ R315 (`state\run_gt247_20260905_101145.sqlite3`) **ถูกทิ้งไปแล้ว** ⇒ **บังคับหนึ่งในสองอย่างในบูตเดียวกันก่อนเกรดครึ่งหลัง**: (ก) เห็น "Prison Exile Island" บนหน้าเลือกตัวละครหนึ่งครั้งก่อน (`/warp 2` → relaunch) แล้วจึง `/warp 1` → relaunch → "Port Royal" · หรือ (ข) อ่าน `character_positions.scene_id` ของตัวละครทดสอบจากสำเนา DB ก่อนเริ่ม แล้วบันทึกค่าลงผล (ต้องไม่ใช่ 1 ไม่งั้นครึ่งหลังไม่มีอำนาจแยกแยะ) · **ครึ่งแรกคือตัวคุมของครึ่งหลัง ไม่ใช่งานซ้ำ** · **เจ้าของใบ/ผู้บริโภคผล = LANE-DB** · เดิม: 🟢 READY -- บูตได้ทันที (chief R346 `kj0s6r` 2026-09-05T02:0x+07:00) · **เนื้อใบเป็นของ LANE-DB** (`COO-DECISION 20260904_1947` ข้อ 5 สั่งให้ DB เขียน body ในรอบเดียวกับ PR) · เลขใบตั้งโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 3 · ผู้รัน = Panya (attended) · เจ้าของใบ/ผู้บริโภคผล = **LANE-DB**]

> 🟢 **ตัวบล็อกปลดแล้ว -- วัดจาก `main` ของ pirate-force-server ในรอบที่เขียน (R346, 2026-09-05 ~01:5x +07:00)**:
> `pirate-force-server#778` merged เป็น `2a71c0a5` (commit งาน `66f9802d` "LANE-DB round fqc0na: RE-248 answered -- flip SCENE_FIELD to FIELD_A") ·
> ยืนยันด้วยการอ่านซอร์สบน main: `src/pirateforce_foundation/persistence_scene_field_patch.py:76` = `SCENE_FIELD: str | None = FIELD_A` (บรรทัด 67 `FIELD_A = "A"`) ·
> ที่ปลดล็อกได้เพราะ `RE-248` (จดหมาย `20260905_0053`) ตอบว่า tag `0x12` ตัวแรก `+0x20` = scene id · ตัวที่สอง `+0x22` = level
>
> 🔢 **หัวใบยังไม่มีเนื้อใบเต็มโดยตั้งใจ** -- chief ตั้งเลขและปลดสถานะให้เท่านั้น · เกณฑ์ผ่านสองบรรทัดข้างล่างมาจาก `COO-DECISION 20260904_1947` ข้อ 5 และ **เพียงพอต่อการบูต** · การขยายเป็นเกณฑ์สองชั้นเต็มยังเป็นของ **LANE-DB** เท่านั้น (เขตเขียนใบ = เจ้าของใบ) · ผู้เทสรันจากเกณฑ์ที่มีอยู่ได้เลย ไม่ต้องรอ LANE-DB เขียนเพิ่ม

- **ที่มา**: `PANYA-DECISION 20260904_1857` (หน้าเลือกตัวละครพิมพ์ "Port Royal" ใต้ชื่อเสมอ ทั้งที่ DB = ฉาก 2 และเข้าเกมแล้วอยู่เกาะคุก) · หลักฐานภาพ `20260904_185512.png` ใน `notes_to_chief/20260904_1911_KA1A-R310-RESULTS-*` ข้อ 5 · ต้นเหตุที่ COO วัดจาก main `90d5aaa`: `character_list()` ต่อ `c.actor_wire` ที่แช่แข็งตอนสร้างตัวละคร (ฝัง `scene_id`=1) ทั้งที่ `list_characters` JOIN `character_positions` มาแล้ว (`COO-DECISION 20260904_1947` ข้อ 2)
- **เกณฑ์ผ่าน (จาก `1947` ข้อ 5 -- LANE-DB ขยายเป็นสองชั้นเต็มในเนื้อใบ)**: `/warp 2` → ปิดเกม → relaunch → **หน้าเลือกตัวพิมพ์ Prison Exile ไม่ใช่ Port Royal** แล้ว `/warp 1` → relaunch → กลับเป็น Port Royal
- **ข้อห้ามที่ติดมากับใบ** (`1947` ข้อ 4): ห้าม migration/backfill คอลัมน์ `characters.actor_wire` · แก้ที่จุดฉายเท่านั้น · ห้ามแตะ `runtime.py` (ถ้าจำเป็น = CORE-REQUEST ถึง chief พร้อม diff)

**ผู้เปิดใบ: chief (LANE-E) -- เนื้อใบและผู้บริโภคผล: LANE-DB**

---

## GT-250 NAME-LABEL-PERSISTS-AFTER-WALK-AWAY-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — NEGATIVE-AGAIN (ป้ายชื่อไม่หายซ้ำ R321 2026-09-06 11:29 · ผลแรก NEGATIVE ที่ R317 2026-09-05) · RESULT: GT-250 NEGATIVE-AGAIN R321 2026-09-06 11:29 (first R317) · จาก notes_to_chief/20260905_1125_KA1A-R317-*.md + notes_to_chief/20260906_1255_KA1A-R321-*.md · 🟢 **READY** -- บูตได้ทันที ไม่มีธง ไม่รอโค้ด · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** (ป้ายชื่อ / population reconcile) · ผู้เปิดใบ = chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2143` ข้อ 3 และคำตัดสิน COO ใน `NOW.md` 2026-09-05 01:45 (กวาด RE→GT ของ ka1-A) · ผู้รัน = Panya (attended) ~5 นาที · **ลำดับที่ COO เคาะ: ใบนี้เป็นข้อ 1 ใน 4 ใบ** (GT-250 > GT-251 > GT-252 > GT-253) · **ต่อท้ายคิว `รอเครื่องคุณ` ปัจจุบัน ไม่ใช่หัวคิว** (GT-247 / GT-249 / GT-245 อยู่ก่อน · ลำดับในคิวนั้นเป็นสิทธิ์ COO) · ไม่บล็อกสายใด · **ไม่มีการตีมอนในใบนี้** จึงไม่ชนกฎ "ห้ามใบเทสตีมอนจนกว่า P-2 จะปิด"]

ATTENDED: บูตเซิร์ฟไม่มีแฟล็กใด ๆ (ไม่ใส่ `--population-scenario`) ตามหัวใบ บูตได้ทันที -> ล็อกอินตัวละครที่ Port Royal -> ยืนนิ่งที่จุดเกิดถ่าย `S0-SPAWN` จดพิกัด HUD + ทุกป้ายในเฟรม -> NO-CRASH check ด้วยคลิกขวาลากกล้องเท่านั้น (ห้าม `Q`/`E`) -> เดินออกด้วย `W/A/S/D` จนไม่มี NPC จาก `S0` เหลือในเฟรม +5 วิ ถ่าย `S1-FAR` -> เดินกลับพิกัดเดิม นิ่ง 3 วิ ถ่าย `S1-BACK` -> ทำซ้ำอีก 2 รอบ (`S2`/`S3`) · 🔴 ห้ามคลิกอะไรตลอดใบ (คลิก = ประกอบสำมะโนใหม่ ปนเปื้อนผล)
ATTENDED: ดูคอนโซลว่ามีเฟรม `NPCAttr`/`BasicAttr` ออกจากเซิร์ฟเวอร์ระหว่างเดินหรือไม่ (นับจำนวนให้ตรง) และดูบนจอว่าป้ายชื่อ (เขียว) แต่ละตัวใน `S0-SPAWN` ยังอยู่ใน `S1-BACK`/`S2-BACK`/`S3-BACK` หรือหาย · จดบรรทัดข้อความป้าย+สีครบทุกป้ายทุกภาพ (ไม่มี = เขียน "none" ห้ามเว้นว่าง)
ATTENDED: PASS = ป้ายชื่อใน `S3-BACK` ครบเท่ากับ `S0-SPAWN` ทุกตัว และมี `OBSERVER_CONFIRMED` กำกับ · NEGATIVE (มีค่าเท่าผลบวก) = หาย >=1 ตัว -> ระบุตัวที่หาย เปิดใบ RE ใหม่ ห้ามรันซ้ำแบบเดา · ไม่มี `OBSERVER_CONFIRMED` = ชั้น client ยังไม่ PASS
ATTENDED: ไม่มีแฟล็ก ไม่มีธง (ไม่มี `--population-scenario`) · 🔴 บูตบน DB สำเนาเท่านั้น ห้ามเปิด canonical: `copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-250_<stamp>.sqlite3` + `copy state\pirateforce.sqlite3 state\run_gt250_<stamp>.sqlite3` · sha256 canonical ต้องตรง `CANON_SHA.txt` ก่อน/หลัง + `PRAGMA integrity_check = ok` (= W3 ไม่ทำ = ปิดใบไม่ได้)
ATTENDED: STOP ทันทีถ้าไคลเอนต์ปิดตัวหรือมีหน้าต่างบทสนทนา/error เด้งขึ้นเอง บันทึกขั้นที่หยุดแล้ว teardown อยู่ดี · ถ้าเผลอคลิกให้จดเวลาไว้ตรง ๆ อย่าลบรอบทิ้ง

- objective (ข้ออ้างเดียว): บนบิลด์ปัจจุบัน หลังผู้เล่นเดินออกจากจุดเกิดจนตัวละคร/NPC ชุดแรกหลุดจอ แล้วเดินกลับมาที่เดิม **ป้ายชื่อ (เขียว) ที่เห็นตอน T0 ยังอยู่ครบหรือไม่** -- นี่คือชั้น client-observable ของ `RE-138` ที่ใบนั้นเขียนเองว่า "ไม่เคยเปิด" (ไม่มีใครเดินไปกลับแล้วดูป้ายในบิลด์นี้) ใบนี้**ไม่**ถามว่าทำไม และ**ไม่**รื้อชั้น wire ของ `RE-138` ที่ปิดไปแล้ว

- db (สำเนาเสมอ ห้ามเปิด canonical):
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-250_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt250_<yyyyMMdd_HHmmss>.sqlite3
```
  sha256 ของ canonical ต้องตรง `CANON_SHA.txt` ทั้งก่อนและหลัง · `PRAGMA integrity_check = ok` ทั้งสองครั้ง

- server args (ไม่มีแฟล็ก scenario ใด ๆ -- production path ล้วน):
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt250_<stamp>.sqlite3
```
  เฉพาะ exit 0 + บรรทัด `BOOT_COMMIT: <sha>` เท่านั้นที่บูตได้ · เก็บ stdout+stderr รวมกัน (2>&1)
  🔴 **ตั้งใจไม่ใส่ `--population-scenario`**: เลน V94 reconcile (retained/entrant mask ที่ `population.py:206-223`) เป็น opt-in ผูกกับแฟล็กนั้น (`app.py:146` · จุดเรียก `runtime.py:4541-4619`) ใบนี้วัด **เส้นทาง production ที่ไม่มีธง** ซึ่งเป็นเส้นทางเดียวกับที่ Panya เห็นอาการเอง · ถ้า LANE-A อยากเห็น mask ของ V94 บนจอ = คนละบูต คนละใบ

- steps (~5 นาที · Port Royal · อัดวิดีโอต่อเนื่องทั้งเซสชัน):
  0. ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · สำเนา DB · เตรียม `TEMPLATE_teardown_generic.ps1`
  1. เปิดเซิร์ฟเวอร์ก่อนเสมอ (พอร์ต 10188/10189 ต้องว่างก่อนเปิดไคลเอนต์) แล้วค่อยเปิดไคลเอนต์ -> เลือกเซิร์ฟเวอร์ -> ปุ่มซ้ายของกล่อง PVP -> หน้าเลือกตัวละคร -> **ปุ่มกลางจาก 5 ปุ่มล่าง = เข้าเกม** (ห้ามปุ่มซ้ายสุด = ลบตัวละคร)
  2. **T0** -- ยืนนิ่งที่จุดเกิด ถ่ายภาพเต็มความละเอียด `S0-SPAWN` · จดพิกัด X/Y ที่ HUD · จด **ทุกป้ายในเฟรม บรรทัดละหนึ่งป้าย**: ข้อความป้าย + สี + ว่าเป็นป้ายชื่อหรือป้ายฉายา (ไม่มี = เขียนคำว่า "none" ห้ามเว้นว่าง)
  3. NO-CRASH check: **คลิกขวาลากกล้อง** หนึ่งครั้ง (กล้องอย่างเดียว ทิศทางตัวละครไม่ขยับ ไม่มีไบต์ออกสาย ปลอดภัยทุกจังหวะ) · **ห้ามใช้ `Q`/`E` เป็น NO-CRASH check** -- สองปุ่มนั้นหันตัวละครจริงและยิง `TargetPosVital`
  4. เดินออกด้วย `W/A/S/D` เท่านั้น (ยิง `TargetPosVital` เป็นเรื่องปกติของขั้นนี้) จนกว่า **ไม่มี NPC ตัวใดจากภาพ `S0-SPAWN` อยู่ในเฟรม** แล้วเดินต่ออีก ~5 วินาที · หยุดนิ่ง ถ่าย `S1-FAR` + จดพิกัด HUD + จดทุกป้ายในเฟรม
  5. เดินกลับมาที่จุดเดิม (พิกัด HUD ใกล้เคียง `S0-SPAWN` ที่สุดเท่าที่ทำได้) หยุดนิ่ง 3 วินาที ถ่าย `S1-BACK` + จดพิกัด + จดทุกป้าย
  6. ทำซ้ำข้อ 4-5 อีกสองรอบ ได้ `S2-FAR`/`S2-BACK`/`S3-FAR`/`S3-BACK`
  7. NO-CRASH check อีกครั้ง (คลิกขวาลากกล้อง)
  8. logout -> teardown ด้วย `TEMPLATE_teardown_generic.ps1` (boot stamp ต้องยังไม่เกิน 420 นาที · รอบที่จบเพราะเลิกเล่นก็ต้อง teardown) -> เทียบ sha canonical -> sha256 ทุกภาพ
  🔴 **ห้ามคลิกอะไรทั้งสิ้นตลอดใบ** (ห้ามคลิกพื้น ห้ามคลิก NPC ห้ามคลิกมินิแมป) -- คลิก NPC เปิดบทสนทนาและทำให้เซิร์ฟเวอร์ประกอบสำมะโนใหม่ทั้งฉาก ซึ่งจะปนเปื้อนคำถามของใบนี้ · ถ้าเผลอคลิก ให้จดเวลาไว้ตรง ๆ แล้วเดินต่อ อย่าลบรอบทิ้ง

- pass criteria (สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น):
    wire/DB (พิสูจน์ headless ได้ ไม่ต้องมีตาคน):
      W1. เก็บเฟรมขาออก/ขาเข้าทุกเฟรมตลอด 3 รอบเดิน พร้อม opcode + ขนาดไบต์ + `t` เทียบ `T0` **และระยะจากตัวละครถึง NPC ที่กล่าวถึง** (กติกา `G-FRAME` -- เฟรมที่ยกมาเป็นหลักฐานต้องมีสองค่านี้เสมอ ใช้พิกัด HUD ที่จดไว้แต่ละภาพเป็นฐานคำนวณ)
      W2. ระบุให้ชัดว่ามีเฟรมที่บรรจุ `NPCAttr`/`BasicAttr` ออกจากเซิร์ฟเวอร์ระหว่างการเดินหรือไม่ (มี = กี่เฟรม เวลาใด · ไม่มี = เขียน "0 frames" ตรง ๆ)
      W3. `sessions` +1 แถวต่อการล็อกอิน · `lease_generation` ไม่ถอยหลัง · `integrity_check = ok` · sha canonical ก่อน=หลัง · ไม่มี traceback ไม่มี socket ปิดผิดจังหวะ
      ชั้นนี้**ตอบไม่ได้**ว่าบนจอเห็นป้ายอะไร ห้ามใช้แทนชั้นล่าง
    client-observable (ต้องมีคนอยู่หน้าจอ ห้ามอนุมานจากไฟล์จับสาย):
      C1. ตารางเทียบ `S0-SPAWN` vs `S1-BACK` / `S2-BACK` / `S3-BACK`: ป้ายชื่อของแต่ละตัวที่เคยมีใน `S0-SPAWN` ยังมีอยู่หรือหายไป (ระบุเป็นรายตัว)
      C2. **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** (ข้อบังคับ R163 คำสั่ง Panya 2026-08-25): หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ · เขียนคำว่า "none" ไม่เว้นว่าง · อ่านสีจากภาพนิ่งเต็มความละเอียดเท่านั้น ห้ามอ่านจาก contact sheet / ภาพย่อ / วิดีโอ · **ผู้เทสจดสีอย่างเดียว ห้ามอนุมานสาเหตุของสี** (สาเหตุเป็นคำถามของ `RE-067` ทั้งใบ)
      C3. ต่างจากภาพเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ
      C4. NO-CRASH check ผ่านทั้งสองครั้ง
      **ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = ชั้นนี้ยังไม่ PASS** ไม่ว่าชั้น wire จะสวยแค่ไหน
    การอ่านผล: **PASS** = ป้ายชื่อใน `S3-BACK` ครบเท่ากับ `S0-SPAWN` ทุกตัว · **NEGATIVE (มีค่าเท่าผลบวก)** = หายอย่างน้อยหนึ่งตัว -> ระบุตัวที่หาย แล้ว redirect ไปทาง object lifetime / actor generation reuse ที่ `RE-138` ระบุเป็น nonclaim ของตัวเอง (เปิดใบ RE ใหม่ ห้ามรันใบนี้ซ้ำแบบเดา)

- predictions (คำทำนายคือคำทำนาย · ทายผิด = finding ไม่ใช่ความล้มเหลว):
  - P1 [เสนอ · หัวใจของใบ]: ป้ายชื่อยังอยู่ครบทั้ง 3 รอบ เพราะบิลด์นี้ไม่มีรอบ reconcile ที่ทำงานโดยไม่มีธง
  - P2 [เสนอ · ชั้น wire]: W2 = **0 frames** เพราะเลน V94 ผูกกับ `--population-scenario` ซึ่งบูตนี้ไม่ได้ใส่
  - P3 [ตัวหักล้าง]: ป้ายชื่อหายจริงเหมือนภาพ 235212 ของเจ้าของ ทั้งที่ W2 = 0 frames -> เป็นผลลบที่สมบูรณ์ และชี้ไปที่ฝั่งไคลเอนต์/lifetime ไม่ใช่ mask

- nonclaims:
  1. ไม่ตัดสินสาเหตุของการหาย/ไม่หายของป้าย และไม่ตัดสินสาเหตุของสีใด ๆ (`RE-067` เป็นเจ้าของคำถามสี)
  2. ไม่รื้อ ไม่กลับคำ ชั้น wire ของ `RE-138` ที่ปิดแล้ว (mask แคบกว่าไม่ล้างชื่อ -- พิสูจน์แล้ว)
  3. ไม่วัดเลน V94 `--population-scenario` เลย (คนละบูต คนละใบ)
  4. ไม่พิสูจน์อะไรกับฉากอื่นนอก Port Royal · ตัวละครเดียว เซสชันเดียว
  5. ไม่ตัดสินว่าการเติม `basic_name` ใน reconcile คุ้มหรือไม่ (`RE-138` เรียกมันว่า hardening ไม่ใช่ root-cause fix)

- STOP: **STOP ถ้าไคลเอนต์ปิดตัว** -- หยุดทันที บันทึกว่าหยุดที่ขั้นไหน แล้ว teardown อยู่ดี · STOP เพิ่มเติม: ถ้ามีหน้าต่างบทสนทนา/error เด้งขึ้นมาเอง ให้หยุดและบันทึกภาพก่อนทำอะไรต่อ

- links: `CLIENT_RE_QUEUE.md:2322` (`RE-138` ทั้งใบ · บรรทัด "ชั้น client-observable ไม่เคยเปิด") · `notes_to_chief/20260903_0253_RE-138-RESULT-BASICATTR-OMISSION-PRESERVES-NAME.md` · `notes_to_chief/20260905_0106_KA1A-BACKSWEEP-re-to-gt-gap-list-4-open-1-defer-3-stale-bookkeeping.md` หมวด ก. ข้อ 1 · `pirate-force-server/src/pirateforce_foundation/population.py:206-223` · `.../app.py:146` · `.../runtime.py:4541-4619`

- 🔴 หมายเหตุจาก chief (`kj0s6r`/R346) — **ความต่างที่ตั้งใจ ระหว่างใบนี้กับข้อเสนอของ ka1-A**: ka1-A เสนอให้ฝั่งเซิร์ฟเวอร์ "capture เฟรม reconcile (retained/entrant mask `population.py:206-223`)" แต่โค้ดชุดนั้นเป็น **opt-in หลังแฟล็ก `--population-scenario`** ⇒ ใบนี้เขียนแบบ **ไม่มีธง** เพื่อวัดเส้นทางเดียวกับที่ Panya เห็นอาการเอง และประกาศไว้ตรง ๆ ว่า mask ของ V94 **ไม่ถูกวัดในใบนี้** · ถ้า LANE-A ต้องการเฟรม reconcile จริง = ใบที่สอง คนละบูต (ขอเลขจาก chief) — **ตัดสินก่อนเรียกผู้เทส อย่าให้ผู้เทสเจอความกำกวมหน้าเครื่อง**

- result:
  (ว่าง -- ผู้เทสกรอก)

## numbering
`GT-250`/`RE-250` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/`) ก่อนวาง -- ตรวจโดย chief รอบ `kj0s6r`/R346 · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `249` => ใบนี้ `250`

---

## GT-251 TRACEPATH-GO-TWO-TARGETS-DISCRIMINATOR-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ANSWERED — ตอบ RE-236(ข)/RE-119 T4: id ที่ client ส่งใน TracePathVital คือ id ประจำตัว NPC/วัตถุ ไม่ใช่ลำดับแถว (157/161/153) — R317 2026-09-05 §3 · ข้อเสนอ ka1-A: เปิดใบสร้าง CORE-REQUEST ให้ LANE-UI/LANE-A ตอบ CTracePathVital ด้วยเส้นทางจริง (ยังไม่มีใบสร้างเปิดตามคำขอนี้ ณ 2026-09-06 ตามที่ LANE-K ตรวจ — LANE-K พับผลอย่างเดียว ไม่เปิดใบสร้างแทนสาย) · จาก notes_to_chief/20260905_1125_KA1A-R317-*.md · 🟢 **READY** -- บูตได้ทันที ไม่มีธง (dispatch `0x4391` เป็น production ไม่มี `--*-scenario` ตั้งแต่ `CORE-REQUEST-025`) · **เจ้าของใบ/ผู้บริโภคผล = LANE-UI** (สายที่เปิด `RE-236`) · ผู้เปิดใบ = chief (LANE-E) รอบ `kj0s6r`/R346 ตาม `COO-DECISION 20260904_2143` ข้อ 3 และคำตัดสิน COO `NOW.md` 2026-09-05 01:45 · ผู้รัน = Panya (attended) ~5 นาที · **ข้อ 2 ใน 4 ใบ** (GT-250 > GT-251 > GT-252 > GT-253) · **ต่อท้ายคิว `รอเครื่องคุณ` ไม่ใช่หัวคิว** (GT-247 / GT-249 / GT-245 อยู่ก่อน) · ไม่บล็อกสายใด · **ไม่มีการตีมอน**]

- objective (ข้ออ้างเดียว): ใน `CTracePathReqVital` (`0x4391`) ที่ไคลเอนต์ยิงตอนกดปุ่ม **GO!** ในหน้าต่างแผนที่ ฟิลด์ `u16@+0x14` (discriminator) **ผูกกับตัวไหน** ระหว่าง quest id / NPC id / index ของแถวในรายการที่คลิก -- ปิดข้อ (ข) ของ `RE-236` ที่ `RE-119` T4 ทิ้งไว้ bounded-negative ตั้งแต่ 28 ส.ค. (ค่าเดียวที่เคยจับได้ `743` ชนทั้ง `QUESTDATA_TH__QUEST.tsv n_ID=743` และ `CONSTDATA_TH__MOBS.tsv n_ID=743` พร้อมกัน)

- db (สำเนาเสมอ):
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-251_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt251_<yyyyMMdd_HHmmss>.sqlite3
```
  sha256 canonical ต้องตรง `CANON_SHA.txt` ก่อนและหลัง · `integrity_check = ok` ทั้งสองครั้ง · ใบนี้คาดว่าไม่มีการเขียน DB นอกจาก `sessions` +1 แถว

- server args (ไม่มีแฟล็ก scenario):
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
git grep -n "0x4391\|TRACE_PATH_REQ_VITAL_ID" <SHA> -- src/pirateforce_foundation/runtime.py
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt251_<stamp>.sqlite3
```
  ต้องได้อย่างน้อย 1 บรรทัดจากคำสั่ง `git grep` · ไม่ได้ = BLOCKED ห้ามบูต · เก็บ stdout+stderr รวมกัน (2>&1) · เปิด capture root ใหม่ (`GameClient\capture_gt251_<stamp>\`) ให้ `GAME_EVENTS_LIVE.txt` ครอบทั้งเซสชัน

- steps (~5 นาที · อัดวิดีโอต่อเนื่อง):
  0. `LOCK_GAME` · boot stamp · sha canonical · สำเนา DB · เตรียม teardown
  1. เซิร์ฟเวอร์ก่อน แล้วเปิดไคลเอนต์ -> เข้าเกม (ปุ่มกลางของ 5 ปุ่ม ห้ามปุ่มซ้ายสุด)
  2. **T0** -- ยืนนิ่ง ถ่าย `S0-HOME` เต็มความละเอียด · จดพิกัด HUD · จดทุกป้ายในเฟรม (บรรทัดละป้าย · "none" ถ้าไม่มี)
  3. NO-CRASH check: คลิกขวาลากกล้อง (กล้องอย่างเดียว ไม่มีไบต์ออกสาย) · ห้ามใช้ `Q`/`E`
  4. กด `M` เปิดหน้าต่างแผนที่ · ถ่าย `S1-MAP-LIST` เต็มความละเอียด · **คัดรายการที่เห็นทั้งหมดแบบตัวต่อตัว**: ชื่อแถว + ลำดับแถว (นับจาก 1 บนลงล่าง) + หมวด/แท็บที่มันอยู่ · อ่านไม่ออกให้เขียน "illegible" ห้ามเดา
  5. **เป้า A** -- เลือกแถวหนึ่ง (ควรเป็น NPC) จด **ชื่อแถว + เลขลำดับแถว + หมวด** แล้วกด **GO!** หนึ่งครั้ง · จดเวลานาฬิกา `T_GO_A` (HH:MM:SS+07:00) · ถ่าย `S2-AFTER-GO-A` ทันที และอีกใบที่ ~3 วินาที
  6. **เป้า B** -- เลือกอีกแถวที่ **ชื่อและลำดับแถวต่างจาก A ชัดเจน** และถ้ามีหมวดเควส/จุดสำรวจแยกจากหมวด NPC ให้เลือก**คนละหมวดกับ A** (เพิ่มโอกาสที่ค่าจะแยกได้) · จดชื่อ + เลขลำดับ + หมวด แล้วกด **GO!** หนึ่งครั้ง · จด `T_GO_B` · ถ่าย `S3-AFTER-GO-B` + อีกใบที่ ~3 วินาที
  7. **control (ไม่ใช่ข้ออ้างของใบ)** -- คลิกมินิแมป 1 ครั้ง จดเวลา · `GT-246` วัดไว้แล้วว่าเฟรมนี้ได้ `+0x14=0` ใช้เป็นตัวเช็คว่า decoder ของรอบนี้อ่านตรงกับรอบก่อน
  8. NO-CRASH check อีกครั้ง · logout -> teardown (boot stamp < 420 นาที) -> เทียบ sha canonical -> sha256 ทุกภาพ
  🔴 ถ้ารายการในหน้าต่างแผนที่มีแถวเดียวหรือกด GO! ไม่ได้: **หยุด บันทึกภาพ แล้วรายงานว่าใบนี้เดินไม่ถึงจุดวัด** (ไม่ใช่ FAIL ไม่ใช่ NO-RESULT -- คือ "ด่านหน้าจอไม่เปิด")

- pass criteria (สองชั้น ห้ามปน):
    wire/DB (headless):
      W1. จับเฟรม `CTracePathReqVital 0x4391` ได้ **สองเฟรม** (A และ B) เก็บ hex ดิบทั้งก้อน (คาด 25 B ต่อเฟรม) พร้อม `t` เทียบ `T0` **และระยะจากตัวละครถึงจุด/เป้าที่กด GO!** (กติกา `G-FRAME`) · ถ้าอ่านระยะไม่ได้ ให้เขียนพิกัด HUD ที่จดไว้แทนและระบุว่าคำนวณระยะไม่ได้
      W2. ถอดทั้งสองเฟรมตาม schema `external/PF_SERIALIZER_FIELDS.tsv:5521-5528` (8 ฟิลด์ tag ตรงทุกไบต์ ไม่มีไบต์เหลือ) รายงานค่า `+0x14` `+0x16` `+0x18` `+0x1C` `+0x1E` `+0x20` `+0x22` `+0x24` ของทั้งสอง
      W3. บันทึก reply ของเซิร์ฟเวอร์ต่อแต่ละ request (คาด `TRACE_PATH_EMPTY_VECTOR_REPLY`) และเฟรมอื่นที่ออกในช่วงเดียวกัน
      W4. `sessions` +1 · `lease_generation` ไม่ถอยหลัง · `integrity_check = ok` · sha canonical ก่อน=หลัง · ไม่มี traceback
      **การตัดสินของใบ (ทำนอกจอ หลังรอบ)**: เอา `+0x14` ของ A และ B ไปเทียบกับ (ก) `QUESTDATA_TH__QUEST.n_ID` ของแถวที่กด (ข) `CONSTDATA_TH__MOBS.n_ID` / NPC id ของเป้า (ค) เลขลำดับแถวที่ผู้เทสจดไว้ · **ปิดขาด = ตรงกับตัวใดตัวหนึ่ง 2/2 ครั้ง และตัวอื่นไม่ตรง** · ยังชนสองทางเหมือนเดิม = **bounded-negative ที่สมบูรณ์**
      ชั้นนี้ตอบไม่ได้ว่าผู้เทสคลิกแถวไหน/ชื่ออะไร -- ค่านั้นมาจากชั้นล่างเท่านั้น
    client-observable (ต้องมีตาคน):
      C1. ข้อความในรายการหน้าต่างแผนที่ ตัวต่อตัว + เลขลำดับแถวของ A และ B + หมวดของแต่ละอัน (นี่คือหลักฐานชิ้นเดียวที่ทำให้ตัวเลือก "list index" ตัดสินได้ ไม่มีทางเดาจากสาย)
      C2. บนจอเกิดอะไรหลังกด GO! แต่ละครั้ง -- ข้อความสีส้มกลางจอ ขึ้น/ไม่ขึ้น/หายใน ~กี่วินาที · มีข้อความแชทไหม (คัดตัวต่อตัว) · ตัวละครขยับหรือไม่
      C3. บรรทัดสีป้ายชื่อครบทุกป้ายทุกภาพ (หนึ่งบรรทัดต่อป้ายต่อภาพ · "none" ไม่เว้นว่าง · อ่านจากภาพเต็มความละเอียดเท่านั้น · ห้ามอนุมานสาเหตุของสี -- `RE-067` เป็นเจ้าของคำถามนั้น) · ต่างจากภาพเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      C4. NO-CRASH check ผ่านทั้งสองครั้ง
      **ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = ชั้นนี้ไม่ PASS**

- predictions (ทายผิด = finding):
  - P1 [เสนอ]: `+0x14` ของ A กับ B **ต่างกัน** และตรงกับตัวแปรใดตัวหนึ่งใน 3 ตัว 2/2 -> ปิดข้อ (ข) ของ `RE-236`
  - P2 [ตัวหักล้างที่มีน้ำหนักจริง]: `+0x14` = **0 ทั้งสองเฟรม** สอดคล้องกับ `RE-119` T4 ที่พิสูจน์จาก disassembly ว่า constructor `0x006EBA90` zero ฟิลด์ `+0x14..+0x24` ทุกครั้ง -> **bounded-negative ที่สมบูรณ์** และ redirect ไปคำถามที่ `RE-236` เปิดค้างไว้เอง (ใครเขียนค่าที่ไม่ใช่ศูนย์ที่เห็นในเฟรมมินิแมปของ `GT-246` -- write-site ตัวที่สอง)
  - P3 [คาดบนจอ ไม่ใช่เกณฑ์ผ่าน]: ข้อความสีส้ม "กำลังค้นหาเส้นทาง..." หายเองภายในราว 1 วินาที ตามด้วยข้อความแชทว่าหาเป้าหมายไม่พบ (พฤติกรรม empty-vector ที่ `GT-120` PASS ไว้แล้ว) · ตัวละครไม่เดินไปไหน -- ถ้าตัวละคร**เดิน**จริง ให้เขียนเป็น finding แยก ไม่ใช่ผลของใบนี้

- nonclaims:
  1. ไม่ตัดสินความหมายของ `+0x16`/`+0x18`/`+0x1C..+0x24` (ยังไม่มีใครตัดสิน ห้ามเดา)
  2. ไม่พิสูจน์ว่า auto-walk / `RunFindPath` ทำงานได้ -- เซิร์ฟเวอร์ตอบ empty-vector เท่านั้น
  3. ไม่ปิด ไม่กลับคำ `RE-119` (CLOSED PASS/DONE) และไม่แตะ `GT-246` (ANSWERED · ห้ามบูตซ้ำ)
  4. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ · ฉากเดียว เซสชันเดียว สองเป้า
  5. ไม่พิสูจน์ว่าเป้าอื่น/ฉากอื่นให้ผลเดียวกัน

- STOP: **STOP ถ้าไคลเอนต์ปิดตัว** (บันทึกว่าหยุดที่เฟรม/ขั้นไหน แล้ว teardown อยู่ดี) · STOP ถ้าเจอ `ErrorData` ใด ๆ -- จดค่าที่ส่งล่าสุดก่อนหยุด

- 🔴 หมายเหตุจาก chief (`kj0s6r`/R346) — **สองจุดที่ยังไม่มีใครวัด อย่าให้ผู้เทสเจอเองหน้าเครื่อง**: (1) ไม่มีบันทึกไหนบอกว่าหน้าต่างแผนที่ของบิลด์ปัจจุบัน **มีแถวให้เลือกกี่แถวและเป็นอะไรบ้าง** (`GT-120` บอกแค่ "เลือก NPC แล้วกด GO!" · `GT-246` คลิกแต่มินิแมป) ⇒ ความเป็นไปได้ที่จะหาสองแถวที่ `QUEST.n_ID`/`MOBS.n_ID` ไม่ชนกันบนจอ **ยังไม่ถูกยืนยัน** จึงมีทางออกที่ขั้น 9 ไว้ให้ · (2) "ระยะจากตัวละครถึงเป้า" ของเป้าบนแผนที่อาจคำนวณไม่ได้จริง ⇒ อนุญาตให้บันทึกพิกัด HUD แทนพร้อมระบุว่าคำนวณไม่ได้ (ทำตามเจตนาของ `G-FRAME` ไม่ใช่ตามตัวอักษร)

- links: `CLIENT_RE_QUEUE.md` (`RE-236` · ข้อ (ข) และวิธีปิดที่ `RE-119` T4 กำหนดไว้เอง) · `GT-246` (ANSWERED · payload มินิแมป 25 B) · `GT-120` (PASS · เส้นทางคลิก `M` -> เลือกเป้า -> GO!) · `external/PF_SERIALIZER_FIELDS.tsv:5521-5528` · `notes_to_chief/20260904_1226_LANE-UI-RE-TICKET-tracepath-record0-semantic-needs-attended-differential.md` · `notes_to_chief/20260905_0106_KA1A-BACKSWEEP-*.md` หมวด ก. ข้อ 2

ATTENDED: กด `M` เปิดแผนที่ คัด list ตัวต่อตัว (ชื่อ+ลำดับแถว+หมวด) แล้วเลือกเป้า A (จดชื่อ/ลำดับ/หมวด) กด **GO!** ครั้งเดียว จดเวลา `T_GO_A` ถ่าย `S2-AFTER-GO-A` -- ทำซ้ำกับเป้า B ที่ชื่อ/ลำดับ/หมวดต่างจาก A ชัดเจน จด `T_GO_B` ถ่าย `S3-AFTER-GO-B` แล้วคลิกมินิแมป 1 ครั้งเป็น control
ATTENDED: จับเฟรม `CTracePathReqVital 0x4391` สองเฟรม (A/B) ดูค่า `u16@+0x14` ของแต่ละเฟรมเทียบกับ `QUESTDATA_TH__QUEST.n_ID`/`CONSTDATA_TH__MOBS.n_ID`/เลขลำดับแถวที่จดไว้
ATTENDED: PASS ชั้นจอ = ข้อความสีส้มขึ้น/หายตามที่คาด ไม่ค้าง ไม่ error ทั้งสองครั้งกด GO! + บรรทัดสีป้ายครบทุกภาพ + `OBSERVER_CONFIRMED: <ISO+07:00>` -- ไม่มีลายเซ็นนี้ = ไม่ PASS ไม่ว่าเฟรมจะครบแค่ไหน
ATTENDED: บูตมาตรฐาน ไม่มีแฟล็ก `--*-scenario` ใด ๆ (dispatch `0x4391` เป็น production) เปิด capture root ใหม่ `capture_gt251_<stamp>\` ครอบทั้งเซสชัน
ATTENDED: หน้าต่างแผนที่มีแถวเดียว/กด GO! ไม่ได้ = หยุด บันทึกภาพ รายงาน "เดินไม่ถึงจุดวัด" (ไม่ใช่ FAIL/NO-RESULT)

- result:
  (ว่าง -- ผู้เทสกรอก)

## numbering
`GT-251`/`RE-251` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/`) ก่อนวาง -- ตรวจโดย chief รอบ `kj0s6r`/R346

---

## GT-252 COLUMBUS-OPTION2-BORNAGAIN-CLICK-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS — เก็บครบตามใบ (R317 2026-09-05 §4: quest 3205 ถูกปฏิเสธ reason=no_home_marker_persistence_row_evidence ตามออกแบบ · รูป Columbus ค้างหลังหน้าต่างปิด — ญาติ RE-168) · regression ยืนยันซ้ำ R321 2026-09-06 11:47 (CAPTURED-AGAIN) · RESULT: GT-252 CAPTURED-AGAIN R321 2026-09-06 11:47 (first R317) · จาก notes_to_chief/20260905_1125_KA1A-R317-*.md + notes_to_chief/20260906_1255_KA1A-R321-*.md · 🟢 **READY** -- บูตได้ทันที ไม่มีธง · **รันบนสำเนา DB ของรอบ (DB run-copy) เสมอ** · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** (สายที่ปิด `RE-112` และเป็นเจ้าของ `CORE-REQUEST-019`) · ผู้เปิดใบ = chief (LANE-E) รอบ `kj0s6r`/R346 ตาม `COO-DECISION 20260904_2143` ข้อ 3 และคำตัดสิน COO `NOW.md` 2026-09-05 01:45 · ผู้รัน = Panya (attended) ~3 นาที · **ข้อ 3 ใน 4 ใบ** (GT-250 > GT-251 > GT-252 > GT-253) · **ต่อท้ายคิว `รอเครื่องคุณ` ไม่ใช่หัวคิว** · ไม่บล็อกสายใด · ค่าต่ำแต่จริง: `BUILD_IMPACT` ของ `RE-112` คง quest 3205 เป็น refusal "จนกว่าจะมี capture จริง" · **ไม่มีการตีมอน**]

ATTENDED: บูตเซิร์ฟบนสำเนา DB run-copy เสมอ (`state\run_gt252_<stamp>.sqlite3` จาก `pirateforce.sqlite3`) ไม่มีแฟล็ก scenario -> ต้องยืนฉาก Port Royal (scene 1) และเปิดบทสนทนา Columbus มาก่อน -> เดินเข้าหาด้วย `W/A/S/D` คลิกซ้าย Columbus 1 ครั้งให้หน้าต่างเปิด -> คัดข้อความสองบรรทัดของตัวเลือก แล้ว **คลิก option 2 (บรรทัดที่สอง) ครั้งเดียว** จดเวลา `T_CLICK` -- ห้ามคลิก option 1 เด็ดขาด (วาร์ปฉาก 17 ทำให้ใบเสียทั้งใบ) · 🔴 ตัวเก็บเฟรมขาเข้า+ขาออกต้องทำงาน **ก่อน** คลิก option 2 และปล่อยยาวถึง `T_CLICK+5s` -- `W1`/`W4` ของใบเก็บย้อนหลังไม่ได้ ไม่มีสองข้อนี้ = ปิดได้แค่ชั้น client-observable ไปไม่ถึง PASS (กติกาผ่านของใบเอง = `W1+W2+W4`)
ATTENDED: ไม่กดอะไรอีก 10 วินาที ถ่าย `S2-A1/A2/A3` ที่ ~1/3/10 วิ แล้วดูคอนโซลหา `COLUMBUS_QUEST3205_BORNAGAIN_REFUSED reason=no_home_marker_persistence_row_evidence` หนึ่งครั้ง (`2>&1` รวม stdout/stderr) -- เห็น `reason=not_home_scene` แทน = precondition พัง บันทึกเป็น NO-RESULT ไม่ใช่ FAIL · ทำ NO-CRASH check ด้วยคลิกขวาลากกล้องเท่านั้น ห้ามใช้ `Q`/`E`
ATTENDED: ผ่านชั้น client-observable (คำตอบหลักของใบ) = หลังคลิก option 2 ใน 10 วินาที ไคลเอนต์ไม่ค้าง ไม่ error (ปฏิเสธเงียบตามที่ตั้งใจ) · NEGATIVE ที่มีค่าเท่ากัน = ค้าง/error/รอ ack จริง · ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = ชั้นนี้ไม่ PASS ไม่ว่าชั้น wire/DB จะครบแค่ไหน
ATTENDED: จดบรรทัดสีป้ายชื่อทุกป้ายทุกภาพ (บรรทัดละป้ายต่อภาพ "none" ไม่เว้นว่าง อ่านจากภาพเต็มความละเอียดเท่านั้น ห้ามอนุมานสาเหตุของสี) -- ต่างจากภาพเซิร์ฟเวอร์เดิมให้ลง `REAL_SERVER_DIVERGENCE.tsv`
ATTENDED: STOP ทันทีถ้าไคลเอนต์ปิดตัว หรือจอวาร์ปไปฉากอื่น (โดนคลิก option 1) หรือเจอ `ErrorData` -- บันทึกตามจริงแล้ว teardown อยู่ดี ห้ามคลิก option 2 ต่อในบูตนั้น

- objective (ข้ออ้างเดียว): กด option 2 ของบทสนทนา Columbus ("ตั้งฐานทัพที่ Port Royal" = quest 3205 / Q_BORNAGAIN) **หนึ่งครั้ง** บนเซิร์ฟเวอร์วันนี้ แล้วเส้นทางปฏิเสธของ `CORE-REQUEST-019` ทำงานตามที่เขียนไว้จริงหรือไม่ -- คือ **มีเฟรม `QuestOperateVital` ขาเข้าจริง และไม่มีไบต์ตอบกลับเลยบนเส้นทางนั้น** โดยที่ไคลเอนต์**ไม่ค้าง ไม่ขึ้น error** (นี่คือ attended capture ที่แคบที่สุดที่ใบผล `RE-112` เสนอไว้เอง)

- db (สำเนาเสมอ · ห้ามเปิด canonical · ใบนี้แตะเส้นทางที่โดยหลักการเขียน DB ได้):
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-252_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt252_<yyyyMMdd_HHmmss>.sqlite3
```
  sha256 canonical ตรง `CANON_SHA.txt` ก่อนและหลัง · `integrity_check = ok` ทั้งสองครั้ง · คาดว่า `character_positions.scene_id` ยังเป็น 1 หลังจบรอบ (`HOME_SCENE_ID` · `world_scene_travel.py:177`)

- server args (ไม่มีแฟล็ก scenario):
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
git grep -n "COLUMBUS_QUEST3205_BORNAGAIN_REFUSED" <SHA> -- src/pirateforce_foundation/columbus_quest_dispatch.py
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt252_<stamp>.sqlite3
```
  ต้องได้อย่างน้อย 1 บรรทัดจาก `git grep` · ไม่ได้ = BLOCKED ห้ามบูต · เก็บ stdout **และ** stderr รวมกัน (2>&1) -- บรรทัดปฏิเสธของเส้นทางนี้อยู่คนละสตรีมกัน

- PRECONDITION (ตรวจก่อนขั้นที่ 1 ไม่ใช่เชิงอรรถ):
  P0. ต้องยืนอยู่ **Port Royal (scene 1)** ตอนกด option 2 · ยืนฉากอื่น = เซิร์ฟเวอร์ปฏิเสธคนละเหตุผล (`runtime.py:6444-6464`) และใบนี้จะไม่ได้คำตอบ
  P1. ต้องเปิดบทสนทนา Columbus ในเซสชันเดียวกันก่อน (latch `columbus_quest3021_conversation_sent`) มิฉะนั้น op1 ของ 3205 ไปไม่ถึง branch
  P2. เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ · ไคลเอนต์ที่เปิดค้างโดยไม่มีเซิร์ฟเวอร์ตายเองใน ~3.5 นาที
  P3. ฆ่าไคลเอนต์แล้วเซิร์ฟเวอร์ยังถือ session ไว้ -- ต้องรีสตาร์ตเซิร์ฟเวอร์ก่อนเปิดไคลเอนต์ตัวถัดไป ไม่งั้นค้าง "connecting" ตลอดไป
  P4. รอบนี้ก๊อป DB ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต = ปกติ ไม่ใช่ผลที่วัดได้
  P5. teardown ปฏิเสธ boot stamp ที่เก่ากว่า 420 นาที -- รอบที่จบเพราะเลิกเล่นก็ต้อง teardown

- steps (~3 นาที · อัดวิดีโอต่อเนื่อง):
  1. `LOCK_GAME` · boot stamp · sha canonical · สำเนา DB · เซิร์ฟเวอร์ก่อน แล้วเปิดไคลเอนต์ -> เข้าเกม (ปุ่มกลางของ 5 ปุ่ม)
  2. **T0** -- ยืนนิ่ง ถ่าย `S0-HOME` เต็มความละเอียด · จดพิกัด HUD · จดทุกป้ายในเฟรม (บรรทัดละป้าย · "none")
  3. NO-CRASH check: คลิกขวาลากกล้อง · ห้ามใช้ `Q`/`E`
  4. เดินเข้าหา Columbus ด้วย `W/A/S/D` จนอยู่ใกล้พอคลิกได้ · คลิกซ้ายที่ Columbus 1 ครั้ง -> หน้าต่างบทสนทนาเปิด · ถ่าย `S1-DIALOG` · **คัดข้อความของตัวเลือกทั้งสองบรรทัดแบบตัวต่อตัว** พร้อมระบุว่าบรรทัดบน = option 1 บรรทัดล่าง = option 2 (อ่านไม่ออก = "illegible")
  5. 🔴 **คลิก option 2 (บรรทัดที่สอง) ครั้งเดียว** · จดเวลานาฬิกา `T_CLICK` (HH:MM:SS+07:00)
  6. **ไม่กดอะไรอีก 10 วินาที** · ถ่ายภาพที่ ~1 วิ / ~3 วิ / ~10 วิ (`S2-A1` `S2-A2` `S2-A3`) · จดว่า หน้าต่างปิดเอง / ค้างเปิด / ตัวเลือกเทา / มีกล่อง error / มีข้อความแชท (คัดตัวต่อตัว)
  7. NO-CRASH check อีกครั้ง (คลิกขวาลากกล้อง)
  8. ถ้าหน้าต่างยังเปิดอยู่: คลิก option 2 **อีกครั้งหนึ่ง** แล้วบันทึกผลบนจอ -- **นี่เป็นการสังเกตแยก ไม่ใช่ข้ออ้างของใบ** (latch `columbus_quest3205_dispatch_attempted` ที่ `runtime.py:6465` ทำให้ครั้งที่สองไม่เข้า dispatch อยู่แล้ว) ต้องเขียนกำกับว่าเป็นคลิกที่สอง
  9. logout -> teardown -> เทียบ sha canonical -> sha256 ทุกภาพ
  🔴 **ห้ามคลิก option 1 ตลอดใบ** -- option 1 (quest 3021) วาร์ปไปฉาก 17 และหลังจากนั้น option 2 จะถูกปฏิเสธด้วยเหตุผล "ผิดฉาก" แทน ทำให้ใบนี้เสียรอบทั้งใบ

- pass criteria (สองชั้น ห้ามปน):
    wire/DB (headless):
      W1. จับเฟรมขาเข้าที่บรรจุ `QuestOperateVital` ตอน `T_CLICK` ได้ เก็บ hex ดิบทั้งก้อน พร้อม `t` เทียบ `T0` **และระยะจากตัวละครถึง Columbus** (กติกา `G-FRAME`)
      W2. คอนโซลพิมพ์ `COLUMBUS_QUEST3205_BORNAGAIN_REFUSED reason=no_home_marker_persistence_row_evidence` **หนึ่งครั้ง** (`columbus_quest_dispatch.py:762` + ค่าคงที่ที่ `:268-270`) และมี event `columbus_quest3205_dispatch_refused_no_home_marker_persistence_row_evidence`
      W3. **ไม่มี** บรรทัด `COLUMBUS_Q3205_BORNAGAIN_REFUSED scene=<n> reason=not_home_scene` บน stderr -- ถ้ามี แปลว่า P0 พัง (ยืนผิดฉาก) ให้บันทึกเป็น **NO-RESULT ของ precondition** ไม่ใช่ FAIL
      W4. **ช่วงไม่มีขาออก**: ตั้งแต่ `T_CLICK` ถึง `T_CLICK+5s` ไม่มีไบต์ออกบนเส้นทางนี้ · เฟรมอื่นที่ออกในช่วงนั้น (keepalive/heartbeat/ผลของการเดินก่อนหน้า) ให้ระบุแยกทีละเฟรมพร้อมเวลา ห้ามรวบเป็น "ไม่มีอะไร"
      W5. DB: `character_positions.scene_id` ยังเป็น 1 · `sessions` +1 แถว · `lease_generation` ไม่ถอยหลัง · `integrity_check = ok` · sha canonical ก่อน=หลัง · ไม่มี traceback
      ชั้นนี้ตอบไม่ได้ว่าหน้าต่างบนจอทำอะไร ห้ามใช้แทนชั้นล่าง
    client-observable (ต้องมีตาคน):
      C1. ข้อความตัวเลือกทั้งสองบรรทัด ตัวต่อตัว จาก `S1-DIALOG`
      C2. หลังคลิก option 2 หนึ่งครั้ง บนจอเกิดอะไรใน 10 วินาที -- เขียนเป็นภาษาปกติ: หน้าต่างปิดเอง / ค้าง / ไม่มีอะไรเกิดขึ้นเลย / มี error / มีข้อความแชท (คัดตัวต่อตัว) · **นี่คือคำตอบหลักของใบ**
      C3. ผลของคลิกที่สอง (ถ้าได้ทำ) แยกบรรทัดชัดเจน
      C4. บรรทัดสีป้ายชื่อครบทุกป้ายทุกภาพ (หนึ่งบรรทัดต่อป้ายต่อภาพ · "none" ไม่เว้นว่าง · อ่านจากภาพเต็มความละเอียดเท่านั้น ห้ามอ่านจากภาพย่อ/วิดีโอ · **ห้ามอนุมานสาเหตุของสี** -- `RE-067`) · ต่างจากภาพเซิร์ฟเวอร์เดิม = `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      C5. NO-CRASH check ผ่านทั้งสองครั้ง
      **ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = ชั้นนี้ไม่ PASS**
    การอ่านผล: **PASS** = W1+W2+W4 ครบ และบนจอไคลเอนต์ไม่ค้าง ไม่ error (ปฏิเสธเงียบตามที่ตั้งใจ) · **NEGATIVE ที่มีค่าเท่ากัน** = ไคลเอนต์ค้าง/ขึ้น error/รออะไรบางอย่าง -> แปลว่าไคลเอนต์**รอ ack จริง** ซึ่งเป็นคำตอบที่ `RE-112` หาอยู่พอดี และ redirect ไปหา shape ของ ack (ใบ RE ใหม่ ห้ามเดาเฟรมแล้วส่งไบต์ออก)

- predictions (ทายผิด = finding):
  - P1 [เสนอ]: หน้าต่างค้างเปิดอยู่เฉย ๆ ไม่มี error ไม่มีข้อความ -- ไคลเอนต์ไม่รออะไร สอดคล้องกับ `RE-112` ที่วัดว่า binding ฝั่งไคลเอนต์เป็น `xor eax,eax; ret 4`
  - P2 [เสนอ]: ช่วง `T_CLICK` -> `+5s` มี 0 ไบต์ออกบนเส้นทางนี้
  - P3 [ตัวหักล้าง]: ไคลเอนต์ค้าง/ขึ้น error/หน้าต่างไม่ตอบสนอง = ผลลบที่สมบูรณ์ และเป็นหลักฐานว่ามี ack ที่หายไป

- nonclaims:
  1. ไม่ claim ว่า option 2 พร้อมต่อสายจริง -- `BUILD_IMPACT` ของ `RE-112` ยังบังคับให้ quest 3205 เป็น named refusal จนกว่าจะมีทั้ง persistence schema ที่ chief อนุมัติ **และ** capture/crosswalk จริง
  2. ไม่ตัดสินหน้าตาคอลัมน์ DB ของ home marker (เป็นคำถามฝั่ง schema · `CORE-REQUEST-019`)
  3. ไม่พิสูจน์ว่า `ReliveMarkerVital 0x3DD6` เกี่ยวข้อง -- `RE-112` ปิดไว้ว่าไม่มี call edge ผูกกับ quest 3205
  4. ไม่แตะข้ออ้างของ `GT-106` (จุดลงฉาก 17) และ `GT-106-R2` (เรนเดอร์ฉากกลางเซสชัน) -- ใช้ trigger ใกล้กันแต่คนละคำถาม
  5. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ · เซสชันเดียว ตัวละครเดียว คลิกเดียว

- STOP: **STOP ถ้าไคลเอนต์ปิดตัว** (บันทึกว่าหยุดที่ขั้นไหน แล้ว teardown อยู่ดี) · STOP ถ้าจอวาร์ปไปฉากอื่น -- แปลว่าคลิกโดน option 1 ให้บันทึกตามจริงและจบใบ ห้ามคลิก option 2 ต่อในบูตนั้น · STOP ถ้าเจอ `ErrorData`

- 🔴 หมายเหตุจาก chief (`kj0s6r`/R346): ข้อความไทยจริงของ option 2 บนจอ **ไม่มีใครเคยคัดไว้** -- ในซอร์สเก็บไว้แค่ทับศัพท์ (`COLUMBUS_QUEST_BORNAGAIN_LABEL_TH_TRANSLIT`) โดยตั้งใจ ⇒ ใบนี้จึงชี้ตัวเลือกด้วย **ตำแหน่งบรรทัด** (บรรทัดที่สอง) ไม่ใช่ด้วยข้อความ และขอให้ผู้เทสคัดทั้งสองบรรทัดกลับมา · หน้าต่าง 10 วินาทีและ 5 วินาทีเป็นตัวเลขจากข้อเสนอของใบผล `RE-112` เอง **ไม่ใช่ค่าที่วัดมา**

- links: `CLIENT_RE_QUEUE.md` (`RE-112` ทั้งใบ · objective ข้อ 3 = attended capture ที่แคบที่สุด · `BUILD_IMPACT`) · `notes_to_chief/20260827_1912_RE-112-RESULT-RESETMARKER-NOOP-ACK-BOUNDED.md` · `pirate-force-server/src/pirateforce_foundation/columbus_quest_dispatch.py:268-270,727-767` · `.../runtime.py:6363-6479` · `.../world_scene_travel.py:177` · `GT-106-R2` (เส้นทางคลิกบทสนทนา Columbus ที่เดินถึงจริงแล้ว) · `notes_to_chief/20260905_0106_KA1A-BACKSWEEP-*.md` หมวด ก. ข้อ 3

- result:
  (ว่าง -- ผู้เทสกรอก)

## numbering
`GT-252`/`RE-252` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/`) ก่อนวาง -- ตรวจโดย chief รอบ `kj0s6r`/R346

---

## GT-255 SECOND-PASSWORD-AND-BAG-INBOUND-FRAME-CAPTURE-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — ปิดได้ตามเกณฑ์ 'จับเฟรม' — Event B (เปิดกระเป๋า) ครบสองชั้น · Event A (ตั้ง/เปลี่ยนรหัสรอง) ครบชั้น client→server (server ไม่มี handler ให้วัดฝั่งนั้น) — R320 2026-09-06 §GT-255 · nonclaims: server ยังไม่ตรวจรหัสจริง (V110 ตอบ OK กับค่าทดสอบ) · จาก notes_to_chief/20260906_0155_KA1A-R320-*.md · 🟢 **READY -- เนื้อใบเต็มวางแล้ว** · 🔴 **แต่เจ้าภาพบูตเดิมหายไป -- อ่านบล็อก "เจ้าภาพบูต" ก่อนลงรอบ** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-DB** · ผู้ตั้งเลข/เปิดใบ = chief (LANE-E) รอบ `5e00uw`/R348 ตาม `COO-DECISION 20260905_0347` ข้อ 1 · เนื้อใบวางโดย chief รอบ `r045nx`/R354 ตามคำขอ `notes_to_chief/20260905_1153_LANE-DB-GT255-full-ticket-body-ready-to-paste.md` · ผู้รัน = Panya (attended) · **ลำดับใน "รอเครื่องคุณ" = ท้ายสุด ไม่บล็อกสายใด** · ไม่มีการตีมอน จึงไม่ชนกฎ "ห้ามใบเทสตีมอนจนกว่า P-2 จะปิด"]
> 🔴 **เจ้าภาพบูต (บล็อกนี้เขียนโดย chief รอบ `r045nx`/R354 -- ไม่ใช่ของ LANE-DB · ห้ามลบ)**
> เนื้อใบข้างล่างเขียนไว้ตอน `GT-242` ยังไม่ได้รัน และสั่งให้ "พ่วงบูตเดียวกับ `GT-242` เท่านั้น" ทุกขั้น
> **แต่ `GT-242` PASS ไปแล้วที่ R316 (2026-09-05T11:02+07:00)** ⇒ จะไม่มีบูตของ `GT-242` ให้พ่วงอีก
> ⇒ **อ่านทุกที่ที่เนื้อใบเขียนว่า "`GT-242` ขั้น 3 / ขั้น 5 / ขั้น 7 / ขั้น 8" ว่าหมายถึง "จังหวะที่เทียบเท่าของบูตเจ้าภาพที่ใช้จริงในรอบนั้น"**:
> ขั้น 3/ขั้น 5 = **จังหวะเปิดกระเป๋าสองครั้งใด ๆ ในบูตเจ้าภาพ** (ถ้าบูตเจ้าภาพเปิดกระเป๋าครั้งเดียว ให้เปิดซ้ำอีกครั้งห่างกัน ~30 วินาที แล้วจดเวลาไว้เอง) · ขั้น 7 = NO-CRASH ของบูตเจ้าภาพ · ขั้น 8 = teardown ของบูตเจ้าภาพ
> **เจ้าภาพบูตใหม่ = บูต attended ใดก็ได้ที่ล็อกอินด้วยบัญชีที่เปิดกระเป๋าได้ และไม่มีธง `--*-scenario`** · ยังคงกฎเดิม: **ห้ามบูตเดี่ยวเพื่อใบนี้** · เจ้าภาพ STOP = ใบนี้ STOP ด้วย
> · db/sha/`integrity_check` ที่เนื้อใบบอกว่า "ยืมของ `GT-242`" = ยืมของ**เจ้าภาพจริง** ไม่ใช่ตัวเลขของ R316
> 🔴 **LANE-DB**: ถ้าไม่เห็นด้วยกับการอ่านแบบนี้ ให้แก้เนื้อใบส่งมาเป็นจดหมายรอบถัดไป chief วางทับให้ (เขตเขียนของ `GAME_TEST_QUEUE.md` ยังเป็นของ chief)

> 🔴 **ใบจับเฟรมอย่างเดียว ไม่ใช่ใบตัดสินความหมายฟิลด์** -- ผลของใบนี้คือ opcode + ความยาว + ลำดับดิบของเฟรมขาเข้า ป้อนให้ `RE-239` เท่านั้น การอ่านความหมายฟิลด์เป็นหน้าที่ของ `RE-239` ไม่ใช่ใบนี้
> 🔴 **ห้ามขยายเป็น "ทดสอบรหัสผ่านรองทำงานถูกไหม"** -- ถ้าอยากรู้ว่า MD5 ที่ป้อนถูกตรวจจริงหรือไม่ (ไม่ใช่แค่ bypass เสมอ) ต้องเปิดใบใหม่คนละใบ ไม่ใช่ใบนี้
> 🔴 **พ่วงบูตเดียวกับ `GT-242` เท่านั้น ห้ามบูตแยก** -- ถ้า `GT-242` ต้อง STOP กลางคัน ใบนี้ STOP ด้วยทันที ไม่ใช่เหตุผลให้บูตซ้ำเฉพาะใบนี้ · ไม่มี RECHECK แยกของใบนี้ -- ใช้ RECHECK ของ `GT-242` เป็นเงื่อนไขก่อนบูตร่วม (ถ้า `GT-242` ยัง BLOCKED ใบนี้บูตไม่ได้เช่นกัน)

- objective: ข้ออ้างเดียว -- **จับเฟรมขาเข้าดิบ (opcode + ความยาว + ลำดับ) ของสองเหตุการณ์รหัสผ่านรอง แยกเป็นสองชุดข้อมูลอิสระ**: (A) ตั้ง/เปลี่ยนรหัสผ่านรอง และ (B) เปิดกระเป๋า/คลังด้วยรหัสผ่านรอง -- ใบนี้ไม่ตัดสินว่าทั้งสอง opcode เหมือนหรือต่างกัน แค่รายงานสิ่งที่จับได้จริงแยกต่อเหตุการณ์

- ที่มา (วัดแล้ว ไม่ใช่การเดา):
  1. `notes_to_chief/20260904_1309_LANE-DB-RE-TICKET-second-password-incoming-credential-frame.md` -- ค้นสามแหล่งที่มีอยู่แล้วในสองรีโปครบตามที่ `COO-DECISION 20260904_1150` ข้อ 2 สั่ง: `second_password_bypass.py` มีแค่เฟรม**ขาออก** (`SECOND_PASSWORD_OK_FRAME_SHA256` 44 B, hash-pinned) · `runtime.py:9953-9998` เรียกมันแบบ proactive (server ยิงเองตอน runtime ready + poll ทุก 2 วิ) ไม่มี handler รับ/parse เฟรมขาเข้าเลยในสองรีโป (`grep -rn "second_password"` ยกเว้น `current/pf_login_game_server_v141.py` = 0 hit ของ incoming parser) · `docs/EXPERIMENT_LEDGER.md:20` บันทึกตรง ๆ ว่า "dialog-open emitted no distinct wire request" และแพ็กเก็ตจริงตอน live session "was not retained"
  2. `notes_to_chief/20260904_1434_LANE-DB-REPLY-chief-re239-route-needs-attended-capture.md` -- ด้วยเหตุผลข้อ 1 ป้ายเส้นทางของ `RE-239` คือ `NEEDS-ATTENDED-CAPTURE` (ไม่ใช่ `STATIC-ON-BRIDGE`/`STATIC-ON-CLOUD` เพราะ corpus ไม่เคยมีเฟรมขาเข้าอยู่ในดิสก์ให้ static ขุดเลย) -- ทางเดียวคือเปิดหน้าต่างจริงบนไคลเอนต์ที่มีตัวจับแพ็กเก็ตอยู่แล้วเก็บทั้งสองเส้นทาง
  3. 🔴 **แต่ `GT-242` เอง (`notes_to_chief/20260904_1430_KA1A-R309-RESULTS-*` finding 1, บันทึกเวลา 14:30 -- อยู่ระหว่างจดหมายสองฉบับข้างบน) มีการสังเกตเฟรมขาเข้าครั้งหนึ่งอยู่แล้วโดยบังเอิญ**: `CheckSecondPwdVital 0x4B98 (64 B)` ตามด้วย reply `V110_CHECK_SECOND_PASSWORD_OK` (44 B) เกิดขึ้นตอนเจ้าของบัญชี **เปิดกระเป๋าเฉย ๆ** ในรอบ attended จริง -- นี่คือการสังเกตแบบ passive ครั้งเดียว ไม่เคยถูกดึง hex ดิบมาเป็น exhibit แยกให้ `RE-239` ใช้ และไม่เคยพิสูจน์ว่าเกิดซ้ำได้ ⇒ **ไม่ขัดกับข้อ 1-2**: จดหมายของ LANE-DB พูดถึงโค้ดที่ commit แล้ว/parser ที่มีอยู่ ส่วนการสังเกตนี้เป็นรอบ attended ที่ไม่เคยถูกทำให้เป็นข้อมูลใช้ซ้ำได้ -- นี่คือช่องว่างที่ใบนี้ปิด

- db: **ใช้สำเนาเดียวกับ `GT-242` เท่านั้น** (`state\run_gt242_<stamp>.sqlite3`) -- 🔴 **ห้ามคัดลอกเพิ่ม ห้ามเปิด canonical เอง** เพราะพ่วงบูตเดียวกัน sha256/`PRAGMA integrity_check` ก่อน-หลังคือรายการเดียวกับที่ `GT-242` บันทึกอยู่แล้ว ใบนี้ไม่ทำซ้ำ -- แค่ต้องยืนยันก่อนเริ่มขั้นตอนของใบนี้ว่าตัวเลข sha ที่ `GT-242` รายงานตรงกับ `CANON_SHA.txt`

- server args: **เหมือน `GT-242` ทุกตัวอักษร ไม่มีแฟล็กเพิ่มของใบนี้เลย** -- บูตมาตรฐาน · client `-SecondPasswordMode bypass` (ขีดเดียว = แฟล็กไคลเอนต์) · 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ และห้ามส่ง `--second-password-mode` (สองขีด) ให้เซิร์ฟเวอร์เด็ดขาด** -- ค่าที่ไม่ใช่ `required` ทำให้ `world_census_enabled` เป็นเท็จและสำมะโนดับทั้ง 13 แมพ (กับดัก GT-192 เดิม `notes_to_chief/20260902_1604_LANE-GM-TO-CHIEF-gt192-*`) · เก็บคอนโซลรวม `2>&1` + `capture_v141\GAME_LIVE.txt` + `capture_v141\GAME_EVENTS_LIVE.txt` -- ไฟล์เดียวกับที่ `GT-242` เปิดค้างอยู่แล้ว **ห้ามเปิดไฟล์ใหม่/ปิดแล้วเปิดซ้ำ**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt242_<stamp>.sqlite3
  ```

- steps: (ทำภายในเซสชัน attended เดียวกับ `GT-242` เท่านั้น -- ไม่มีบูตของตัวเอง · เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ ตามที่ `GT-242` ทำไปแล้ว)

  **Event B (เปิดกระเป๋า/คลัง) -- ไม่ต้องกดอะไรเพิ่ม ใช้จังหวะของ `GT-242` เอง:**
  1. ระหว่าง `GT-242` ขั้น 3 (negative control พื้นว่าง, เปิดกระเป๋า) และขั้น 5 (`T0`+30s, เปิดกระเป๋าจริง) -- **ไม่ต้องคลิกอะไรเพิ่ม** ทั้งสองจังหวะนั้นเป็นเหตุการณ์เปิดกระเป๋าที่ใบนี้ต้องการอยู่แล้ว
  2. บันทึกเวลาที่ `GT-242` บันทึกไว้แล้วสำหรับสองจังหวะนี้ (เวลาเปิดกระเป๋าขั้น 3 และ `T0` ของขั้น 5) ไว้ใช้ตัด hex ภายหลัง -- ใบนี้ไม่ได้จดเวลาใหม่ ยืมของ `GT-242`

  **Event A (ตั้ง/เปลี่ยนรหัสผ่านรอง) -- การกระทำใหม่หนึ่งบล็อก แทรกหลัง `GT-242` ขั้น 7 (NO-CRASH camera-drag) และ**ก่อน**ขั้น 8 (ปิดเซิร์ฟเวอร์) เท่านั้น:**
  3. 🔴 **ยืนยันก่อนพิมพ์ตัวเลขใด ๆ ว่ากล่องโต้ตอบรหัสผ่านมี keyboard focus จริง** (เห็นเคอร์เซอร์กะพริบในช่อง) -- ตัวเลขที่พิมพ์ตอนกล่องไม่ focus กลายเป็นฮอตคีย์ของเกม ไม่ใช่ตัวอักษรรหัสผ่าน และจะทำให้การจับเฟรมนี้อ่านไม่ออกว่าเกิดอะไรจริง
  4. หาจุดเข้าของเมนู "ตั้ง/เปลี่ยนรหัสผ่านรอง" -- **จำกัดเวลาค้นหา ~2 นาที** (กันไม่ให้บูตที่พ่วงอยู่ยาวเกิน): จุดที่ควรเช็คก่อนจุดอื่นคือ **ลิงก์/ปุ่มในกล่องโต้ตอบเดียวกับที่เด้งตอนกดกระเป๋า** (`GT-242` ขั้น 3/5) เพราะเกมทั่วไปมักวางปุ่ม "เปลี่ยนรหัสผ่าน" ไว้หน้าเดียวกับหน้ากรอกรหัส -- ถ้าไม่เจอที่นั่น ค่อยไล่เมนูตัวละคร/ระบบ · ภาพนิ่ง `S-A0` เต็มความละเอียดของหน้าจอที่พบจุดเข้า **ก่อน**คลิก
  5. ถ้า**ไม่พบ**จุดเข้าภายในเวลาที่กำหนด: หยุดค้นหา บันทึก `EVENT_A_UI_NOT_FOUND` พร้อมรายชื่อเมนูที่เช็คแล้วทั้งหมด แล้วข้ามไปขั้น 8 ตรง -- นี่คือผลของ Event A ชั้น client-observable แล้ว (ดู pass criteria (6)) ไม่ใช่การรอเทสใหม่
  6. ถ้า**พบ**: จดเวลา `T_A0` (ก่อนคลิกเปิดกล่อง) → คลิกเปิด → ภาพนิ่ง `S-A1` เต็มความละเอียด (เห็นกล่องเต็ม) → พิมพ์ค่าทดสอบคงที่ที่จดไว้ในผล (เลขที่ตกลงล่วงหน้า **ห้ามใช้รหัสผ่านจริงส่วนตัวของผู้เทส**) → จดเวลา `T_A1` (ตอนกดยืนยัน/ส่ง) → ภาพนิ่ง `S-A2` เต็มความละเอียด
  7. NO-CRASH ของบล็อกนี้: **ไม่ต้องทำซ้ำ** -- ใช้ผลคลิกขวาลากกล้องของ `GT-242` ขั้น 7 ร่วมกัน (ใบนี้ไม่มี NO-CRASH check ของตัวเอง)
  8. ส่งต่อให้ `GT-242` ขั้น 8 เป็นต้นไป (ปิดเซิร์ฟเวอร์ เก็บหลักฐาน teardown) -- ใบนี้ไม่ทำซ้ำขั้นเหล่านั้น อ่านหลักฐานชุดเดียวกับที่ `GT-242` เก็บ
  9. ตัด hex ดิบจาก `capture_v141\GAME_LIVE.txt` หน้าต่าง **+/- 5 วินาที** รอบ `T_A0`/`T_A1` (ถ้าถึงขั้น 6) และรอบเวลาเปิดกระเป๋าสองจังหวะของ `GT-242` (ขั้น 3, `T0` ของขั้น 5) -- ทุก opcode ไม่กรองอะไรทิ้ง พร้อม frame index + จำนวนไบต์ต่อเฟรม แยกเป็นสองตารางต่างหาก (Event A / Event B) ห้ามรวมเป็นตารางเดียว
     ```
     findstr /C:"CheckSecondPwdVital" /C:"V110_CHECK_SECOND_PASSWORD_OK" <คอนโซลรวม>
     ```

- pass criteria: 🔴 **สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น** · ครบชั้นเดียว = `🟡 <ชั้นที่ครบ> ... · <ชั้นที่ขาด> = NOT MEASURED · ใบยังไม่ปิด` **ห้ามปั๊ม PASS**

  **wire/DB** (จาก `GAME_LIVE.txt`/คอนโซล -- ไม่ต้องมีตาคน):
  1. **Event A**: ถ้าถึงขั้น 6 -- รายการ opcode + ความยาว + frame index ของทุกเฟรมขาเข้าในหน้าต่าง `T_A0`..`T_A1` +/-5s (ตารางแยก) · ถ้าหยุดที่ขั้น 5 (`EVENT_A_UI_NOT_FOUND`) -- ชั้นนี้ของ Event A คือ **`NO-RESULT: ไม่พบจุดเข้าเมนูภายในเวลาที่กำหนด`** ซึ่ง**นับเป็นผลลบที่มีค่า** ไม่ใช่ FAIL และไม่ใช่ช่องว่าง -- ชี้ทางไปว่าต้องมีใบตามหาเมนูนี้แยกต่างหาก
  2. **Event B**: รายการ opcode + ความยาว + frame index ของทุกเฟรมขาเข้าในหน้าต่างเปิดกระเป๋าทั้งสองจังหวะของ `GT-242` (ขั้น 3 และขั้น 5) -- คำทำนาย (ดูหัวข้อ prediction) คือ `CheckSecondPwdVital 0x4B98` (64 B) ปรากฏซ้ำทั้งสองจังหวะ -- รายงาน**สิ่งที่พบจริง** ไม่ว่าจะตรงคำทำนายหรือไม่ ความไม่ตรงเองก็เป็น finding
  3. เปรียบเทียบชุด opcode ของ Event A (ถ้ามี) กับ Event B แล้วเขียนผลเป็นคำเดียวชัดเจน: `SAME` / `DIFFERENT` / `EVENT-A-EMPTY` -- **ห้ามอนุมานเกินคำนี้** การตัดสินว่ามันหมายถึงอะไรเป็นของ `RE-239`
  4. `integrity_check` = `ok` และ sha canonical ตรง -- ยืมผลของ `GT-242` เอง ไม่รันซ้ำ
  5. 🔴 **ชั้นนี้ตอบไม่ได้เลยว่าหน้าจอที่ผู้เทสกดคือหน้าจอที่ตั้งใจจริงหรือไม่ (เช่น กดถูกเมนู "ตั้งรหัสผ่านรอง" จริงไหม)**

  **client-observable** (ต้องมีตาคน -- ห้ามอนุมานจากคอนโซล):
  6. `S-A0`/`S-A1`/`S-A2` (หรือบันทึก `EVENT_A_UI_NOT_FOUND` พร้อมรายเมนูที่เช็ค ถ้าไม่พบ) -- Panya เขียนด้วยคำพูดธรรมดาว่าหน้าจอที่เห็นคือหน้าอะไร ไม่ใช่แค่แปะภาพ
  7. `S-B1`/`S-B2`/`S-B3` = ยืมภาพ `S1`/`S2`/`S3` ของ `GT-242` เอง (คนละหน้าเดียวกัน) -- Panya ยืนยันว่าเป็นแผงกระเป๋า/คลังจริง ไม่ใช่หน้าจออื่น
  8. ไม่มีอาการค้าง/หลุด/`ErrorData` ตลอดบล็อก Event A ทั้งหมด
  9. **บันทึกสีป้ายชื่อทุกป้ายในเฟรมของภาพที่ใบนี้ยกมาเอง** (`S-A0`, `S-A1`, `S-A2` ถ้ามี) หนึ่งบรรทัดต่อป้ายต่อภาพ · ไม่มีป้ายเขียน `none` ห้ามเว้นว่าง · อ่านจาก**ภาพนิ่งเต็มความละเอียดเท่านั้น** · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น) · ส่วนภาพ `S-B*` สีป้ายถูกบันทึกอยู่แล้วในผลของ `GT-242` เอง (10) ไม่ต้องทำซ้ำ
  🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <ISO+07:00>` เท่านั้น (`G-OBS`) -- หลักฐานครบแต่ไม่มีลายเซ็นคน = `AWAITING-OBSERVER` ไม่ใช่ PASS ไม่ใช่ FAIL

- prediction (**คำทำนาย ไม่ใช่ผลวัด** -- ทำนายผิด = finding ไม่ใช่ความล้มเหลว):
  P1: Event B แสดง `CheckSecondPwdVital 0x4B98` (64 B) ซ้ำทั้งสองจังหวะ ตรงกับการสังเกตครั้งเดียวใน R309/KA1A -- ถ้าไม่ตรง (opcode/ความยาวต่าง) นั่นคือ finding ว่าการสังเกตเดิม**ไม่ทั่วไป**
  P2: opcode ของ Event A ไม่ทราบล่วงหน้า -- ทำนายว่า **ไม่น่าจะ**เหมือน Event B ไบต์ต่อไบต์ (ตั้งกับตรวจเป็นคนละการกระทำ) แต่ก็เปิดทางว่าอาจใช้เฟรมตระกูลเดียวกันพร้อมฟิลด์โหมดแยก -- ผลด้านใดก็มีค่าให้ `RE-239` เท่ากัน
  P3: ภายใต้ `-SecondPasswordMode bypass` มีโอกาสจริงที่**เมนูตั้ง/เปลี่ยนรหัสผ่านรองเข้าไม่ถึงเลยในบูตนี้** (bypass อาจกระทบแค่คำตอบของเซิร์ฟเวอร์ ไม่ใช่การเปิดใช้เมนูฝั่งไคลเอนต์ -- ไม่มีใครวัดมาก่อน) -- ถ้าขั้น 5 เกิดขึ้นจริง (`EVENT_A_UI_NOT_FOUND`) **นี่ไม่ใช่ความล้มเหลวของใบนี้** แต่เป็นผลลบที่ชี้ทาง: ต้องมีใบถัดไปลองจับภายใต้บูตที่เซิร์ฟเวอร์บังคับ `second_password_mode=required` ซึ่ง**อยู่นอกขอบเขตใบนี้**เพราะ `server args` ของใบนี้ (ยืมจาก `GT-242`) ห้ามส่งแฟล็กนั้นให้เซิร์ฟเวอร์เด็ดขาด

- nonclaims:
  ① ไม่ตัดสินความหมาย/โครงฟิลด์ของเฟรมใดที่จับได้ (`RE-239` เท่านั้น)
  ② ไม่พิสูจน์ว่ารหัสผ่านรองที่ป้อนใช้งานได้จริงภายหลัง (คนละใบ นอกขอบเขตตามคำถามแคบที่ COO อนุมัติ)
  ③ ไม่ยืนยันว่า Event A กับ Event B ใช้ opcode เดียวกันหรือต่างกัน -- รายงานแค่สิ่งที่พบ
  ④ ไม่ขยาย/ไม่แตะเกณฑ์หรือขั้นตอนของ `GT-242` -- พ่วงบูตเฉย ๆ ถ้า `GT-242` ต้อง STOP ใบนี้ STOP ด้วย ไม่ใช่เหตุผลให้บูตเพิ่ม
  ⑤ `NO-RESULT` บน Event A (หาเมนูไม่พบ) ไม่ได้แปลว่าเมนูนั้นไม่มีอยู่จริง -- แค่ไม่พบภายในการค้นที่จำกัดเวลาของรอบนี้
  ⑥ ไม่แตะ canonical DB (บูตบนสำเนาของ `GT-242` เท่านั้น)
  ⑦ ไม่ตัดสินสาเหตุสีป้าย (`RE-067`)

- links: `GT-242` (บูต/เซสชันร่วม, ต้นทางการสังเกต Event B ครั้งแรก) · `RE-239` (ผู้บริโภคผลลัพธ์ดิบของใบนี้) · `notes_to_chief/20260904_1309_LANE-DB-RE-TICKET-second-password-incoming-credential-frame.md` · `notes_to_chief/20260904_1434_LANE-DB-REPLY-chief-re239-route-needs-attended-capture.md` · `notes_to_chief/20260904_1430_KA1A-R309-RESULTS-*` finding 1 · `docs/EXPERIMENT_LEDGER.md:20` · `src/pirateforce_foundation/second_password_bypass.py` · `runtime.py:9953-9998`

- numbering: `GT-255`/`RE-255` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง -- ตรวจโดย chief รอบ `5e00uw`/R348 · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `254` ก่อนวางใบนี้ ⇒ ใบนี้ `255`

- result: (ผู้รันกรอก: Event A -- ตารางเฟรมดิบหรือ `EVENT_A_UI_NOT_FOUND` + รายเมนูที่เช็ค · Event B -- ตารางเฟรมดิบสองจังหวะ · คำตัดสิน `SAME`/`DIFFERENT`/`EVENT-A-EMPTY` · ภาพ `S-A0`-`S-A2` (ถ้ามี) พร้อมสีป้ายครบทุกภาพ · sha256 + integrity_check (อ้างอิงของ `GT-242`) · commit ที่บูต · `OBSERVER_CONFIRMED: <ISO+07:00>`)

**STOP:** ไคลเอนต์ปิดตัว / `ErrorData` ใด ๆ ที่จุดไหนของบล็อก Event A -> หยุดทันที บันทึกสิ่งที่กดล่าสุด -- นี่หยุด `GT-242` ทั้งเซสชันด้วยเพราะพ่วงบูตเดียวกัน ต้องรายงานเข้าไปในผลของ `GT-242` เองด้วย ไม่ใช่แค่ใบนี้

**ผู้เปิดใบ: chief (LANE-E) รอบ `5e00uw`/R348 ตาม `COO-DECISION 20260905_0347` ข้อ 1 -- ผู้บริโภคผล: LANE-DB (ส่งวัตถุดิบต่อให้ `RE-239`)**

## numbering
`GT-255`/`RE-255` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง -- ตรวจโดย chief รอบ `5e00uw`/R348 · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `254` ก่อนวางใบนี้ ⇒ ใบนี้ `255`

---

## GT-257 CHAT-TWO-VITAL-TAIL-ONE-TYPING-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS 3/3 — กด M เปิด/ปิดแล้ว /warp ทันที ไม่พบ two-vital ในบูตนี้ (สมมติฐาน 'จะเห็น vital ที่สอง' ผลคือไม่เห็น) — R320 2026-09-06 §GT-257 · จาก notes_to_chief/20260906_0155_KA1A-R320-*.md · 🟢 **READY** -- บูตได้ทันที **แต่ไม่ต้องบูตเดี่ยว: พ่วงบูตอื่นได้**
> 🔴 **เงื่อนไขกระตุ้นที่ผู้เทสต้องทำ (เติมโดย chief (LANE-E) รอบ `r045nx`/R354 ตาม `COO-DECISION 20260905_1349` ข้อ 3)**: พิมพ์คำสั่งแชท **ทันที**หลังเข้าแมพ ขณะไคลเอนต์ยัง flush `UserSetting` อยู่ ไม่งั้นเฟรมมาเป็น vital เดี่ยวและ**ไม่ exercise ใบนี้เลย** -- R318 วัดแล้ว (§5): `/warp 126` ตอน 12:25:31 พิมพ์หลังอยู่ในแมพนานแล้ว ได้เฟรมเดี่ยว 48 ไบต์ · `TAIL_UNDECLARED_BODY`=0 · `LANE_GM_CHAT_TAIL`=0 ⇒ รอบนั้น**ไม่ได้เดินใบนี้** แม้จะพิมพ์คำสั่งจริง (ที่มาของเงื่อนไข: R313 เห็นหางสองไวทัลตอนพิมพ์ทันทีหลังเข้าแมพ) · ไม่บล็อกสายใด · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · ผู้ตั้งเลข/เปิดใบ = chief (LANE-E) รอบ `pv4zg1`/R352 ตาม `COO-DECISION 20260905_0947` ข้อ 3 ("ใบขอเลข GT ของ GM `20260905_0426` ค้าง 5 ชม. ผ่านมาสองรอบ -- ไม่รับค้างต่อ") และ "ใครทำอะไรต่อ" ข้อ (2) ของใบเดียวกัน · ผู้รัน = Panya (attended) ~3 นาทีบนจอ · **ลำดับ: ท้ายคิว `รอเครื่องคุณ` พ่วงกับบูตใดก็ได้ที่ล็อกอินด้วยบัญชี GM อยู่แล้ว** · **ไม่มีการตีมอน** จึงไม่ชนกฎ "ห้ามใบเทสตีมอนจนกว่า P-2 จะปิด"]

- precondition ของใบ (จ่ายแล้ว): จดหมาย `20260905_0426` เขียนเงื่อนไขตัวเองว่า "PR รอบ `ff30oi` ขึ้น main แล้ว"
  **[วัดแล้ว chief (LANE-E) รอบ `pv4zg1` 2026-09-05T11:2x+07:00 บน clone ของเซิร์ฟเวอร์เอง]**:
  `git grep -n "TAIL_UNDECLARED_BODY" origin/main -- src/pirateforce_foundation/gm/chat_frame_tail.py` = **เจอ 3 บรรทัด** (`:48` `:156` `:159` · นิยามจริงอยู่ที่ `:156`)
  **[วัดแล้ว บนสะพาน · แหล่งที่สองที่ไม่ใช่จดหมายต้นเรื่อง]** `rounds/GM_20260905_0558_ht6qwv_*.md:28-29` = `#792` merged บน main (`bdd1938`)
  ⇒ เงื่อนไขของใบจ่ายครบสองแหล่งที่เป็นอิสระต่อกัน (กราฟ git + ไฟล์รอบของ LANE-GM) · **ด่านก่อนบูตข้อ 0 ยังต้องรันอยู่ดี** เพราะมันวัด commit ที่จะบูตจริง ไม่ใช่ main เมื่อชั่วโมงก่อน

- objective (ข้ออ้างเดียว): บนบิลด์ที่มี `TAIL_UNDECLARED_BODY` แล้ว เมื่อไคลเอนต์ส่ง **เฟรมแชทที่มี vital ที่สองพ่วงมาในเฟรมเดียวกัน** (`0x0F01` `UserSetting_UpdateServerSettingVital` ที่ยิงทุกครั้งที่เปิด/ปิดหน้าต่าง UI ตาม R313 §3) คำสั่ง GM ในเฟรมนั้น **ทำงานจากการพิมพ์ครั้งเดียว** ไม่ใช่ครั้งที่สอง -- นี่คือชั้นบนจอของบั๊ก R313 §3 ที่ปิดฝั่งเซิร์ฟเวอร์ไปแล้วรอบ `ff30oi` ใบนี้**ไม่**ตัดสินความหมายของฟิลด์ใน `0x0F01` และ**ไม่**ประกาศความยาว body ของมัน

- db (สำเนาเสมอ ห้ามเปิด canonical):
  - **พ่วงบูต (ทางหลัก)**: ใช้ไฟล์ run-copy ของบูตเจ้าภาพที่เปิดอยู่แล้ว **ห้ามคัดลอก DB ใหม่กลางบูต**
  - **ถ้ารันเดี่ยว**:
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-257_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt257_<yyyyMMdd_HHmmss>.sqlite3
```
  sha256 canonical ต้องตรง `CANON_SHA.txt` ทั้งก่อนและหลัง · `PRAGMA integrity_check = ok` ทั้งสองครั้ง
  🔴 ชื่อสำเนา **ห้ามเป็น** `pirateforce.sqlite3` และ **ห้ามมี `~`** ไม่งั้นเกต `_speed_db_is_canonical` (`gm/chat_command_action.py`) กันคำสั่ง GM ทิ้งทั้งใบ [วัดแล้ว · `GAME_TEST_QUEUE.md:12122`]
  รอบคัดลอก DB ⇒ ตัวละครกลับจุดเกิดทุกบูต = ปกติ ไม่ใช่ผลวัด

- server args (บูตมาตรฐาน **ไม่มีแฟล็ก scenario ใด ๆ**):
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
git grep -n "TAIL_UNDECLARED_BODY" <SHA> -- src/pirateforce_foundation/gm/chat_frame_tail.py
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gt257_<stamp>.sqlite3 2>&1
```
  บัญชีที่ล็อกอินต้องอยู่ใน `config/gm_accounts.json` (หรือสำเนาที่ `PF_GM_ACCOUNTS_CONFIG` ชี้ไป -- **ห้ามแก้ไฟล์จริง**) · เก็บ stdout+stderr รวมกัน (`2>&1`) เพราะโทเคนเลนนี้ออกทาง **stderr** ล้วน [วัดแล้ว · `GAME_TEST_QUEUE.md:12125`]

- steps (~3 นาที · playbook `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่อง):
  0. **ด่านก่อนบูต**: คำสั่ง `git grep` ข้างบนต้องได้ **อย่างน้อย 1 บรรทัด** · ไม่ได้ = `[BLOCKED]` ห้ามบูต ห้ามเรียกผู้เทส · ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical
  1. **เซิร์ฟเวอร์ก่อนไคลเอนต์เสมอ** (พอร์ต 10188/10189 ต้องว่างก่อน) แล้วเข้าเกม (ปุ่มกลางของ 5 ปุ่มล่าง · ห้ามปุ่มซ้ายสุด = ลบตัวละคร) · ยืนยันจากคอนโซลว่าบัญชีนี้เป็น GM จริง
  2. **T0** -- ยืนนิ่ง ถ่าย `S0-BEFORE` เต็มความละเอียด · จดฉากที่ยืน + พิกัด HUD + **ทุกป้ายชื่อในเฟรม บรรทัดละหนึ่งป้าย** (ไม่มี = เขียน "none" ห้ามเว้นว่าง)
  3. NO-CRASH check: **คลิกขวาค้างลาก** หนึ่งครั้ง (กล้องอย่างเดียว · ทิศทางตัวละครไม่ขยับ · ไม่มีไบต์ออกสาย ปลอดภัยทุกจังหวะ) · 🔴 **ห้ามใช้ `Q`/`E` เป็น NO-CRASH check** -- สองปุ่มนั้นหัน**ตัวละคร**จริงและยิง `TargetPosVital`
  4. **ขั้นวัด (ครั้งที่ 1)** -- กด `M` เปิดหน้าต่างแผนที่ แล้วกดปิดทันที (ไคลเอนต์ยิง `UserSetting_UpdateServerSettingVital` ทุกครั้งที่เปิด/ปิด ตาม R313 §3) → คลิกช่องแชท **ยืนยันด้วยตาว่าเคอร์เซอร์อยู่ในช่องจริง** → พิมพ์ `/warp 2` แล้ว Enter **ทันที ห้ามรอ 5 วินาที** · จดเวลานาฬิกา `T_TYPE_1` (HH:MM:SS+07:00)
     🔴 `/warp 2` เป็น **คำสั่ง GM ยาว 7 ตัวอักษร ไม่ใช่ทริกเกอร์แชท 12 ตัวอักษร** -- **ห้ามเติมอักษรให้ครบ 12** และ **ห้ามพิมพ์อักษรใดขณะช่องแชทไม่โฟกัส** (ตัวอักษรจะกลายเป็นฮอตคีย์)
  5. **ห้ามแตะอะไร 5 วินาที** จ้องจอ · ถ่าย `S1-AFTER-1` ภายใน ~3 วิ · บันทึกตรง ๆ ว่าฉากเปลี่ยนหรือไม่ (และถ้าไม่เปลี่ยน มีข้อความอะไรขึ้นบ้าง คัดตามตัวอักษร)
  6. **ถ้าจอยังไม่ขยับ** -- พิมพ์ `/warp 2` **ซ้ำครั้งที่สอง** จด `T_TYPE_2` ถ่าย `S2-AFTER-2` (การพิมพ์ซ้ำครั้งนี้ **คือหลักฐานของ FAIL** ไม่ใช่การกู้รอบ ห้ามข้ามไม่บันทึก)
  7. **ทำซ้ำได้ไม่เกิน 3 ครั้งในบูตเดียวกัน** โดยสลับปลายทางเพื่อไม่ให้คำสั่งซ้ำฉากเดิม: ครั้งที่ 2 ใช้ `/warp 1` (Port Royal = `HOME_SCENE_ID`) ครั้งที่ 3 ใช้ `/warp 2` · ทุกครั้งต้องเปิด/ปิดหน้าต่างก่อนพิมพ์เสมอ · ถ่าย `S3-*` ตามลำดับ + จดป้ายทุกภาพ
  8. NO-CRASH check อีกครั้ง (คลิกขวาค้างลาก) · logout → teardown ด้วย `TEMPLATE_teardown_generic.ps1` (**boot stamp ต้องไม่เกิน 420 นาที** · รอบที่จบเพราะเลิกเล่นก็ต้อง teardown) → เทียบ sha canonical → sha256 ทุกภาพ
  9. คัดดิบ ห้ามตีความ:
```
findstr /N /C:"LANE_GM_CHAT_TAIL" /C:"LANE_GM_CHAT_ACTION" /C:"GM_CHAT_STAGED" /C:"GM_CHAT_NO_BYTES_SENT" /C:"GM_CHAT_WARP_REFUSED" server_console_live.*.txt
```

- pass criteria (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**):
    wire/DB (พิสูจน์ headless ได้ ไม่ต้องมีตาคน):
      W1. คอนโซลมีบรรทัด `LANE_GM_CHAT_TAIL reason=tail_undeclared_body tail_vitals>=1 ids=0x0F01 chat_bytes=<n>` **และ** `LANE_GM_CHAT_ACTION warp` **จากการพิมพ์ครั้งเดียวกัน** (เทียบเวลากับ `T_TYPE_1`)
          หมายเหตุการอ่านบรรทัด (ไม่ใช่การผ่อนเกณฑ์): `tail_vitals>=1` หมายถึง **ฟิลด์ `tail_vitals` มีค่าตั้งแต่ 1 ขึ้นไป** ไม่ใช่ข้อความ `>=` ตามตัวอักษร · บรรทัดจริงอาจมีฟิลด์ต่อท้ายเพิ่ม เช่น `payload_bytes=<n>` [วัดแล้ว · คอนโซลจริงของ R313 พิมพ์ `payload_bytes=151`] และบรรทัด action จริงเคยพิมพ์เต็มว่า `LANE_GM_CHAT_ACTION warp route=action` [วัดแล้ว · `GAME_TEST_QUEUE.md:6226-6228`] ⇒ **จับคู่ที่ชื่อฟิลด์ ไม่ใช่ทั้งบรรทัดตรงตัว** · คัดบรรทัดดิบทั้งบรรทัดลงผลใบเสมอ
      W2. **ไม่มี** `GM_CHAT_NO_BYTES_SENT ... command=warp why=...` และ **ไม่มี** `GM_CHAT_WARP_REFUSED` ในช่วงเดียวกัน (มี = คัดดิบ แล้วดูกล่องอ่านผลด้านล่าง)
      W3. `character_positions.scene_id` ของตัวละครทดสอบในสำเนา DB = ฉากปลายทางของ **การพิมพ์ครั้งแรก** · `sessions` +1 แถวต่อการล็อกอิน · `lease_generation` ไม่ถอยหลัง · `integrity_check = ok` สองครั้ง · sha canonical ก่อน=หลัง · ไม่มี traceback
      🔴 **ชั้นนี้ตอบไม่ได้ว่าตัวละครย้ายฉากบนจอจริงหรือไม่** -- ห้ามใช้แทนชั้นล่าง
    client-observable (🔴 ต้องมีคนนั่งหน้าจอ ห้ามอนุมานจากคอนโซล):
      C1. **ตัวละครย้ายฉาก (หรือขึ้นสถานะ staged ตามปลายทาง) จากการพิมพ์ครั้งเดียว ไม่ใช่ครั้งที่สอง** -- เขียนเป็นตาราง: ครั้งที่พิมพ์ / เวลา / จอเปลี่ยนหรือไม่ / ข้อความบนจอคัดตามตัวอักษร
      C2. **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** (ข้อบังคับ R163 คำสั่ง Panya 2026-08-25): หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ · "none" เขียนออกมา ไม่เว้นว่าง · อ่านสีจาก **ภาพนิ่งเต็มความละเอียด** เท่านั้น ห้ามอ่านจาก contact sheet / ภาพย่อ / วิดีโอ · **ผู้เทสจดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (สาเหตุคือทั้งใบของ `RE-067`)
      C3. ต่างจากภาพเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ
      C4. NO-CRASH check ผ่านทั้งสองครั้ง
      **ไม่มี `OBSERVER_CONFIRMED: <ISO+07:00>` = ชั้นนี้ยังไม่ PASS** ไม่ว่าคอนโซลจะสวยแค่ไหน (G-OBS) · รันจบแต่ยังไม่มีลายเซ็นตาคน = `AWAITING-OBSERVER` ไม่ใช่ PASS ไม่ใช่ FAIL
    การอ่านผล (เก็บสองชั้นแยกกันก่อน แล้วค่อยตัดสิน · นิยามตามจดหมาย `20260905_0426` ตรงตัว):
      **PASS** = ครั้งเดียวติด (W1 ครบสองบรรทัดจากการพิมพ์ครั้งเดียว **และ** C1 = จอย้ายฉากจากการพิมพ์ครั้งนั้น)
      **FAIL** = ยังต้องพิมพ์ซ้ำ (จอขยับจากการพิมพ์ครั้งที่สอง หรือไม่ขยับเลย)
      **NOT-EXERCISED** = **ไม่มีบรรทัด `LANE_GM_CHAT_TAIL` เลย** แปลว่าเฟรมที่ส่งเป็น vital เดี่ยว ไม่ใช่เฟรมพ่วง ⇒ ใบยังไม่ถูกทดสอบ ต้องบูตใหม่ให้เฟรมพ่วงกันจริง (ไม่ใช่ FAIL ไม่ใช่ NO-RESULT) · **ห้ามเปิดบูตเดี่ยวเพื่อไล่ให้เจอ** -- พ่วงบูตหน้าแทน
      🔴 **ผลลบมีค่าเท่าผลบวก**: FAIL = บั๊ก R313 §3 ยังไม่ปิดบนจอ ⇒ redirect กลับไปที่ `gm/chat_frame_tail.py` ฝั่งเซิร์ฟเวอร์ (เจ้าของ = LANE-GM) พร้อมไบต์เฟรมจริงของรอบนี้ ไม่ใช่ให้ผู้เทสรันซ้ำแบบเดา

- predictions (คำทำนายคือคำทำนาย · ทายผิด = finding ไม่ใช่ความล้มเหลว):
  - P1 [เสนอ · หัวใจของใบ]: PASS -- ครั้งเดียวติด เพราะ `TAIL_UNDECLARED_BODY` เก็บ body ไว้แล้วเมื่อ prefix ถูกรับครบทุกไบต์
  - P2 [เสนอ]: บรรทัด `LANE_GM_CHAT_TAIL` จะมี `ids=0x0F01` ตัวเดียว และ `tail_vitals=1`
  - P3 [ตัวหักล้าง]: เห็น `LANE_GM_CHAT_TAIL` แต่ไม่มี `LANE_GM_CHAT_ACTION warp` ตามมา ⇒ ขอบเขต body ถูกเก็บแล้วแต่ตัวส่งต่อยังทิ้ง = finding ใหม่คนละจุดกับที่ `ff30oi` แก้

- ผลพ่วงถ้า PASS (ไม่ใช่เกณฑ์ผ่าน · เจ้าของ = LANE-GM): บรรทัด "ผู้เทสควรรอ ~5 วิหลังเข้าแมพก่อนพิมพ์คำสั่ง GM" ในหมวด "บทเรียนเครื่องมือ" ของ R313 **ถอนได้เมื่อใบนี้ PASS** · ก่อนหน้านั้นยังคงไว้

- nonclaims:
  1. ไม่ตัดสินความหมายของฟิลด์ใด ๆ ใน `0x0F01` และไม่ประกาศความยาว body ของมัน
  2. ไม่พิสูจน์ว่าคำสั่ง GM อื่น (`/say` `/speed` `/lv` `/item`) รอดเงื่อนไขเดียวกัน -- วัด `/warp` อย่างเดียว
  3. ไม่ปิด ไม่ทวง `CORE-REQUEST-GM-057` และไม่แตะคำถาม thread/lock ของ `send_lock`
  4. ไม่พิสูจน์อะไรที่ต้องรอดข้าม relog (บูตบนสำเนา DB)
  5. ไม่ตัดสินสาเหตุของสีป้ายใด ๆ (`RE-067`) · ไม่แตะเกณฑ์ของใบเจ้าภาพที่พ่วงบูตอยู่ (ถ้าใบเจ้าภาพต้องหยุด ใบนี้หยุดด้วย ไม่ใช่เหตุผลให้บูตเพิ่ม)
  6. ไม่มีการตีมอน

- STOP: **STOP ถ้าไคลเอนต์ปิดตัว** -- หยุด บันทึกว่าหยุดที่ขั้นไหน แล้ว teardown อยู่ดี · 🔴 ถ้าไคลเอนต์ตายแล้วต้องเปิดใหม่ **ต้องรีสตาร์ตเซิร์ฟเวอร์ก่อนเสมอ** (เซิร์ฟเวอร์ยังถือเซสชันเดิม ไคลเอนต์ตัวถัดไปจะค้าง "connecting" ตลอดกาล) · STOP ถ้าเจอ `ErrorData` ใด ๆ ที่ไม่เกี่ยวกับใบนี้ -- จดค่าที่ส่งล่าสุดก่อนหยุด

- links: `notes_to_chief/20260905_0426_LANE-GM-TO-CHIEF-r313-chat-2vital-closed-need-gt-number.md` (ใบต้นเรื่อง · เกณฑ์สองชั้นฉบับผู้เขียน) · `notes_to_chief/20260905_0212_KA1A-R313-RESULTS-*.md` §3 (ไบต์จริงของเฟรม #8 171 ไบต์) · `rounds/GM_20260905_0411_ff30oi_*.md:58-101` (ตัวแก้ · เหตุ · เทส `R313CapturedFrameTests`) · `rounds/GM_20260905_0558_ht6qwv_*.md:28-29` (`#792` merged บน main `bdd1938`) · `notes_to_chief/20260905_0947_COO-DECISION-*.md` ข้อ 3 · `src/pirateforce_foundation/gm/chat_frame_tail.py` · `GAME_TEST_QUEUE.md:6226-6228` (ตารางอ่านโทเคน `LANE_GM_CHAT_ACTION`) · `ATTENDED_SESSION_RUNBOOK.md` + `BRIDGE_BOOT_PROCEDURE.md`

- result:
  (ว่าง -- ผู้เทสกรอก **แยกสองชั้น · ชั้นไหนไม่ได้วัดเขียน `NOT MEASURED`**: PASS / FAIL / NOT-EXERCISED / AWAITING-OBSERVER · branch+commit ที่บูต · `T0` · `T_TYPE_*` ทุกครั้ง · บรรทัดคอนโซลดิบทุกบรรทัดจาก `findstr` · `scene_id` ก่อน/หลัง · ภาพ `S0`-`S3` + sha256 · **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** · sha canonical ก่อน/หลัง · `integrity_check` · NO-CRASH/CRASH · teardown รันแล้ว · `OBSERVER_CONFIRMED`)

## numbering
`GT-257`/`RE-257` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง **[วัดแล้ว รอบนี้]** · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `256` (`RE-256`) ⇒ ใบนี้ `257` · ตรวจโดย chief (LANE-E) รอบ `pv4zg1`/R352

---

## GT-269 GMUI-P3-WINDOW-ROW-CENSUS-LABELS-001  [🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — PASS-CLIENT (GMUI 3 แท็บ 7/5/5 แถวตรง census · ต้องมี GameMaster.dll ติดถาวรข้าง client — P0 ใหม่) — R321 2026-09-06 §5 · RESULT: GT-269 PASS-CLIENT R321 2026-09-06 12:4x (P0 GameMaster.dll added) · จาก notes_to_chief/20260906_1255_KA1A-R321-*.md · 🟢 **READY -- attended, in-game** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · เลขตั้งโดย chief (LANE-E) รอบ `siynev`/R361 · เนื้อใบลงไฟล์โดย chief รอบ `6z131u`/R362 คำต่อคำจากจดหมาย `notes_to_chief/20260905_2225_LANE-GM-TO-CHIEF-p3-denominator-17-rows-attended-block-for-labels.md` · **ไม่แตะเซิร์ฟเวอร์เลย** ขึ้นรถบัส capture คันเดียวกับ `GT-233`/`GT-266` ได้]

**คำถามของใบ**: ป้าย (label) ของทั้ง **17 แถวฟังก์ชัน** ใน GMUI สามหน้า (7/5/5) อ่านว่าอะไร — และช่องว่างสูงหนึ่งแถวระหว่างแถว 5 กับ 6 ของหน้า 1 มีวิดเจ็ตซ่อนอยู่หรือไม่

**ทำไมใบเดียวไม่ใช่ 17 ใบ** (LANE-GM `2225`): แตกเป็นใบละแถวจะกินเวลาเครื่อง Panya 17 ครั้งเพื่อข้อมูลที่ภาพเดียวตอบได้ · และตราบใดที่ป้ายยังไม่ครบ สายนี้ยังไม่รู้ว่าแถวไหนควรทำก่อน ⇒ ป้ายทั้ง 17 คือ **input เดียว** ของการจัดคิว P-3

**สถานะที่วัดแล้วก่อนใบนี้** (LANE-GM รอบ `y1evqj`, จากภาพถ่าย client จริงที่ commit ไว้ตั้งแต่ 2026-09-02 · sha256 หมุดใน `gm/gmui_catalog.ROW_CENSUS_SCREENSHOTS`): หน้า 1 = 7 แถว · หน้า 2 = 5 · หน้า 3 = 5 · `gmui_catalog.progress()` = `(0, 17)` · `total_is_unknown()` = False · แต่ **15 แถวเป็น `UNREAD`** และ 2 แถวเป็น `LATIN_PARTIAL` (ขึ้นต้น `NPC` หน้า 1 แถว 3 · `BUFF` หน้า 3 แถว 2)

ATTENDED: เปิด GMUI ด้วยปุ่ม GM (บูตปกติ ไม่ต้องมีธง) แล้วถ่ายทีละแท็บ 1-2-3 ที่ 1656x1000
ATTENDED: แต่ละแท็บ: อ่านป้ายของทุกแถวที่มี radio หน้าซ้าย พิมพ์ตามที่เห็นเรียงบนลงล่าง
ATTENDED: หน้า 1 เพิ่มหนึ่งข้อ: ระหว่างแถวที่ 5 กับ 6 มีช่องว่างสูงเท่าหนึ่งแถว - มีอะไรอยู่ตรงนั้นไหม
ATTENDED: ผ่าน = ได้ป้ายครบ 17 แถว (7/5/5) และตอบช่องว่างหน้า 1 ได้ว่ามี/ไม่มีวิดเจ็ต
ATTENDED: ไม่ผ่าน = จำนวนแถวที่เห็นบนจอไม่ใช่ 7/5/5 (แปลว่า census ผิด ให้รายงานจำนวนจริง)

**เกณฑ์ผ่านสองชั้น** (กฎบ้าน: client-observable กับ wire/DB ห้ามอ้างข้ามชั้น)
- **ชั้น client-observable**: ป้ายครบ 17 แถวตามที่ตาเห็นบนจอ + คำตอบเรื่องช่องว่างหน้า 1 (`OBSERVER_CONFIRMED` + เวลา)
- **ชั้น wire/DB**: ใบนี้ **ไม่มีชั้นนี้โดยเจตนา** — ไม่มีเฟรมออกสาย ไม่มีแถว DB ที่เปลี่ยน · ผลของใบนี้เข้าไปที่ `gmui_widget_census.tsv` (ข้อมูลนิ่ง) เท่านั้น ⇒ **ห้ามอ่านผลใบนี้เป็นหลักฐานว่าปุ่มไหนทำงาน**

**nonclaims (จาก `2225` คำต่อคำ)**: ไม่อ้างว่ามีปุ่มไหนทำงาน (`progress()` = ศูนย์จาก 17) · **ไม่อ้างว่า 17 คือทั้งหมด** (ช่องว่าง ~80px หน้า 1 อาจมีวิดเจ็ตที่ layout มีแต่ไม่ถูกวาด · `total_is_confirmed_on_screen()` = False จนกว่าจะมีคนดูจอ) · ไม่อ้างว่ารู้ว่าแถวไหนส่ง opcode อะไร (opcode = `None` ทั้ง 17 ภาพถ่ายบอกเรื่องนี้ไม่ได้) · ไม่มีบัญชีไหนได้สถานะ GM จากรอบที่วัด census

**ถ้าผลลบ**: จำนวนแถวจริงบนจอ != 7/5/5 = census ผิด ให้รายงานจำนวนจริงกลับมา (LANE-GM แก้ `gmui_widget_census.tsv` + หมุด sha256 ในรอบของตัวเอง) — **ผลลบแบบนี้เป็นผลที่มีค่า ไม่ใช่ใบล้ม**

> 🔴 **ห้ามสายอื่นใช้เลข `GT-269`** · numbering: `GT-269`/`RE-269` = 0 hit ทั้งสามที่ ตอนที่ R361 ตั้งเลข · chief รอบ `6z131u` วัดซ้ำก่อนวางเนื้อใบ: คำสั่งนับเลขของบ้านคืน 267 (เลข 268/269 ยังไม่ลงไฟล์ ตามข้อ ① ห้ามจองล่วงหน้า) และ `GT-268` ยังเป็นของ LANE-A ตามที่ประกาศใน `FROM_CHIEF_R361_TO_ALL_20260906_0040.md`


## GT-218 SPEED-SAFE-VALUE-400-DRY-RUN-CLIENT-SURVIVES-001  [**CLOSED** -- ❌ **FAIL · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00**
🔴 **คำ `CLOSED` เติมโดย LANE-GM (สายที่ถือผลใบนี้) รอบ `83wujr` 2026-09-06T07:2x+07:00 ตาม `FROM_CHIEF_R364` ข้อ 2 -- ไม่ใช่การเปลี่ยนผล** เหตุผลสองข้อ ตรวจได้เอง: (ก) ใบนี้ **ถูกบูตและเกรดจบไปแล้ว** (FAIL + `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00` โดย chief รอบ `pk14rf`/R326) ⇒ ไม่มีอะไรให้บูตอีก การเติมบล็อก `ATTENDED:` จะพาใบที่ตัดสินแล้วขึ้นรถบัส capture ของเจ้าของโดยไม่มีคำถามค้าง (`FROM_CHIEF_R364` ข้อ 2 สั่งเองว่า "ใบที่ตอบไปแล้วให้ปิด แทนการเติมบล็อก") (ข) ที่ `pf_queue_status.py` รายงานใบนี้ว่า "พร้อมบูต" คือ **รูของ regex ไม่ใช่สถานะจริง**: `FAIL` ไม่อยู่ในรายการโทเคนของ `STATUS` (`tools_bridge/pf_queue_status.py:19`) ⇒ ตัวจับไปหยิบโทเคน "พร้อมบูต" ที่เคยอยู่ในวลีประวัติท้ายหัวใบแทน (วลีนั้นถูกเขียนใหม่ในรอบเดียวกันแล้ว) · คำ `CLOSED` ที่อยู่ซ้ายสุดแก้การนับนี้โดยไม่แตะเครื่องมือ (เครื่องมือไม่ใช่เขตของสายนี้) · 🔴 **ผลและงานที่ผลนี้ส่งต่อไม่ถูกปิดไปด้วย**: ผู้ต้องหาคือ**รูปเฟรม `UpdateAttrVital 0x309A`** (`COO-DECISION 20260903_1744`) ยังเป็นหนี้เปิดของ LANE-GM และเป็นคำถามเดียวกับที่ `RE-LV-LIVE-UPDATE-FRAME-001` (ขอไว้ใน `notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-slash-lv-*.md`) ถาม · 🔴 **chief/COO ไม่เห็นด้วย = พลิกกลับได้ด้วยการลบคำ `CLOSED` แล้วเขียนสถานะที่ต้องการลงไปแทน** ไม่มีอะไรถูกลบหรือย้าย · 🔴 **อย่าลบเฉย ๆ**: pf-adversary รอบนี้รันจริงแล้วพบว่าการลบคำเดียวโดยไม่ใส่อะไรแทน ทำให้เครื่องมือไปหยิบโทเคน "พร้อมบูต" จากวลีประวัติในบรรทัดถัดมาผ่านหน้าต่าง fallback `body+1` แล้วรายงานว่าอ่านมาจากเนื้อใบอย่างชอบธรรม (คอลัมน์ `body+1`) -- รูเดิมแต่พรางตัวดีกว่าเดิม ⇒ วลีนั้นถูกแก้เป็น "สถานะก่อนบูต (ประวัติ...)" ในรอบเดียวกันเพื่อปิดรูนั้นไม่ว่าใครจะลบ `CLOSED` หรือไม่ (แจ้งไว้ใน `notes_to_chief/20260906_07xx_LANE-GM-TO-CHIEF-*`) (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — `/speed 400` (ค่าเดียวกับที่ล็อกอินส่งทุกวัน) ทำไคลเอนต์ตายในเฟรมเดียว: HP `0/1` เงิน `0` ไดอะล็อกตาย · เฟรม `LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL` 74 ไบต์ออกจริงครั้งเดียว `SPEED DEFERRED` = 0 · แถว DB ไม่เสียหาย รีล็อกอินรอดเพราะประตูล็อกอิน (`#632`) ⇒ 🔴 **ค่าพ้นผิด ผู้ต้องหาคือรูปเฟรม `UpdateAttrVital 0x309A`** (`COO-DECISION 20260903_1744`) · ผลไปที่ **LANE-GM** ไม่ใช่ chief · สถานะก่อนบูต (ประวัติ ไม่ใช่สถานะวันนี้): ปลดเป็นบูตได้แล้ว R317 -- RECHECK ผ่านครบ 4/4 · chief วัดเองบน `origin/main` `01960240` 2026-09-03T09:5x+07:00 (ไม่ได้เชื่อจดหมาย: `LANE-GM 0822` และ `COO 0845` เป็นแหล่งที่สองที่สาม) · ล็อกทั้งสองของ `/speed` **ยังปิดค้างไว้ตามเดิม ไม่มีใครพลิก** ประตูเปิดในเซสชันผู้เทสด้วย `PF_SPEED_TRIAL=400` เท่านั้น · 🔴 ใบนี้พิสูจน์ "เส้นทางปลอดภัย" **ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์อ่านแถว** อ่านหัวข้อ "ข้อจำกัดที่ใบนี้พิสูจน์ไม่ได้" ก่อนรายงานผล]

### 🔴 PRECONDITION ที่ต้องทำจริงก่อนขั้น 1 -- ไม่ใช่หมายเหตุ (`COO-DECISION 20260903_0845` ข้อ 3)
  P1. `set PF_SPEED_TRIAL=400` **ในหน้าต่างคำสั่งเดียวกับที่จะบูตเซิร์ฟเวอร์ และก่อนบูต** · ค่าอื่นนอกจาก `400` = ออกนอกขอบเขตใบ หยุดและรายงาน
  P2. ยืนยันว่าตั้งติดจริงก่อนบูต: `echo %PF_SPEED_TRIAL%` ต้องพิมพ์ `400` (ไม่ใช่ `%PF_SPEED_TRIAL%`) — คัดบรรทัดนี้ลงผลใบ
  P3. บูตเซิร์ฟเวอร์จากหน้าต่างนั้น **หน้าต่างเดียวกัน** · ตัวแปรปิดเองเมื่อโปรเซสตาย · 🔴 **ห้ามแก้โค้ดเพื่อเปิดประตู และห้ามพลิกธงบน `main`**
  P4. ไม่ตั้ง `PF_SPEED_TRIAL` = `/speed 400` จะถูกกักและขึ้น `SPEED DENIED` ⇒ รอบนั้นเป็น **NO-RESULT ไม่ใช่ FAIL** (ดู pass criteria ข้อ (4))
  ที่มาของกลไก: `gm/speed_wire.py:430` `SPEED_TRIAL_ENV = "PF_SPEED_TRIAL"` · `trial_opening()`/`trial_admits()` อ่าน `os.environ` สดทุกครั้ง ไม่แคช · ผู้เรียกบนเส้น dispatch `gm/chat_command_action.py:4122`

### 🔴 ข้อจำกัดที่ใบนี้พิสูจน์ไม่ได้ -- อ่านก่อนเขียนผล (`COO-DECISION 20260903_0845` ข้อ 4 · ย้ำ `COO 0054`)
  หลังไมล์สโตน `009` **ค่า DEFAULT ของคอลัมน์ `characters.speed_walk` = `400.0` = ค่าคงตัวที่ฮาร์ดโค้ดเดิมทุกไบต์**
  ⇒ "เซิร์ฟเวอร์อ่านแถวแล้วส่ง 400" กับ "เซิร์ฟเวอร์ส่งค่าคงตัว 400" ให้ **ไบต์ชุดเดียวกัน** บนดาต้าเบสสดทุกตัว **รวมของเจ้าของ**
  ⇒ ใบนี้พิสูจน์ได้อย่างเดียวว่า **เส้นทาง `/speed` ปลอดภัยที่ค่า 400** · 🔴 **ห้ามรอบไหนรายงานผลใบนี้เป็น "ชัยชนะบนจอ" หรือเป็นหลักฐานว่า `/speed` ทำงาน**
  แยกสองอย่างนี้ออกจากกันได้ด้วย fixture ที่เขียนค่าอื่น หรือด้วยการรัน `/speed` ค่าที่ต่างจาก 400 เท่านั้น = **ใบใหม่หลังใบนี้ผ่าน**

> เปิดโดย chief รอบ R310 ตาม `COO-DECISION 20260902_2148` ใบที่ 1 · numbering: `GT` สูงสุดในคิว = 217 · `RE` สูงสุดใน `CLIENT_RE_QUEUE.md` = 133 ⇒ ใบนี้คือ **218**
> 🔴 โค้ดใต้ล็อกทั้งสอง **ยังไม่เคยถูกรันแม้แต่ครั้งเดียว** วันที่ล็อกที่สองเปิด = วันแรกที่มันทำงาน และมันจะทำงานต่อหน้าเจ้าของ ⇒ ใบนี้ถูกออกแบบให้ **พังได้อย่างปลอดภัย** · 🔴 **ห้ามพ่วงงานอื่นในใบนี้** ใบอื่นห้ามพังไปกับมัน

RECHECK: (ตัดสินด้วยเนื้อโค้ดบน `origin/main` ห้ามเชื่อคำบอกเล่าหรือเลข commit · ผ่านครบสี่ข้อ = เลื่อนเป็น `READY` ได้เองโดยไม่ต้องรอเจ้าของใบ)
  🔴 **บล็อกนี้ถูกเขียนใหม่ทั้งบล็อกตาม `COO-DECISION 20260903_0649` ข้อ ② (chief รอบ R315)** — รูปเดิมเรียกร้อง `SPEED_LOGIN_READ_LANDED = True` และ `SHAPES_CLEARED_BY_A_REAL_CLIENT` ไม่ว่าง **เป็นเงื่อนไขเข้ารอบ** ทั้งที่สองอย่างนั้นคือ **ผลลัพธ์ของรอบนี้เอง** ⇒ ใบไม่มีวันบูตได้ (วงปิดที่ `LANE-GM 20260903_0529` ข้อ 2 รายงาน)
  🔴 **ล็อกทั้งสองตัวคงค่าเดิมบน `main` ตลอดใบนี้ · RECHECK ห้ามวัดว่ามันเปิด และห้ามใครพลิกมันเพื่อให้ใบนี้บูตได้** (`gm/speed_wire.py:357` = `return not SPEED_LOGIN_READ_LANDED` ⇒ ธงนั้นคือ **ล็อกตัวจริง ไม่ใช่บันทึกข้อเท็จจริง** · "`#605` ลงแล้ว" ไม่ใช่เหตุผลที่พลิกได้) · ประตูเปิด **ในเซสชันของผู้เทสเท่านั้น** ผ่านเกต runtime ข้อ 3 และปิดเองเมื่อโปรเซสตาย
  1. `(cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/session.py | findstr /C:"login_speed.resolve_for_character")`
  2. `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/login_speed.py | findstr /C:"speed_wire.send_deferred()" /C:"wire_deferred")`
  3. `(cd pirate-force-server && git show origin/main:src/pirateforce_foundation/gm/speed_wire.py | findstr /C:"PF_SPEED_TRIAL")`
  4. `(cd pirate-force-server && py -3 -m pytest tests/test_login_speed.py tests/test_gm_speed_deferred.py tests/test_gm_speed_shape_hold.py -q)`
  ข้อ 1 ต้อง **เจอ** = login-read ต่อที่ seam จริง (ล็อกที่ 1 · `COO 1846`)
  ข้อ 2 ต้อง **เจอทั้งสองคำ** = เกตล็อกอินของ `COO-DECISION 20260903_0645` อยู่บน `main` แล้ว: ขณะ `/speed` ถูกกัก ล็อกอิน **ส่งค่าคงตัว** ไม่ใช่ค่าจากแถว (ลงรอบ R315 · `login_speed.held_by_the_speed_deferral`)
     🔴 ข้อนี้คือเหตุผลที่ขั้น "รีล็อกอินเพื่อกู้" ในใบนี้ไม่ใช่กับดัก — ไม่เจอ = **ห้ามบูตใบนี้เด็ดขาด** เพราะแถว `300.0` ที่ `GT-193` ทิ้งไว้จะขึ้นไวร์ตอนล็อกอินถัดไป (`00 00 96 43` ไบต์ชุดเดียวกับที่ล็อกไคลเอนต์ 426 เฟรม)
  ข้อ 3 ต้อง **เจอ** = LANE-GM ลงเกต runtime `PF_SPEED_TRIAL` แล้ว (`COO-DECISION 20260903_0646`) ⇒ ผู้เทสเปิดประตูในเซสชันตัวเองได้โดยไม่ต้องแก้โค้ดและไม่ต้องพลิกล็อกบน `main`
     ~~**ยังไม่เจอวันนี้** (chief วัดบน `origin/main` `d916725` รอบ R315) ⇒ ใบคง `[BLOCKED]`~~ **← ขีดฆ่า ไม่ลบ (R317)**: บรรทัดนั้นจริงตอนเขียน · `#634` merge 2026-09-03T01:11:13Z = **08:11+07:00** คือ **หลัง** การวัดของ R315 ⇒ ไม่ใช่ความผิดของใคร
     **วัดใหม่ R317 (`mgm333`) บน `origin/main` `01960240`: เจอ 8 ครั้ง ⇒ ข้อ 3 ผ่าน** · ทั้งสี่ข้อผ่าน (ข้อ 1 เจอ 1 · ข้อ 2 เจอ 5 และ 3 · ข้อ 4 `138 passed / 66 subtests` รันบน worktree ของ `origin/main` เปล่า) ⇒ **ป้ายพลิกเป็น `[🟢 READY]` ตามที่หัวบล็อกนี้เขียนสั่งไว้เอง**
     🔴 **บล็อก RECHECK ไม่ถูกลบ** — มันยังเป็นเกตถาวรของทุกรอบที่จะบูตใบนี้ · ข้อใดพลิกกลับเป็นไม่เจอเมื่อไหร่ ป้ายกลับเป็น `[BLOCKED]` ทันทีโดยไม่ต้องถามใคร
  ข้อ 4 เขียวทั้งชุด · ข้อใดไม่ตรง = คง `[BLOCKED]` **ห้ามบูต ห้ามเรียกผู้เทส**
  ใบนี้มีชั้น client-observable ⇒ **G-OBS บังคับ**: จดหมายผลต้องมี `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · รันจบแต่ยังไม่มีลายเซ็นตาคน = **`AWAITING-OBSERVER`** (ไม่ใช่ PASS ไม่ใช่ FAIL) · ทุกเฟรมที่ยกมาอ้างต้องมี `t` เทียบ `T0` และ `dist` (G-FRAME)

- objective: ข้ออ้างเดียว -- **พิมพ์ `/speed 400` หนึ่งครั้งบนไคลเอนต์จริง แล้วตัวละคร "รอด": ไม่ตาย และไคลเอนต์ยังรับอินพุตต่อได้** (`GT-193` FAIL: `/speed 300` ⇒ HP 0 · เงิน 0 · ตาย · 426 เฟรมถัดมาไม่มีคลิกเลย · DB ฝั่งเราสะอาด)

- ค่าที่อนุญาต: **`400` ค่าเดียว** พิมพ์ `/speed 400` เป๊ะ ห้ามลองค่าอื่นในรอบนี้แม้แต่ครั้งเดียว
  🔴 **ซอร์สวันนี้ไม่มี clamp และไม่มี allow-list ของค่าเลย**: `gm/speed_wire.py:132-153` (`parse_speed_value`) และ `:184-188` รับ float finite ทุกค่า ปฏิเสธแค่ bool/NaN/Inf · ช่วงเดียวที่มีคือช่วง f32 ทั้งช่วง (`persistence_typed_attrs.py:114` ใช้ที่ `:227-235`,`:250-254`) ⇒ **`400` ปลอดภัยด้วยหลักฐาน ไม่ใช่ด้วยประตูในโค้ด**
  หลักฐานของ `400`: เป็นเลขที่ทุกล็อกอินส่งให้ไคลเอนต์อยู่แล้ววันนี้ (`player_wire.py:77`) · เป็นค่าคอนสตรัคเตอร์ของไคลเอนต์เอง VA `0x00464AF2` ไบต์ `00 00 C8 43` (`migrations/008_character_speed_walk_seed.sql:39,123` · `persistence_attr_compose.py:281,289`) · เป็นค่าในบล็อก "สมประกอบ" ของตัวละครบูต (x7 = 400)
  ⇒ ค่าตรงกับของเดิมทุกไบต์ ⇒ ถ้าไคลเอนต์ยังตายอีก **ผู้ต้องสงสัยคือทรงเฟรม ไม่ใช่ตัวเลข** ซึ่งเป็นคำตอบที่วันนี้เราไม่มี

- 🔴 **อาจต้องรีล็อกอิน -- รู้ไว้ก่อนกด ไม่ใช่ตอนจอค้าง**: ถ้าไคลเอนต์ล็อกตัวเองซ้ำแบบ `GT-193` ทางออกเดียวคือปิดไคลเอนต์ **แล้วรีสตาร์ตเซิร์ฟเวอร์ก่อน** จึงบูตไคลเอนต์ใหม่ (ไม่รีสตาร์ต = ตัวถัดไปค้าง "connecting" ตลอดกาล) · การรีล็อกอินนี้เป็น **ขั้นกู้ ไม่ใช่ผลวัด** และการที่ต้องใช้มัน = **FAIL ของชั้น client-observable**
  🔴 **ขั้นกู้นี้อยู่ได้ก็ต่อเมื่อ RECHECK ข้อ 2 ผ่านแล้วเท่านั้น** (`COO-DECISION 20260903_0649`): ก่อนเกต `0645` ลง `main` การรีล็อกอินคือทางที่แถวเก่าของ `/speed` ขึ้นไวร์เอง ⇒ ขั้นกู้กลายเป็นกับดักที่ทำซ้ำอาการเดิม · เมื่อกู้แล้วให้บูตเซิร์ฟเวอร์ใหม่ **โดยไม่ตั้ง** `PF_SPEED_TRIAL` (ประตูปิดตามค่าเริ่มต้น) เว้นแต่ใบสั่งใหม่บอกเป็นอย่างอื่น

- db: canonical `state\pirateforce.sqlite3` -- 🔴 **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ `state\run_gt218_<yyyyMMdd_HHmmss>.sqlite3`
  🔴 **ชื่อสำเนาห้ามเป็น `pirateforce.sqlite3` และห้ามมี `~`** ไม่งั้นเกต `_speed_db_is_canonical` (`gm/chat_command_action.py:3463-3493`) กันคำสั่งทิ้งทั้งใบ
  sha256 สำเนาก่อน/หลัง · sha256 canonical ก่อน/หลัง ต้องเท่ากัน · `PRAGMA integrity_check` = `ok` สองครั้ง · **teardown เสมอ** (เทมเพลตปฏิเสธ boot stamp เก่ากว่า 420 นาที) · รอบคัดลอก DB ⇒ ตัวละครกลับ spawn ทุกบูต ปกติ ไม่ใช่ผลวัด

- server args: บูตมาตรฐาน **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` · บัญชี GM ใน `config/gm_accounts.json` · 🔴 เก็บคอนโซลรวม stdout+stderr (โทเคนเลนนี้ออกทาง stderr ล้วน):
  `set PF_SPEED_TRIAL=400`
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt218_<stamp>.sqlite3 2>&1`
  🔴 **ตั้งตัวแปรนี้ในหน้าต่างคำสั่งเดียวกับที่บูตเซิร์ฟเวอร์ ก่อนบูต** (`COO-DECISION 20260903_0646`/`0649`) — มันคือสิ่งเดียวที่เปิดประตู `/speed` ในรอบนี้ · ปิดเองเมื่อโปรเซสตาย · **ห้ามแก้โค้ดเพื่อเปิดประตู และห้ามพลิกธงบน `main`**
  🔴 ค่าที่ตั้งต้องเป็น `400` เท่านั้น ตรงกับค่าที่ใบนี้อนุญาตให้พิมพ์ · ตั้งค่าอื่น = ออกจากขอบเขตใบ หยุดและรายงาน
  🔴 **เกตนี้เปิดประตูเดียว คือ `/speed` ขาออก ไม่เปิดประตูล็อกอิน** — และนั่นตั้งใจ (chief R315 เข้มกว่าใบ `0645` หนึ่งขั้นหลัง pf-adversary): ระหว่าง trial ล็อกอินยังส่ง **ค่าคงตัว** และพิมพ์ `LOGIN_SPEED wire_trial_only` เพราะ trial อนุมัติ **ค่าเดียว** แต่แถวอาจถือค่าที่ไม่ได้รับอนุมัติ (`/speed` เขียนแถวแม้เฟรมถูกกัก)
  ⇒ **ขั้นรีล็อกอินในเซสชันที่ตั้ง `PF_SPEED_TRIAL` จึงปลอดภัย** · เห็น `LOGIN_SPEED wire_trial_only` ในคอนโซล = ปกติ ไม่ใช่ finding · เห็น `LOGIN_SPEED from_row` ระหว่าง trial = **finding หยุดและรายงาน**
  บรรทัด `LOGIN_SPEED ... withheld_row=<ค่า>` บอกว่าแถวถือค่าอะไรอยู่ตอนถูกกัก — คัดดิบลงผลใบด้วย มันคือหลักฐานเดียวที่บอกว่าเกตกันอะไรไว้จริง

- steps: (playbook `ATTENDED_SESSION_RUNBOOK.md` · อัดวิดีโอต่อเนื่องตลอด `LOCK_GAME` · ~10 นาทีบนจอ)
    0. RECHECK ผ่านก่อน · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB
    1. **server ก่อน client เสมอ** · ล็อกอิน GM · ยืนยันบล็อก "สมประกอบ" จากคอนโซล (level 1 · class 1 · stats จาก `CHARCREATE_CLASS s_SCORE` · HP/MP จาก `STANDARD_STATUS` · x7 = 400 · ชื่ออยู่ `BasicAttr` x1 `+0x28` ห้ามอยู่ x37 · x39/x41/x42 = 0) ไม่ครบ = หยุด ไม่รัน · จด scene + X/Y/Z + `T0` เป็นเวลาจริง +07:00
    2. `S0-BASE` full-res โดยเห็น **เลข HP และเลขเงิน** ชัด · จัดกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น (หมุนกล้องอย่างเดียว · facing ไม่ขยับ · ไม่มีไบต์ขึ้นไวร์)
    3. baseline: กด `W` ค้าง 5 วินาทีจากจุดที่จำได้ จด X/Y ก่อน-หลัง · `S1-WALK` · (`W/A/S/D` และ `Q`/`E` เปลี่ยน **facing ของตัวละคร** และยิง `TargetPosVital` ⇒ ใช้เฉพาะขั้นที่สั่งให้เดิน)
    4. คลิกช่องแชท **ยืนยันว่าโฟกัสจริง** พิมพ์ `/speed 400` แล้ว Enter · เป็นคำสั่ง GM **ไม่ใช่** ทริกเกอร์แชท 12 ตัวอักษร **ห้ามเติมอักษรให้ครบ 12** · **ห้ามพิมพ์อักษรใดตอนช่องแชทไม่โฟกัส** (กลายเป็นฮอตคีย์)
    5. **ห้ามแตะอะไรเลย 5 วินาที** จ้องจอ · `S2-AFTER` ภายใน ~3 วิ ต้องเห็นเลข HP · เลขเงิน · ช่องแชท
    6. NO-CRASH: **คลิกขวาค้างลากหมุนกล้อง** (🔴 ห้ามใช้ `Q`/`E` เป็นตัวเช็คนี้)
    7. เดินซ้ำแบบขั้น 3 จากจุดเดิม กด `W` ค้าง 5 วินาที · `S3-WALK2` · ออกเกมด้วยปุ่ม X
    8. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **teardown เสมอ** · ห้าม commit เอง
    9. คัดดิบ ห้ามตีความ:
       `findstr /N /C:"LANE_GM_CHAT_ACTION" /C:"LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL" /C:"SPEED DEFERRED" /C:"GM_CHAT_NO_BYTES_SENT" /C:"LOGIN_SPEED" server_console_live.*.txt`
    🔴 **STOP:** HP กลายเป็น 0 · เงินกลายเป็น 0 · ตัวละครตาย ⇒ หยุดทั้งใบทันที ถ่าย `S2-AFTER` ให้ได้ แล้วรายงาน (นี่คือ **ผลของใบ** ไม่ใช่ความผิดของผู้เทส)

- pass criteria: (สองชั้น 🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้นเด็ดขาด**)
    wire/DB (headless พิสูจน์ได้ ไม่ต้องมีตาคน):
      (ก) มี `LANE_GM_CHAT_ACTION speed route=action` แล้วตามด้วย `[G>] LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL` **หนึ่งครั้ง** · **ไม่มี** `SPEED DEFERRED` และ **ไม่มี** `GM_CHAT_NO_BYTES_SENT ... why=withheld_speed_*`
      (ข) เฟรมนั้นต้องมี `00 00 C8 43` (400.0) **ไม่ใช่** `00 00 96 43` (300.0 ของ `GT-193`)
      (ค) หลังเฟรมนั้นมีเฟรมขาเข้าที่ **ไม่ใช่ heartbeat อย่างน้อย 1 เฟรม** (`GT-193` วัดได้ 0 จาก 426)
      (ง) `characters.speed_walk` ในสำเนา = `400.0` · ฟิลด์อื่นในแถวเท่าเดิมทุกไบต์ (diff ก่อน/หลัง)
      (จ) `integrity_check` = `ok` สองครั้ง · sha canonical ไม่เปลี่ยน · ไม่มี traceback หลุด
      🔴 **ชั้นนี้ตอบไม่ได้ว่าตัวละครยังมีชีวิตบนจอไหม** -- `GT-193` พิสูจน์แล้วว่า DB ฝั่งเราสะอาดได้ทั้งที่ตัวละครตาย
    client-observable (🔴 ต้องมีคนนั่งหน้าจอ ห้ามอนุมานจากคอนโซล · **ชั้นนี้เท่านั้นที่ตัดสินใบ**):
      (1) ครบ 5 วินาทีหลัง Enter: **เลข HP เท่าเดิมและไม่ใช่ 0 · เลขเงินเท่าเดิม · ไม่ตาย ไม่มีหน้าจอชุบชีวิต** -- เขียนเลขจริงจาก `S0-BASE` และ `S2-AFTER` ทั้งคู่
      (2) ไคลเอนต์ยังรับอินพุต: คลิกขวาค้างลากแล้ว **กล้องหมุนจริงบนจอ** และกด `W` แล้ว **ตัวละครขยับจริงบนจอ**
      (3) **[คำทำนาย ไม่ใช่ผลวัด]** ความเร็วเดิน **ไม่เปลี่ยน** เพราะ 400 คือเลขที่ล็อกอินส่งอยู่แล้ว ⇒ เขียนระยะที่เดินได้ทั้ง `S1-WALK` และ `S3-WALK2` · **ทำนายผิด = finding ไม่ใช่ความล้มเหลว**
      (4) คัดข้อความในช่องแชทตรงตัว · เห็น `SPEED DENIED` (12 ตัวอักษร ASCII) = ล็อกที่ 2 ยังปิด ⇒ รอบนี้เป็น **NO-RESULT ไม่ใช่ FAIL** หยุดและรายงาน
      (5) 🔴 **จดสีป้ายชื่อทุกป้ายทุกภาพ หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ** ไม่มีป้ายให้เขียน `none` ห้ามเว้นว่าง · อ่านจาก **full-res เท่านั้น** · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · ต่างจากภาพเซิร์ฟเวอร์จริง ⇒ `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
      🔴 **ชั้นนี้ตอบไม่ได้ว่าเฟรมใดออกจากเซิร์ฟเวอร์ หรือแถวใน DB เป็นอะไร**
    🔴 **ผลลบมีค่าเท่าผลบวก**: ตายอีกทั้งที่ค่าเป็น 400 ⇒ ผู้ต้องสงสัยย้ายจาก **ตัวเลข** ไปที่ **ทรงเฟรม** ⇒ redirect ไปคำถาม deserializer · **ห้ามปลด `SHAPES_CLEARED_BY_A_REAL_CLIENT` ด้วยผลลบนี้**

- nonclaims:
  1. ไม่พิสูจน์ว่า `speed_walk` รอดข้ามล็อกอิน -- ใบนี้ใช้ค่าที่เท่ากับค่าเดิมโดยตั้งใจ
  2. ไม่พิสูจน์ว่าค่าอื่นปลอดภัย -- ครอบ `400` ค่าเดียว · `300` ยังเป็นค่าที่ฆ่าตัวละครมาแล้ว (`GT-193`)
  3. ไม่พิสูจน์ว่า `/speed` ทำให้ความเร็วบนจอเปลี่ยนได้จริง (ต้องใช้ค่าที่ต่างจาก 400 = ใบใหม่หลังใบนี้ผ่าน)
  4. ไม่พิสูจน์ vital_version byte ของ `UpdateAttrVital` (0x309A) · ไม่ตัดสินสาเหตุอาการของ `GT-193`
  5. ไม่ตัดสินความหมายของสีป้าย (`RE-067`) · ไม่แตะคอมแบต/ดรอป/กระเป๋า
  6. ไม่ใช่ negative control ของ `check 0/4` -- ใบที่ 2 ของ COO `2148` พ่วงเป็นขั้น `0N` ใน `GT-207` ไม่ใช่ใบนี้

- links: `COO-DECISION 20260902_2148` (ใบที่ 1) · `COO-DECISION 20260902_1846`/`1847` · `GT-193` (FAIL) · `RE-067` ·
  `gm/speed_wire.py:277,327` · `gm/chat_command_action.py:3803,3861` · `session.py` (`login_speed.resolve_for_character`) · `login_speed.py` · `player_wire.py:77`

- result: (ผู้เทสกรอก: PASS/FAIL/NO-RESULT · branch/commit ที่บูต · `S0-BASE`/`S1-WALK`/`S2-AFTER`/`S3-WALK2` · เลข HP/เงินทั้งสองภาพ · บรรทัดคอนโซลดิบทุกโทเคน · ตารางสีป้ายครบทุกป้ายทุกภาพ · sha256 ทั้งสี่ค่า · `integrity_check` · NO-CRASH/CRASH · ต้องรีล็อกอินหรือไม่ · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

**ผู้เปิดใบ: chief (สาย E) รอบ R310 `gnhlin` ตาม `COO-DECISION 20260902_2148` -- chief บริโภคผลใบนี้เอง**

---


## GT-277 LV-SET-CHARACTER-LEVEL-RELOG-001  [✅ **PASS สองชั้น · OBSERVER_CONFIRMED (ผู้เทสไม่ได้เขียน ISO เป๊ะ แต่ทำซ้ำสามครั้ง 11:13/12:18/12:20 +07:00 2026-09-06)** — ตั้งเลข+วางเนื้อ+พับ+archive ในรอบเดียวโดย LANE-K รอบ `n3s0rg` 2026-09-06T14:10+07:00 ตาม `COO-DECISION 20260906_1346` ข้อ 3(ก) · เนื้อใบคำต่อคำจาก `notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-slash-lv-lands-gt-body-and-re-question.md` ข้อ 1 · ผลคำต่อคำจาก `notes_to_chief/20260906_1255_KA1A-R321-RESULTS-*.md` §3 (`RESULT: GT-LV(no number) PASS R321 2026-09-06 11:13-12:21`) · เจ้าของใบ = LANE-GM · ปิด `PANYA-ORDER 20260906_0155` (เส้นตาย 14:00) ทางเอกสาร]

- objective: `/lv <n>` (คำสั่ง GM) เขียนเลเวลลง DB จริง และเลเวลใหม่ปรากฏบนจอหลัง relog
- owner/consumer = LANE-GM

ATTENDED: บูต run-copy DB (`--db state\run_gtlv.sqlite3`) ด้วยบัญชี GM · เข้าเกมด้วยตัวละครหนึ่งตัว
ATTENDED: จดเลเวลที่จอแสดงตอนนี้ · พิมพ์ในช่องแชต: `/lv 30`
ATTENDED: ดู (ก) ประโยค `LV SET RELOG` โผล่ในช่องแชตภายใน 5 วินาที (ข) คอนโซลเซิร์ฟเวอร์มีบรรทัดขึ้นต้น `GM_LV`
ATTENDED: logout แล้ว login ใหม่ด้วยตัวละครเดิม · ดูเลเวลที่หน้าต่างสถานะและที่ป้ายชื่อ
ATTENDED: PASS = ข้อ 4 เห็นเลขที่ตั้ง · FAIL = ยังเห็นเลขเดิม (จดว่าเห็นที่ไหนบ้าง/ไม่เห็นที่ไหน)

**เกณฑ์ผ่านสองชั้น**
- **wire/DB**: แชท `LV SET RELOG` + คอนโซล `GM_LV ... level -> <n> (row written; next login sends it)`
- **client-observable**: หลัง relog จอ/ป้ายชื่อแสดงเลเวลใหม่ (`LOGIN_VITALS from_row level=<n>`)

**nonclaims** (คำต่อคำจากผู้เขียนใบ, LANE-GM):
- ผลลบมีค่าเท่าผลบวก: ถ้าแถวเปลี่ยนแต่จอไม่เปลี่ยน = ไคลเอนต์ไม่ได้วาดจาก BasicAttr bit `0x0002` (คำตอบเดียวกับที่ `GT-200` ยังค้างอยู่)
- ห้ามใช้ `/lv` เป็นหลักฐานว่า M-อะไรผ่าน · ใบไหนใช้ `/lv` ไปถึงสภาพเทสต้องมี nonclaim ว่าข้ามขั้นไหน
- ยาม canonical DB ทำให้ `/lv` ทำงานเฉพาะบูต run-copy ⇒ เลเวลอยู่รอด relog **ภายในบูตเดียว** เท่านั้น บูตถัดไปที่ copy DB ใหม่จะกลับเป็นค่าเดิม (ข้ามบูตต้องเป็นคำสั่งใหม่ของเจ้าของ)

**result** (คัดลอกคำต่อคำจาก `notes_to_chief/20260906_1255_KA1A-R321-RESULTS-*.md` §3):
`/lv 5` 11:13:09 → แชท `[ทั่วไป] : LV SET RELOG` · err `GM_LV … level -> 5 (row written; next login sends it)` · จอยัง LV 1 (ตั้งใจ ยังไม่ relog) → relog 11:17 → **จอ LV 5** · `LOGIN_VITALS from_row level=5` · `/lv 1` 12:18 → relog → LV 1 · `/lv 5` 12:20 → relog → LV 5 · ทำซ้ำ 3 ครั้งตรงทุกครั้ง
สถานะที่เสนอ (ka1-A): **PASS สองชั้น** — chief/COO สั่งว่าตั้งเลขใบแล้วปิดจากผลนี้ได้เลย ไม่ต้องบูตซ้ำ (`COO-DECISION 20260906_1346` ข้อ 3(ก))

**links**: `RE-LV-LIVE-UPDATE-FRAME-001` (`RE-278`, คำถามต่อยอด: เฟรม live-update เลเวลไม่ต้อง relog) · `GT-200` (ยังค้าง, คำถามเดียวกันเรื่อง BasicAttr bit `0x0002`) · `attr_wire.py:424` แถว x=2 (`RE-117`)

**ผู้เปิดใบ: LANE-GM (ผ่าน `notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-*`) ตาม `PANYA-ORDER 20260906_0155` -- ตั้งเลข/วาง/พับ/archive: LANE-K รอบ `n3s0rg` ตาม `COO-DECISION 20260906_1346` ข้อ 3(ก) -- ผู้บริโภคผล: LANE-GM**

---

## GT-242 BACKPACK-OPEN-DOES-NOT-WIPE-THE-GROUND-001  [✅ **ปิดใบ: PASS สองชั้น (เว้น item(4) NO-RESULT) ตาม `R316` 2026-09-05T11:02+07:00 `OBSERVER_CONFIRMED: 2026-09-05T10:50+07:00`** — ยืนยันโดย `COO-DECISION 20260906_1452`: R316 คือผลปิดใบ (`GROUND_REANNOUNCE_AFTER_SECOND_PWD scene='Bg0002' items=2` ครบ + negative control `REFUSED` ตอนพื้นว่าง + ของอยู่บนจอก่อน/ระหว่าง/หลัง ตรง objective เดียวของใบ) · **`R321` (ในบล็อกประวัติด้านล่าง) BLOCKED = ความพยายามวัดซ้ำหลัง PASS แล้ว ไม่ใช่ผลใหม่ที่หักล้าง** (บูตซ้ำเกิดเพราะ R316 ไม่เคยถูกพับ ไม่ใช่เพราะผลขัดแย้งกัน) · item(4) `oldest_left` NO-RESULT แยกเป็นข้อค้นพบ "lifetime not enforced" ต่างหาก ไม่ถ่วงใบนี้ (ใบใหม่เจ้าของ **LANE-B** ยังไม่มีคนตั้งเลข ณ รอบนี้ — รอ LANE-B ส่งเนื้อใบ) · พับปิด+archive โดย **LANE-K รอบ `rsmsia`** 2026-09-06T15:09+07:00 · ---- 🔧 LANE-K พับผล รอบ `n3s0rg` 2026-09-06T14:10+07:00 — 🔴 ผลค้างพับก่อนหน้าที่รอบ `slug54` มองข้าม: **R316 2026-09-05T11:02+07:00 เสนอ PASS สองชั้น** — wire (1)(2)(3)(5) ครบ + client (7)(8)(9) ครบ (ของยังอยู่บนจอก่อน/ระหว่าง/หลังเปิดกระเป๋า) · เฉพาะข้อ (4) `oldest_left` เดี่ยว = NO-RESULT (ไม่กระทบข้ออื่น) · `OBSERVER_CONFIRMED: 2026-09-05T10:50+07:00` · จาก `notes_to_chief/20260905_1102_KA1A-R316-RESULTS-*.md` · RESULT: GT-242 PASS-สองชั้น(เว้น item4 NO-RESULT) R316 2026-09-05 · [สมมติของสาย LANE-K - รอ COO ยืนยัน] ไม่ทราบว่า R321 (2026-09-06 ด้านล่าง) ตั้งใจวัดซ้ำทั้งที่ R316 ผ่านแล้ว หรือ R316 ยังไม่นับปิดใบเพราะเหตุผลอื่น — ถามแล้วใน `notes_to_chief/20260906_1410_LANE-K-ASK-COO-gt242-r316-pass-vs-r321-blocked.md` · **ยังไม่ archive จนกว่า COO ตอบ** · ---- 🔧 LANE-K พับผล รอบ `slug54` 2026-09-06T13:15+07:00 — BLOCKED (R321 2026-09-06 §8: ต้องฆ่ามอน แต่มอนฉาก 2 เขียว/ตีไม่ได้จากบั๊ก §1 login-126-no-faction — ไม่ใช่ผลของเกณฑ์ใบนี้เอง) · RESULT: GT-242 BLOCKED R321 2026-09-06 (same as GT-220/223) · จาก notes_to_chief/20260906_1255_KA1A-R321-*.md · ✅ **READY -- บูตได้ทันที** (ปลดหัวโดย chief รอบ `rs8uyz`/R350 2026-09-05T08:2x+07:00) · **วัดจาก `main` ในรอบที่เขียน ไม่ใช่จากบันทึกรอบก่อน** (`NOW.md` `COO 1849`): `#781` merge แล้ว = `f71cb9ae` · `mob_drop_presence.py:818` มี `GROUND_REANNOUNCE_AFTER_SECOND_PWD` บน main · จุดเรียก `runtime.py:10130` `reannounce_ground(` บน main — สองครึ่งครบ · เดิม: 🟠 BLOCKED รอ `#781` (chief รอบ `kj0s6r`/R346 2026-09-05T02:3x+07:00) · ✅ **(ก) ฟังก์ชันประกาศของบนพื้นซ้ำ = อยู่บน `main` แล้ว** (`mob_drop_presence.reannounce_ground` · LANE-B ตาม `COO 20260904_1649` ข้อ 2) · 🟠 **(ข) จุดเรียกของ chief = push แล้ว รอเกต+merge ที่ `#781`** (`COO 20260904_1648` ข้อ 2 · commit `3393eb85` · ทดสอบ headless 8 ใบ มิวแทนต์ตายสองตัว · ชุดเต็ม 10360 passed / 0 failed เขียว(cloud sanity) `python3 -V` = 3.11.15) · ✅ ~~ห้ามบูตจนกว่ารอบถัดไปจะเห็น `#781` `merged=true`~~ **จ่ายแล้ว R350** (`AGENTS.md` §7: อยู่บน main ต่อเมื่อรอบถัดไปวัดได้ — R350 วัดแล้ว ดูหัวใบ) · `RECHECK` ผ่านครบ = ปลดเป็น `READY` · เปิดโดย chief รอบ `oi2r2n`/R340 · เจ้าของใบ/ผู้บริโภคผล = **chief (LANE-E)** · ผู้รัน = **Panya (attended)** ~8 นาที]

> 🔴 **ใบข้อบกพร่อง ไม่ใช่ใบสำรวจ** — อาการวัดแล้ว ใบนี้พิสูจน์ว่า**ตัวแก้ได้ผล**
> 🔴 **ห้ามผูก ห้ามต่อคิว ห้ามเกรดรวมกับ `GT-223`** (`COO 20260904_1648` ข้อ 2 คำต่อคำ) — ใบนี้อยู่ในเซสชันล็อกอินเดียว ไม่มีรีล็อกอิน

- objective: ข้ออ้างเดียว -- **การเปิดกระเป๋าไม่ทำให้ของที่ยังอยู่บนพื้น (เซิร์ฟเวอร์ยังถือ ยังไม่หมดอายุ) หายไปจากจอ**
- ที่มา (วัดแล้ว ไม่ใช่การเดา): `notes_to_chief/20260904_1430_KA1A-R309-RESULTS-*` finding 1 — ดรอป `2205601` แล้วเจ้าของ **เปิดกระเป๋าเฉย ๆ** ⇒ ของหายจากจอ · ไคลเอนต์ส่ง `CheckSecondPwdVital 0x4B98` (64 B) → เราตอบ `V110_CHECK_SECOND_PASSWORD_OK` (44 B) **ท้ายเฟรม `0B 00` = ground-list ว่าง** · หลังจากนั้นคอนโซลยังพิมพ์ `MOB_DROP_PRESENCE ... live=1 announced=0 carried=1 oldest_left=65.6s` ⇒ **ของไม่ได้หมดอายุ**

- RECHECK: (รันจากราก `pf_bridge` · ข้อใดไม่ผ่าน = ยัง BLOCKED ห้ามบูต)
  ```
  git -C ../pirate-force-server fetch origin
  git -C ../pirate-force-server grep -c "GROUND_REANNOUNCE_AFTER_SECOND_PWD" origin/main -- src/
  git -C ../pirate-force-server grep -n "mob_drop_presence.reannounce_ground" origin/main -- src/pirateforce_foundation/runtime.py
  ```
  ข้อ 1 ต้อง **>= 1 hit** · ข้อ 2 ต้อง **>= 1 hit** และอยู่ทันทีหลังบรรทัด `actions = super().dispatch(parsed)` (`runtime.py` ~10051-10125)
  ✅ **แก้แล้วโดย chief รอบ `kj0s6r`/R346 — คำสั่ง grep เดิมใช้ไม่ได้ ต้องแก้พร้อมโค้ดในรอบเดียวกัน** (`AGENTS.md` §7 · `NOW.md`): ชื่อโทเคนที่เคยเสนอไว้ (`GROUND_REANNOUNCE_AFTER_SECOND_PWD`) **ไม่ได้อยู่ใน `runtime.py`** — มันเป็นค่าคงที่ของ `mob_drop_presence.py` (ฟังก์ชันเป็นคนพิมพ์เอง) ⇒ grep เดิมจะได้ **0 hit ตลอดกาล** และ RECHECK จะไม่มีวันผ่าน แม้สายจะเสียบถูกทุกอย่าง · คำสั่งข้างบนคือชื่อจริงที่ลงบน `main` แล้ว
  🔴 **จุดเสียบไม่ใช่ที่ที่ใบขอไว้เดิม และนี่คือความตั้งใจ** (วัดแล้วรอบ `kj0s6r` ด้วยการรันจริง): `GROUND_REANNOUNCE_WIRING` ชี้ไปที่บล็อกที่เรียก `make_proactive_second_password_ok` ซึ่ง **ทั้งสองบล็อกอยู่หลัง `second_password_mode == "bypass"`** ⇒ เป็นโค้ดตายบนบูต attended ทุกครั้ง (บิลด์ attended ต้องเป็น `required` มิฉะนั้นสำมะโนดับทั้ง 13 แมพ) · เฟรมตอบ 44 ไบต์ถูกส่งบนบูต `required` จริง **ผ่านการสืบทอด** (`PersistentGameSessionState(legacy.GameSessionState)` → `super().dispatch()` → `pf_login_game_server_v141.py:3864-3867`) ซึ่งเป็นเหตุที่ grep หาชื่อ vital ใน `runtime.py` ไม่เจอ · ยืนยันจากบันทึก R309 เอง: `14:18:01 client CheckSecondPwdVital 0x4B98 (64 B) -> server V110_CHECK_SECOND_PASSWORD_OK (44 B)` บนบูตไม่มีธง

- db: **สำเนาเท่านั้น** `copy state\pirateforce.sqlite3 state\run_gt242_<stamp>.sqlite3` แล้วบูตทับสำเนา · sha256 canonical ก่อน/หลังต้องตรง `CANON_SHA.txt` · `PRAGMA integrity_check` = `ok` สองครั้ง
- server args: บูตมาตรฐาน · `-SecondPasswordMode bypass` · 🔴 **ไม่มีแฟล็ก `--*-scenario`** · เก็บคอนโซลรวม `2>&1` + `capture_v141\GAME_LIVE.txt`
  🔴🔴 **กับดัก GT-192 ซ้ำ — chief เติมบรรทัดกันไว้รอบ `kj0s6r`/R346** (`notes_to_chief/20260902_1604_LANE-GM-TO-CHIEF-gt192-server-args-line-would-disable-the-census.md`):
  `-SecondPasswordMode bypass` **ขีดเดียว = แฟล็กของไคลเอนต์** ใส่ตรงบรรทัดคำสั่งเปิด `GameClient` เท่านั้น ·
  🔴 **ห้ามส่ง `--second-password-mode` (สองขีด) ให้เซิร์ฟเวอร์เด็ดขาด** — ค่าที่ไม่ใช่ `required` ทำให้
  `world_census_enabled` เป็นเท็จและ **สำมะโนดับทั้ง 13 แมพ** ⇒ ไม่มีมอนให้ฆ่า ไม่มีของตก ใบนี้กลายเป็น NO-RESULT
  ที่ดูเหมือนความผิดของตัวแก้ · เซิร์ฟเวอร์ของใบนี้บูตด้วยค่าเริ่มต้น (`required`) เท่านั้น และ**นั่นคือบูตที่ตัวแก้ทำงาน**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt242_<stamp>.sqlite3
  ```

- steps: (เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง · ฆ่าไคลเอนต์แล้วต้องรีสตาร์ตเซิร์ฟเวอร์ก่อน · 🔴 **ห้ามพิมพ์ลงแชท** ตัวอักษรตอนแชทไม่ focus = ฮอตคีย์)
  1. RECHECK ผ่านครบ · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB
  2. บูตเซิร์ฟเวอร์ใหม่สด → บูตไคลเอนต์ → ล็อกอินลงฉาก 2 → รอโหลดจบ
  3. 🔴 **NEGATIVE CONTROL ห้ามข้าม:** ตอนพื้น**ยังไม่มีของ** เปิดกระเป๋า → ภาพ `S0` เต็มความละเอียด → ปิด · จดว่าเปิดด้วยปุ่ม/คีย์อะไร แล้วใช้ท่าเดิมทุกครั้ง
  4. ฆ่ามอนหนึ่งตัวให้มีของตก · **อย่าเก็บ อย่าเดินหนี** · ภาพ `S1` (เห็นโมเดล + ป้ายชื่อของ) · จด **T0 = เวลา (+07:00) ของบรรทัด `MOB_LOOT_DROPS_CENSUS` ของการตกครั้งนี้**
  5. 🔴 **ภายใน 30 วินาทีจาก T0** (อายุประกาศ 120 วิ — ช้ากว่านี้เสี่ยงวัดการหมดอายุแทน) เปิดกระเป๋าท่าเดิม · **ห้ามคลิกอะไรทั้งในแผงและบนพื้น** · รอ ~10 วิ · ภาพ `S2` **มุมเดียวกับ `S1`** เห็นทั้งแผงกระเป๋าและพื้นจุดที่ของตกในภาพเดียว
  6. ปิดกระเป๋า · ภาพ `S3` มุมเดียวกับ `S1`
  7. NO-CRASH: **คลิกขวาค้างลากกล้องอย่างเดียว** (🔴 ห้ามใช้ `Q`/`E` — มันหมุนตัวละครและยิง `TargetPosVital`) · ออกด้วยปุ่ม X
  8. ปิดเซิร์ฟเวอร์ แล้วคัดหลักฐาน:
     ```
     findstr /C:"MOB_LOOT_DROPS_CENSUS" /C:"MOB_DROP_PRESENCE" <คอนโซลรวม>
     findstr /C:"GROUND_REANNOUNCE_AFTER_SECOND_PWD" <คอนโซลรวม>
     findstr /C:"CheckSecondPwdVital" /C:"V110_CHECK_SECOND_PASSWORD_OK" <คอนโซลรวม>
     ```
  9. sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ** · ห้าม commit เอง

- pass criteria: 🔴 **สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น** · ครบชั้นเดียว = `🟡 <ชั้นที่ครบ> ... · <ชั้นที่ขาด> = NOT MEASURED · ใบยังไม่ปิด` **ห้ามปั๊ม PASS**
  - **wire/DB** (คอนโซล + `GAME_LIVE.txt` · ไม่ต้องมีตาคน):
    (1) ขั้น 4 มีครบคู่ `MOB_LOOT_DROPS_CENSUS ... items=<id>:x1@<obj>` และ `MOB_DROP_PRESENCE ... live=1 announced=1 ... declared_lifetime=<n>`
    (2) ขั้น 5 มี `CheckSecondPwdVital` ขาเข้า (64 B) + reply 44 B · คัด**ท้ายเฟรม 2 ไบต์** ของ reply — อ่านไม่ได้เขียน `tail=unread` **ห้ามเดา** · ~~`tail=0B 00` = **FAIL ชั้นนี้**~~ 🔴 **ถอนเกณฑ์นี้ทิ้ง — chief รอบ `kj0s6r`/R346 (วัดแล้ว)**: reply 44 ไบต์คือ `make_check_second_password_success()` ซึ่งถูก **พินด้วย sha256** (`second_password_bypass.SECOND_PASSWORD_OK_FRAME_SHA256`) และมาจาก v141 ที่แช่แข็ง ⇒ ท้ายเฟรมของมัน **เป็น `0B 00` เสมอและเปลี่ยนไม่ได้** ตัวแก้ของรอบนี้ต่อเฟรมประกาศซ้ำ *เพิ่ม* หลัง reply ไม่ได้แก้ตัว reply ⇒ เกณฑ์เดิมทำให้รอบที่**ทำงานถูกทุกอย่าง**ยังรายงาน FAIL ชั้น wire และใบปิดไม่ได้ตลอดกาล (เสียเวลาผู้เทส 8 นาทีโดยรับประกันว่าไม่ปิด) · **อีกอย่าง `0B 00` ไม่ใช่ "รายการของบนพื้นที่ว่าง"**: มันคือ derived-class change mask = 0 ที่ `make_runtime_vitals` ต่อท้าย **ทุกเฟรม** runtime-vitals (V99 show-message และ V100 music ก็ลงท้าย `0B 00` เหมือนกัน) ⇒ รายการของบนพื้น **ไม่มีอยู่ในเฟรม** (derived bit `0x08` ไม่ถูกตั้ง) ไม่ใช่ "มีแต่ว่าง" · คำถามว่า member ที่ไม่มีอยู่ล้าง pool ของไคลเอนต์ไหม **ยัง UNMEASURED** ตามที่ LANE-B เขียนไว้เอง (`mob_loot.py:5189-5195` `[ASSUMPTION OF LANE B - AWAITING COO]`)
    **(2-ใหม่) แทนที่**: ขั้น 5 ต้องมี `CheckSecondPwdVital` ขาเข้า (64 B) + reply 44 B · แล้ว**ทันทีหลัง reply** ต้องมีบรรทัดคอนโซล `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene=<n> items=<k>` **หนึ่งบรรทัด** (`items=0` = พื้นโล่งจริง ตรวจแล้ว · ไม่มีบรรทัดนี้เลย = **บิลด์เก่า ไม่ใช่ผลลบ** ⇒ NO-RESULT ห้ามเกรด) · `GROUND_REANNOUNCE_AFTER_SECOND_PWD_REFUSED` = ชั้นนี้ FAIL พร้อม `reason=` ที่พิมพ์มา · คัด `tail=` ของ reply ไว้เป็น**บันทึก** ไม่ใช่เกณฑ์
    (3) `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene=<n> items=<n>` อย่างน้อยหนึ่งบรรทัด**หลัง** reply ของขั้น 5 และ `items >= 1` · **0 บรรทัด = `NO-RESULT` ไม่ใช่ FAIL** (บูตบิลด์ที่ยังไม่มีตัวแก้ — รายงาน commit ที่บูต)
    (4) `MOB_DROP_PRESENCE ... oldest_left=<s>` ที่ออก**หลัง**ขั้น 5 ต้อง `> 0` · `<= 0` หรือไม่มีบรรทัด = **`NO-RESULT` รันใหม่ให้เร็วขึ้น**
    (5) `integrity_check` = `ok` · sha canonical ตรง · ไม่มี traceback
    🔴 (6) **NEGATIVE CONTROL:** บรรทัด (3) ตอนขั้น 3 (พื้นว่าง) ต้อง**ไม่มี หรือ `items=0`** · ได้ `items >= 1` ตอนพื้นว่าง = **finding ต้องรายงาน**
    **ชั้นนี้ตอบไม่ได้เลยว่าบนจอผู้เล่นเห็นของอยู่หรือหาย**
  - **client-observable** (ต้องมีตาคน · ห้ามอนุมานจากคอนโซล):
    (7) `S1` เห็นโมเดล + ป้ายชื่อของบนพื้น **ก่อน** เปิดกระเป๋า
    (8) 🔴 `S2` (แผงกระเป๋าเปิด) **ยังเห็นของชิ้นเดิม ตำแหน่งเดิม** — พื้นว่าง = **FAIL ชั้นนี้ และคือข้อบกพร่องที่ใบนี้เปิดมาจับ ⇒ ผลนั้นมีค่า ต้องส่ง**
    (9) `S3` (ปิดกระเป๋า) ยังเห็นของที่เดิม
    (10) บันทึกสีป้ายชื่อทุกป้ายในเฟรม หนึ่งบรรทัดต่อป้ายต่อภาพ ครบ `S0`-`S3` · ไม่มีป้ายเขียน `none` ห้ามเว้นว่าง · อ่านจาก**ภาพนิ่งเต็มความละเอียดเท่านั้น** · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น)
    (11) 🔴 **`G-FRAME` ทุกภาพที่ยกมาอ้าง:** `FRAME: <ไฟล์>  t=+<วินาที> จาก T0=<ISO+07:00>  dist=<หน่วยเกม> ถึงจุดที่ของตก` (วัด `dist` ไม่ได้เขียน `dist=unmeasured` ห้ามเว้นว่าง) · จดหมายผลต้องมีบรรทัด `UNMEASURED_DIST: <n>/<ทั้งหมด>`
    🔴 (12) **`S0` ไม่ใช่หลักฐานของข้อ (8)** — รอบที่เปิดกระเป๋าตอนพื้นว่างอย่างเดียว = `NO-RESULT: ไม่มีของบนพื้นตอนเปิดกระเป๋า` **ห้ามอ่านว่า PASS**
  🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <ISO+07:00>` เท่านั้น (`G-OBS`) · หลักฐานครบแต่ไม่มีลายเซ็นคน = `AWAITING-OBSERVER` **ไม่ใช่ PASS ไม่ใช่ FAIL**

- prediction (**คำทำนาย ไม่ใช่ผลวัด** · ทำนายผิด = finding): P1 โทเคน `items>=1` **และ** `S2` เห็นของ ⇒ ผ่านสองชั้น · P2 ไม่มีโทเคนเลย ⇒ `NO-RESULT` ชี้ที่บิลด์ ไม่ใช่โค้ด · P3 มีโทเคนแต่ `S2` พื้นว่าง ⇒ **ผลที่มีค่าที่สุด** ชี้ที่รูปเฟรม/ลำดับส่ง = ใบถัดไปของ **LANE-B** · 🔴 **ผลลบมีค่าเท่าผลบวก** P2/P3 ส่งงานคนละสาย

- nonclaims: ① ไม่ผูก/ไม่เกรดร่วมกับ `GT-223` ② ไม่พิสูจน์ว่าเก็บของหลังปิดกระเป๋าได้ (คนละใบ) ③ ไม่พิสูจน์ว่า `0x4B98` เป็น action เดียวที่ล้างพื้น ④ ไม่ตัดสินว่า reply 44 B "ควร" มีรูปอะไร ⑤ ไม่แตะสาเหตุสีป้าย (`RE-067`) · ไม่พิสูจน์อะไรบน canonical (บูตบนสำเนา)
- links: `20260904_1430_KA1A-R309-RESULTS-*` finding 1 · `COO 20260904_1648` ข้อ 2 · `COO 20260904_1649` ข้อ 2 · `COO 20260904_1247` (chief ห้ามประกอบเฟรมดรอปเอง) · `runtime.py:10110-10160` · `mob_loot.py refresh_frames` · `mob_drop_presence.py CONSOLE_TOKEN` · `GT-188` cp2 (กลไกเดียวกัน) · `GT-215` (วินัย db/teardown)
- numbering: ตัวนับร่วม (กฎ ②) คืน `240` · `RE-241` ลง `CLIENT_RE_QUEUE.md` ⇒ ใบนี้ `242`
- result: **R316 2026-09-05T11:02+07:00** (พับโดย LANE-K รอบ `n3s0rg`, คัดลอกคำต่อคำจาก `notes_to_chief/20260905_1102_KA1A-R316-RESULTS-*.md`, ยกมาไว้ตรงนี้เพราะเป็นครั้งเดียวที่ใบนี้เคยถูกวัดจริง — ดูจดหมายต้นฉบับสำหรับ hex/ภาพเต็ม):
  wire/DB: (1) `MOB_LOOT_DROPS_CENSUS ... items=2400046:x1,2204801:x1` + `MOB_DROP_PRESENCE live=2 announced=2` ✓ (2-ใหม่)(3) `CheckSecondPwdVital` 64B ขาเข้า → reply 44B → ทันทีตามด้วย `GROUND_REANNOUNCE_AFTER_SECOND_PWD scene='Bg0002' items=2` ✓ (4) `oldest_left` หลังขั้น 5: ไม่มีบรรทัดใหม่หลัง reply (ไม่ได้ฆ่าเพิ่ม) = **NO-RESULT เดี่ยว** (5) integrity ok · canonical sha ไม่เปลี่ยน (`4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454`) · traceback 0 (6) negative control (พื้นว่าง เซสชัน 1): ไม่ใช่ `items=0` ธรรมดา แต่เป็น `GROUND_REANNOUNCE_AFTER_SECOND_PWD_REFUSED reason=refused_cell_has_no_scene_to_publish` = finding ก (บันทึกไว้ ไม่ตัดคะแนน)
  client-observable: (7)(8)(9) ของ (Blood/Exile crystal) อยู่ก่อนเปิด/ระหว่างเปิด (กระพริบหนึ่งที)/หลังปิด ✓ ภาพ `104708.png` (10) สีป้ายบันทึกแล้ว (มอนชมพู ของส้ม/แดงเข้ม) (11) `UNMEASURED_DIST: 4/4`
  `OBSERVER_CONFIRMED: 2026-09-05T10:50+07:00`
  หมายเหตุ: R316 ใช้สองเซสชัน (negative control เซสชัน 1, วัดจริงเซสชัน 2) ต่างจาก steps ในใบนี้ที่สั่งเซสชันเดียว — ผู้เขียนจดหมายอธิบายว่าเซสชันแรกเปิดกระเป๋าตอนพื้นว่างไปแล้วก่อนมีของ (เห็น negative control ไปแบบไม่ตั้งใจ) จึง relogin ทำเซสชันใหม่เพื่อให้ "เปิดกระเป๋าครั้งแรก" ตรงกับตอนมีของจริงตามที่ใบต้องการ

**ผู้เปิดใบ: chief (LANE-E) รอบ `oi2r2n`/R340 ตาม `COO-DECISION 20260904_1648` ข้อ 2 -- ผู้บริโภคผล: chief (LANE-E)**


---

## GT-114 DIAG-MULTI-OBJECT-001 [attended, in-game]: five diagnostic objects at the city-center test point (X=11865, Y=6147), each one field away from control D0 -- does each single-field difference produce the on-screen effect that field is predicted to control, jointly closing the attended half of RE-107/RE-108/RE-109's own proposed follow-ups  [CANCELLED - covered by R309 (D0 · RE-108) / refuted by production DYING_TIMER_SECONDS=20 (D1a · ภาพ 185937) / covered by GT-129 (D1b) / D2 control-only / covered by GT-084-R2 + P-2/RE-067 (D3) — Panya agreed 2026-09-04 21:4x · ปิดโดย chief รอบ `epkucn`/R344 2026-09-04 22:56 +07:00 ตาม `COO-DECISION 20260904_2158` (ถอน `2142` ข้อ 2 = ไม่พ่วงบูตกับ `ATTACK-POSE-ONE-FIELD-AB-001`) · กฎ `PANYA-DECISION 20260903_1934` · เหตุผลรายข้ออยู่ใน `notes_to_chief/20260904_2133_KA1A-TO-COO-attack-pose-*` §1 · เดิม: PENDING -- wiring landed R202 (9b6zl6)]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-114`/`RE-114` = 0 hits in both files, archive included (2026-08-27, this round). Highest number in use is `113` (`RE-113`, CLOSED PASS/DONE) => this entry is `114`.
> Entries `RE-085`-`RE-113` and `GT-101`-`GT-110` stay exactly where they are, unchanged -- this is a new entry, not a replacement for any of them.

### source
PANYA-ORDER 18:55+07:00 + ADDENDUM 19:05 (`notes_to_chief/20260827_1855_PANYA-ORDER-diag-multi-object-boot-one-round-answers-RE107-108-109.md`) asked for one boot, five objects, each one field from a shared control D0, byte-diff-proven before any human round. LANE-B built the composition layer that round: `src/pirateforce_foundation/mob_diag_multi_object.py` (`tests/test_mob_diag_multi_object.py` all green). Builds the five `DiagObject` records, prints `describe_boot()`; sends nothing, not called from `runtime.py` yet. RE-107/108/109 are each CLOSED BOUNDED-NEGATIVE/DONE, each proposing this kind of narrow attended capture as its own next step -- this entry is that follow-up.

**CORRECTED, LANE-B round following PANYA-DECISION 2026-08-27T20:10+07:00 "M1-P" item 3**: the body is Mountain Deer, MOBS n_ID 27 (per that same letter's ADDENDUM 20:18), NOT Jungle Big Tiger (template 60), which this entry originally named -- see nonclaim (10) below for the full swap history. `mob_diag_multi_object.DIAG_BODY_TEMPLATE_ID` is now `27`; its stats are hand-mined from `CONSTDATA_TH__MOBS`/`MOBS_TIP`/`STANDARD_MOB` directly (Mountain Deer is not a member of either bg0001's or the newly-mined Bg0002's generated roster -- its `s_OUTFIT` is a two-variant list that fails the mining tool's outfit-unambiguous selection rule). `mob_death.WIDENING_RULINGS` carries a new, dedicated entry for template 27, scoped to scene "bg0001" (where these five objects are actually placed, not Bg0002). Still `BLOCKED-ON-WIRING` -- this round corrects which monster the ticket names, it does not unblock it.

### objective
One boot, five position-distinguished objects, each one field from D0, five independent readings in one sitting:
- D0: does a left-click open the target panel, does Tab (RE-108)
- D1a: does the corpse fall/animate once DEAD is held back 20s instead of 700ms, or freeze like production (RE-107 "DEAD too fast" branch)
- D1b: does a dead-only frame (no DYING), sent only after a prior TargetVital for that identity, fall/animate or freeze (RE-107 "model-loaded bit" branch)
- D2: a second on-screen D0 at another position -- a repeat-control reference point, NOT a new value (nonclaim 4)
- D3: a body without the hostile faction splice (plain-town-NPC shape, same template/HP/name) -- clickable/hittable at all? what name colour?
A reading on one object never substitutes for another (nonclaim 3).

### db
default_state\pirateforce.sqlite3 -- copy only, canonical never opened. Copy to `pf_bridge\backup\pirateforce_before_GT-114_<yyyyMMdd_HHmmss>.sqlite3`, then `state\run_gt114.sqlite3`. sha256 vs `CANON_SHA.txt` before/after; `PRAGMA integrity_check=ok` on the working copy both times.

### server args
WIRED R202 (9b6zl6). No new server CLI flag -- the diagnostic is gated by an on-disk
allowlist, not a `--scenario` argument: create `config/diag_multi_object.json` (or set
`PF_DIAG_MULTI_OBJECT_CONFIG` to point elsewhere) with `{"diag_multi_object_accounts":
["<the attended test account name, exact case>"]}` on the machine that boots this
ticket, BEFORE boot. No file / account not listed = zero behaviour change (pinned by
`tests/test_diag_multi_object_runtime_wiring.py`, run through the real dispatcher, not
just the composer). Boot with no other flag; log in with the listed account; reaching
the bg0001 arrival census (first TargetPos after the runtime ack) prints exactly 5
`DIAG object=<D#> variant=<...> identity=0x<...> pos=(<x>,<y>,<z>)` lines, one per
object in D0/D1a/D1b/D2/D3 order, plus one `DIAG_CENSUS assembled=5 census=115 wire=120
...` line. `world_census_actor_count` stays 115 -- the +5 lives in the frame bytes, not
the census count that gates later recomposes (see `diag_multi_object_wiring.
census_frames()`'s own docstring for why an inflated count there would break every
later hit). D0/D1a/D1b/D2 resolve as combat targets immediately; D3 does too but is not
expected to reach 0 HP this round.

### steps (fill in once server args above holds a real command line)
1. LOCK_GAME; confirm exactly 5 `DIAG object=...` console lines before opening the client -- otherwise BLOCKED, do not boot.
2. Boot, log in, reach (X=11865, Y=6147); record HUD X/Y.
3. NO-CRASH: right-click-drag camera 360 degrees only (never WASD/Q/E -- those move the character and emit TargetPosVital).
4. Per object: visible immediately or late (model-load lag, free data).
5. D0: photo (name colour), click once, photo, Tab, photo; attack to 0 HP, photo death + result.
6. D1a: attack to 0 HP, wait a full 25s, photo result.
7. D1b: click once (emits TargetVital), then attack to 0 HP, photo result.
8. D2: photo name colour before click / after click / after death.
9. D3: photo name colour; try one click and one attack; record if either registers.
10. NO-CRASH again; log out; teardown via `TEMPLATE_teardown_generic.ps1` (stamp under 420 min); recheck canonical sha256; sha256 every capture.

Colour rule (per Panya's order 2026-08-25): one line per label per image, write "none" not blank, full-res stills only (never a contact sheet/video), never infer a cause -- RE-067 is open and is the only place that question lives.

### pass criteria (two layers)
wire/DB: (a) exactly 5 `DIAG object=...` lines matching `describe_boot()`; (b) the module's own pre-human byte-diff (signed off per pf-adversary, run before this ticket is ever booted) shows D1a/D2/D3 differ from D0 only in the one named field, D1a/D1b death frames differ only in schedule timing; (c)/(d) canonical sha256 + integrity_check ok before/after.
client-observable: five separate readings, none substituting for another -- D0 panel/click/Tab + name colour; D1a fall/freeze after 20s hold (either is a finding, not a failure); D1b fall/freeze on dead-only-after-TargetVital; D2 name colour before/after click/death; D3 name colour + does click/attack register at all. All colours per the colour rule.

### nonclaims
(1) WAS blocked pending chief wiring `GT_DIAG_MULTI_OBJECT_WIRING`; landed R202 (9b6zl6), see server args above -- kept as history, not deleted, per queue rule. (2) Does not itself produce the required pre-human byte-diff proof. (3) Bundles five readings into one boot on the owner's own instruction; each stays independently reported. (4) D2 here is a byte-identical repeat of D0, NOT the GT-032 alternate-faction-value object the original order's table named -- that needs a value with provenance RE has not produced yet. (5) Does not test the player's own orange name (ADDENDUM 19:05 excludes it). (6) Does not decide the cause of any colour observed -- RE-067 only. (7) City-center placement is diagnostic only, not a real field-placement claim. (8) D1b's gate is only as good as whatever session state the eventual wiring actually tracks -- if it tracks nothing, the wiring reply must say so. (9) `DIAG_CENTER_Z` (2231.17) is a nearest-neighbour estimate from `population.py`'s own census (~931 units away), not a terrain query at this exact point -- objects rendering mid-air/underground is itself a result to record, not a reason to abort silently. (10) ~~DOUBLY BLOCKED as of ADDENDUM 20:18 (+07:00, same day, landed after this ticket was drafted): the owner named Mountain Deer (MOBS n_ID 27) as the body for all five objects, superseding this round's Jungle Big Tiger (template 60) pick -- Mountain Deer needs a fresh mine (not in bg0001's roster) and a new `mob_death.WIDENING_RULINGS` entry (template 27 not covered by the existing bg0001 ruling). Next LANE-B round's work; do not boot this ticket against the current module without that swap landing first.~~ DONE, the LANE-B round after this one (PANYA-DECISION 2026-08-27T20:10+07:00 "M1-P" item 3): Mountain Deer's row is hand-mined (it is not a member of ANY generated roster, bg0001's or the newly-mined Bg0002's -- both mining runs exclude template 27 on the same outfit-ambiguity ground) and `mob_death.WIDENING_RULINGS` carries a dedicated entry for template 27. Still BLOCKED-ON-WIRING for the unrelated reason nonclaim (1) already names. (11) THE SWAP TRADES AWAY PART OF ADDENDUM 19:05's ORIGINAL JUSTIFICATION FOR AN AGGRO MONSTER: Mountain Deer's own `n_AI_WANDER` (16) maps to `n_AGGRO` 0 in `field_mob_ai_tables.AI_WANDER_ROWS` -- it is NOT an aggro monster, unlike the Jungle Big Tiger pick it replaced (`n_AI_WANDER` 11, `n_AGGRO` 1200). It still grants EXP (`f_RATIO_EXP` 1.0, same contrast this ticket's original criterion used). The owner's later, more specific ADDENDUM 20:18 instruction is followed as given rather than re-argued; this is recorded so a reader of "unmistakably born as a monster" (ADDENDUM 19:05's own phrase) knows which half of that phrase the final body actually satisfies. (12) NEW R202: D1b (step 7 above) has NO death handling this round -- nothing in this codebase tracks "has this client already been sent a TargetVital for this identity", so `dead_only_schedule`'s refusal is never bypassed with a guessed `target_vital_seen=True` (see `diag_multi_object_wiring.D1B_UNWIRED_REASON`). Step 7 will still show a result (photo it as instructed) but expect NO dying/dead frames from the server for D1b specifically -- the client's own local reaction (if any) to a target reaching 0 HP with no server death frames IS itself the reading this object was built to produce, not a wiring bug to report. A follow-up CORE-REQUEST (a per-session set of TargetVital'd identities) would be needed to answer D1b's original question with a real "yes it was sent" rather than this negative result.

### result
(tester fills this in)

**ผู้เปิดใบ: LANE-B -- archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00**

---

## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log  [❌ **CANCELLED - refuted by R306 finding 3 (`notes_to_chief/20260903_1655_*`)** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — รูป same-scene ที่มีพิกัดส่ง `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS` แล้ว **ไคลเอนต์ปิดตัวเอง** (`ErrorData=28317`) วัดบนจอเจ้าของ ⇒ คำถามของใบนี้ ("ตัวละครขยับไปพิกัดนั้นไหม") ตอบไม่ได้ด้วยรูปเฟรมที่มีอยู่ และ `COO-DECISION 20260903_1744` ข้อ 3 สั่งปิด `/warp` แบบมีพิกัดไปแล้ว · 🔴 **เปิดใบใหม่ (ไม่ใช่ปลดใบนี้) เมื่อ LANE-GM เปลี่ยนรูปเฟรมและมี headless proof** — ใบใหม่ต้องเขียนเกณฑ์บนรูปเฟรมใหม่ ไม่ใช่ยกด่านเก่าทั้งชุดมาใช้ · สถานะเดิม: ~~BLOCKED — token compares nothing (COO-DECISION 20260829_0041)~~ **STILL BLOCKED — token fixed, but a separate COO-held gate remains (see chief R243 update at end)**: ห้ามเกรด ห้ามบันทึกผลใด ๆ ด้วยโทเคน `GM_WARP_POSITION_CONFIRMED` ตัวปัจจุบัน เพราะมันเทียบแค่ "แถวเปลี่ยนค่า" ไม่ได้เทียบกับ**จุดที่สั่ง** · ปลดเมื่อชุดแก้โทเคน+audit ลง main (chief, ภายใน 2026-08-29 23:59+07:00) · **อัปเดตรอบ `nz0qt2`:** ครึ่ง audit ที่เป็นเขต LANE-GM (แถว `outcome`, `CORE-REQUEST-GM-032` ข้อ 1-2) อยู่ใน PR `pirate-force-server#223` **รอ merge** · ครึ่งโทเคน (`GM_WARP_POSITION_TARGET_MATCH/MISMATCH`, `CORE-REQUEST-GM-031`) และข้อ 3 ของ GM-032 ยังเป็นของ chief ⇒ ป้าย BLOCKED ของใบนี้ **ยังไม่ถูกปลด** ด้วยรอบนี้ · 🔴 **เหตุผลที่วัดแล้ว ไม่ใช่แค่เหตุผลเชิงหลักการ** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `xk4wmz`): pf-adversary วัดว่าโทเคนตัวปัจจุบัน **ยิงตอนผู้เล่นเดินเองหนึ่งก้าว**หลัง warp ที่ไคลเอนต์เมิน ⇒ ใบนี้ "ผ่าน" ได้โดยที่ warp ไม่ทำงานเลย · **ของที่ LANE-GM ทำเสร็จแล้วเพื่อชุดของ chief:** `gm/warp_target_record.py` เก็บปลายทางของ warp ใบนั้นไว้เทียบได้ หยิบได้ครั้งเดียว ผูกกับ `character.id` (รอบ `z6gu2n` บน main แล้ว) และ `CORE-REQUEST-GM-031` ขอให้ chief พิมพ์ `GM_WARP_POSITION_TARGET_MATCH` / `..._MISMATCH` **เพิ่ม** จากโทเคนเดิม (ห้ามเอา match มาเป็นเงื่อนไขของโทเคนเดิม -- วันนี้ client เมิน `ForcePos` ผลที่คาดคือ MISMATCH ถ้ารวมกันโทเคนจะหายทั้งใบ) · BLOCKED x4 รวมข้อนี้ (~~x3~~ ~~x2~~ นับผิดมาแต่แรก มีสามข้อมาตลอด) -- ห้ามบูต: (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่คืน action ที่สาขา `0xAC52`) · **อัปเดตรอบ `vvxkft`:** ตัวโมดูล `gm/chat_command_action.py` เองก็เพิ่งกลับขึ้น main รอบนี้ (PR #204 -- PR #200 ของรอบ `gr2q9j` ถูกปิดเพราะ gate แดง ไม่เคย merge) และ GM-029 เปลี่ยนความหมายเป็น "**แทนที่**บรรทัด `fire()` ของ GM-028 ในคอมมิตเดียว" ไม่ใช่ "เพิ่มจุดเรียก" (ใบ `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md`) ⇒ วันที่ใบนี้บูตได้ `GT-127` จะใช้ไม่ได้ตามเกณฑ์เดิมอีกต่อไป เพราะ event เปลี่ยนเป็น `gm_chat_action_*` -- **บูต `GT-127` ให้จบก่อน** (ข) ~~`RE-129` ยังไม่ตอบ~~ **RE-129 ตอบแล้ว 2026-08-28T20:09+07:00 (`ForcePos vital_version = 0`) แต่ข้อนี้ยังบล็อกอยู่ด้วยเหตุใหม่:** `COO-DECISION 20260828_2130` ล็อกแข็งว่าห้ามเปลี่ยน `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main (`CORE-REQUEST-GM-030`, รอบ `fo2lgh`) **แม้ RE-129 จะตอบก่อนก็ตาม** ⇒ โมดูลยังปฏิเสธการส่งด้วยตัวเอง และตอนนี้มีเทสบังคับด้วย (`pirate-force-server/tests/test_gm_force_pos_version_lock.py` แดงถ้าเปลี่ยนค่าก่อนโทเคน `GM_WARP_POSITION_CONFIRMED` อยู่บน main) · เหตุผลชั้นที่สองจาก RE-129 เอง: handler ที่ client จดทะเบียนไว้สำหรับ `ForcePos` = `mov al,1; ret 4` ไม่อ่าน payload ⇒ **version ถูกไม่ได้แปลว่าจะขยับ** ใบนี้ยังเป็นใบเดียวที่ตัดสินข้อนั้นได้ (ค) ~~🔴 **คำถาม "ใครเป็นเจ้าของตำแหน่งหลัง warp" ยังไม่มีคำตอบ**~~ **ตอบแล้ว 2026-08-28T21:30+07:00 (`COO-DECISION`): เจ้าของคือตำแหน่งที่ client ยืนยันแล้ว · เซิร์ฟเวอร์ห้ามเขียนตำแหน่งที่ตัวเองไม่ได้สังเกตเห็น · ตัวยืนยันคือ `TargetPos` ใบแรกหลังเฟรม** ⇒ ข้อนี้เหลือ "รอการเดินสาย" ไม่ใช่ "รอคำตอบ" -- ปลดเมื่อ `CORE-REQUEST-GM-030` ลง main และ COO ปลดล็อก · ผู้เทสต้องบันทึกในผล: หลัง warp ให้เดินหนึ่งก้าวเพื่อบังคับ `TargetPos` แล้วดูว่าคอนโซลมี `GM_WARP_POSITION_CONFIRMED` หรือไม่ · **บริบทเดิมของข้อนี้ (เก็บไว้):** — pf-adversary รอบ `gr2q9j` ชี้ว่า หลังส่ง `ForcePos` แล้ว แถวใน DB และ `selected.position` ยัง**ค้างที่จุดเดิม** (โมดูลไม่เรียก `foundation.checkpoint`) ⇒ client อยู่จุดใหม่ เซิร์ฟเวอร์คิดว่าอยู่จุดเก่า · aggro/pickup/logout ใช้จุดผิด · ต้องได้คำตอบ (`ASK-COO` รอบนี้) **ก่อน**เปลี่ยนค่าคงที่ของ `RE-129` ไม่ใช่หลัง · **อัปเดตรอบ `38c4tv` 2026-08-29T08:22+07:00 (LANE-GM เจ้าของใบ) — เพิ่มด่านก่อนบูตข้อ 4 ไม่ได้ปลดหรือเพิ่มบล็อก:** จดหมาย chief `20260829_0604` ข้อ ②bis (ก) วัดได้ว่าล็อกอินที่ใช้ override ฉากเป็น **visit** ⇒ ไม่เขียนแถวตำแหน่ง ⇒ `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** บนเซสชันนั้น · ใบนี้ตัดสินด้วยโทเคนนั้น จึงต้องยืนยันก่อนบูตว่าบัญชีไม่มีใบล็อกอินค้าง ทั้ง `gm_login_scene.json` และ `gm_login_scene_standalone.json` (ดูด่านข้อ 4) 🔴 กับดักซ้อน: ขั้นตอนข้อ 4 ของใบนี้เอง (`/warp <ฉากอื่น>`) เป็นตัวสตางค์ใบนั้น · **อัปเดต chief รอบ `3ru85y` (R243) 2026-08-30T~16:xx+07:00 — CORE-REQUEST-GM-030/031 wired, แต่ตัวบล็อกจริงของใบนี้ยังปิดอยู่:** `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` พิมพ์แล้วจริง เพิ่มจากโทเคนเดิม ไม่แทนที่ (พิสูจน์ headless: warp ตรงพิกัด -> MATCH หนึ่งบรรทัด, warp ผิดพิกัด -> MISMATCH พร้อมระยะ, เดินเองไม่มี warp -> ไม่มีทั้งคู่, target ค้างข้ามเฟรมไม่เกิด — เทสใหม่ 5 ใบใน `tests/test_gm_warp_position_confirmed.py`, สวีตเต็ม 5480 passed) · 🔴 **pf-adversary พบ**: กิ่ง `unknown_character_mismatch` ที่ `CORE-REQUEST-GM-031` ข้อ 5 ขอ เป็น **dead code ในโปรดักชัน** — ลำดับการ์ดเดิม (`character_changed` early-return) ดักทุกกรณี re-select จริงไว้ก่อนกิ่งใหม่จะถึง เทสที่พิสูจน์กิ่งนี้ต้อง park เป้าหมายตรงผ่าน `record_warp_target` เอง ไม่ใช่ผ่านเส้นทาง `/warp` จริง — [ไม่อ้าง] ว่ากิ่งนี้ทำงานได้จริงในโปรดักชัน คงไว้เป็น defense-in-depth ตามที่คอมเมนต์ใหม่ใน `runtime.py:_gm_warp_open_confirm_window` บันทึกไว้ ส่งคำถามลำดับการ์ดนี้ต่อให้ LANE-GM/COO ตัดสินว่าจะแก้หรือรับสภาพ (ดูจดหมาย `CHIEF-REPLY` รอบนี้) · pf-adversary ยังพบบั๊กเดิมที่ไม่เกี่ยวกับ diff นี้ (rearm เป็นตัวละครอื่นก่อนมี TargetPos ทำให้ `gm_warp_pending_character` ค้างชื่อเก่า แล้วโทเคนทั้งชุดเงียบทั้งเฟรมของตัวละครใหม่) — ไม่แก้รอบนี้ (นอกขอบเขตใบ) รายงานไว้ให้ทราบ · ~~🔴🔴 **ตัวบล็อกจริงของใบนี้ทั้งใบยังไม่ปลด**: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` ยังเป็น `None`~~ **อัปเดต chief รอบ `9fv1m8` (R253) 2026-08-31T~02:1x+07:00: ค่าคงที่ปลดแล้ว** (`teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = 0`, ตาม `COO-DECISION 20260830_1645`/`1742` -- ค่า RE-129 literal ไม่ใช่การอ่านชื่อ `*_PROVEN_BY_RE129`) พร้อมแก้เทส 13 ใบใน 6 ไฟล์ที่พึ่งค่า shipped เดิมโดยไม่ patch ตรง ๆ (pf-adversary รีวิวผ่านก่อน commit) สวีตเต็ม 5600 passed 0 failed เขียว(cloud sanity) · **รอ merge ก่อน** -- `pirate-force-server` PR ของรอบ `9fv1m8` ยังไม่ merge เช็ค `PR_STATE.txt` ก่อนบูต · ไบต์ `ForcePos` จะออกสายจริงเมื่อ merge แล้วเท่านั้น · ตัวบล็อกที่เหลือของใบนี้ (ลำดับการ์ด `unknown_character_mismatch` dead-code ที่ pf-adversary พบรอบ `3ru85y`, และ rearm-character bug ที่ยังไม่แก้) **ยังไม่ปลด** -- นี่คือแค่การเปิดสายไบต์ ไม่ใช่การปิดใบ ผู้เทสยังต้อง ยันหน้าจอจริงตามด่านเดิมของใบนี้]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md` · รอบ `gr2q9j` จอง `RE-129` ที่นั่นและ `GT-128` ที่นี่
> grep ยืนยันก่อนจอง 2026-08-28T18:2x: `GT-128` / `RE-129` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า = `GT-127` / `RE-128`

### ต่างจาก GT-127 อย่างไร (สองใบนี้ไม่ซ้ำกัน อย่ารวม)
`GT-127` ตัดสินที่ **ndjson audit log** = "เซิร์ฟเวอร์อ่านบรรทัดที่ GM พิมพ์ได้ไหม" (ครึ่งอ่าน)
`GT-128` ตัดสินที่ **จอ** = "แล้วมีอะไรเกิดขึ้นกับตัวละครไหม" (ครึ่งส่ง) · จุดเรียกเดียวกันปลดทั้งสองใบ
แต่ `GT-128` ต้องรอ `RE-129` เพิ่มอีกใบ ⇒ `GT-127` จะบูตได้ก่อนเสมอ

### ด่านก่อนบูต (~~ทั้งสาม~~ **ทั้งสี่** ต้องผ่าน มิฉะนั้นเลื่อน ห้ามบูต)
> นับผิดมาหนึ่งรอบ: ข้อ 4 เพิ่มโดยรอบ `38c4tv` แต่หัวข้อยังเขียนว่าสาม — pf-adversary จับได้
> ก่อน push · ผู้เทสที่อ่านหัวข้อแล้วนับถึงสามจะไม่เคยรันข้อ 4 เลย
1. grep บน `main` เจอจุดเรียก `make_gm_chat_command_action` จริงที่สาขา `0xAC52` ของ `runtime.py`
   (ไม่ใช่แค่ PR merged -- ต้องเห็นบรรทัดบน main)
2. `grep -n "FORCE_POS_VITAL_VERSION_CONFIRMED" src/pirateforce_foundation/gm/teleport_wire.py`
   ต้อง**ไม่ใช่** `None` และคอมเมนต์เหนือมันต้องอ้าง `RE-129` ที่ปิดแล้วพร้อม VA
3. บัญชีที่เจ้าของจะบูตอยู่ใน `gm_accounts.json` (ค่าเริ่มต้นว่าง = ไม่มีใครเป็น GM)
4. 🔴 **ด่านใหม่ ต้องผ่านด้วย** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `38c4tv` 2026-08-29T08:22+07:00
   หลัง `pirate-force-server#236` merge — เหตุมาจากจดหมาย chief `20260829_0604` ข้อ ②bis (ก)):
   **บัญชีที่จะบูตต้องไม่มีใบล็อกอินฉากค้างอยู่** ทั้งสองแฟ้ม —
   `grep -c '<ชื่อบัญชี>' config/gm_login_scene.json config/gm_login_scene_standalone.json`
   ต้องได้ `0` ทั้งคู่ (ไฟล์ไม่มี = ผ่าน)
   เหตุผลที่ **วัดแล้วในโค้ด ไม่ใช่ข้อควรระวัง**: ล็อกอินที่ใช้ override เป็น **"การไปเยือน"**
   (`runtime.py` ตั้ง `login_scene_override_visit = True`) ⇒ เซสชันนั้น **ไม่เขียนแถวตำแหน่งผ่าน
   checkpoint ของ TargetPos เลย** (ถ้อยคำแคบลงหลัง pf-adversary ชี้: จุดเขียนของ world-travel departure
   ที่ `runtime.py:6139` อยู่ **นอก** guard ตัวนี้ — วันนี้เข้าไม่ถึงเพราะประตู walk-in ปิดอยู่ทั้งหมด
   คอนโซลพิมพ์ `WORLD_TRAVEL_INERT` ทุกเซสชัน แต่ถ้อยคำเดิม "ไม่เขียนแถวตำแหน่งจริงเลย" เป็นจริง
   เพราะแฟล็กตัวนั้น ซึ่งด่านนี้ไม่ได้เอ่ยถึง)
   ⇒ โทเคน `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** เพราะไม่มีการเขียนจริงให้รอด
   ⇒ ผู้เทสที่เดินตามขั้นตอนข้อ 3 จะเห็นคอนโซลเงียบ แล้วบันทึก FAIL ให้ `/warp`
   ทั้งที่สาเหตุคือใบล็อกอินที่ค้างอยู่ ไม่ใช่ warp
   🔴 กับดักนี้เกิดง่ายเป็นพิเศษกับใบนี้: `/warp <ฉากอื่น>` **สตางค์ใบล็อกอินให้บัญชีเดียวกัน**
   (ขั้นตอนข้อ 4 ของใบนี้เอง) ⇒ ถ้าเทสรอบก่อนพิมพ์คำสั่งนั้นแล้วไม่ได้ล็อกอินกินใบทิ้ง
   ใบยังค้างอยู่ข้ามรอบ · ใบ GM-gated ถูกกินโดยล็อกอินถัดไปหนึ่งครั้ง (`COO-DECISION 0441` ข้อ 2)
   แต่ใบใน **แฟ้ม standalone ไม่ถูกกินเลย** (`COO-DECISION 0542`) ⇒ ค้างจนกว่าจะลบด้วยมือ
   🔴 **grep ที่ path ไหน — อย่าเชื่อ path ปริยาย** (แก้โดย pf-adversary ก่อน push รอบ `38c4tv`):
   ตัว resolve อ่าน **ตัวแปรสภาพแวดล้อมก่อน** แล้วค่อยตกมาที่ path ปริยายซึ่งอิง cwd ⇒ ตรวจตามลำดับนี้
   `echo %PF_GM_LOGIN_SCENE_CONFIG%` และ `echo %PF_GM_LOGIN_SCENE_STANDALONE_CONFIG%` — ตั้งไว้ก็ grep ไฟล์นั้น
   ไม่ได้ตั้งจึงใช้ `config\gm_login_scene.json` และ `config\gm_login_scene_standalone.json`
   **เทียบจาก cwd ที่บูตเซิร์ฟเวอร์จริง ไม่ใช่จากรากรีโป** · `config/` อยู่ใน `.gitignore` (`/*`)
   ⇒ ในโคลนใหม่จะ **ไม่มีโฟลเดอร์นี้เลย** ซึ่ง = ผ่าน ไม่ใช่ = ตรวจไม่ได้
   วิธีเคลียร์: ลบบรรทัดของบัญชีนั้นออกจากทั้งสองแฟ้มก่อนบูต
   🔴 **สิ่งที่คอนโซลยืนยันให้ไม่ได้ ถ้าไม่บูตด้วย `--export-events`** (pf-adversary วัดแล้ว):
   `gm_login_scene_override_applied_*` และ `gm_login_scene_override_visit_no_durable_write_scene_*`
   เป็น `self.events.append` **ล้วน ๆ** ไม่มีที่ไหนใน `runtime.py` พิมพ์ `self.events` ออกมาเอง —
   ทางเดียวที่ออกจอคือ `--export-events` (`app.py`) และรูปที่พิมพ์คือ `PF-EVENT <seq> <event>`
   ⇒ **ถ้าบูตธรรมดา คอนโซลเงียบทุกกรณี** ⇒ "ไม่เห็นบรรทัดนี้" ไม่ใช่หลักฐานว่าไม่มีใบค้าง
   มันคือด่านที่ตอบ PASS ได้อย่างเดียว ซึ่งเป็นความล้มเหลวแบบเดียวกับที่ด่านนี้ถูกเขียนขึ้นมากัน
   ⇒ **ตัว grep สองแฟ้มข้างบนคือด่านจริง** · จะยืนยันซ้ำที่คอนโซลก็ได้ **ต้องบูตด้วย `--export-events`**
   (ตรวจก่อนว่ามีจริง: `git grep -n 'export-events' <SHA> -- src/pirateforce_foundation/app.py`)
   แล้ว grep แบบ substring บนบรรทัด `PF-EVENT` ไม่ใช่ grep ชื่อ event เปล่า ๆ

### ขั้นตอน (ที่ใจกลางเมือง X=11865 Y=6147 ห้ามท่าเรือ ตามกฎสายนี้)
1. login ด้วยบัญชี GM รอจนโหลดฉากเสร็จ **จดพิกัดตั้งต้นที่เห็นบนจอ**
2. พิมพ์ในกล่องแชทธรรมดา: `/warp <scene_id ที่อยู่ตอนนี้> 11900 6200` (ขยับสั้น ๆ ในฉากเดิม)
3. บันทึก: ตัวละครขยับไหม · ขยับไปตรงพิกัดที่สั่งไหม · จมพื้น/ลอยไหม (z มาจาก connection ไม่ได้แต่ง)
4. **เคสลบที่ต้องทำด้วย** พิมพ์ `/warp <ฉากอื่น> 1 2` -> ต้อง**ไม่เกิดอะไรขึ้น** (ForcePos ข้ามฉากไม่ได้
   โมดูลปฏิเสธโดยตั้งใจ ไม่ใช่บั๊ก) · และพิมพ์ข้อความธรรมดา (ไม่ขึ้นต้น `/`) -> ต้องไม่มีอะไรผิดปกติ
5. ให้ผู้เล่นธรรมดา (บัญชีนอก `gm_accounts`) พิมพ์คำสั่งเดียวกัน -> ต้องไม่เกิดอะไร และไม่มีแถวใน ndjson

### เกณฑ์สองชั้น
- **ชั้น wire/DB:** คอนโซลเซิร์ฟเวอร์มี label ~~`LANE_GM_CHAT_WARP_FORCE_POS`~~ **`LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS`**
  หนึ่งครั้งต่อหนึ่งคำสั่งที่รับ (แก้โดยผู้เปิดใบ LANE-GM รอบ `w8hnu9` 2026-08-28T23:3x+07:00 --
  ชื่อเดิมในใบนี้ **ไม่เคยตรงกับโค้ด**: ค่าคงที่จริงคือ `chat_command_action.WARP_ACTION_LABEL`
  ซึ่งมีคำว่า `TELEPORT` คั่นกลางมาตั้งแต่รอบ `gr2q9j` เพราะ `runtime.py:3654-3675` ทดสอบ
  substring นั้นเพื่อเปิด grace window ของ move-authority ⇒ ผู้เทสที่ grep ชื่อเดิมจะไม่เจอ
  แล้วบันทึก FAIL ทั้งที่ระบบทำงานถูก · grep ที่ถูกคือ `LANE_GM_CHAT_WARP` ก็พอ)
  · ndjson: ~~**หนึ่งแถวต่อหนึ่งคำสั่ง (ไม่ใช่สองแถว -- สองแถว = เผลอ wire ทั้ง `fire()` และ action)**~~
  **แก้รอบ `dm8o4l` (chief R240, ของที่ LANE-GM ชี้ 2026-08-30T12:33+07:00):** ตั้งแต่ `CORE-REQUEST-GM-032`
  ข้อ 1-2 หนึ่งคำสั่ง = **`issued` + `outcome`** อย่างน้อย และตั้งแต่ `CORE-REQUEST-GM-040` (R237/GM ครึ่งหลัง
  รอบ `dm8o4l`) เพิ่มเป็น **`issued` → `outcome:composed` → `outcome:queued`** ได้ถึงสามแถวต่อหนึ่งคำสั่ง
  (record_id เดียว append-only ไม่ใช่แก้แถวเดิม) ⇒ วิธีจับ double-wire เปลี่ยนเป็น **นับ `record_id`
  ที่ไม่ซ้ำกัน**: หนึ่งคำสั่งต้องได้ `record_id` เดียว · เห็นสอง `record_id` สำหรับบรรทัดที่พิมพ์ครั้งเดียว =
  เผลอ wire สองทางจริง · คนอ่านที่ต้องการทราบสถานะล่าสุดของคำสั่ง ให้หยิบแถว `outcome` ตัวสุดท้ายของ
  `record_id` นั้น ไม่ใช่ "แถว outcome" เฉย ๆ (ดู P1 ของ `GT-127` สำหรับวิธีตัดสินว่า BOOT_COMMIT ของคุณเป็นแบบไหน)
- **ชั้น client-observable:** ตัวละครอยู่ที่พิกัดใหม่บนจอ (ภาพ/คำบอกเล่าของเจ้าของ)

### 🔴 ถ้าจอไม่ขยับ ให้แยกสามสถานะก่อนบันทึกผล (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `tvbiqc` 2026-08-29T22:3x+07:00)
โทเคนใหม่บนคอนโซลเซิร์ฟเวอร์: `GM_CHAT_NO_BYTES_SENT` (โมดูล `gm/chat_command_action.py` ของสาย GM
· ไม่ต้องใช้ `--export-events` · พิมพ์ลง stderr เหมือนโทเคนอื่นของเส้นทางนี้)
| เห็นอะไรบนคอนโซลหลังพิมพ์คำสั่ง | แปลว่า | บันทึกผลว่า |
|---|---|---|
| `LANE_GM_CHAT_ACTION warp route=action` **แล้วตามด้วย** `GM_CHAT_NO_BYTES_SENT ... why=withheld_force_pos_vital_version` | เซิร์ฟเวอร์ **จงใจไม่ส่ง** เพราะเกต version ยังปิด (ด่านก่อนบูตข้อ 2 ไม่ผ่าน) | **BLOCKED ไม่ใช่ FAIL** -- ใบนี้ยังไม่ได้ถูกทดสอบเลย |
| `LANE_GM_CHAT_ACTION warp route=action` **อย่างเดียว ไม่มีบรรทัดที่สอง** | เฟรมออกไปแล้วจริง ๆ | ใบนี้ถูกทดสอบแล้ว จอไม่ขยับ = **ผลลบของจริง** (คือคำตอบที่ `RE-129` ทำนายไว้) |
| ไม่มี `LANE_GM_CHAT_ACTION` เลย | เส้นทางไม่ถูกเรียก (ด่านข้อ 1) หรือบัญชีไม่ใช่ GM (ด่านข้อ 3) | **ห้ามเกรด** กลับไปด่านก่อนบูต |
🔴 ก่อนรอบนี้ สามสถานะนี้หน้าตาเหมือนกันบนคอนโซล ⇒ ใบนี้เคยเกรดผิดได้โดยไม่มีใครรู้

### nonclaims ที่ผลของใบนี้ **ห้าม**ถูกใช้อ้าง
1. [ไม่อ้าง] ว่า warp ข้ามฉากทำได้ -- ใบนี้ทดสอบ **ในฉากเดียว**เท่านั้น (`ForcePos` ไม่มีช่อง scene id)
2. [ไม่อ้าง] ว่า M2 หรือ milestone ใดผ่าน -- **GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน**
   ถ้าใบนี้ PASS สิ่งที่พิสูจน์คือ "เราย้ายตัวละครไปจุดที่อยากเทสได้" ไม่ใช่ว่าการเดินทางในเกมทำงาน
3. [ไม่อ้าง] อะไรเกี่ยวกับ `BT_GM`/`GMUI_BASIC`/`0x51E9` -- คนละประตู (`RE-126` ยังเปิด)
4. [ไม่อ้าง] ว่าคำสั่ง GM อื่น (`npc`/`item`/`lv`/`spawn`/`say`) ทำงาน -- ยังไม่มี wire ทั้งห้าตัว

**ผู้เปิดใบ: LANE-GM (รอบ `gr2q9j`)** -- ผลกลับมาที่สาย GM บริโภค -- archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00

---

## GT-146 PICKUP-CLICK-OPCODE-CAPTURE-001 [attended, in-game]: คลิกซ้ายลงบน element ของตกที่เซิร์ฟเวอร์เราส่งเอง แล้ว **ไคลเอนต์ยิงเฟรมอะไรออกสาย** -- ใบ capture ที่ปลด `RE-125`/`GT-124`/M5  [⚪ **CANCELLED - covered by R303 attended capture 20260902_1755 (46 inbound 0x4543 frames, 2 completed takes), confirmed R306** — ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_0249` ข้อ 1 (ทวงเป็นครั้งที่สองโดย `COO-DECISION 20260905_1649` หลังค้าง 14 ชม.) · **คำถามของใบนี้ถูกตอบบนไวร์ไปแล้ว**: R303 จับเฟรมขาเข้า `0x4543` 46 เฟรมจากการคลิกจริง ยืนยันซ้ำ R306 · หลักฐานที่วัดบนไวร์ชนะคำสั่งที่เขียนจากชื่อใบ (`COO 0249`) · 🔴 **คำถามที่ยังเปิดอยู่ในใบนี้ไม่ได้ปิดไปกับมัน** — `REEMISSION_REDRAWS_THE_LABEL` ย้ายไปอยู่ใต้ `GT-223`/`RE-208` ของ LANE-B ในรอบเดียวกัน ตาม `COO 0249` ข้อ 1 ประโยคท้าย · ~~🔴 BLOCKED - until P-2 closes (NOW) — เงื่อนไขเดียว ไม่มีเงื่อนไขอื่น~~ · ตั้งโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 5 · ที่มา: `NOW.md` หัวข้อ "ห้ามทำจนกว่า P-2 จะปิด" ระบุชื่อใบนี้ตรง ๆ · เงื่อนไข `GT-188` checkpoint 2 **ตัดทิ้งแล้ว** (`GT-188`/`GT-188cp1` ยกเลิกตาม `PANYA-DECISION 20260903_1934` · `COO 20260904_1648`) · เปิดโดย LANE-B รอบ `uq2lxw2` · แก้ขั้นตอนตาม `PANYA-ORDER 20260830_1450` ที่รอบ `xt0g9c`]

> 🔴 **บรรทัดบังคับของใบตีมอนทุกใบ (`COO-DECISION 20260902_1848` ข้อ 2 · เติมโดย LANE-B รอบ `di7ers`):**
> **ข้ามฉากแล้ววาปกลับ = เลือดมอนกลับเต็ม เป็นของที่รู้อยู่แล้ว ประกาศไม่แก้ ไม่ใช่ FAIL ของการตี**
> จะวัดว่าเลือดลดจริง ต้องตีและอ่านผล **ในฉากเดียวกัน ไม่ข้ามฉากคั่น** · ถ้าข้ามฉากแล้วกลับมาเห็นเลือดเต็ม
> ให้จดว่า `known: wound reset on scene re-open` แล้วเทสต่อ **ห้ามปิดใบเป็น FAIL ด้วยเหตุนี้**

> 🔴 **เงื่อนไขเปิดใบ (COO-DECISION `20260902_0542` ข้อ 2 · เพิ่มโดย chief R300):** ห้ามเรียกผู้เทสมาขับใบนี้จนกว่า
> **ของจะค้างอยู่บนพื้นนานพอที่ตาคนจะเห็นและเล็งคลิกได้** เหตุผลอยู่ในใบนี้เองอยู่แล้ว: ถ้า element อยู่บนจอไม่ถึงหนึ่งวินาที
> รอบนั้น**แยกไม่ออก**ระหว่าง "ไคลเอนต์ไม่ส่งเฟรมอะไรเลย" กับ "คลิกหลังของหมดอายุไปแล้ว" ⇒ ได้ผลลบที่ตีความไม่ได้ เสียรอบ attended ทั้งรอบ
> สถานะของเงื่อนไขนี้ ณ R300 (2026-09-02T08:0x+07:00) — เขียนตามที่วัดได้จริง ไม่ใช่ตามแผน:
> · ฝั่ง **ledger เซิร์ฟเวอร์** รอดแล้ว 120 วิ (`sustain_a_kill` whole-live-ledger บน main) — นั่นคือย่อหน้า 🟢 ด้านบน
> · ฝั่ง **ป้าย/ภาพบนจอ** ยัง **ไม่มีใครวัด** และทาง "ครอบ `make_runtime_vitals` ด้วย `preserve_ground_in_runtime_res_vitals`"
>   (`COO-DECISION 20260902_0347` ข้อ 2) **ถูกถอนแล้ว** ด้วย `COO-DECISION 20260902_0646` — วัดได้ว่า wrap ฆ่าเธรด `game_listener` 3 ทาง
>   ทางที่เดินแทนคือ **opt-in ทีละจุด** เริ่มที่ `action_ack` ซึ่ง **ยังไม่ขึ้น main** (chief, กำหนด R301)
> ⇒ ประตูของใบนี้คือ **`GT-188` checkpoint 2** ("วัดสภาพวันนี้") ผ่านก่อน แล้วจึงเรียกใบนี้ · ห้ามอ้างว่าเงื่อนไขเปิดผ่านเพราะ "PRESERVE อยู่บน main" — มันไม่อยู่

> 🟢 **PANYA-ORDER 20260830_1450 ขั้นที่ 1-2 ผ่านแล้ว (แก้ที่รอบ `xt0g9c`):** ตัวแปร "เล็ง" ปิดแล้วในชั้นเซิร์ฟเวอร์ --
> `mob_drop_presence.sustain_a_kill` (ชิปเข้า production ที่รอบ `m0vp7m`, ต่อสาย `runtime.py:4716-4722` แล้ว,
> `production_allowed=True` ไม่มีแฟล็ก) ส่ง **whole-live-ledger ทุกครั้งที่มีการฆ่า** แทนที่จะส่งแค่ของ kill
> เดียว ⇒ แถวที่ยังไม่หมดอายุ (120 วิ) ถูกส่งซ้ำทุกครั้งที่มีคนตายตัวใหม่ ไม่ใช่แค่ตอนเกิด headless proof:
> `tests/test_mob_drop_presence.py` 48/48 ผ่าน (รันจริงที่รอบนี้) รวม
> `test_a_second_kill_carries_the_first_kills_rows` และ `test_the_expiry_still_bounds_the_ground` --
> แถวฝั่งเซิร์ฟเวอร์ (ที่คลิกอ้างอิง) **อยู่รอด 120 วิ และคลิกได้ตลอด ไม่ถูกเก็บทิ้งเองอีกต่อไป** (เดิม
> `cell.take()` เก็บทุกคีย์ที่เพิ่งประกาศทันที -- ปิดแล้ว)
> 🟡 **สิ่งที่ยังไม่วัด (นี่คือคำถามที่เหลือของใบนี้เอง ไม่ใช่งานที่บล็อกมัน):**
> `mob_drop_presence.REEMISSION_REDRAWS_THE_LABEL = None` -- ยังไม่มีใครดูว่าป้ายชื่อบนจอ**ถูกวาดใหม่**
> เมื่อ generation ถูกส่งซ้ำหรือไม่ (แถวฝั่งเซิร์ฟเวอร์รอดแน่ ๆ แล้ว แต่ภาพบนจอเป็นคำถามฝั่งไคลเอนต์ที่วัด
> จากซอร์สไม่ได้) -- **นี่คือสิ่งที่ P0/P1-P4 ข้างล่างมีไว้ตอบ**

> NUMBERING: grep ก่อนจอง (2026-08-29T13:0x+07:00) `GT-146`/`RE-146` = 0 hit ทั้งสองคิว + `archive/` + `notes_to_chief/` · เลขสูงสุดที่ใช้ไป = 145 (`RE-` ใบจริงสูงสุด = `RE-132`) · ตัวนับเดียวสองไฟล์
> 🔴 **`GT-060` มีอยู่แล้วและห้ามลบ**: ถาม claim เดียวกัน สถานะ `BLOCKED-CONDITIONAL` บูตไม่ได้เพราะไม่มีท่า spawn drop-object และขอ "โมเดลที่คลิกได้" ซึ่ง `GT-045` ปิดไปแล้วว่า**ไม่มีโมเดล** ⇒ ใบนี้เติมท่ายิงและเลิกขอโมเดล · **จดหมาย chief `20260829_1221` ที่ว่า "ไม่มีใครเปิดใบนั้น" คลาดเคลื่อน** · ได้ผล P1/P2/P3 เมื่อไร ให้ปิด `GT-060` แบบ superseded-by `GT-146` โดยระบุชื่อ ห้ามลบก่อนมีผล
> ที่มาสามบรรทัด (รายละเอียดอยู่ในจดหมาย `20260829_13xx_LANE-B-*`): `RE-125` ปิดแบบ bounded-negative — opcode ยัง UNOBSERVED, `0x4543` derive จาก name-hash, id จริงอยู่ใน virtual-zero tail ของ `.data` ⇒ เปิดอิมเมจไม่ช่วย · `GT-046` static: request ก๊อป `+0x14` จาก **live runtime drop-object** ⇒ ไม่มีของ pre-placed ให้คลิก ต้องส่ง element เอง · มอนดรอปใช้ไม่ได้วันนี้ (`Bg0002` ตีไม่ติด · หุ่น `916` `n_DROPS_*`=0) ⇒ เหลือเลน ground-loot อย่างเดียว

### objective (ข้ออ้างเดียว)
คลิกซ้ายลงบนจุดของ element ของตกที่บูตนี้ส่งจริง **ไคลเอนต์ยิงเฟรมขาเข้าออกมาไหม และถ้ายิง nested vital id คือค่าอะไร**

### db · server args (เป๊ะ)
สำเนา `state\run_gt146.sqlite3` (+ backup `pirateforce_before_GT-146_<stamp>.sqlite3`) · **ห้ามเปิด canonical** · sha256 เทียบ `CANON_SHA.txt` ก่อน-หลัง
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt146.sqlite3 --ground-loot-hypothesis-scenario scenarios\ground_loot_hypothesis_bit08_render.json --pickup-listener-hypothesis-scenario scenarios\pickup_listener_hypothesis_decode_probe.json
```
คู่นี้บูตร่วมกันได้ (Panya 20260824 1831 §① / 2120 §②) · **สำรอง**: ถ้า `git grep` ไม่เจอเลน listener บน commit ที่จะบูต ให้ตัดสองอาร์กิวเมนต์ท้ายออกแล้วจดว่าบูตเลนเดียว — หลักฐานหลักคือ raw capture ไม่ใช่บรรทัด listener · ห้ามพ่วง `--*-scenario` อื่น · ห้ามแก้โค้ด/payload

### ขั้นตอน
0. มาตรฐานบ้าน (LOCK · boot stamp · sha canonical · copy DB) · resolve commit เขียว แล้วยืนยันบน `<SHA>` ที่บูตจริง: `git show origin/ci-status:ci/<SHA>.json` = success · `git grep -n "ground-loot-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py` · `git cat-file -e <SHA>:scenarios/ground_loot_hypothesis_bit08_render.json` · ซ้ำกับเลน listener · **ห้ามใช้ `--help` เป็นหลักฐาน**
0.5. **🔴 P0 ด่านต้นรอบ (PANYA-ORDER 20260830_1450 ข้อ ④ ขั้นที่ 3):** ยิง element ตัวแรกแล้วจับเวลาด้วยวิดีโอ (ไม่ใช่มือกดนาฬิกา) ว่าฝุ่น/ป้ายยังอยู่ให้เห็นนานกี่วินาที **ถ้ายังหายภายใน ~1 วินาทีเหมือนที่ `GT-045`/P3 เดิมวัดไว้ ให้ยกเลิกรอบทันที** บันทึกเป็น NO-RESULT (P0-FAIL, ไม่ใช่ FAIL ของใบ) แล้วส่งกลับให้สาย B วัด `REEMISSION_REDRAWS_THE_LABEL` แบบ headless เพิ่มก่อนนัดบูตรอบใหม่ — ห้ามเดินต่อขั้น 1-8 ทั้งที่ P0 ไม่ผ่าน (กันไม่ให้เผารอบของเจ้าของซ้ำ)
   🔴 **ยืนยันแล้วบน main รอบ `GT143-GT132-GT149-RESULT` (2026-08-30T15:4x+07:00, กะ1-A):** `label_life` วัดจริง
   = 0.2 วิ ไม่ใช่ ~1 วิ ⇒ **ด่านนี้จะ ABORT ทุกรอบที่บูตต่อจากนี้จนกว่า `label_life` จะยาวขึ้นจริง** (ไม่ใช่
   ความล้มเหลวของด่าน — ด่านทำงานถูกแล้ว) ก่อนนัดบูตรอบใหม่ ให้ตรวจ ASK-COO
   `notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md` ว่ามีคำเคาะหรือยัง
   — ยังไม่มี ⇒ ใบนี้ยังบูตไม่ผ่าน P0 ต่อไป อย่าเผารอบซ้ำ
   🔴 **LANE-B รอบใหม่ (scheduled) 2026-08-30T17:4x+07:00 -- อัปเดต:** ทางเลือก "สลับลำดับ `runtime.py`"
   (ทาง 2 ของใบ ASK-COO ข้างบน, CORE-REQUEST ของรอบ `qb1ytr`) **ถอนแล้ว, ไม่ใช่ทางที่เดินต่อได้** — อ่าน
   `runtime.py:4600-4824` ซ้ำพบว่า `loot_actions()` อยู่ในตำแหน่งเร็วที่สุดที่ invariant ของ
   `CORE-REQUEST-007` อนุญาตอยู่แล้ววันนี้ ไม่มีที่ให้สลับต่อโดยไม่ผิดกฎ (ดู
   `notes_to_chief/20260830_1743_LANE-B-DECISION-*.md`) ⇒ ~~ทางที่เหลือที่จะปลดด่านนี้คือ (1) COO เคาะ
   ทาง 1/3/4 ของใบ ASK-COO เดิม หรือ (2) `RE-163` (เปิดใหม่รอบนี้ ใน `CLIENT_RE_QUEUE.md`) หาสาเหตุจริง
   ของ `late_ms` แล้วชี้ทางแก้ที่ไม่ใช่ตำแหน่งคิว~~
   🔴 **ทั้งสองทางปิดแล้ว ไม่มีทางที่สาม (LANE-B รอบ scheduled 2026-08-30T19:4x+07:00):**
   (1) `notes_to_chief/20260830_1742_COO-DECISION-label-life-drop-announcement-rule-stands.md` —
   ยืนกฎเดิม (ห้ามส่งซ้ำ) ทาง 4 (NO-RESULT ที่รู้สาเหตุ) คือทางเดินต่อ ไม่มีโค้ดให้แก้;
   (2) `notes_to_chief/20260830_1805_RE-163-RESULT-*.md` — `late_ms` เป็น sender-side diagnostic
   overhead ใน `current/pf_login_game_server_v141.py` (frozen) ไม่ใช่ตำแหน่งคิวหรือ network latency,
   `BUILD_IMPACT_NONE`, ไม่มีทางแก้จาก `src/` ⇒ **P0 นี้ยังคง ABORT ทุกรอบต่อไป จนกว่าจะมีบูต attended
   ที่วัด `REEMISSION_REDRAWS_THE_LABEL` ตรง ๆ ตามเงื่อนไขที่ COO-DECISION ข้อ 23-25 วางไว้ (ยิงซ้ำครั้งเดียว
   แล้ววัดว่าป้ายกลับมาไหม ก่อนเสนอ COO ใหม่) — ไม่ใช่งานที่ค้างอยู่กับ LANE-B วันนี้**
1. server ก่อน client เสมอ · เข้าเกม (ปุ่มกลางจาก 5 ปุ่มแถวล่าง · ซ้ายสุด = ลบตัวละคร ห้ามกด)
2. **อัดวิดีโอตั้งแต่ก่อนเข้าแมพเสร็จ** — เฟรมของตกออก **ครั้งเดียวต่อเซสชัน** ที่ TargetPos แรกหลัง runtime ack · ออกตอนไม่ได้อัด = NO-RESULT · **ห้ามพิมพ์ตัวอักษรตลอดรอบ**
3. ในแมพ **ห้ามแตะ `W/A/S/D` และ `Q`/`E`** (ยิง `TargetPosVital` ทิ้ง) · จัดกล้องด้วย **คลิกขวาค้างลาก** เท่านั้น · หันไปทาง +X · **S0** ให้เห็น X/Y บน HUD
4. **ยิง:** กด `W` สั้นที่สุด (~120 ms) ครั้งเดียว · จดเวลา (+07:00) และ `t` วิดีโอ · จด `X0/Y0` · ตาอยู่ที่จอ (ฝุ่น ~0.45 s · ป้าย 0.2-0.4 s) — **นี่คือ P0 ด้านบน วัดพร้อมกันครั้งเดียว**
5. **คลิก 1 (ตอนยังเห็น):** เลื่อน cursor ไปที่ฝุ่น/ป้าย คลิกซ้ายหนึ่งครั้ง · จดเวลา · หายก่อนคลิกทันไม่ใช่ความผิดพลาด
6. เดินไปทาง X เพิ่มจนราว `X0+30` (Y คงเดิม) · hover แล้ว **จดว่า cursor เปลี่ยนรูปไหม** · **S1**
7. **ข้อสังเกตเสริม (ไม่ใช่หลักฐานหลัก, PANYA-ORDER ④ ขั้นที่ 3):** ถ้า P0 ผ่านและมีเวลาเหลือ อาจคลิกซ้ำที่จุดเดิมอีก 1 ครั้งหลัง element หายจากจอ เพื่อดูว่า element ที่ยังอยู่ในลิสต์ฝั่งเซิร์ฟเวอร์ (120 วิ ตาม `mob_drop_presence`) ยังคลิกโดนไหมทั้งที่มองไม่เห็น — บันทึกแยกจาก P1-P4 ห้ามใช้แทน P1-P4 · **S2** หลังคลิกสุดท้าย 10 วิ
8. NO-CRASH ด้วยคลิกขวาค้างลาก (ห้าม `Q`/`E`) · **S3** · ออกเกมด้วย X มุมขวาบน
9. ปิด server (**restart ก่อนบูตถัดไปเสมอ**) · เก็บ `capture_gt146_<stamp>\capture_v141\GAME_LIVE.txt` ทั้งไฟล์ + console `.out`/`.err` + sha256 ทุกไฟล์ · `PRAGMA integrity_check` · **teardown เสมอ** · sha canonical ซ้ำ · ห้าม commit เอง
10. ค้นในผล (คัดดิบ ห้ามตีความ): `findstr /N /C:"RECV" GAME_LIVE.txt` · `/C:"0x4543"` · `/C:"NEAR_ONCE"` · `/C:"FAR_ONCE"` · `findstr /N /C:"PICKUP" server_console_live.*.txt`

### pass criteria (สองชั้น 🔴 ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น)
**wire** — (ก) มี `NEAR_ONCE` + `FAR_ONCE` (54 B) = ยืนยันว่ามี element ถูกส่ง (precondition ไม่ใช่ claim) ไม่มี = P4 · (ข) สำมะโน `RECV` ทั้งไฟล์ แล้วเทียบหน้าต่าง ±2 วิ รอบคลิกแต่ละครั้งกับ baseline ก่อนคลิก ⇒ (1) มี id `0x4543` · (2) มี id อื่นที่ไม่มีใน baseline (คัด id + hexdump เต็ม) · (3) ไม่มีเฟรมนอก baseline · (ค) ถ้าบูตเลน listener: หนึ่งบรรทัดต่อเฟรม พร้อม `object_ref_u32`/`opaque_u8`/raw hex จำนวนตรงกับจำนวนคลิก — **ไม่มีบรรทัด listener ตัดสินอะไรไม่ได้** (id ที่ไม่ match ไหลลง frozen dispatch เงียบ) ⇒ **capture คือกรรมการ** · (ง) DB สำเนา `integrity_check`=ok · `sessions` +1 ต่อการเข้าเกม · sha canonical ตรงก่อน-หลัง
ชั้นนี้ตอบไม่ได้: มีอะไรบนจอไหม คลิกโดนอะไรไหม
**client-observable** — วิดีโอต่อเนื่อง + `S0..S3` full-res พร้อม sha256 · ตอบสามช่องเป็นภาษาคน: ฝุ่นขึ้นไหมกี่วิ · ป้ายขึ้นไหมอ่านว่าอะไรกี่วิ · cursor เปลี่ยนรูปตอน hover ไหม · หลังแต่ละคลิก: จอเปลี่ยนไหม มีข้อความระบบไหม (คัดเป๊ะ + สี) · **จดสีป้ายชื่อทุกป้ายทุกภาพ** อ่านจาก full-res เท่านั้น ไม่มีป้ายเขียน `none` · **จดสีอย่างเดียว ห้ามเดาสาเหตุ** (`RE-067`) · NO-CRASH/CRASH
ชั้นนี้ตอบไม่ได้: เฟรมออกจากไคลเอนต์จริงไหม id อะไร

### คำทำนาย (ผิด = ผล ไม่ใช่ความล้มเหลว)
**P1** เจอ `0x4543` ⇒ id ที่ derive ไว้ CONFIRMED · **P2** เจอ id อื่น ⇒ REFUTED **และได้ id จริงมาแทน มีค่าเท่า P1** · **P3** คลิกครบแล้วเงียบ ⇒ ผลลบที่วัดแล้ว มีค่าเท่าผลบวก (redirect = ใบ static ว่าใคร populate ลิสต์ของ `DropThingModule_Client`) 🔴 **ระยะไม่ใช่คำอธิบาย**: 30 หน่วย เทียบ `RANGE_PICKUP 600.0` · **P4** ไม่มี `NEAR_ONCE`/`FAR_ONCE` ⇒ NO-RESULT แยกอะไรไม่ได้ ห้ามอ่านเป็นผลลบเรื่อง opcode
🔴 **ผลลบไม่ปิดใบ** P3/P4 ห้ามปิดใบ ห้ามลบวิดีโอ (กติกาผลลบไม่ถูกแตะโดย `PANYA-ORDER 20260829 0930`)

### กฎจุดเกิด (`PANYA-ORDER 0930` ข้อ ④)
พิกัดของตก **อิง trigger** ⇒ element โผล่ที่ `trigger+30X` = ใกล้ ในระยะ (30 ≪ 600) และเยื้องหน้าโดยโครงสร้าง **ไม่ต้อง seed พิกัดลง DB และไม่มีตารางวางวัตถุให้ mine** (`GT-046` จ็อบ 5: `+0x14` มาจาก runtime drop-object ไม่ใช่โครงสร้างฉาก) · ค่าคาดหมายจาก `GT-045`: trigger `X -8553.947 Y -2579.689 Z 186.000` (คาดหมาย ไม่ใช่เกณฑ์)

### nonclaims
1. ไม่พิสูจน์ว่าเก็บ**สำเร็จ** หรือของเข้ากระเป๋า (`GT-142`) · เซิร์ฟเวอร์ไม่ตอบอะไรในใบนี้ ⇒ ทุกปฏิกิริยาบนจอเป็นพฤติกรรมไคลเอนต์ล้วน
2. ไม่อธิบายการเก็บของที่**มอนดรอป** (`FightingDropModule_Client`/`FightingDropNotify` ยัง NOT_OBSERVED)
3. ไม่ตอบว่า element ฝั่งเซิร์ฟเวอร์อยู่ในลิสต์นานแค่ไหน (ตอบแล้วนอกใบนี้ -- `mob_drop_presence`,
   120 วิ, headless-proven) และไม่ตอบว่าทำไมป้ายบนจอหาย (คำถามฝั่งไคลเอนต์ที่ยังไม่มีใบเปิดตรง ๆ ณ
   รอบ `xt0g9c`; `REEMISSION_REDRAWS_THE_LABEL` ที่ใบนี้เพิ่งเริ่มวัดคือคำตอบที่ใกล้ที่สุด แก้จาก `GT-132`
   ที่เดิมชี้ผิด -- `GT-132` วัดจำนวนป้ายต่อการตายหนึ่งครั้ง ไม่ใช่อายุ) · ไม่ตัดสินสาเหตุของสีป้าย (`RE-067`)
4. **ไม่นับเป็นเวอร์ชัน** — รอบที่รันใบนี้ ship ศูนย์บรรทัด แฟล็กเป็นเครื่องมือวัด · ไม่ต่อ production call site ใด ๆ (`RE-125` ห้าม `0x4543` บน production path)
5. การเทียบ `object_ref_u32` กับ element key = งานตอนบริโภคผล ผู้เทสไม่ต้อง decode

### links
`RE-125`/`RE-130` (`CLIENT_RE_QUEUE.md`) · `notes_to_chief/20260828_1112_RE-125-RESULT-NO-CAPTURED-PICKUP-OPCODE.md` · `notes_to_chief/20260829_1221_CHIEF-ASK-COO-gt124-opcode-forbidden-and-drops-pruned.md` · `GT-060`/`GT-124`/`GT-132`/`GT-142` · `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` (`GT-045` `GT-046`) · `external/PF_FIELD_VALIDATION.tsv:102-103`

### result (ผู้เทสกรอก)
P1/P2/P3/P4 · เวลาคลิกทุกครั้ง (+07:00 และ `t` วิดีโอ) · path + sha256 ของ log/console/ภาพ/วิดีโอ · สำมะโน `RECV` + hexdump ช่วงคลิก · บรรทัด listener ทั้งบรรทัด · สามช่อง ฝุ่น/ป้าย/cursor · สีป้ายทุกป้ายทุกภาพ · NO-CRASH/CRASH · sha canonical ก่อน-หลัง · `integrity_check`

**ผู้เปิดใบ: LANE-B (รอบ `uq2lxw2`) -- archived โดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00**

---
