[LANE-Q round vmm7vf | 2026-09-06T12:16+07:00 | claim: pf_bridge#1478]

# LANE-Q round vmm7vf -- Instance.AddBonusPoint/AddBonusReward real (path b), Instance.* reaches 9/9

## What this round did, and what it moved on NOW.md

Lock check at round start: GitHub search, `is:pr is:open in:title "LANE-Q
round"` on `pf_bridge`, found zero open `[LANE-Q] round *: claim` PRs --
lock free, no takeover needed (re-checked again immediately before opening
this round's own claim PR, still zero). Mailbox check (`grep -rl
"ADDRESSEE: Q" notes_to_chief/*.md`, skipping any with a `.CONSUMED.txt`
stub) found zero unconsumed letters -- nothing to consume this round.

Per `prompts/COMMON_LANE_ROUND.md`'s priority order, with no letter and no
new NOW.md line naming this lane directly, this round followed round
`92j6so`'s own "Next round" list:

1. **Re-check `RE-273` fresh.** Still `OPEN` in
   `pf_bridge/CLIENT_RE_QUEUE.md` line 1783 as of this round's own grep.
   Its own `[STATIC-ON-BRIDGE]` first path explicitly needs a pass beside
   the bridge's own client copy, which this cloud clone (no `GameClient`
   binary) cannot do -- still the one remaining named blocker of this
   lane's charter milestone sentence.
2. **Re-check `persistence_quest_state.py` landing on `main`.** `find
   pirate-force-server -iname persistence_quest_state.py` and `git log
   --all --oneline -- '*quest_state*'` in that repo: both still empty.
   LANE-DB's per-character `Quest.*` state door is still not open; the
   remaining 24 `Quest.*` names stay blocked.

Both blockers unchanged versus round `92j6so`. Per the standing backup
rule, this round picked up round `92j6so`'s own named recommendation for
`Instance.AddBonusPoint`/`AddBonusReward` and chose **path (b)**: accept
the SCORECOUNT trace's negative result and implement both as pure
invocation counters, same shape `CallScoreCount` already uses, with no
reward semantics claimed.

### What was built (full detail in `pirate-force-server`'s
`docs/SCRIPT_LANE.md`, round `vmm7vf` section)

- `InstanceRegistry.add_bonus_point`/`add_bonus_reward`: per-instance-id
  invocation counters, same cap/refusal posture as the pre-existing
  `call_score_count`/`set_lasting_time`. `add_bonus_point`'s optional
  argument (both real corpus call shapes exist: 0 args in
  `t_drp&insbospnt_himdfx.lua`, 1 arg in `t_insbospnt_himdfx.lua`) is
  accepted and discarded unread -- its meaning (point value vs.
  bonus-category id) is still genuinely unknown and this round does not
  guess it.
- Two new dispatch handlers in `RealInstanceNamespace.__getitem__`,
  arity-checked against the real corpus (`AddBonusPoint`: 0 or 1 args;
  `AddBonusReward`: 0 args only, matching its one call site).
- Both names moved from `STILL_STUBBED` (now empty) to `REAL_METHODS`.
  `Instance.*` is 9/9 real -- the first namespace in this lane's charter
  to reach 100%.
- Eight new/changed tests in `tests/test_script_lua_api_instance.py`
  (registry-level tally/independence/refusal/cap tests, namespace-level
  tests for both real corpus call shapes, arity-guard extension).

## Mailbox

Zero unconsumed letters addressed to `Q` this round (grep run fresh, not
quoted from a prior round). No `CANCELLED`/queue-triage action needed --
`RE-273` remains this lane's only open queue item with the right status.

## Tests + gates

- `PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_instance.py -q -rs`
  (no `lupa` in this clone): `37 passed, 4 skipped, 11 subtests passed`,
  after the adversary-fix commit.
- Full suite, `PYTHONPATH=src:tests python3 -m pytest tests/ -q`, run once
  on the final merged tree (`origin/main` was already `4e64b7d`, this
  branch's own base, so the merge step was a no-op): `12170 passed, 365
  skipped, 25068 subtests passed in 605.69s`, exit 0.
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`:
  PREFLIGHT PASS.
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server
  --pr-body <file> --pr-stage final`: PREFLIGHT PASS, marker check PASS
  (exactly one bare `PF-AUTOMERGE: v4` line).
- ASCII-only verified on every touched file (`instance.py`,
  `test_script_lua_api_instance.py`, `docs/SCRIPT_LANE.md`) by direct
  byte scan (zero bytes > 127), not assumed.

## ADVERSARY

`pf-adversary` invoked at round start (own isolated worktree), against the
new registry methods, dispatch handlers, and tests. Result returned
before push. Two confirmed findings, both fixed in a follow-up commit
before this PR opened:

1. `call_score_count`'s own docstring still called `AddBonusPoint`/
   `AddBonusReward` "named stubs, see `STILL_STUBBED`" -- stale the
   moment this round's own diff moved both names to `REAL_METHODS`.
   Fixed: corrected the cross-reference.
2. `test_every_still_stubbed_name_is_reachable_and_logs_its_own_line`
   iterated `for name in instance.STILL_STUBBED`, which this round's own
   change emptied -- the loop became silently vacuous (0 iterations,
   always green). Removed; a sibling test already asserts the empty dict
   directly.

No concurrency bug, sandbox-escape, or arity/coercion defect found: 32
threads x 5000 calls against one instance id landed the tally exactly on
80000/80000 with no lost updates; fuzzing the discarded `AddBonusPoint`
argument (NaN/inf, huge ints, a raising `__repr__`) caused no crash.
Adversary also raised one open design question, recorded verbatim in
`docs/SCRIPT_LANE.md`'s round section rather than answered here: since
nothing forces revisiting the SCORECOUNT join, this counter risks quietly
becoming the permanent implementation by default rather than a stated
placeholder -- named as a decision for whoever next has charter priority
on `Instance.*`, not resolved this round.

## `TWO_SESSIONS_SAME_SCENE:`

N/A -- `InstanceRegistry` state is per-instance-id process memory, same
shared-world shape the pre-existing `call_score_count`/`set_lasting_time`
already use and already have their own shared-registry proof
(`test_two_hosts_sharing_one_registry_see_each_other_s_writes`); this
round adds two more counters to the same registry, not a new state shape.

## nonclaims

1. Does not implement any SCORECOUNT-table lookup, does not compute or
   award an actual point value or item, and does not resolve which
   `CONSTDATA_TH__SCORECOUNT.tsv` row (if any) either calling script's
   instance actually uses -- round `92j6so`'s trace stands, unchanged, as
   a closed dead end for static tracing.
2. Does not move `RE-273` or land `persistence_quest_state.py` -- both
   re-checked fresh this round and both still blocked, unchanged from
   round `92j6so`.
3. Does not open a new `.npc` binary parser and does not open a new RE
   ticket for path (a) -- path (b) was chosen instead, per this round's
   own stated reasoning above.
4. Does not touch `runtime.py`/`app.py`/`store.py`, any other lane's
   write zone, `GAME_TEST_QUEUE.md`, or `CHIEF_CONTINUATION.md`. No new
   CORE-REQUEST opened this round.
5. Does not claim `pirate-force-server#915` is merged -- only that it is
   open, not draft, gate-preflight-passed, with the full suite green and
   `pf-adversary`'s findings fixed before it opened. Landing on `main` is
   next round's job to confirm (`git merge-base --is-ancestor`).

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/happy-tesla-vmm7vf`: four commits
  (Instance.* real, docs, adversary-fix, adversary-doc) -- PR `#915`,
  open, not draft, `PF-AUTOMERGE: v4` present from open, verified via GET
  after creation (`mergeable_state: "unstable"` is GitHub's own
  pending-check state, not a conflict -- `head.sha` `e9dedc8b` matches the
  last commit pushed).
- `pf_bridge` branch `claude/gracious-lovelace-vmm7vf`: this round file --
  claim PR `#1478`, marker added next to unlock, in this same round.

## Next round

1. Confirm `pirate-force-server#915` landed on `main`
   (`git merge-base --is-ancestor <sha> origin/main`) before anything
   else.
2. Re-check the same two named blockers fresh again (do not trust this
   round's file once it is more than one round old): `RE-273`'s status in
   `CLIENT_RE_QUEUE.md`, `persistence_quest_state.py` landing on `main`.
   Whichever clears first is the next round's first real-API job.
3. If both stay blocked: `docs/SCRIPT_LANE.md`'s round `vmm7vf` section
   names the fresh backup-work candidate -- a pure-function stub audit
   across `Guild.*`/`Party.*`/`Mob.*`/`Player.*` for a name with the same
   "unambiguous from every call site, no state door needed" shape
   `Instance.*`'s names had -- rather than starting from scratch.

SCOREBOARD: NONE | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอรอบนี้ (ทั้งสองบล็อกเกอร์ของ
charter สาย Q ยังปิดไม่ได้ -- RE-273 เปิดอยู่, ประตูสถานะเควสของ LANE-DB ยัง
ไม่ขึ้น main) แต่ Instance.* ครบ 9/9 real แล้ว (AddBonusPoint/AddBonusReward
เป็นตัวนับการเรียก ไม่อ้าง SCORECOUNT semantics) และ pf-adversary เจอสอง
จุดแล้วแก้ก่อน push | pirate-force-server#915 (สี่คอมมิต, full suite เขียว
12170/0 fail), pf_bridge claim PR #1478 (รอบนี้)
