# R253 (session `9fv1m8`) -- chief round

2026-08-31T~02:0x-02:2x+07:00

## Why this round mattered

`COO-DECISION 20260831_0146_gt128-gm042-owner-is-chief-not-coo-gate.md` put both
`FORCE_POS_VITAL_VERSION_CONFIRMED` unlock (blocking `GT-128`) and `CORE-REQUEST-GM-042`
squarely on chief, with a hard deadline: measurable progress before the 2026-08-31 09:00+07
executive round, or COO would issue `COO-ESCALATION-chief`. Both items had already been
investigated-and-deferred once before (R244 for FORCE_POS, R246/R248 for GM-042).

## Round-lock recovery check (step B of the runbook)

`pull_request_read(method="get")` confirmed both R252 PRs merged=true:
- `pf_bridge#547` -- merged=true
- `pirate-force-server#347` -- merged=true

Nothing lost from the previous round.

## 1. FORCE_POS_VITAL_VERSION_CONFIRMED unlock -- DONE, pushed, awaiting merge

Dispatched a subagent (isolated worktree) with the full R244 context (the 11-then-13 failing
tests, the two design options R244 left open, the explicit instruction to read each test's
docstring before touching any assertion rather than take a shortcut).

Result: `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED` flipped `None -> 0` (RE-129's
measured value, written as a literal per `RecordsAreInertTests`'s ban on reading any
`*_PROVEN_BY_RE129`-named constant). 13 tests across 6 files (drifted from R244's 11/5 --
the agent found 5 in `test_gm_chat_command_action.py` not 4, 4 in
`test_gm_command_audit_outcome.py` not 3) were repaired by adding
`close_the_version_gate()`/`close_the_warp_gate()` helper siblings of each file's existing
`open_the_*_gate()` helpers, used wherever a test's real subject is the withheld/gate-closed
path. Two lock-assertion tests that pinned the constant at `None` were renamed and now pin it
at `0`.

Chief-level review (not delegated) applied the patch to the working branch, then:
- Fixed one collateral out-of-scope failure the subagent correctly stopped at rather than
  silently widening scope: `tests/test_gm_standalone_map_is_not_chat_writable.py`'s
  `test_the_shipped_say_gate_is_still_shut` carried a secondary `assertIsNone` on the *warp*
  gate inside a test whose real subject is the unrelated *say* gate -- updated to
  `assertEqual(..., 0)` with a comment distinguishing the two gates.
- Ran `pf-adversary` (mandatory before any non-typo commit) on the full diff before
  committing. Findings: [CONFIRMED, MEDIUM] `gm/chat_command_action.py`'s own module
  docstring (the file that actually reads the constant at the one production call site,
  `chat_command_action.py:1346`) still said "the constant is still None on purpose" --
  outside the subagent's edit scope, inside the diff's own blast radius. Fixed using the
  project's existing strikethrough style (history preserved, not deleted) rather than
  deleting the old prose. Also flagged (not a defect in this diff, pre-existing and already
  COO-acknowledged as a separate ticket): `GM_WARP_POSITION_CONFIRMED` fires on "a write
  survived" not "the write matched the commanded target" -- noted for awareness, not acted
  on (out of this diff's scope, `runtime.py` untouched).
- Also updated two other stale "still None" prose spots the subagent's scope excluded:
  `gm/login_scene_stage.py`'s module docstring (same strikethrough style).
- Ran the fixed collateral test file, then the full suite twice (once before, once after the
  docstring fix): **5600 passed, 0 failed, 323 skipped, 9729 subtests passed** (~197-200s),
  green (cloud sanity) both times.
- `tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no drift.
- ASCII check: confirmed every line *added* by this round's diff is pure ASCII; two files
  (`teleport_wire.py`, `login_scene_stage.py`, `chat_command_action.py`) carry pre-existing
  non-ASCII Thai commentary from before this round -- verified via `git show HEAD:<file>`
  that those bytes predate this diff, not introduced by it.

`GAME_TEST_QUEUE.md`'s `GT-128` entry updated: struck the "still blocked, constant is None"
line, appended a status note that the unlock is pushed but **not yet merged** ("รอ merge
ก่อน" per house convention for tickets depending on an unmerged commit), and that GT-128's
own remaining blockers (the `unknown_character_mismatch` dead-code card-ordering question
from R243, the rearm-character bug) are still open -- this round only reopens the wire, it
does not close the ticket.

## 2. CORE-REQUEST-GM-042 -- decided: deferred, with a materially different reason than before

Dispatched a second parallel subagent (separate isolated worktree) to read
`mob_ledger_admission.py` in full (the file two prior rounds stopped short of reading), plus
`gm_npc_toggle_recompose.py`, `mob_scene_recompose.py`, and `runtime.py`'s
`_dispatch_mob_combat`.

Finding: the risk both prior rounds worried about (filtering the roster would corrupt
`mob_ledger_admission`'s `covered_count`/`roster_count`/`_unconsulted_rows` console-observable
counts) is real and confirmed, but conditional -- it only bites for an id actually present in
the roster. This round's subagent found something unconditional and structurally fatal to the
request as specified: **none of the 7 GM-switchable `mob_id`s (855/871/882/897/902/8180/8181)
are ever present in `recompose_frames`'s `roster` argument, on any currently-shipped
composer.** `gm.npc_switch_catalog.NPC_ID_TO_NAME`'s keys are raw client `MOBS.n_ID` values;
`roster`'s membership is keyed by `field_mobs.FieldMob.actor_identity`, a synthetic value
(`0x2000 + placement_index + 1`) with no relationship to `n_ID`. None of the 7 ids appear in
any field-mob source table. 5 of them appear only in `world_port_royal_identity.py`, a naming
crosswalk for a *different* pipeline (`world_population.build_world_population`'s fixed
census) that `roster` does not control membership for; even there, the
override/splice mechanism (`full_roster_override` -> `splice_identity_override`) only
overlays bytes onto identities the base collection already has and explicitly refuses to
emit an empty entry -- there is no way to *remove* a placement through it. The other 2 ids
(8180/8181, "Water Lantern") appear nowhere else in `src/` at all.

Implementing the requested filter as specified would therefore produce code that passes a
round-trip unit test (which only inspects the `roster` variable) while having zero effect on
the actual wire bytes -- a defect that looks fixed and isn't. Decided not to implement.
Two owner-level design questions escalated instead (what should "off" mean for the 5 ids
that DO exist in a fixed census today; do 8180/8181 exist server-side at all) -- any real fix
belongs in `world_population.py`/`world_population_bg0002.py`, out of this task's scope and
carrying their own pinned actor-count invariants a future round would need to read first.

Full technical writeup with file:line citations sent to LANE-GM/COO:
`notes_to_chief/20260831_0204_CHIEF-REPLY-CORE-REQUEST-GM-042-deferred-roster-filter-structurally-inert-not-a-time-problem.md`.
No files touched by this investigation (confirmed: pure read, full suite re-run twice on the
untouched tree by the subagent itself as a baseline sanity check -- 5540 passed both times,
0 failed).

This is not a formal parking of LANE-GM (the lane has other live work -- `gm/attr_wire.py`,
just approved by COO in `20260831_0146_COO-DECISION-approve-gm-attr-wire-*.md`). Only
`GM-042` itself is blocked pending an owner answer.

## 3. Mailbox: 12 letters addressed to chief/all consumed

`PANYA-ORDER` (shrink `GAME_TEST_QUEUE.md`), `KA1A-NOTE` (claim-pattern collision risk),
`KA1A-FINDING` (LANE-GM parked, superseded by COO-DECISION 0146's clarification that the
ball is with chief), `LANE-A-STATUS` (sea-destination wired, informational), `PANYA-QUESTION`
(why is /lv blocked -- answered by COO-DECISION approving gm/attr_wire.py), two `COO-DECISION`
letters (attr-wire approval, gt128/gm042 owner-is-chief -- both acted on this round), two
`CODEX_ATTR` checkpoints (no addressee, informational, external files not on git -- flagged
for bridge-side owner), `CODEX_ATTR_P0_CONFLICT` (same), `PANYA-ADDENDUM` (probe-request
intake process, no chief action needed), `LANE-B-DECISION` (loot-reorder invariant confirmed
standing, CORE-REQUEST-007 unchanged, new `mob_combat_membership.py` predicate noted as
backlog for a future round).

Two items explicitly deferred and recorded rather than actioned this round (lower priority
than the 09:00 deadline items): `PROCESS_GATES.md`'s claim-pattern still needs narrowing to
`_CLAIM-LANE-` per KA1A-NOTE; `GAME_TEST_QUEUE.md` shrink per PANYA-ORDER not started (its
own text says start only when `PR_STATE.txt` shows no LANE-A/B/GM PR open, and this round had
higher-priority build work).

## 4. Small infra fix

`pirate-force-server/.gitignore`: added `/.claude/worktrees/` -- the Agent tool's isolated
worktree feature (used twice this round for the two parallel subagents) creates this
directory as local tool machinery; without the ignore entry it shows as untracked and risks
being accidentally staged.

## Files touched

- `pirate-force-server`: `src/pirateforce_foundation/gm/teleport_wire.py`,
  `src/pirateforce_foundation/gm/chat_command_action.py`,
  `src/pirateforce_foundation/gm/login_scene_stage.py`, 7 test files (see commit for exact
  list), `.gitignore` (1 line). 10 files total for the FORCE_POS unlock commit + gitignore.
- `pf_bridge`: `PR_STATE.txt` (refresh), `GAME_TEST_QUEUE.md` (1 entry updated), 2 new
  `CHIEF-REPLY` letters, 12 `.CONSUMED.txt` stubs + 12 `consumed/` copies, `CHIEF_CONTINUATION.md`
  (round index line), this file.

## What was NOT proven

No client opened, no DB measured this round. `GT-128` is not closed -- only its constant-level
blocker is resolved (pending merge); the ticket's own remaining blockers and its
client-observable pass/fail still need an attended tester. `GM-042` has zero code change --
still parse+log+diagnostic exactly as before, pending an owner decision on what "off" should
mean.

## CHIEF_CONTINUATION.md size note

29,789B after this round's append -- 211B under the 30KB cap. Next round should archive
another block of old round-index lines before appending, or the cap will be exceeded.

## Companion PRs

`pf_bridge` (draft claim `9fv1m8`, updated across this round's 5 commits) /
`pirate-force-server` (draft claim `9fv1m8`, updated across this round's 2 commits: gitignore,
then the FORCE_POS unlock).
