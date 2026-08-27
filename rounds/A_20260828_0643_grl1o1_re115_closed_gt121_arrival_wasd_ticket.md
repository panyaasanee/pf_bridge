# A_20260828_0643 (grl1o1) -- RE-115 closed (map window is client-local, no build item), GT-121 opened (test the arrival-census fix without WASD), no runtime.py code this round

## §2 item 7 (previous round fate check)

`pf_bridge#274` / `pirate-force-server#173` (round `ga4k2t`) both `merged=true` per the previous round file's
own Protocol A check -- not re-derived here, nothing to cherry-pick.

Since `ga4k2t`, one more full LANE-A cycle happened on `main` that this round's briefing predates: chief's
`R207` (branch `confident-ride-sf9kel` / `jolly-mccarthy-sf9kel`) wired `CORE-REQUEST-026` --
`pirate-force-server@13fe3aa`, confirmed on `origin/main` ancestry this round
(`git merge-base --is-ancestor 13fe3aa 375e4ab` => yes, `375e4ab` = merge commit of `pirate-force-server#177`).
This round's own branch (`claude/sleepy-ride-grl1o1`) was still forked from BEFORE that commit, so the first
action this round was `git merge origin/main` on the `pirate-force-server` clone (merge commit `afb4971`,
clean, no conflicts, 2 files: `runtime.py` + the new `tests/test_bg0002_census_wiring.py` tests) -- picking up
chief's own already-landed work, not authoring new runtime.py content.

## What CORE-REQUEST-026 actually does (read from the merged source this round, not from the letter alone)

`runtime.py`'s WORLD-CENSUS-001 bg0002 branch (`5637-5690` area) now admits an arrival with
`self.last_target_pos is None`, but ONLY when `scene_id == world_population_bg0002.SCENE2_N_ID` (a disjunct
added to the outer guard) -- anchored on `world_scene_travel.spawn_position(world_scene_travel.destination(
scene_id, scene_entry_registry))` as a fallback, latching `world_census_refused = True` (not retrying) if that
lookup fails. bg0001 (Port Royal) is untouched, still requires `last_target_pos is not None` in every path --
confirmed structurally and by the new control test `test_scene1_still_waits_for_a_target_pos_vital_unlike_
scene2`. `production_allowed = True` in `world_population_bg0002.py`, `world_census_enabled = not active_lanes
and second_password_mode == "required"` in `runtime.py` -- this is default-on, no `--*-scenario` flag needed,
same as the charter mandates.

Still true, unchanged since CORE-REQUEST-021: no seed path exists on ANY default boot for a stored character
row that names `scene_id=2` (`grep P0_P30_P91\|scene2.*seed` in `src/` = 0 hits). Getting a real client onto
this code path requires the run-DB-copy seed procedure M1-P's own attended session already used once
successfully today (`character_positions.scene_id` 1->2 on a throwaway copy) -- confirmed by
`20260828_0038_CHIEF-REPLY-KA1A-2240-*.md` to be attended/tester work, not chief's or this lane's to build.

## Mailbox: one genuinely new, unconsumed item found -- RE-115 RESULT

Fresh mailbox scan (files named `2026082[89]_0[5-9]*` or later, cross-checked against `.CONSUMED.txt`
siblings) turned up `notes_to_chief/20260828_0221_RE-115-RESULT-SCENE-NPC-STATIC-LOCAL-GO.md` -- written
02:21+07:00, addressed `chief cloud (cc), Panya, สาย A`, still had no `.CONSUMED.txt` and `CLIENT_RE_QUEUE.md`
still showed the RE-115 header as `🟡 OPEN` at the time this round started. This predates this round's own
briefing snapshot (which cited `ga4k2t`/`5m2a6z` as the latest state) -- it landed on the bridge sometime after
those rounds closed and before this one started, and nobody had processed it yet.

**Verdict (static, image-proven, this round only reads and relays it):** the in-game map window's "NPCs in
this scene" list is CLIENT-LOCAL -- parsed from the scene's own `Data\Scene\Save\<scene>\<model>.npc` file
(`MOBSET` records: NPC id + X/Y), dressed with `MOBS`/`MOBS_TIP` by NPC id. Full `external/` scope (30 files,
29.9MB, fingerprint pinned) has no separate list opcode/handler -- this is NOT this project's own actor
census (`world_population.py`/`world_population_bg0002.py`) and never was. GO! resolves the picked NPC id
locally too (`item+0x94` -> `map+0x9C` -> local event `0x14`, no X/Y, no network-send call in the traced CFG)
-- this does not contradict RE-119 (`CTracePathReqVital`/`0x4391` IS a real outbound frame, static-proven
separately): RE-115's CFG stops at the internal event `0x14` dispatch, a plausible upstream trigger for the
separately-registered tracepath module RE-119 already found, not the same call chain RE-115 walked.

**BUILD_IMPACT, quoted from the result letter:** "Server ไม่ควร invent packet รายชื่อ NPC เพื่อทำให้หน้าต่าง M
แสดงรายการ; client มี source + display metadata + coordinates อยู่แล้วจากไฟล์ scene." No buildable item for this
lane directly -- what already matters (scene identity + NPC-id-compatible census data) is exactly what
CORE-REQUEST-021/026 already build. Also resolves the "Mirage Reel" side-question from M1-P gap 5 at the
*mechanism* level (why it shows in the map list without our census sending it -- client-local, as expected)
without resolving the specific n_ID (still a separate, open lead, not closed by this ticket).

**Action taken:** `CLIENT_RE_QUEUE.md`'s RE-115 header closed to `CLOSED PASS/DONE` with the verdict/
BUILD_IMPACT quoted inline (RE-115 was opened by this lane originally, so its own header is this lane's to
close per addendum v2 B.3). `.md.CONSUMED.txt` stub written per the `.md.CONSUMED.txt` naming standard
(COO-DECISION 2026-08-28T00:43), plus a copy into `notes_to_chief/consumed/` matching the existing pattern
(root `.md` stays, copy added, not moved -- verified against `RE-116`'s own already-consumed pair as the
live example).

## Rule F: this would have been LANE-A's second consecutive code-empty round -- picked (c)

`ga4k2t` (0529) was already a doc/mailbox-only round for this lane (its own letter explicitly says so, citing
real prior-round work at `5m2a6z` as why it wasn't itself a rule-F violation). Checked all four rule-F options
fresh before concluding a second empty round was unavoidable in `src/`:
- (a) pre-approved backlog: every open lane-A backlog item (heading-real, GO-real auto-walk, attr
  completeness, Port Royal identity) is blocked on RE runner, chief's `runtime.py`, or the owner's own M2
  pause (`PANYA-DECISION 20:10`, still standing, `PANYA-DECISION 0200`'s own priority list still lists "M2
  ยังพัก" at position 6) -- confirmed by re-reading each, not assumed.
- (b) STATIC-ON-BRIDGE ticket answerable from source/factpack already in this clone: tried this first, for
  real -- spent real time cross-referencing `gamedata/tables/CONSTDATA_TH__MOBS.tsv` /
  `TEXTDATA_TH__MOBS_TIP.tsv` against `Bg0002.placements.tsv`'s unresolved 9 (n_ID 37 + MOBSET 101-104), to
  see if the "Mirage Reel" identity or the 101-104 block could be resolved from tables alone. Result: NN=37
  ("Port transportation") confirmed to have a `MOBS_TIP` title but genuinely NO `CONSTDATA_TH__MOBS` row at
  all (`awk` gap check: `36 -> 38` in the id sequence) -- this independently reproduces
  `scene2_prison_exile_tables.py`'s own already-documented finding byte-for-byte, so there was nothing new to
  add there; it is already correctly UNRESOLVED, not a hidden bug. The 101-104 block stays explicitly
  UNKNOWN/forbidden-to-guess per `PANYA-DECISION 20:10` -- did not attempt to resolve it further (would need
  RE-runner-grade image work this lane does not have access to, not local-table work). RE-115 (found during
  this same mailbox pass, see above) turned out to be the real (b) item this round.
- (c) write/adjust a queue entry: **picked** -- `GT-121` (below).
- (d) pf-adversary-flagged technical debt in this lane's own files: none found this round (checked
  `world_population_bg0002.py`/`scene2_prison_exile_tables.py`/`trace_path.py` docstrings and existing
  nonclaims sections for open TODOs -- all current debt items named there are either already resolved or are
  explicitly `runtime.py`-scoped, chief's file, not this lane's to fix).

## GT-121 opened -- tests CORE-REQUEST-026 specifically, without WASD

`GAME_TEST_QUEUE.md` gained one new entry, `GT-121 CORE-REQUEST-026 BG0002-ARRIVAL-CENSUS-NO-WASD-001`.
Numbering re-verified fresh before writing (`GT-121`/`RE-120` = 0 hits pre-entry, highest in use = `GT-120`).

Why this is a real, new test and not a re-run of M1-P: M1-P's own PASS session (00:2x-00:5x+07:00, boot
commit `6406a05`) ran BEFORE `13fe3aa` existed, and its own console evidence (L260 -> L264-265) shows the
census arriving only after the client's first `TargetPosVital` -- i.e. M1-P's tester DID press a movement key
before the census showed up, which is exactly how gap ① got noticed at all. Nobody has tested the fixed
build's actual claim yet: does the roster appear at T0, before any key press. GT-121 reuses M1-P's own proven
seed procedure (`character_positions.scene_id` 1->2, spawn `26905,21185,1680` -- verified this round to be the
exact literal `scenarios/world_scene_registry_001.json` pins, via `python3 -c "json.load(...)"`, not assumed
from a comment) and adds an explicit "do not press any key" discipline to the steps that M1-P's own procedure
did not need. Every grep target in the ticket's ด่าน 2 (`world_census_bg0002_arrival_anchor_refused`,
`SCENE2_N_ID` in `world_population_bg0002.py`, the new test names) was independently re-grepped against the
actual merged source this round before being written into the ticket, not copied from the letter/round-file
descriptions uncorroborated.

## pf-adversary (manual pass -- no code this round, so `.claude/agents/pf-adversary.md`'s subagent tool was
not invoked; the review below applies its own 11 named failure shapes by hand against every doc claim written)

- Stale pins (#3): the `pirate-force-server@13fe3aa` / PR `#177` ancestry claim is independently re-derivable
  (`git merge-base --is-ancestor`, shown above), not copied from a letter. The GT-121 ticket itself tells its
  own future reader to re-confirm at boot time (ด่าน 0/1/2), not to trust the writing-time SHA blindly.
- Evidence layer laundering (#8): GT-121's pass criteria keep wire/DB (already closed headless by the 4 new
  tests) and client-observable (this entry's own job) in two clearly separate sections, same convention as
  GT-120.
- Unlabeled proposal vs measurement (#11): GT-121's P1/P2/P3 predictions are explicitly labeled predictions,
  not measurements, matching GT-120's own format.
- cp874 (#7): `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` are outside the gate's enforced scope
  (`src/ tools/ current/` only, per this lane's own charter note) and already use ①②③ etc. throughout (105
  pre-existing hits) -- the new GT-121/RE-115 text follows the same existing convention, not a new exception.
- "Nobody has done this yet" from a single source (#9): the RE-115 closure and the GT-121 spawn coordinate
  were both independently re-verified against the actual repo files this round (grep, `git log`, `json.load`)
  rather than trusted from the letters alone -- shown throughout this file.
- No defects found requiring a fix before push.

## Files touched

**pf_bridge** (this repo): `CLIENT_RE_QUEUE.md` (RE-115 header closed + verdict quoted), `GAME_TEST_QUEUE.md`
(new `GT-121` entry appended), `notes_to_chief/20260828_0221_RE-115-RESULT-SCENE-NPC-STATIC-LOCAL-GO.md.
CONSUMED.txt` (new stub), `notes_to_chief/consumed/20260828_0221_RE-115-RESULT-SCENE-NPC-STATIC-LOCAL-GO.md`
(copy), this round file, the companion `notes_to_chief/` letter.

**pirate-force-server**: no new authored code this round -- one merge commit (`afb4971`, `git merge
origin/main`) to bring this branch current with chief's already-landed `CORE-REQUEST-026`. `git diff` against
the merge's own two parents shows zero additional changes beyond what the merge itself carried.

## What is not proven

- GT-121 itself is unrun -- it is a queue entry for a human tester, not a claim that the fix works on a real
  client. That is exactly what it exists to find out.
- The 101-104 MOBSET block and NN=37 stay UNRESOLVED, unchanged from before this round -- explicitly not
  attempted to guess this round either (see rule-F (b) section above).
- RE-115's own nonclaims stand as written by the RE runner (does not claim event `0x14`'s full semantic, does
  not claim no other server map/actor traffic exists outside the scoped fingerprint) -- this round only
  relays and closes the ticket, does not extend the claim.

## CORE-REQUEST

None opened this round.

## เปิดใบให้สาย C

None opened this round (RE-115 was CLOSED, not opened, and was this lane's own prior ticket).
