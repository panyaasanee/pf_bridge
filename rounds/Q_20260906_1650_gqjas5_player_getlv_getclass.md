# LANE-Q round `gqjas5` (2026-09-06T16:50+07:00) -- Player.GetLv/GetClass, the first 2 of 73 Player.* names, real

## Round-start checks (prompts/COMMON_LANE_ROUND.md order)

1. **NOW.md**: read fresh (fetched origin/main first). Nothing overrides
   this lane's charter queue at round start. Bridge silent since 13:48
   (Panya's machine off) does not block this lane -- static-on-bridge work
   only.
2. **Lock**: listed open PRs in pf_bridge titled `[LANE-Q] round *: claim`
   -- zero. Claimed via PR `#1525` (branch `claude/kind-albattani-gqjas5`,
   this session's own harness-assigned branch -- the deviation round
   `gk0dz4` first recorded still applies: this session's two branches are
   fixed by the harness, not freely chosen `claude/*` names, so the claim
   branch and this round's own final branch are the same one, per
   COMMON's own "push the final round file to the same branch as the
   claim" step). Listed again immediately after opening `#1525`: no other
   `[LANE-Q]` claim appeared.
3. **Mailbox**: `grep -l "ADDRESSEE: LANE-Q" notes_to_chief/*.md`, skipping
   any with a `.CONSUMED.txt` stub -- zero unconsumed letters with LANE-Q
   as primary addressee. `FROM_CHIEF_R370_TO_ALL_20260906_1456.md` read
   (already consumed by an earlier lane; per the "known gap" in
   `notes_to_chief/README.md`, a second reader records its own
   consumption rather than re-stubbing) -- item 1 (reaper's two new
   auto-close rules) noted, no LANE-Q-specific action; items 2-5 name
   LANE-GM/LANE-UI/LANE-A/LANE-B/LANE-K, not this lane.
4. **AGENTS.md SS7**: re-read fresh. Nothing new since round `bxly5p`'s own
   reading that changes this lane's write zone or queue.
5. **Last round file** (`rounds/Q_20260906_1503_bxly5p_...md`)'s own "next
   round" list: item 1 (run pf-adversary on branch
   `claude/happy-tesla-bxly5p` for PR `#928`) and item 2 (check `#928`'s
   gate) are moot -- `#928` merged at `2026-09-06T08:51:22Z` (confirmed
   via the GitHub API), before this round started. Item 3 (check whether
   chief landed the LANE-DB whitelist for
   `persistence_quest_state`/`character_quest_state`) -- re-checked fresh:
   `grep -rln "persistence_quest_state\|character_quest_state" src/` on
   current `main` finds only this project's own docstring text quoting
   that exact grep command (in `lua_api/quest.py`'s module docstring), not
   a real module; `migrations/` now ends at `015_character_equipment.sql`,
   still no quest-state migration. **Still blocked.** Item 4 (RE-273's
   crosswalk) -- re-checked fresh in `CLIENT_RE_QUEUE.md`: still `OPEN`,
   still needs an attended capture from the bridge machine, which `NOW.md`
   says has been off since 13:48. **Still blocked.**

## Why this round did not touch `Trigger.*`/`Quest.*`

Both of this lane's own two named charter blockers are external and both
were re-confirmed still closed above, same as every round since `4jsydv`.
Per `AGENTS.md` SS7's backup-work order and this lane's own charter
("งานสำรอง" item 1): implement the next stub-table name that needs neither
another lane nor the LANE-DB door, highest call count first -- this round
read every one of `Player`'s 73 names (`api_spec.tsv`'s own call-count
column) looking for that shape.

## What this round built: `Player.GetLv`/`Player.GetClass` real

`GetLv` (91 call sites, 89 files) and `GetClass` (60 call sites, 14 files)
are the only two `Player.*` names of the whole 73 with `arity_min=arity_max=0`
in `api_spec.tsv` -- grepped across the real corpus (e.g.
`gamedata/lua/Quest/q_day_watch.lua:13`,
`Player.GetLv() <= (Quest.Var4)`), every call site invokes them with zero
arguments, which only makes sense as "the level/class of the player
running this script" -- a value the calling convention supplies
implicitly, the same shape `Quest.CheckOpenTime` already established for a
name needing no argument-side state.

`model.Character` (this repository's own row-backed player record) already
carries exactly that pair -- `level: int | None`, `class_id: int | None`,
filled in by `session.py` from the login-vitals seam
(`COO-DECISION 20260903_0647` for level/HP, `COO-DECISION 20260904_0446`
point 3 for class) -- the same fields `world_m2_arrival.level_refusal()`
already reads a character's level off of elsewhere in this codebase. No
new state, no new LANE-DB column, no other lane's write zone touched:
this round only adds a per-invocation `PlayerContext` seam
(`lua_api/player.py`) a future real dispatcher will fill from that
existing `Character`, the same shape `lua_api.trigger.TriggerContext`/
`lua_api.instance.InstanceContext` already established for their own
namespaces.

**Player-visible right now: nothing** (same honest posture round `bxly5p`'s
own plumbing PR took) -- there is still no live dispatch point that loads
a real `.lua` file against a real session's `PlayerContext`;
`DEFAULT_CONTEXT` reads the same fixed constants
(`player_wire.PLAYER_LOGIN_LEVEL`/`PLAYER_LOGIN_CLASS_ID`) every fresh
login already composes today, openly labelled as such in the module
docstring.

The remaining 71 `Player.*` names are catalogued in `lua_api/player.py`'s
own `STILL_STUBBED` dict, one of eight grouped, grep-grounded reasons each
(item/equipment state, a stat-grant write seam, other per-character stat
reads this lane's `PlayerContext` does not carry yet, skill/buff state
cross-lane with combat, a teleport/vehicle/camera wire frame, a
UI/cutscene/message wire frame, the instance-entry frame, and `MobAppear`
itself, which LANE-A's own letter (`20260906_0727`) names explicitly as
not servable yet).

## A finding this round made along the way: this cloud session actually HAS `lupa`

Every prior LANE-Q round recorded `lupa` as absent from the cloud clone and
ran the corpus/Lua-integration test classes skipped. Nobody had tried
`pip install lupa` here before -- it installs cleanly (a manylinux wheel
exists for this interpreter) and the full corpus test suite
(`tests/test_script_lua_corpus.py`, guarded by `LUA_CORPUS_RUNNABLE` =
`BRIDGE_LUA_SCRIPTS` AND `LUPA_PACKAGE`, both present in this session:
pf_bridge cloned as a sibling, lupa pip-installed) ran for real against
the actual 616-file corpus. This let this round MEASURE, rather than
guess, `BASELINE_TOTAL_STUB_CALLS`'s new pinned value after
`GetLv`/`GetClass` went real: 5018 -> 4937 (not 5018 - (91+60) --
`report.real_call_counts` shows `{'Player.GetLv': 60, 'Player.GetClass':
42}`, and giving these two names a real nonzero answer instead of
`STUB_DEFAULT` changes which branches some scripts take afterward, which
changes which OTHER still-stubbed names execute -- the same kind of
measured, non-additive shift `Quest.CheckOpenTime`'s own
9-call-sites-but-only-2-execute finding already established as normal
here, not a discrepancy to chase down). `docs/PYTEST_SKIP_PINS.json`
updated to match (one existing entry's count 21->22 plus one new entry),
verified against `tests/test_pytest_precondition_census.py`'s own AST
walker, not counted by hand.

This does not change anything about the Windows gate (which per
`COO-DECISION 20260905_2246`/round `ksp5d3`'s own fix already runs with
lupa installed via its pip line) -- it only means this lane's OWN cloud
rounds no longer need to guess at or skip the corpus-dependent pins; a
future round can measure them directly instead of estimating or writing
`ADVERSARY_UNAVAILABLE`/"no lupa" from habit.

## Tests + gates

- New file alone: 15 passed (12 namespace-level, no lupa needed; 3
  `RealPlayerLuaIntegrationTests`, needing lupa, all ran and passed for
  real this round rather than skipping).
- `tests/test_script_host_spike.py` (widened stub-reachability exclusion +
  new `test_the_2_real_player_names_are_excluded_above_not_forgotten`
  regression guard, the same shape the Trigger/Instance/Quest guards
  already use): green.
- `tests/test_script_lua_corpus.py` (re-measured pin, 5018 -> 4937): was
  RED (`4937 != 5018`) before the update, confirming the old pin was
  genuinely stale and the new one is measured, not asserted; green after.
- `tests/test_pytest_precondition_census.py`: was RED (pin/AST-walker
  name-list mismatch) before updating `docs/PYTEST_SKIP_PINS.json`; green
  after.
- `PYTHONPATH=src python3 -m pirateforce_foundation.gm.lane_gate_name_audit`:
  exit 0, clean.
- `git merge origin/main` into the branch as the final step (main moved
  once mid-round, LANE-E's runtime.py wiring + LANE-UI's addendum, zero
  file overlap with this round's seven touched files) -- clean merge, no
  conflicts.
- Full suite, run ONCE on the final merged tree per COMMON's own rule:
  `PYTHONPATH=src:tests python3 -m pytest tests/ -q -rs` ->
  **12461 passed, 327 skipped, 26384 subtests passed, 0 failed** (593 s).
  (An earlier run on the PRE-merge tree showed 1 failure in
  `test_world_scene_registry.py::TheWiringAsk`, checking for anchors
  LANE-E's own `runtime.py` wiring commit added on `main` after this
  branch's fork point -- confirmed fixed by the merge, not by anything
  this round's own diff touched, before treating the suite as green.)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`
  on the final merged tree of both repos: **PREFLIGHT PASS** (cp874, no
  new skips, main-in-branch, census agrees, both branches
  `claude/*`-named, bridge files under ceiling, no manual scoreboard row
  touched).

## ADVERSARY

`pf-adversary` invoked at the point the code was written (worktree-isolated,
per `AGENTS.md` SS7's rule), well before push -- available and ran to
completion this round, unlike several recent rounds' `ADVERSARY_UNAVAILABLE`.

**Result: safe to push, code/tests sound, two concrete documentation
defects found and fixed in this round's own commit before push:**
1. A new test's own comment/docstring cited the wrong Lua function name
   for a real gate (`gamedata/lua/Quest/q_day_watch.lua` line 13 is inside
   `Accept_Check()`, not `Report_Check()` as first written -- the line
   number was right, the function name was not). Fixed: renamed the test
   to `test_the_real_q_day_watch_accept_check_gate_is_real_now`, corrected
   the comment, and updated `docs/PYTEST_SKIP_PINS.json`'s matching test
   name.
2. An illustrative docstring comment in `tests/test_script_lua_corpus.py`
   had an arithmetic typo (`5018 - (91+60) = 4866`, should be `4867`) --
   the real pinned number (4937) and the measured delta (81) were both
   independently correct; only the "what the naive wrong answer would
   look like" illustration was off by one. Fixed.

Independently reproduced, in an isolated worktree with the real corpus and
lupa: the 73/71/2 name accounting exactly, the arity claims, the aggregate
143/160-stub/17/160-real table numbers, `BASELINE_TOTAL_STUB_CALLS=4937`
and its `real_call_counts` breakdown, both `PYTEST_SKIP_PINS.json` entries
against the actual AST walker, and that both new regression guards are
load-bearing (reverting either reproduces a real, clean failure). Fuzzed
`GetLv`/`GetClass` through a live `ScriptHost` with wrong-arity/`nil`/
string/extra-arg calls -- all degrade to `STUB_DEFAULT` and log, never
raise; confirmed `attribute_filter=deny_every_attribute` closes attribute
walk-out at the runtime level even though `PlayerContext` itself is never
handed to Lua (only plain ints via closures). Spot-checked 10+
`STILL_STUBBED` category assignments against the real corpus -- all
reasonable; one (`GetBoatHealth`/`BoatHealth` filed under the vehicle
bucket rather than a stat-read bucket) noted as a mild imprecision, not a
wrong classification, not blocking.

## `TWO_SESSIONS_SAME_SCENE:`

N/A -- this round's diff touches only the Lua-API namespace layer
(`lua_api/player.py`, `script_host.py`'s namespace wiring) and its own
tests/docs/pins. No process-shared world/runtime state
(`world_scene_registry`, `mob_ground_persistence`, `mob_death_persistence`,
or any registry LANE-A/B own) is read or written by this round's code.

## PANYA-DECISION consumed this round, queued for next round: `LUA_HOST_API_MAP`

Letter `notes_to_chief/20260906_1704_KA1A-PANYA-DECISION-COO-Q-host-api-map-fn-to-system-have-missing.md`
(primary ADDRESSEE: COO, cc: chief, LANE-Q; landed on `main` mid-round via
the `origin/main` merge above, timestamped 17:04, after this round's own
16:50 start) -- Panya, relayed by ka1-A, wants LANE-Q to spend its *next*
round producing `LUA_HOST_API_MAP.tsv`/`.md`: every host-API function the
616-file corpus calls, mapped to the server system it implies, with a
measured `status` (REAL/STUB/MISSING, file:line-cited) and
`system_exists` (YES/PARTIAL/NO) column, so COO can rank which system to
build next. The letter's own spec says "no code changes this round" and
names it explicitly as "รอบถัดไป" (Q's next round), and says COO -- not Q
-- places it into `NOW.md`. Not primary-addressed to this lane and `NOW.md`
does not carry it yet as of this round's own final fetch, so this round
did not redirect into it mid-flight (this round's own code was already
written, tested and adversary-reviewed by the time this letter landed);
recorded here instead as this lane's explicit top job for whichever round
runs next, ahead of the usual charter-queue/backup-work order, regardless
of whether `NOW.md` has been updated with it yet by the time that round
starts (the letter's own intent is unambiguous even before COO's transcription).
Not stubbed as `.CONSUMED.txt` here since this lane is only cc'd, not the
primary addressee -- COO's own consumption governs that letter's queue
lifecycle; this note is this lane's own record of having read it.

## PR ที่เปิดรอบนี้

- `pirate-force-server` -- opened this round, not draft, `PF-AUTOMERGE: v4`
  present from open, verified via GET. See PR body for the full summary
  (same content as "What this round built" above).
- `pf_bridge` `#1525` [LANE-Q] round gqjas5: claim -- this round's own lock
  PR; unlocked (marker added to its body) once the server PR above is
  confirmed open and not draft.

## รอบหน้าทำอะไร (ลำดับ)

1. **`LUA_HOST_API_MAP.tsv`/`.md`** (see PANYA-DECISION section above) --
   this lane's explicit top job for the next round, a research/documentation
   deliverable, no code changes. Read the full letter first
   (`notes_to_chief/20260906_1704_KA1A-PANYA-DECISION-COO-Q-host-api-map-fn-to-system-have-missing.md`)
   for the exact 11-column TSV spec, the UI/AUTH `hook_side` split, and the
   152-vs-160 count reconciliation ka1-A's own regex count raised (explain
   the difference in one line per that letter's own instruction, do not
   silently pick one number). Check `NOW.md` first in case COO has by then
   folded this into the lane's queue with different wording.
2. If that letter has been superseded/withdrawn by the time the next round
   starts: re-check the same two named blockers fresh (`RE-273`,
   `persistence_quest_state.py`) -- whichever clears first is the next
   real-API job on `Trigger.*`/`Quest.*`.
3. If both stay blocked and no mapping task is queued: continue `Player.*`'s
   stub audit -- re-derive the next candidate needing neither another lane
   nor the LANE-DB door fresh from `STILL_STUBBED`'s own categories rather
   than assumed from this round's grouping (a category reason can turn out
   wrong for one specific name on closer reading, per pf-adversary's own
   caution this round).
4. This session's cloud clone now has `lupa` (this round's own finding,
   above) -- a future LANE-Q cloud round should check first
   (`python3 -c "import lupa"`, or just `pip install lupa`) rather than
   assume it is absent from habit.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอรอบนี้ -- แต่ Player.GetLv/Player.GetClass (91+60 จุดเรียกในคอร์ปัส) อ่านค่าจริงจาก context ที่ฉีดเข้าไปได้แล้วแทนที่จะได้ 0 เสมอ ยังไม่มี dispatcher จริงที่ผูก context นี้กับ session จริง -- ตัวบล็อกทั้งสองของ charter สาย Q (RE-273, ประตูสถานะเควสของ LANE-DB) ยังปิดเหมือนเดิม | pirate-force-server PR (เปิดแล้ว รอ gate, PF-AUTOMERGE: v4 ยืนยัน), pf_bridge PR #1525 (claim, จะปลดล็อกท้ายรอบนี้), full suite 12461 passed/0 failed, preflight PASS
