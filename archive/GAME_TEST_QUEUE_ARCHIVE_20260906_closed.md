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

## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [🟢 **PASS รอบ UA1 — ปิดโดย chief R232**: `OBSERVER_CONFIRMED: 2026-08-29T19:1x+07:00 โดย Panya ("ยืนยัน" ทั้งรอบ UA1 · ถ่ายทอดผ่านกะ3-A ใบ `20260829_1919` §① — นาทีเป๊ะตามที่ใบบันทึก)` · หลักฐาน smoke = รอบ unattended UA1 (ใบ `20260829_1552` §③, BOOT_COMMIT `33572b24`: boot→login→เข้าแมพ→teardown สะอาด) · **HOLD (recurring) ปลดสำหรับรอบนี้ตามเงื่อนไข v6.3 หัวข้อ 18 ข้อ 7 — recurring ใบยังเปิด รอบถัดไป re-arm ตามปกติ** · ประวัติ HOLD: ดูการแก้ไขของ chief R175 ใต้หัวใบ · 🟡 บันทึกเดิม R230 (ก่อนคำยืนยันมา): AWAITING-OBSERVER เพราะใบ `1728` ยืนยันเฉพาะ GT-063 · **PASS ล่าสุด: `f8562c1` (R168) 2026-08-25 20:43 (+07:00) — PASS พร้อม erratum** · *(PASS ก่อนหน้า: `fa1e804` 2026-08-24 09:41 · R145)*] 🔁

> ### 🔴🔴 R175 correction (chief R175 · 2026-08-26, พบโดย `pf-adversary`) — HOLD ไม่ได้ถูกปลด ต้องขอโทษที่เขียนผิดไปก่อนหน้านี้ในรอบเดียวกัน
> รอบนี้เคยแก้หัวใบเป็น "HOLD ปลดแล้ว" โดยอ้าง `parse errors = 0` และ "ทดสอบสองทาง (หันอยู่กับที่/เดิน 40 หน่วย)"
> **ข้อความสองท่อนนั้นสืบไม่ถึงเอกสารใดในรีโปเลย** — ตรวจแล้วด้วย `pf-adversary`: `notes_to_chief/consumed/20260825_2335_COO-DECISION-R170-*.md:32`
> (จดหมายที่ให้เลขบรรทัด 37-44 มาแต่แรก) เขียนไว้เองชัดเจนว่า **"ยังไม่ได้รัน... จะไม่ขอปลด HOLD จนกว่าจะมีจ็อบ parse-check รันผ่านจริง"**
> และตารางท้ายจดหมายเดียวกันยังคงให้ "parse-check `1166` แล้วรายงาน" เป็นงานค้างข้อ 2 (ยังไม่มีเครื่องหมายว่าเสร็จที่ไหน)
> ที่มาของข้อความที่เขียนผิดไปคือ bullet เดี่ยวในจดหมายส่งมอบกะสองใบ (`HANDOVER-TO-SHIFT-1` และ `HANDOVER-CHIEF-PROMPT-v6-full`)
> ที่บอกว่า "รันผ่านจริงแล้ว" **โดยไม่มีเลขจ็อบ ไม่มีเวลา ไม่มี output แนบมาเลย** — ไม่ต่างจาก bullet เดี่ยว จึงไม่นับเป็นรายงานตาม G1/G8
> ⇒ **คืนสถานะ HOLD** จนกว่าจะมีจดหมายที่อ้างเลขจ็อบ/เวลา/ output จริงของการรัน `1166_gt001_teardown_verify_update_canon.ps1` แบบ parse-check
> 🔴 **บทเรียน:** ห้ามยกรายละเอียดที่ "ฟังดูสมเหตุสมผล" (เช่นวิธีทดสอบสองทาง) มาเติมให้ข้อความบาง ๆ ดูสมบูรณ์ขึ้น — ถ้าไม่มีจดหมายอ้างอิงได้ ให้เขียนว่า "ยังไม่มีรายงาน" ตรง ๆ
>
> ### 🔴🔴 HOLD เดิม (chief R170 · `pf-adversary` จับได้) — ยังมีผลอยู่ ยังไม่ปลด
> เกณฑ์ `samePos` ยังเทียบ `heading` อยู่ และ **`heading` เปลี่ยนทุกครั้งที่ตัวละครหันหน้า**
> ⇒ หยิบใบนี้ตอนนี้ = **`ABORT(20)` ซ้ำแน่นอน ก่อนถึงขั้นอัปเดต `CANON_SHA.txt`** ⇒ **การ์ด CANON ของทุกใบ abort ตาม = สะพานบูตไม่ได้ทั้งสะพานอีกรอบ**
> 🟢 **ปลด HOLD ได้เมื่อ:** สคริปต์เทียบเฉพาะ `X`/`Y`/`Z` และรายงาน `heading` โดยไม่ตัดสิน (ใบสั่งอยู่ในจดหมาย `FROM_CHIEF_R170_*`) ⇒ ผู้ที่แก้ **ตอบกลับมาว่าแก้บรรทัดไหน** แล้ว chief ปลดให้รอบถัดไป
> 🔴 **chief ปลดเองจากคลาวด์ไม่ได้** — สคริปต์อยู่บนสะพาน ไม่อยู่ในรีโป

> ### 🟢 ผลรอบ 2026-08-25 20:43 (+07:00) — **PASS พร้อม erratum** (chief R170 · จ็อบ 1164/1165/1166)
>
> **boot:** `f8562c14781809b39a124f11029d1a6faff60f63` (คอมมิต R168 · merge เข้า `main` ทาง PR #34) ⇒ **ครอบทุกอย่างที่ merge วันนั้น**
> ```
> selected        10 -> 11      ตรงที่ใบคาด
> lease           11 -> 12      ตรงที่ใบคาด
> open sessions   0             integrity ok      FK 0      กระเป๋าเหมือนเดิมทุกแถว
> POS  X -8553.947265625   Y -2579.68896484375   Z 186.0    <- เหมือนเดิมทุกหลัก
>      heading  4.53208589553833 -> 3.1123385429382324      <- เปลี่ยน
> ```
>
> 🔴 **erratum — ข้อบกพร่องของ *เกณฑ์* ไม่ใช่ของเซิร์ฟเวอร์:** `1166_gt001_teardown_verify_update_canon.ps1` เทียบแถว `POS` **ทั้งแถวรวม heading** ⇒ `samePos=False` ⇒ `ABORT(20) DB delta criteria failed`
> **ทุกเกณฑ์อื่นผ่านหมด และเดลต้าทั้งก้อนคือสิ่งที่ใบคาดไว้เอง** ⇒ **chief ตัดสิน: ใบนี้ = PASS**
> 🟢 **คำตัดสินเกณฑ์ (chief R170):** เกณฑ์ `samePos` ต้องเทียบ **`X`/`Y`/`Z` เท่านั้น** · **`heading` ให้รายงานแต่ไม่ตัดสิน**
> 🔴 **สคริปต์อยู่บนสะพาน — chief แก้เองไม่ได้จากคลาวด์** ⇒ ใบสั่งแก้อยู่ในจดหมาย `FROM_CHIEF_R170_*` (แก้แล้วให้ตอบกลับมาว่าแก้บรรทัดไหน)
>
> 🆕 **ของแถมที่ไม่มีใครเคยจด: เซิร์ฟเวอร์เขียน `heading` ลง canonical จริง**
> ตัวละคร **ไม่ได้เคลื่อนที่เลย** (X/Y/Z ตรงกันทุกหลัก) แต่ **ทิศที่หันหน้าถูกบันทึก** ⇒ ต่อยอดจาก `GT-041`
> 🔴 **nonclaim:** ยังไม่รู้ว่า heading ถูกเขียน **ตอนไหน** (ระหว่างเล่น / ตอนออก) และ **ไม่รู้ว่าอ่านกลับมาใช้ตอน relog หรือไม่** — **สังเกตครั้งเดียว ยังไม่ใช่คุณสมบัติ**
>
> 🔴 **ผลลูกโซ่ของการ abort — และคำเคาะของเจ้าของ:** จ็อบ abort **ก่อน** ขั้นอัปเดต `CANON_SHA.txt` ⇒ canonical เปลี่ยนแล้วแต่ไฟล์ยังเป็นค่าเก่า ⇒ **การ์ด CANON ของทุกใบ abort ทั้งหมด**
> 🟢 **เจ้าของเคาะ: รับค่าใหม่เป็นฐานใหม่** (คำเคาะข้อ 1 · จดหมาย `20260825_2110`) ⇒ ผู้ช่วยอัปเดตแล้วและ chief ยืนยันค่าในรีโป:
> ```
> CANON_SHA.txt  670CE534...FEC21  ->  4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454
> backup ก่อนรอบ: backup\pirateforce_before_GT-001_20260825_204328.sqlite3 = 670CE534...FEC21  (ตรวจ sha แล้ว)
> ```
> 🔴 **กฎใหม่ที่ chief รับจากข้อเสนอของผู้ช่วย:** *จ็อบที่ **เขียน** canonical ต้องอัปเดต `CANON_SHA.txt` **ก่อน** ตรวจเกณฑ์ผล หรือไม่ก็ต้องมีขั้นกู้คืนเมื่อ abort*
> เหตุผล: ตอนนี้ **การ abort ของเกณฑ์ตัวเดียวทำให้สะพานทั้งสะพานบูตไม่ได้** — abort ที่แพงเกินกว่าเหตุ

> 🔁 **อัปเดต chief R167 · 2026-08-25 ~19:xx (+07:00) — ใบนี้ *ถึงกำหนดจริง* ไม่ใช่ของแถม**
> ตั้งแต่ PASS ล่าสุด (`fa1e804`) `main` ขยับไปแล้วทั้ง PR #24–#32 **และ R167 กำลัง merge เลนใหม่ที่แตะ `src/` อีกก้อน**
> (`ground_loot_nameprop_hypothesis.py` + wiring ใน `app.py`/`runtime.py` + เพดานเวอร์ชัน ledger ทั้งไฟล์)
> ⇒ บูตที่ commit **หลัง merge ของ R167** · `CANON_SHA` จะขยับตามที่ใบคาดไว้เพราะใบนี้รันบน canonical DB จริง (ต่างจากรอบ GT-033 ที่รันบนสำเนา)

> ✅ **PASS R145 (ผลหน้าสะพาน 2026-08-24 09:41 +07:00 · Codex LOCAL):** full loop บน resolver-green `fa1e804` (tree ตรง main HEAD `94f0ce3`) — login → Port Royal → ออกด้วย X · selected sessions `9→10` · max lease `10→11` · open sessions หลังหยุด 0 · `integrity_check=ok` FK 0 · frame proof 3/3 · **`CANON_SHA.txt` อัปเดตแล้วโดยสะพาน** `EE785A79…` → `670CE534…` (การเข้าเกมเพิ่ม selected session/lease ตามที่ใบคาด)

> ✅ **RESULT 2026-08-23 01:10–01:14 (+07:00) — PASS บน main HEAD `cf81730` (worktree clean)** · full loop: login → Channel 1 → PVP → Arena01 → เข้าแมพ (HP 100/100 · Port Royal · chat online) → ออกด้วย X+ยืนยัน → Ctrl+C สะอาด
> canonical DB SHA เปลี่ยน**แบบคาดหมาย** (session +1): `6BFCEDD5…FE498FC7` → `23FD885AC4CBBFAC5E06C9B11506F6EA9F985DA82F4522383DFCC14A91C1816A` · `CANON_SHA.txt` อัปเดตแล้วโดยผู้เทส · backup ค่าเก่ายังอยู่
> ผลเต็ม: `notes_to_chief/20260823_0115_GT001-PASS-latest-main-smoke.md` (บริโภค R123)

> ✅ **RESULT รอบใหญ่ #3 — PASS ทุกเกณฑ์ที่ `f286945`** · รายละเอียดเต็มย้ายไป archive รอบ 97:
> `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md` ก้อน 2
> - 🔁 **re-arm รอบ 78:** commit รอบ 78 แตะ `src/` (app.py + runtime.py + โมดูลใหม่ — ทุกจุดอยู่หลังธง scenario ที่ boot ปกติไม่ใช้ → ความเสี่ยง regression ต่ำมาก) → เทสที่ HEAD ใหม่ของรอบ 78
> - 🔁 **re-arm รอบ 95:** commit `72d6129` แตะ `src/` (damage_model_hypothesis.py + runtime.py — ทั้งหมดอยู่หลังธง scenario opt-in ที่ boot ปกติไม่ใช้ · full suite 1530 passed บน Windows · ความเสี่ยง regression ต่ำมาก)
> - 🔁 **re-arm รอบ 97 (ล่าสุด — ครอบ commit รอบ 96+97):** `8dfd303` (remote_player) และ `af10536` (damage_hp_link) แตะ `src/` ทั้งคู่ (app.py + runtime.py + โมดูลใหม่ — ทุกจุดอยู่หลังธง scenario opt-in ที่ boot ปกติไม่ใช้ · full suite **1803 passed 1 skipped** บน Windows · ความเสี่ยง regression ต่ำมาก) → **GT-001 = PENDING ที่ `af10536`** รันในรอบใหญ่ถัดไปตามท่ามาตรฐาน PLAYBOOK
> - 🔁 **re-arm R125 (ล่าสุด):** PR #9 GROUND-LOOT-001 merge เข้า `main` แตะ `src/` (app.py + runtime.py + โมดูลใหม่ —
>   ทุกจุดอยู่หลังธง scenario opt-in ที่ mutually exclusive กับโหมดอื่น · boot ปกติไม่เปลี่ยน · เขียว(Actions run 32616696590 · subset))
>   → **GT-001 = PENDING** · **บูต commit จาก `pf_resolve_green_boot.py` ตอนจะรันจริง — จงใจไม่พิน hash ในใบนี้**
>   (ทุก merge ระหว่างหน้าต่างไม่เฝ้าเครื่องจะขยับ HEAD ได้อีก · resolver คือคำตอบเดียวที่ไม่ stale)

> 🗂 **ประวัติ re-arm รอบ 52 / 53 / 65 (superseded โดย re-arm รอบ 78 ด้านบน) ย้ายไป
> `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R85_HOUSEKEEPING.md`** (chief รอบ 85)

- objective: ยืนยันว่า commit ล่าสุดบน main ไม่ทำให้ loop พื้นฐานพัง
  (login → select → เข้าแมพ → ออก → server exit 0)
- db: `state\pirateforce.sqlite3` (ค่าเริ่มต้น)
- server args: `-SecondPasswordMode bypass`
- steps: ตาม PLAYBOOK ทั้ง 8 ข้อ
- pass criteria: เข้าแมพเห็นครบ (HP/minimap/ชื่อแมพ/chat online) + ออกสะอาด X+ยืนยัน +
  stopped ×1 + stderr 0B + listeners 0 + sessions +1 (นับแบบ selected_character_id IS NOT
  NULL) + lease +1 + backpack `[1@0,2@1,4@3]` เดิม + position เดิม (ถ้าไม่เดิน) + integrity ok
- nonclaims: ไม่พิสูจน์ inventory/combat/movement · path delete/logout/chat แยกเทสของตัวเอง
- หมายเหตุ recurring: หลัง commit ใดแตะ src/ ให้ตั้งกลับเป็น PENDING พร้อม hash ที่จะเทส
- result: (ผู้เทสกรอก)

## GT-026 EXIT-PATHS-001: ปิดเกม "ตอนอยู่ในแมพ" และปุ่ม logout ในเกม  [ท่อน A ✅ **PASS** · ท่อน B 🟡 **รันแล้ว (default scenario) — request ยืนยัน · ไม่ freeze · handler เป็น opt-in ไม่ active** · ข้อ 8 🔴 **BLOCKED** บน logout-transition ที่ทำงาน → ดู GT-033]

> 🟡 **รันแล้วรอบใหญ่ #9 (2026-08-20 09:52→10:20, HEAD `87f0769`, จ็อบ 933-937, tester next 938) — ผลเต็มบริโภคโดย chief รอบ 100:** ท่อน A PASS สองชั้น (X ในแมพ → dialog "ต้องการปิดเกมหรือไม่?" ปุ่ม `ยืนยัน`/`ยกเลิก` → กดยืนยัน หน้าต่างหาย ≤1 วิ · wire/DB: `closed_at` ถูกเติมตรงเวลากด = ออกสะอาดในสายตา server) · ท่อน B รันบน **default scenario** (handler HYP-PF-012/013 เป็น opt-in จึงไม่ active): client ส่ง `LogoutVital 0x1B40` จริงถูกต้อง มี **mode discriminator `08 03`=กลับหน้าเลือกตัวละคร / `08 01`=ออกจากเกม** · server default ไม่ตอบ · **client ไม่ transition แต่ก็ไม่ freeze** (รับคลิกปกติ ปิดด้วย X ได้) — ปมอยู่ที่ response shape ที่ทำให้ client เปลี่ยนหน้า ซึ่งรอบ 100 static RE (agent D) พบว่า **echo ทำไม่ได้แน่นอน** (inbound 0x446F30 เป็น reconcile pass ล้วน) → ดู GT-033

> **เปิดโดย chief รอบ 92 (2026-08-20)** — มาจาก **nonclaims ของ LOCALTEST-001 โดยตรง**
> ผู้เทส local พิสูจน์แล้วว่าปุ่ม X ใช้ได้ **แต่พิสูจน์จากหน้า disconnect dialog เท่านั้น**
> ⇒ ยังไม่มีใครรู้ว่า **ตอนอยู่ในแมพ** (ซึ่งมี dialog ยืนยัน) และ **ปุ่ม logout ในเกม** ทำงานยังไงจากฝั่ง local
> 🔴 นี่ไม่ใช่รายการ "ของแถม" — **ทุกรอบใหญ่จบด้วยการออกจากเกม** ถ้าเส้นทางออกไม่ถูกพิสูจน์
> teardown ของทุกเทสจะยืนอยู่บนสมมติฐาน และ **การออกไม่สะอาดคือต้นเหตุของวงจรอุดตันที่กินเวลาเราไปทั้งคืน 2 รอบแล้ว**

- **ไม่ต้อง commit อะไรก่อน** — เทสพฤติกรรม client + เส้นทางออก ไม่ได้เทสฟีเจอร์ใหม่
- **scenario:** ค่าเริ่มต้น (ไม่ต้องเปิด flag ใด ๆ) · **db:** สำเนา canonical ตามปกติ · **server args:** `-SecondPasswordMode bypass`
- **เปิด client ด้วย `Invoke-CimMethod Win32_Process Create`** (ข้อ 8b ในหัวไฟล์ — อย่าใช้ `Start-Process` กับ `.bin`)

## ⭐ GT-060 PICKUP-CLICK-CAPTURE-001 [attended, in-game]: คลิกซ้ายบน drop-object ที่วาดจริงบนจอ แล้วจับเฟรม `PickupTerrainThing` **ตัวจริงตัวแรก** บน wire — id `0x4543` ที่ derive ไว้ ถูกหรือผิด  [❌ **CANCELLED - covered by GT-146** · ปิดโดย chief (LANE-E) รอบ `kj0s6r`/R346 2026-09-05T02:0x+07:00 ตาม `COO-DECISION 20260904_2349` ข้อ 4 · `GT-146` ถามคำถามเดียวกัน (คลิกซ้ายบนของตกที่เซิร์ฟเวอร์ส่งเอง แล้วไคลเอนต์ยิงเฟรมอะไร) ด้วยขั้นตอนที่ใหม่กว่า ⇒ ใบนี้ไม่ต้องใช้เวลาผู้เทสอีกใบ · 🔴 หมายเหตุ: `GT-146` เองอยู่ในสถานะ `BLOCKED - until P-2 closes (NOW)` ⇒ คำถาม opcode ยังไม่ถูกตอบด้วยตา ยังเปิดอยู่ แต่ถืออยู่ที่ `GT-146` ใบเดียว ไม่ใช่สองใบ · เนื้อใบและเงื่อนไขเดิมเก็บไว้ข้างล่างเพื่อการอ้างอิง (ห้ามลบ) — เดิม: **BLOCKED-CONDITIONAL — ห้ามบูตจนกว่าเงื่อนไข (ก)(ข)(ค) ข้างล่างครบทั้งสามข้อ** · เลน server = HYP-PF-036 (R151 · ✅ (ก) ปิดแล้ว R152: PR #22 merge เข้า `main` `2c0e3ba`) · เงื่อนไข (ข) เหลือแค่ผลตา GT-045 (นัด 2026-08-26) — คำเคาะ composition มาแล้ว (จดหมาย 1831 §①) และโค้ด composed-boot merge เข้า `main` แล้ว (R154: PR #23 → `cad3e28` เขียว Actions run 32726495224) · ✅ **(ค) ปลดแล้ว — Panya ปลดพักเลน attended ทั้งเลน (2026-08-24 ~21:1x +07:00 · จดหมาย 2120 §① · บันทึกโดย R155)** — คำสั่งพัก 16:56 ของ 23 ส.ค. สิ้นสุด · กฎรอบ unattended ยังเหมือนเดิมทุกตัวอักษร · 🆕 R155: คำเคาะ 2120 §② ขยาย allow-list เป็น**สามตัว** `ground-loot + pickup-listener + item-operate-res` — ใบนี้ได้ประโยชน์ถ้ารวมบูตกับ GT-063 (โค้ดสามตัว = PR #25 รอ gate — ดูหัวใบ GT-063)]

**ที่มา:** สามใบประกอบกัน — **GT-046** (STATIC PASS: `PickupTerrainThing` เป็น **outbound** สร้างที่ call `0x006B0639` เติมค่าจาก live runtime drop-object · ตัวจุดชนวน = `WM_LBUTTONDOWN` ที่ `0x006B0570` **เฉพาะเส้นทาง in-range**) + **GT-045** (WIRE PASS / CLIENT NO-RESULT — การวาด drop-object จาก wire ยังพิสูจน์ไม่ได้ รอเทสตา) + เลน server ใหม่ **HYP-PF-036** (R151): inbound listener หลัง `--pickup-listener-hypothesis-scenario` — เมื่อเฟรมขาเข้ามี nested vital id `0x4543` มันจะ decode-count-record (`object_ref_u32` · `opaque_u8` · raw body hex) ลง session state `pickup_listener_accepted_count`/`records`/`refusals` และปล่อย **log บรรทัดเดียว ASCII** · **ไม่ตอบกลับ ไม่เขียน DB** · ไบต์ผิดรูป = refusal มีชื่อถูกจดไว้ · codec อิง `external\PF_SERIALIZER_FIELDS.tsv` แถว 859-862

**หมวด:** attended, in-game — ต้องมีคนหน้าจอ **และต้องมีมือคลิก** · จับ `LOCK_GAME` ตามปกติ

**ค้น external แล้ว: เจอ** — `PF_SERIALIZER_FIELDS.tsv` แถว 859-862 (codec ที่ listener ใช้) · `PF_FIELD_VALIDATION` แถว 102-103 (**corpus มีเฟรม `PickupTerrainThing` = 0 เฟรม** — ไม่มีของจริงให้เทียบ) · `FACTPACK_L2_CLASSCENSUS001` แถว 1003 (id `0x4543` เป็นค่า **derive จาก name-hash** ไม่ใช่ค่าที่เคยเห็นบนสาย)
**ค้น gamedata แล้ว: เจอแต่ไม่ใช้เพิ่ม** — `TEXTDATA_TH__MESSAGE.tsv` ผูก `0x1F/0x03/0x22` แล้ว (addendum GT-046 R132) · ใบนี้ไม่แตะข้อความตอบกลับใด (server เราไม่ตอบเลยโดยดีไซน์)

## GT-084-R2 HOSTILE-PAIR-VISIBLE-001: รอบสองของ GT-084 -- คู่ faction (1,6) ที่ผู้เล่นได้ครึ่งของตัวเองแล้ว ทำให้ Tornado Eagle ขึ้นศัตรูจริงบนจอไหม (~~ชื่อแดง + แผงเป้าแดง~~ [UPDATE 2026-08-27T17:34+07:00 LANE-B ต่อยอด PANYA-REFERENCE 16:35+07:00: เกณฑ์สีที่ถูกต้องคือ **ส้ม (ยังไม่ aggro) → แดงเข้ม (aggro) → เทา (ตาย)**, ไม่ใช่ "แดง" เฉยๆ] + แผงเป้า) บนบูตไร้แฟล็ก -- ก่อนจะไปถึงเรื่องตี  [🟡 **RESULT -- claim หลัก (hostile ที่ตาเห็น) PASS ด้วยหลักฐานพฤติกรรม (ขอบแดง+ลูกศรแดงคู่, ดับเบิลคลิกตีติดจริง) แต่ไม่ใช่สีตามใบเป๊ะ (ชื่อชมพู/magenta ตลอด ไม่ใช่ส้ม→แดงเข้ม→เทาตามลำดับสถานะจริง, ไม่มีแผงเป้า) -- ผลต่อขั้นตี-ตาย: ดู GT-084 -- รายละเอียด notes_to_chief/20260827_1620_GT084R2-RESULT-*.md, RE-107/RE-108 ปิดแล้ว (bounded negative), RE-109 เปิดใหม่ถามครบ 6 สี, สถานะสุดท้าย (PASS/MIXED) รอ chief ตั้ง**]

🆕 **RIDER-084-B (เจ้าของใบ LANE-B · รอบ `szdkgs` · 2026-08-29 ~01:0x +07:00) — ตัวตนของเป้าหมายในใบนี้ถูกแก้แล้วครึ่งหนึ่ง ไม่แก้ objective/เกณฑ์ผ่านของใบแม่แม้แต่ตัวอักษรเดียว**
รอบนี้ `field_mob_tables.py` ถูก regenerate ผ่าน crosswalk ของ `RE-128` (`SCENE_NAME.n_CLINE_TYPE` → `CLINE.n_LEADER_BK1`) ผลที่ผู้เทสจะเห็นต่างจากรอบก่อน:
- **สี่ placement 103/105/107/109** เมื่อวานส่งเป็น `Mutant Green Eagle` (เลขชุด 97) วันนี้ส่งเป็น **`n_ID 916 Training Iron Man`** avatar `M016_000_000_N` (เมื่อวานคือ `M011_000_002_SP3`) — **ของจริงตามตาราง ไม่ใช่การประกอบเอง** และเป็นตัวที่ `COO-DECISION widen-death-scope-916-training-iron-man 2026-08-27T09:55+07:00` อนุญาตให้ฆ่าไว้แล้ว
- **อีกเก้า placement (รวม P30 `0x201F` เป้าหมายของใบนี้)** ยังส่งไบต์เดิมทุกอย่างในรอบนี้ ⇒ **ใบนี้ยังรันได้เหมือนเดิม ไม่ต้องแก้ขั้นตอน** 🔴 แต่ให้รู้ไว้ว่า **ชื่อ "Tornado Eagle" ของ P30 ถูกพิสูจน์แล้วว่าไม่ใช่ตัวตนจริงของ placement นั้น** (crosswalk บอกว่า Mob-Set 31 = `n_ID 248 Da Vinci`) การย้ายอีกเก้าแถวไปตัวตนจริงเป็นงานรอบถัดไปของสาย B (ประมาณ 840 pin)
- 🔴 **สิ่งที่ควรจดเพิ่มถ้าได้นั่งรอบนี้ (ไม่ใช่เกณฑ์ผ่าน):** ที่พิกัดราว (11789..15649, 9317..9364, 2200) มีหุ่นสี่ตัว — **หน้าตาเปลี่ยนจากนกเป็นหุ่นเหล็กหรือไม่** และชื่อใต้ตัวอ่านว่า `Training Iron Man` หรือไม่ · ตอบ "เปลี่ยน/ไม่เปลี่ยน" พอ ไม่ต้องตีความ

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md. เลขสูงสุด ณ เวลาเขียนใบนี้: GT-099 / RE-098.
> 🔢 **ใบนี้ไม่กินเลขคิวใหม่** -- เป็น **รอบที่สองของ GT-084** เลนเดียวกัน (มอนสเตอร์เป้าหมายเดียวกัน 0x201F
> Tornado Eagle, บูตไร้แฟล็กเดียวกัน, ท่าเดียวกับ GT-030-R3 ที่อยู่ใต้เลขเดิม) ตามคำสั่งเจ้าของ (Panya)
> 2026-08-27 09:15 ผ่าน notes_to_chief/20260827_0915_PANYA-CHASE-owner-decisions-...md ข้อ ①.2 ประโยคสุดท้าย,
> และ notes_to_chief/20260827_0520_ATTENDED-URGENT-R187-...md ง§④ ข้อ 3-4. ใบ `GT-084` เดิม (รวม
> `RIDER-084-A` และทุกอัปเดตต่อท้ายถึง R188) **ยังอยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ** -- ใบนี้ยืน
> อยู่บนผลของมัน ไม่ใช่ใบแทน.

🆕 **ความคืบหน้า world-wipe (ยังไม่ใช่ "พร้อม") — LANE-B รอบ `rbuta4` 2026-08-28T18:1x+07:00:**
เพิ่ม headless proof `pirate-force-server/tests/test_world_wipe_headless_proof.py` — บูตไร้แฟล็ก
→ โดนตี 1 → ตาย 1 → เฟรม `MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` ยังมีครบทุกตัวที่
census ตอน arrival ส่งไป **วัดจาก `frame` ซึ่งเป็นบัฟเฟอร์ที่ `v141:7755 c.sendall(out_frame)` ส่งออกจริง**
(ไม่ใช่ `pc` ซึ่งไคลเอนต์ไม่เคยได้รับ) เทียบกับเฟรม arrival ของเซสชันเดียวกัน
🔴 **แก้คำผิดของอัปเดตฉบับแรก (เขียนไว้ 17:49 น. ถอนแล้ว):** ฉบับแรกเขียนว่า "grep token เชื่อได้แล้ว
ผู้เทส grep ได้โดยไม่ต้องกลัว" — **ผิด และถอนคำนั้น** `pf-adversary` สร้าง regression จริงที่ทำให้เทสทั้ง 19 ใบ
เขียว ในขณะที่เฟรมที่ออกสายมี body เดียว (เฟรมของ `MOB_DEATH_*` ยังผูกกับ `death_step` ตัวเก่าขณะที่ `pc`
ถูกอัปเดตแล้ว) เพราะเทสฉบับแรกวัด `pc` ไม่ใช่ `frame` แก้แล้วในรอบเดียวกันนี้
🔴 **ผู้เทส: ยังห้ามใช้บรรทัด `*_CENSUS_RECOMPOSE actor_count=115` เป็นหลักฐานเดี่ยว** มันพิมพ์
`world_census_actor_count` ที่อ่านจาก session state **ก่อน** ประกอบเฟรม ⇒ เป็น **INPUT ไม่ใช่ผลลัพธ์**
บรรทัดนี้ยืนยันได้แค่ว่า "เส้นทาง recompose ถูกเดิน" ไม่ได้ยืนยันว่า "เฟรมมีครบ 115" — หลักฐานจำนวนตัวจริง
เป็นชั้น headless ในเทส ไม่ใช่ชั้นคอนโซล
🔴 **นี่คือชั้น wire เท่านั้น ไม่ใช่ชั้นจอ** — `RIDER-084-A` `OW1`-`OW3` **ยังเป็นขั้นสังเกตบังคับเหมือนเดิมทุก
ตัวอักษร** ห้ามอ่านบรรทัดนี้ว่า world-wipe ปิดแล้วบนจอ ใบนี้และริเดอร์ไม่ถูกแก้แม้แต่ตัวอักษรเดียวจากอัปเดตนี้
🔴 **addendum-G ยัง "ไม่ปิด"** — `pf-adversary` ยก 14 ข้อ ระดับ critical 2 ข้อ รอบนี้แก้ที่โค้ดแล้ว
แต่การประกาศปิดเกณฑ์เป็นของ COO ไม่ใช่ของสาย B ⇒ ดู `archive/rounds_2026-08-27_to_28/B_20260828_1749_world_wipe_headless_proof.md` ก่อนตัดสิน

🆕 **RIDER-084-C (เจ้าของใบ LANE-B · รอบ `sn42vo` · 2026-08-29T03:53+07:00) — เป้าหมายของใบนี้ถูกถอนออกจาก roster แล้ว · ไม่แก้ objective/เกณฑ์ผ่านของใบแม่แม้แต่ตัวอักษรเดียว**
🔴 **อ่านก่อนบูต:** `pirate-force-server#221` (merged 2026-08-29T03:32+07:00) ถอนเก้าแถวเลขชุดออกตาม COO-DECISION 00:41 ⇒ **`0x201F` (P30 "Tornado Eagle") ไม่อยู่ใน roster อีกแล้ว** ข้อความใน `RIDER-084-B` ที่ว่า "อีกเก้า placement (รวม P30 `0x201F`) ยังส่งไบต์เดิม" ~~เป็นจริง ณ รอบ `szdkgs`~~ **หมดอายุแล้ว ณ รอบนี้** (ขีดฆ่า ไม่ลบ ตามกติกา)
วัดสดบน main รอบนี้ (`field_mobs.load_roster()`): roster = **4 แถว** ทั้งหมด `n_ID 916 Training Iron Man` avatar `M016_000_000_N` · placement **103/105/107/109** ⇒ actor identity **`0x2068` `0x206A` `0x206C` `0x206E`** · level 100 · HP 198125 · `rank=0` · `ai_combat=0` · `n_DROPS_*` = 0 ทั้งสามคอลัมน์ · scene bg0001
⇒ **ใบนี้รันตามขั้นตอนเดิมไม่ได้** เพราะไม่มีเป้าหมายเดิมให้คลิก · ตัวที่ยืนอยู่จริงคือหุ่นสี่ตัว และ COO เคาะไว้แล้วว่ามันคือ **หุ่นซ้อม ไม่ใช่มอนสเตอร์ของฉากนี้** (`rank=0`, `ai_combat=0`) 🔴 **คำถามหลักของใบนี้ (ส้ม→แดงเข้ม→เทา) อาจถามกับหุ่นซ้อมไม่ได้ตั้งแต่ต้น** — สถานะใบและเป้าหมายทดแทนเป็นของ chief/COO ตั้ง ไม่ใช่ของสาย B ตั้งเอง สาย B รายงานข้อเท็จจริงเท่านั้น

🔴 **เกณฑ์ addendum-G ข้อ "census หลังเหตุการณ์ยัง 115/115 (grep คอนโซลได้)" — สาย B รายงานว่า *เขียนแบบนี้แล้วปิดไม่ได้* ไม่ใช่ว่ายังไม่ได้ทำ**
สองเหตุผล วัดแล้วทั้งคู่:
1. **เลข 115 ไม่ใช่เลขของบูตไร้แฟล็ก** — 115 คือขนาดตาราง placement ที่แช่ไว้ · สิ่งที่บูตไร้แฟล็ก **ประกอบได้จริง** คือ **108** (`SHIPPED_CENSUS_COUNT`, `tests/test_world_wipe_headless_proof.py:156`, ที่มา RE-128/CLINE) ⇒ เกณฑ์ที่ถูกคือ **108/108**
2. **ชั้นคอนโซลตอบคำถามนี้ไม่ได้เลย** — บรรทัด `*_CENSUS_RECOMPOSE actor_count=N` พิมพ์ `world_census_actor_count` ที่อ่านจาก session state **ก่อน** ประกอบเฟรม ⇒ เป็น **INPUT ไม่ใช่ผลลัพธ์หลังเหตุการณ์** (รอบ `rbuta4` ถอนคำอ้างนี้ไปแล้วเอง) มัน grep ได้ แต่ยืนยันได้แค่ "เส้นทาง recompose ถูกเดิน"
⇒ **สิ่งที่จะปิดเกณฑ์นี้ได้จริง** คือบรรทัดคอนโซลที่นับ **จำนวน body ในเฟรมที่ประกอบเสร็จแล้ว** แล้วพิมพ์หลังประกอบ · จุดพิมพ์อยู่ใน `runtime.py` ซึ่ง **เป็นเขตของ chief** ⇒ สาย B เปิดเป็น CORE-REQUEST ใน body ของ `pirate-force-server#228` แทนการแก้เอง
~~🔴 **สาย B ไม่เขียนบรรทัด "พร้อมสำหรับ GT-084-R2" ในรอบนี้ และจงใจไม่เขียน** — ชั้น wire ปิดแล้วจริง (`test_world_wipe_headless_proof.py` 7 ใบ วัดจาก `frame` ที่ `v141:7755` ส่งออก ไม่ใช่ `pc`) แต่ชั้นที่เกณฑ์ขอ (คอนโซล) ยังไม่มีของให้ grep และเป้าหมายของใบก็เพิ่งหายไป ⇒ เขียน "พร้อม" ตอนนี้คือคำอ้างที่รอบ `rbuta4` เพิ่งถอนไปเอง~~

🆕 **RIDER-084-D (เจ้าของใบ LANE-B · รอบ `z096sw` · 2026-08-29T18:5x+07:00) — ครึ่งคอนโซลของเกณฑ์ addendum-G ปิดแล้ว วัดจริง · ไม่แก้ objective/เกณฑ์ผ่านของใบแม่แม้แต่ตัวอักษรเดียว**

รอบก่อนเขียนไว้เองว่า "สิ่งที่จะปิดเกณฑ์นี้ได้จริงคือบรรทัดคอนโซลที่นับจากเฟรมที่ประกอบเสร็จแล้ว · จุดพิมพ์อยู่ใน `runtime.py` ซึ่งเป็นเขตของ chief" — **ข้อหลังผิด**: กฎบัตรสาย B ข้อ G มอบบล็อก `bar_frames`/`death_frames` ให้สายนี้แก้ได้หนึ่งครั้งเพื่องานนี้โดยตรง ⇒ รอบนี้แก้เองแทนที่จะรอ CORE-REQUEST

**🟢 พร้อมสำหรับ GT-084-R2 — เฉพาะครึ่ง world-wipe ของเกณฑ์ addendum-G** (ไม่ใช่ทั้งใบ ดูข้อจำกัดท้ายบล็อก)

🔴 **อ่านย่อหน้านี้ก่อน — ฉบับแรกของริเดอร์นี้เขียนเกินหลักฐาน และ pf-adversary จับได้ก่อน push**
ฉบับแรกยกบรรทัด `actor_count=108 wire_actors=108` เป็นหลักฐานว่า "โลกรอด" · **นั่นเป็น tautology ไม่ใช่การวัด**:
เมื่อ compose สำเร็จ `wire_actors` เท่ากับ `actor_count` เสมอโดยพีชคณิต (recompose เรียก
`build_world_population(legacy, anchor, count)` ด้วย `count` ตัวเดียวกัน และ `census_order` อ่านตารางนิ่ง
ที่หดไม่ได้) ⇒ มิวแทนต์ที่ **ไม่อ่านสายเลย พิมพ์ input ซ้ำ** เขียวทั้งสวีต
🟢 **สิ่งที่ทำให้บรรทัดนี้มีค่าจริงคือของที่แก้หลังจากนั้น** ไม่ใช่เลข 108/108:
บรรทัดถูกย้ายออกมา **นอก `if` และนอก `try`** ⇒ สองเส้นทาง fallback (compose โยน / ไม่มี anchor ซึ่ง
คอมเมนต์ใน `runtime.py` เองบอกว่า "เกิดในการเล่นปกติ") **เคยส่งเฟรม one-entry ออกสาย = ตัว world wipe เอง
แล้วคอนโซลเงียบสนิท** — นั่นคือสภาพเดียวที่ผู้เทสต้องการบรรทัดที่สุด และเป็นสภาพเดียวที่ไม่มีบรรทัด

grep token ที่ผู้เทสต้องใช้ (ASCII ล้วน · cp874 ปลอดภัย):

```
MOB_COMBAT_BAR_CENSUS_RECOMPOSE        actor_count=<input>  wire_actors=<measured>  target=0x....
MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=<input> wire_actors=<measured>  target=0x....
MOB_DEATH_FRAMES_CENSUS_RECOMPOSE       actor_count=<input> wire_actors=<measured>  target=0x....
```

🔴 **อ่านสองฟิลด์นี้ให้ต่างกัน ไม่ใช่ฟิลด์เดียวกันเขียนสองครั้ง**
- `actor_count=` **ของเดิม ความหมายเดิม ไม่เปลี่ยน** = `world_census_actor_count` อ่านจาก session state **ก่อน** ประกอบเฟรม (INPUT) · เก็บชื่อเดิมไว้เพราะใบนี้กับ runbook สั่ง grep คำนี้อยู่แล้ว การเปลี่ยนความหมายเงียบ ๆ แย่กว่าดีเฟกต์ที่กำลังแก้
- `wire_actors=` **ของใหม่รอบนี้** = จำนวนที่ **collection header ของเฟรมที่ส่งออกจริงประกาศ** อ่านหลังประกอบ ด้วย `world_population_handoff.wire_count_of` ตัวเดียวกับที่ headless proof เรียก และ**อ่านต่อเมื่อ `frame == legacy.frame_pc(pc)` ผ่านแล้วเท่านั้น**
- ถ้าอ่านไม่ได้จะพิมพ์ `wire_actors=unmeasured reason=<ชื่อ>` **ไม่เคยพิมพ์ตัวเลขที่เดาไว้** (`frame_is_not_this_pc` / `header_unreadable` / `legacy_refused` / `pc_not_bytes` / `frame_not_bytes`)

**วัดจริงบนบูตไร้แฟล็ก รอบนี้** (สคริปต์ขับ harness เดียวกับ `test_world_wipe_headless_proof.py` · ไม่ใช่ค่าที่เทสคำนวณเอง):

```
arrival        : WORLD_CENSUS assembled=108/115 wire=108 ... (collection header ประกาศ 108)

--- บูตปกติ compose สำเร็จ (โลกรอด) ---
ตี 1 ครั้ง      : MOB_COMBAT_BAR_CENSUS_RECOMPOSE        actor_count=108 wire_actors=108 target=0x2068
ตาย 1 ตัว      : MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=108 wire_actors=108 target=0x2068
                MOB_DEATH_FRAMES_CENSUS_RECOMPOSE       actor_count=108 wire_actors=108 target=0x2068
compose refusals/skips : ไม่มีสักรายการ

--- 🔴 fallback: compose ถูกปฏิเสธ = world wipe จริง (เมื่อก่อนบรรทัดนี้ไม่มีเลย) ---
                MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=108 wire_actors=1 target=0x2068
                MOB_DEATH_FRAMES_CENSUS_RECOMPOSE       actor_count=108 wire_actors=1 target=0x2068
events         : mob_death_frames_census_compose_refused_RuntimeError
```

⇒ **นี่คือสิ่งที่ผู้เทสต้องอ่านจริง ๆ:** ไม่ใช่ "เห็น 108/108 แล้วสบายใจ" แต่คือ
**`wire_actors` ต่างจาก `actor_count` เมื่อไหร่ = โลกถูกล้างเมื่อนั้น** · `108 vs 1` คือหน้าตาของ world wipe
🔴 `state.events` **ไม่เคยถูกพิมพ์ที่ไหนเลยในทรีนี้** (append 276 จุด · print 0 จุด) ⇒ ก่อนรอบนี้
สัญญาณเดียวที่ผู้เทสมีในสภาพนั้นคือ **การไม่มีบรรทัด** ซึ่งเป็นความผิดพลาดที่ `GT-084` เคยทำมาแล้วครั้งหนึ่ง

⇒ **เกณฑ์ที่ถูกคือ 108/108 ไม่ใช่ 115/115** (ข้อ 1 ของบล็อกบนยังคงเดิมทุกตัวอักษร: 115 คือขนาดตารางที่แช่ไว้ · 108 คือสิ่งที่บูตไร้แฟล็กประกอบได้จริง)

🔴 **สี่ข้อที่บรรทัดนี้ยังไม่ปิด และห้ามอ่านว่าปิด**
1. **ตอน compose สำเร็จ สองเลขนี้ต่างกันไม่ได้** — มันเป็นเลขเดียวกันโดยพีชคณิต ⇒ `108/108`
   ยืนยันได้แค่ "เส้นทางเดินและเฟรมที่ส่งคือเฟรมของ pc นั้น" **ห้ามอ่านว่า "นับ body แล้วครบ"**
   ค่าของบรรทัดนี้อยู่ที่เคส fallback ล้วน ๆ
2. **`wire_actors` คือจำนวนที่ header ประกาศ ไม่ใช่จำนวน body ที่นับได้** — เฟรมที่ประกาศ 108 แต่ใส่มา 12 ตัวจะพิมพ์ `wire_actors=108` และเป็น world wipe (วัดแล้วโดย pf-adversary: ตัด body เหลือ 12 จาก 108 → บรรทัดยังพิมพ์ 108) · คนที่เห็นเรื่องนั้นคือชั้น headless (`test_world_wipe_headless_proof.py` นับ occurrence ต่อ identity) ซึ่ง**ยังอยู่ครบทุกใบ ไม่ถูกแทนที่**
3. **บนบูต GM ที่มี diag object สองเลขจะไม่เท่ากันโดยถูกต้อง** — วัดแล้ว: `actor_count=108 wire_actors=113` เพราะ diag object ห้าตัวถูก append เข้า collection ⇒ **`wire_actors` มากกว่า = ปกติบนบูต GM · `wire_actors` น้อยกว่า = wipe** บรรทัดไม่มีฟิลด์แยกสองกรณีนี้ให้ ต้องรู้จากบูตที่ใช้
4. **ใบ `GT-084-R2` ยังไม่มีเป้าหมายให้คลิก** — `RIDER-084-C` ข้างบนยังคงเดิม: `0x201F` ไม่อยู่ใน roster และที่ยืนอยู่คือหุ่นซ้อมสี่ตัว · การตั้งเป้าหมายทดแทน/สถานะใบเป็นของ chief/COO ⇒ "พร้อม" ข้างบนคือ **พร้อมของเกณฑ์ addendum-G เท่านั้น** ไม่ใช่ "ใบนี้รันได้แล้ว"

โค้ด: `src/pirateforce_foundation/mob_census_wire_count.py` (โมดูลใหม่ของสาย B · ไม่มีแฟล็ก · `production_allowed = True` · ไม่โยนเข้า dispatch เด็ดขาด) · `tests/test_mob_census_wire_count.py` · จุดพิมพ์ใน `runtime.py` (การแก้ครั้งเดียวที่ข้อ G สงวนไว้ให้สายนี้)

🆕 **RIDER-084-E (เจ้าของใบ LANE-B · รอบ `jop8ph` · 2026-08-29T19:5x+07:00) — ฟิลด์ใหม่บนบรรทัดที่ผู้เทส grep อยู่แล้ว · ไม่แก้ objective/เกณฑ์ผ่าน/nonclaims ของใบแม่แม้แต่ตัวอักษรเดียว**

บรรทัด `MOB_CENSUS_HOSTILITY` ได้ฟิลด์ท้ายสุดเพิ่มหนึ่งตัว: `ledger=<state>`
(ฟิลด์เดิมทุกตัวอยู่ที่เดิม ลำดับเดิม ⇒ การ grep หา `MOB_CENSUS_HOSTILITY` ยังแมตช์เหมือนเดิม)

```
MOB_CENSUS_HOSTILITY scene_id=.. scene=.. roster=.. backed=.. unbacked=.. refused=.. override=.. ledger=<state>
```

🔴 **สิ่งที่ผู้เทสต้องอ่านให้ถูก:**
- `ledger=not_reported` = **จุดเรียกไม่ได้ส่ง ledger ให้บรรทัดนี้** ไม่ใช่ "ไม่มี ledger"
  **นี่คือสิ่งที่บูตวันนี้จะพิมพ์** จนกว่า chief จะต่อสองคีย์เวิร์ด (ดูจดหมาย `20260829_1955_LANE-B-CORE-REQUEST-*`)
- `ledger=same_scene` = ledger ถูกใช้จริง ⇒ **มอนที่บาดเจ็บจะถูกส่งซ้ำด้วยเลือดที่เหลือจริง**
- `ledger=other_scene` / `unscoped_incomplete` / `same_scene_incomplete` = **ถูกปฏิเสธ**
  ⇒ census ประกอบตามปกติ ไบต์เท่ากับตอนไม่ส่ง ledger ⇒ **มอนบาดเจ็บกลับมาเลือดเต็ม**
  (นี่ไม่ใช่ error และไม่ทำให้บูตล้ม — เป็นสภาพที่มีชื่อ)
- `ledger=absent` = ผู้เรียกส่ง `None` มาเอง · `ledger=ledger_unreadable` = ของที่ส่งมาไม่ใช่ ledger

บรรทัดละเอียดสำหรับตอนอยากรู้ว่าทำไม (พิมพ์เมื่อจุดเรียกเรียก `describe_ledger_admission`):
```
MOB_LEDGER_ADMISSION scene_id=.. scene=.. ledger_scene=.. state=.. admitted=yes|no covered=N/M missing=.. vacuous=yes|no
```
`covered=N/M` คือครึ่งที่ **วัด** (`state=` คือครึ่งที่ **ตัดสิน**) · `missing=not_measured`
แปลว่าไม่มีการอ่าน ledger เลย ไม่ใช่ "ไม่ขาดอะไร"

🔴 **ริเดอร์นี้ไม่อ้างอะไรที่ชั้นจอ และไม่เปลี่ยนไบต์บนบูตวันนี้** — สองคีย์เวิร์ดที่ทำให้มันเปลี่ยน
อยู่ใน `runtime.py` (เขตของ chief) และยังไม่ต่อ · `RIDER-084-A` `OW1`-`OW3` ยังบังคับเหมือนเดิมทุกข้อ

โค้ด: `src/pirateforce_foundation/mob_ledger_admission.py` (โมดูลใหม่ของสาย B · ไม่มีแฟล็ก · `production_allowed = True` · ไม่โยนเข้า dispatch เด็ดขาด) · `tests/test_mob_ledger_admission.py`

## GT-101 GM-001 LOGIN-STATE-VISUAL-PROBE-001: ล็อกอินด้วยบัญชีในลิสต์ gm_accounts แล้ว GM_UpdateGMStateVital (0x5A19) ที่ CORE-REQUEST-006 ต่อสายเข้า login path แล้ว จอเปลี่ยนอะไรไหม  [RESULT -- ไม่ใช่ PASS/NO-RESULT/BLOCKED, ดูผลด้านล่าง]

> เลขใบ: ตัวนับเดียวร่วมกับ CLIENT_RE_QUEUE.md, prefix สองแบบ ห้ามแยกตัวนับ.
> เลขสูงสุดที่ใช้ไปแล้ว ณ เวลาเขียนใบนี้: GT-099 (GAME_TEST_QUEUE.md) และ RE-100 (CLIENT_RE_QUEUE.md,
> บันทึกไว้เองว่า "เลขว่างถัดไป = 101"). grep ยืนยันก่อนจอง: GT-101 = 0 hit, RE-101 = 0 hit ทั้งสองไฟล์
> (ยืนยัน 2026-08-27). ใบเก่าทุกใบอยู่ที่เดิม ไม่ถูกแตะ ไม่ถูกย้าย.

## GT-114 DIAG-MULTI-OBJECT-001 [attended, in-game]: five diagnostic objects at the city-center test point (X=11865, Y=6147), each one field away from control D0 -- does each single-field difference produce the on-screen effect that field is predicted to control, jointly closing the attended half of RE-107/RE-108/RE-109's own proposed follow-ups  [CANCELLED - covered by R309 (D0 · RE-108) / refuted by production DYING_TIMER_SECONDS=20 (D1a · ภาพ 185937) / covered by GT-129 (D1b) / D2 control-only / covered by GT-084-R2 + P-2/RE-067 (D3) — Panya agreed 2026-09-04 21:4x · ปิดโดย chief รอบ `epkucn`/R344 2026-09-04 22:56 +07:00 ตาม `COO-DECISION 20260904_2158` (ถอน `2142` ข้อ 2 = ไม่พ่วงบูตกับ `ATTACK-POSE-ONE-FIELD-AB-001`) · กฎ `PANYA-DECISION 20260903_1934` · เหตุผลรายข้ออยู่ใน `notes_to_chief/20260904_2133_KA1A-TO-COO-attack-pose-*` §1 · เดิม: PENDING -- wiring landed R202 (9b6zl6)]

> NUMBERING NOTE: grep confirmed before reserving -- `GT-114`/`RE-114` = 0 hits in both files, archive included (2026-08-27, this round). Highest number in use is `113` (`RE-113`, CLOSED PASS/DONE) => this entry is `114`.
> Entries `RE-085`-`RE-113` and `GT-101`-`GT-110` stay exactly where they are, unchanged -- this is a new entry, not a replacement for any of them.

## GT-128 GM-003 CHAT-WARP-VISIBLE-001 [attended, in-game]: GM พิมพ์ `/warp <ฉากปัจจุบัน> <x> <y>` ลงกล่องแชทธรรมดา แล้ว**ตัวละครขยับไปยังพิกัดนั้นบนจอจริงหรือไม่** -- ใบแรกของสาย GM ที่ตัดสินที่จอ ไม่ใช่ที่ log  [❌ **CANCELLED - refuted by R306 finding 3 (`notes_to_chief/20260903_1655_*`)** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2) — รูป same-scene ที่มีพิกัดส่ง `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS` แล้ว **ไคลเอนต์ปิดตัวเอง** (`ErrorData=28317`) วัดบนจอเจ้าของ ⇒ คำถามของใบนี้ ("ตัวละครขยับไปพิกัดนั้นไหม") ตอบไม่ได้ด้วยรูปเฟรมที่มีอยู่ และ `COO-DECISION 20260903_1744` ข้อ 3 สั่งปิด `/warp` แบบมีพิกัดไปแล้ว · 🔴 **เปิดใบใหม่ (ไม่ใช่ปลดใบนี้) เมื่อ LANE-GM เปลี่ยนรูปเฟรมและมี headless proof** — ใบใหม่ต้องเขียนเกณฑ์บนรูปเฟรมใหม่ ไม่ใช่ยกด่านเก่าทั้งชุดมาใช้ · สถานะเดิม: ~~BLOCKED — token compares nothing (COO-DECISION 20260829_0041)~~ **STILL BLOCKED — token fixed, but a separate COO-held gate remains (see chief R243 update at end)**: ห้ามเกรด ห้ามบันทึกผลใด ๆ ด้วยโทเคน `GM_WARP_POSITION_CONFIRMED` ตัวปัจจุบัน เพราะมันเทียบแค่ "แถวเปลี่ยนค่า" ไม่ได้เทียบกับ**จุดที่สั่ง** · ปลดเมื่อชุดแก้โทเคน+audit ลง main (chief, ภายใน 2026-08-29 23:59+07:00) · **อัปเดตรอบ `nz0qt2`:** ครึ่ง audit ที่เป็นเขต LANE-GM (แถว `outcome`, `CORE-REQUEST-GM-032` ข้อ 1-2) อยู่ใน PR `pirate-force-server#223` **รอ merge** · ครึ่งโทเคน (`GM_WARP_POSITION_TARGET_MATCH/MISMATCH`, `CORE-REQUEST-GM-031`) และข้อ 3 ของ GM-032 ยังเป็นของ chief ⇒ ป้าย BLOCKED ของใบนี้ **ยังไม่ถูกปลด** ด้วยรอบนี้ · 🔴 **เหตุผลที่วัดแล้ว ไม่ใช่แค่เหตุผลเชิงหลักการ** (เพิ่มโดย LANE-GM เจ้าของใบ รอบ `xk4wmz`): pf-adversary วัดว่าโทเคนตัวปัจจุบัน **ยิงตอนผู้เล่นเดินเองหนึ่งก้าว**หลัง warp ที่ไคลเอนต์เมิน ⇒ ใบนี้ "ผ่าน" ได้โดยที่ warp ไม่ทำงานเลย · **ของที่ LANE-GM ทำเสร็จแล้วเพื่อชุดของ chief:** `gm/warp_target_record.py` เก็บปลายทางของ warp ใบนั้นไว้เทียบได้ หยิบได้ครั้งเดียว ผูกกับ `character.id` (รอบ `z6gu2n` บน main แล้ว) และ `CORE-REQUEST-GM-031` ขอให้ chief พิมพ์ `GM_WARP_POSITION_TARGET_MATCH` / `..._MISMATCH` **เพิ่ม** จากโทเคนเดิม (ห้ามเอา match มาเป็นเงื่อนไขของโทเคนเดิม -- วันนี้ client เมิน `ForcePos` ผลที่คาดคือ MISMATCH ถ้ารวมกันโทเคนจะหายทั้งใบ) · BLOCKED x4 รวมข้อนี้ (~~x3~~ ~~x2~~ นับผิดมาแต่แรก มีสามข้อมาตลอด) -- ห้ามบูต: (ก) `CORE-REQUEST-GM-029` ยังไม่ลง main (จุดเรียกที่คืน action ที่สาขา `0xAC52`) · **อัปเดตรอบ `vvxkft`:** ตัวโมดูล `gm/chat_command_action.py` เองก็เพิ่งกลับขึ้น main รอบนี้ (PR #204 -- PR #200 ของรอบ `gr2q9j` ถูกปิดเพราะ gate แดง ไม่เคย merge) และ GM-029 เปลี่ยนความหมายเป็น "**แทนที่**บรรทัด `fire()` ของ GM-028 ในคอมมิตเดียว" ไม่ใช่ "เพิ่มจุดเรียก" (ใบ `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md`) ⇒ วันที่ใบนี้บูตได้ `GT-127` จะใช้ไม่ได้ตามเกณฑ์เดิมอีกต่อไป เพราะ event เปลี่ยนเป็น `gm_chat_action_*` -- **บูต `GT-127` ให้จบก่อน** (ข) ~~`RE-129` ยังไม่ตอบ~~ **RE-129 ตอบแล้ว 2026-08-28T20:09+07:00 (`ForcePos vital_version = 0`) แต่ข้อนี้ยังบล็อกอยู่ด้วยเหตุใหม่:** `COO-DECISION 20260828_2130` ล็อกแข็งว่าห้ามเปลี่ยน `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None` จนกว่าจุดเขียนตำแหน่งแบบยืนยันจะอยู่บน main (`CORE-REQUEST-GM-030`, รอบ `fo2lgh`) **แม้ RE-129 จะตอบก่อนก็ตาม** ⇒ โมดูลยังปฏิเสธการส่งด้วยตัวเอง และตอนนี้มีเทสบังคับด้วย (`pirate-force-server/tests/test_gm_force_pos_version_lock.py` แดงถ้าเปลี่ยนค่าก่อนโทเคน `GM_WARP_POSITION_CONFIRMED` อยู่บน main) · เหตุผลชั้นที่สองจาก RE-129 เอง: handler ที่ client จดทะเบียนไว้สำหรับ `ForcePos` = `mov al,1; ret 4` ไม่อ่าน payload ⇒ **version ถูกไม่ได้แปลว่าจะขยับ** ใบนี้ยังเป็นใบเดียวที่ตัดสินข้อนั้นได้ (ค) ~~🔴 **คำถาม "ใครเป็นเจ้าของตำแหน่งหลัง warp" ยังไม่มีคำตอบ**~~ **ตอบแล้ว 2026-08-28T21:30+07:00 (`COO-DECISION`): เจ้าของคือตำแหน่งที่ client ยืนยันแล้ว · เซิร์ฟเวอร์ห้ามเขียนตำแหน่งที่ตัวเองไม่ได้สังเกตเห็น · ตัวยืนยันคือ `TargetPos` ใบแรกหลังเฟรม** ⇒ ข้อนี้เหลือ "รอการเดินสาย" ไม่ใช่ "รอคำตอบ" -- ปลดเมื่อ `CORE-REQUEST-GM-030` ลง main และ COO ปลดล็อก · ผู้เทสต้องบันทึกในผล: หลัง warp ให้เดินหนึ่งก้าวเพื่อบังคับ `TargetPos` แล้วดูว่าคอนโซลมี `GM_WARP_POSITION_CONFIRMED` หรือไม่ · **บริบทเดิมของข้อนี้ (เก็บไว้):** — pf-adversary รอบ `gr2q9j` ชี้ว่า หลังส่ง `ForcePos` แล้ว แถวใน DB และ `selected.position` ยัง**ค้างที่จุดเดิม** (โมดูลไม่เรียก `foundation.checkpoint`) ⇒ client อยู่จุดใหม่ เซิร์ฟเวอร์คิดว่าอยู่จุดเก่า · aggro/pickup/logout ใช้จุดผิด · ต้องได้คำตอบ (`ASK-COO` รอบนี้) **ก่อน**เปลี่ยนค่าคงที่ของ `RE-129` ไม่ใช่หลัง · **อัปเดตรอบ `38c4tv` 2026-08-29T08:22+07:00 (LANE-GM เจ้าของใบ) — เพิ่มด่านก่อนบูตข้อ 4 ไม่ได้ปลดหรือเพิ่มบล็อก:** จดหมาย chief `20260829_0604` ข้อ ②bis (ก) วัดได้ว่าล็อกอินที่ใช้ override ฉากเป็น **visit** ⇒ ไม่เขียนแถวตำแหน่ง ⇒ `GM_WARP_POSITION_CONFIRMED` **ไม่มีทางยิง** บนเซสชันนั้น · ใบนี้ตัดสินด้วยโทเคนนั้น จึงต้องยืนยันก่อนบูตว่าบัญชีไม่มีใบล็อกอินค้าง ทั้ง `gm_login_scene.json` และ `gm_login_scene_standalone.json` (ดูด่านข้อ 4) 🔴 กับดักซ้อน: ขั้นตอนข้อ 4 ของใบนี้เอง (`/warp <ฉากอื่น>`) เป็นตัวสตางค์ใบนั้น · **อัปเดต chief รอบ `3ru85y` (R243) 2026-08-30T~16:xx+07:00 — CORE-REQUEST-GM-030/031 wired, แต่ตัวบล็อกจริงของใบนี้ยังปิดอยู่:** `GM_WARP_POSITION_TARGET_MATCH`/`_MISMATCH` พิมพ์แล้วจริง เพิ่มจากโทเคนเดิม ไม่แทนที่ (พิสูจน์ headless: warp ตรงพิกัด -> MATCH หนึ่งบรรทัด, warp ผิดพิกัด -> MISMATCH พร้อมระยะ, เดินเองไม่มี warp -> ไม่มีทั้งคู่, target ค้างข้ามเฟรมไม่เกิด — เทสใหม่ 5 ใบใน `tests/test_gm_warp_position_confirmed.py`, สวีตเต็ม 5480 passed) · 🔴 **pf-adversary พบ**: กิ่ง `unknown_character_mismatch` ที่ `CORE-REQUEST-GM-031` ข้อ 5 ขอ เป็น **dead code ในโปรดักชัน** — ลำดับการ์ดเดิม (`character_changed` early-return) ดักทุกกรณี re-select จริงไว้ก่อนกิ่งใหม่จะถึง เทสที่พิสูจน์กิ่งนี้ต้อง park เป้าหมายตรงผ่าน `record_warp_target` เอง ไม่ใช่ผ่านเส้นทาง `/warp` จริง — [ไม่อ้าง] ว่ากิ่งนี้ทำงานได้จริงในโปรดักชัน คงไว้เป็น defense-in-depth ตามที่คอมเมนต์ใหม่ใน `runtime.py:_gm_warp_open_confirm_window` บันทึกไว้ ส่งคำถามลำดับการ์ดนี้ต่อให้ LANE-GM/COO ตัดสินว่าจะแก้หรือรับสภาพ (ดูจดหมาย `CHIEF-REPLY` รอบนี้) · pf-adversary ยังพบบั๊กเดิมที่ไม่เกี่ยวกับ diff นี้ (rearm เป็นตัวละครอื่นก่อนมี TargetPos ทำให้ `gm_warp_pending_character` ค้างชื่อเก่า แล้วโทเคนทั้งชุดเงียบทั้งเฟรมของตัวละครใหม่) — ไม่แก้รอบนี้ (นอกขอบเขตใบ) รายงานไว้ให้ทราบ · ~~🔴🔴 **ตัวบล็อกจริงของใบนี้ทั้งใบยังไม่ปลด**: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` ยังเป็น `None`~~ **อัปเดต chief รอบ `9fv1m8` (R253) 2026-08-31T~02:1x+07:00: ค่าคงที่ปลดแล้ว** (`teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = 0`, ตาม `COO-DECISION 20260830_1645`/`1742` -- ค่า RE-129 literal ไม่ใช่การอ่านชื่อ `*_PROVEN_BY_RE129`) พร้อมแก้เทส 13 ใบใน 6 ไฟล์ที่พึ่งค่า shipped เดิมโดยไม่ patch ตรง ๆ (pf-adversary รีวิวผ่านก่อน commit) สวีตเต็ม 5600 passed 0 failed เขียว(cloud sanity) · **รอ merge ก่อน** -- `pirate-force-server` PR ของรอบ `9fv1m8` ยังไม่ merge เช็ค `PR_STATE.txt` ก่อนบูต · ไบต์ `ForcePos` จะออกสายจริงเมื่อ merge แล้วเท่านั้น · ตัวบล็อกที่เหลือของใบนี้ (ลำดับการ์ด `unknown_character_mismatch` dead-code ที่ pf-adversary พบรอบ `3ru85y`, และ rearm-character bug ที่ยังไม่แก้) **ยังไม่ปลด** -- นี่คือแค่การเปิดสายไบต์ ไม่ใช่การปิดใบ ผู้เทสยังต้อง ยันหน้าจอจริงตามด่านเดิมของใบนี้]

> เลขใบ: ตัวนับเดียวร่วมกับ `CLIENT_RE_QUEUE.md` · รอบ `gr2q9j` จอง `RE-129` ที่นั่นและ `GT-128` ที่นี่
> grep ยืนยันก่อนจอง 2026-08-28T18:2x: `GT-128` / `RE-129` = 0 hit ทั้งสองไฟล์ · สูงสุดก่อนหน้า = `GT-127` / `RE-128`

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

## 🆕🔬 GT-159 M2-DEST-COLUMBUS-MARKER17-TRANSFORM-TO-SHIP-001 [attended, in-game]: ถ้าเซิร์ฟเวอร์เคยส่งฉาก 126 ที่ `MARKER[17]` พิกัด `(3050, 232, 90)` หันหน้า 6 แทนฉาก 17 -- ผู้เล่น**แปลงร่างเป็นเรือและอยู่ในทะเล**ตามที่เจ้าของจำได้ (`GT-106` ข้อ ④.2) จริงหรือไม่ -- ตัดสินด้วยตา ไม่ใช่ด้วยการเถียงตาราง  [⚪ **CANCELLED - covered by `GT-266` · no longer needs proving because `PANYA-DECISION 20260905_1329`** -- ปิดโดย chief (LANE-E) รอบ `m8wtlr`/R356 2026-09-05T17:0x+07:00 ตาม `COO-DECISION 20260905_1543` · **สองครึ่งของใบตายคนละทาง**: (ก) ครึ่ง "มาถึง 126 ที่ MARKER 17 (3050,232,90) แล้วเป็นเรือในทะเลจริงไหม" = `GT-266` วัดตรงตัว (จุดมาถึงเดียวกัน วัตถุที่ต้องเห็นเดียวกัน · กลไกขนส่งต่างกันไม่เปลี่ยนสิ่งที่ตาเห็น) · (ข) ครึ่ง "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" = **ไม่ต้องพิสูจน์แล้ว** เพราะ `PANYA-DECISION 20260905_1329` เคาะจุดมาถึง 126 = MARKER `n_ID 17` ถาวร — คำถาม id space ตายด้วยคำสั่ง ไม่ใช่ด้วยการเทส · 🔴 **สิ่งที่ยังไม่ถูกตอบและห้ามผูกกับใบนี้อีก**: Columbus ยังชี้ฉาก 17 บน main (`world_m2_sea_destination.py:314`) — เมื่อ LANE-A แก้ปลายทาง Columbus → 126 เป็น PR จริง **ใบ GT ของ PR นั้นออกใหม่ตอนนั้น** ไม่ใช่เก็บใบนี้รอ (`COO 1543` ข้อ 3 · เวลา attended แพงที่สุด `PANYA 20260903_1934`) · ~~🔴 BLOCKED (คงเดิม) -- การปิดใบของ chief รอบ `r045nx`/R354 ถูกถอน ในรอบเดียวกันหลัง `pf-adversary` D4 · ใบนี้ยังไม่ปิด และรอ COO ตัดสิน~~ **COO ตัดสินแล้ว `1543`**
> 🔴 **ที่ถอนและทำไม (chief เขียนเอง ไม่ใช่ให้ใครมาจับได้ทีหลัง)**: `COO-DECISION 20260905_1349` ข้อ 5 ให้ทางเลือกสองทางเท่านั้น — "ถ้าใช่ปิดด้วย `CANCELLED - covered by <GT ใหม่>` **ถ้าไม่ ระบุว่าต่างตรงไหน (สั้น)**" · chief สรุปเองว่าใบ `/warp 126` ใหม่ (`GT-266`) **ไม่ครอบ** ใบนี้ = ตกเข้าทาง "ถ้าไม่" ซึ่งอนุญาตแค่ให้**เขียนความต่าง** แต่ chief กลับปิดใบด้วยตัวครอบที่ COO ไม่ได้เอ่ยถึงเลย ⇒ **เกินอำนาจ** และขัดบรรทัดในหัวใบนี้เอง ("ห้ามปิดเองจนกว่า COO ตัดสิน" · `PANYA-DECISION 20260903_1934`)
> 🔴 **และข้ออ้างที่ใช้ปิดก็เกินจริง**: คำถามของใบนี้ไม่ใช่ "ฉาก 126 เป็นทะเลไหม" แต่คือ **กด Columbus (quest 3021) บนเซิร์ฟเวอร์ที่ถูกแก้ให้ส่ง 126@`MARKER[17]` แทน 17 แล้วเกิดอะไร** — เพื่อแยกสอง id space ที่ `world_m2_sea_destination.py:305-314` ประกาศเองว่า `[CONTESTED]` และ "no control in any table separates them" · บูตของ `GT-233` ทุกครั้งเข้าฉาก 126 ผ่าน `PF_M2_SURVEY_TRIAL` + relogin **ไม่เคยแตะ `columbus_quest_dispatch` หรือแถว 3021 เลย** ⇒ ไม่แยก id space ให้สักนิด · กิ่งผลลบของใบ ("ยังเป็นคน ไม่ได้อยู่ในทะเล เช่นยืนอยู่ฉาก 17") ไม่มีใครเคยเห็น
> 🔴 **และป้าย `OBSERVER_CONFIRMED 12:48` ถูกยืมผิดที่**: ใน R318 §2.2 ป้ายนั้นเซ็นประโยค "**ไม่มีหน้าต่างอะไรเด้ง**" (ผลลบของ `GT-233`) ส่วน "เป็นเรือ" อยู่ในย่อหน้าเดียวกันแบบ**ไม่มีลายเซ็น** ("`HP -1/1` ขณะเป็นเรือ (สังเกตการณ์)") — ย้ายป้ายข้ามข้ออ้างแบบนี้ผิด `G-OBS`/`G5` ตรง ๆ
> ⇒ **ที่ chief ทำได้ตามอำนาจจริงคือบรรทัดเดียวนี้**: `GT-266` (`/warp 126` สด) **ไม่ครอบ** ใบนี้ — `GT-266` ถามว่า "วาปสดขณะเล่นไปโผล่ 126 ได้ไหมโดยไม่ relogin" ส่วนใบนี้ถามว่า "`DESTINATION_SCENE_N_ID = 17` อ่านใน id space ไหน" ซึ่งต้องกด Columbus บนบิลด์ที่แก้ปลายทาง · **เสนอ COO: ใบนี้ยังจำเป็นหรือไม่ ในเมื่อกลไก M2 ที่เดินอยู่จริงคือ `RE-227`/`GT-233` ไม่ใช่การสลับปลายทางของ Columbus** — คำตอบเป็นของ COO ไม่ใช่ของ chief
> เดิม (ถอนแล้ว ไม่ลบเพื่อเป็นประวัติ): ~~`CANCELLED - covered by GT-233 boots R313/R315/R317/R318`~~
> เดิม: 🔴 **BLOCKED** · `STATUS-SET-BY-CHIEF 2026-09-05T02:0x+07:00 from body` ตาม `COO-DECISION 20260904_2349` ข้อ 6]

> 🔢 **หมายเหตุเลข:** grep ยืนยันก่อนจอง 2026-08-30T14:2x+07:00: `GT-159`/`RE-159` = 0 hit ทั้งสองไฟล์ ·
> สูงสุดก่อนหน้า `GT-158` (`GT`/`RE` ใช้ตัวนับเดียวร่วมกัน ตามกฎที่ `RE-152` หัวใบเคยระบุไว้)
> ⇒ ใบนี้คือ `GT-159` · ใบ `RE-085`-`RE-158`/`GT-001`-`GT-158` อยู่ที่เดิมทั้งใบ ห้ามลบ ห้ามย้าย ห้ามแก้ถ้อยคำ

## GT-188 GROUND-DROP-HEARTBEAT-PRESERVE-CONFIRM-001  [**checkpoint 1 = ❌ CANCELLED - covered by GT-216** (🟢 PASS สองชั้น · `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00`) · **checkpoint 2 = 🔵 MEASURED (BASELINE) รอบ R309 — ผลคือ "หาย"** ยังไม่ปิดใบ · ปิด cp1 โดย chief รอบ `oi2r2n`/R340 ตาม `COO-DECISION 20260904_1648` ข้อ 3 + `PANYA-DECISION 20260903_1934`]

> **checkpoint 1 คำต่อคำ**: "ของที่ตกยังเห็นอยู่บนจอข้าม heartbeat ~2 วิ อย่างน้อยสองรอบ (~4-5 วินาที ไม่หยิบ)" — `GT-216` **PASS สองชั้นบนจอเจ้าของ R306** วัดสิ่งที่แรงกว่านั้นไปแล้ว: เจ้าของคลิกเก็บ **10 ครั้ง เข้ากระเป๋า 9** ในรอบเดียว ⇒ ของอยู่บนพื้นนานกว่าสอง heartbeat หลายเท่า มิฉะนั้นคลิกครั้งที่สองก็ไม่มีอะไรให้คลิก · R307 (`GT-220`) เห็นซ้ำอีกครั้ง ของค้างเป็นนาทีจนหมดอายุ 120 วินาทีกลายเป็นของผี
> 🔴 **สิ่งที่การปิด cp1 ไม่ได้อ้าง**: ไม่ได้อ้างว่า `preserve_ground_heartbeat_frame` เป็นเหตุของผลนั้น (ใบตั้งคำถามชั้นจอ ไม่ใช่ชั้นสาเหตุ) · ไม่ได้อ้างว่าอ่าน reconciler ของ Codex ถูก — ใบเดิมก็เขียนไว้เองว่าไม่อ้าง
> 🔵 **checkpoint 2 ยังไม่ปิด และ COO สั่งยกเลิกเฉพาะ cp1**: cp2 ("หนึ่ง action ที่ถูกตอบ ล้างพื้นไหม") **ถูกวัดโดยบังเอิญในรอบ R309** — S4: เจ้าของเปิดกระเป๋ารอโดยไม่คลิกอะไร แล้วของบนพื้น**หายเอง** · สาย: ไคลเอนต์ส่ง `CheckSecondPwdVital 0x4B98` (64 B) → เซิร์ฟตอบ `V110_CHECK_SECOND_PASSWORD_OK` (44 B) **ลงท้าย `0B 00`** = ground-list ทรง CLEAR · หลังจากนั้น `MOB_DROP_PRESENCE … live=1 announced=0 carried=1 oldest_left=65.6s` ⇒ **เซิร์ฟยังถือของอยู่ ไคลเอนต์ล้างจอไปแล้ว** = คำทำนายของ cp2 เป็นจริง
> 🔴 **cp2 ยังไม่ถูกเกรด PASS/FAIL และห้ามยกไปเป็นฐานของใบอื่น**: ไม่มีภาพ STEP-D — เจ้าของเล่าเองในรอบ attended · ใบที่จะวัดซ้ำ**หลังแก้** คือ **`GT-242`** (เปิดรอบ `oi2r2n` เดียวกันนี้) · 🔴 `GT-242` **ห้ามผูกกับ `GT-223`** (`COO 1648` ข้อ 2)
> สถานะเดิม (ยกมาคำต่อคำ ไม่ได้ลบ): PENDING -- TWO CHECKPOINTS as of R299 (COO-DECISION `20260902_0347` item 4). Checkpoint 1 (heartbeat) is bootable now: PR #441 on main, verified `git merge-base --is-ancestor 072967a origin/main`. 🔴 Checkpoint 2 (one player ACTION) is a BASELINE measurement of TODAY, not a test of a fix: chief's vitals wrap was WITHDRAWN in R299 before it landed -- see RECHECK item 2

- objective: one claim only -- after the fix that patches `legacy.make_runtime_res_empty_exact` to `preserve_ground_heartbeat_frame` (wired in `src/pirateforce_foundation/app.py`, strictly before the `legacy.game_listener = adapt_game_listener(...)` line, per chief round 6o3gr1 and `pirate-force-server` PR #437), a real client that watches a mob drop an item keeps the dropped item's own non-text model/geometry (not merely its name-label, and not the killed mob's own corpse -- see steps/pass criteria/nonclaims 5-6) visible on screen across at least two ~2s heartbeat intervals (~4-5s total wait, no pickup), instead of the pre-fix behavior where the drop silently vanished within ~2s regardless of whether anyone picked it up. This is LANE-B's P-1 (COO-DECISION 20260901_0347): bug found and confirmed against real bytes in round n8kq4r, server-side fix landed round 6o3gr1. This ticket is the client-observable half; it does not by itself prove Codex's client-image read of the reconciler.
- db: default state\pirateforce.sqlite3 -- always a fresh copy for this boot only, never the canonical file. Record the copy's filename and sha256 before/after the round, and confirm the canonical file's sha256 is unchanged before/after.
- server args: standard playbook boot on `main`, with both `pirate-force-server#437` (mob_loot.py, merged) and `#441` (app.py wiring, chief round 6o3gr1) confirmed present on `main`. No special flags required. Do not boot until RECHECK below shows both are in.
- steps:
  1. Boot server, confirm it is freshly started (age < 3.5 min) and not a leftover from a previously killed client; boot client only after server is up.
  2. Log in. Right-click-drag only (camera rotation, does not change facing, emits nothing) to a clean angle -- no Q/E, no WASD yet. Full-res photo BASELINE, recorded as two separate fields: (a) non-text item model/geometry visible on the ground y/n (expect none -- no mob has been killed yet; dust, shadows, any name/label text, and (once a kill happens) the killed mob's own corpse/body mesh never count as a model sighting -- see step 3's own note), and (b) name-label visible y/n plus the colour of every name label in frame (one line per label, write "none" if there are none). Also record scene name and X/Y/Z from HUD.
  3. Kill exactly one mob that drops an item. If the kill produces more than one drop/loot event (this project has observed a single kill emit two `MOB_LOOT_DROP` events, per `GT-084`'s own result line), pick one dropped item at STEP-A and track that same one through STEP-B/STEP-C -- name which item (by icon/appearance and rough ground position) you are tracking, in writing, at STEP-A, so a later step can be checked against it. Immediately after the drop appears, full-res photo STEP-A, recorded as two separate fields: (a) non-text item model/geometry visible on the ground y/n -- the actual dropped-item 3D object, distinct from any name/label text, dust, or shadow, and distinct from the killed mob's own corpse/body mesh at the kill site (none of those ever count as a model sighting -- this project has separately confirmed, in `GT-084`/`GT-084-R2`/`GT-129`/`RE-107`, that a killed mob's corpse can freeze in place and persist on screen indefinitely, which is a known, unrelated client bug, not evidence for this ticket's claim; if a corpse is present, describe the tracked item's shape/position as distinct from the corpse, not merely "something is there"), and (b) name-label visible y/n plus the colour of every name label in frame (one line per label, write "none" if there are none).
  4. Do not pick up the item. Wait past at least one heartbeat interval (~2-3s) without moving (right-click-drag only if a liveness check is wanted -- do not use Q/E or WASD, that would change facing and emit TargetPosVital, which is not part of this claim). Full-res photo STEP-B on the same tracked item as STEP-A, recorded as two separate fields: (a) non-text item model/geometry still visible y/n (dust/shadow/label text and the mob's own corpse/body mesh never count -- see step 3's note), and (b) name-label still visible y/n plus label colours.
  5. Continue waiting to cross a second heartbeat (~4-5s total elapsed since the drop appeared). Full-res photo STEP-C on the same tracked item, recorded as two separate fields: (a) non-text item model/geometry still visible y/n (dust/shadow/label text and the mob's own corpse/body mesh never count -- see step 3's note), and (b) name-label still visible y/n plus label colours.
  6. Record wall-clock time for every step, to cross-check against the server console/capture log afterward.
  7. Optional, non-blocking, not part of this ticket's pass/fail: if the tracked item's model is still visible at STEP-C, the tester may click it and note whether a pickup opcode appears to fire. This is colour only -- it does not stand in for GT-146's own claim and must not be written as gating or blocking GT-146, which remains a separate ticket held under its own hold.
  8. 🔴 CHECKPOINT 2, added R299 (COO-DECISION `20260902_0347` item 4). Only after STEP-C is photographed: take exactly ONE action the server answers with a vital -- one `W` step is enough (it sends `TargetPosVital` and the server answers) -- and then STOP moving again. Full-res photo STEP-D on the same tracked item, same two separate fields as every step above: (a) non-text item model/geometry still visible y/n (dust/shadow/label text and the mob's own corpse never count), (b) name-label still visible y/n plus label colours. Record the wall-clock time of the keypress and of the photo. One action, not several: the question is whether a SINGLE answered vital wipes the ground, and a burst of them cannot tell which one did it.
  🔴 **R301 (chief, รอบ `smrum3`) -- ห้ามพลิก checkpoint 2 เป็น "วัดผลของการแก้" ตาม `COO 0646` ข้อ 5 ยัง**
  `COO 0646` ข้อ 5 เขียนไว้ว่าเมื่อ `action_ack` ขึ้น main ให้พลิกข้อนี้กลับเป็นการวัดผลของการแก้ · **chief ไม่พลิก และนี่คือเหตุผล** (pf-adversary รอบเดียวกัน D4, วัดแล้ว):
  ① ขั้นนี้สั่งกด `W` = `TargetPosVital` · จุดที่ opt-in คือ **EA7D ActionVital** หลังจับ TargetVital kind 1 ⇒ คนละเส้นทาง
  ② ขั้นนี้สั่งบูต **"No special flags required"** · จุดที่ opt-in เปิดด้วย `--scene-load-scenario ..._ea7d_ack.json` เท่านั้น ⇒ ไม่ใส่แฟล็ก = `scene_load_scenario` เป็น `None` ⇒ **บรรทัดที่แก้ไม่ถูกรันเลยแม้แต่ครั้งเดียว**
  ⇒ ถ้าพลิกตามตัวอักษร ผลของการกด `W` บนเซิร์ฟเวอร์ที่โค้ดใหม่ไม่เคยทำงาน จะถูกบันทึกเป็นหลักฐานของโค้ดใหม่
  **checkpoint 2 ยังเป็น "วัดสภาพวันนี้" ตามเดิม** จนกว่าจะมีขั้นที่กดปุ่มที่ไปถึงจุดนั้นจริง ใต้แฟล็กที่เปิดมันจริง · ส่งคำถามกลับ COO ในใบ `20260902_0920`
  🔴 RECHECK ข้อ 2 ของใบนี้ (`grep install_ground_vitals_preserve app.py` ต้องไม่มีผล) **ตาบอดต่อการ opt-in รายจุด** -- มันผูกกับชื่อไฟล์และสัญลักษณ์ของ wrap ที่ถอนไปแล้ว ไม่ใช่กับ composer ที่จุดไหนใช้ · ตัวตรวจที่เห็นจริง: `git grep -n 'preserve_ground_in_runtime_res_vitals' -- src/pirateforce_foundation/`
- pass criteria (two layers, kept separate):
    wire/DB: the server console/capture log for this boot shows the heartbeat frames sent during the STEP-B/STEP-C windows carry the PRESERVE shape (ground-list mask 0x08 present, count 0, no elements -- the same envelope `drop_collection_pc` already uses) rather than the old CLEAR shape (`0x0B, 0x00` twice, read by the client as `TerrainThingPool == NULL`). This is provable headless, from the capture log alone, and does not by itself prove what the client drew on screen.
    🔴 TWO CHECKPOINTS, GRADED SEPARATELY (R299): CHECKPOINT 1 = STEP-B/STEP-C, standing still across at least two heartbeats. CHECKPOINT 2 = STEP-D, after exactly one answered action. They are separate results and this entry records BOTH; do not collapse them into one PASS/FAIL. If checkpoint 1 passes and checkpoint 2 fails, that is the EXPECTED shape today (no vitals fix exists on `main`; see RECHECK item 2), and the heartbeat half stays regardless -- which is also what COO-DECISION `20260902_0347` item 4 ordered for the case where a vitals fix does exist and does not hold. If checkpoint 1 itself fails, checkpoint 2 tells us nothing and must be recorded as NO-RESULT rather than as a second failure.
    client-observable: the human at the screen reports, from the BASELINE/STEP-A/STEP-B/STEP-C/STEP-D photos, the model and label fields recorded separately per step above, for the one tracked item named at STEP-A. PASS on this ticket's own claim -- that the dropped item's own model/geometry persists on screen across heartbeats -- requires non-text model/geometry to be visible (not just a label, and not the killed mob's own corpse/body mesh -- see step 3/nonclaim 6) at STEP-A, and the same tracked item to remain visible through STEP-B and STEP-C. If STEP-A never shows the item's model (label only, corpse only, or nothing at all), do not mark this ticket's model-persistence claim PASS or FAIL: record it as NO-RESULT, and record the label's own visibility at STEP-B/STEP-C separately alongside it -- a label-only or corpse-only sighting must never be used to satisfy this ticket's own claim. Where the item's model was seen at STEP-A, a negative result (model vanishes by STEP-B or STEP-C despite not having been picked up) is a finding worth exactly as much as a PASS -- record it as such. A negative would mean the PRESERVE-shape server fix did not restore client-side persistence, and would redirect further investigation to nonclaim 1 below (the client-image read of the reconciler), not back to the server wiring, which this round's own tests already pin at the byte level.
- nonclaims:
  1. Does not verify Codex's static IMAGE read of the client reconciler (`GSCN_RunTimeProtocolRes+0x20` / `DropThingModule_Client`) against the client binary itself -- this round's fix was cross-checked only from the server side (byte inspection of `make_runtime_res_empty_exact()` output at offsets 10-13).
  2. Does not claim a full running-server boot test exists anywhere in the repo -- `app.py` is not unit-boot-tested elsewhere in this repo's test layout. The wiring is pinned structurally (`test_app_installs_the_ground_heartbeat_patch_before_adapting_the_listener`) and behaviorally, with a real `legacy` load proving the patch only fires for a caller named `heartbeat_worker` and every other caller (e.g. the connect-time `RUNTIME_RES_ACK_FIRST_REQ`) keeps v141's original bytes (`tests/test_foundation_legacy_seam.py::FoundationLegacySeamTests::test_ground_heartbeat_patch_only_changes_the_heartbeat_worker_caller`), plus at the byte level (`tests/test_mob_loot.py::PreserveGroundHeartbeatTests`, 7/7 passing) -- not end-to-end via a live server boot.
  3. Does not require or claim that the pickup-click opcode is captured during this same session -- that is GT-146's own claim, on its own hold. This ticket must not be treated as blocking or gating GT-146.
  4. Does not attribute a cause to any label's colour -- record colours only, per RE-067 (the cause of label colour is unknown and is that ticket's own subject; do not infer here).
  5. This ticket's own claim is about client-rendered item model/geometry persisting on the ground, not about name-label text persisting -- that is exactly why BASELINE/STEP-A/STEP-B/STEP-C track model-visible and label-visible as two separate fields instead of one combined "drop visible" field. A label alone, with no model ever having rendered, proves nothing about this ticket's claim and must be recorded as NO-RESULT for the model question, per `notes_to_chief/CODEX_URGENT_20260901_1350_GT188-MODEL-NOT-LABEL-GATE.md` and conflict item #1 of `notes_to_chief/20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md`.
  6. Does not accept the killed mob's own corpse/body mesh as evidence of the dropped item's model -- this project has separately, previously confirmed (`archive/notes_to_chief_2026-08/20260827_1620_GT084R2-RESULT-PASS-hostile-kill-full-wire-but-corpse-freezes-no-target-panel.md`, OBSERVER_CONFIRMED; `CLIENT_RE_QUEUE.md` RE-107, CLOSED BOUNDED-NEGATIVE; `GT-129`) that a killed mob's corpse can freeze in place and persist on screen indefinitely, as a known, unrelated, still-open client bug with its own tickets. A corpse sighting at STEP-A/B/C is not this ticket's claim and must not be recorded as a model sighting; step 3 requires the tester to name/describe the tracked dropped item distinctly from any corpse present at the same kill site. [pf-adversary finding, round `1mw5lf`]
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="preserve_ground_heartbeat_frame" --grep="make_runtime_res_empty_exact" --grep="GT-188" | head -5`
  (confirm both `#437` and `#441` are present on `main` before booting; empty or partial output means still BLOCKED -- do not boot, report back instead).
- RECHECK item 2 (checkpoint 2 only, added R299, CORRECTED the same round): `cd pirate-force-server && grep -n "install_ground_vitals_preserve" src/pirateforce_foundation/app.py` on a fresh `main` clone must print NOTHING. That is the CORRECT state: chief built that wrap in R299, pf-adversary measured that it kills the game-listener thread on two live paths (`--second-password-mode bypass`, every backpack item move) while preserving the ground on none of the paths a player's action actually takes, and it was withdrawn before it was committed (letter `notes_to_chief/20260902_0605_CHIEF-TO-COO-vitals-preserve-wrap-withdrawn-*`). If that grep ever DOES print, a later round relanded it -- read that round's letter before booting, because this entry's checkpoint 2 then means something different.
- 🔴 WHAT CHECKPOINT 2 MEANS TODAY (R299, chief, corrected): NOTHING on `main` preserves the ground across a player's action. The answer to a movement step is composed by this project's own `action_ack`, not by the frozen snapshot, and no site has been opted in yet. So a drop that VANISHES at STEP-D is the EXPECTED result and is still worth the photo: it is the first client-observable confirmation of the reading this whole thread rests on (an empty derived mask clears the ground), and it is the control that a later per-site fix will be graded against. A drop that SURVIVES at STEP-D is the more interesting result -- it would mean the reading is wrong and the per-site plan should stop before it starts. Either way this is a measurement of today, not a PASS/FAIL of anyone's fix.
- links: `pirate-force-server#437` (mob_loot.py, merged) -- `pirate-force-server#441` (app.py wiring, chief round 6o3gr1) -- `notes_to_chief/consumed/20260901_0420_LANE-B-CORE-REQUEST-heartbeat-preserve-ground-list-fixes-drop-clear.md` (original CORE-REQUEST, now consumed) -- `notes_to_chief/consumed/CODEX_URGENT_20260901_0407_DROP-EVIDENCE-CORRECTION.md` and `notes_to_chief/consumed/20260901_0443_CODEX-CHECKPOINT-THREE-PRIORITY-GATES.md` (evidence boundary) -- `COO-DECISION 20260901_0347` (assigned LANE-B this investigation) -- `PROCESS_GATES.md` rule #18 -- `notes_to_chief/CODEX_URGENT_20260901_1350_GT188-MODEL-NOT-LABEL-GATE.md` (model-vs-label pass-gate warning, folded into steps/pass-criteria this round) -- `notes_to_chief/20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md` conflict item #1 (same warning, second source).
- numbering: per the shared-counter search command (rule ② at the top of this file), the highest confirmed number before this entry, across `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`, and `archive/*QUEUE*ARCHIVE*.md`, is `GT-187`. This entry is `188`.
- result: (tester fills in: PASS/FAIL/BLOCKED, evidence, timestamp, OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

## GT-205 UI-A-BACK-BUTTON-VISIBLE-NOTICE-001  [🟡 **ไม่ยกเลิก — ครึ่ง wire ยังไม่ถูกวัดสำหรับ subcode ของใบนี้** (chief รอบ `pk14rf`/R326 ตาม `PANYA-DECISION 20260903_1934` + `COO 20260903_1943` ข้อ 2): `GT-211` พิสูจน์ composer ตัวเดียวกันบนสาย (`LANE_A_UIA_NOTICE_COMPOSED ... EXIT REFUSED` 66 ไบต์) แต่นั่นคือ **subcode ของปุ่มล็อกเอาต์** ไม่ใช่ subcode 3 ของใบนี้ ⇒ ไม่เข้าเงื่อนไข covered ทั้งสามรูป · 🔴 **เจ้าของใบ LANE-A เป็นคนตัดสินว่า subcode 3 ยังต้องวัดสายของตัวเองไหม** (เจ้าของสั่งไว้เองในใบ `1934`) — ตัดสินแล้วให้เขียนบรรทัดปิด/คงเปิดที่หัวใบนี้ในรอบเดียวกัน · ป้าย `BACK_REFUSED`→`EXIT` ที่ `COO 20260903_1746` ข้อ 2 สั่ง แก้เสร็จแล้วต้องอัปเดตสตริงในเกณฑ์ของใบนี้ด้วยในรอบเดียวกัน (`AGENTS.md` §7) · สถานะเดิม: **client-observable = PASS · wire/DB = NOT MEASURED · ใบยังไม่ปิด** — สถานะเขียนโดย LANE-A (เจ้าของใบ) รอบ `kozzu1` 2026-09-03T11:5x+07:00 · 🔴 **จงใจไม่เขียน `✅ PASS` เดี่ยว ๆ**: เกณฑ์ของใบนี้เขียนเองว่า "TWO layers -- neither layer may ever be offered as proof of the other" และรอบ R303 วัดมาชั้นเดียว ⇒ ปั๊ม PASS ทั้งใบคือรูปเดียวกับหนี้ `GT-192` ที่ถูกบันทึกว่าจ่ายสองรอบ (ผู้ตรวจ pf-adversary รอบ `kozzu1` D3) · **ตัวปิดใบเหลืออะไร: คัดโทเคน `LANE_A_UIA_NOTICE_COMPOSED` จากคอนโซล + ตารางสีป้ายชื่อตามเกณฑ์ + ระบุว่าบรรทัดขึ้นที่พาเนลไหน** — สามอย่างนี้เก็บได้ฟรีในรอบ attended ถัดไปที่บูตอยู่แล้ว ไม่ต้องบูตเพื่อใบนี้ใบเดียว · 🔴 **คำตัดสินของเจ้าของใบ (LANE-A รอบ `gs8hmn` 2026-09-03T22:5x+07:00 ตาม `PANYA-DECISION 20260903_1934` + chief `20260903_2010`): คงเปิด แต่เป็น "เก็บฟรี" เท่านั้น — **ห้ามบูตรอบ attended เพื่อใบนี้ใบเดียว ไม่ว่ากรณีใด** ถ้ารอบ attended ถัดไปจบโดยไม่มีใครบูตอยู่แล้ว ใบนี้ค้างต่อได้ ไม่นับว่าใครค้าง · เหตุผลที่ไม่ปิด: เกณฑ์ของใบนี้เขียนเองว่าสองชั้น และชั้น wire ของ **subcode 3** ยังไม่เคยถูกวัด — `GT-211` วัด subcode ของปุ่มล็อกเอาต์ ไม่ใช่ subcode นี้ (chief ตัดสินแล้วว่าไม่เข้า covered ทั้งสามรูป) ปิดตอนนี้ = ปั๊ม PASS จากชั้นเดียว รูปเดียวกับหนี้ `GT-192` · เหตุผลที่ไม่ให้บูตเพื่อใบนี้: เวลา attended คือทรัพยากรที่แพงที่สุด (`1934`) และตัวปิดสามอย่างที่เหลือเก็บได้จากคอนโซลของบูตใด ๆ ที่มีอยู่แล้ว · 🔴 **กฎ grep `AGENTS.md` §7 ไม่เข้าเงื่อนไขกับใบนี้ วัดแล้วไม่ใช่เดา**: การเปลี่ยนชื่อป้ายรอบ `omhpqj` แตะปุ่ม UI-B ปุ่มเดียว (`UIB_ACTION_LABEL`) · ป้ายของ UI-A ยังเป็นสตริงเดิมของ chief เป๊ะ (`world_logout_button_notice.py:503` `UIA_ACTION_LABEL = "LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE"`) และบรรทัดเดียวที่ chief ยังจะสลับ (~~`runtime.py:7033`~~ **เลขบรรทัดนี้เน่าแล้ว จริงคือจุดที่ประกอบ `uia_notice_actions` ในสาขา `nested_id == LOGOUT_VITAL_ID` — grep เอา อย่าใช้เลข**) อ่านค่าเดียวกันนั้นกลับมา ⇒ **สตริงที่ใบนี้ grep (`LANE_A_UIA_NOTICE_COMPOSED` และ `BACK REFUSED`) ไม่ถูกแตะทั้งก่อนและหลังที่ chief สลับ ไม่ต้องแก้เกณฑ์ข้อไหน**
> 🆕 **อัปเดตรอบ `oi2r2n`/R340 (chief) — หนี้ "แก้สตริงในเกณฑ์รอบเดียวกัน" ที่หัวใบนี้สั่งไว้: จ่ายแล้ว โดยการวัดซ้ำ ไม่ใช่การแก้**: chief สลับบรรทัดนั้นแล้วรอบนี้ (PR เซิร์ฟเวอร์ `oi2r2n` ยังรอเกต) · วัดซ้ำแล้วว่าใบนี้ **ไม่มี** สตริง `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE` อยู่ในเกณฑ์เลยสักที่ และสองสตริงที่มันใช้จริง (`LANE_A_UIA_NOTICE_COMPOSED` · `BACK REFUSED`) ไม่ถูกแตะ ⇒ **ไม่มีเกณฑ์ข้อไหนต้องแก้** · ป้าย UI-A ไม่เปลี่ยนทั้งสองโลก · หนี้เดียวกันของ `GT-211` **ต้องแก้จริง** และแก้ไปแล้วในใบนั้น (ที่นั่นมีสตริงนี้อยู่ในเกณฑ์)
> **ชั้น client-observable = PASS (รันแล้ว R303 2026-09-02 เจ้าของกดปุ่มเอง)**: บรรทัด `[thua pai] : BACK REFUSED` **ขึ้นบนจอ** = ข้อความสำเร็จของใบเอง (ยกคำจาก `notes_to_chief/20260902_1755_KA1A-R303-RESULTS-*.md`) · สกรีนช็อตอยู่กับเจ้าของ **ไม่ได้อยู่ในรีโปทั้งสอง** (ไม่มี path ไม่มี sha256) · boot `7e14bde1` · capture `capture_r303_20260902_161029`
> **บูตนั้นไม่มี scenario ล็อกเอาต์แน่นอน** (ไม่ได้อ่านจากใบ แต่ตามจากเกต: `runtime.py` ประกอบบรรทัดนี้เฉพาะตอน `logout_hypothesis_scenario is None`) · 🔴 **แต่ "บูตไร้แฟล็ก" ยังไม่ถูกวัด** — ใบสั่งเขียนว่า "NO scenario flag of any kind" แต่ **คำสั่งไม่ใช่การวัด** และใบผลบันทึก head/boot/tree/db/capture/jobs/teardown แต่ **ไม่มี argv** · โมดูลยังประกอบบรรทัดนี้บนบูตที่ถือ scenario อื่นอีกราว 28 ตัว (docstring ข้อ 3 ของโมดูลวัดไว้เอง)
> **ทำไมถึงเชื่อว่าเป็นไบต์ของเซิร์ฟเวอร์**: บรรทัดที่เห็นมี **ช่องผู้พูดว่าง** (`[ป้ายช่อง] : ข้อความ`) ขณะที่ของที่ไคลเอนต์สะท้อนเองอ่านว่า `[ป้ายช่อง] Arena01: ...` และ `say_wire.DEFAULT_SPEAKER = ""` ถูกปักไว้ ⇒ เป็นตัวจำแนก **แต่ไม่ใช่หลักฐานปิด** เพราะไม่มีใครในรีโปเห็นสกรีนช็อต
> 🔴 **เจ็ดอย่างที่รอบนั้นไม่ได้เก็บ ห้ามอ่านว่าเก็บแล้ว**: (1) **ชั้น wire/DB ไม่ได้วัด** — ใบผลเขียนเองว่า "wire/DB: not separately instrumented for this ticket" ⇒ ชั้นนั้นยังยืนบนหมุด headless ใน `tests/test_world_logout_button_notice.py` เหมือนเดิม · (2) **ขั้น 8 ไม่ได้ตอบว่าไดอะล็อกยังเปิดอยู่ไหม** · (3) **ความยาว 12 ตัวอักษรไม่ขยับ** ไม่ได้อนุญาต 5 หรือ 26 · (4) **argv ของบูต** · (5) **บรรทัดขึ้นที่ไหนบนจอ / ห่างจากคลิกกี่วินาที / อยู่นานแค่ไหน** — ขั้น 8 ถามห้าข้อ ใบผลตอบข้อเดียว ⇒ เกณฑ์ "in the local chat/talk area" **ยังไม่ถูกยืนยัน** · (6) **ตารางสีป้ายชื่อทุกภาพ** ที่เกณฑ์บังคับไว้ **ไม่มีในผลเลย** = skip ที่ไม่มีใครนับ · (7) **n = 1** คลิกเดียว เซสชันเดียว และเป็นบูตที่ใบก่อนหน้า (`GT-193`) เพิ่งฆ่าตัวละครและทำให้ไคลเอนต์ไม่ส่งอะไรเลย — ไม่มีบันทึกว่ามีการรีล็อกอินคั่นหรือไม่
> 🔴 **ผลนี้ไม่ได้แปลว่า UI-A เสร็จ** ปุ่มยังพากลับหน้าเลือกตัวละครไม่ได้จริง (`GT-184` ยังเปิด · `NOW.md` คิว UI-A) · 🔴 **ไม่ใช่หลักฐานของ `GT-211`** (subcode 1 คนละปุ่ม) · 🔴 คำถามถึง chief: ใบนี้ถูกใส่กลับเข้าคิวผู้เทสหลังผล R303 มาแล้วสองครั้ง (`FROM_CHIEF_R308` · R317 §4) ขณะที่ `NOW.md` เขียนว่า PASS — ถ้าตั้งใจให้รันซ้ำเพื่อเก็บสามอย่างที่ขาด **ขอให้เขียนในใบว่ารันซ้ำเพื่ออะไร** ไม่งั้นผู้เทสจะเผาบูตซ้ำข้อเดิม
> ~~[🟢 READY (R303, 2026-09-02T13:0x+07:00) -- PR #563 merged 11:55 +07:00; RECHECK run by chief on `origin/main` `96503ff9` and it HIT (`runtime.py:28` import, `runtime.py:5798` `observe_parsed`). Bootable]~~]

> 🔴 **สถานะเปลี่ยนโดย chief รอบ `ogq686` / R302 (2026-09-02T11:2x+07:00):** บรรทัดที่ใบนี้รออยู่
> **เขียนแล้วและ push แล้ว** -- `pirate-force-server` PR **#563** (`runtime.py::_dispatch_with_lanes`
> เรียก `world_logout_button_notice.observe_parsed` ก่อนเกต scenario · เฟรมต่อท้ายท้ายสุดของ `return`)
> **รอ merge เท่านั้น ยังห้ามบูตจนกว่า RECHECK ข้างล่างจะได้ hit จริงบน `origin/main`**
> เกตอ่านจาก `production_allowed` ของโมดูลตรง ๆ ไม่ผ่าน `lane_hooks.module_production_allowed()`
> (มีเทสอ่านซอร์สจริงบังคับไว้) ⇒ ปัญหา D7 ที่ใบกลัวไว้ ปิดแล้ว
> 🔴 chief เพิ่มเกต **fail-closed เมื่อยังไม่ได้เลือกตัวละคร** ที่ใบนี้ไม่ได้ขอ (วัดแล้ว: ก่อนมีเกต
> เซสชันที่ไม่เคยล็อกอินยังได้เฟรมกลับ) ⇒ **ผู้เทสต้องล็อกอินเข้าฉากจริงก่อนกดปุ่มเสมอ** ไม่งั้นได้
> `lane_a_uia_notice_no_selected_no_reply` แล้วจะอ่านเป็น FAIL ผิด ๆ

> Opened by LANE-A round `od1xso` (2026-09-02 +07:00). LANE-A consumes the result itself.
> numbering: shared counter with `CLIENT_RE_QUEUE.md` (rule (2) at the top of this file).
> Highest `GT` in `GAME_TEST_QUEUE.md` = `GT-204`; highest `RE` in `CLIENT_RE_QUEUE.md` = `RE-202`.
> This entry is `205`.

- objective: single claim, decided by human eyes only -- with the character standing in a live map,
  the player opens the HOME menu and clicks "กลับหน้าเลือกตัวละคร" (back to character select), and the
  one line `BACK REFUSED` (exactly 12 printable ASCII characters) APPEARS ON SCREEN in the local
  chat/talk area, either while the logout dialog is still open or right after it closes.

- background (read once, then work from the steps): round `od1xso` built
  `src/pirateforce_foundation/world_logout_button_notice.py`. On `LogoutVital 0x1B40` subcode 3 (the
  owner's own captured 34-byte frame) it composes ONE `Channel_LocalTalkMessageVital` notice via
  `gm/say_wire.make_local_talk_notice_frame`, body exactly `BACK REFUSED`. Subcode 1 (the
  "ออกจากเกม" button, 119-byte frame) gets NOTHING from this lane, on purpose, so `GT-194`'s evidence
  cannot change underneath it. The wire/DB half is already proven headless (~~28 tests~~ **30 tests
  as of round `8z9h9n`** -- the entry was written saying 28 when the suite it names already had 29;
  corrected here by the lane that wrote it, pf-adversary D15), byte-equality with say_wire's
  composer. The tester's job in this entry is ONLY the screen half.
  The spelling `BACK REFUSED` is no longer a lane assumption: `COO-DECISION 20260902_0943`
  (`notes_to_chief/20260902_0943_COO-DECISION-uia-notice-text-back-refused-confirmed.md`) confirmed
  it, so a tester who reads a DIFFERENT spelling off the screen is reporting a defect, not a
  wording that was still being decided.

- PRECONDITION: ~~the module composes bytes but is NOT wired yet~~ **CLEARED by chief, R303
  (2026-09-02T13:0x+07:00).** PR #563 merged at 11:55 +07:00 and the RECHECK below was run against
  the merged `main`:
  `cd pirate-force-server && git fetch origin && git show origin/main:src/pirateforce_foundation/runtime.py | grep -n "world_logout_button_notice"`
  -> two hits on `origin/main` `96503ff9`: line 28 (import) and line 5798 (`observe_parsed`).
  Record `96503ff9` (or whatever `main` you actually boot) in the result.
  The tester may re-run the RECHECK; an empty result would mean the boot is on a stale clone, not
  that this entry regressed.
  BOOT ORDER for this round's tickets, per `COO-DECISION 20260902_1146` item 2:
  `GT-207` -> `GT-193` -> **`GT-205`** -> `GT-204` last.

- db: `state\pirateforce.sqlite3` -- COPY ONLY, never open the canonical file. Copy to
  `state\run_gt205_<yyyyMMdd_HHmmss>.sqlite3` and boot against the copy. Record sha256 of the copy
  before and after; record sha256 of the canonical file before and after and confirm it is unchanged;
  `PRAGMA integrity_check` = `ok` on the copy both times.

- server args: standard boot per `BRIDGE_BOOT_PROCEDURE.md` / `ATTENDED_SESSION_RUNBOOK.md`,
  `-SecondPasswordMode bypass`, NO scenario flag of any kind. Once wired this path is live on a
  default boot (`production_allowed = True`).
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt205_<stamp>.sqlite3`

- steps: (cheap: about 10 minutes on screen. Server first, client second, always.)
  1. RECHECK above must return a real hit. Then LOCK_GAME, boot stamp, sha of canonical, copy the DB.
  2. Boot server, then client. Log in. Confirm a FRESH server start (if a client was killed earlier,
     the server keeps the session and the next client hangs on "connecting" forever -- restart the
     server first).
  3. Frame the shot with RIGHT-CLICK-DRAG only (camera only; the character's facing does not move and
     nothing goes on the wire). Do NOT change the character's facing: no `Q`/`E`, no `W/A/S/D`.
     Do not type any characters -- with chat unfocused every keystroke is a hotkey.
  4. Screenshot S0 BASELINE, full resolution, showing the chat/talk area. Note the wall-clock time
     (+07:00) and the video timestamp.
  5. Open the HOME menu. Screenshot S1 (menu open).
  6. Click "กลับหน้าเลือกตัวละคร" ONE time. Write down the wall-clock time and the video `t` of that
     click before doing anything else.
  7. WATCH THE SCREEN CONTINUOUSLY FOR AT LEAST 30 SECONDS. Take S2 at about +2s, S3 at +10s,
     S4 at +30s, all full resolution, all showing the chat/talk area. Do not click anything, do not
     dismiss the dialog by hand during those 30 seconds unless the client itself closes it.
  8. Record, in the result: did the twelve characters `BACK REFUSED` appear -- yes/no; WHERE on screen
     (which panel/line); at what offset from the click; for how long it stayed; and whether the logout
     dialog was still open at that moment or had already closed.
  9. Optional second attempt, only if attempt 1 showed nothing: relog, repeat steps 5-8 once with the
     chat window/tab explicitly OPEN and its history tab visible before clicking the button. Label the
     screenshots S0b..S4b and record the two attempts separately -- do not merge them.
  10. NO-CRASH check with RIGHT-CLICK-DRAG (never `Q`/`E`). Screenshot S5. Exit with the window X.
  11. Shut the server down. Keep console `.out`/`.err`, `capture_v141\GAME_LIVE.txt`,
      `capture_v141\GAME_EVENTS_LIVE.txt` + sha256 of each. `PRAGMA integrity_check`. Re-check the
      canonical sha. Run teardown ALWAYS, even if the round ended because she simply stopped playing
      (the template refuses a boot stamp older than 420 minutes -- do not let the round age out).

- pass criteria: (TWO layers -- neither layer may ever be offered as proof of the other)
    wire/DB          : headless-readable from the console/capture alone. The subcode-3 request arrives
      and the console prints
      `LANE_A_UIA_NOTICE_COMPOSED button=BACK_TO_CHARSELECT subcode=3 vitals=1 trailing=0 text=BACK REFUSED pc=56 frame=66`
      (one line, exactly as printed -- the `pc=`/`frame=` lengths are the composed bytes, so the token
      cannot appear unless bytes exist). If she also clicks the exit button at any point, the matching
      line is ~~`LANE_A_UIA_STOOD_DOWN button=EXIT_GAME subcode=1 vitals=4 trailing=85`, which shows this
      lane composed NO BYTES for subcode 1 -- it still prints that one line, which is itself evidence
      `GT-194`'s reader will see; "nothing at all" would be the wrong expectation.~~ **CHANGED, LANE-A
      round `1d6rta` (2026-09-02T13:4x+07:00), per `COO-DECISION 20260902_1145`: the exit button is no
      longer a stand-down.** On a boot that carries this round's code (server PR of round `1d6rta`; the
      RECHECK below tells you which `main` you have), the exit click prints
      `LANE_A_UIA_NOTICE_COMPOSED button=EXIT_GAME subcode=1 vitals=4 trailing=85 text=EXIT REFUSED pc=56 frame=66`
      and a second twelve-character line may appear on screen. **That belongs to `GT-211`, not to this
      entry** -- this entry is graded on `BACK REFUSED` alone. On an older `main` the struck
      `LANE_A_UIA_STOOD_DOWN` line is still the correct one and is not a defect. Copy whichever lines
      appeared, verbatim, do not interpret.
      Three other tokens can appear instead, and each means something different:
      `LANE_A_UIA_WITHDRAWN` (the module is switched off), `LANE_A_UIA_NOTICE_FAILED` (the composer
      refused -- a bug to report, not a tester error), `LANE_A_LOGOUT_FRAME_UNCLASSIFIED verdict=<word>`
      (the frame reached this lane and was rejected; the word is the live classifier's own verdict).
      Copy whichever appeared. `integrity_check` = `ok`; canonical sha unchanged; no uncaught traceback.
      This layer CANNOT answer: whether anything was drawn on screen.
    client-observable: needs the human at the screen; never inferred from the console. Within the
      30-second window after the click, a human SEES the line `BACK REFUSED` -- twelve ASCII
      characters, that exact spelling -- in the local chat/talk area. Compare S0 against S2/S3/S4.
      Record for EVERY still (S0-S5, and S0b-S4b if attempt 2 was run) the colour of EVERY name label
      in frame, one line per label per image, the word `none` written out rather than left blank.
      Read colours from full-resolution stills only -- never from a contact sheet, a downscaled image,
      or video. Record the colour and nothing else: what decides a label's colour is unknown and is the
      whole subject of `RE-067`. Divergences from the original server's screenshots get one row each in
      `REAL_SERVER_DIVERGENCE.tsv`.
      This layer CANNOT answer: what bytes were composed, or which subcode arrived.

- prediction (THIS IS A PREDICTION, not a measurement; a wrong prediction is a finding):
    P1 console token present AND `BACK REFUSED` visible within ~2s => both layers pass.
    P2 console token present but nothing visible in 30s => the notice channel does not render while the
       logout dialog owns the input/render state. That is a real finding about the dialog, NOT proof the
       composer is wrong -- redirect to an RE about the dialog's render state, do not re-run blind.
    P3 no console token at all => the call site is not on the path she clicked; re-run RECHECK and
       report which `main` commit was booted. NO-RESULT for the screen half, not FAIL.

- nonclaims:
  1. Does NOT test whether the client returns to the character-select screen. That is `GT-184` and it
     remains unsolved (`GT-033` measured both known response policies leaving the client on the same
     map for 50-77s). Seeing `BACK REFUSED` says nothing about the transition.
  2. A negative is a real finding of equal worth: it is evidence about the logout dialog's input/render
     state, NOT proof that the notice composer is wrong. The render evidence for this channel
     (`GT-006`/`GT-009`) was measured with the dialog CLOSED, so this entry is the first time it is
     asked to draw with the dialog OPEN.
  3. Does NOT test the "ออกจากเกม" button (`GT-186`/`GT-194`/**`GT-211`**) and must not be run in a way
     that changes their evidence. If she clicks it anyway, log it as a separate observation with its own
     token line -- and on a `main` that carries round `1d6rta`, that observation IS `GT-211`'s evidence:
     record it there rather than grading this entry on it.
  4. Claims nothing about `ReturnSelectServerVital 0x709E` or `HYP-PF-040`.
  5. Does not claim the PR is merged; the RECHECK line, not this header, decides that.

- links: `NOW.md` item UI-A · `GT-184` · `GT-185` · `GT-194` · `RE-197` (closed this round) ·
  `notes_to_chief/consumed/20260901_1930_KA1A-CAPTURE-the-owner-clicked-both-UI-A-and-UI-B-buttons-herself-exact-bytes-plus-a-design-problem-for-HYP-PF-040.md`
  · `GT-193` (the `SPEED DENIED` notice -- same channel, same 12-character shape)

- result: (tester fills in: PASS/FAIL/BLOCKED/NO-RESULT · screenshots S0-S5 · verbatim console lines ·
  label colours one line each · timestamps +07:00 · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>`)

## GT-218 SPEED-SAFE-VALUE-400-DRY-RUN-CLIENT-SURVIVES-001  [**CLOSED** -- ❌ **FAIL · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00**
🔴 **คำ `CLOSED` เติมโดย LANE-GM (สายที่ถือผลใบนี้) รอบ `83wujr` 2026-09-06T07:2x+07:00 ตาม `FROM_CHIEF_R364` ข้อ 2 -- ไม่ใช่การเปลี่ยนผล** เหตุผลสองข้อ ตรวจได้เอง: (ก) ใบนี้ **ถูกบูตและเกรดจบไปแล้ว** (FAIL + `OBSERVER_CONFIRMED 2026-09-03T16:51+07:00` โดย chief รอบ `pk14rf`/R326) ⇒ ไม่มีอะไรให้บูตอีก การเติมบล็อก `ATTENDED:` จะพาใบที่ตัดสินแล้วขึ้นรถบัส capture ของเจ้าของโดยไม่มีคำถามค้าง (`FROM_CHIEF_R364` ข้อ 2 สั่งเองว่า "ใบที่ตอบไปแล้วให้ปิด แทนการเติมบล็อก") (ข) ที่ `pf_queue_status.py` รายงานใบนี้ว่า "พร้อมบูต" คือ **รูของ regex ไม่ใช่สถานะจริง**: `FAIL` ไม่อยู่ในรายการโทเคนของ `STATUS` (`tools_bridge/pf_queue_status.py:19`) ⇒ ตัวจับไปหยิบโทเคน "พร้อมบูต" ที่เคยอยู่ในวลีประวัติท้ายหัวใบแทน (วลีนั้นถูกเขียนใหม่ในรอบเดียวกันแล้ว) · คำ `CLOSED` ที่อยู่ซ้ายสุดแก้การนับนี้โดยไม่แตะเครื่องมือ (เครื่องมือไม่ใช่เขตของสายนี้) · 🔴 **ผลและงานที่ผลนี้ส่งต่อไม่ถูกปิดไปด้วย**: ผู้ต้องหาคือ**รูปเฟรม `UpdateAttrVital 0x309A`** (`COO-DECISION 20260903_1744`) ยังเป็นหนี้เปิดของ LANE-GM และเป็นคำถามเดียวกับที่ `RE-LV-LIVE-UPDATE-FRAME-001` (ขอไว้ใน `notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-slash-lv-*.md`) ถาม · 🔴 **chief/COO ไม่เห็นด้วย = พลิกกลับได้ด้วยการลบคำ `CLOSED` แล้วเขียนสถานะที่ต้องการลงไปแทน** ไม่มีอะไรถูกลบหรือย้าย · 🔴 **อย่าลบเฉย ๆ**: pf-adversary รอบนี้รันจริงแล้วพบว่าการลบคำเดียวโดยไม่ใส่อะไรแทน ทำให้เครื่องมือไปหยิบโทเคน "พร้อมบูต" จากวลีประวัติในบรรทัดถัดมาผ่านหน้าต่าง fallback `body+1` แล้วรายงานว่าอ่านมาจากเนื้อใบอย่างชอบธรรม (คอลัมน์ `body+1`) -- รูเดิมแต่พรางตัวดีกว่าเดิม ⇒ วลีนั้นถูกแก้เป็น "สถานะก่อนบูต (ประวัติ...)" ในรอบเดียวกันเพื่อปิดรูนั้นไม่ว่าใครจะลบ `CLOSED` หรือไม่ (แจ้งไว้ใน `notes_to_chief/20260906_07xx_LANE-GM-TO-CHIEF-*`) (chief รอบ `pk14rf`/R326 · หนี้ค้างจาก `COO-DECISION 20260903_1743` ข้อ 4) — `/speed 400` (ค่าเดียวกับที่ล็อกอินส่งทุกวัน) ทำไคลเอนต์ตายในเฟรมเดียว: HP `0/1` เงิน `0` ไดอะล็อกตาย · เฟรม `LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL` 74 ไบต์ออกจริงครั้งเดียว `SPEED DEFERRED` = 0 · แถว DB ไม่เสียหาย รีล็อกอินรอดเพราะประตูล็อกอิน (`#632`) ⇒ 🔴 **ค่าพ้นผิด ผู้ต้องหาคือรูปเฟรม `UpdateAttrVital 0x309A`** (`COO-DECISION 20260903_1744`) · ผลไปที่ **LANE-GM** ไม่ใช่ chief · สถานะก่อนบูต (ประวัติ ไม่ใช่สถานะวันนี้): ปลดเป็นบูตได้แล้ว R317 -- RECHECK ผ่านครบ 4/4 · chief วัดเองบน `origin/main` `01960240` 2026-09-03T09:5x+07:00 (ไม่ได้เชื่อจดหมาย: `LANE-GM 0822` และ `COO 0845` เป็นแหล่งที่สองที่สาม) · ล็อกทั้งสองของ `/speed` **ยังปิดค้างไว้ตามเดิม ไม่มีใครพลิก** ประตูเปิดในเซสชันผู้เทสด้วย `PF_SPEED_TRIAL=400` เท่านั้น · 🔴 ใบนี้พิสูจน์ "เส้นทางปลอดภัย" **ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์อ่านแถว** อ่านหัวข้อ "ข้อจำกัดที่ใบนี้พิสูจน์ไม่ได้" ก่อนรายงานผล]
