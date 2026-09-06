# LANE-Q round `x6gxzd` (2026-09-07T01:29+07:00) -- Player.MobAppear real (a per-player visibility FLAG, not a world spawn), plus a cross-lane accessor for LANE-A's future NPC filter

## Lock

Listed open `[LANE-Q] round *: claim` PRs on `pf_bridge` at round start
(`list_pull_requests`, state open, sorted by `created`): zero hits (the
only LANE-Q-titled open PR was `#1583`, "round `uadtc7` addendum:
pf-adversary result (clean)" -- not a claim, title does not end
`: claim`). Both repos reset to fresh `origin/main` before any code was
touched (`pf_bridge` to `22032f8`, `pirate-force-server` to `f51ca62`,
later fast-forwarded to `82c6ef4` after LANE-E's `#968` merged mid-round --
see "Tests + gates" below). Claim opened as `pf_bridge#1602` (branch
`claude/kind-albattani-x6gxzd`, the branch this session was given);
re-listed immediately after opening -- no other open `[LANE-Q] round *:
claim`, so this round holds the lock uncontested.

Heartbeat: `notes_to_chief/_BRIDGE_HEARTBEAT.txt`'s last line
(`2026-09-07T01:26:01+07:00`) is 3 minutes before this round's own
`TZ=Asia/Bangkok date` timestamp (01:29) -- well within the 60-minute
tolerance.

## Mailbox

`grep -l "ADDRESSEE: LANE-Q" notes_to_chief/*.md` then checked each for a
`.CONSUMED.txt` twin. One letter open at round start:

- `20260907_0043_COO-DECISION-panya0039-quest-state-table-feeds-visibility-filter-LANE-Q.md`

Consumed this round by acting on it, not merely reading it -- see "What
this round built" below for the full derivation, "จบรอบ" for the stub.

## AGENTS.md ยง7

Read fresh this round. No new rule since round `lvoma1`'s own read that
changes this lane's posture. Two existing rules leaned on directly:
"เซสชันที่มี Agent/Task tool จริง ต้องเรียก pf-adversary ทุกรอบที่แก้อะไรที่ไม่ใช่การแก้คำผิด
-- รีวิวมือแทนได้เฉพาะเซสชันที่ยืนยันว่าไม่มีเครื่องมือจริงเท่านั้น" -- this
session's own tool surface was checked via `ToolSearch` (both a broad
query and `select:pf-adversary,Agent,Task`) and carries neither a
`Task`/`Agent`-shaped subagent launcher nor a `pf-adversary` tool, so this
round did the documented `ADVERSARY_UNAVAILABLE` fallback (manual
self-review) rather than skip the requirement -- see ADVERSARY below; and
the "sandbox: attribute access must be closed at runtime, tests must pin
on the RETURNED VALUE" rule (`ยง7`'s own Lua-host-specific line) -- checked
directly: this round's own new closure (`Player.MobAppear`) hands the Lua
side nothing but plain `int`/`bool`/`STUB_DEFAULT` values, same posture
every other real closure in this package already takes, verified by
reading the closure's own `return` statements, not assumed.

## Why this round exists

Two mailbox letters landed since round `lvoma1`'s own close, both flowing
from the same owner decision (`PANYA-DECISION 20260907_0039`, via ka1-A,
`cc: LANE-Q`): NPCs are per-player visibility FLAGS, monsters/loot/bosses
stay one shared world (`rank 0` = flag, `rank>0` = shared world, decided
by `n_RANK`/`n_AI_COMBAT`). The COO's own routing letter
(`COO-DECISION 20260907_0043`, `ADDRESSEE: LANE-Q`) names two concrete
asks for this lane:

1. This lane's own item-1 quest-state door (`#965`, `QuestStateStore`)
   must answer, per character: "has quest X been accepted yet / reported
   yet" -- LANE-A's future NPC-visibility filter reads exactly that
   against `CONSTDATA_TH__MOBS.tsv`'s `s_QUEST_BEGIN`/`s_QUEST_END`
   columns, and the letter says add the accessor NOW, not wait for item 3.
2. `Player.MobAppear` (until now `STILL_STUBBED`, category "world spawn,
   not nameable by this lane") should become a stub that RECORDS the
   per-player flag, because the owner's decision makes clear it was never
   meant to be a world spawn/despawn call: it is `Player.*` (a per-player
   calling convention), not `Scene.*`.
3. Third instruction riding with the second: if any call site's `id`
   argument is provably a `rank>0` mob (the 24 quest-tied monster rows in
   `CONSTDATA_TH__MOBS.tsv`), do not decide anything -- write to COO with
   the id(s).

## What this round built

**`lua_api/player.py`: `Player.MobAppear` moves from `STILL_STUBBED` to
`REAL_METHODS` (6/73 `Player.*` real now).** New seam,
`PlayerMobAppearStore` (`Protocol`) / `InMemoryPlayerMobAppearStore`
(default), the exact same shape `lua_api.quest.QuestStateStore` /
`InMemoryQuestStateStore` already established: per-(character_id, mob_id)
boolean flag, keyed and capped the same way, injectable via
`build_namespace(..., store=...)` and now `ScriptHost(..., player_store=
...)` / `load_script_file(..., player_store=...)`. `PlayerContext` gained
one new field, `character_id: int = 0` (the only field this closure
reads), same "0 = not a real character" sentinel `lua_api.quest.
DEFAULT_CONTEXT` already uses. The closure coerces `(mob_id, visible)`,
writes through the store, logs `LUA_PLAYER_REAL Player.MobAppear
character=<n> mob_id=<n> visible=<bool> (per-player flag only, not a
world spawn)`, returns the value read back. It does NOT import, call, or
reference `world_scene_registry`/`mob_ground_persistence`/
`mob_death_persistence` (LANE-A's write zone) -- confirmed by this file's
own import list, unchanged (`.. inventory`, `..player_wire` only).

**`lua_api/quest.py`: `is_quest_accepted`/`is_quest_reported`, the
cross-lane accessor `COO-DECISION 20260907_0043` item 1 asked for.** Two
plain functions, not new `QuestStateStore` methods and not new Lua-facing
`Quest.*` names -- they wrap the SAME `store.get_quest_flag` the real
`Quest.GetQuestFlag` closure already calls, compared against the SAME
`QUEST_ACTIVE`/`QUEST_FINISH` constants this file already derived.
`is_quest_accepted` is `True` only while the flag equals `QUEST_ACTIVE`
(NOT "ever accepted" -- flips back to `False` once reported, matching
`s_QUEST_BEGIN`/`s_QUEST_END`'s own "appear while active, vanish once
reported" shape). LANE-A's own future filter calls these directly from
Python; this lane does not read either `MOBS.tsv` column itself and does
not decide which mob ids they gate -- stays entirely LANE-A's item 3, per
the decision's own "ลำดับ 1->2->3->4->5 ไม่เปลี่ยน" line.

**The rank>0 question: checked, not decided, reported honestly (grep
recorded here, per ยง7's own RE/grep-first house rule).** `grep -rhoE
"Player\.MobAppear\([^)]*\)" gamedata/lua/ | sort | uniq -c`: 3,532
total call sites, EVERY one passes a table-driven `Quest.VarN` argument
(`Var13`-`Var20`, 294-295 sites each) -- zero literal mob-template-id
calls. Which real `n_ID` (and therefore which `n_RANK`) any given call
names lives in each quest's own `QUESTDATA_*.tsv` row (`n_VARI_13`..
`n_VARI_20`-shaped columns), not mined this round -- so this round
genuinely cannot say yes or no to "does any call site collide with a
rank>0 mob id" from the script text alone. NOT escalated to COO: no
conflicting evidence was actually found (an open measurement gap is a
different thing from the "found a collision, don't know what to do" case
the letter asks to escalate) -- carried to "รอบหน้าทำอะไร" instead.

**Checked, found already fixed: the bad-VALUE logging item carried
forward twice.** Round `lvoma1`'s own "รอบหน้าทำอะไร" repeated "add a
bad-VALUE log line to the 9 closures pf-adversary named in round
`7v7yn2`" as still-open. Re-read `lua_api/quest.py`'s own `_log_bad_value`
docstring and its five call sites (`SetFlag`/`SetQuestFlag`/
`MobKillCount`/`CheckMobKillCount`/`GetMobKillCount`) plus `GetQuestFlag`'s
own equivalent (`_log_flag` with a `quest_id=-1` sentinel, which that
function's own docstring explicitly calls out as already covering this
case) -- all 9 of round `7v7yn2`'s real closures that can receive a
right-arity, wrong-VALUE argument already log one; `GetFlag`/
`CanReportDailyQuest`/`ReportDailyQuest` take no arguments, so there is
nothing to validate. This item was actually done in round `7v7yn2`
itself; the carry-forward note in two round files since was stale
bookkeeping, not a real gap -- corrected here rather than carried a
third time. `lua_api/player.py` gained its OWN `_log_bad_value` this
round (`MobAppear` is the first `Player.*` real closure with a
right-arity, wrong-type failure mode), which is new work.

## What this round does NOT do, said plainly

Does not implement `PANYA-DECISION 20260907_0039`'s own visibility filter
(point 2, "ส่งตัวละครนี้ให้คนนี้ไหม") -- that composition stays LANE-A's
item 3, after P-2, unbuilt here on purpose. Does not wire `MobAppear` (or
`is_quest_accepted`/`is_quest_reported`) into any live network dispatch --
no `ScriptHost` run is bound to a real player session yet, same gap every
prior real-method round in this lane has named. Does not touch
`world_scene_registry`/`mob_ground_persistence`/`mob_death_persistence`,
`runtime.py`, `app.py`, or `store.py`.

## Tests + gates

New tests: `tests/test_script_lua_api_player.py` (`MobAppear` --
namespace-contract tests: sets/clears the flag, per-character isolation
across two injected stores, wrong arity, wrong value type incl. a plain
int rejected same as `_coerce_int`'s own bool-vs-int posture, a broken
injected store raises rather than degrading, one Lua-integration test
reproducing `q_kill5.lua`'s own `Delete_Run` call shape).
`tests/test_script_lua_api_quest.py` (`is_quest_accepted`/
`is_quest_reported` -- never-set/active/finished/none states, plus
per-character and per-quest isolation). Updated:
`tests/test_script_host_spike.py` (`q_kill5` fixture's own lifecycle
test: `Player.MobAppear` moves out of the stub-call assertion into a new
real-call assertion, 4 unconditional `Delete_Run` calls measured -- the
other 12 call sites in this fixture sit behind `if (Quest.VarN > 0)` and
never fire under `STUB_DEFAULT=0`; renamed
`test_the_5_real_player_names_are_excluded_above_not_forgotten` ->
`test_the_6_..`). `tests/test_script_lua_corpus.py`:
`BASELINE_TOTAL_STUB_CALLS` RE-MEASURED against the real 616-file corpus
with `lupa==2.8` installed (`pip install lupa==2.8`, same pin
`COO-DECISION 20260905_2246` uses for the bridge's own gate): 3716 ->
2620, EXACTLY (`report.real_call_counts['Player.MobAppear'] == 1096`
under the fixed clock) -- no branch-shift this time, unlike every prior
real-method landing this file documents, because `MobAppear` is a pure
side-effecting call inside branches other stub reads already gate, never
itself a condition another call sits behind.

`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_player.py
tests/test_script_lua_api_quest.py tests/test_script_lua_api_trigger.py
tests/test_script_lua_api_instance.py tests/test_script_host_spike.py
tests/test_script_lua_corpus.py tests/test_npc_interaction_wire.py -q`:
225 passed, 335 subtests passed, 0 failed.

`tests/test_pytest_precondition_census.py` (the AST census over every
`docs/PYTEST_SKIP_PINS.json` pin, re-run after updating the two entries
this round's renames/additions touch -- `tests/test_script_host_spike.py`'s
own `lupa_package` pin, name only, count unchanged at 25;
`tests/test_script_lua_api_player.py`'s own `lupa_package` pin, 6 -> 7):
69 passed, 1135 subtests passed.

Mid-round, `origin/main` moved (`pirate-force-server#968`, LANE-E's own
round `lk97bl`, merged) -- fetched and fast-forward-merged into this
round's branch before the final full run (no conflict: this round's own
changes were still uncommitted working-tree edits at that point).

Full `pytest tests/` run before push (one run, per house rule):
**12616 passed, 327 skipped, 26645 subtests passed, 0 failed, 463s
(0:07:43)**.

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`
(from `pf_bridge`, after committing): PREFLIGHT PASS (cp874 + no new
skips + main already in HEAD + precondition census agrees + no bridge
file grew past its ceiling on this branch + neither queue file grew past
its per-PR cap + no manual scoreboard row touched + no new filename over
100 characters -- the `.CONSUMED.txt` stub below is 101 characters but
exempt: its underlying letter (88 characters) already exists on
`origin/main`, the tool's own documented `inherited` exemption for a
stub whose length this branch did not choose).

## ADVERSARY

`ADVERSARY_UNAVAILABLE` -- this session's tool surface carries no `Task`/
`Agent`-shaped subagent launcher and no `pf-adversary` tool (checked via
`ToolSearch`, both a broad query and a direct
`select:pf-adversary,Agent,Task` query, zero hits). Per house rule, did
the self-review by hand instead: read every hunk in `git diff --cached`
before each commit.

Findings from the self-review: (a) `MobAppear`'s closure rejects a plain
Lua/Python int (`0`/`1`) as the visibility argument, not just non-bool
garbage -- a script accidentally passing `1` instead of `true` gets
`STUB_DEFAULT` and a `LUA_PLAYER_BAD_VALUE` line, not a silently-wrong
"visible" write (mutation check: removing the `isinstance(visible, bool)`
guard makes `test_mob_appear_bad_argument_type_refuses_rather_than_guesses`
fail exactly as expected -- verified by temporarily deleting the guard and
re-running that one test, then restoring it); (b) the injected-store
isolation tests mutate one namespace/store and assert the OTHER instance
is untouched, not just that both started empty, the same shape
`OneScriptHostSharesOneQuestStateStoreTests` already established for the
opposite claim (shared, not isolated); (c)
`PlayerMobAppearStore.set_mob_appear_flag`'s cap-refusal branches mirror
`InMemoryQuestStateStore`'s own tested shape, and a non-positive cap
raises `ValueError` in `__init__`, matching every sibling store's own
contract; (d) `is_quest_accepted`/`is_quest_reported` take the store as
an explicit argument rather than reading a module-global, so two
different tests using two different stores cannot leak into each other.
No defect found this pass. Next round of this lane: try `pf-adversary`
again as the FIRST action, per house rule for a session that found the
tool missing.

## TWO_SESSIONS_SAME_SCENE

Not applicable, on the same grounds every prior round in this lane gives:
`PlayerMobAppearStore` is keyed by `character_id`, never by scene string,
and (like `QuestStateStore`) is explicitly a PER-PLAYER bucket by design,
not a world-shared one -- two different `ScriptHost` runs still get two
different default stores unless a future caller explicitly shares one
object into both (no code does that today). This round's own design
citation (`PANYA-DECISION 20260907_0039` point 3) makes the "per-player,
not world" property a deliberate REQUIREMENT this round satisfies, not
merely an accident that happens not to collide.

## จบรอบ

Consumed the one open mailbox letter -- answered by acting on it:

- `20260907_0043_COO-DECISION-panya0039-quest-state-table-feeds-visibility-filter-LANE-Q.md`
  -- both concrete asks built (see "What this round built" above); the
  rank>0 check done and reported, not escalated (no collision found).
  Stub: `notes_to_chief/20260907_0043_COO-DECISION-panya0039-quest-state-table-feeds-visibility-filter-LANE-Q.md.CONSUMED.txt`.
  Original copied to `notes_to_chief/consumed/`.

`pirate-force-server` PR: `#971` ("[LANE-Q] Player.MobAppear real
(per-player visibility flag, not a spawn) + quest-state accessor for
LANE-A", base `main`, head `claude/hopeful-hopper-x6gxzd`), NOT draft (no
boot/login/actor-identity/client-frame code touched -- Lua-sandbox-
internal wiring and doc/pin bookkeeping only), `PF-AUTOMERGE: v4` present
on open, GET-verified (`mergeable_state: unstable` -- gate still running,
not a merge conflict; body carries the marker on exactly one line).

`pf_bridge`: this round file + one mailbox stub + claim-file removal, on
`claude/kind-albattani-x6gxzd`. Claim PR `pf_bridge#1602` body updated
with the marker to unlock, once the server PR carries its own -- see
below.

## รอบหน้าทำอะไร

1. `store.py`'s quest-state door (`pirate-force-server#954`) -- still
   worth a status check with COO/chief if still unmerged.
2. `RE-285`'s own two not-RE leads (grep the corpus for other `Trigger.*`
   literal-argument calls; check the `.tgr` table `RE-273` opened) --
   neither chased this round either.
3. Inventory seam write side (`AddItem`/`RewardItemSelect`/`AddAndEquip`)
   still blocked on `RE-280`.
4. `CheckWishQuest` (Quest namespace) still needs LANE-GUILD's own state
   door or an RE ticket -- low call count (1), not blocking.
5. LANE-A's own item 3 (the actual NPC-visibility filter reading
   `is_quest_accepted`/`is_quest_reported` against `s_QUEST_BEGIN`/
   `s_QUEST_END`) is LANE-A's to build, after P-2 -- watch for a letter
   back if the two functions' own shape needs to change once a real
   caller exists.
6. If a future round finds a literal, provably `rank>0` mob id reaching
   `Player.MobAppear`, write to COO with the id, per `PANYA-DECISION
   20260907_0039` point 3 -- not decided here because none was found in
   this round's own grep, not because the check was skipped. Mapping
   `Quest.VarN` back to real mob ids via each quest's own `QUESTDATA_*.tsv`
   row is the concrete next step if this needs a real answer.
7. Try `pf-adversary` again as the first action of the next LANE-Q round
   (this round found it unavailable).

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ -- Player.MobAppear (1,766+1,766 จุดเรียกในสคริปต์เควสจริงของ Accept_Run/Report_Run) กับ accessor สถานะเควสสำหรับฟิลเตอร์การมองเห็น NPC ของ LANE-A ทำงานจริงแล้วฝั่งเซิร์ฟเวอร์ (เก็บ/อ่านธงต่อผู้เล่นได้จริง ไม่ใช่แค่ log stub) แต่ยังไม่มี dispatch จริงต่อกับ session ผู้เล่น ยังไม่มีที่เก็บถาวรข้าม relog และ LANE-A ยังไม่ได้ต่อฟิลเตอร์การมองเห็นเข้ากับมัน | pirate-force-server#971, API status 32/160 real
