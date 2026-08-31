# LANE-A round fx0007

2026-08-31T17:29+07:00 - 2026-08-31T17:45+07:00 (approx).

## Step A / B (mandatory, start of round)

Both repos' most recent `[LANE-A]` PR (`pf_bridge#609`, `pirate-force-server#394`)
already `merged=true` at HEAD - nothing to recover. No unconsumed
`ADDRESSEE: LANE-A` mail found. Heartbeat 5 minutes stale, under threshold.
No open `[LANE-A]` PR (614/399 are `[LANE-B]`). Placed a claim before
starting (`notes_to_chief/20260831_1729_CLAIM-LANE-A-round-fx0007-bg0006-ocean-walled-city.md`),
re-checked `origin/main` unchanged after.

## What this round did

Built the fourth door in the multi-round sequence `COO-DECISION
2026-08-30T14:41+07:00` approved: scene 6, Bg0006 ("Ocean Walled City"), 80
native placements, the highest of the seven still shut when this round
started (3, 6, 7, 8, 9, 11, 130). Full account, numbers and adversary pass
are in the server repo's own round file (see links below) - this bridge-side
file only carries the bridge-visible deltas: the new GT ticket and RE
ticket, and this round's claim/consume.

Same compressed build+wire+open-in-one-pass shape round `l03cgh` used for
scene 5, for the identical reason: the generic contract test
(`tests/test_lane_a_scene_census.py::ComposerContractTests`) already
assumed every scene this lane composes for is also open at login, since
scenes 4/5/10/14 all were by the time this round started.

**One new failure shape this scene needed that no sibling scene did**:
three resolved-in-MOBS leaders (939, 940, 941) whose `MOBS_TIP.s_NAME` is
CJK script (`海皇城寨傳送員`) that `cp874` cannot encode. Dropped
fail-closed rather than shipped mis-encoded, same principle as an empty
`s_OUTFIT`; opened to lane C (`RE-171`) rather than guessed at.

## Numbers measured this round

Placements: 80 total, 66 shippable, 14 unshippable (2 no-MOBS-row + 9
empty-outfit + 3 non-ASCII-name). Full test suite (server repo):
5791 passed, 327 skipped, 11136 subtests, 0 failed (up from 5742/327/10708
at round `l03cgh`'s own close). `runtime.py`/`app.py`/
`current/pf_login_game_server_v141.py`: untouched.

## Player-visible claim

A character whose own persisted row names scene 6, or a GM `/warp 6`, now
lands on Ocean Walled City and sees up to 66 of its 80 native placements
instead of being refused at login. No ordinary player's stored row can name
scene 6 today (no production path writes one), so this reaches only a
staged GM account or a hand-edited config. Reversible in exactly one
boolean.

## Tickets opened

- `GT-173 OCEAN-WALLED-CITY-FIRST-EYES-001` (`GAME_TEST_QUEUE.md`), same
  shape as `GT-171`/`GT-165`.
- `RE-171 BG0006-CJK-TELEPORTER-NAME-001` (`CLIENT_RE_QUEUE.md`): does an
  ASCII/Thai alternate name exist for leaders 939/940/941 in a table this
  round did not open?

## Claim consumed

`notes_to_chief/20260831_1729_CLAIM-LANE-A-round-fx0007-bg0006-ocean-walled-city.md`
moved to `notes_to_chief/consumed/` this round, with a `.CONSUMED.txt` stub
left in its place.

## CORE-REQUEST

None this round.

## ASK-COO

None this round. Continuing the already-approved door sequence.
