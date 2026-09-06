[LANE-Q round 0rgg6q | 2026-09-06T07:28+07:00 | claim: pf_bridge#1447]

# LANE-Q round 0rgg6q -- recovered pirate-force-server#874 (Quest.CheckOpenTime, 1/25 Quest.* real), landed the CHIEF-GRANT exemption in the same commit, pf-adversary reviewed and its findings fixed

## What this round did, and what it moved on NOW.md

Per the previous round's (`xltzkx`) own "Next round" section and the
`0226` SYNC-NOTICE, this round's first job was recovering
`pirate-force-server#874` (`claude/hopeful-hopper-vqng2z`, commit
`93d0318`, `Quest.CheckOpenTime`), which was closed by the gate's
one-open-claude-PR lock (not a real test failure) before it could be
rebased, and never merged. Confirmed the branch was still intact via the
GitHub API (`git fetch`, not assumed) before starting.

Cherry-picked `93d0318` onto a fresh branch off current `main`
(`git cherry-pick -n 93d0318`). `main` had independently gained
`Instance.*` (7/9 real, round `4fxvsq`, PR #883) since the quest branch's
own base, producing four conflicts (`script_host.py`,
`test_script_host_spike.py`, `test_script_lua_corpus.py`,
`docs/PYTEST_SKIP_PINS.json`) -- resolved all four by combining both
sides' changes rather than picking one, verified against a live pytest
transcript that every touched module's observed skip count still matches
its pin exactly (module-by-module detail in the PR body).

Landed the CHIEF-GRANT exemption (`notes_to_chief/20260906_0510`) as the
first entry in `ALLOWED_SYMBOLS` in `tests/test_npc_interaction_wire.py`,
in this same commit as the code, per that grant's own condition. Verified:
`31 passed, 34 subtests passed` on that test file, matching the count the
grant itself measured on the original `#874` branch.

Ran `pf-adversary` at round start (in parallel with the full test suite,
per house rule), which reviewed the merge by actually installing `lupa`
in an isolated worktree and executing the tests, not just reading the
diff. It found three real defects (two in `docs/SCRIPT_LANE.md` --
wrong arithmetic in the status-table header, a dangling orphan sentence
fragment inherited from the original `#874` commit -- and one stale
docstring sentence in `script_host.py` omitting Instance from a
three-way union it already implements). All three fixed in a follow-up
commit; re-ran the targeted modules and the full suite again on the final
commit before push.

This moves `NOW.md`'s M2 milestone line ("ชั้นถัดไป = Trigger.* ของ Q")
indirectly: `Quest.CheckOpenTime` is not Trigger.*, but it is the queue
item chief's own team roster line (`FROM_CHIEF_R364`) already names as
part of this lane's charter (`Quest.* #874 -> 0510`), and closes out the
`0510` CHIEF-GRANT that was open since round `4fxvsq`.

## Mailbox

All letters addressed to `LANE-Q` in `notes_to_chief/` were already
consumed by round `xltzkx` (`.CONSUMED.txt` stubs present for all of
them, checked fresh this round, not assumed). Read
`notes_to_chief/FROM_CHIEF_R364_TO_ALL_20260906_0515.md` (broadcast to
all lanes, two items: a reaper-gate bug that closed 3 rounds' PRs without
merging, since fixed in `#1430`; and a queue-triage sweep for missing
`ATTENDED:` blocks) -- neither item names an action for LANE-Q beyond
awareness; its "new in queue" section confirms `RE-273` (this lane's own
trigger-id-to-script-file mapping ticket, opened via
`notes_to_chief/20260906_0155_LANE-Q-RE-TICKET-*`) is now numbered and
listed in `CLIENT_RE_QUEUE.md`, still `OPEN`, blocked on an RE runner
(Panya) -- nothing new to consume, this lane already wrote and submitted
that ticket's content verbatim in a prior round.

A new letter arrived mid-round (fetched via `git merge origin/main` right
before this round's own push):
`notes_to_chief/20260906_0727_LANE-A-TO-LANE-Q-world-registry-interface-and-trigger-hit-hook-point.md`,
LANE-A's answer to the `20260905_2056` COO-DECISION this lane's own
earlier round was waiting on. Read in full. It documents: (a) three
process-shared world registries that exist on `main` today
(`world_scene_registry`/`mob_ground_persistence`/`mob_death_persistence`,
keyed by case-folded scene folder, not raw scene id -- three named
footguns for Q specifically: the folder-vs-id key mismatch, `note_balance`
refusing HP=0, and every write door returning a `NoteOutcome.refusal`
string instead of raising, which this lane's fail-closed sandbox would
otherwise mask silently); (b) a hook point already safe to register on
today, `lane_hooks.hook("vital_inbound_trigger_vital")`, firing on every
inbound `TriggerVital` `0x1FB2` a ship-vs-trigger collision sends, with
`first_tag_value(...)` to read the trigger id out of the payload without
hand-rolling TLV parsing; and (c) what does NOT exist yet
(`Player.MobAppear`/live `Scene.*` movement -- no spawn/despawn/move door
that sends a frame -- and registry-1's own seed wiring into `runtime.py`
is an unbuilt CORE-REQUEST) with an explicit invitation to write back if
that blocks this lane rather than wait silently.

This is next round's job to use, not this one's: this round's own work
(`Quest.CheckOpenTime`) neither reads nor writes any world registry, and
the hook point is for `Trigger.*` real-implementation work, which is
blocked on `RE-273` (still `OPEN`). Consumed here (copied to
`consumed/`, `.CONSUMED.txt` stub placed) because it has been read and
its non-use explained, per house rule -- not because it has been acted
on. Whichever future round resumes `Trigger.*` (after `RE-273` answers,
or `GetContactMode` specifically) must re-read this letter's (a)/(b)/(c)
sections before writing that code, not re-derive them.

## Tests + gates

- `PYTHONPATH=src:tests python3 -m pytest tests/test_npc_interaction_wire.py -q -rs`:
  `31 passed, 34 subtests passed`.
- `PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_quest.py
  tests/test_script_host_spike.py tests/test_script_lua_corpus.py
  tests/test_script_lua_api_instance.py tests/test_script_lua_api_trigger.py
  tests/test_npc_interaction_wire.py -q -rs` (after the adversary-fix
  commit): `106 passed, 42 skipped, 101 subtests passed`.
- Full suite, first commit, on `origin/main` `a05ad4d` in:
  `python3 -m pytest tests -q -rs` = `11940 passed, 369 skipped, 23158
  subtests passed in 595.97s`, exit 0.
- Full suite again, final commit (after the adversary-fix commit):
  `11940 passed, 369 skipped, 23158 subtests passed in 563.70s`, exit 0.
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`:
  PREFLIGHT PASS (both before and after the adversary-fix commit).
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server
  --pr-body <file> --pr-stage final`: PREFLIGHT PASS, marker check PASS
  (exactly one `PF-AUTOMERGE: v4` line).
- pf-adversary: ran in an isolated worktree (own `git worktree`, `lupa`
  installed there only, uninstalled after, live checkout never written
  to), executed the tests rather than only reading the diff. Findings and
  fixes documented above and in the PR body.

## ASCII

Code, commit messages and the PR body are ASCII-only, verified
(`python3 -c "..."` scan for non-ASCII bytes on the PR body file found
only the mandated attribution emoji in the footer, matching the pattern
already present on merged PRs like `pirate-force-server#891`). This round
file and this letter are Thai-permitted per `prompts/COMMON_LANE_ROUND.md`,
written in English here to keep the technical narrative (merge conflict
detail, pin-count arithmetic) in the same vocabulary as the source and the
PR body.

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/hopeful-hopper-0rgg6q`: two commits
  (the cherry-pick + merge resolution, then the adversary-fix follow-up)
  -- PR `#900`, open, not draft, `PF-AUTOMERGE: v4` present from open,
  verified via GET after creation. `mergeable_state` was `unstable`
  (pending checks) at push time; separately confirmed with
  `git merge-tree` against the latest fetched `main` that no real conflict
  exists against the newest tip.
- `pf_bridge` branch `claude/kind-albattani-0rgg6q`: this round file --
  claim PR `#1447`.

## `TWO_SESSIONS_SAME_SCENE:`

N/A -- no shared-world/scene state touched. `Quest.CheckOpenTime` reads a
clock and returns a bool; no registry, not even a private one.

## nonclaims

1. Does not claim `pirate-force-server#900` is merged -- only that it is
   open, not draft, gate-preflight-passed, with the full suite green on
   the commit tested twice. Landing on `main` is next round's job to
   confirm (`git merge-base --is-ancestor`).
2. Does not claim the gate (Windows-only runtime) will be green -- the
   preflight tool explicitly does not promise that; out of scope for this
   clone.
3. Does not claim `RE-273` is answered -- still `OPEN` in
   `CLIENT_RE_QUEUE.md`, blocked on an RE runner. This lane already
   submitted its content; nothing further to do until an answer arrives.
4. Does not implement `Quest.GetWeekDay` or any other `Quest.*` name --
   `GetWeekDay` stays RE-blocked (undocumented weekday enum), the
   remaining 23 need LANE-DB's per-character state door, neither changed
   this round.
5. Does not touch `runtime.py`/`app.py`/`store.py`, any other lane's write
   zone, `GAME_TEST_QUEUE.md`, or `CHIEF_CONTINUATION.md`. No new
   CORE-REQUEST opened this round.
6. Does not claim pf-adversary reviewed anything beyond the files this
   round's own commits touched (`script_host.py`, `quest.py`,
   `test_script_host_spike.py`, `test_script_lua_corpus.py`,
   `test_script_lua_api_quest.py`, `test_npc_interaction_wire.py`,
   `docs/PYTEST_SKIP_PINS.json`, `docs/SCRIPT_LANE.md`) -- it did not
   re-review the rest of the 616-script corpus or the Trigger/Instance
   pins untouched by this merge.

## Next round

1. Confirm `pirate-force-server#900` landed on `main`
   (`git merge-base --is-ancestor <sha> origin/main`) before anything
   else; if chief's gate-red census tooling shows anything new, re-check
   fresh rather than assume clean.
2. `RE-273` (trigger-id -> `.lua` file mapping, `GetContactMode`'s own
   blocker) is still the one remaining named blocker of this lane's
   charter milestone ("ผู้เทสแล่นเรือชนทริกเกอร์แล้วสคริปต์ทำงาน") --
   check its status fresh in `CLIENT_RE_QUEUE.md`; if still `OPEN`,
   nothing to do but wait for an RE runner. If answered, that unblocks
   `Trigger.GetContactMode` (the highest-call-count remaining
   `Trigger.*` stub) as the very next real-API target. Whichever round
   picks this up must re-read
   `notes_to_chief/consumed/20260906_0727_LANE-A-TO-LANE-Q-*.md` first --
   it names the live hook point (`lane_hooks.hook("vital_inbound_trigger_vital")`),
   the trigger-id payload reader (`first_tag_value`), and three footguns
   in the world-registry write doors (scene-folder-vs-id key mismatch,
   HP=0 refusal, unchecked `.refusal` strings) that this lane's own
   fail-closed sandbox would otherwise mask.
3. If both of the above stay blocked: per the backup-work rule, audit the
   remaining stub surface (72 `Player.*` + `Guild.*`/`Party.*` low-call
   names) for another pure-function candidate needing neither the LANE-DB
   state door nor a wire frame this lane does not own, the same shape
   `CheckOpenTime` itself was.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ (Quest.CheckOpenTime ยังไม่มี live quest-accept flow เรียกมันจริงในเซิร์ฟเวอร์) แต่โค้ดที่หายไปตั้งแต่ PR #874 ถูกกู้กลับมาและขึ้น PR ใหม่แล้ว ผ่านทั้ง unit test เฉพาะจุด, ชุดเต็ม 11940 ผ่าน 0 ล้ม สองรอบ (ก่อนและหลัง adversary แก้), และ pf-adversary ยืนยันตรวจจริงด้วยการติดตั้ง lupa รันโค้ดจริง (ไม่ใช่แค่อ่าน diff) พบ 3 จุดในเอกสาร/docstring และแก้ครบก่อน push | pirate-force-server#900 (สองคอมมิต, full suite green x2), pf_bridge claim #1447
