# LANE-Q round `uadtc7` (2026-09-06T22:54+07:00) -- recover #947, wire one shared QuestStateStore between Trigger and Quest

## Lock

No open `[LANE-Q] round *: claim` PR on `pf_bridge` at round start (checked
via `list_pull_requests`, state open, sorted by `created`: the open list
at round start carried `[LANE-A]`/`[LANE-K]`/`[LANE-GM]`/`[LANE-DB]`
claims plus `#1493` (a non-claim addendum), zero `[LANE-Q] round *` hits).
Both repos reset to fresh `origin/main` before code was touched
(`pf_bridge` to `283ecd7`, `pirate-force-server` to `cf961be`), per
`prompts/COMMON_LANE_ROUND.md`. Claim opened as `pf_bridge#1579` (branch
`claude/kind-albattani-dyqifb`, the branch this session was given -- not
a self-chosen name); re-listed immediately after opening (`list_pull_requests`
state open, sorted `created` ascending) -- no other open `LANE-Q round`
claim among the six open PRs returned, so this round holds the lock
uncontested. **Process note, said plainly**: the claim PR was opened
partway through this round (after the code investigation and cherry-pick
had already started), not at the very first action -- a gap from this
round's own process, not a lock race (no other `LANE-Q` claim ever
appeared), but worth naming so the next round opens its claim first.

Heartbeat: `notes_to_chief/_BRIDGE_HEARTBEAT.txt`'s last line is
`2026-09-06T19:00:02+07:00`, about 3h54m before this round's own
`TZ=Asia/Bangkok date` timestamp (22:54). `NOW.md`'s own top section
already explains this exact condition ("เครื่อง Panya ปิด 19:0x heartbeat
หยุดตามเครื่อง ไม่ใช่สะพานตาย"), same as round `qbr5h8` treated it -- not a
fresh clock fault.

## Mailbox

`grep -l "ADDRESSEE: LANE-Q" notes_to_chief/*.md` then checked each for a
`.CONSUMED.txt` twin (`${f}.CONSUMED.txt`, NOT `${f%.md}.CONSUMED.txt` --
round `qbr5h8`'s own note about that exact mistake, re-checked this
round). Result: every letter addressed `ADDRESSEE: LANE-Q` already
carries `.CONSUMED.txt` EXCEPT one:
`20260906_2151_CHIEF-REPLY-LANE-Q-quest-state-door-granted-1950-1951-not-yet-earned.md`
(chief round `awnjat`, answering LANE-Q's own two CORE-REQUEST letters
from round `7v7yn2`: `20260906_1950_...quest-flag-counter-daily-stamp-columns.md`
and `20260906_1951_...quest-store-wiring-trips-the-foundation-guard.md`).
This is this round's authority, consistent with source #4 in
`prompts/COMMON_LANE_ROUND.md`'s own priority order too: round `qbr5h8`'s
own "รอบหน้าทำอะไร" item 1 named exactly this ("Check the two open
CORE-REQUEST letters from round `7v7yn2` first ... if either is
answered, wire it in"). Consumed this round -- see "จบรอบ" below.

## AGENTS.md ยง7

Read fresh this round. LANE-Q's own write zone unchanged: `src/
pirateforce_foundation/script_*.py`, `lua_api/`, `tests/test_script_*`,
`docs/SCRIPT_LANE.md`, `lane_hooks/lane_q_*` (server) / `rounds/Q_*`
(this repo) -- `store.py`/`runtime.py`/`app.py` explicitly NOT this
lane's. This round's one exception, explicitly pre-authorized rather than
self-granted: three lines added to `tests/test_npc_interaction_wire.py`'s
`ALLOWED_SYMBOLS["script_host.py"]` dict, per chief's own letter above
(chief owns that guard; the letter names the exact patch and the
condition under which LANE-Q may land it). No new ยง7 rule since last
round's own read that changes this lane's posture.

## What this round built

### Part 1 -- recovered `pirate-force-server#947` (closed by the reaper, never merged)

`#947` ("flag-quest-state: 9 more Quest.*, 2 more Trigger.* real", round
`7v7yn2`) was based on `main` at `cf961be` -- the SAME sha `origin/main`
still sits on this round. Fetched `refs/pull/947/head` and cherry-picked
its two commits (`023548f`, `5d15de7`) unchanged onto a fresh branch from
that exact base: both applied with zero conflicts (`git cherry-pick
--no-commit` reported no output either time), because nothing has landed
on `main` since `#947` was opened that touches the same files. Re-ran the
recovered tests immediately after each cherry-pick to confirm nothing
about the recovery itself needed adjustment: 65 passed, 39 skipped, 61
subtests passed, before any of this round's own new code was written.

### Part 2 -- new this round: one shared `QuestStateStore` between Trigger and Quest

`lua_api.trigger.build_namespace`'s own docstring (landed by `#947`,
carried through the cherry-pick unchanged) already named the gap in
detail: a first draft threading `quest_context`/`quest_store` through
`ScriptHost.__init__`/`load_script_file` was reverted before `#947`'s own
push because it tripped `tests/test_npc_interaction_wire.py`'s
`QuestAndShopStateGuardTests` (three new symbols, no exemption -- "that
exemption is chief's to grant after reading the names, not this lane's to
add itself"). CORE-REQUEST `20260906_1951` asked for exactly that grant;
chief's reply (see Mailbox above) pre-approved three symbol names with an
exact patch, conditioned on landing it in the SAME PR as real wiring code
(the guard's `test_every_symbol_exemption_is_still_earned` refuses an
exemption for a symbol that does not exist in `script_host.py` yet).

Built the wiring the docstring already specified: `ScriptHost.__init__`/
`load_script_file` gained `quest_context: Optional[lua_api_quest.QuestContext]`
and `quest_store: Optional[lua_api_quest.QuestStateStore]` parameters.
Inside `__init__`, both are rebound IN PLACE to their own default
(`lua_api_quest.DEFAULT_CONTEXT`/`lua_api_quest.InMemoryQuestStateStore()`)
when `None` -- deliberately NOT into new local names like
`shared_quest_context` -- then passed to BOTH `lua_api_trigger.build_namespace`
(as `quest_context=`/`quest_store=`) and `lua_api_quest.build_namespace`
(as `context=`/`store=`), so the two namespace builders that used to each
default to their OWN private store now default to the SAME one.

**Why "rebound in place, not a new name" matters, measured not assumed**:
ran `QuestAndShopStateGuardTests` against a first draft that used
`shared_quest_context`/`shared_quest_store` as the local names -- the
guard flagged FIVE offending symbols, not three
(`_in_memory_quest_state_store`, `quest_context`, `quest_store`,
`shared_quest_context`, `shared_quest_store`), because those two new
names are not on chief's pre-approved list. Renamed to reuse the
parameter names directly; re-ran the guard: exactly the three chief
pre-approved (`quest_context`, `quest_store`,
`_in_memory_quest_state_store` -- confirmed the CamelCase normalizer
really does produce that exact leading-underscore form for
`InMemoryQuestStateStore` in this file's real source, not assumed from
the letter's own draft). Added chief's patch text verbatim (adjusted
nothing -- the real code matched the letter's own draft exactly).

## What this round does NOT do, said plainly

No production persistence: `InMemoryQuestStateStore` is still the only
`QuestStateStore` implementation anywhere in this codebase. Chief's own
DB-backed accessor (CORE-REQUEST `1950`, `store.py`'s
`get_quest_flag`/`set_quest_flag`/`get_quest_counter`/`set_quest_counter`
+ `migrations/016_character_quest_state.sql`) landed in chief's OWN round
`awnjat`, but that PR (`pirate-force-server#954`) is ALSO closed by the
reaper, unmerged -- `store.py`/`migrations/` are chief's write zone, not
this lane's, so re-landing `#954` is NOT this round's job and was not
attempted. Until it lands, switching `ScriptHost`'s default store to the
real accessor stays a one-parameter change for a future round, exactly as
chief's own letter says. No live dispatch: nothing binds a `ScriptHost`
run to a real player session/character id. Player-visible impact: none.

## Tests + gates

New: `tests/test_script_host_spike.py`'s `OneScriptHostSharesOneQuestStateStoreTests`
(3 tests) -- `test_trigger_and_quest_namespaces_hold_the_identical_store_object`
(`assertIs` on both `_quest_store`/`_store` and `_quest_context`/`_context`,
not equality -- catches the two-separate-but-equally-empty-instances bug
`is` alone can catch), `test_a_trigger_quest_progress_write_is_visible_to_a_later_quest_read`
(a tiny Lua script calling `Trigger.QuestActiveProgress(42)` then
`Quest.GetQuestFlag(42)` on a `ScriptHost()` with NOTHING injected --
the default-sharing path every existing caller takes -- returns `1`, not
`0`), `test_an_explicitly_injected_store_is_the_one_both_namespaces_share`
(same shape with an explicit store/context pair, checked both through the
Lua call AND by reading the injected Python object directly afterward).

`lupa` is not installed in this cloud container by default (`pip install
lupa==2.8` this round, same version COO pinned for the bridge's own gate
pip line per `COO-DECISION 20260905_2246`) -- installed to actually run
the Lua-backed suite rather than trust the diff by inspection.

`docs/PYTEST_SKIP_PINS.json`'s `tests/test_script_host_spike.py` entry:
count 22 -> 25, the three new test names added (alphabetical position
verified against the existing list's own ordering), note appended.
MEASURED against the real file via `tests/test_pytest_precondition_census.py`'s
own AST walker (`PinFileTests`), not counted by hand -- both
`test_each_pinned_module_guards_exactly_its_pinned_count` and
`test_the_pinned_names_are_the_tests_the_source_actually_guards` went red
before this fix (25 != 22, and the derived name set) and green after.

`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_quest.py
tests/test_script_lua_api_trigger.py tests/test_script_lua_api_instance.py
tests/test_script_lua_api_player.py tests/test_script_host_spike.py
tests/test_script_lua_corpus.py tests/test_npc_interaction_wire.py -q`:
194 passed, 333 subtests passed, 0 failed.

Full `pytest tests/` run before push (`origin/main` merge is a no-op,
already current at `cf961be`): 12544 passed, 327 skipped, 26403 subtests
passed, 1 failed --
`tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`,
`NOW.md`'s own `KNOWN_RED_MAIN` row. Confirmed pre-existing, not this
round's: `git stash` (reverting this round's own diff back to unmodified
`origin/main`), ran that one test alone on the clean tree -- fails
identically. LANE-A's own file, not touched by this round, not this
lane's write zone; `git stash pop` restored this round's diff afterward,
confirmed via `git status --short` (same four then five modified paths as
before the stash).

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`:
PREFLIGHT PASS. Also ran `--pr-body <file> --pr-stage final` against the
actual PR body before opening it: PASS.

## ADVERSARY

`ADVERSARY_PENDING pirate-force-server#960`. Invoked via the
`pf-adversary` subagent, but AFTER the diff was already committed and the
full suite already run -- not at round start. This is the same process
gap round `qbr5h8`'s own "รอบหน้าทำอะไร" already named ("Invoker
`pf-adversary` as the FIRST action next round, not partway through") and
this round repeated it rather than fixing it. Result not back by push
time; will land as a follow-up commit on `claude/hopeful-hopper-dyqifb`
or as this round file's own addendum, per house rule. Per
`prompts/COMMON_LANE_ROUND.md`: pushed anyway rather than holding the
round lock waiting on it, and this file does NOT claim "passed adversary"
anywhere above.

## TWO_SESSIONS_SAME_SCENE

Not applicable, same reasoning `#947` and round `qbr5h8` already
established for this exact door: quest flag/counter state is keyed by
`character_id`, never by scene. Sharing ONE store instance within a
SINGLE `ScriptHost` run does not create a new two-sessions hazard: two
different `ScriptHost` instances (i.e. two different sessions) still get
two different default stores unless a future caller explicitly passes
the identical object into both -- no code does that today, and no live
dispatch exists yet for two sessions to race through this door anyway.

## จบรอบ

Consumed the mailbox letter: `notes_to_chief/20260906_2151_CHIEF-REPLY-LANE-Q-quest-state-door-granted-1950-1951-not-yet-earned.md`
answered -- acted on (this round's entire Part 2). Stub written:
`notes_to_chief/20260906_2151_CHIEF-REPLY-LANE-Q-quest-state-door-granted-1950-1951-not-yet-earned.md.CONSUMED.txt`
("consumed by LANE-Q round uadtc7 -- landed the wiring code + the
pre-approved ALLOWED_SYMBOLS patch in pirate-force-server#960").

`pirate-force-server` PR: `#960` ("[LANE-Q] recover #947 + share one
QuestStateStore between Trigger and Quest", base `main`, head
`claude/hopeful-hopper-dyqifb`), NOT draft (no boot/login/actor-identity/
client-frame code touched -- this is Lua-sandbox-internal wiring),
`PF-AUTOMERGE: v4` present on open, GET-verified (`mergeable_state:
unstable` -- gate still running, not a merge conflict; body carries the
marker on exactly one line).

`pf_bridge`: this round file + mailbox stub + claim-file removal, on
`claude/kind-albattani-dyqifb`. Claim PR `pf_bridge#1579` body updated
with the marker to unlock, now that the server PR carries its own marker
-- GET-verified.

## รอบหน้าทำอะไร

1. Read this round's own `ADVERSARY_PENDING pirate-force-server#960`
   result first (whatever landed as a follow-up commit or an addendum
   here) before claiming new work.
2. Invoke `pf-adversary` as the FIRST action, not partway through -- this
   round repeated the SAME gap round `qbr5h8` already named and did not
   fix either.
3. `store.py`'s quest-state door (`pirate-force-server#954`, chief's own
   PR, closed unmerged) is NOT this lane's to re-land -- but flag it to
   COO/chief if it is still unmerged next round, since two of this lane's
   own PRs (`#947` originally, now this one) have each separately been
   blocked or delayed by it.
4. Per `COO-DECISION 20260906_1846`'s ranking: inventory seam read side
   is 3/3 real (round `qbr5h8`, `pirate-force-server#953`, not yet
   merged) -- write side (`AddItem`/`RewardItemSelect`/`AddAndEquip`)
   still blocked on `RE-280`.
5. `CheckWishQuest` (Quest namespace) still needs an RE ticket -- low call
   count (1), not blocking.
6. The 9 closures pf-adversary flagged in round `7v7yn2` for a missing
   bad-VALUE log line (observability parity with `GetQuestFlag`) are
   still not fixed -- carried forward again.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ -- สคริปต์หนึ่งตัวที่เรียกทั้ง Trigger.QuestActiveProgress/QuestFinishProgress และ Quest.* ในรอบเดียวกันตอนนี้เห็นค่าที่อีกฝั่งเขียนจริงแล้ว (ก่อนหน้านี้แยกคนละที่เก็บ) แต่ยังไม่มี dispatch จริงต่อกับ session ผู้เล่นและยังไม่มีที่เก็บถาวรข้าม relog | pirate-force-server#960 (เปิดแล้ว, marker แล้ว, ADVERSARY_PENDING), 3 new tests
