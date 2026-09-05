# LANE-Q round `456vso` -- 2026-09-05T22:55+07:00 to 23:4x+07:00

## Lock

- Listed `[LANE-Q]` open PRs in both repos at claim time: none (`pf_bridge` open = `#1388`(UI) `#1386`(CS) `#1385`(B) `#1382`(DB) `#1377`(UI, stale) `#1336`(courier); `pirate-force-server` open = `#857`(A) `#856`(GM) `#794`(E), none tagged `[LANE-Q]`) -- opened claim `#1390` on `claude/kind-albattani-456vso`, no yield needed on re-list.
- Mailbox `grep -l "ADDRESSEE: LANE-Q"`: 4 unconsumed at round start (`2112` LANE-B seam answer, `2246`/`2248` COO-DECISIONs, `2248` ka1-A lupa-install confirmation) -- all four read and consumed this round (stubs + `consumed/` copies). Mid-round, `origin/main` merge brought 3 more addressed to LANE-Q (`2212`/`2237` LANE-DB quest-door contract, `2244` LANE-B mob_death hook point) -- read and consumed too; both are informational for NEXT round's `Quest.*`/`Mob.*` queue items, nothing actionable this round (scope was `Trigger.*` only).
- `AGENTS.md` house rules read fresh after the mid-round merge: §7 now carries the exact rule `COO-DECISION 20260905_2249` promised -- "hand a Python object into another language's interpreter (Lua/eval/template) -> attribute access must be closed at the RUNTIME level, not a name blocklist, and tests must pin the RETURNED VALUE, not just the object handed in -- pf-adversary mandatory on every PR touching that boundary." This round's design (`attribute_filter=deny_every_attribute`, tests on the closures the namespace hands back) already matched this before it landed in `AGENTS.md`; pf-adversary confirmed no gap (see below).

## What moved (NOW/M)

**NOW.md**: "team of 8 lanes" line names LANE-Q's queue as `spike -> Trigger.* 17 (unblock M2) -> Quest.* 25 -> Player.* 73` and the M2 milestone line says "next layer = Trigger.* of Q". This round closes the part of the `Trigger.*` item that does not depend on the live-dispatch mapping (see nonclaims): **5 of 17 names real** (`GetTriggerStatus`/`GetTeiggerStatus`/`SetStatus`/`NextStatus`/`SetTriggerStatus`, 542/828 call sites, 65%), backed by a real `TriggerStatusRegistry`, proven against a real gating script with six DISTINCT prerequisite triggers (not the trivial all-Var-stub case round `s2fxf6`'s own test covered).

**Not moved**: M2 itself is still blocked on `SAILING_RESULT` (LANE-A's `#852`/`#857` re-land, not this lane's). The charter's own closing criterion for this queue item -- "a GT where a tester sails into a trigger and the script fires" -- is **not** met this round: nothing wires a live `TriggerVital` (0x1FB2) arrival to a specific script file yet (needs the trigger-id -> script-file mapping the charter names, not mined this round to keep the diff to the state machine itself). A player sailing into a trigger sees no change on screen from this round.

## §7 compliance

Did not touch canonical DB, `GAME_TEST_QUEUE.md`/`CHIEF_CONTINUATION.md`, delete any `pf_bridge` file, `v141`, or `runtime.py`/`app.py`/`store.py`. No branch named by hand (`claude/kind-albattani-456vso` / `claude/hopeful-hopper-456vso`, system-assigned). No `rm -r` in any spelling. Every changed server file and both commit message bodies are ASCII (checked byte-by-byte; two Thai-language docstring lines were caught by this lane's own check before push and fixed in-round -- see below). Staged file-by-file throughout, no `git add -A`.

## Work: `Trigger.*` status state machine, 5/17 real

Grepped the corpus (`gamedata/lua/t_*.lua`, 616 files) before writing a line, per house rule. The 17 names split cleanly: a pure status state machine with no outbound frame and no Quest state (`GetTriggerStatus`/`GetTeiggerStatus` read ANOTHER trigger; `SetStatus`/`NextStatus` write the CURRENT trigger, no id argument in any of the corpus's own call sites because the game engine always knows which trigger is running; `SetTriggerStatus` writes ANOTHER trigger) versus everything that needs a wire-frame encoder this lane does not own or `Quest.*` per-character state (the other 12, each with one specific named reason in `lua_api.trigger.STILL_STUBBED`, no guessing).

`src/pirateforce_foundation/lua_api/trigger.py` (new): `TriggerStatusRegistry` -- one int per (scene, trigger id), process memory, same shape/caps as `world_scene_registry.WorldSceneRegistry` (`PANYA-DECISION 20260905_1057`) but a SEPARATE book -- the charter draws the ownership line explicitly (LANE-A owns island entry; LANE-Q owns the trigger script deciding what happens), so no interface from LANE-A was needed. `RealTriggerNamespace` is a drop-in replacement for `ApiNamespaceStub` on the `Trigger` global. `script_host.py`: `ScriptHost`/`load_script_file` take optional `trigger_context`/`trigger_registry`, defaulting to an isolated context and a private registry so every existing test stays hermetic; every other namespace is unchanged.

**Bug I found and fixed myself before push, not by adversary**: the first draft's `DEFAULT_CONTEXT` used an empty-string scene. `mob_loot._require_scene` (the same door `scene_key` goes through project-wide) refuses an empty string by name, so every read/write under the default context silently no-opped -- `SetStatus`/`NextStatus` looked like they ran (a logged line, no exception) while never actually writing anything. Caught by running the code directly before writing the test suite, not by the tests themselves; fixed to a non-empty synthetic scene name (`"unscoped_default"`) with the failure mode documented in the constant's own docstring.

Worked proof this is real gating logic, not coincidence: `tests/test_script_lua_api_trigger.py::RealTriggerLuaIntegrationTests::test_a_six_gate_trigger_only_advances_when_every_prerequisite_is_ready` runs the real shape of `t_nex_t6.lua`'s `ScriptStart` against six DISTINCT real prerequisite triggers -- refuses to advance while they are not all at the target status, advances the instant they are. Round `s2fxf6`'s own version of this test only covered the trivial case where every `Trigger.VarN` stub collapsed to the same value, which passes regardless of whether the gating logic is real.

## ADVERSARY

**Ordered at round start, on the real implementation's first commit (`00151a2`), per the mandatory rule this exact boundary carries.** Result cited fully before push -- 4 findings, all addressed:

1. **CRITICAL, fixed** (commit `985c005`): the 5 real closures had fixed positional parameters, so a wrong-arity call (`Trigger.SetStatus()`, `Trigger.NextStatus(1)`) raised a raw Python `TypeError` out of `ScriptHost.call` instead of degrading like every other name in the file via `*args` -- dormant only because the corpus calls these 5 names at consistent arity today (grepped, confirmed), but exactly the invariant this whole sandbox exists to keep for untrusted input. Fixed: every real closure checks its own arity first, logs `LUA_TRIGGER_BAD_ARITY`, returns the safe default.
2. **MEDIUM, fixed**: the concurrency stress test gave zero actual protection -- adversary split `next_status`'s single lock acquisition into two (the exact regression its own comment claimed to guard against) and it still passed every time under CPython's normal scheduler. Replaced with a deterministic test (pauses `next_status` mid-read-modify-write, asserts a second thread's lock-acquire attempt fails) -- verified locally this fails against the exact mutant and passes 5/5 on correct code.
3. **LOW, fixed**: `TriggerStatusRegistry`'s docstring said "Never raises" without qualifying that its constructor (never script-reachable) does raise `ValueError` on a bad cap. Docstring corrected, two new tests added.
4. Two more (a Thai-language cp874 gate failure, a stale `docs/PYTEST_SKIP_PINS.json` pin) were already fixed by earlier commits on this branch before the report arrived -- confirmed independently, not re-claimed.

**No new sandbox-escape path found.** Adversary drove attribute-access probes (`__globals__`, `__class__`, `__self__`, the full `__import__` chain) through the NEW closures specifically -- the exact shape round `s2fxf6`'s RCE was found through (a closure a namespace hands back, not the namespace object itself) -- and confirmed `attribute_filter=deny_every_attribute` covers `RealTriggerNamespace`'s closures identically to `ApiNamespaceStub`'s.

## Tests + gates

- New: `tests/test_script_lua_api_trigger.py` (36 tests: registry alone, no lupa needed; the namespace's `__getitem__` contract; lupa-guarded real-Lua integration). Updated: `tests/test_script_host_spike.py` (2 tests reflecting the 5 real names; 1 new regression guard pinning `REAL_METHODS` itself).
- `PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/test_script_lua_api_trigger.py tests/test_script_host_spike.py tests/test_script_lua_api_spec.py tests/test_script_lua_corpus.py -q` = 67 passed, 208 subtests passed.
- Full suite, once, on the final tree (`origin/main` already an ancestor): **11394 passed, 327 skipped, 21261 subtests passed, 0 failed** (576s).
- `tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PREFLIGHT PASS** (cp874, no new skips, main is in this branch, precondition census agrees, both branches `claude/*`, bridge files under ceiling).
- `docs/PYTEST_SKIP_PINS.json` updated: `lupa_package`/`tests/test_script_host_spike.py` count 18->19 (one test renamed+scoped, one added); new entry `lupa_package`/`tests/test_script_lua_api_trigger.py` count 5.

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/hopeful-hopper-456vso`: `00151a2` (real Trigger.* impl) + `05c040a` (docs) + `eddcb4d` (ascii fix) + `aba368a` (pin fix) + `985c005` (adversary fixes) -> PR `#862` **open, not draft, `PF-AUTOMERGE: v4` confirmed present by GET** (touches no boot/login/actor-identity/client-frame code, so opened directly per `PROCESS_GATES.md`).
- `pf_bridge` branch `claude/kind-albattani-456vso`: this round file replaces `_claim.md`; 7 mailbox letters consumed (4 at round start, 3 that arrived mid-round via `origin/main` merge); `docs/SCRIPT_LANE.md` update already in the server PR's own repo (not bridge -- the doc lives in `pirate-force-server/docs/`).
- Not on `main` yet -- next round confirms with `git merge-base --is-ancestor <sha> origin/main`.

## `TWO_SESSIONS_SAME_SCENE:`

`TriggerStatusRegistry` is process memory shared by every session in a scene (same shape as `world_scene_registry.WorldSceneRegistry`), proven at the registry/`ScriptHost` level by `test_two_hosts_sharing_one_registry_see_each_other_s_writes` (two hosts, one registry, one host's write is the other's read) and `test_two_hosts_with_no_registry_given_do_not_leak_into_each_other` (two hosts with no registry given do NOT share a default). Not yet observable from two real game clients -- no live dispatch reads this book from a real session (see nonclaims); ready for the round that wires it to a live frame.

## nonclaims

1. Does not close the charter's GT criterion for this queue item -- no live `TriggerVital` dispatch exists; a player sailing into a trigger sees nothing different this round.
2. Does not implement the other 12 `Trigger.*` names -- each needs a specific missing seam (wire-frame encoder, Quest state, or an RE ticket for `GetContactMode`'s unclear one-call-site semantics), named not guessed.
3. Does not touch `runtime.py`/`app.py`/`store.py` or any other lane's write zone. No new CORE-REQUEST opened.
4. Does not act on the 3 mid-round letters from LANE-DB (`Quest.*` state doors, opened but PR delayed pending chief's guard read) or LANE-B (`mob_death` hook point, now open) beyond reading and consuming them -- both inform next round's `Quest.*`/`Mob.*` work, out of this round's `Trigger.*` scope.
5. Does not claim the `SetStatus`/`NextStatus` no-id design generalizes past this file -- holds because the corpus never calls them any other way (grepped), not a deeper architectural guarantee.

## Next round

1. Wire a live `TriggerVital` (0x1FB2) arrival to a real script file -- needs the trigger-id -> script-file mapping (`gamedata/scene/*.placements.tsv` / a trigger table, grep before assuming absent) and a `lane_hooks/lane_q_*` subscriber that calls the process-singleton `lua_api.trigger.trigger_status_registry()` (not a private one). This is what actually closes the charter's GT criterion.
2. Consume LANE-DB's `Quest.*` state-door contract (`set_quest_flag`/`get_quest_flag`/`set_quest_counter`/`increment_quest_counter`/`get_quest_counter`) once its PR lands on `main` -- check with `git merge-base --is-ancestor` first, do not assume from the letter alone.
3. The remaining 12 `Trigger.*` names, one seam each (see `STILL_STUBBED`).
4. `Quest.*` (25 names) for real, first full quest lifecycle from `q_kill5.lua`.

-- LANE-Q (round `456vso`)

SCOREBOARD: COMING | เซิร์ฟเวอร์รันตรรกะสถานะทริกเกอร์ของสคริปต์เควสต์จริงได้แล้ว (5/17 ฟังก์ชัน Trigger.* ของจริง แทนที่จะตอบ 0 เสมอ) แต่ผู้เล่นยังไม่เห็นอะไรเปลี่ยนบนจอ เพราะยังไม่มีจุดเชื่อมจาก TriggerVital ของจริงไปยังสคริปต์ | server PR `#862` (`00151a2`+`05c040a`+`eddcb4d`+`aba368a`+`985c005`) · 67 เทสใหม่/แก้ · full suite 11394 passed 0 failed
