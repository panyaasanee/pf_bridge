FROM: LANE-Q, round `t7945q` addendum, 2026-09-06T18:18+07:00
ADDRESSEE: COO
cc: chief, ka1-A

# LUA_HOST_API_MAP: adversary result is back, fixed -- update your ranking if you already used the old table

Follow-up to `notes_to_chief/20260906_1812_LANE-Q-TO-COO-lua-host-api-map-delivered.md`
(sent while `pf-adversary` was still `PENDING`). Full detail:
`rounds/Q_20260906_1818_t7945q_adversary-fix.md`.

## The one finding that changes your ranking table

The `movie-ui (client-only)` row in the .md's summary table said "S / no-op+log
enough" -- but 2 of its 3 names (`Mob.ShowAnimation` 716 calls,
`Quest.PlayNPCVoice` 8 calls = 88% of that row's 824 calls) are actually
BOTH-hook (measured, verified again this round against the raw `.lua`
source), meaning they need a real AUTH-side wire, not a no-op. **If you
already read the old table as "movie-ui is small and solved," that was
wrong.** Fixed: those two moved into `message-wire`, which is now the
**4th-highest system by call volume (907 calls, size L)**, right after
`flag-quest-state`. `movie-ui (client-only)` now correctly shows only
`Quest.PlayNPCMovie` (100 calls, S, genuinely trivial).

Three more low-severity citation fixes (a wrong line number in one worked
example, `script_host.py:270`->`272`, and one nonclaims sentence that
understated its own method) -- none change any ranking, listed in the
round file for completeness.

## Status

Both files re-verified within their byte ceilings; `pirate-force-server`
PR `#938` updated with the fix (commit `874456b9`) and its body now
carries the full adversary-findings-and-fixes summary instead of
`ADVERSARY_PENDING`. Nothing further pending on this deliverable.

-- LANE-Q
