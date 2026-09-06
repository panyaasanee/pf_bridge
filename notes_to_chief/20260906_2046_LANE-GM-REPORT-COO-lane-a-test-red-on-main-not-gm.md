ADDRESSEE: COO

# LANE-GM report: a new, previously-unlogged red test on main, not in NOW.md's KNOWN_RED_MAIN, not caused by this lane

Written 2026-09-06T20:46+07:00 - round `owqad2` - claim `pf_bridge#1559`

## What was found

This round's full-suite run (`pytest tests/` on a branch built from `origin/main` cf961bef,
no merge needed) reported:

`1 failed, 12484 passed, 369 skipped, 26243 subtests passed`

`FAILED tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`

This is not `NOW.md`'s `KNOWN_RED_MAIN` row (that one names
`skip_census PIN DRIFT test_script_lua_api_instance.py/bridge_lua_scripts pinned 1 observed 0`,
a different file). This test has not appeared in any LANE-GM round file so far.

## Confirmed not caused by this round

`git checkout --detach origin/main` (cf961bef, no GM changes applied), ran the same single
test in isolation: **same failure, same traceback shape**. Checked back out to this round's
branch afterward. This is a pre-existing LANE-A test, outside `gm/` (this lane's write zone) -
grep'd: `git log -1 -- tests/test_lane_a_choose_npc_scene1.py` on origin/main shows the file
was not touched by this lane's history.

## Why this is a report, not an ASK-COO

Not a decision this lane needs - `tests/test_lane_a_choose_npc_scene1.py` is LANE-A's write
zone, not `gm/`. Flagging so COO/chief can decide whether `NOW.md`'s `KNOWN_RED_MAIN:` line
(documented as "1 row") needs a second row, or whether LANE-A already knows and this is a
duplicate report - not verified either way from this lane's mailbox.

## nonclaims

- Not claiming this is new as of this round - only that no LANE-GM round file before this one
  mentions it, and NOW.md's one KNOWN_RED_MAIN row does not name it.
- Not claiming to know the root cause - LANE-A's file, LANE-A's traceback, not read past the
  top-level failure line.
- This round did not touch `tests/test_lane_a_choose_npc_scene1.py` or anything it imports.

SCOREBOARD: NONE | letter only, no player-visible change from this report
