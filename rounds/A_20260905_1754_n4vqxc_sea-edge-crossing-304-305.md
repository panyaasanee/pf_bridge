# LANE-A round `n4vqxc` — sea-edge crossing at scene 126 gets real arrival points (304/305)

Answers `COO-DECISION 20260905_1748`, which itself answers LANE-A's own
`20260905_1639` (sent last round, `ihjytc`). This is `1348` item 6's backup
task, picked up as this round's main work because M2's primary path
(`GT-233`) is still `BLOCKED-ON-RE` — no client-observable move today, but
this round builds what does not need RE to build.

**What a player will see that they did not see yesterday:** nothing yet on
a client screen. The actual send still needs one line in `runtime.py`
(chief's file, CORE-REQUEST sent this round) — see "What is NOT proven"
below. What this round buys: the two destinations a sea-edge crossing at
scene 126's map edge leads to now have real, checked arrival points, and
the responder's scope (which scene, which wire id, which destination) is
written and tested, so the one remaining line has something correct to call.

## Round-start checks

- **Lock**: `pf_bridge` had no open `[LANE-A]` PR at round start (the
  previous round's claim, `#1345`, had already merged). `pirate-force-server`
  had `#838` ([LANE-A] round `ihjytc`) open, gate-pending — its claim already
  merged, so per the end-of-round rule this is not a live lock. Confirmed
  during the round: `#838` merged to main mid-round (`46d7f59`), so this
  round's branch was rebased onto it via `git merge origin/main` rather than
  cherry-picked.
- **Previous round's PR fate** (ADDENDUM A): `pf_bridge#1345` merged=true.
  `pirate-force-server#838` was open at round start, merged mid-round
  (`46d7f59`) — nothing lost, no recovery needed.
- **Mailbox** (ADDENDUM B): consumed `20260905_1748` (the actionable one),
  `20260905_1749` and `20260905_1750` (both closed with no LANE-A task, per
  their own text). Stubs written, originals copied to `consumed/`.
- `KNOWN_RED_MAIN:` none — NOW.md 16:52/17:55 records `test_combat_pose`
  fixed on main by `#835`/`#837`.

## What this round did

### 1. Checked for a table-authored answer first (COO 1748 item 2)

Per the order, before falling back to a decree: does any committed table
give wire trigger ids 7/69 a destination-scene or coordinate column?
Checked `pf_bridge/gamedata/tables/CONSTDATA_TH__Trigger.tsv` (313 rows,
columns `n_ID`/`s_Trigger_Fail_SOUND`/`s_Trigger_Success_SOUND`/
`n_MESSAGE_TYPE` — no scene or coordinate column of any kind) and
`TEXTDATA_TH__Trigger_TIP.tsv` (name/tip/fail/success message columns).
Id 7 there is **"Viper Wicket"**, a dungeon entrance (`เข้าดันเจี้ยน Viper
Wicket`); id 69 is **"Ground Site Entrance"**, a structure
(`สิ่งก่อสร้างลึกลับ`) — both ordinary double-click props, and neither row
carries anything that could resolve a destination. This is a **second**
measurement of what `RE-265` already found for five of R318's seven
observed ids: the wire-level `TriggerVital` id and this catalog's `n_ID` are
different namespaces. So no table answer exists, and item 3's fallback
governs.

### 2. Regenerated the marker crosswalk (COO 1748 item 6, step 1)

`world_marker_copy.QUOTED_MARKER_IDS` gained `343` and `345`. Regenerated
`src/pirateforce_foundation/world_data/world_marker_crosswalk.json` with the
documented command (`world_marker_copy.curate('../pf_bridge/gamedata/tables')`,
`newline=''`, `PYTHONDONTWRITEBYTECODE=1` + `python3 -B` for the whole
round). `COPY_SHA256` updated in the same commit:
`ee4f601f...` → `c030f6fd96a8724f1450fcd4b1b1e1ea2cb083c8c77af1dbacd8f39896fa9117`.

### 3. Pinned the two decree rows (`world_scene_marker.DECREED_ARRIVAL_ROWS`)

```
(343, 304, 6918, -792, 90, 9)   # scene 304, Dark Fog Sea
(345, 305, 1538, 4819, 70, 6)   # scene 305, Pale Silver Sea
```

`343`'s raw `n_Y` in `CONSTDATA_TH__MARKER.tsv` is the unsigned text
`4294966504`; `s32(4294966504) == -792`. `345`'s `n_X`/`n_Y` need no
conversion (both already below 2^31). Candidate sets re-measured directly
from the table (not re-quoting last round's own letter): **304 has 7
candidates** (20, 21, 93, 95, 96, 343, 344), **305 has 11** (41, 42, 70,
101, 102, 111, 336, 345, 346, 347, 348) — matching `20260905_1639`. `343`
carries the furthest `n_X` of the seven (6918). `345` carries the furthest
`n_Y` of the eleven (4819) once `348`'s degenerate `(0, 0, 100)` origin is
excluded from the comparison; the next-highest `n_Y` in the set is `347`'s
`2538` (shared with its duplicate, `70`). `348` excluded from both
candidate sets per COO's order.

### 4. Widened the `decreed_arrival` loader to accept `decreed_provisional`

`world_scene_travel.py`'s loader previously required
`evidence_tier == "decreed_permanent"` whenever a `decreed_arrival` block
was present — correct for scene 126 (`PANYA-DECISION 20260905_1329` ruled
it permanent), wrong for 304/305 (the owner has not ruled on either). The
check now accepts `decreed_permanent` OR `decreed_provisional`; both go
through the SAME four structural checks unchanged (marker row must be one
`world_marker_copy` carries verbatim, its `n_SCENE` must point back at the
scene, the spawn must stand exactly on the marker's point, the heading must
match `n_DIRTECTION`). `decreed_permanent` still requires the block (a bare
claim of that tier with no block still raises).

### 5. Registry rows 304/305 (`scenarios/world_scene_registry_001.json`)

Arrival point only — no cast, no population, matching the narrow scope
scene 126 itself had before an earlier round built its cast separately.
`table_row`'s 14 columns, `model_id`/`image_name`, and
`native_placement_count`/`native_definition_count`/`native_sha256` all
re-derived directly from `pf_bridge/gamedata/tables/CONSTDATA_TH__SCENE_NAME.tsv`
and `pf_bridge/gamedata/PF_GAMEDATA_SCENE_INDEX.tsv` (rows `Bg3007`/`Bg3008`),
not typed from memory. `login_entry_allowed: false` for both — addresses,
not doors, same shape as 126.

### 6. `world_sea_edge_crossing.py` (new) — the three-tier responder scope

`crossing_target(current_scene_id, wire_trigger_id)`:
1. source scene must be 126,
2. wire id must be a key of the closed map `{7: 304, 69: 305}` — asserted
   disjoint from `lane_a_island_trigger_log.M2_OBSERVED_ISLAND_TRIGGER_IDS`
   (the island-docking ids 2/3) at import time,
3. the destination must resolve through `gm.warp_executor.
   warp_no_coords_live_target` — the SAME gate `/warp <scene>` uses, so the
   two paths cannot disagree about which scenes qualify.

**Sends nothing.** No frame composed, no session touched. Composing and
returning a live-teleport frame from `runtime.py`'s TriggerVital branch is
chief's file — CORE-REQUEST sent this round
(`20260905_1834_LANE-A-CORE-REQUEST-wire-sea-edge-crossing-triggervital-response.md`).

### 7. `world_scene_folder.py`

Added folder entries for 304 (`Bg3007`)/305 (`Bg3008`) — confirmed against
the actual bridge directory names, not assumed from `model_id`.

## pf-adversary — 2 findings, both addressed

Run once (quota 1 of 2 used), returned before push, both findings fixed in
a second commit under this same round code before the full suite ran.

- **Finding (Medium-High, measured, fixed).** The first draft's own
  `world_sea_edge_crossing.py` docstring and both registry rows' `status`
  text claimed 304/305 were reachable *only* through the not-yet-wired
  responder ("no /warp gate names this scene either"). **False, caught by
  calling the function rather than trusting the prose**: pinning
  `decreed_arrival` also satisfies `has_authored_entry`, which is all
  `gm.warp_executor.warp_no_coords_live_target` checks — so a bare GM
  `/warp 304`/`/warp 305` is live *today*, independent of whether anything
  ever calls `crossing_target` from `runtime.py`. The adversary's own
  proof: it is what this round's own `test_gm_warp_chain_census_shipped.
  _bare_warp_destinations()` docstring already said correctly, in the same
  commit, while the module docstring said the opposite two files away. This
  is the same widening `#838` already made for scene 126 — here an accepted
  side effect of reusing that scene's own gate rather than a decision made
  on purpose for these two. Still GM-only (`accounts.is_gm_account` gates
  `/warp` itself, unchanged); still no ground bounds or census for either
  scene. **Fixed**: corrected the module docstring (added an explicit
  "ONE THING THIS ROUND DELIBERATELY WIDENS" section, the same shape `#838`
  used) and both registry `status` strings, and added
  `test_pinning_the_decree_also_opens_bare_warp_to_both_scenes` so the
  claim is checked, not just fixed in prose.
- **Suspicion (Low, not acted on).** The "furthest in the entry direction"
  framing picks the maximum coordinate on both axes regardless of whether
  "west"/"south" would suggest a minimum in the destination scene's own
  (unrelated) coordinate frame. Not verifiable as wrong — 126 and 304/305
  share no coordinate frame — and this is exactly the criterion COO's own
  decision named (`1748` item 3, confirming LANE-A's own `1639` choice);
  `GT-267` is partly a test of the guess itself, and a wrong guess costs one
  JSON value next round, not a new ticket.
- **Re-derived independently and confirmed clean, no fix needed**: the s32
  conversion of marker 343's raw `n_Y`; all 7 (scene 304) and 11 (scene 305)
  candidate marker rows recomputed by hand from `CONSTDATA_TH__MARKER.tsv`
  (not quoted from last round's own letter); furthest-X/furthest-Y
  selection; the crosswalk regeneration reproduced byte-for-byte with a
  matching `COPY_SHA256`; registry provenance (`table_row`,
  `native_placement_count`/`native_definition_count`/`native_sha256`) cross
  -checked directly against `CONSTDATA_TH__SCENE_NAME.tsv` and
  `PF_GAMEDATA_SCENE_INDEX.tsv`, not the JSON's own claims; the
  `decreed_arrival` loader's four structural checks apply identically to
  both evidence tiers (verified: they sit inside one unconditional block,
  not gated per-tier). Mutants tried and caught: removing `crossing_target`'s
  type checks (2 tests red), swapping scene 304's decreed marker to a real
  but wrong candidate (module fails to load, 15 failed/56 errors), and a
  manufactured collision between the sea-edge and island-docking id maps
  (import-time `AssertionError`).

## Tests

`BYTECODE_PURGED: PYTHONDONTWRITEBYTECODE=1 + python3 -B for the whole round`
(no `__pycache__` deleted — `PROCESS_GATES` 26).

Narrow, run repeatedly while working:
`tests/test_world_sea_edge_crossing.py` (new, 17 tests/11 subtests after the
adversary-fix commit added one more), `tests/test_world_scene_decreed_arrival.py`,
`tests/test_world_scene_travel.py`, `tests/test_world_marker_copy.py`,
`tests/test_world_scene_marker.py`, `tests/test_gm_warp_chain_census_shipped.py`,
`tests/test_world_scene_folder.py`, plus a ~110-file sweep of every test
referencing the touched modules (`gm/warp_*`, `gm/login_scene_*`,
`world_population_*`, `world_m2_*`, `lane_a_*`) — all green throughout,
before and after the adversary-fix commit.

Full suite, once, on the final commit (`ef7f8c1`) merged with `main`
(`4a856d8`, includes `#838`/`#839`): **11116 passed, 327 skipped, 20964
subtests passed, 0 failed** (498.27s).

## Letters this round

- `20260905_1834_LANE-A-CORE-REQUEST-wire-sea-edge-crossing-triggervital-response.md`
  — the one line chief needs in `runtime.py`'s TriggerVital branch.
- `20260905_1900_LANE-A-GT-267-TICKET-BODY-sea-edge-crossing-126-to-304-305.md`
  — the attended-test body for chief to paste under the already-reserved
  `GT-267` header, marked `BLOCKED-ON-WIRING` (not `READY`, and not
  `BLOCKED-ON-MERGE` — this round's own PR carries no blocker) with a
  RECHECK script for chief/the tester to confirm the hookup landed before
  ever booting it.
- Consumed: `20260905_1748`, `20260905_1749`, `20260905_1750` (stubs +
  `consumed/` copies).

## What is NOT proven

- **Nothing on a screen.** No client was booted this round. The arrival
  points and the responder scope are code-level facts, checked against the
  same gate `/warp <scene>` uses and against the committed client tables —
  not a measurement of what a ship sailing the edge actually does.
- **The fallback coordinates are a guess, tagged as one.** `decreed_
  provisional`, not `decreed_permanent`: the owner has not ruled on either
  scene the way she ruled on 126, and `GT-267` exists partly to test the
  guess itself (record where the ship actually surfaces).
- **No cast.** 304/305 have no population/composer — `test_gm_warp_chain_
  census_shipped.SCENES_WITH_NO_CENSUS_COMPOSER_YET` names this explicitly
  rather than silently exempting it. Building one is real future LANE-A
  work this round's letter did not ask for.
- **The durable write will refuse**, same shape as scene 126: both new
  scenes carry `login_entry_allowed=false`, so `gm.warp_scene_persist.
  login_would_accept` refuses both once the send is wired. Expected, not a
  defect — the same gap `#838` already named for 126.
- **The third observed edge (wire id 48, north) is not pinned.** COO named
  only 7 and 69; a third row would be inventing a destination nobody has
  ruled on.
- **Access widened, declared (pf-adversary finding, above).** A bare GM
  `/warp 304`/`/warp 305` is live today — an accepted side effect of the
  same `has_authored_entry` gate `#838` already widened for scene 126, not
  a decision made on purpose for these two. GM-only; no ground bounds or
  census composed for either scene if used this way today.

TWO_SESSIONS_SAME_SCENE: not applicable — this round adds no per-scene
mutable world state (no roster, no mob, no ground item); it only adds a
static registry pin and a pure lookup function. Nothing here writes to
shared per-scene memory a second session could observe diverging.

## Status

Server PR: **`pirate-force-server#843`**, open, not draft, marker verified
by a GET, waiting on the gate. Round lock released at this claim PR's
marker, per the standing rule — not waiting on the server gate or its
merge.
