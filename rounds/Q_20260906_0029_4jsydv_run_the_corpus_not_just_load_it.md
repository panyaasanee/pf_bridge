# LANE-Q round `4jsydv` -- 2026-09-05T23:59+07:00 to 2026-09-06T0x:xx+07:00

## Lock

- Listed `[LANE-Q]` open PRs in `pf_bridge` at claim time: none. Opened claim PR `#1395` on
  `claude/gracious-lovelace-4jsydv` (this session's system-assigned branch, per this session's own
  attribution instructions -- one session, one branch, matching COMMON_LANE_ROUND.md's rule).
  Re-listed immediately after opening: still only `#1395` tagged `[LANE-Q]` -- no race, no yield needed.
- Mailbox `grep -l "ADDRESSEE: LANE-Q"`: all consumed already at round start (7 letters, stubs +
  `consumed/` copies present from round `456vso`) -- checked freshly, none unconsumed. No new LANE-Q
  mail arrived mid-round either (re-checked after merging `origin/main` twice).
- `AGENTS.md` §7 read fresh: no new rule since round `456vso` changes this lane's queue or write zone.
- Last round file `rounds/Q_20260905_2337_456vso_trigger-status-machine-5-of-17-real.md`'s "Next round"
  section named three items, all checked this round before writing code (see "What moved" below) --
  all three are genuinely blocked, not skipped.

## What moved (NOW/M)

**NOW.md**: LANE-Q's queue line still reads `spike -> Trigger.* 17 (unblock M2) -> Quest.* 25 ->
Player.* 73`. This round does not advance any of those three counts (still 5/17 Trigger.* real, 0/25
Quest.*) -- all three of round `456vso`'s named next steps are blocked on something outside this lane's
write zone, checked fresh this round, not assumed from the old round file:

1. **Trigger-id -> script-file mapping** (closes the charter's own GT criterion: "a tester sails into a
   trigger and the script fires"): grepped `gamedata/tables/`, `external/`, `archive/`,
   `notes_to_chief/consumed/` before assuming absent -- no hit anywhere, and the script filenames
   themselves do not encode the id either. Real gap in the committed artifacts. Wrote
   `notes_to_chief/20260906_0029_LANE-Q-ASK-COO-trigger-id-to-script-file-mapping-needs-an-RE-ticket.md`
   asking for an RE ticket number rather than guessing or self-assigning one.
2. **LANE-DB's `Quest.*` state-door contract**: declared in letters `2212`/`2237` (consumed round
   `456vso` already), but confirmed this round with `grep -rl "quest_flag\|quest_counter" src/` (server
   repo, zero hits) that it is NOT on `main` yet -- the `2237` letter itself says it tripped a
   chief-owned coverage guard and is waiting on a read, not a code problem.
3. **The remaining 12 `Trigger.*` names**: re-read `lua_api/trigger.py`'s own `STILL_STUBBED` -- every
   one already names its missing seam (a CS/A/UI wire-frame encoder this lane does not own, `Quest.*`
   state per item 2, or an RE ticket for `GetContactMode`'s unclear semantics). None free to implement.

So this round did the charter's own backup work item 2 instead (`prompts/LANE-Q.md`: "regression test:
load all 616 scripts every round, count remaining `LUA_API_STUB`, print the number in the round file --
this number must fall every week"), which was still missing: `load_corpus()` (round `s2fxf6`) only
PARSES the 616 files, it never calls a single function they define, so the API surface has never been
exercised at realistic call volume outside single-call unit tests.

**Not moved**: no player-visible change this round. This is instrumentation over the existing sandbox
(a better regression harness + two real bugs found in the shipped scripts), not a new feature. A player
sailing into a trigger, or accepting a quest, sees nothing different than before this round.

## Work: `run_corpus_entry_points` -- call every script's entry points, not just load them

`src/pirateforce_foundation/script_host.py`: `run_corpus_entry_points(root, log)` loads every `.lua`
file (same one-state-per-script isolation as `load_corpus`), then calls every one of
`STANDARD_ENTRY_POINTS` -- the 8 zero-argument names the ORIGINAL engine calls, not invented: measured
by grepping every top-level `function Name(...)` definition across the real 616-file corpus (`find
gamedata/lua -name "*.lua" -print0 | xargs -0 grep -hoE ...` -- note the `-print0`/`xargs -0`: one file,
`t_test auto.lua`, has a space in its name and silently splits a call site under bare `xargs`, which is
exactly the mistake pf-adversary's own re-derivation of one of these numbers made, see ADVERSARY below).
These eight account for 2396 of ~2451 top-level definitions in the corpus; the rest are internal helpers
a script calls on itself (`Ex_Mission`, `Check_Level`, ...), not something an outside caller invokes.

Every call is fail-closed the same way `load_corpus` already is: an entry point that raises is logged
(`LUA_SCRIPT <path> ERR entry=<name> <message>`) and recorded in a structured `EntryPointRun.errors`
dict (name -> message), never allowed to stop the run for the other 615 files.

**Measured on the real corpus: 5057 total `LUA_API_STUB` calls across 137 distinct
`<Namespace>.<Method>` names** (`BASELINE_TOTAL_STUB_CALLS` in `tests/test_script_lua_corpus.py`, pinned
exact-match, same idiom as `KNOWN_LOAD_FAILURES`). Separately, **346 calls land on Trigger's 5
already-real methods** (`NextStatus` 201, `GetTriggerStatus` 121, `SetTriggerStatus` 23,
`GetTeiggerStatus` 1) -- counted apart so real coverage never gets misread as stub debt (see ADVERSARY
finding 1, this was a real bug in the first draft). Top five stub names by volume: `Player.MobAppear`
(1096), `Mob.ShowAnimation` (658), `Quest.SetFlag` (405), `Player.RemoveItem` (289),
`Scene.PlacementOFF` (173).

**Two real bugs in the SHIPPED scripts, found by actually calling them** (invisible to `load_corpus`'s
load-only check), pinned in `KNOWN_ENTRY_POINT_CALL_FAILURES` (17 `(path, entry_point)` pairs):

- 4 files declare `local check_N` inside nested `if`/`else` blocks in `Report_Check`, then read
  `check_N` again after those blocks close -- ordinary Lua lexical scoping resolves that read to a
  stray, ever-nil GLOBAL. Confirmed straight from the source, not a guess about Lua semantics.
- 13 files call a bare global `rate(dicevalue)` defined in a DIFFERENT file, `utility.lua` -- this
  host's one-Lua-state-per-script design (deliberate, stops 616 files sharing one global table from
  overwriting each other's same-named entry points) means a name defined in one file is never visible
  from another. `utility.lua` is itself one of the 5 `KNOWN_LOAD_FAILURES` (blocked `os.time()` at its
  own top level), so even a shared-preload design would need the sandbox widened too.

Full evidence, top-stub-name breakdown, and both bugs' grep citations: `docs/SCRIPT_LANE.md`, section
"Round 4jsydv".

## ADVERSARY

**Ordered at round start** (`AGENTS.md` §7: mandatory whenever this session's Agent tool changes
anything beyond a typo). Reported against the first draft's staged diff. 4 findings:

1. **HIGH, fixed**: first draft's `total_stub_calls` summed every namespace's raw `.calls` list length,
   silently folding 346 real `Trigger.*` calls into a number meant to mean "still stubbed"
   (`RealTriggerNamespace` shares one `.calls` list between its 5 real and 12 stub methods) -- caught
   independently BY HAND before adversary's report came back, and by adversary itself, landing on the
   identical corrected split (5057 stub / 346 real) both ways -- strong corroboration, not just
   silencing a complaint. Fixed with `REAL_QUALIFIED_NAMES` (a set of fully-qualified real method names,
   checked regardless of which Python object's `.calls` list a call came from) and a new regression test
   (`test_stub_vs_real_call_split_is_not_conflated`).
2. **HIGH, not fixed, documented as a nonclaim**: no timeout or instruction-count budget on
   `ScriptHost.call` -- adversary built and ran a 6-line repro (`function f() return f() end`, a proper
   Lua tail call that never overflows the C stack into a catchable error) that hangs the call
   indefinitely. Independently re-confirmed this round: `grep -rlE "\bwhile\b" gamedata/lua` is empty,
   so the current 616-file corpus has no live trigger for this -- but `lua_api/trigger.py`'s own
   docstring names this exact call path as the template a future live `TriggerVital` dispatch will
   reuse, so a hang there would wedge a listener thread for a whole scene, not just fail a test. Named
   in `run_corpus_entry_points`'s own docstring and `docs/SCRIPT_LANE.md` nonclaim 6 -- not fixed this
   round (would need its own design + adversary pass), not silently deferred either.
3. **MEDIUM-HIGH, fixed**: a pinned test recovered which entry point failed via `name in (run.error or
   "")` -- a SUBSTRING search over one concatenated error string. Adversary built a real counter-example
   (an entry point that returned cleanly got misattributed as failed because its own name happened to
   appear inside a DIFFERENT entry point's error text) and reproduced it against the actual code. Fixed:
   `EntryPointRun.errors` is now a `dict` keyed by entry-point name -- no string search anywhere.
4. **NIT, fixed**: a leftover duplicate `return report` (dead, unreachable second line).

**One adversary claim did not survive independent re-derivation**: adversary's own re-grep of
`Accept_Run`'s definition count got 306 (this round's comment says 305) -- re-counted with
`find ... -print0 | xargs -0 grep -c` (a bare `xargs` silently splits on the one filename in the corpus
that has a space in it, `t_test auto.lua`) and reproduced exactly 305, matching the original comment.
Not changed. Recorded for the record, not to score a point -- the same fragile-`xargs`-on-filenames trap
is worth remembering next time anyone re-derives one of these census numbers by hand.

## Tests + gates

- New: `tests/test_script_lua_corpus.py` +5 tests (`FullCorpusEntryPointCallsTests`).
- `PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/test_script_lua_api_trigger.py
  tests/test_script_host_spike.py tests/test_script_lua_api_spec.py tests/test_script_lua_corpus.py
  tests/test_pytest_precondition_census.py -q` = **141 passed, 1189 subtests passed**.
- `docs/PYTEST_SKIP_PINS.json`: `lua_corpus_runnable`/`tests/test_script_lua_corpus.py` count 4 -> 9 --
  RE-MEASURED, not guessed: `pip uninstall -y lupa` then `pytest -rs` in this same cloud session,
  counted the actual `SKIPPED` summary lines (9), then `pip install lupa` back before continuing.
- `python3 tools/pf_pytest_precondition_census.py --run` = **RESULT: PASS** ("every skip is declared,
  named and pinned").
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (run from this `pf_bridge`
  checkout) = **PREFLIGHT PASS** (cp874, no new skips, main is in this branch, precondition census
  agrees, both branches `claude/*`, bridge files under their size ceilings).
- Full suite, once, on the final merged tree (`origin/main` already an ancestor): **PENDING AT WRITE
  TIME -- started before this file was written, still running; see the claim-PR's own body/commit for
  the actual pass/fail line once it finishes. Not pushing until it reports green**, per house rule
  ("รันชุดเต็มครั้งเดียวต่อรอบ ... เป็น commit สุดท้ายจริง").
- ASCII-checked every changed file (0 bytes above 127), including the new JSON pin entry.

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/happy-tesla-4jsydv`: commit `6e8f414` (run_corpus_entry_points +
  tests + docs + pin) + merge commits bringing `origin/main` (which itself picked up round `456vso`'s
  `#862`, merged mid-round -- confirmed via `git merge-base --is-ancestor`) -> PR opening after this
  file (see claim PR `#1395`'s body once updated, or the next round file, for the exact PR number and
  marker-confirmed-present line).
- `pf_bridge` branch `claude/gracious-lovelace-4jsydv`: this round file + one new letter
  (`notes_to_chief/20260906_0029_LANE-Q-ASK-COO-trigger-id-to-script-file-mapping-needs-an-RE-ticket.md`)
  replace `rounds/Q_20260905_2359_4jsydv_claim.md` on this branch.
- Not on `main` yet -- next round confirms with `git merge-base --is-ancestor <sha> origin/main`.

## `TWO_SESSIONS_SAME_SCENE:`

N/A this round -- no shared-world state touched. `run_corpus_entry_points` builds a fresh `ScriptHost`
(and, for `Trigger`, a fresh private `TriggerStatusRegistry`) per file inside its own loop; nothing
persists across files or across calls to the function, and nothing here reads or writes
`world_scene_registry` or any process-singleton registry.

## nonclaims

1. Does not close the charter's GT criterion for any queue item -- no player-visible change this round;
   this is instrumentation over the existing sandbox, not a new feature a tester can see on screen.
2. Does not open the trigger-id -> script-file RE ticket -- the grep evidence above establishes the gap
   is real; a status letter to COO carries the ask forward (RE runner time is scarce, needs a ticket
   number from chief, shared counter with GT per `AGENTS.md` §9).
3. Does not claim `rate`'s original-engine behavior either way -- plausibly the real client preloads
   `utility.lua` into a shared environment before running any trigger/quest script; not measured against
   the real client.
4. `BASELINE_TOTAL_STUB_CALLS` (5057) is a floor, not a live-game call count -- every `Quest.VarN`/
   `RewardItemN`/`StringVarN` field this harness supplies reads `STUB_DEFAULT=0`, so a branch gated on
   one being nonzero never runs here.
5. No timeout/instruction budget added to `ScriptHost.call` this round -- see ADVERSARY finding 2.
6. Does not touch `runtime.py`/`app.py`/`store.py` or any other lane's write zone. No new CORE-REQUEST.

## Next round

1. **Whichever of the three blockers clears first is the next round's first job.** Check
   `notes_to_chief/` for a COO-DECISION answering this round's RE-ticket ask (topic:
   trigger-id -> script-file mapping) and check `git merge-base --is-ancestor` against LANE-DB's
   `Quest.*` state-door PR before assuming either is still blocked -- do not re-derive from this file's
   own claims, they may be stale by the time the next round starts.
2. If both stay blocked: re-check `GetContactMode`'s RE-ticket status specifically (the one of the
   remaining 12 `Trigger.*` names that is a pure RE gap like item 1, not a cross-lane wire-frame wait) --
   it may unblock independently of the trigger-id mapping question.
3. If all three stay blocked: `docs/SCRIPT_LANE.md`'s own "Next round" section (charter backup work item
   1) says to implement the next stub API that needs no other lane -- re-audit `STILL_STUBBED` and the
   72 `Player.*`/other-namespace names' call-site counts for anything that turns out not to need a DB
   column or wire frame after all, now that this round's `run_corpus_entry_points` gives a real call-
   volume ranking (`Player.MobAppear` 1096, `Mob.ShowAnimation` 658, ...) to prioritize by, instead of
   the static `PF_GAMEDATA_LUA_API.tsv` call-site count alone.
4. Follow-up named but not built this round: an instruction-count or wall-clock budget on
   `ScriptHost.call` (ADVERSARY finding 2) -- worth its own round once the live-dispatch path that will
   actually call real scripts against real player input starts getting built, so the guard is proven
   before it is load-bearing rather than after.

-- LANE-Q (round `4jsydv`)

SCOREBOARD: STUCK | เซิร์ฟเวอร์รันสคริปต์ 616 ไฟล์จริงและนับได้ว่าฟังก์ชัน API ตัวไหนยังเป็น stub อยู่กี่ครั้ง (5057 ครั้ง จาก 137 ชื่อ ไม่รวม 346 ครั้งที่เป็นของจริงแล้ว) พร้อมเจอบั๊กจริง 2 แบบในสคริปต์ต้นฉบับที่ไม่เคยถูกมองเห็นมาก่อน แต่ผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอ เพราะงานหลัก (Trigger.*/Quest.* ต่อ) ติดคอขวดนอกเขต Q ทั้งสามข้อ (ตาราง trigger-id->สคริปต์ที่ไม่มีในเอกสาร, PR ประตูเควสของ DB ยังไม่ขึ้น main, seam ที่เหลือของ Trigger.* ต้องรอสายอื่น) | server PR (เลขรอตอนจบรอบ, commit `6e8f414`) · pf_bridge round file นี้ · จดหมาย ASK-COO เรื่อง RE ticket
