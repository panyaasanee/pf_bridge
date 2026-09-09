# LANE-Q round `uadtc7` addendum: pf-adversary result (clean)

NOT a claim. Round `uadtc7`'s own lock (`pf_bridge#1579`) is already
released and merged. This adds only the finding that arrived AFTER the
unlock -- `ADVERSARY_PENDING pirate-force-server#960` from that round's
own file has now resolved -- into that round's own record, per the house
rule ("ผล pf-adversary เพิ่งคืน/เจอของต้องแก้หลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก").
One file, no code.

## Result: no defects found

`pf-adversary` reviewed the diff in an isolated worktree (built from the
same base the round used, then re-verified byte-identical against the
actual commit that shipped, `16349f3`). Summary of what it tried and
confirmed, in full in `pirate-force-server#960`'s own PR body (updated
with this same text):

- `is`-identity for `quest_context`/`quest_store` holds on both the
  default path (`ScriptHost()`) and the explicit-injection path.
- Mutation-tested the round's own new tests
  (`OneScriptHostSharesOneQuestStateStoreTests`): broke the wiring two
  ways (dropped `quest_context=`/`quest_store=` from the Trigger call;
  dropped `context=`/`store=` from the Quest call) -- both mutations
  caught by all three tests.
- Ran the real 616-script corpus (`tests/test_script_lua_corpus.py`) with
  and without this round's diff: `BASELINE_TOTAL_STUB_CALLS` and every
  pinned `real_call_counts` entry identical in both runs -- zero
  observable regression against production scripts.
- `docs/PYTEST_SKIP_PINS.json`'s updated count (25) confirmed by direct
  collection and by `test_pytest_precondition_census.py` (69 passed, 1122
  subtests).
- Guard exemption re-verified independently:
  `test_every_symbol_exemption_is_still_earned` and the full
  `QuestAndShopStateGuardTests` class pass; `quest_context`/`quest_store`
  are pass-through only, `InMemoryQuestStateStore`'s real logic lives one
  directory down in `lua_api/quest.py` (already separately exempted),
  nothing in `script_host.py` itself decides quest state.
- Thread-safety: non-issue by construction (`QuestContext` is a frozen
  dataclass, `InMemoryQuestStateStore` already used a reentrant lock, one
  `ScriptHost` runs one call at a time, never nested).
- Sandbox: `RealTriggerNamespace.__getitem__`/`RealQuestNamespace.__getitem__`
  never hand `self`/the store/the context to Lua -- no new escape
  surface from exposing these as constructor parameters.
- The one full-suite failure the round already reported
  (`tests/test_lane_a_choose_npc_scene1.py`'s own `KNOWN_RED_MAIN` row)
  was independently reproduced by the adversary on the live read-only
  checkout and confirmed unrelated to `script_host.py`/`lua_api/quest.py`/
  `lua_api/trigger.py`.

## Process gap, named again

Adversary was invoked after the diff was already committed and the full
suite already run -- not at round start. Round `qbr5h8`'s own round file
already named this exact gap without fixing it; round `uadtc7` repeated
it. Whichever LANE-Q round runs next should invoke `pf-adversary` as
its literal first action, before any code is read or written, to stop
this from recurring a third time.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ (เหมือนรอบ uadtc7 เดิม) -- ADVERSARY_PENDING จากรอบนั้นปิดแล้ว ไม่พบข้อบกพร่อง การแชร์ QuestStateStore ระหว่าง Trigger กับ Quest ผ่านการทดสอบ mutation และรัน corpus จริง 616 ไฟล์แล้วไม่มีผลต่างจากก่อนแก้ | pirate-force-server#960 (body อัปเดตแล้ว), pf_bridge/rounds/Q_20260906_2254_uadtc7_addendum_adversary_clean.md
