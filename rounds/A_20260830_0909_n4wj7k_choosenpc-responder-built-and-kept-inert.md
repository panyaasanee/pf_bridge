# LANE-A round n4wj7k

Opened 2026-08-30T08:30+07:00, closed 2026-08-30T09:09+07:00.
Lock: pf_bridge#469 / pirate-force-server#295.

Player-visible change: none yet, on purpose. Scene 14's 81 NPCs still render
but stay unclickable, exactly as round R235 left them.

## What this round did

1. Consumed mailbox items addressed to this lane: `20260830_0817`
   (COO-DECISION, no action needed on the door-reader-precedence question
   this round) and `20260830_0030` (attended shift's GT-131 PASS / GT-151
   PARTIAL results). Updated both ticket headers in `GAME_TEST_QUEUE.md`
   (struck the old status, did not delete it). Answered the owner's question
   about the mob-to-npc identity swap at the yellow-ship pier with static
   evidence already committed in `pirate-force-server` (the legacy Mob-Set
   migration window `COO-DECISION 20260829_0041` closing, not a cross-scene
   roster leak) -- one point left unconfirmed and flagged rather than
   asserted (a placement-index mismatch between two tables, 58 vs 60).

2. Built the `ChooseNPC` responder for roster scenes that `COO-DECISION
   20260830_0818` assigned this lane: a registry in `lane_hooks/__init__.py`
   mirroring the existing census-composer registry, the scene-14 responder
   itself (`lane_hooks/lane_a_choose_npc_scene14.py`), and the wiring in
   `lane_a_scene_census.py` so a scene's census gets real membership only
   when a responder is both registered and `production_allowed` for that
   scene -- withhold stands unchanged for every scene with no responder.

3. `production_allowed = False` on the new responder, on purpose. Nothing in
   `runtime.py`'s `dispatch()` routes `ChooseNPC` through it yet, and a real
   click today would hit one of the 16 (of scene 14's 81) placement indices
   missing from the frozen client's own `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS`
   table and raise an uncaught `KeyError`, dropping the connection. A test
   (`TheCrashThisModuleGuardsAgainstTests`) forces the gate open and measures
   this crash live on the real dispatcher, so the hazard is pinned rather
   than described.

## pf-adversary

Ran in an isolated worktree before commit (the live checkout was never
mutated). No defects found; every factual claim in the handback was
independently re-derived from source rather than taken on report (the
`runtime.py:6644` dispatch path, the `v141:1093` KeyError site, the 16/81
and 65/81 counts, cp874-encodability, scope). Full suite green (5487 tests
at adversary's pre-merge check; 5336 passed + 212 skipped after this lane
merged main's own PR #296 on top, same 17 pre-existing `capstone`-import
collection errors unrelated to this change).

One partial-compliance note raised, for chief/COO judgment rather than
fixed silently: COO-DECISION 20260830_0818 asked for tests that drive the
real dispatcher both ways, including "responder present -> actually
clickable." What shipped drives the real dispatcher for the
census/arming half; the actual click test calls the responder's `respond()`
directly rather than `state.dispatch()`, because the real dispatcher click
still crashes today (see above) pending the CORE-REQUEST below. Disclosed
in the module docstring, the test docstring, and this letter -- not spun as
done.

## CORE-REQUEST for chief

In `runtime.py`'s `dispatch()`, before the frozen `super().dispatch(parsed)`
call (currently `runtime.py:6644`), add a guard for
`CHOOSE_NPC`/`TARGET_VITAL`: when `population_indices` is armed for a scene
with a registered `lane_hooks.scene_choose_npc_responder(scene_id)`, route
through that responder instead of letting the frozen path run over indices
its own table does not have. Once that lands, this lane's one-line
follow-up is flipping `lane_a_choose_npc_scene14.production_allowed` to
`True` -- nothing else moves.

## What was not done

Did not touch `runtime.py` or `app.py`. Did not touch the frozen
`current/pf_login_game_server_v141.py`. Did not widen the responder to any
scene besides 14. Did not flip `production_allowed` to `True` -- that is
gated on the CORE-REQUEST above landing.
