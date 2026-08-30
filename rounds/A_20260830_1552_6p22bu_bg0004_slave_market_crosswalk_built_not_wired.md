# LANE-A round 6p22bu

Opened 2026-08-30T14:52+07:00, closed 2026-08-30T15:52+07:00 (approx).

Player-visible change: none. Scene 4's `login_entry_allowed` is unchanged
(`false`) and no code path a player can reach changed this round.

## What this round did

Carried out `COO-DECISION 2026-08-30T14:41+07:00`
(`notes_to_chief/20260830_1441_COO-DECISION-scene4-slave-market-first-door.md`),
approving this lane's own recommendation from round `12lyda`: start the
CLINE->MOBS native-actor crosswalk for scene 4 (Bg0004, Slave Market Island,
116 native placements, the highest of the ten still-shut doors surveyed),
same pattern as BUILD-001's bg0001 crosswalk and M3's bg0015 crosswalk.

1. Re-derived the join by hand directly off this clone's own committed
   tables (not copied from any sibling module's citation of the same
   tables): `gamedata/tables/CONSTDATA_TH__SCENE_NAME.tsv` (scene 4 ->
   `n_CLINE_TYPE=4`, `n_SCENE_LV=45`), `CONSTDATA_TH__CLINE.tsv` (type 4's
   61 rows), `CONSTDATA_TH__MOBS.tsv`, `TEXTDATA_TH__MOBS_TIP.tsv`,
   `CONSTDATA_TH__STANDARD_MOB.tsv`, and
   `gamedata/scene/bg0004/bg0004.placements.tsv` (116 rows). All five
   shared-table digests re-derived this round matched what sibling
   crosswalk modules already pin; the scene's own placements TSV got a
   fresh digest.

2. Measured (not estimated): 55 distinct Mob-Set numbers used across the
   116 placements, all 55 present in CLINE type 4's 61-key block (six
   unused keys, 109-114, all carry leader 0 -- "no creature"). 48 of the 55
   resolve to a real body; 7 do not (1 has no `CONSTDATA MOBS` row at all --
   the same "Port transportation" boat prop that recurs, under different
   ids, at both Bg0001 and Bg0015; 6 have a MOBS row with an empty
   `s_OUTFIT`). 109 of 116 placements ship; 7 are dropped, each with its
   placement index and reason on the console.

3. One resolved leader (917, outfit `INVISIBLE`) has no `MOBS_TIP` row and
   ships with an empty name -- the exact shape `world_port_royal_identity.py`
   already ships for the SAME leader id at Bg0001 (its own Mob-Set 98/103).
   This one leader alone accounts for 25 of the 109 shippable placements
   (Mob-Set 107, instances 01-25) -- more than a fifth of the island. Nine
   sets carry a `;`-separated multi-variant outfit (44 of 109 shippable
   placements affected); shipped first-variant only, the same
   `[LANE-A ASSUMPTION - AWAITING COO/OWNER CONFIRMATION]` every sibling
   crosswalk module already carries.

4. Named two anomalies rather than silently resolving them: placements 82
   and 83's free-text `name` column disagrees with the machine-parsed
   `template_ids` column ("Mob_Set_34 08/09" vs. 45/46) -- followed
   `template_ids`, the column `field_mob_tables_bg0002.py` already treats as
   authoritative for its own scene. Placement 83 also carries a second,
   unbuilt spawn triple in its raw row; not shipped as a 117th actor this
   round (that would silently move the round's own 116-placement target),
   recorded by name in `EXTRA_TRIPLE_NOT_SHIPPED`.

5. Built and verified end to end against the real frozen `v141` encoder:
   `src/pirateforce_foundation/world_bg0004_identity.py` (the crosswalk
   table) and `src/pirateforce_foundation/world_population_bg0004.py` (the
   census composer, reusing the exact frozen serializers every sibling
   composer already uses -- no new encoder path). A real build produces a
   109-actor collection whose wire header count agrees with its 109 bodies,
   every body byte-intact, every console line cp874-encodable. Added
   `tests/test_world_bg0004_identity.py` (15 tests / 64 subtests) and
   `tests/test_world_population_bg0004.py` (14 tests / 355 subtests),
   including a GT-078-regression check against the real wire bytes (the
   NPCAttr template field carries the real `MOBS.n_ID`, never the raw
   Mob-Set number) and an explicit AST-walk pin that nothing under `src/`
   imports the new census module yet.

6. NOT registered anywhere a player can reach: `world_scene_travel.
   CENSUS_SOURCES`, `world_population_handoff.ROSTER_COMPOSERS` and
   `lane_hooks/lane_a_scene_census.py`'s console-reader table are all
   untouched, and scene 4's `login_entry_allowed` stays `false`, exactly as
   the COO decision instructs. `world_bg0015_identity.py` / `world_
   population_bg0015.py`'s own history shows the identity+census pair
   landing several rounds before their wiring did (`w0pu2i` built it,
   `ga91m5-r2` wired it, several rounds apart) -- this round does the same
   first half for scene 4, deliberately, so this round's diff can be
   verified on its own before a later round's wiring touches three more
   shared plumbing files and their tests.

## Fallout fixed in the same round: the actor-entry static-census pins

Adding `world_population_bg0004.py` moved three numbers
`pirate-force-server`'s `tools/pf_runtimeres_actor_entry_static.py` pins
from `src/`'s own content (entry sites 17->18, carrier sites 26->27,
entry-building modules 16->17, new name inserted alphabetically between
`world_population_bg0002.py` and `world_population_bg0015.py`). This is
outside the round brief's four named write-zone paths, but it is the same
maintenance duty every prior lane that added an actor-entry call site has
had to carry out in the same commit (`w0pu2i`, `y9s0xo`, `7ptoku` and others
all did this three-place re-pin for their own new module) --
`tests/test_static_verifier_pins_cloud.py` exists specifically to catch a
lane that skips it. Re-pinned this round: the verifier's own guards, the
bridge-only test module's copy of the same three pins, and the report's
`RUNTIMERES_COUNTS` JSON block plus one new append-only NOTE section (no
existing prose in that report rewritten, following its own erratum
convention).

## Full test suite (pirate-force-server)

`python3 -m pytest tests -q`: **5431 passed, 383 skipped, 9540 subtests
passed, 0 failed** (118s). Before the actor-entry-pin fix above, the same
run showed 11 failed (all in the two static-verifier-pin test modules,
purely from the three numbers this round's own new module moved -- nothing
else). The 383 skips are the pre-existing image-gated / `capstone`-import
gap this environment cannot run, unchanged in count from before this round.

## What's blocked / waiting

- The pairing (which Mob-Set number is which leader) is table inference
  only -- no human has stood in this scene (registry `status:
  never_sent_to_any_client_by_this_project`). No ticket opened for it this
  round since nothing is wired to a login path yet.
- Whether any of this scene's monster-shaped placements (Scythe Beetle, Orc
  Chief, Dragon Gladiator etc., the level 46-58 sets with a nonzero
  `n_RANK`) should be hostile is a LANE-B decision, explicitly not made
  here -- the same split PANYA-DECISION 2026-08-27 20:10 drew for Bg0002.
- Wiring (`CENSUS_SOURCES` / `ROSTER_COMPOSERS` / `lane_hooks` console
  reader) -- next round of this same multi-round order, per the COO
  decision's own "multi-round, no deadline" instruction.

## What was not done

Did not touch `runtime.py` or `app.py`. Did not touch the frozen
`current/pf_login_game_server_v141.py`. Did not touch
`scenarios/world_scene_registry_001.json`'s `login_entry_allowed` for scene
4. Did not decide hostility for any monster-shaped placement (LANE-B's
call). Did not wire the new composer into any player-reachable path.

## CORE-REQUEST

None this round.

## ASK-COO

None this round (the COO decision this round carries out already answered
the open question from round `12lyda`).
