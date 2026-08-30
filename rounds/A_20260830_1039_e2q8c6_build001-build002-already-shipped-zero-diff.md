# LANE-A round `e2q8c6`

Opened 2026-08-30T10:24+07:00 (per orchestrating session). This account written
2026-08-30T10:39+07:00 (`TZ=Asia/Bangkok date`).

## Assignment received

BUILD-001 (M1): "shoot all 115 actors at once" for bg0001, with a pre-check
that the frozen `current/pf_login_game_server_v141.py` AGENTS.md §7 rule is
not violated (owner-recalled ruling is not a written sign-off, so any fix must
route through an already-editable seam).

BUILD-002 (M2): scene_id default is 1, never anything else; first target
n_ID 278 `Bg1177` (beach football field, TEST), per
`archive/notes_to_chief_2026-08-19_to_26/20260825_2020_PANYA-REQUEST-*.md`.

## What investigation found

BUILD-001 is **already fully realized on `main`**, from prior rounds this
session did not run. BUILD-002's door mechanic is likewise shipped, but the
M2 milestone itself is formally paused, not closed -- see item 2 below:

1. **BUILD-001**: `src/pirateforce_foundation/world_population.py` (this
   lane's own module, `production_allowed = True`) widens the same encoder
   over the same frozen `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` table from 3 to
   the full census, wired unflagged into `runtime.py`'s default dispatch
   since round R173. `GT-131` (attended, in-game) **PASSED** with the owner's
   own words on 2026-08-30T00:2x, confirming NPC identity on the wire path.
   The frozen file was never edited — exactly the seam the task description
   predicted, confirmed by grep and by reading the module's own docstring
   history (RE-128, CHARTER-02 amendment, COO-DECISION 20260829_1941 on the
   108/115 data ceiling).

2. **BUILD-002**: the Columbus -> scene 17 door mechanic
   (`columbus_quest_dispatch.dispatch_columbus_quest3021`) is real and
   player-visible, unflagged since 2026-08-27, client-observed standing on
   the ship deck per `GT-106` (attended). That is a shipped mechanic, not a
   closed milestone: M2 itself remains **formally paused**.
   `PANYA-DECISION 2026-08-27 20:10` paused BUILD-002/M2 to focus on
   M1/identity-first, and that pause has not been lifted — reaffirmed in
   `pf_bridge/notes_to_chief/20260828_1044_COO-DECISION-m2-pause-vs-addendum-conflict-affirmed.md`
   and `pf_bridge/notes_to_chief/20260828_2250_COO-DECISION-lane-A-m3-without-the-m2-door.md`
   ("ไม่ปลดพัก M2 — ผมเคาะไม่ได้ ... เจ้าของเท่านั้นที่ปลดได้" — only the owner can lift it).
   Separately, `GT-106-R2` — the reconfirmation ticket `COO-DECISION 20260827_1746`
   requires before anyone may announce M2 passed — has never been opened
   (`pf_bridge/GAME_TEST_QUEUE.md:4951-4958`). Neither of these is mentioned
   by claiming "BUILD-002 already shipped" as a milestone; only the door
   mechanic should be described that way.

   Scene 278 (`Bg1177`, this round's literal assignment target) is fully
   pinned in `scenarios/world_scene_registry_001.json` with an authored
   spawn and passes `load_scene_registry`'s validation, but that target is
   itself stale: `COO-DECISION 20260826_1645` (2026-08-26T16:45, answering
   the owner's own `20260826_1600_PANYA-DECISION-there-is-no-walk-in-travel-gate-...md`)
   redefined M2's acceptance criteria away from any walk-in scene-278 gate
   entirely, in favor of Columbus/sea-map/dock/captain-report. Whoever
   generates the next round's assignment brief should stop citing scene 278
   as the M2 target. A walk-in travel gate to scene 278
   (`src/pirateforce_foundation/world_travel_gate.py`, gate
   `port_royal_columbus_departure`) exists, is tested, and works — but that
   same `COO-DECISION 20260826_1645` (not `20260826_0150`, which is a
   different letter about the M2/v2-slice definition split and explicitly
   disclaims proving scene 278 walkable) explicitly pulled this "walk and
   stop" mechanic out of M2 acceptance criteria and ordered it kept
   debug-only, off by default, forever, because the owner confirmed the
   real in-game door out of town is Columbus/ship/dock, not a walk-in
   trigger. Enabling it this round would directly contradict a standing
   COO ruling, not just duplicate finished work.

3. **Open thread, not this round's to close**: `notes_to_chief/
   20260830_0909_LANE-A-STATUS-choosenpc-responder-*.md` (round `n4wj7k`) is
   still unconsumed — a one-line `CORE-REQUEST` for a `runtime.py` guard so
   scene 14's fully-built `ChooseNPC` responder can flip
   `production_allowed = True` safely. Re-flagged in this round's status
   letter since it is the single highest-leverage next unblock and nobody
   has acted on it yet.

4. **NPC facing-direction defect** (one of the four owner-filed polish gaps
   from `GT-131`, flagged by the orchestrating session as the "most
   interesting" candidate): `RE-116` (2026-08-28, DONE/BOUNDED-NEGATIVE)
   already closed this — no per-placement heading exists in either the raw
   `.npc` placement bytes or `CONSTDATA_TH__MARKER.n_DIRECTION`. The owner's
   own note says the `FACE_PLAYER_POSITION_HEADING` frame goes out correctly;
   the gap is between the frame and how the client renders it, not a missing
   send. Nothing to build here without inventing data or new client-side
   evidence, which this round's rules forbid.

## Verification performed (no code changed)

`python3 -m unittest discover -s tests -p "test_*.py"` on `pirate-force-server`
HEAD: **5508 tests, errors=18 (all `ModuleNotFoundError: capstone`,
pre-existing environment gap, unrelated to this lane), skipped=212, no new
failures.**

## Files touched this round

- `pf_bridge/notes_to_chief/20260830_1039_LANE-A-STATUS-build001-build002-already-shipped-zero-diff.md` (new)
- `pf_bridge/rounds/A_20260830_1039_e2q8c6_build001-build002-already-shipped-zero-diff.md` (this file, new)
- `pirate-force-server/rounds/A_20260830_1039_e2q8c6_CLAIM.md` (new, pointer)

Zero diff under `src/ scenarios/ tools/ current/ tests/` in either repository
this round, by investigation rather than default — BUILD-001 is done and
player-confirmed; BUILD-002's door mechanic is done and player-confirmed but
the M2 milestone it belongs to remains formally paused pending owner release
and `GT-106-R2`; and the one remaining travel mechanism for the literal
(and now stale) BUILD-002 scene-278 target is off by explicit, standing COO
ruling.
