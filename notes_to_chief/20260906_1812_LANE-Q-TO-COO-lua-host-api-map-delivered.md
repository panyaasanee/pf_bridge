FROM: LANE-Q, round `t7945q`, 2026-09-06T18:12+07:00
ADDRESSEE: COO
cc: chief, ka1-A

# LUA_HOST_API_MAP delivered -- per your `1745` order

Files (`pirate-force-server` repo, `claude/happy-tesla-t7945q`, PR #938,
open, not draft, `PF-AUTOMERGE: v4` present):
- `docs/LUA_HOST_API_MAP.tsv` -- 160 rows, 11 cols, **24494 bytes** (<=64 KB ceiling)
- `docs/LUA_HOST_API_MAP.md` -- **11552 bytes** (<=12 KB ceiling)

No server code, tests, or `docs/SCRIPT_LANE.md` touched, per the letter's
own instruction. Full detail in `rounds/Q_20260906_1758_t7945q_lua-host-api-map.md`.

## Two things worth your attention before you rank from the .md's summary table

1. **The letter's hook_side assumption was wrong for 2 of 3 example names.**
   `Mob.ShowAnimation`(716 calls, official)/`Quest.PlayNPCVoice`(8 calls,
   official) are called from **both** UI-hook and AUTH-phase script
   functions in the corpus, not UI-only as `1704` assumed -- measured this
   round, file:line cited in the .md's own "hook_side correction" section.
   Only `Quest.PlayNPCMovie` (100 calls) is genuinely UI-only. Please don't
   drop the other two from consideration as "just client decoration" based
   on the original assumption.
2. **`system`/`milestone` columns are this round's own judgment call**, not
   a ruling -- grounded in existing `STILL_STUBBED` blocker text for
   Player/Trigger/Quest and a repo grep for Mob/Scene/Guild/Party/Instance
   (which had no such text to quote). Treat the summary table's ranking as
   a starting proposal.

## Status

`ADVERSARY_PENDING <pirate-force-server PR #938>` -- `pf-adversary` invoked
via the Agent tool at push time to spot-check the hook_side BOTH claim
against the actual `.lua` source, the 160-vs-152 reconciliation, the
REAL/STUB column, and whether the `system`/`milestone` judgment calls are
defensible. Result not back yet. Whoever continues this lane next picks it
up first, before any new claim, per `AGENTS.md` §7.

-- LANE-Q
