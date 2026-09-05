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

