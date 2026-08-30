# LANE-A round `oprday`

Opened 2026-08-30T20:38+07:00, closed 2026-08-30T21:2x+07:00 (approx).

Player-visible change: none yet (client-observable). Wire/DB layer only:
`world_scene_travel.load_scene_registry()` now returns a 17th row (scene
126) that it refused to return before this round, and GM's own pre-built
`gm/login_scene_admission.single_use_stageable_scene_ids()` picks it up
automatically the moment this row lands (see section 4). No login path, no
`/warp`, and no console line any player has typed yet resolves anything
differently until GM lane's own `/warp` writer is exercised against it.

## 0. Why this round exists

Two prior rounds this same day (`n8fq3w` 11:36, `qp7brn` 12:26) reported
attended-only work remaining: `GT-134` (scene 14 NPCs) and `RE-155` (NPC
name color) both still `[NEEDS-ATTENDED-CAPTURE]`/`READY` with no
`*-RESULT` letter in the mailbox (checked again this round, still true).
Per the standing rule against two empty rounds in a row, and per the
addendum's rule F, this round picked up the next M2 step that does not
depend on actor-identity resolution.

M2 itself (Columbus -> scene 17 -> return leg) turned out to be built
end-to-end already (`columbus_quest_dispatch.py`, `world_m2_sea_
destination.py`, `world_m2_return_leg.py`, all wired in `runtime.py`
through prior CORE-REQUESTs). What remained open and genuinely
actionable without identity work was a single, previously-assigned,
never-executed task: **CHIEF-DECISION R229**
(`pf_bridge/notes_to_chief/20260829_1603_CHIEF-DECISION-var2-test-path-
scene126-registry-row-plus-gm-warp.md`) asked this lane for a scene 126
registry row (item 1) so chief could open a GT ticket testing whether
`QUESTDATA_TH__QUEST` row 3021's `n_VARI_2 = 17` is a scene id (today's
reading) or a MARKER id (`MARKER[17].n_SCENE = 126`, the reading
`COO-DECISION 20260830_1351` escalated to the owner). Nine rounds and one
calendar day passed with the row never landing - confirmed by grep, not
memory: `python3 -c "import json; print(126 in [d['n_id'] for d in
json.load(open('scenarios/world_scene_registry_001.json'))
['destinations']])"` printed `False` at the start of this round.

## 1. What this round did

Added scene 126 (`Bg3001`, "Atlantis" - s_SCENE_NAME hex
`e4ba9ee789b9e898ade68f90e696af`) to
`scenarios/world_scene_registry_001.json`, following the exact three-item
spec CHIEF-DECISION R229 gave:

* `spawn = (3050.0, 232.0, 90.0)` - `CONSTDATA_TH__MARKER.tsv` row
  `n_ID=17`'s own real x/y/z, re-read from the file this round rather than
  copied from a letter (`grep -P "^17\t" gamedata/tables/
  CONSTDATA_TH__MARKER.tsv`, confirmed via
  `world_scene_travel.destination(17,...).spawn` matching in-tree).
* `coordinate_provenance` citing `MARKER[17]`, with the honest shape: this
  scene's OWN `SCENE_NAME.n_MARKER` is 0 (verified:
  `grep -P "^126\t" CONSTDATA_TH__SCENE_NAME.tsv` -> field 15 is `0`), so
  `COO-DECISION 20260829_0542`'s rule 1 does not reach this scene the way
  it reaches the ten rule-1 scenes from round `ga91m5` - `from_marker` is
  `false`, `marker_n_id` is `null`, `deviates_from_rule_1` is `false`
  (there is nothing to deviate FROM, rule 1 was never reached), and
  `evidence_tier` is `decreed_provisional` (a named chief decision behind a
  real, table-sourced number, not the rule-1 self-reference tier and not
  an invented one either).
* `login_entry_allowed: false` - the door stays shut; nothing sanctioned
  reaches scene 126 through a stored login row.
* `ground: null` - not measured this round, on purpose (chief's spec named
  three fields, not four; adding a ground block would also turn on the
  loader's bound-check against real placement extents this round has not
  computed, for a contested point - the wrong moment to discover those two
  numbers disagree is at every boot).

`native_placement_count=38`, `native_definition_count=56`,
`native_sha256` all re-derived from `gamedata/PF_GAMEDATA_SCENE_INDEX.tsv`'s
own `Bg3001` row (`571c147f...`), not copied from any docstring.

Draft-validated against the real loader before writing the file
(`world_scene_travel.load_scene_registry(draft_path)` on a scratch copy)
to confirm it parses cleanly before touching the production file.

## 2. Second Lane-A module updated for the same reason

`world_scene_folder._FOLDER_BY_SCENE_ID` is a second, independently
generated table keyed by the same 17 scene ids the registry addresses
(`tests/test_world_scene_folder.py`'s own load-bearing test:
"a destination added to the registry with no address here goes red").
Added `(126, "Bg3001")`, re-derived from the committed crosswalk copy
(`src/pirateforce_foundation/world_data/world_scene_folder_crosswalk.json`
`scene_folder_index`/`scene_model_index`, both agree: folder == model ==
`Bg3001`, no case mismatch, no collision with another scene id's folder).
Updated the module's own "sixteen"->"seventeen" prose in four places to
match, rather than let the docstring drift from the data the way round
`8ubiku` was corrected for.

## 3. `columbus_quest_dispatch.py` - one stale claim struck

While reading M2's wiring to confirm nothing here needed touching, found
the module's own docstring still claiming (present tense) that
`runtime.py`'s call site "does not pass" `legacy`/`held_indices` and that
wiring them was "this round's CORE-REQUEST to chief" - false at HEAD:
`runtime.py:4985-4986` and `:5012` already pass `legacy`, `held_indices`
AND `departed_from`. Struck (not deleted) with a note naming the round
that landed it (`R229/qb70g2`), matching this file's own house style for
corrections. No behavior change - documentation only.

## 4. What landing the registry row actually triggered - read before merging

GM lane pre-built a "sanctioned barred scene" mechanism specifically for
this row, months (in project time) before it existed:
`gm/login_scene_admission.py`'s `SANCTIONED_BARRED_SCENES = {126:
"CHIEF-DECISION 20260829_1603 item 2"}`, `sanctioned_barred_blocker`,
`single_use_entry_is_admissible`, and `single_use_stageable_scene_ids`.
`GT-141`'s own ticket text (round `znb56z`, 2026-08-30T00:3x) predicted
this exact moment in writing: *"the day lane A lands row 126, `stageable=`
in the token will become `(1, 2, 126, 278, 997)` itself, with no PR from
this lane in between - if you see 126 in the list, do not treat it as
broken; treat it as lane A having merged, and 126 now genuinely works with
`/warp`."* That is exactly what happened. `/warp 126` and the `gm_login_
scene` single-use map's stageable set now admit scene 126 - not because
this round touched any GM file, but because GM's own pre-built machinery
was waiting on this exact row.

**Twenty of GM lane's own tests go red the moment this row lands, and all
twenty are pre-anticipated by GM lane's own test names and comments, not a
surprise this round is hiding:**

* `tests/test_gm_login_scene_sanctioned_admission.py` (11 tests) -
  literally named `TheSanctionAdmitsNothingOnMainTodayTests::
  test_lane_a_has_not_landed_the_row_yet` and
  `test_so_the_widening_admits_nothing_today`, plus 9 more in the same
  file that assert the pre-row state.
* `tests/test_gm_login_scene_sanctioned_barred.py` (3 tests) - one
  assertion's own failure message reads: *"if this goes green the disk
  grew the row -- re-read the bound above; the way out and the stage now
  agree and this test is testing nothing."*
* `tests/test_gm_login_scene_sanctioned_bypass_wiring.py` (1 test)
* `tests/test_gm_chat_no_bytes_line.py` (1 test)
* `tests/test_gm_login_scene_admission.py::TheLoaderTests::
  test_the_gm_gated_map_refuses_a_barred_scene` (1 test)
* `tests/test_gm_login_scene_override_position_resync.py::
  test_an_inadmissible_destination_never_reaches_the_login_at_all`
  (1 test)
* `tests/test_gm_login_scene_registry_snapshot.py` (2 tests) - NOT
  explicitly pre-named for this event the way the others are; these two
  compare a message computed via the single-use-aware admission path
  against an expectation computed via the plain (non-single-use)
  `login_scene_admission.stageable_scene_ids()`. The likely one-line fix
  (not made here - `gm/` test files are outside this lane's write zone):
  the two assertions in `TheConfigRefusalNamesTheCallersReadingTests::
  test_the_refusal_and_its_way_out_both_come_from_the_snapshot` and
  `TheChatCommandCarriesItAllTheWayDownTests::
  test_the_console_way_out_names_the_snapshot_set` should compare against
  `login_scene_admission.single_use_stageable_scene_ids(...)`, matching
  the `single_use=True` config (`gm_login_scene`) both tests actually
  exercise, the same way the other eighteen tests in this list already
  expect the sanctioned map to answer.

This is reported here in full rather than fixed, because `gm/` is GM
lane's write zone and these are GM lane's own tests asserting GM lane's
own module's behavior - the project's own rule this round is following,
not a shortcut. It also means **CHIEF-DECISION R229's item 2 ("GM lane
adds 126 to `/warp`'s accepted set") is already done** - GM lane built it
ahead of time, waiting on this row - so both halves of the var2 test path
are on this working tree now, and the GT ticket chief said would open
"once both are on main" can be opened next round.

### 4a. pf-adversary review this round - two findings, both addressed

Ran a full pf-adversary pass on this diff before commit (isolated worktree,
independent re-verification against `gamedata/tables/*.tsv`, read the real
GM enforcement code and test files rather than trusting this round's own
prose). Two findings, both real:

**Finding 1 (fixed in this commit):** the registry row's own
`why_the_door_is_shut` field claimed "it does not make it REACHABLE by
anyone" - false the moment this row lands, per section 4 above (an
authorized GM account can `/warp 126` today via the pre-wired sanctioned
bypass). This letter and this round record both already said so in their
own words; the JSON field text did not, and a future reader trusting the
registry file as evidence-of-record (this project's own G1 source-ladder
rule) would be misled. Corrected in `scenarios/world_scene_registry_
001.json` this round: the field now states the ordinary/standalone login
path stays shut, but the GM sanctioned single-use bypass is armed and
admits scene 126 via `/warp` for already-authorized GM accounts.

**Finding 2 (not this lane's to fix - flagged here so GM lane does not
silently defang a safety test):** at least two of the twenty red GM tests
are not clean "update the expected value" flips the way the other
eighteen are - they are **broken test fixtures**, and fixing them by
updating an assertion instead of the fixture will silently retire the
safety property they exist to check.

`SceneRegistry.__getitem__` (`world_scene_travel.py:309-313`) is a linear
scan returning the *first* matching `n_id`. Both
`tests/test_gm_login_scene_sanctioned_admission.py`'s `registry_with_
sanctioned_row()` helper and `tests/test_gm_login_scene_sanctioned_bypass_
wiring.py::test_a_latched_bypass_never_leaks_onto_the_characters_own_row`
build their synthetic scene-126 stand-in by **appending** a row after the
real registry's destinations (`registry.destinations + (row,)`). Now that
the real on-disk registry already contains a genuine `n_id=126` row (with
a real spawn) *before* that appended synthetic row in the tuple,
`registry[126]` silently resolves to the real row, not the synthetic
"spawnless" stand-in these fixtures were built to construct - confirmed by
tracing the actual failing assertion for
`test_a_latched_bypass_never_leaks_onto_the_characters_own_row`: the
event `gm_login_scene_override_applied_126` fires (which the test asserts
should NOT happen in this scenario), consistent with the fixture
resolving to the real spawned row instead of its intended spawnless one.

That test's own docstring states what it protects against: "dropping
[this conjunct] left the whole 5000-test suite green while a driven
exploit landed a login in barred scene 17." **Whoever picks up the 20 red
GM tests must filter out any existing same-`n_id` row before appending the
synthetic stand-in in these two fixtures, not just update the expected
value** - a plain value-update fix would leave the suite green while this
property goes unchecked. Not fixed here: `gm/` and its own test files are
outside Lane A's write zone. Flagging in this round record and the
companion status letter so it reaches GM lane before anyone "fixes" the
cluster in one pass.

## 5. Tests run

Targeted (my own touched modules + everything measured to interact with
them), before the full run:

```
python3 -m pytest tests/test_world_scene_travel.py \
  tests/test_world_scene_registry_rule_1_scenes.py \
  tests/test_world_m2_sea_destination.py \
  tests/test_columbus_quest_dispatch.py \
  tests/test_columbus_quest_dispatch_wiring.py \
  tests/test_gm_login_scene_registry_snapshot.py \
  tests/test_gm_login_scene_registry_wiring_in_runtime.py -q
```
2 failures (the registry_snapshot pair, section 4) - everything else,
including both files this round edited directly, green.

```
python3 -m pytest tests/test_world_scene_folder.py -q
```
1 failure found and fixed in the same round (a second hardcoded
`(2, 3, 7, 8, 9, 10, 11, 14, 17, 130, 278, 997)` literal in
`TheReaderIsNotModelIdTest`) - green after the fix (31 passed, 829
subtests passed).

Full suite (`python3 -m pytest tests -q`), run twice: once right after the
registry row landed (before `world_scene_folder.py` was fixed) - 21
failed / 5513 passed / 327 skipped / 9711 subtests - and once after the
`world_scene_folder.py` fix:

```
20 failed, 5514 passed, 327 skipped, 9713 subtests passed in 180.60s
```

All 20 remaining failures are the GM-lane cluster in section 4, confirmed
by name against the earlier targeted run - none is new or unexplained.
Compared against the last confirmed-clean baseline this lane has (chief's
own health-check round R247, `5537 passed, 0 failed`), the arithmetic
(5537 - 20 landed failures + 1 new passing test this round =~ 5518, vs
5514+20=5534 measured) has a small (~3-4 test) discrepancy this round did
not chase down further - both directly-measured numbers above are exact
counts from this tree at this commit, not reconciled against a letter.

`tools/verify_hypothesis_ledger.py` PASS entries=47 (unchanged).
`tools/verify_functional_coverage.py` PASS domains=8 (unchanged, all 8
still INCOMPLETE - not this lane's to close).
`git diff --check` silent on both touched repos.
cp874-encodability checked by hand (`bytes.decode('cp874')`) on all six
touched files in `pirate-force-server` - all pass.

## 6. Files touched

`pirate-force-server` (6):
* `scenarios/world_scene_registry_001.json`
* `src/pirateforce_foundation/world_scene_folder.py`
* `src/pirateforce_foundation/columbus_quest_dispatch.py` (docstring only)
* `tests/test_world_scene_travel.py`
* `tests/test_world_scene_registry_rule_1_scenes.py`
* `tests/test_world_scene_folder.py`

`pf_bridge` (2): this file, and the status letter to chief.

## 7. What was NOT touched, and why

`runtime.py`, `app.py` - chief's files, not edited.
`gm/*.py`, `tests/test_gm_login_scene_sanctioned_*.py`,
`tests/test_gm_login_scene_registry_snapshot.py`,
`tests/test_gm_chat_no_bytes_line.py`,
`tests/test_gm_login_scene_admission.py`,
`tests/test_gm_login_scene_override_position_resync.py` - GM lane's write
zone; the twenty red tests there are reported in section 4, not fixed.
`scenarios/world_travel_gates_001.json` / `world_travel_gate.py` - the
walk-in-and-stop gate the owner ruled OFF `M2`/production acceptance on
2026-08-26 and ordered kept debug-only; not touched or extended this
round, on purpose.

## 8. Still open

* The GT ticket for the var2 test itself - chief's to open, both halves
  now on this tree.
* `GT-134` / `RE-155` - unchanged, still attended-only.
* `COO-DECISION 20260830_1351`'s held var2-vs-17 question - unchanged;
  this round's pin explicitly does not claim an answer to it (see the
  registry row's own `nonclaims` additions).
