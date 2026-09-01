# R207 (confident-ride-sf9kel / jolly-mccarthy-sf9kel) — CORE-REQUEST-026: bg0002 census on arrival

2026-08-28 ~06:1x (+07:00)

## §2 item 7 (previous round fate check)

Confirmed via single-PR GET (list endpoint's `merged` field is unreliable — returned `false`
for both, `get` returned `true`): `pf_bridge#271` / `pirate-force-server#173` (R206) both
`merged: true`. R206's work is on `main`; no cherry-pick recovery needed.

Note for future rounds: `mcp__github__list_pull_requests`'s `merged` field cannot be trusted —
it read `false` for ~30 recently-closed PRs across both repos, including R204/R205/R206, all of
which are actually merged per `pull_request_read` (method `get`). Always confirm with a
single-PR GET before concluding a round's PR did not merge.

## §17 item 3 (CORE-REQUEST check, done first)

Registry review (`CHIEF_CONTINUATION.md` rows 001-025) found exactly one actionable, unblocked
CORE-REQUEST: row 026 (LANE-A, bg0002 census arrival trigger), explicitly deferred by R206 under
the one-topic-per-PR rule. 011/012 remain blocked (no `GmCommand` decode from 0x51E9 yet). 015
remains blocked (no pickup-request opcode decoder). 013 stays superseded/moot. Everything else
already wired. No new mailbox letters addressed to chief arrived since R206 that name a fresh,
unblocked CORE-REQUEST.

## What changed (pirate-force-server)

`runtime.py`'s WORLD-CENSUS-001 block (`5637-5690`, `scene_id == world_population_bg0002.SCENE2_N_ID`
branch only): the outer guard previously required `self.last_target_pos is not None` for every
scene, including bg0002 — meaning Prison Exile Island stayed empty until the player pressed a
movement key (M1-P's own attended-test gap). For bg0002 only, the census now fires as soon as
`teleport_sent and runtime_ack_sent` are true (arrival), falling back to
`world_scene_travel.spawn_position(world_scene_travel.destination(scene_id, scene_entry_registry))`
as the anchor when `last_target_pos` is still `None`. A real `TargetPosVital` that arrives first
still wins as the anchor, unchanged. bg0001's branch is untouched — it still requires
`last_target_pos is not None` in every code path (confirmed structurally and with a new control
test).

**pf-adversary caught one real defect before push**: the first draft's anchor-lookup failure
handler assumed the registry read was a "transient" failure worth retrying on the next poll.
It is not — `scene_entry_registry` is loaded exactly once at boot (`make_state_class`) and never
reloaded, so a missing/unpinned bg0002 spawn is a deterministic, permanent fact for the rest of
the process's life. Left as "retry," a real occurrence would re-raise and re-log an identical
failure on every `RuntimeProtocolReq` poll for the whole session — an unbounded event/console
flood, and the census would silently never populate. Fixed to latch (`world_census_refused = True`)
exactly like the sibling population-build refusal a few lines below it in the same branch.

pf-adversary also flagged one pre-existing, out-of-scope issue (not introduced by this round,
not fixed this round): `runtime.py:5733-5737`'s `world_scene_travel.destination()` call in the
same branch (the `WORLD_SCENE` console-line print) has no `try/except`, unlike the new fallback.
If the registry breaks after boot, that line still raises uncaught. Proposed as a backfill item
for a round with time — see `CHIEF_CONTINUATION.md` row 026's own note.

## Tests

`tests/test_bg0002_census_wiring.py`, 4 new tests (12 total in file, all passing), driving the
real dispatcher (`state.dispatch(...)`, not calling internal functions directly):

- `test_the_scene2_census_arrives_with_no_target_pos_vital_ever_sent` — an empty runtime poll
  (`vital_count == 0`, the same constant proven elsewhere in the suite) right after login fires
  the full 97-actor census, anchored on the scene's pinned spawn, with `last_target_pos` still
  `None`.
- `test_a_late_target_pos_vital_still_wins_as_the_anchor` — a real `TargetPosVital` still anchors
  the census when it does arrive.
- `test_an_unpinned_arrival_anchor_latches_a_refusal_not_a_retry_loop` — the adversary-found fix:
  a failed registry lookup latches `world_census_refused`, logs one event, and a later poll (even
  with the failure cleared) does not retry.
- `test_scene1_still_waits_for_a_target_pos_vital_unlike_scene2` — control: an ordinary scene-1
  boot sends nothing on an empty poll, exactly as before this round.

Full suite: `3582 passed, 0 failed, 198 skipped, 23 errors` (same pre-existing capstone/pefile/
tools `ModuleNotFoundError` collection errors every prior round has reported, not new),
เขียว(cloud sanity). `tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no drift.

## Files touched

**pirate-force-server** (2, one topic): `src/pirateforce_foundation/runtime.py`,
`tests/test_bg0002_census_wiring.py`.

**pf_bridge** (this repo, doc/mailbox only): `CHIEF_CONTINUATION.md` (row 026 + round index line),
`GAME_TEST_QUEUE.md` (see below), 2 mailbox `.CONSUMED.txt` stubs + 2 `consumed/` copies, this
round file, `notes_to_chief/FROM_CHIEF_R207_TO_ATTENDED_*.md`.

## What is not proven

- Not reachable on any boot today: no seed path exists for a stored character row that names
  `scene_id=2` (same handback as CORE-REQUEST-021/row 021 — chief's own open item, still not
  started).
- No attended/client-observable confirmation that arrival-trigger census actually populates the
  scene on a real client — blocked on the same seed-path gap above, not opened as a new GT entry
  (would be untestable until seeding exists).
- `CHIEF_CONTINUATION.md` is still over the 30KB cap (pre-existing debt since R204, deliberately
  not touched further this round to keep this PR single-topic, per `PANYA-ORDER 1230` item 2).
- The pre-existing unguarded `world_scene_travel.destination()` call at `runtime.py:5733-5737`
  (see above) is not fixed this round — flagged, not this CORE-REQUEST's scope.

## CORE-REQUEST

CORE-REQUEST-026 opened (as a renumber of the shadow-collided "024") and closed this round.

## เปิดใบให้สาย C

none

Companion PR: `pirate-force-server` (the actual wiring + tests, full detail above).
