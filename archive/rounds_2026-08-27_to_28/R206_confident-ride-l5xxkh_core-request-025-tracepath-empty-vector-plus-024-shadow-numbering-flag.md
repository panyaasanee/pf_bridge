# R206 (confident-ride-l5xxkh / jolly-mccarthy-l5xxkh) 2026-08-28 ~05:0x (+07:00)

## Lock-fate check (v6.2 §2 item 7, done first)

`pf_bridge#268` / `pirate-force-server#170` (R205, LANE-E) both `merged: true` (confirmed via
`pull_request_read`). R205's work is on `main`; no cherry-pick recovery needed.

## CORE-REQUEST check (§17 item 3, done before any other work)

`notes_to_chief/20260828_0427_LANE-A-CORE-REQUEST-025-wire-tracepath-empty-response-fallback.md`
was the one actionable, unblocked CORE-REQUEST addressed to chief since R205. Wired it this
round. The registry's other open rows (011/012 GmCommand decode gap, 014 second half, 015
mob_pickup, 017 point 2) remain blocked on RE work this clone cannot do or on functions that do
not exist yet — unchanged from R205's own check.

While reading letter 025 I found it flags something chief needs to act on: LANE-A's own
`20260828_0234_LANE-A-CORE-REQUEST-024-*.md` letter (bg0002 census sent on arrival instead of
on the first `TargetPosVital`) was assigned "024" by LANE-A before it knew LANE-B's
attack-cadence letter had already claimed "024" for real (R205, merged 2026-08-27T21:19Z).
Neither commit/letter that already shipped under "024" gets renumbered (rule: never edit a
pushed letter/commit), but the registry can't carry two different requests under one number
going forward — reserved **CORE-REQUEST-026** for LANE-A's bg0002-census-arrival request. Not
wired this round: this round already has one topic (025) and PANYA-ORDER 1230 item 2 caps a PR
at one topic, ~6 files. 026 is a different single-point change in a different part of
`runtime.py` (line ~5574 vs. the dispatch chain near line 4530) but chief did not open two PRs
back-to-back this round rather than gate on the first one's merge mid-round (§7's "ใบต่อไปเปิด
หลังใบก่อน merge" implies waiting for confirmation the first actually landed, which this
single-pass round has no way to observe synchronously). Queued for the next round; not urgent —
LANE-A's own letter already says the census cannot actually reach any real character today
(needs `scene_id=2` seeded rows, which chief has not started).

## What changed

Client's map-window GO! button sends `CTracePathReqVital` (0x4391); the server never answered
it at all (grep confirmed 0 hits for `0x4391`/`0x2F92`/`TracePath` anywhere in `runtime.py` or
`app.py` before this round) — client shows "finding path..." forever (KA1A finding,
`20260828_0235_KA1A-FOUND-GO-button-*.md`). RE-119 (STATIC-ON-BRIDGE, PASS/DONE, this project's
own RE runner) proved the client's response handler treats an *empty* `CTracePathVital`
(0x2F92, `u16` record count = 0, no records) as a clean signal to dispatch `EndFindPath` and
clear the stall — no waypoint/auto-walk semantics needed or claimed.

New `src/pirateforce_foundation/trace_path.py`: `TRACE_PATH_REQ_VITAL_ID`(0x4391) /
`TRACE_PATH_VITAL_ID`(0x2F92) constants, `make_trace_path_empty_response(legacy)` built on the
proven `legacy.u16tag`/`legacy.make_runtime_vitals` primitives (no hand-rolled framing). Version
byte for the reply vital is an explicitly-labelled unproven default (0), matching this
codebase's own convention for reply vitals RE has not separately pinned a version for
(`CHIT_RESULT_VITAL_VERSION`, `PICKUP_LISTENER_VITAL_VERSION`, `LEARN_SKILL_REQUEST_VITAL_VERSION`
are all 0 too).

`runtime.py`: unconditional dispatch branch (no scenario flag — this is a production path, not
a probe) inserted right after the existing logout post-ack guard in `_dispatch_with_lanes`.
Replies only when `self.foundation.selected is not None` (fail-closed otherwise, matching every
other in-world lane's own convention, e.g. `_dispatch_item_move_capture`).

**pf-adversary caught one real defect before push**: the module docstring's prose used the
literal word "quest" (describing RE-119 T4's bounded-negative discriminator field as
compatible-but-unproven between "quest id / NPC id / list index") and tripped
`tests/test_npc_interaction_wire.py`'s repo-wide regex guard
(`test_no_foundation_module_implements_quest_or_shop_behavior`) that scans every
`src/pirateforce_foundation/*.py` file for whole-word `quest`/`shop`/`store5`/`price`/`reward`/
`trade` outside an explicit `ALLOWED_HITS` allowlist — `trace_path.py` wasn't in it. Fixed by
rewording ("a story-trigger id, an NPC id, a list index") rather than adding an allowlist
exception, since the module genuinely implements no quest logic. Adversary specifically also
tried and could not find: dispatch-chain shadowing (grepped the whole chain + legacy base module
for `0x4391`, only hit is the new branch), a `nested_id is None` false-match crash (`None ==
0x4391` is `False`, no crash), an off-by-one in the new test's manual re-parse of the trailing
derived-class mask byte, or a spam/amplification concern (reply only reachable post-select,
fixed tiny frame both ways).

New `tests/test_trace_path_wiring.py` (4 tests, drives `make_state_class` headless through the
real dispatcher, same style as `tests/test_mob_combat_cadence_wiring.py`): no reply with no
character selected (fail-closed); the reply is byte-identical to calling the builder directly
once a character is selected; the reply payload structurally re-parses to exactly one `u16`
tag `0x12`=0 record-count field and nothing else; repeated requests each get their own reply
independently.

Full suite: `3568 passed, 0 failed, 198 skipped, 23 errors` (same pre-existing
capstone/pefile/tools `ModuleNotFoundError` collection errors every prior round has reported,
not new) — เขียว(cloud sanity). `tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no
drift.

## Files touched (this repo, 3, one topic)

`src/pirateforce_foundation/runtime.py` (2 edit sites: one import line, one dispatch branch),
`src/pirateforce_foundation/trace_path.py` (new), `tests/test_trace_path_wiring.py` (new).

## What is not proven

- No waypoint/auto-walk behavior of any kind — deliberately out of scope; RE-119 T4 leaves the
  request's own discriminator field bounded negative and this round does not touch it.
- The `TRACE_PATH_VITAL_VERSION = 0` byte is an unproven default, not RE-pinned specifically for
  this vital.
- No attended/client-observable confirmation yet that the GO! button actually stops hanging in
  the real client — wire/DB layer only this round, per G5. Queuing a `GAME_TEST_QUEUE.md`
  attended entry this round (client-observable layer) since this is exactly the kind of fix that
  needs eyes on a screen, not just dispatcher tests, to close.
- `CORE-REQUEST-026` (bg0002 census arrival trigger, ex-024) reserved but not wired — see above.

## CORE-REQUEST

CORE-REQUEST-025 opened and closed same round. CORE-REQUEST-026 opened (renumbered from a
shadow-collided "024"), not closed — queued for next round.

## เปิดใบให้สาย C

none
