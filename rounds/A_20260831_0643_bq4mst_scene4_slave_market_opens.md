# LANE-A round `bq4mst`

2026-08-31T06:43+07:00 (`TZ=Asia/Bangkok date`).

## Step A / B (mandatory, start of round)

This sandbox has no `gh` and no GitHub API/MCP tool this round (confirmed by
the orchestrating session before this round started, which does hold API
access and checked on my behalf rather than leaving it unverified): the
newest `[LANE-A]` PR in each repo (`pirate-force-server#362` /
`pf_bridge#570`'s predecessor, round `pbpkv4`) is `merged=true` in both
repos, both working trees were clean and fast-forwarded to `origin/main`
before this round started, and no `[LANE-A]` PR was open going in. Nothing
to recover, no draft lock-holder needed.

Mailbox: `FROM_CHIEF_R256_TO_LANE-A_20260831_0556.md` was the one
unconsumed item addressed to this lane (`[ถึง: LANE-A | ... รอบ 0g16ru
(R256)]`, no `.CONSUMED.txt` stub next to it). It asks this lane to check
current status on five old `ASK-COO` letters (2026-08-28/29, all older than
the COO's 90-letter bulk-archive carve-out) and report back whether each
still blocks real work. Checked all five against the mailbox's own
`COO-DECISION` history rather than trusting the letter titles:

| ASK-COO letter | Answered by | Still blocking? |
|---|---|---|
| `20260828_2240_...cline-identity-clears-the-anchor-bar.md` | `20260828_2345` + `20260830_1351_COO-DECISION-cline-anchor-bar-cleared-gt131-pass.md` | No -- acted on already, `[ASSUMPTION]` tag struck in `world_port_royal_identity.py:107` |
| `20260829_0739_...does-rule-1-retro-move-scene-1-home.md` | `20260829_0848` + `20260830_1351_COO-DECISION-scene1-home-spawn-not-retroactive.md` | No |
| `20260829_2035_...harbour-needs-an-owner-verdict.md` | `20260829_2245_COO-DECISION-harbour-stays-empty-lisa-177-forbidden.md` + `20260830_1351_COO-DECISION-harbour-left-empty.md` | No |
| `20260829_2110_...who-owns-scene-2-when-the-seam-is-wired.md` | `20260829_2245_COO-DECISION-scene2-login-owns-composer-removed-from-crossing.md` + `20260830_1351_COO-DECISION-scene2-ownership-standing-rule.md` | No |
| `20260829_2240_...scene-14-door-has-one-blocker-left.md` | `20260829_2342_COO-DECISION-open-scene14-door-gt134-d3-stays-open.md` | No -- acted on, `scenarios/world_scene_registry_001.json` line 666 shows the door open, verified on disk this round |

All five: NOT blocking. Reported back to chief in a short letter this round
so the whole backlog batch can be archived together. Consumed stub written
for the chief letter.

## What this round found and built

Read `rounds/` and `notes_to_chief/` history before picking work, per the
task brief. `BUILD-001`/`BUILD-002` have been re-verified zero-diff five
rounds running; the M2 report family was declared fully wired by round
`1sejs4` and the one real gap found since (`pbpkv4`, the crossing-handoff
dispatch order) is already merged. So this round is not another
re-verification pass: `COO-DECISION 20260830_1441` (answering this lane's
own `12lyda` recommendation) named scene 4 (Slave Market Island, Bg0004) as
the first of ten shut marker doors to open, on the explicit condition
**"do not flip `login_entry_allowed` until the composer is truly ready"**.
Round `6p22bu` built the composer, round `2jdde8` wired it into
`CENSUS_SOURCES`/`ROSTER_COMPOSERS`/`lane_hooks`, and left the door shut on
purpose (`world_population_bg0004.py`'s own docstring: "WIRED, ROUND
`2jdde8`, DOOR STILL SHUT"). Nothing has touched it since. Composer is
109/116 shippable, tested, wired -- this round is the one that judges it
ready and flips the boolean, following the exact precedent scene 14 set
(`COO-DECISION 20260829_2342`), checked against THIS scene rather than
assumed:

* **D1 equivalent** (frozen `v141:4292` legacy branch composing bg0001
  actors into whatever scene an opt-in boot happens to be standing in):
  CLOSED GENERICALLY, not per-scene. `scene_admission_gate.
  strip_frozen_legacy_population` (wired into `runtime.py` the same round
  scene 14 opened) drops every `V134_P0_P30_P91_ISOLATED_*` action whenever
  the session's scene is not `world_population.SCENE_ID`, regardless of
  which scene travel put the session in. Verified this round, not assumed:
  `tests/test_world_faction_admission.py::TheOptInBootHazardTests` drives
  this by mechanism, not by scene id, and round `12lyda` already checked
  the gate's scope directly against source.
* **D2 equivalent** (a `character_positions` row labelled scene 1 while
  carrying another scene's XYZ): CLOSED GENERICALLY, same as scene 14 --
  `runtime.py`'s `login_scene_override_visit` branch withholds the durable
  write for the whole session regardless of destination scene id, and
  scene 4's row carries no `persist_position_allowed` override (defaults
  true, the same shape scene 14's own row carries).
* **D3 equivalent** (the faction-1 byte dropped outside scenes `(1, 2)`):
  DOES NOT APPLY to this scene at all -- a SAFER position than scene 14's,
  not an equal one. `world_population_bg0004.py`'s own docstring states no
  entry in this composer carries a faction bit ("whether any of this
  scene's monster-shaped placements should be hostile is a LANE-B
  decision, deliberately not made here"), so there is no hostile-pair
  mismatch for a player to walk into. `world_faction_admission`'s
  blast-radius derivation (`login_entry_allowed AND n_SAVE==1`) picks this
  scene up automatically the moment the key reads true (verified by test,
  see below) and will still have nothing to send.

## What was built

`scenarios/world_scene_registry_001.json`: scene 4's `login_entry_allowed`
flipped `false -> true`. `status` field struck (not deleted) and replaced
with the open-at-login note. `table_row_differences.
login_entry_allowed_because` added, mirroring scene 14's own field exactly
in shape, naming this round, the COO decision, and the three-defect check
above. `arrival_point_rule.why_the_ten_doors_are_shut`'s own closing
sentence appended with an UPDATE noting scene 4 is the first exception and
the other nine are unchanged.

`tests/test_lane_a_scene_census.py`: `SlaveMarketRegistrationTests`'
`test_the_real_registry_still_shuts_this_door` replaced with
`test_the_real_registry_now_composes_and_that_is_the_round` (mirrors
`TheAdmissionCheckIsTheGateTests`'s own VOLCANO test, inverted assertion,
old assertion kept as a struck comment rather than silently dropped). New
end-to-end production test added to `OnTheRealDispatcherTests`:
`test_with_the_real_registry_the_slave_market_census_ships_109` -- full
dispatcher boot, login, `START_GAME`, a `TargetPosVital` at scene 4's spawn,
asserts `WORLD_CENSUS_LANE_SCENE4_INITIAL_109`/`_REAPPLY_109` in the actions
list, the byte-count event, and both `WORLD_POP_HANDOFF scene=4` and
`WORLD_CENSUS_BG0004 assembled=109/116` printed -- same shape as scene 14's
own headline test, driven against the real registry file, no monkeypatch.

`tests/test_world_scene_registry_rule_1_scenes.py`: `RULE_1_SCENES_STILL_SHUT`
added (the original ten minus 4), the four admission-layer tests in
`TheDoorIsShutAndThisIsTheLoadBearingTest` switched to it, and a new test
(`test_the_one_scene_that_opened_is_no_longer_in_this_set`) added asserting
the opposite for scene 4 specifically, through the same four predicates
(registry field, `world_scene_travel.destination`, `login_entry_is_pinned`,
`stageable_scene_ids`, `resolve_entry`).

`tests/test_world_scene_marker.py`: `Scene14RegistryTests.
test_the_other_ten_marker_doors_did_not_open_with_it`'s loop narrowed from
ten scenes to nine (4 removed), with a new sibling test asserting scene 4's
admission the opposite way -- this file's own "blast radius of round
vvy6q7" claim would otherwise have gone quietly stale about a scene it does
not mention.

Five more literal admissible/stageable-set assertions found by running the
full suite and fixed the same way (append the new scene, keep the reasoning
comment, do not touch anything the literal was not there to prove):
`tests/test_world_faction_admission.py` (`admitted_scene_ids()` now
`(1, 2, 4, 14)`, console-line assertion), `tests/
test_gm_login_scene_admission.py` (`ADMISSIBLE_TODAY`, one console-token
assertion, one bent-registry assertion), `tests/
test_gm_login_scene_stage.py` (`stageable_scene_ids()` literal, GT-141's
own ticket), `tests/test_gm_login_scene_sanctioned_barred.py`
(`ADMISSIBLE_TODAY`), `tests/test_gm_login_scene_registry_snapshot.py`
(`ADMISSIBLE_ON_DISK_TODAY`, one bent-row assertion), `tests/
test_gm_login_scene_override_position_resync.py` (one console-token
assertion). Every one of these is the same class of test scene 14's own
opening round (`vvy6q7`) predicted it would need updating -- a silent
door-flip discovered by a red test, not by an attended round.

## Manual adversary pass (no subagent tool available in this environment,
## same limit every LANE-A round since `i95a1z` has reported)

1. Reverted `login_entry_allowed: true` back to `false` on scene 4's row in
   a scratch copy -- `SlaveMarketRegistrationTests::
   test_the_real_registry_now_composes_and_that_is_the_round` and
   `OnTheRealDispatcherTests::
   test_with_the_real_registry_the_slave_market_census_ships_109` both fail
   immediately (`assertTrue`/`assertIsNotNone` on a `None` compose result).
   Reverted.
2. Checked whether `world_faction_admission`'s derivation is actually keyed
   on `login_entry_allowed` and `n_SAVE` rather than a scene-id literal, by
   reading the module (not trusting its own docstring): confirmed at
   `src/pirateforce_foundation/world_faction_admission.py`'s predicate
   function, and independently by the new
   `test_the_admitted_set_is_exactly_the_two_proven_scenes_and_the_volcano`
   failing loudly (with the exact tuple diff) before the fix, which is the
   file doing what its own comment says a hardcoded answer cannot do.
3. Checked `lane_hooks/lane_a_scene_census.py`'s admission check
   (`scene_is_open_to_players`) is generic (reads `login_entry_allowed` off
   whatever `scene_id` it is given) rather than scene-14-hardcoded, by
   reading the function directly (`world_scene_travel.destination(scene_id,
   registry)` then `getattr(destination, "login_entry_allowed", False)`,
   no scene id anywhere in the body) -- confirms the flip alone is
   sufficient, no `runtime.py`/`app.py` change needed, matching what
   `2jdde8`'s own docstring already claimed and this round is the first to
   depend on being true.
4. Ran the FULL suite, not just the files touched, specifically to surface
   every literal admissible/stageable-set assertion the flip could break --
   this is how the six files in the "What was built" section beyond the
   four originally planned were found. Fixing only the files I expected to
   touch would have shipped a passing targeted run and a red full suite.

## Gate, measured

| check | result |
|---|---|
| `python3 -m pytest tests/test_lane_a_scene_census.py tests/test_world_scene_registry_rule_1_scenes.py tests/test_world_faction_admission.py tests/test_gm_login_scene_admission.py tests/test_scene_admission_gate.py tests/test_world_population_bg0004.py tests/test_world_bg0004_identity.py tests/test_world_scene_travel.py tests/test_gm_login_scene_stage.py tests/test_lane_scene_census_wiring.py tests/test_mob_scene_recompose.py` | all passed after fixes |
| `python3 -m pytest tests -q` (full suite) | **5664 passed, 327 skipped, 9759 subtests passed, 0 failed** (round `pbpkv4` baseline: 5661/327/9758 -- +3 subtests is this round's one new production test plus the two new admission tests, net of the literal-fix diffs which do not add test count) |
| `tools/verify_hypothesis_ledger.py` | `PASS entries=47` (unchanged) |
| `tools/verify_functional_coverage.py` | `PASS domains=8`, `OPEN DOMAINS: 8` (unchanged) |
| `tests/test_tree_is_cp874_safe.py` | 5 passed, 407 subtests (this round's new strings scanned clean) |
| manual cp874 scan of `scenarios/world_scene_registry_001.json` (every string value, via `str.encode("cp874")`) | clean |
| `git diff --stat` on `src/` | empty (registry JSON edit is under `scenarios/`, not `src/`; no Python source touched) |
| `git diff --stat` on `scenarios/` | 1 file, 9 lines |
| `git diff --stat` on `tests/` | 9 files, 225 insertions(+), 46 deletions(-) |
| `git diff --stat` on `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` | empty (none touched, none needed) |
| `python3 -c "import json; json.load(...)"` on the registry after every edit | valid JSON, checked after each of the three edits |

## What a player sees

A character whose own persisted row names scene 4, or a staged GM account
(`config/gm_login_scene.json`, `scene_id: 4`) or a GM `/warp 4`, now lands
on Slave Market Island and sees up to 109 of its 116 native placements
instead of being refused at login with `WORLD_SCENE_ENTRY_REFUSED
[scene_not_allowed_at_login]`. No ordinary player's own stored row can come
to name scene 4 today (no production path writes one), so this reaches a
staged account, the same reach scene 14 had the round its door opened.

## Not proven by this round

No human has watched a client log into scene 4 -- `GT-165` (opened this
round) is the attended ticket for that, `PENDING`. Whether `MARKER[4]`'s
authored point is standable ground is unmeasured (recorded in the registry
row's own `marker_geometry_measured_not_enforced` block, not claimed as
safe). `GT-144`'s remaining nine scenes are untouched by this round --
still `login_entry_allowed: false`, still no composer.

## CORE-REQUEST

None. The admission check, the faction-admission derivation, and the
scene-admission gate are all already generic (read the registry, not a
scene-id literal), so opening this one door needed no `runtime.py`/`app.py`
change -- confirmed by reading each, not assumed from their docstrings.

## Tickets opened for lane C

None. This round answered nothing new from the client; it built and opened
a door on evidence this lane and chief had already assembled and the COO
had already approved the sequence for (`COO-DECISION 20260830_1441`).

-- LANE-A (WORLD) round `bq4mst`
