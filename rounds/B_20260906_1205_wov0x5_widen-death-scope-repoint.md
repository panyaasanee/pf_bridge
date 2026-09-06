# LANE-B round wov0x5 -- 2026-09-06T12:05+07:00 start

## round moves which NOW/M item
NOW "LANE-DB: PANYA-ORDER..." block item "B1122 ratified repoint four
strings to 1150" (the line naming this letter directly) and the M4 combat
scope for scenes 6/7/9/11. No new player-visible unlock this round: P-2
(monster name colour) still forbids an attended monster-hit GT for these
scenes, so this is a citation-correctness fix behind that gate, not a new
kill.

## mailbox consumed this round
Lock check: no other `[LANE-B]` claim open (checked before and again right
after opening `pf_bridge#1477`). Opened claim, read mailbox, found seven
open LANE-B letters (none pre-dating this round by more than ~8h):

1. `20260906_1150_COO-DECISION-b1122-...LANE-B.md` -- THE round's main task.
   Ratifies the four widen-death-scope-bg0006/7/9/11 entries PR #907 (round
   4tnhzw, this lane's own prior round) shipped citing
   `notes_to_chief/20260906_0748_...`, a letter whose own item 1 only asked
   for a ruling, never granted one. This lane's own
   `20260906_1122_LANE-B-ASK-COO-pr907-...md` (written by round p4ts3e)
   flagged that gap. 1150 does not reverse the four scenes -- it ratifies
   them and orders the citation repointed to itself. Done, see below.
2. `20260906_1148_COO-DECISION-b1050-...LANE-B.md` -- no-penalty
   acknowledgement for the 4tnhzw/p4ts3e duplicate-work incident; nothing
   for this lane to build.
3. `20260906_0350_CHIEF-REPLY-corereq-2242-class-id-wired-gt271-reserved.md`
   + `20260906_0419_..._ADDENDUM-provenance-counter-wired-per-coo-0346.md`
   -- both already fully implemented by chief on main (verified: runtime.py
   :1414/5187-5188, action_ack.py's `make_production_hit_pose_echo` accepts
   and mutates `provenance_reported` in place). Nothing left in LANE-B's
   own zone. Late stubs filed.
4. `20260906_0434_CHIEF-SELFCORRECTION-gt271-was-a-premature-number.md` --
   GT-271 is NOT reserved; noted for whoever writes the pose-trial GT
   ticket later (not this round -- out of scope).
5. `20260906_0540_...pr888-closed-never-merged.md` +
   `20260906_0732_...pr895-closed-never-merged.md` -- both are the same
   Bg0008 (Silver Harbour) registration work, gate-failed twice
   (branches `claude/nice-meitner-4m2kx7`, `claude/gifted-clarke-oabhhe`)
   before landing successfully via commit `606f914` (confirmed ancestor of
   origin/main today, `field_mob_tables_bg0008.py` exists, `mob_death.py`
   carries its real ruling). No recovery needed; late stubs filed.

## what was done (real work, not a probe)

### widen-death-scope-bg0006/7/9/11: citation repoint per COO-DECISION 1150
Changed, in `pirate-force-server`:
- `src/pirateforce_foundation/mob_death.py`: the 8 dict-key timestamps
  across `WIDENING_RULINGS` and `WIDENING_RULING_SCENES` (4 scenes x 2
  dicts) from `2026-09-06T07:48+07:00` to `2026-09-06T11:50+07:00`, plus
  rewrote the explanatory comment block to cite the real ratifying letter
  (1150) instead of the request letter (0748) and to narrate why (0748
  only asked; 1150 grants).
- `src/pirateforce_foundation/field_mobs.py:597`'s comment: same retiming
  and re-citation, matching the letter's explicit instruction.
- `tests/test_mob_death_wired_widening.py`: the pinned
  `ruling_registered_at()` expected-value table updated
  (`202609060748` -> `202609061150` for all four).
- Also touched, NOT named by the letter but mechanically required:
  `tests/test_field_mob_tables_bg0006.py`, `_bg0007.py`, `_bg0009.py`,
  `_bg0011.py`. Each defines a module-level `RULING_NAME` string that is
  `assertIn`'d against `mob_death.WIDENING_RULINGS`/
  `WIDENING_RULING_SCENES` and used in further dict lookups -- left at the
  old timestamp, these four test files would have gone red the moment
  `mob_death.py`'s keys moved. Updated their `RULING_NAME` constants and
  docstring citations the same way. This is a 7-file PR, one over the
  house guideline of ~6; noted here because it is one mechanically-coupled
  string repoint, not scope creep, and splitting it would have left main
  red between the two PRs.
- **Not changed, verified**: the covered template-id `frozenset` values
  themselves (bg0006 `{222,226}`, bg0007 `{388,390,393,395,397,526,536}`,
  bg0009 `{314,317,320,546,549}`, bg0011 `{669,674,693,696,697}`) are
  byte-for-byte identical to before -- confirmed by diff review (no
  numeric frozenset literal appears in the diff) and by pf-adversary
  independently (see below).

### own defect found and fixed the same round
While drafting the new `mob_death.py` comment I pasted a Thai quotation
("only asked", quoted from the ratifying letter) directly into a Python
comment instead of glossing it in English. This violates the ASCII-only
house rule and was caught by `tests/test_mob_stat_fabrication_guard.py`'s
`.read_text(encoding="ascii")` check on every `LANE_B_MODULES` file.
Fixed in a second commit on the same branch (English paraphrase, no
meaning change). Full suite re-run confirmed green after the fix.

## pf-adversary (ordered start-of-round; result returned before push --
not PENDING)
Told to try to break the claim. **CONFIRMED** one real defect: exactly the
ASCII violation above (independently found and reported with identical
file:line evidence, byte offset, and root cause) -- already fixed before
this round pushed. It ran a `git stash` A/B in an isolated worktree to
prove the failure was this round's regression and not pre-existing, and
ran the truly unscoped `pytest tests/ -q` (not just the narrow selection
this lane ran first), which is exactly what caught it.
Everything else checked clean: no frozenset literal touched anywhere in
the diff; `ruling_registered_at()`'s leftmost/earliest-timestamp parsing
is unaffected (every touched key still carries exactly one ISO timestamp,
same shape as before); every surviving "07:48" mention in the touched
files is a deliberate historical citation explaining the correction, not
a stale live comparison.
One informational-only finding, out of scope for this PR and not acted on:
`src/pirateforce_foundation/mob_scene_recompose.py` (LANE-A's write zone,
per its own "ADDED ROUND ... LANE-A" comment) still narrates the old 0748
timestamp for these four scenes in prose comments with no live string
comparison -- harmless today, a cleanup LANE-A or chief may want, not
this lane's zone to fix and not named by letter 1150's three-artifact
scope.
It also raised a process question worth relaying to COO rather than
answering myself: letter 1150's own enforcement (item 3) is a *manual*
grep COO runs every executive round to match ruling-name keys on main
against `notes_to_chief` filenames -- given this very round shows an
*automated* test catching a real defect a hand-picked narrow test
selection missed, should the ruling-citation/timestamp invariant itself
be pinned by a repo-wide automated test instead of a recurring manual
step? Not filing a separate ASK-COO for this (would cost a GT/RE-runner
slot for a process suggestion) -- flagging it here for COO to pick up or
not.

## not touched (out of scope this round)
- `GT-274` CS pairing check: still cannot start, `GT-274` is not in
  `GAME_TEST_QUEUE.md` (grepped) -- CS has not placed the ticket body yet
  per NOW `0645`.
- `Bg0010` registration: still not registered. The `0903`/`1046` STATIC
  ticket to chief has not been numbered/answered yet (grepped
  `notes_to_chief/` for a chief/COO reply naming it -- none found). Mining
  it readable is not authorisation to register it.
- `apply_hp_damage` caller: still paused per NOW, waiting on Door B.
- No `world_*` files touched, no LANE-A zone touched (only read
  `mob_scene_recompose.py` to evaluate the adversary's informational
  finding, did not write it).

## verification
- `python3 -m pytest tests/test_mob_death_wired_widening.py
  tests/test_field_mob_tables_bg000{6,7,9,11}.py -q`: 49 passed, 1503
  subtests passed (before the ASCII fix was even needed to show here --
  this narrow selection never exercised the guard that caught the bug).
- Full suite on the branch that actually pushed (post ASCII-fix, merged
  with origin/main -- no new commits from origin/main during this round):
  `python3 -m pytest tests/ -q` -> **12159 passed, 369 skipped, 25068
  subtests passed, 0 failed** (431.51s).
- `python3 tools_bridge/pf_gate_preflight.py --repo
  ../pirate-force-server`: PREFLIGHT PASS (cp874, no new skips, main is in
  branch, precondition census agrees, both branches mergeable, bridgesize
  debt is pre-existing/old not grown by this branch, no manual scoreboard
  row touched).
- `python3 tools_bridge/pf_gate_preflight.py --pr-body <file> --pr-stage
  final`: `[prbody] PASS - exactly one marker line ... nothing else
  mentions the token`.
- After opening `pirate-force-server#916`, GET'd the PR back and confirmed
  the body server-side actually carries `PF-AUTOMERGE: v4` as its own bare
  line (not just the file that was validated).

TWO_SESSIONS_SAME_SCENE: not applicable. This round only repoints citation
strings in a comment/dict-key and a test pin; no runtime behavior, no wire
frame, no shared-world state read or written.

## PR/status
- `pf_bridge` claim `pf_bridge#1477` (`claude/practical-knuth-wov0x5`)
- `pirate-force-server#916` (`claude/gifted-clarke-wov0x5`) -- **opened,
  not draft, `PF-AUTOMERGE: v4` present and GET-verified**. Two commits:
  the repoint, then the ASCII fix. Full suite green on the final commit.
  Rest on gate. **Do not write "on main" until a later round confirms with
  `git merge-base --is-ancestor`.**

## next round
1. Confirm `pirate-force-server#916` with
   `git merge-base --is-ancestor <sha> origin/main` before treating it as
   landed.
2. `GT-274` -- start the CS pairing check once CS places the ticket body
   (still not in `GAME_TEST_QUEUE.md` as of this round).
3. `Bg0010` -- register only after the `0903`/`1046` STATIC ticket gets a
   number and an answer from chief/COO; still not authorised.
4. Backup work if the above are still blocked: one flag promotion from
   `docs/PROMOTION_BACKLOG.md` in this lane's own zone (item 4,
   `ground_loot_hypothesis.py`, per NOW's promotion pipe list).

SCOREBOARD: COMING | Deep Sea Temple (scene 10) mining aside, the four
scenes this lane already widened last round (Silver Harbour's neighbours:
scenes 6, 7, 9, 11 -- 19 new hostile templates over 26 placements) now
carry a citation that actually points at the letter that approved them,
closing a paperwork gap this lane's own prior-round ASK-COO caught before
it shipped further; no new kill reaches a player's screen this round (P-2
still gates the attended monster-hit GT for these scenes) | `pirate-force-server#916` · `notes_to_chief/20260906_1150` (ratifying letter) · `notes_to_chief/20260906_1122` (this lane's own flag) · full suite 12159 passed/0 failed on the pushed commit
