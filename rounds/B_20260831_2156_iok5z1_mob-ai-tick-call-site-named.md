# LANE-B round `iok5z1` (COMBAT) -- bridge-side mirror

Full detail lives in `pirate-force-server`'s
`rounds/B_20260831_2156_iok5z1_mob-ai-tick-call-site-named.md` (that repo is
where the code changed this round). This file is the short mirror the
bridge repo's own history expects for every round.

## Player-visible change

None yet -- see the server-repo round file's own "Player-visible change"
section for the full reasoning.

## Summary

Round `256rvs` (2026-08-31T18:50) built `mob_ai_scheduler.tick_session`
(a caller for `mob_ai_control.tick_step`, which had zero production callers
since round `3lzfhw`) but deliberately left the exact `runtime.py` call site
unnamed, not knowing which existing dispatch point runs live or where a
real player identity number comes from. This round answered both by
reading two EXISTING production call sites in `runtime.py`
(`dispatch(self, parsed)` ~line 5164, and the `performer` identity formula
already used at ~line 4142 and ~line 6728), and built
`src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py` -- the
option-(b) direct-call wrapper (no `runtime.py` edit; that stays chief's,
see this round's CORE-REQUEST letter) with a console-spam guard (prints
only rows that actually changed phase, pinned by a test against a real
17-row Bg0002 register) and its own exact wiring text
(`LANE_B_MOB_AI_TICK_WIRING`).

Also fixed a containment-test blind spot found while building this:
`tests/test_mob_ai_scheduler.py`'s "no importer yet" check only ever
scanned the flat top level of `src/pirateforce_foundation/`, never the
`lane_hooks/` subpackage where this round's new file lives -- widened to a
recursive scan so the claim stays honest.

## Numbers

```
tests/test_lane_b_mob_ai_tick.py : new, 9 tests, all pass
Full suite (pirate-force-server), before/after via git stash:
  before: 0 failed, 5874 passed, 387 skipped, 11981 subtests (122.66s)
  after:  0 failed, 5883 passed, 387 skipped, 11981 subtests (124.64s)
  delta: +9 passed exactly, nothing else moved
```

## Letters this round

- `notes_to_chief/20260831_2156_LANE-B-STATUS-mob-ai-tick-hook-built-call-
  site-named-core-request.md` -- CORE-REQUEST to chief with the exact
  block, ADDRESSEE: chief.

## nonclaim

Did not touch `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`.
Did not touch `scenarios/world_*.json`. No new on-screen milestone claimed.

-- LANE-B (COMBAT) round `iok5z1`
