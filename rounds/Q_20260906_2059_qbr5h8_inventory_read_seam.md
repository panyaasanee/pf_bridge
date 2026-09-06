# LANE-Q round `qbr5h8` (2026-09-06T20:59+07:00) -- inventory seam, read side: Player.CheckItemNum/GetItemNum/CheckEquipItem real

## Lock

No open `[LANE-Q] round *: claim` PR on `pf_bridge` at round start (checked
via `list_pull_requests` on `panyaasanee/pf_bridge`, state open, sorted by
`created`: 0 hits for a title starting `[LANE-Q] round`). Both repos reset
to fresh `origin/main` before any code was touched, per
`prompts/COMMON_LANE_ROUND.md`. Claim opened as `pf_bridge#1562` (branch
`claude/gracious-lovelace-qbr5h8`); re-listed immediately after opening
(`search_pull_requests repo:panyaasanee/pf_bridge is:pr is:open in:title
"LANE-Q round"` and a direct `list_pull_requests` cross-check) -- no other
open `LANE-Q round` claim, so this round holds the lock uncontested.

Heartbeat note: `notes_to_chief/_BRIDGE_HEARTBEAT.txt`'s own last line is
`2026-09-06T19:00:02+07:00`, about 2 hours before this round's own
`TZ=Asia/Bangkok date` timestamp -- NOW.md's own top section already
explains this exact gap ("เครื่อง Panya ปิด 19:0x heartbeat หยุดตามเครื่อง
ไม่ใช่สะพานตาย"), so this round treats it as the known, already-reported
condition rather than a fresh clock fault of its own.

## Mailbox

`for f in $(grep -l "ADDRESSEE: LANE-Q" notes_to_chief/*.md); do [ -f
"${f}.CONSUMED.txt" ] && echo CONSUMED || echo OPEN: $f; done` (note the
stub name keeps the original's own `.md`, e.g. `<name>.md.CONSUMED.txt` --
an earlier pass this round used `${f%.md}.CONSUMED.txt` and wrongly read
every already-consumed LANE-Q letter, including `20260906_1846`, as
OPEN; caught and fixed before finalizing this file). Correct result:
every letter ever addressed `ADDRESSEE: LANE-Q` already carries a
`.CONSUMED.txt` twin -- mailbox is genuinely empty this round. In
particular, `20260906_1846_COO-DECISION-q1812-host-api-map-ranking-LANE-
Q.md` was already consumed by round `7v7yn2` (its own stub:
"consumed by LANE-Q round 7v7yn2 ... acted on the 'flag-quest-state'
item") -- this round did NOT re-consume it. This round's task instead
comes from source #4 in `prompts/COMMON_LANE_ROUND.md`'s own priority
order (the last round file's own "รอบหน้าทำอะไร"): round `7v7yn2`'s own
next-steps section 3 named "`COO-DECISION 20260906_1846`'s own ranking,
item 2 (`inventory seam`, read side) is next after this item closes" --
that citation, not a fresh letter, is this round's authority. The two
CORE-REQUEST letters round `7v7yn2` sent (`..._1950_..._quest-flag-
counter-daily-stamp-columns.md`, `..._1951_..._quest-store-wiring-trips-
the-foundation-guard.md`) are LANE-Q's own outgoing mail, still
unanswered (no `.CONSUMED.txt`, and nothing addressed FROM chief/DB TO
LANE-Q about either) -- nothing about either blocks this round's own item
2 work, so neither was waited on.

## AGENTS.md SS7

Read fresh this round. LANE-Q's own write zone (unchanged): `src/
pirateforce_foundation/script_*.py`, `lua_api/`, `tests/test_script_*`,
`docs/SCRIPT_LANE.md`, `lane_hooks/lane_q_*` (server) / `rounds/Q_*` (this
repo) -- `store.py`/`runtime.py`/`app.py` explicitly NOT this lane's, and
this round does not touch any of them (see below). No new SS7 rule since
last round's own read that changes this lane's posture.

## What this round built: `Player.CheckItemNum`/`GetItemNum`/`CheckEquipItem` real

`COO-DECISION 20260906_1846`'s system-wide ranking put item 2 ("inventory
seam") next once item 1 (flag-quest-state, round `7v7yn2`) closed, with an
explicit split: read side first (`CheckItemNum`/`GetItemNum`/
`CheckEquipItem`, "bind to `inventory.py`/`store.py` that already exist, no
byte-guessing"), write side (`AddItem`/`RewardItemSelect`/`AddAndEquip`)
blocked on `RE-280` until it answers.

Grepped every call site in `gamedata/lua/**/*.lua` before writing a line
(not guessed): `Player.CheckItemNum(templateId, count)` (211 calls/105
files/arity 2) is always a boolean "does the player hold at least `count`
of `templateId`" gate (e.g. `Quest/q_guildgather1.lua:41`);
`Player.GetItemNum(templateId)` (99 calls/72 files/arity 1) is always
assigned into a local as an integer count (e.g.
`Quest/q_gather_new.lua:205`); `Player.CheckEquipItem(templateId)` (14
calls/2 files/arity 1) OR/AND-chains several literal template ids as a
plain boolean across exactly two files (`Quest/q_kill1_2.lua`,
`Quest/q_con3.lua`).

`lua_api/player.py`'s `PlayerContext` widens by two fields --
`backpack: inventory.BackpackState`, `equipped_template_ids:
frozenset[int]` -- both defaulting to EMPTY (no items, no equips; NOT
either governed golden snapshot `INITIAL_BACKPACK`/`MERGED_V111_BACKPACK`,
which would assert something about who the anonymous default player is
that nothing supports), the exact same "inert default" posture `level`/
`class_id` already established for `GetLv`/`GetClass` (round `gqjas5`).
`GetItemNum` sums `ItemAttrState.quantity` across matching rows;
`CheckItemNum` compares that sum against the caller's second argument;
`CheckEquipItem` is template-id membership in `equipped_template_ids`. All
three fail closed on wrong arity (`LUA_PLAYER_BAD_ARITY`, `STUB_DEFAULT`)
and on an uncoercible argument (own `_coerce_int`, same shape as
`lua_api.trigger._coerce_int`, kept as its own copy per this package's
established no-cross-namespace-import convention) -- `GetItemNum` answers
0, `CheckItemNum`/`CheckEquipItem` answer `False`, never raise.

**What this round does NOT do, said plainly**: no live dispatcher exists
yet (same gap `GetLv`/`GetClass` already had) -- nothing in this round
calls `store.get_backpack`/`store.list_equipped_items` or builds a
`PlayerContext` from a real session; every test supplies its own context
directly. `store.py`/`migrations/` are not this lane's write zone and were
not touched -- the module docstring names exactly which two `store.py`
functions a future dispatcher would call, so that wiring needs no new
store-side reads when it lands. The write half of the inventory seam
stays a stub, untouched, still blocked on `RE-280`.

## Tests + gates

`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_player.py
tests/test_script_lua_api_quest.py tests/test_script_lua_api_trigger.py
tests/test_script_lua_api_instance.py tests/test_script_host_spike.py
tests/test_script_lua_corpus.py -q` -- 159 passed, 306 subtests passed, 0
failed (24 new unit tests + 3 new Lua-integration tests in
`test_script_lua_api_player.py`, including 3 regression tests reproducing
the adversary's crash findings below; two pinned regression guards this
round had to update: the `REAL_METHODS` guard in `test_script_host_spike.py`
and `BASELINE_TOTAL_STUB_CALLS` in `test_script_lua_corpus.py`, 4937 ->
4715, re-measured against the real corpus with `report.real_call_counts`,
not naive arithmetic -- see that file's own updated comment for the full
derivation including a 20-call branch-shift remainder, the same emergent
phenomenon documented for round `gqjas5`'s own GetLv/GetClass landing).

Full `pytest tests/` run before push: 12544 passed, 323 skipped, 1 failed
in 414s. The 1 failure
(`tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`)
is confirmed pre-existing on `origin/main`, not this round's: reproduced
by `git stash` (reverting this round's own diff back to
`origin/main`+PR#944) and running that one test alone -- still fails,
identically. LANE-A's own module, not touched by this round, not this
lane's write zone.
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`:
PREFLIGHT PASS (cp874 + no new skips + main already in HEAD + precondition
census agrees + no bridge file grew past its ceiling on this branch +
neither queue file grew past its per-PR cap + no manual scoreboard row
touched). Also ran `--pr-body <file> --pr-stage final` against the actual
PR body before opening: PASS, exactly one `PF-AUTOMERGE: v4` marker line.

## ADVERSARY

Invoked via the `pf-adversary` subagent partway through the round (after
the diff was ready, not strictly at round start -- this round's own
process gap; next round should invoke it as the very first action
instead, per house rule) against `src/pirateforce_foundation/lua_api/
player.py`'s new code on branch `claude/happy-tesla-qbr5h8`, in an
isolated worktree. Result returned before push, folded in:

- **Real defect found and FIXED this round**: `PlayerContext(backpack=
  None)`, `PlayerContext(equipped_template_ids=None)`, and a backpack row
  with `quantity=None` each raised a raw `TypeError`/`AttributeError`
  straight out of `ScriptHost.call` (not exploitable today -- no
  dispatcher builds a `PlayerContext` from live data yet -- but a crash
  surface left for whichever future round wires one from unvalidated
  `store.get_backpack` output). Fixed: `_item_count`/new `_is_equipped`
  now catch and degrade to `0`/`False`, matching every other real
  closure's fail-closed contract; 3 new regression tests reproduce the
  adversary's exact three inputs.
- **Confirmed, not a new defect**: `CheckItemNum`/`CheckEquipItem`'s
  arity-mismatch `STUB_DEFAULT` (0) reads truthy in real Lua -- but
  `Quest.CheckOpenTime` (already shipped, real, boolean-shaped) has the
  identical shape and the identical test-suite gap; inherited, not
  introduced.
- No crash found from Lua-controlled arguments (fuzzed every position,
  every namespace method, zero exceptions). Semantics (sum-not-count,
  arity, call counts) independently re-verified against the real corpus,
  not trusted from the docstring. Mutation testing on all three core
  comparisons caught by the existing suite. Sandbox posture preserved (no
  `BackpackState`/`ItemAttrState`/frozenset object ever crosses into Lua).
- Full text: `docs/SCRIPT_LANE.md`'s own "Round qbr5h8" ADVERSARY section.

## TWO_SESSIONS_SAME_SCENE

Not applicable the way it usually is for a shared-world door: a backpack
and an equipment set are per-CHARACTER state (mirrors
`store.get_backpack`/`store.list_equipped_items`'s own `character_id`
keying), never a scene string -- two sessions in the same scene share
nothing through this seam, and no live dispatcher exists yet for two
sessions to race through it anyway (same posture already stated for
`level`/`class_id`).

## จบรอบ

`pirate-force-server` PR: `pirate-force-server#953` (`[LANE-Q] Player.
CheckItemNum/GetItemNum/CheckEquipItem real: inventory seam read side`,
base `main`, head `claude/happy-tesla-qbr5h8`), NOT draft (no boot/login/
actor-identity/client-frame code touched), `PF-AUTOMERGE: v4` present on
open, GET-verified (`mergeable_state: unstable` -- gate still running,
not a merge conflict; body carries the marker on exactly one line).
`pf_bridge`: this round file + claim-file removal on
`claude/gracious-lovelace-qbr5h8`; claim PR `pf_bridge#1562` body updated
with the marker to unlock, now that the server PR carries its own.

## รอบหน้าทำอะไร

1. Check the two open CORE-REQUEST letters from round `7v7yn2` first
   (`quest-flag-counter-daily-stamp-columns`,
   `quest-store-wiring-trips-the-foundation-guard`) -- if either is
   answered, wire it in citing the grant/answer as authority, before
   claiming new work.
2. Inventory seam read side is now 3/3 real. If `RE-280` has answered by
   the next round, its write side (`AddItem`/`RewardItemSelect`/
   `AddAndEquip`) is next per `COO-DECISION 20260906_1846`'s own ranking,
   still ahead of item 3 (`Player.MobAppear`, explicitly LANE-A's
   territory, not this lane's to build).
3. `CheckWishQuest` (Quest namespace) still needs an RE ticket -- low call
   count (1), not blocking.
4. If CI/gate surfaces a `lupa`-version or Windows-specific difference this
   Linux-container run could not catch, fix it here rather than starting
   over, per `SYNC-NOTICE`'s own standing instruction.
5. Invoke `pf-adversary` as the FIRST action next round, not partway
   through, per house rule -- this round's own process gap.
6. The adversary's own open question (`docs/SCRIPT_LANE.md`'s "Round
   qbr5h8" ADVERSARY section): whichever round builds the live dispatcher
   should decide whether to also revalidate through
   `inventory.require_backpack_shape` before constructing a
   `PlayerContext`, as defense in depth on top of this round's own
   closure-level fix.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ -- ตรรกะฝั่งเซิร์ฟเวอร์ของ Player.CheckItemNum/GetItemNum/CheckEquipItem (นับ/เช็คของในกระเป๋าและของที่สวมใส่) ถูกต้องและมีเทสยืนยันแล้ว แต่ยังไม่มี dispatcher จริงต่อกับ session ผู้เล่น (ช่องว่างเดียวกับ GetLv/GetClass เดิม) | pirate-force-server#953 (เปิดแล้ว, marker แล้ว), Player.* fns real 5/73 (+3 this round), inventory-seam read side 3/3 done
