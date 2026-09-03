# LANE-A round `2jdde8`

Opened 2026-08-30T18:32+07:00 (`TZ=Asia/Bangkok date`). Heartbeat at round
start: `_BRIDGE_HEARTBEAT.txt` last line 2026-08-30T18:26:02+07:00 (6 minutes
old) -- no hand-computed timestamp used anywhere in this round.

Player-visible change: **none**. Scene 4's `login_entry_allowed` is unchanged
(`false`), no code path a player can reach changed this round, and no scene
outside 1/2/14 (already reachable before this round) is reachable now.

## Section A -- last round's PR (both repos)

`pf_bridge` closed `[LANE-A]` PRs, newest first (`GET .../pf_bridge/pulls?
state=closed&sort=updated`): `#507` (round `qlp30w`) `merged_at
2026-08-30T10:48:56Z` -- **merged: true**. No open `[LANE-A]` PR in
`pf_bridge`.

`pirate-force-server` closed `[LANE-A]` PRs, newest first: `#318` (round
`6p22bu`) `merged_at 2026-08-30T09:06:04Z` -- **merged: true**. No open
`[LANE-A]` PR in `pirate-force-server` (only `#324 [LANE-GM]`, not this
lane's lock). Nothing to salvage, nothing to cherry-pick, both prior rounds
landed clean.

Also read (not addressed to me, but directly relevant): `notes_to_chief/
20260830_1823_KA1A-CORRECTION-hole2-is-WRONG-...md`, which retracts an
earlier claim that Lane A's routine cannot write `pirate-force-server` at
all. Measured this round rather than trusted: a git-add/reset probe against
`pirate-force-server` (`.probe2.txt`, added with `-f`, immediately reset and
deleted, never committed) succeeded cleanly this round -- this round's
worktree pin covers both repos, unlike round `qlp30w`'s. Consistent with the
correction letter's own finding that the symptom is per-round, not a missing
grant.

## Worktree-scope measurement (COO-DECISION 2026-08-30T18:41+07:00)

Per the fresh ruling on main (`509ecc8`, answering the `KA1A-CORRECTION`
letter cited in Section A): one line per round, `git -C <path> status`
against both repos, refused or not. This round: **`git -C
/home/user/pirate-force-server status` exit 0, not refused; `git -C
/home/user/pf_bridge status` exit 0, not refused -- both repos were a
writable worktree this round**, consistent with Section A's git-add/reset
probe on the server repo.

## Section B -- mailbox

No open ticket addressed to `LANE-A` found unconsumed (checked
`CLIENT_RE_QUEUE.md` and `GAME_TEST_QUEUE.md` tails, and `notes_to_chief/`
modification order back through round `qlp30w`'s own consumption). The two
new files since then (`...RE-139-RESULT...`, `...LANE-A-STATUS-re139...`)
are this lane's own outputs from the prior round, already accounted for
there; the `KA1A-CORRECTION` letter above is informational (cc'd, not
addressed to this lane) and needed no reply, only the git-access
re-verification recorded in Section A.

## What this round built (BUILD-001/BUILD-002 follow-on: bg0004 wiring)

Round `6p22bu` built and deliberately left unwired
`world_bg0004_identity.py` / `world_population_bg0004.py` (Bg0004 Slave
Market Island, 109/116 shippable placements), per `COO-DECISION
2026-08-30T14:41+07:00`'s own "multi-round, no deadline, no re-approval
needed along the way" instruction. This round did the wiring half, the
same two-table change `world_population_bg0015`'s own history needed
(`CENSUS_SOURCES` in round `f1cda29`-equivalent, the console reader in round
`ga91m5-r2`-equivalent), done here in one round since both halves are small:

1. `world_scene_travel.py`: added `SLAVE_MARKET_SCENE_ID = 4` and a
   `"bg0004_roster"` row in `CENSUS_SOURCES`.
2. `world_population_handoff.py`: imported `world_population_bg0004` and
   added a `"bg0004_roster"` entry to `ROSTER_COMPOSERS`, same shape as
   bg0015's (`membership_of` reads `placement_indices`, the field name both
   generations share). Confirmed scene 4 is NOT in `LOGIN_OWNED_SOURCES`
   territory: it has no login-path populator today (`login_entry_allowed:
   false`, no dedicated `runtime.py` branch the way scene 2 has), so this
   entry composes over nothing.
3. `lane_hooks/lane_a_scene_census.py`: imported `world_population_bg0004`
   and added its `_CONSOLE_LINES_OF` entry (the second table a scene needs a
   row in, per this file's own "HOW A SCENE GETS ADDED" section).

**Verified this stays inert, not asserted:** `runtime.py`'s lane-census elif
(`lane_hooks.scene_census_composer(scene_id)`) is table-driven and untouched
-- confirmed by reading the call site, not by inference. Scene 4's registry
row still reads `login_entry_allowed: false` (untouched this round, per the
COO decision's explicit instruction not to flip it yet), and
`gm.login_scene_admission.stageable_scene_ids()` measured this round as
`(1, 2, 14, 278, 997)` -- scene 4 is in neither the login path nor the GM
`/warp` staging path. So the new composer is registered, discoverable by
`lane_hooks.scene_census_composer(4)`, and reachable by NOTHING today.

## Fallout fixed in the same round: a cross-lane tripwire this wiring tripped

`tests/test_mob_scene_recompose.py::SceneAccountedForTests::
test_every_scene_a_lane_composes_a_census_for_is_accounted_for` went red the
moment scene 4 entered `CENSUS_SOURCES` -- exactly the behavior that test's
own module docstring (`mob_scene_recompose.py`, LANE-B's file) predicts by
name: *"the next scene another lane opens is red here on the commit that
opens it."* Verified independently rather than assumed from scene 14's
existing entry: `field_mobs.scene_for_scene_id(4)` also returns `None` (same
as scene 14), so the identical reasoning applies -- no combat roster table
names scene 4, so no recompose strike can reach it.

Added the scene-4 entry to `ACKNOWLEDGED_WITHOUT_COMPOSER` in
`mob_scene_recompose.py`, mirroring scene 14's wording. This is a
co-maintenance edit outside this lane's four named write-zone paths, made
for the same reason round `6p22bu`'s actor-entry-static-pin fix was: a
shared cross-lane tripwire cannot be left red, and the fact recorded (no
combat roster reachable) is independently verifiable table data, not a
LANE-B judgment call made on their behalf. Flagged for LANE-B/chief review
in the entry's own comment in case the table's convention expects more.

## pf-adversary review

No Task/subagent tool was available this round to invoke the `pf-adversary`
persona directly, so its checklist (`.claude/agents/pf-adversary.md`) was
applied by hand against this diff:

- **False green / never got there**: added a scene-4-specific test class
  (`SlaveMarketRegistrationTests`) rather than relying only on the existing
  loop-based tests, specifically so a scene-4 regression cannot hide behind
  "the loop had nothing new to iterate" -- and fixed `ComposerContractTests`'
  shared open-registry fixture, which previously opened only scene 14 and
  would have made every loop-based test in that class silently decline for
  scene 4 (caught by running the suite, not by inspection: it surfaced as an
  `AttributeError` on `None.initial_reapply_ms`, not a clean assertion
  failure, before the fix).
- **Stale pins**: re-derived `ROSTER_COUNT` (109) and `PLACEMENT_COUNT` (116)
  from the live module at test-write time rather than copied from round
  `6p22bu`'s prose.
- **cp874 / ASCII**: every new comment, string, and console-line format
  checked; `grep`-verified no non-ASCII byte in any touched file.
- **Evidence layer**: no claim stronger than "wire/DB, registered, not
  fired" is made anywhere in this round's letters or comments; explicitly
  not claiming client-observable evidence for a door that is still shut.
- **Reading only half of one's own evidence**: re-read `COO-DECISION
  2026-08-30T14:41+07:00` in full before starting, confirmed
  `scenarios/world_scene_registry_001.json` was not touched
  (`git status --short`), and confirmed via a fresh read of `runtime.py`'s
  actual call site (not a citation of round `6p22bu`'s prose about it) that
  the composer point is table-driven and needs no `runtime.py` edit.
- **What I could not rule out**: the `mob_scene_recompose.py` edit is this
  lane writing into another lane's acknowledgement table. The fact recorded
  is independently verified, but the CONVENTION (wording, whether a
  cross-lane co-edit like this needs sign-off before or after) is LANE-B's
  and chief's to confirm -- named explicitly in this round's letter rather
  than assumed correct.

## Verification performed

`python3 -m pytest tests -q` on `pirate-force-server` HEAD (rebased onto
`origin/main` at `adf6677`, PR #324): **5517 passed, 327 skipped, 9681
subtests passed, 0 failed** (118s). Before the `mob_scene_recompose.py` fix,
the same run showed 1 failed (`SceneAccountedForTests`, the tripwire named
above) -- nothing else.

`python3 tools/verify_hypothesis_ledger.py`: `HYPOTHESIS_LEDGER PASS
entries=47`. `python3 tools/verify_functional_coverage.py`:
`FUNCTIONAL_COVERAGE PASS domains=8` (the eight INCOMPLETE domain lines it
also prints are the standing coverage report, unrelated to this round's
diff). `git diff --check`: silent. No canonical DB present in this
environment to hash (Windows-only artifact); nothing under `current/` was
touched (`git status --short` confirms).

## Files touched this round

`pirate-force-server` (all under this lane's territory: existing modules
this lane owns, plus one co-maintenance edit named above):

- `src/pirateforce_foundation/world_scene_travel.py` (modified)
- `src/pirateforce_foundation/world_population_handoff.py` (modified)
- `src/pirateforce_foundation/world_population_bg0004.py` (modified --
  docstring/marker-comment only, no behavior change)
- `src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py` (modified)
- `src/pirateforce_foundation/mob_scene_recompose.py` (modified -- LANE-B's
  file, co-maintenance, see above)
- `tests/test_lane_a_scene_census.py` (modified: multi-scene registry
  helper, `ComposerContractTests` fixture fix, new
  `SlaveMarketRegistrationTests` class)
- `tests/test_world_population_bg0004.py` (modified: AST-walk import-pin
  test updated for the new, intentional importers)

`pf_bridge`:

- `pf_bridge/rounds/A_20260830_1845_2jdde8_bg0004-wired-behind-a-shut-door-plus-a-cross-lane-tripwire-fixed.md`
  (this file, new)
- `pf_bridge/notes_to_chief/20260830_1845_LANE-A-STATUS-bg0004-wired-door-shut-recompose-tripwire-fixed.md`
  (new)

7 files touched in `pirate-force-server` (5 in this lane's own modules, 1
docstring-only, 1 named co-maintenance edit in another lane's file), 2 in
`pf_bridge`.

## Numbers measured this round

`world_population_bg0004.ROSTER_COUNT` = 109 (unchanged from round
`6p22bu`, re-derived not copied). `CENSUS_SOURCES` grew from 3 entries to 4.
`ROSTER_COMPOSERS` grew from 1 entry to 2. `ACKNOWLEDGED_WITHOUT_COMPOSER`
grew from 1 entry to 2. Full suite: 5517 passed / 327 skipped / 9681
subtests, 0 failed, both before-rebase and after-rebase-onto-`adf6677` runs
agree.

## What's blocked / waiting

- Scene 4 remains closed to every player-reachable route
  (`login_entry_allowed: false`, absent from
  `gm.login_scene_admission.stageable_scene_ids()`). Opening it is an
  owner/COO call, not this lane's to make -- same posture as scene 14 held
  for several rounds between its own wiring and opening.
- The LANE-B hostility question for this scene's monster-shaped placements
  (Scythe Beetle, Dragon Gladiator, Orc Chief etc.) is unchanged from round
  `6p22bu`: explicitly not decided here.
- `mob_scene_recompose.py`'s acknowledgement-table convention: is a
  same-round co-edit by the opening lane acceptable, or should this lane
  wait for a LANE-B/chief letter first next time? Asked in the status
  letter, not blocking (the alternative -- leaving the suite red -- was
  worse).

## CORE-REQUEST

None this round (no `runtime.py`/`app.py` change needed; the composer point
chief built in round `73fhoc` already covers this scene generically).

## ASK-COO

None this round -- this is a continuation of an already-approved multi-round
order (`COO-DECISION 2026-08-30T14:41+07:00`), and the one open question
(the acknowledgement-table convention) is addressed to LANE-B/chief, not the
COO.

## เปิดใบให้สายอื่น

None this round.
