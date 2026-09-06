[LANE-Q round gk0dz4 | 2026-09-06T14:09+07:00]

# LANE-Q round gk0dz4 -- recover pirate-force-server#915 (stale REAL_METHODS guard)

## Deviation from COMMON_LANE_ROUND's branch/lock convention -- stated up front

This session's two branches (`pf_bridge` `claude/kind-albattani-gk0dz4`,
`pirate-force-server` `claude/hopeful-hopper-gk0dz4`) are fixed by the
harness that launched this session, not freely assigned by `claude/*`
random-branch-per-push the way `prompts/COMMON_LANE_ROUND.md` describes,
and this session may not push to any other branch name. This round
therefore did not open a separate `[LANE-Q] round <id>: claim` lock PR
before starting work (there is nowhere else to push a claim branch from);
it used round id `gk0dz4` (the shared suffix of both assigned branches)
and did the lock/mailbox/AGENTS-SS7/last-round checks below before
touching anything, same as the checklist requires, then worked and pushed
directly on the assigned branches. Flagging this plainly rather than
writing the round as if the branch had been freely chosen.

## Round-start checks

- **Lock**: `search_pull_requests` on `pf_bridge`,
  `is:pr is:open in:title "LANE-Q round"` -- zero open claim PRs. No
  takeover needed.
- **Mailbox**: `grep -l "ADDRESSEE: LANE-Q" notes_to_chief/*.md`, skipping
  any with a `.CONSUMED.txt`/`.md.CONSUMED.txt` stub -- one unconsumed
  letter, `20260906_1246_SYNC-NOTICE-pirate-force-server-pr915-closed-
  never-merged.md` (consumed this round, see below). Also read
  `FROM_CHIEF_R364_TO_ALL_20260906_0515.md` (addressed to all lanes
  including Q, cc COO/Panya) -- consumed this round; no action item
  specific to LANE-Q beyond the already-tracked `RE-273` mention and the
  reaper-bug awareness (this round's own branch is fixed, not
  freshly-cut, so the fixed reaper's file-count heuristic does not apply
  the same way -- noted, not acted on further).
- **`AGENTS.md` SS7**: re-read fresh this round; nothing new since last
  round's own reading that changes LANE-Q's write zone or queue.
- **Last round file**: `rounds/Q_20260906_1216_vmm7vf_instance-
  addbonuspoint-addbonusreward-real.md`'s own "Next round" list, item 1:
  "Confirm `pirate-force-server#915` landed on `main`
  (`git merge-base --is-ancestor <sha> origin/main`) before anything
  else." It had not: the SYNC-NOTICE letter above is exactly this --
  `#915`'s gate went RED (job `34013631038`) and the PR was closed
  unmerged, branch `claude/happy-tesla-vmm7vf` kept.

## What this round did

Per the SYNC-NOTICE's own instructions ("read the gate log for the head
commit and find the ONE step that failed... fix that cause on the branch
above... do not start the round over"):

1. Fetched job `34013631038`'s full log (`get_job_logs`, `job_id
   101433574720`, no `failed_only` truncation) and found the actual
   failure (not visible in the last-200-lines view alone, which only
   shows the skip census + summary): `pytest_subset exit=1`, one failure --
   `ApiNamespaceStubBehaviourTests.
   test_the_7_real_instance_names_are_excluded_above_not_forgotten` in
   `tests/test_script_host_spike.py`, `AssertionError: Items in the first
   set but not the second: 'AddBonusPoint', 'AddBonusReward'`.
2. Root cause: round `vmm7vf` widened `lua_api/instance.REAL_METHODS`
   from 7 to 9 names and correctly updated
   `tests/test_script_lua_api_instance.py`, but a SECOND, independent
   regression guard on the same `REAL_METHODS` constant, in
   `tests/test_script_host_spike.py`, was not updated -- exactly the
   silent-drift failure mode that guard exists to catch, caught by the
   gate rather than by `pf-adversary` or a human (round `vmm7vf`'s own
   file records `pf-adversary` running against the new registry code and
   the OTHER spike-file test it touched, but not this one, which its own
   diff did not modify).
3. Fetched branch `claude/happy-tesla-vmm7vf` (kept per the SYNC-NOTICE,
   base `4e64b7d`, already an ancestor of current `main`) and
   cherry-picked its four commits onto this session's own branch --
   clean, no conflicts, base file unchanged since the fork point.
4. Fixed the actual cause: renamed the guard to
   `test_the_9_real_instance_names_are_excluded_above_not_forgotten`,
   extended its frozenset with `AddBonusPoint`/`AddBonusReward`, and
   updated `docs/PYTEST_SKIP_PINS.json`'s `lupa_package` pin for that
   module to the renamed test (count unchanged at 21 -- rename only, no
   test added/removed, verified against
   `tools/pf_pytest_precondition_census.py`'s own walker via
   `tests/test_pytest_precondition_census.py`, not hand-counted).
5. Re-checked this lane's two named charter blockers fresh, per round
   `vmm7vf`'s own "Next round" item 2, before treating this recovery as
   the whole round: `RE-273` still `OPEN` in `CLIENT_RE_QUEUE.md` line
   1783 (needs the bridge's own client copy, which this cloud clone does
   not have); `persistence_quest_state.py` still does not exist anywhere
   in `pirate-force-server` (`find` + `git log --all -- '*quest_state*'`
   both empty). Both unchanged from round `vmm7vf` -- this round's real
   work is the recovery, not new `Trigger.*`/`Quest.*` API surface.
6. Merged `origin/main` into the branch as the final step before each
   push (twice -- `main` moved once mid-round, LANE-A's `#919`, zero file
   overlap with this round's two touched files) and ran the full suite
   after each merge.

## Tests + gates

- `PYTHONPATH=src:tests python3 -m pytest tests/test_script_host_spike.py
  tests/test_script_lua_api_instance.py
  tests/test_pytest_precondition_census.py -q -rs`: green (`37 passed, 25
  skipped, 11 subtests passed` on the two spike/instance files; `69
  passed, 1092 subtests passed` on the census file -- no `lupa` in this
  cloud clone, same gap every prior round records).
- Full suite, `PYTHONPATH=src:tests python3 -m pytest tests/ -q -rs`, run
  THREE times this round, not the usual once, because the merge-then-test
  ordering surfaced a real problem each of the first two times:
  1. Before the fix, on the four cherry-picked commits alone: `1 failed,
     11204 passed, 143 skipped` -- reproduced the exact gate failure
     above, confirming the root cause before touching anything.
  2. After the fix, before the second `origin/main` merge: `12209 passed,
     369 skipped, 25084 subtests passed in 601.07s` -- green.
  3. After merging `origin/main` a second time (LANE-A's `#919` landed
     mid-round): run in background at push time; result not yet returned
     when this file was written (see nonclaims).
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`:
  PREFLIGHT PASS (both before and after the second merge).
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server
  --pr-body <file> --pr-stage final`: PREFLIGHT PASS, marker check PASS
  (exactly one bare `PF-AUTOMERGE: v4` line), verified twice (body edited
  once between checks to move ADVERSARY from UNAVAILABLE to PENDING
  wording -- re-verified after the edit, not assumed still valid).

## ADVERSARY

`pf-adversary` invoked (own isolated worktree) at the point this round
found the root cause, not held back until push, per `AGENTS.md` SS7's
three-line rule. Result had not returned when PR `#924` needed to open,
so per the same rule this round pushed and opened it anyway
(`ADVERSARY_PENDING pirate-force-server#924` at that point) rather than
holding the round's lock open to wait; self-review performed in the
meantime (read every hunk in `git diff --cached` before the commit, ran
the targeted mutation by hand).

**Result, returned before this round closed: no real defects found.**
Independently read `lua_api/instance.py`'s actual `REAL_METHODS` (not
this round's claim) and confirmed the renamed guard's frozenset matches
it member-for-member; `git grep`'d the whole tree for the old test name
and found only the already-correct pin-file rename plus one
historical-narrative reference in `docs/SCRIPT_LANE.md`'s own `vmm7vf`
section (correctly left alone, an accurate record of what that round did
at the time -- matches this round's own historical-vs-live-doc
distinction, independently reached); verified `PYTEST_SKIP_PINS.json`
stays valid JSON with its `count` matching its `tests` array length and
no other entry touched; ran the three affected test files clean (106
passed, 25 skipped for missing `lupa`, 1103 subtests, 0 failed); and
proved the fix is not vacuous by reverting just the frozenset body while
keeping the rename in an isolated worktree, which reproduced the fresh,
correct failure (calling the guard's test function directly to bypass
`unittest`'s class-level skip dispatch, since this interpreter has no
`lupa`). Full result recorded in `pirate-force-server`'s
`docs/SCRIPT_LANE.md`, round `gk0dz4` section, and in PR `#924`'s body
(both updated this round after the result returned).

One open, unresolved (not blocking) design question raised by the
reviewer, recorded verbatim rather than answered: is there a static check
(beyond each module's own hand-maintained guard test) that would catch
the *next* time a `REAL_METHODS`/`STILL_STUBBED`-shaped set in any
`lua_api/*.py` module widens without its sibling guard test in
`test_script_host_spike.py` being updated -- or does every future
widening rely on a human (or another gate run) noticing the same two-file
coupling by hand, as happened here? Named as a decision for whoever next
touches this pattern, not resolved this round.

## `TWO_SESSIONS_SAME_SCENE:`

N/A -- this round's diff touches only a test's hardcoded expected set and
a JSON pin-file entry (plus the four cherry-picked `Instance.*` commits,
whose own shared-world proof is `vmm7vf`'s own file, unchanged here). No
runtime/world state shape touched.

## Mailbox

Three letters consumed this round:
- `20260906_1246_SYNC-NOTICE-pirate-force-server-pr915-closed-never-
  merged.md` -- acted on directly, this whole round.
- `FROM_CHIEF_R364_TO_ALL_20260906_0515.md` -- read; the reaper-bug fix
  (`#1430`) and the `ATTENDED:` queue triage table name no LANE-Q items;
  `RE-273`'s mention there matches what this round independently
  re-confirmed still `OPEN`. No further action.
- `FROM_CHIEF_R370_TO_ALL_20260906_1456.md` (arrived mid-round, picked up
  on the second `pf_bridge` `origin/main` merge) -- read; new reaper
  ghost-claim/`SUPERSEDED-BY:`/`DUPLICATE-OF:` auto-close rules (item 1)
  and LANE-GM/LANE-K/LANE-UI/LANE-A/LANE-B items (2-4) name no LANE-Q
  action. Item 5's two tooling lessons (self-test fixtures before central
  files, three-way check on `.github/workflows/*.yml` edits) noted for
  future reference; this round touched neither.

No `CANCELLED`/queue-triage action needed on LANE-Q's own items --
`RE-273` remains this lane's only open queue item, status unchanged and
correctly `OPEN`.

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/hopeful-hopper-gk0dz4`: five
  commits (four cherry-picked from `claude/happy-tesla-vmm7vf` unchanged,
  plus this round's own fix commit), a merge commit for `origin/main`'s
  `#919`, a `docs/SCRIPT_LANE.md` commit recording the clean adversary
  result, and a second merge commit for `origin/main`'s `#921` -- PR
  `#924`, open, not draft, `PF-AUTOMERGE: v4` present, verified via GET
  after both the initial open and the final body update (head sha
  `c5fb739` confirmed matching the last push at GET time;
  `mergeable_state: "unstable"` is GitHub's own pending-check state, not a
  conflict).
- `pf_bridge` branch `claude/kind-albattani-gk0dz4`: this round file plus
  three `.CONSUMED.txt` stubs (originals copied to `notes_to_chief/
  consumed/`, not moved) -- PR `#1495`, open, not draft,
  `PF-AUTOMERGE: v4` present, verified via GET.

## nonclaims

1. Does not claim `pirate-force-server#924` is merged, or that its gate
   is green -- only that `pf_gate_preflight.py` passed on every push and
   the full local suite passed green three times (once per merge of a
   moving `main`), plus `pf-adversary`'s independent result was clean.
   Landing on `main` is next round's job to confirm
   (`git merge-base --is-ancestor <sha> origin/main`).
2. Does not implement any new `Trigger.*`/`Quest.*`/other API name --
   this round is entirely recovery of already-real work, not new charter
   progress. Both named blockers (`RE-273`, `persistence_quest_state.py`)
   re-checked fresh and both still stand.
3. Does not open a claim PR or use a freshly-cut `claude/*` branch, for
   the reason stated at the top of this file -- this is a structural
   mismatch between this session's harness-assigned branches and
   `prompts/COMMON_LANE_ROUND.md`'s branch-per-round convention, not a
   choice made mid-round. Whoever runs the LANE-Q schedule next may hit
   the same mismatch; this file names it explicitly rather than silently
   working around it every time.
4. Does not touch `runtime.py`/`app.py`/`store.py`, any other lane's
   write zone, `GAME_TEST_QUEUE.md`, or `CHIEF_CONTINUATION.md`. No new
   CORE-REQUEST opened.
5. Does not resolve the adversary's one open design question (a static
   coupling check across `lua_api/*.py` modules for the
   `REAL_METHODS`/guard-test pattern this round's bug was an instance of)
   -- recorded as a decision for whoever next touches this pattern, not
   answered here.

## Next round

1. Confirm `pirate-force-server#924`'s final head landed on `main`
   (`git merge-base --is-ancestor <sha> origin/main`) before anything
   else.
2. Re-check the same two named blockers fresh again: `RE-273`'s status in
   `CLIENT_RE_QUEUE.md`, `persistence_quest_state.py` landing on `main`.
   Whichever clears first is the next round's first real-API job.
3. If both stay blocked: `docs/SCRIPT_LANE.md`'s round `vmm7vf` section
   names the fresh backup-work candidate -- a pure-function stub audit
   across `Guild.*`/`Party.*`/`Mob.*`/`Player.*` for a name with the same
   "unambiguous from every call site, no state door needed" shape
   `Instance.*`'s names had.

SCOREBOARD: NONE | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอรอบนี้ (รอบนี้คือการกู้งานที่
เสร็จแล้วจากรอบก่อนกลับขึ้น main หลังเกตแดง ไม่ใช่ฟีเจอร์ใหม่ -- Instance.*
9/9 real ยังรอ #924 ขึ้น main อยู่ ทั้งสองบล็อกเกอร์ของ charter สาย Q ยังปิด
ไม่ได้เหมือนเดิม -- RE-273 เปิดอยู่, ประตูสถานะเควสของ LANE-DB ยังไม่ขึ้น
main) | pirate-force-server#924 (ห้าคอมมิต + merge, full suite เขียวสองรอบ
12209/0 fail, preflight PASS สองรอบ), pf_bridge round file นี้
