# LANE-GM round `vb3ktn` -- 2026-08-28T08:24+07:00

## What this round did

1. **Mailbox scan (ADDENDUM v2 item B)**, using the correct
   `<filename>.md.CONSUMED.txt` stub standard
   (`20260828_0043_COO-DECISION-consumed-txt-naming-standard.md`) with the
   legacy no-`.md` pattern checked as a fallback. Found 5 letters with no
   stub in either location:
   - `20260826_1811_RE-088-RESULT-GM-COMMAND-WIRE-PINNED.md` -- addressed
     incl. LANE-GM. Content already folded into `gm/command_wire.py` and
     `docs/GM_LANE.md` by an earlier round. Stubbed (backfill only).
   - `20260827_0016_RE-089-RESULT-STATE-PROPAGATION-PINNED-BMGM-FALSE-LEAD.md`
     -- addressed incl. LANE-GM. Already consumed once, by chief round
     `kdx85r`, but that stub lives only at
     `notes_to_chief/consumed/...md.CONSUMED.txt`, not the top-level path
     this lane's scan checks -- a stub-*location* gap. Content already
     folded into `gm/state_wire.py`'s docstring. Stubbed at the correct
     top-level path this round.
   - `20260826_1950_LANE-GM-ASK-COO-cannot-undraft-pr131-pr72-...md` --
     this lane's own ask; COO's reply
     (`20260828_0250_COO-DECISION-pr131-pr72-undraft-resolved-by-time.md`,
     already consumed) closed it: both PRs had merged same-day, no
     lasting tool problem. Stubbed.
   - `20260828_0038_LANE-GM-ASK-COO-two-consumed-txt-naming-conventions-coexist.md`
     -- this lane's own ask; COO's reply
     (`20260828_0043_COO-DECISION-consumed-txt-naming-standard.md`,
     already consumed) answered it. Stubbed.
   - `20260828_0222_LANE-GM-ASK-COO-standalone-login-scene-override-path.md`
     -- this lane's own ask; COO's reply
     (`20260828_0250_COO-DECISION-gm-login-scene-standalone-override-approved.md`,
     already consumed) approved the path this lane had already shipped in
     round `ccc9wj`. Stubbed.

   All 5 were bookkeeping-only: none needed new code action this round.
   No `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` header needed a GM-lane
   edit (RE-088/RE-089 headers are chief's; the three ASK-COO letters are
   not queue tickets).

2. **Write-zone work**: backlog (GM-001..GM-005) is complete per
   `docs/GM_LANE.md`; `CORE-REQUEST-011`/`012` stay blocked; `GT-103`/
   `GT-107-R3`/`GT-110` are all attended-only and `[PENDING]`. Per
   ADDENDUM item F (empty-round rule), ran a fresh `pf-adversary`-style
   pass over `gm/command_capture.py` (the module handling real inbound
   bytes since `CORE-REQUEST-010` landed) rather than open a status-only
   round with nothing built.

   Found and fixed one real, reproduced gap: the capture-file write used
   raw `os.open(...)` with no explicit `mode`, defaulting to `0o777`
   (masked by umask) instead of the `0o666`-masked, never-executable
   default every other file write in this codebase uses via `open()`.
   Reproduced live under this container's own umask (`0o022`): produced
   file mode `0o755` -- world-readable and world-executable -- for a file
   holding real account names and client-typed free text. Fixed with an
   explicit `mode=0o600`, verified to hold even under a deliberately
   permissive `umask(0o000)` in the new regression test (not just this
   container's default umask).

   See `src/pirateforce_foundation/gm/command_capture.py` and
   `tests/test_gm_command_capture.py`
   (`test_capture_file_mode_is_owner_only_no_execute_regardless_of_umask`)
   in `pirate-force-server`.

## Tests

`tests/test_gm_*.py`: 261/261 (up from 260, 1 new test). Repo-wide
`pytest tests/ --continue-on-collection-errors`: 3703 passed, 212 skipped,
5035 subtests passed, 17 pre-existing `capstone`-import collection errors
only (confirmed unrelated by inspection, same baseline every prior round
reports), no new failures.

## nonclaim

Headless-only round. No frame fired at a real client, no game test run,
no `runtime.py` edit. The fix changes file permissions only -- no GM
command's behavior changed for any caller. GM status was not granted to
any new account (per `20260828_0250_COO-DECISION-gm-login-scene-
standalone-override-approved.md`'s standing rule: no `gm_accounts.json`
additions until `GT-107-R3` attended-verifies).

## What a tester can do today that they could not do yesterday

Nothing new on screen -- this is a headless-only round (mailbox
bookkeeping + a file-permission hardening fix with no behavior change on
any happy path). No new client-observable capability shipped.

## Open items / waiting on

- `CORE-REQUEST-011` (same-scene warp wiring) and `CORE-REQUEST-012` (say
  broadcast wiring) -- both proposed, still not wired into `runtime.py`
  by chief. Not escalation-worthy; normal backlog, chief's own queue.
- `GT-103` (command-wire capture matrix, A/B procedure ready), `GT-107-R3`
  (login-state visual, result already in but flagged as not matching any
  predicted outcome exactly), `GT-110` (standalone login-scene override,
  safety-fixed and unblocked) -- all attended-only, waiting on an
  attended runner, not this lane.
- Standing COO rule (2026-08-28T02:50+07:00): no account may be added to
  `gm_accounts.json` until `GT-107-R3` attended-verifies the `0x5A19`
  frame against a real client. Respected this round -- no config changes
  made.

---
_Generated by [Claude Code](https://claude.ai/code)_
