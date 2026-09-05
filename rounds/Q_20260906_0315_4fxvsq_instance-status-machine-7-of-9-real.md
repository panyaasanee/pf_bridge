[LANE-Q round 4fxvsq | 2026-09-06T03:15+07:00 | claim: pf_bridge#1418]

# LANE-Q round 4fxvsq -- Instance.* status machine, 7/9 real

## What this round did, and did not, move on NOW.md/M

Did not close M2's own remaining criterion ("a tester sails into a trigger
and the script fires" -- that still needs the trigger-id -> script-file
mapping, still unassigned). Did not touch Quest.* (both its doors, the
guard exemption and the LANE-DB column, are still pending chief). Moved:
7 more of the 160-name API surface from stub to real, in a namespace
(`Instance.*`) not previously touched, using the exact backup-work rule
the charter names when the two named queue items are genuinely blocked --
checked fresh this round, not assumed from the last round file.

## Why Instance.*, checked fresh (not assumed)

1. **Trigger-id -> script-file mapping (RE-ticket content `0155`)**: not
   yet numbered or answered. `notes_to_chief/20260906_0256_COO-DECISION-*`
   orders chief to assign the number and decide the guard exemption
   (below) as chief's own item 1; chief's latest round file
   (`FROM_CHIEF_R362_TO_ALL_20260906_0210.md`) predates that decision
   (`02:56` > `02:10`), so it has not been acted on yet.
2. **Quest.* guard exemption (`0209`) + LANE-DB door**: round `vqng2z`'s
   `pirate-force-server#874` (`Quest.CheckOpenTime`) was gate-closed by the
   reaper (`notes_to_chief/20260906_0226_SYNC-NOTICE-*`, consumed this
   round -- see stub) because any reference to the bare token `quest` from
   `script_host.py`'s new `Quest` wiring trips
   `tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests`.  The
   proposed `ALLOWED_SYMBOLS` patch is written
   (`notes_to_chief/20260906_0209_LANE-Q-CORE-REQUEST-*`) but re-checked
   this round by reading the guard's own dict directly in the
   `pirate-force-server` clone: no `script_host`/`lua_api` entry present,
   so it has not landed.  Separately, LANE-DB's per-character Quest-state
   column (`COO-DECISION 20260905_2058`) is also still absent
   (`grep -rl "quest_flag\|quest_counter" src/`: no hit).  Two blockers,
   neither cleared -- starting a second `Quest.*` implementation now would
   only produce a second gate-closed PR.
3. **The other 12 `Trigger.*` names**: `lua_api/trigger.py`'s own
   `STILL_STUBBED` is unchanged; `GetContactMode`'s RE ticket has still not
   been opened by anyone (`grep -rl "GetContactMode"
   notes_to_chief/*.md`: no hit).

With all three genuinely still blocked, this round audited the WHOLE
160-name table (not just `Trigger.*`/`Quest.*`) for the next stub with no
cross-lane dependency, highest call count first, per the charter's own
backup-work rule -- `Instance.*`'s 9 names, grepped fresh across the real
616-file corpus (`pf_bridge/gamedata/lua/`) before writing a line of code,
same discipline round `456vso` used.

## What became real (server PR #882)

7 of 9 `Instance.*` names, 52/55 call sites (94.5%, corrected from an
arithmetic error caught by pf-adversary, see below): `GetInstanceID` and its
shipped alternate-case alias `GetInstanceId` (1 call site), `GetLastingTime`
/`SetLastingTime`, `AddKeyEvent`/`RemoveKeyEvent`, `CallScoreCount` -- all
pure per-instance scratch state (process memory, gone on reboot, same shape
`TriggerStatusRegistry` uses), no outbound frame, no Quest state.  Left as
named stubs (not guessed): `AddBonusPoint` (2 call sites, ambiguous whether
the one optional argument is a point value or a bonus-category id) and
`AddBonusReward` (1 call site, gives an actual reward with no argument at
all).  A CANDIDATE reward table was found by pf-adversary (see below) --
`gamedata/tables/CONSTDATA_TH__SCORECOUNT.tsv`, keyed from
`CONSTDATA_TH__INSTANCE.tsv`'s `n_SCORECOUNT_ID` -- but tracing it to the
specific instances that run these two APIs is unstarted work, not something
this round finished.  Full write-up, corpus evidence and per-name reasoning:
server repo `docs/SCRIPT_LANE.md`, round `4fxvsq` section.

## Tests + gates

- `tests/test_script_lua_api_instance.py` (new, 35 tests): registry alone
  (no lupa), the namespace `__getitem__` contract including the
  wrong-arity degrade-safely proof (mirrors `Trigger.*`'s own), lupa-guarded
  real-Lua integration including the shared-world two-hosts-one-registry
  proof, and a worked example against the REAL shipped
  `gamedata/lua/t_inscnt.lua`.
- `tests/test_script_host_spike.py`: widened still-stubbed exclusion +
  new `Instance.REAL_METHODS` regression guard, same shape as the existing
  `Trigger.*` one.
- `tests/test_script_lua_corpus.py`: `BASELINE_TOTAL_STUB_CALLS` measured
  down 5057 -> 5020 (37 calls moved to real, re-running
  `run_corpus_entry_points` against the real corpus with the new namespace
  installed).
- `docs/PYTEST_SKIP_PINS.json`: pin counts updated (widened
  `test_script_host_spike.py` `lupa_package` 19->20; two new pins for this
  round's own test module, `lupa_package` 4 and `bridge_lua_scripts` 1) --
  verified against `tools/pf_pytest_precondition_census.py`'s own static
  walker (`test_pytest_precondition_census.py`: 69 passed / 1018 subtests),
  not hand-counted.
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`
  (run from this `pf_bridge` checkout, re-run clean after the adversary-fix
  commit) = **PREFLIGHT PASS** (cp874, no new skip markers vs origin/main
  beyond the pinned ones, main already in HEAD, precondition census agrees,
  both branches `claude/*`, bridge files under ceiling).
- `python3 tools_bridge/pf_gate_preflight.py --pr-body <file> --pr-stage
  final` on the server PR body = **[prbody] PASS** (exactly one marker
  line) before opening; GET on the opened PR confirms `state=open`,
  `draft=false`, body carries `PF-AUTOMERGE: v4` verbatim.
- Gate simulation with no `pf_bridge` sibling present (this round adds a
  new `tests/test_*.py` file and moves skip pins, per house rule): ran in a
  detached `git worktree` off this round's first commit (`c0bcaa86`) --
  **`pytest_subset` exit=0** (10687 passed, 127 skipped, 19953 subtests,
  0 failed) and **`skip_census` exit=0** (`RESULT: PASS`, confirmed
  `bridge_lua_scripts tests/test_script_lua_api_instance.py x1` matches
  the pin exactly).
- Full suite (`pytest tests/`) on the tree with `origin/main` already an
  ancestor of HEAD (no merge needed -- verified with
  `git merge-base --is-ancestor origin/main HEAD`): **11671 passed, 323
  skipped, 22201 subtests passed, 0 failed** (591.66s).
- `pf-adversary`: ordered at round start (`AGENTS.md` SS7), result returned
  before push. Independently re-ran the full suite in its own worktree
  (11671 passed / 323 skipped / 0 failed, matching) and re-derived every
  measured claim rather than trusting this round's numbers. **4 real
  findings, all fixed in a follow-up commit (`7596461b`) before push**:
  (1) MEDIUM-HIGH -- "no reward/score table found" was false, a candidate
  table exists (`CONSTDATA_TH__SCORECOUNT.tsv`, keyed from
  `CONSTDATA_TH__INSTANCE.tsv`'s `n_SCORECOUNT_ID`); (2) MEDIUM -- "no
  script checks a richer return value" was false, 7+ scripts branch on
  `GetLastingTime()`/`GetInstanceID()`; (3) LOW -- call-count arithmetic
  error, 52/55 not 53/55; (4) LOW/cosmetic -- `lua_api/__init__.py` did not
  register the new module. All four are docstring/text corrections, no
  logic changed; full suite re-run clean after the fix (100 passed / 198
  subtests on the touched files). Full detail: server repo
  `docs/SCRIPT_LANE.md`, round `4fxvsq`, ADVERSARY section.

## ASCII

Every changed/new file in both repos checked byte-by-byte (0 bytes above
127) before commit.

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/happy-tesla-4fxvsq`, commits
  `c0bcaa86` (the round itself) + `7596461b` (adversary-finding fixes) ->
  PR `#882`, **open, not draft, `PF-AUTOMERGE: v4` confirmed present by
  GET** (touches no boot/login/actor-identity/client-frame code, opened
  directly per `PROCESS_GATES.md`).
- `pf_bridge` branch `claude/gracious-lovelace-4fxvsq`: this round file,
  the claim PR (`#1418`), and the SYNC-NOTICE consumed stub.

## `TWO_SESSIONS_SAME_SCENE:`

N/A this round -- `InstanceRegistry` is this lane's own new process-memory
book (same shape as `TriggerStatusRegistry`), not a write into
`world_scene_registry` or any other lane's shared state.  No script in the
corpus writes a namespace table field at runtime (verified, same grep
`s2fxf6` already ran across all 616 files for this exact question).

## Consumed this round

- `notes_to_chief/20260906_0226_SYNC-NOTICE-pirate-force-server-pr874-closed-never-merged.md`
  -- read and used (see "Why Instance.*" item 2 above); stub placed,
  original copied to `consumed/`.

## nonclaims

1. Does not close the charter's GT criterion for ANY queue item -- no
   player-visible change this round.
2. Does not touch `Quest.*`, the remaining 12 `Trigger.*` names, or any
   other lane's write zone -- blocked status re-confirmed with fresh
   evidence this round, not assumed from a stale file (see "Why
   Instance.*" above, each item names its own grep/check).
3. Does not claim `AddBonusPoint`'s or `AddBonusReward`'s real-engine
   semantics, and does not claim the candidate `CONSTDATA_TH__SCORECOUNT.tsv`
   table (found by pf-adversary, see "Tests + gates" above) is definitely
   the right one or definitely wired to these two names for any given
   instance -- named as an open trace, not guessed either way; no RE ticket
   opened this round (RE runner time is scarce, per `AGENTS.md` SS7's
   one-ticket budget) -- named as next-round follow-up.
4. `Instance.CallScoreCount`'s registry counts INVOCATIONS, not a score or
   a reward -- a candidate reward table exists (see above) but tracing it
   to a real instance is unstarted work this round did not do.
5. Does not touch `runtime.py`/`app.py`/`store.py` or any other lane's
   write zone. No new CORE-REQUEST opened this round.
6. `BASELINE_TOTAL_STUB_CALLS`'s new value (5020) reflects today's OTHER
   stub coverage as much as this round's own change, same caveat round
   `4jsydv` wrote for its own baseline move.
7. Server PR this round touches 7 files (over the informal ~6-file
   guideline in `HOWTO_OPEN_A_PR.md`) -- not split, because every file is
   load-bearing for the same single change (the new namespace module, its
   wiring, its own tests, the two existing test files whose exclusions/
   baselines the new real methods force to move, and the pin file the
   census checks against); splitting would land code and its own tests/
   pins in different PRs, which is a worse shape than one slightly larger
   one.

## Next round

1. **First job, already done this round**: adversary's result returned
   before push (4 findings, all fixed in commit `7596461b`) -- the next
   round does not need to spend its first job on a pending result.
2. Re-check the same three named blockers fresh: chief's guard-exemption
   decision on `0209`/RE-number on `0155`
   (`notes_to_chief/20260906_0256_COO-DECISION-*` item 1),
   `persistence_quest_state.py` landing on `main`
   (`git merge-base --is-ancestor`), `GetContactMode`'s RE ticket status.
   Whichever clears first is the next round's first real-API job -- if the
   guard exemption landed, rebase `claude/hopeful-hopper-vqng2z` (or its
   successor) onto it per the SYNC-NOTICE's own instructions rather than
   restarting `Quest.CheckOpenTime` from scratch.
3. If all three stay blocked again: trace `CONSTDATA_TH__INSTANCE.tsv`'s
   `n_SCORECOUNT_ID` column against the instance rows that actually run
   `t_insbospnt_himdfx.lua`/`t_insbosev_himdfx.lua`/
   `t_drp&insbospnt_himdfx.lua` (pf-adversary's own closing question, not
   answered this round) before deciding whether `AddBonusPoint`/
   `AddBonusReward` even need an RE ticket, or whether the table resolves
   cleanly enough to implement directly.
4. Otherwise: re-audit the remaining stub surface for another pure-function
   candidate with no cross-lane dependency, using
   `run_corpus_entry_points`'s real call-volume ranking rather than the
   static census table alone -- the method this round used to find
   `Instance.*`.

SCOREBOARD: COMING | เซิร์ฟเวอร์ตอบคำถามเกี่ยวกับ instance ได้จริงจากหน่วยความจำโปรเซส (Instance.GetInstanceID/GetLastingTime/SetLastingTime/AddKeyEvent/RemoveKeyEvent/CallScoreCount เป็นของจริง 7 ใน 9 ชื่อ ไม่ใช่ค่า stub อีกต่อไป) แต่ผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอ เพราะยังไม่มี dispatch จริงที่ผูกทริกเกอร์/อินสแตนซ์ขาเข้าเข้ากับสคริปต์ และคิวหลัก (Trigger.*/Quest.* เต็มวงจร) ยังติดคอขวดนอกเขต Q เหมือนเดิมทั้งสามข้อ (รอ chief ตัดสิน guard exemption + เลข RE ตาม COO-DECISION 0256) · pf-adversary เจอ 4 ข้อจริง (เอกสารอ้างผิด ไม่ใช่โค้ด) แก้แล้วก่อน push | server PR #882 (commits c0bcaa86+7596461b, ชุดเต็มเขียว 11671 passed/0 failed) · pf_bridge claim #1418
