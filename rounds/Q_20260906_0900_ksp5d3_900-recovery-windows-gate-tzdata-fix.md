[LANE-Q round ksp5d3 | 2026-09-06T09:00+07:00 | claim: pf_bridge#1458]

# LANE-Q round ksp5d3 -- recovered pirate-force-server#900 (gate RED, not the lock this time), root-caused and fixed the Windows tzdata/ZoneInfo failure, pf-adversary reviewed and both its findings fixed

## What this round did, and what it moved on NOW.md

Lock check at round start: `grep`-equivalent search (GitHub search API,
`is:pr is:open in:title "LANE-Q round"` on `pf_bridge`) found zero open
`[LANE-Q] round *: claim` PRs -- lock free, no takeover needed. Mailbox
check (`grep -rl "ADDRESSEE: LANE-Q" notes_to_chief/*.md`, skipping any
with a `.CONSUMED.txt` stub) found exactly one unconsumed letter:
`notes_to_chief/20260906_0830_SYNC-NOTICE-pirate-force-server-pr900-closed-never-merged.md`.

That notice reports round `0rgg6q`'s own recovery PR
(`pirate-force-server#900`, which itself recovered `#874`'s
`Quest.CheckOpenTime` work after the one-open-claude-PR lock closed that
one) was ALSO closed -- this time by the gate going genuinely RED, not
the lock. Per the notice's own instructions ("fix that cause on the
branch above - do not start the round over"), read the gate log for the
failing commit (`https://github.com/panyaasanee/pirate-force-server/actions/runs/34003119697`)
rather than guessing: exactly one pytest failure,
`RealQuestNamespaceTests.test_default_clock_reads_the_bangkok_timezone`,
`ModuleNotFoundError: No module named 'tzdata'`, raised inside
`lua_api/quest.py`'s own `_server_clock()` -> `ZoneInfo("Asia/Bangkok")`
call.

Root cause: Windows' stdlib `zoneinfo` carries no system IANA tz
database (unlike Linux, which is why this passed in every prior round's
own cloud-clone run of the full suite -- not a flake, a real platform
gap), and this repo pins no dependency on the `tzdata` PyPI package that
would supply one there. Cherry-picked `#900`'s own two commits
(`e52220a`/`fb71ba5`) from the kept branch `claude/hopeful-hopper-0rgg6q`
onto current `main` (`31193e9`) -- clean, no conflicts (main had not
touched `Quest.*`/`Instance.*` since `#900` was cut) -- then fixed the
root cause as a third commit: `_server_clock()` now catches
`ZoneInfoNotFoundError` specifically (any other exception still
propagates) and falls back to a fixed-offset `timezone` for
`Asia/Bangkok` (UTC+7, no DST since 1920 -- verified against the IANA
`tz` database's own `asia` source file, not asserted from memory). Added
a regression test reproducing the failure on any platform (monkeypatches
`zoneinfo.ZoneInfo` itself) rather than relying on a Windows-only machine
to catch a regression here again, and a fourth commit documenting the
round in `docs/SCRIPT_LANE.md`.

`pf-adversary` (ordered at round start per house rule, ran in its own
isolated `git worktree` with `lupa` installed there only, executed the
tests rather than only reading the diff) returned before this round's
push with two real findings, both fixed in a fifth commit:

1. The fallback was keyed only on the exception type
   (`ZoneInfoNotFoundError`), not on which zone name failed to resolve --
   it would have silently reused Bangkok's UTC+7 offset for ANY future
   `SERVER_TIMEZONE_NAME` that also failed to resolve on a tzdata-less
   platform (e.g. a later move to `Asia/Tokyo`, UTC+9, deployed to the
   same Windows gate: 2 hours wrong, no error, no log line). Fixed: the
   fallback is now a small table of verified fixed-offset equivalents
   keyed by exact zone name; an unresolvable zone with no entry re-raises
   instead of guessing. Added a test proving the fail-loud path, and
   fixed the original regression test (which had pointed
   `SERVER_TIMEZONE_NAME` at an arbitrary bogus string) to monkeypatch
   `ZoneInfo` itself instead, since the zone name must now stay
   `"Asia/Bangkok"` to hit the fallback table at all.
2. `docs/SCRIPT_LANE.md`'s "Round vqng2z" narrative section (carried
   over verbatim from the original, gate-lock-closed `#874` branch)
   quoted `BASELINE_TOTAL_STUB_CALLS`/skip-pin numbers (5057->5055,
   19->20) that were correct for that round's own branch state at the
   time, but became stale once round `0rgg6q` rebased it onto a `main`
   where the parallel `Instance.*` round (`4fxvsq`) had already landed
   independently -- the numbers actually in force today (5018, pin 21)
   were already correct in the code and in `docs/PYTEST_SKIP_PINS.json`,
   only the narrative text was stale and self-contradictory against the
   very table at the top of the same file. Left the original measurement
   in place (this project's own house rule against silently rewriting a
   past round's measured record) and added a correction note explaining
   the drift rather than editing history to look consistent in hindsight.
   Also fixed an unrelated duplicated/garbled phrase in
   `PYTEST_SKIP_PINS.json`'s own note field from the same
   combine-two-rounds process.

Both findings verified fixed by re-running the targeted test modules and
the full suite again on the final commit before push (see Tests below).

This moves `NOW.md`'s M2 milestone line the same way round `0rgg6q`
already did (`Quest.CheckOpenTime` is not `Trigger.*`, but is this lane's
own charter queue item) -- this round does not change `Quest.CheckOpenTime`'s
`real` status, only fixes a portability bug that was silently blocking it
from ever landing on `main` at all. `NOW.md`'s own Q line (`Trigger.* 5/17 ·
Quest.* #874 -> 0510 · RE-273 · งานแรก = pin drift PR แยก (0550)`) is
stale versus the round history (pin drift and `#874` recovery are both
already done, in rounds `xltzkx` and `0rgg6q`) -- not this lane's file to
edit (`NOW.md` is Panya/COO-only per house rule), flagged here for chief's
own upkeep pass.

## Mailbox

One unconsumed letter, handled above: `notes_to_chief/20260906_0830_SYNC-NOTICE-pirate-force-server-pr900-closed-never-merged.md`.
Consumed here (copied to `consumed/`, `.CONSUMED.txt` stub placed next to
the original, original not deleted).

No other letters addressed to `LANE-Q` arrived this round (checked fresh
after merging `origin/main` in, immediately before writing this file).
No new `FROM_CHIEF_*_TO_ALL_*`/`_TO_ทุกสาย_*` broadcast newer than `R364`
(`20260906_0515`, already consumed by round `0rgg6q`) exists on `main` as
of this round's own merge (`ee59d60`).

## Tests + gates

- `PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_quest.py -q -rs`
  (no `lupa` in this clone), after the initial tzdata-fix commit:
  `14 passed, 3 skipped, 37 subtests passed`; after the adversary-fix
  commit (two new tests): `18 passed, 3 skipped, 37 subtests passed`.
- `PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_quest.py
  tests/test_script_host_spike.py tests/test_script_lua_corpus.py
  tests/test_script_lua_api_instance.py tests/test_script_lua_api_trigger.py
  tests/test_npc_interaction_wire.py -q -rs`, run in an isolated venv with
  `lupa==2.8` installed: `148 passed, 268 subtests passed` after the
  initial fix, `150 passed, 268 subtests passed` after the adversary-fix
  commit (matching the two new tests, zero skips with `lupa` present).
- Simulated the actual Windows failure directly on this Linux clone
  (monkeypatched `zoneinfo.ZoneInfo` to always raise
  `ZoneInfoNotFoundError`, since this clone's own `zoneinfo` resolves
  `Asia/Bangkok` from the Linux system tz database and cannot reproduce
  the bug by zone name alone): confirmed the fallback returns UTC+7 for
  `Asia/Bangkok` and re-raises for an unresolvable non-Bangkok zone
  (`Asia/Tokyo` in the test).
- Full suite, first commit (`f65a851`, the cherry-pick recovery alone),
  on `origin/main` `31193e9`: `12035 passed, 369 skipped, 23522 subtests
  passed in 494.11s`, exit 0.
- Full suite again, third commit (`7a7ec24`, after the initial tzdata
  fix, before the adversary-fix commit): `12078 passed, 327 skipped,
  23689 subtests passed in 476.30s`, exit 0.
- Full suite again, final commit (`eb48402`, after the adversary-fix
  commit), same base `31193e9`: `12079 passed, 327 skipped, 23689
  subtests passed in 484.79s`, exit 0.
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`:
  PREFLIGHT PASS on the final commit (cp874, no new skips, main already
  in branch, precondition census agrees, both branches on their assigned
  `claude/*` names, bridge files under ceiling, no manual scoreboard row
  touched).
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server
  --pr-body <file> --pr-stage final`: PREFLIGHT PASS, marker check PASS
  (exactly one bare `PF-AUTOMERGE: v4` line, nothing else mentions the
  token).
- pf-adversary: ran in an isolated worktree (own `git worktree`,
  `lupa`/`pytest`/`capstone`/`pefile` installed there only, uninstalled
  after, live checkout never written to -- only read via `Read`/`Grep`/
  `git diff`), executed the tests rather than only reading the diff.
  Two real findings, both fixed and re-verified above; also independently
  confirmed `ZoneInfo(...)` on both pure-Python and C-accelerated
  `zoneinfo` backends never lets a raw `ModuleNotFoundError` escape
  uncaught (always re-raised as `ZoneInfoNotFoundError`), and confirmed
  the "Bangkok fixed UTC+7 since 1920" claim against the IANA `tz`
  database's own `asia` source file. One cosmetic-only nit (a module
  docstring's "lupa hands every Lua number back as a float" claim is
  empirically false for `lupa==2.8`/Lua 5.5's integer subtype, but
  harmless since `_decode_hhmm` already accepts both) left as a follow-up,
  not fixed this round (no functional impact, named in Next round).

## ASCII

Code, commit messages, the PR body and this round file's own English
technical narrative are ASCII-only, verified (`python3 -c "..."` scan for
non-ASCII bytes on every touched file: `docs/SCRIPT_LANE.md`,
`docs/PYTEST_SKIP_PINS.json`, `src/pirateforce_foundation/lua_api/quest.py`,
`tests/test_script_lua_api_quest.py` -- zero non-ASCII bytes in each).
This round file is written in English (matching the source PRs and prior
Q round files' own convention for technical narrative), which
`prompts/COMMON_LANE_ROUND.md` permits (Thai is required for
letters/round files generally, English is what every prior LANE-Q round
file in this directory already uses for the technical body).

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/happy-tesla-ksp5d3`: five commits
  (cherry-pick recovery, tzdata fix, docs, adversary-fix, this round's
  final state is the adversary-fix commit `eb48402` since the docs commit
  landed before it) -- PR `#904`, open, not draft, `PF-AUTOMERGE: v4`
  present from open, verified via GET after creation
  (`mergeable_state: unstable` is GitHub's own pending-check state, not a
  conflict -- `head.sha` matches the last commit pushed).
- `pf_bridge` branch `claude/gracious-lovelace-ksp5d3`: this round file +
  mailbox consumption stub -- claim PR `#1458`.

## `TWO_SESSIONS_SAME_SCENE:`

N/A -- no shared-world/scene state touched. `Quest.CheckOpenTime` reads a
clock and returns a bool; the fix changes which timezone object backs
that clock on a platform without an IANA database, nothing else.

## nonclaims

1. Does not claim `pirate-force-server#904` is merged -- only that it is
   open, not draft, gate-preflight-passed, with the full suite green on
   the final commit tested three times across the round (cherry-pick
   alone, after the tzdata fix, after the adversary-fix). Landing on
   `main` is next round's job to confirm
   (`git merge-base --is-ancestor`).
2. Does not claim the Windows gate itself will be green on `#904`'s
   commit -- out of scope for this cloud clone; the preflight tool
   explicitly does not promise that. Claims only that the one specific,
   named failure from run `34003119697` has its root cause fixed and
   covered by a test that reproduces it on any platform, including this
   one.
3. Does not implement `Quest.GetWeekDay` or any other `Quest.*` name --
   `GetWeekDay` stays RE-blocked (undocumented weekday enum), the
   remaining 23 need LANE-DB's per-character state door, neither changed
   this round.
4. Does not add the `tzdata` PyPI package as a dependency -- the
   fixed-offset fallback makes that unnecessary for this one name; left
   as an open question for a future round if more timezone-sensitive code
   is ever added (named in `docs/SCRIPT_LANE.md`'s own round section).
5. Does not touch `runtime.py`/`app.py`/`store.py`, any other lane's
   write zone, `GAME_TEST_QUEUE.md`, or `CHIEF_CONTINUATION.md`. No new
   CORE-REQUEST opened this round.
6. Does not claim `RE-273` (trigger-id -> `.lua` file mapping,
   `GetContactMode`'s own blocker) is answered -- still `OPEN` in
   `CLIENT_RE_QUEUE.md` as of this round's own check, unrelated to this
   round's work either way.
7. Does not fix the cosmetic "lupa hands every number back as a float"
   docstring inaccuracy pf-adversary noted -- named as a follow-up, not
   silently dropped (no functional impact, confirmed by adversary's own
   testing).

## Next round

1. Confirm `pirate-force-server#904` landed on `main`
   (`git merge-base --is-ancestor <sha> origin/main`) before anything
   else; if it was closed again (gate RED for a DIFFERENT reason, or the
   lock), read that gate log fresh rather than assume this round's fix
   was insufficient for an unrelated failure.
2. `RE-273` (trigger-id -> `.lua` file mapping, `GetContactMode`'s own
   blocker) is still the one remaining named blocker of this lane's
   charter milestone ("ผู้เทสแล่นเรือชนทริกเกอร์แล้วสคริปต์ทำงาน") --
   check its status fresh in `CLIENT_RE_QUEUE.md`; if still `OPEN`,
   nothing to do but wait for an RE runner. If answered, re-read
   `notes_to_chief/consumed/20260906_0727_LANE-A-TO-LANE-Q-*.md` first
   (already consumed by round `0rgg6q`, names the live hook point
   `lane_hooks.hook("vital_inbound_trigger_vital")`, the trigger-id
   payload reader `first_tag_value`, and three world-registry footguns)
   before writing `Trigger.GetContactMode`.
3. Small, optional cleanup named by pf-adversary this round: correct
   `lua_api/quest.py`'s module docstring claim that "lupa hands every Lua
   number back as a float" -- empirically false for `lupa==2.8`/Lua 5.5's
   integer subtype (a Lua integer literal comes back as a Python `int`),
   though harmless since `_decode_hhmm` already accepts both `int` and
   whole-number `float`. No test or behavior change needed, doc-only.
4. If both of the above stay blocked: per the backup-work rule, audit the
   remaining stub surface (72 `Player.*` + `Guild.*`/`Party.*` low-call
   names) for another pure-function candidate needing neither the
   LANE-DB state door nor a wire frame this lane does not own, the same
   shape `CheckOpenTime` itself was.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ (Quest.CheckOpenTime ยังไม่มี live quest-accept flow เรียกมันจริงในเซิร์ฟเวอร์) แต่ code ที่เคยตกรถสองรอบติดกัน (ล็อกครั้งแรกที่ #874 แล้วเกต RED จริงที่ #900) ตอนนี้แก้ต้นตอ (Windows ไม่มี tzdata สำหรับ ZoneInfo) แล้วขึ้น PR ใหม่ #904 ผ่านทั้ง unit test เฉพาะจุด, ชุดเต็ม 12079 ผ่าน 0 ล้ม, และ pf-adversary ยืนยันตรวจจริง (ติดตั้ง lupa รันจริง) พบ 2 จุดจริง (silent-wrong-zone fallback, เอกสารเลขค้างจากรอบก่อน) แก้ครบก่อน push | pirate-force-server#904 (ห้าคอมมิต, full suite green x3), pf_bridge claim #1458
