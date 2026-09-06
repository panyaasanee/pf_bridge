# LANE-Q round `7v7yn2` (2026-09-06T19:50+07:00) -- flag-quest-state, 9/25 more Quest.*, 2/17 more Trigger.* real

## Lock

No open `[LANE-Q] round *: claim` PR on `pf_bridge` at round start (checked via
`search_pull_requests repo:panyaasanee/pf_bridge is:pr is:open in:title "LANE-Q round"`,
0 results). Branches reset to fresh `origin/main` on both repos before any
code was touched, per `prompts/COMMON_LANE_ROUND.md`.

## Mailbox

`grep -rl "ADDRESSEE:" notes_to_chief/*.md | xargs grep -l "ADDRESSEE: LANE-Q"`,
filtered for missing `.CONSUMED.txt` companions: exactly one open letter,
`notes_to_chief/20260906_1846_COO-DECISION-q1812-host-api-map-ranking-LANE-Q.md`
(the source of this round's whole task -- consumed below).

## What this round did, and what it did not

**Made real** (COO-DECISION `20260906_1846`'s "flag-quest-state" item,
answering `20260906_1812_LANE-Q-TO-COO-lua-host-api-map-delivered`'s own
question about what comes next):

- `Quest.*`, 9 names: `GetQuestFlag`, `SetFlag`, `SetQuestFlag`, `GetFlag`,
  `MobKillCount`, `CheckMobKillCount`, `GetMobKillCount`,
  `CanReportDailyQuest`, `ReportDailyQuest` -- Quest.* now 10/25 real
  (`CheckOpenTime` was already real).
- `Trigger.*`, 2 names: `QuestActiveProgress`, `QuestFinishProgress` --
  Trigger.* now 7/17 real.
- Fixed a real correctness bug found while doing this: `Quest.None`/
  `Active`/`Finish` previously all silently read back as the generic
  `STUB_DEFAULT` (0) through the namespace's own "anything else" fallback
  -- meaning `Quest.Active` and `Quest.Finish` were INDISTINGUISHABLE from
  each other and from "never set" before this round, which would have
  broken every flag comparison in the corpus (489+416+90+67 call sites)
  the moment `GetQuestFlag`/`SetFlag` etc. went real, silently, with no
  test able to catch it (both sides of every `==` would have agreed on the
  wrong number). Derivation of the two proven values (`None`=0, `Active`=1)
  from a cross-script correlation (`t_opnq_t1.lua`/`t_clsq.lua`, the same
  open/close trigger family) is in `lua_api/quest.py`'s own module
  docstring; `Finish`=2 is a tagged assumption (free choice, no corpus site
  literal-compares it to a number).
- Full design rationale, the exact 9-name grep evidence from
  `gamedata/lua/Quest/q_kill5.lua` and 68 sibling files, and the
  `QuestStateStore`/`InMemoryQuestStateStore` seam this is all built on:
  `lua_api/quest.py`'s own module docstring (this round's version).
  `lua_api/trigger.py`'s module docstring covers the 2 `Trigger.*` names
  and the derivation of `Quest.Active`/`Finish`'s values.

**Refused, one name short of COO's list of 12**: `CheckWishQuest`. COO's
letter named it alongside the other 9 Quest.* names, but grepping for what
a "wish" precondition actually checks (`gamedata/tables/` for any table
with "wish" in its name or near `q_wish.lua`'s own quest id, `external/`,
`notes_to_chief/consumed/`) turned up nothing -- no table, no RE answer, no
prior letter defines the semantics `Quest/q_wish.lua`'s own `Accept_Check`
gates on (1 call site total). Making it real would mean guessing a
quest-accept precondition, the exact thing `prompts/LANE-Q.md` forbids and
the same posture already taken twice in this same pair of files for the
same reason (`GetWeekDay`, `Trigger.GetContactMode`). Named in
`lua_api/quest.py`'s own `STILL_STUBBED` dict with this exact reason, not
silently dropped to match COO's count.

**NOT done, said plainly, per the module docstrings' own "what this does
not do yet"**:
- No production persistence. `InMemoryQuestStateStore` -- the default a
  bare `build_namespace(...)` call falls back to when given no `store` --
  is process memory, explicitly documented as NOT the production answer
  (does not survive a relog, a regression against `PANYA-DECISION
  20260904_0233`'s own M5 milestone if ever left as the permanent answer).
  The real, persistent half of this door is a LANE-DB/chief-owned table
  this lane cannot write itself (`store.py`/`migrations/` are named
  off-limits in `prompts/LANE-Q.md`) -- a `CORE-REQUEST` asking for it,
  with the exact contract `QuestStateStore` already codes against, went
  out this same round:
  `pf_bridge/notes_to_chief/20260906_1950_LANE-Q-CORE-REQUEST-quest-flag-counter-daily-stamp-columns.md`.
- No live dispatch. Nothing in this round binds a script run to a real
  player session/character id -- `QuestContext`/`quest_store` are
  caller-supplied seams (today: tests only), same posture
  `TriggerContext`/`trigger_registry` already had before the `bxly5p`
  round's own live wire, and still have for everything except the
  `TriggerVital` hook that round built.
- **`script_host.ScriptHost` does NOT yet share one `QuestStateStore`
  between its `Trigger` and `Quest` namespaces.** A first draft of this
  round threaded `quest_context`/`quest_store` through
  `ScriptHost.__init__`/`load_script_file` to fix exactly that -- reverted
  before push because it trips `tests/test_npc_interaction_wire.py`'s
  foundation quest/shop guard (three new symbols not in that test's
  `ALLOWED_SYMBOLS`, chief's to grant, not this lane's to add itself; same
  situation round `vqng2z` hit and chief granted via
  `pf_bridge/notes_to_chief/consumed/20260906_0510_CHIEF-GRANT-...`).
  Asked again this round:
  `pf_bridge/notes_to_chief/20260906_1951_LANE-Q-CORE-REQUEST-quest-store-wiring-trips-foundation-guard.md`.
  Until granted, `Quest.*` and `Trigger.QuestActiveProgress`/
  `QuestFinishProgress` each work fully correctly on their OWN independent
  private default store when driven through a live `ScriptHost` with no
  explicit wiring -- only cross-namespace consistency within one script run
  is the gap, and no script in the corpus is known to need both in one call
  stack today (`t_opnq_t1.lua`/`t_clsq.lua` are always two separate
  `ScriptStart` runs). `build_namespace`'s own unit tests (this round, both
  files) prove the sharing WORKS when a caller passes one store to both
  builders directly -- the gap is only that `ScriptHost` does not do that
  wiring itself yet.
- `MobKillCount`'s `target` argument is not persisted (only progress,
  reset to 0, is) -- every measured corpus call site re-supplies the same
  table-driven literal to the paired `CheckMobKillCount` call directly, so
  storing a second copy would be redundant state. Actual kill-progress
  INCREMENTS on a real mob death are explicitly out of scope (a future
  LANE-B `lane_hooks` subscriber, per this lane's own charter boundary:
  "combat state of B = read via lane_hooks after the event").
- **Player-visible impact: none yet.** No wire frame changes, no dispatch
  reaches a live session. SCOREBOARD below reflects this honestly.

## Evidence, two layers

- **Server-side, direct**: `lua_api/quest.py`/`lua_api/trigger.py`'s own
  unit tests (`tests/test_script_lua_api_quest.py` -- new
  `QuestFlagAndCounterTests` class, 15 tests; `tests/test_script_lua_api_trigger.py`
  -- 3 new tests) exercise every one of the 11 newly-real closures directly
  against `InMemoryQuestStateStore`, no Lua involved: flag round-trips
  (current-quest vs arbitrary-quest-id, two characters never colliding),
  mob-kill registration/check/read lifecycle (two mobs in one quest
  independent), daily-report gating (same day false, next day true, per
  quest not shared), the three status constants distinct, wrong-arity and
  bad-argument refusal (never raises).
- **Corpus-wide, measured not assumed**: ran the full 616-file corpus
  through `script_host.run_corpus_entry_points` against a fixed clock
  (`PYTHONPATH=src`, `lupa==2.8` installed this session --
  `pip install lupa==2.8` succeeds on this Linux container even though the
  Windows gate is the one that matters for merge). `report.real_call_counts`
  printed the exact new counts folded into `docs/SCRIPT_LANE.md`'s table
  and `tests/test_script_lua_corpus.py`'s updated
  `BASELINE_TOTAL_STUB_CALLS` (4937 -> 3931, i.e. 1006 fewer stub calls,
  wider than the naive 995+7=1002 new real calls -- the same
  measured-not-assumed branch-shift phenomenon this file's own comment
  already documents for earlier rounds, this time shifting `Player.GetClass`
  from 42 to 48 with zero lines of `lua_api/player.py` touched, because an
  earlier `Quest.*` comparison in the same script stopped reading
  `STUB_DEFAULT`). No regression in `KNOWN_LOAD_FAILURES`/
  `KNOWN_ENTRY_POINT_CALL_FAILURES` (both subtests still pass unchanged).
- `q_kill5.lua`'s own full lifecycle test
  (`tests/test_script_host_spike.py::TwoNamedSpikeScriptsRunHeadlessTests::test_q_kill5_full_quest_lifecycle_runs_to_completion`)
  updated: `Quest.MobKillCount`/`SetFlag`/`CheckMobKillCount` moved from the
  expected STUB set into an asserted REAL set (both checked, neither
  silently dropped).

## Tests + gates

`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_quest.py
tests/test_script_lua_api_trigger.py tests/test_script_host_spike.py
tests/test_script_lua_corpus.py -q` -- all green (see counts above). Full
`pytest tests/` run on this branch as the last commit before push, per
house rule (result folded into this file before push if it finished in
time; see below if not). `python3 tools_bridge/pf_gate_preflight.py --repo
../pirate-force-server` run before push.

## ADVERSARY

Invoked at round start per house rule, on the staged diff
(`git diff --cached` at commit time). Result folded in before push if it
returned in time; if not, `ADVERSARY_PENDING` on this PR, and next round
picks it up first per `AGENTS.md` Section 7's timing rule.

## TWO_SESSIONS_SAME_SCENE

Not applicable the way it usually is: quest flag/counter state is
per-CHARACTER (via `QuestContext.character_id`), not per-scene --
`InMemoryQuestStateStore` keys everything off `character_id`, never a scene
string, so two sessions in the same scene share nothing through this door
(and two sessions as the SAME character, which this server does not
support today, are out of scope, same as every other per-character door in
this codebase).

## รอบหน้าทำอะไร

1. Check both CORE-REQUEST letters first: the guard exemption
   (`20260906_1951_...trips-the-foundation-quest-shop-guard.md`) -- if
   granted, re-apply the reverted `ScriptHost`/`load_script_file`
   `quest_context`/`quest_store` wiring citing the grant as authority, same
   pattern round `xcbnbn`'s grant letter described; and the persistence
   accessor (`20260906_1950_...-quest-flag-counter-daily-stamp-columns.md`)
   -- if answered, wire the real accessor in as `QuestStateStore`'s default,
   nothing else should need to change per its own Protocol shape.
2. `CheckWishQuest` needs an RE ticket before it can go real (see refusal
   reason above) -- not blocking, low call count (1).
3. Per `COO-DECISION 20260906_1846`'s own ranking, item 2 (`inventory
   seam`, read side) is next after this item closes, EXCEPT the write side
   (`AddItem`/`RewardItemSelect`/`AddAndEquip`) which stays blocked on
   `RE-280` per that same letter -- do not guess bytes ahead of it.
4. If CI/gate surfaces a `lupa`-version or Windows-specific difference this
   Linux-container run could not catch (same risk every prior LANE-Q round
   flagged), fix it here rather than starting over, per
   `SYNC-NOTICE`'s own standing instruction.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ -- ตรรกะฝั่งเซิร์ฟเวอร์ของ 9 Quest.* + 2 Trigger.* ถูกต้องและมีเทสยืนยันแล้ว แต่ยังไม่ต่อกับ session ผู้เล่นจริงและยังไม่มีที่เก็บถาวรข้าม relog (รอ CORE-REQUEST) | pirate-force-server PR (เปิดแล้ว, ดูหัวข้อ "จบรอบ" ด้านล่าง), quest-flag fns real 9/12 (COO's list; CheckWishQuest refused, see above), Trigger fns real 2/2
