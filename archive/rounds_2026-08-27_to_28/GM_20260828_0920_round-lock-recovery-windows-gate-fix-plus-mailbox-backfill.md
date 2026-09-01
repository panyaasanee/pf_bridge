# LANE-GM round `5f9lxw` -- 2026-08-28T09:20+07:00

## Round-lock check (ADDENDUM v2 step 1)

- `pf_bridge`: most recent `[LANE-GM]` PR was #285, `state=closed`,
  `merged=true` (HEAD `48f8712` is well past it). Landed clean, nothing to
  recover on this side.
- `pirate-force-server`: most recent `[LANE-GM]` PR was #185,
  **`state=closed`, `merged=false`** -- reaper-closed for gate RED. This is
  exactly the "did not land" case ADDENDUM v2 describes: the branch
  `claude/upbeat-knuth-wipchl` still existed on origin with nothing lost
  (confirmed by the reaper's own closing comment), so this round fetched
  it, cherry-picked the real work commit (`9bdc24b`) cleanly onto a fresh
  branch off current `main`, diagnosed the gate-RED cause from the actual
  failed run's job log, and fixed it in the same round (see below) instead
  of assuming the previous round's own status letter ("push done, waiting
  on merge") was still accurate -- it was not; `docs/GM_LANE.md`'s "round
  `vb3ktn`" section described a fix that was never on `main`.

## Root cause of the gate RED (pirate-force-server PR #185)

Job log for the failed run (`33132956815`, job `gate`):

```
AssertionError: 438 != 384 : 0o666
tests/test_gm_command_capture.py:219: AssertionError
```

`tests/test_gm_command_capture.py::test_capture_file_mode_is_owner_only_no_execute_regardless_of_umask`
(added by round `vb3ktn` alongside the real `os.open(..., mode=0o600)` fix)
asserted the resulting file mode is exactly `0o600`, unconditionally. That
holds on POSIX but not on Windows: NTFS has no POSIX permission-bit split,
and CPython's `os.open()` on Windows only ever reads the `mode` argument
for one bit (writable vs read-only) -- any owner/group/other split,
including `0o600`, is accepted and silently ignored. This project's gate
runs on `windows-latest` on purpose (`.github/workflows/gate-windows.yml`'s
own docstring names the real deployment target as the reason), so the
previous round's local `pytest` pass (this sandbox, POSIX) could not have
caught this -- the test was correct on the machine it was written on and
wrong on the machine that decides "green."

## Fix (this round)

- Cherry-picked `9bdc24b` (the real fix commit) verbatim onto a fresh
  branch off current `main` -- clean, no conflicts.
- Made the assertion `os.name`-conditional: exact `0o600` on POSIX
  (unchanged strength, still catches the original `0o777`-default bug on
  every machine that can enforce it), and on Windows only "the write
  succeeds and a real file exists" -- the strongest statement this
  platform can actually make about the outcome, not a silently narrowed
  test.
- Documented the platform split in both the `gm/command_capture.py`
  docstring at the `os.open` call site and in `docs/GM_LANE.md` (new
  "Round `vb3ktn`'s own PR did not merge" section), including the
  security-relevant consequence: this means `mode=0o600` gives real
  owner-only enforcement in every POSIX sandbox/CI this project runs, but
  gives **no enforcement on the real Windows production bridge**, where
  access is governed by the containing directory's NTFS ACL instead --
  outside this lane's write zone (no `pywin32`/ACL API available here).
  Not a new regression -- the pre-`vb3ktn` code had the identical Windows
  exposure, just via a different (also-ineffective-on-Windows) default
  mode.
- Filed `notes_to_chief/20260828_0920_LANE-GM-ASK-COO-capture-file-mode-not-enforced-on-windows.md`
  asking COO whether this residual exposure is acceptable as-is (single-
  operator bridge, no other OS users) or needs a follow-up
  `CORE-REQUEST` for an ACL-capable dependency. Not blocking -- this
  round's own PR is not held up on the answer.

## Mailbox (ADDENDUM v2 step B)

Scanned `notes_to_chief/` for anything addressed to `LANE-GM` (or `cc:`)
without a `.CONSUMED.txt` stub in either the top-level path or
`notes_to_chief/consumed/`. Found 4, all already actioned by earlier
rounds -- pure bookkeeping backfill, no new code action:

- `20260827_2131_LANE-GM-STATUS-adversary-sweep-newer-modules-one-fix.md`
  -- this lane's own STATUS letter, no reply owed. Stubbed.
- `20260827_2318_LANE-GM-STATUS-second-idle-round-rule-f-invoked.md` --
  same. Stubbed.
- `20260828_0727_LANE-GM-STATUS-capture-quota-estimate-undercount-fixed.md`
  -- same. Stubbed.
- `20260827_2259_CHIEF-REPLY-KA1A-GT110-console-tokens-plus-scene2-login-path-confirmed.md`
  -- addressed to attended session "กะ1-A", `cc: LANE-GM`. Its GT-110
  section ("chief agrees with decoupling override from GM status") was
  already implemented by round `ccc9wj` (`pf_bridge` PR #258 /
  `pirate-force-server` PR #163, `gm/login_scene_override.py`) *before*
  this letter was even written -- confirmed by checking the merge
  timestamps (`ccc9wj` merged 2026-08-27T19:32Z, this letter is dated
  2026-08-27T22:59Z). No action needed. Stubbed.

No `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` header edit was needed --
none of the 4 are queue tickets this lane opened.

## Tests

`tests/test_gm_*.py`: 261/261 (unchanged count from before the gate-RED
recovery -- one assertion strengthened/branched by platform, none added,
none removed, none narrowed on the platform where it already worked).
Repo-wide `pytest tests/ --continue-on-collection-errors`: 3706 passed,
212 skipped, 5035 subtests passed, 17 pre-existing `capstone`-import
collection errors only (same baseline every prior round reports,
confirmed unrelated by inspection -- the `3703` -> `3706` delta is `main`
having advanced with LANE-B's RE-122 stat-fabrication-guard test in the
meantime, not this round). No new failures. เขียว (local pytest, this
session, POSIX sandbox -- exercises the POSIX branch of the fixed test;
the Windows branch is exercised for real by the gate this PR runs on).

## nonclaim

Headless-only round. No frame sent to a real client, no game test run, no
`runtime.py` edit. The fix changes test/documentation correctness and one
code comment only -- the actual `gm/command_capture.py` write behavior is
byte-identical to what round `vb3ktn` already shipped (same cherry-picked
commit). GM status was not granted to any new account (no `gm_accounts.json`
change this round -- still respecting the 2026-08-28T02:50+07:00 COO
standing rule to wait for `GT-107-R3` attended-verification).

## What a tester can do today that they could not do yesterday

Nothing new on screen. This round exists because the previous round's real
fix (capture-file permission hardening) never actually reached `main` on
the server side -- it does now, plus the test that verifies it no longer
falsely reports the fix as broken (or, if left unfixed, would have kept
reaper-closing every future round's PR until someone untangled why the
gate stayed red on a change that looked correct in every local run).

## Open items / waiting on

- `CORE-REQUEST-011` (same-scene warp wiring) and `CORE-REQUEST-012` (say
  broadcast wiring) -- both proposed, still not wired into `runtime.py` by
  chief. Normal backlog, chief's own queue, not escalation-worthy.
- `GT-103`, `GT-107-R3`, `GT-110` -- all attended-only, waiting on an
  attended runner, not this lane.
- New this round: `20260828_0920_LANE-GM-ASK-COO-capture-file-mode-not-enforced-on-windows.md`
  -- not blocking, this lane keeps working regardless of the answer.
- Standing COO rule (2026-08-28T02:50+07:00): no account may be added to
  `gm_accounts.json` until `GT-107-R3` attended-verifies. Respected.

---
_Generated by [Claude Code](https://claude.ai/code)_
