# LANE-GM round `usinho` -- 2026-08-28T10:35+07:00

## Round-lock check (ADDENDUM v2 step A)

- `pf_bridge`: most recent `[LANE-GM]` PR was #285, `state=closed`,
  `merged=true` (`pull_request_read` confirmed directly -- the `list_pull_requests`
  list endpoint's `merged` field returned `false` for every PR in the list
  including this one, a REST list-endpoint quirk, not a real signal; always
  confirm via `pull_request_read` `get` on the specific PR before trusting
  it). Nothing to recover.
- `pirate-force-server`: most recent `[LANE-GM]` PR was #188 (round `5f9lxw`'s
  own recovery of round `vb3ktn`'s stranded fix), `merged=true`, confirmed
  the same way. Nothing to recover.
- Open PRs at round start in both repos: one each, both `[LANE-E]` (`pf_bridge#294`,
  `pirate-force-server#191`) -- not this lane's lock, not touched.

## Mailbox (ADDENDUM v2 step B)

One item pending: `notes_to_chief/20260828_0945_COO-DECISION-capture-file-windows-acl-risk-accepted.md`,
answering this lane's own `20260828_0920_LANE-GM-ASK-COO-capture-file-mode-not-enforced-on-windows.md`.
COO accepts the residual Windows-ACL risk as proposed (single-operator
bridge, no dependency added). No code action needed -- consumed and
stubbed at `notes_to_chief/20260828_0945_COO-DECISION-capture-file-windows-acl-risk-accepted.md.CONSUMED.txt`
(original copied to `notes_to_chief/consumed/`).

Also scanned everything dated after `0920` for an `ADDRESSEE: LANE-GM` tag
addressed to this lane -- none found (`20260828_0925_GT116-121-120-RESULT`
cc's "สาย GM/B" but its `ADDRESSEE` tags are `chief`/`LANE-A` only, and its
content is not about this lane's write zone). No queue-header edits needed.

## Work this round: real defect found and fixed via `pf-adversary`

Ran a full adversarial sweep of `src/pirateforce_foundation/gm/` (first
since round `i76is0`) in `pirate-force-server`. Findings and fixes, in
order:

1. **[CONFIRMED, fixed]** `gm/commands.py`'s `log_gm_command` created its
   ndjson audit-log file (full `say`-message bodies and other GM-typed
   free-text) via builtin `open("a")` with no explicit mode -- the exact
   permission-bug class round `vb3ktn` fixed for `gm/command_capture.py`'s
   `os.open()` call, in a sibling file that fix never touched. Fixed with
   the same `os.open(..., mode=0o600)` pattern.
2. **[CONFIRMED, fixed]** Both `log_gm_command`'s and `capture_raw_gm_command`'s
   containing directories were created via `mkdir` with no explicit mode --
   world-writable under a permissive umask even though the files inside
   are `0o600`. First pass added `mode=0o700` to both leaf `mkdir` calls.
3. **[CONFIRMED, fixed]** A follow-up `pf-adversary` verification pass on
   that exact diff (required by house rule before any non-typo commit)
   found the directory fix was incomplete: `Path.mkdir(exist_ok=True)`
   never chmods a directory that already exists, and `DEFAULT_LOG_PATH`
   and `DEFAULT_CAPTURE_ROOT` share the literal parent `capture/`
   (`.gitignore` documents it as never cleaned up) -- whichever function
   ran first on a real host would lock that shared parent at whatever mode
   the umask in effect at that one moment produced, forever, regardless of
   every later call's own umask. Fixed with an unconditional
   `os.chmod(leaf_dir, 0o700)` on every call, plus two tests that create
   the directory loose (`0o777`) first to prove the retightening actually
   fires (the scenario the first-pass tests could not catch, since they
   only ever exercised first creation).

Same Windows caveat as `vb3ktn`'s original fix applies to every mode bit
touched this round: NTFS ignores the owner/group/other split, so none of
this is real enforcement on the actual production bridge, only on every
POSIX CI/sandbox this project runs in. Not a new regression, and not
re-flagged to COO -- it is the identical, already-accepted risk the
standing `20260828_0945_COO-DECISION` covers, not a new one.

Things the adversary sweep looked hard for and did not find broken (see
full report in the agent transcript, summarized here for the record): GM
allowlist bypass (no path found where a non-`gm_accounts` account gets any
GM-only response), the `str`-subclass `__eq__`/`__hash__` bypass class
(re-checked at every set/dict-membership boundary, all still use
`type(x) is not str`), the capture-quota byte-estimate math (re-derived
independently, still conservative), path traversal in capture filenames,
TOCTOU on the capture-file lock, and the rate-limiter/quota lock scope --
all clean.

## Tests

`tests/test_gm_*.py`: 266/266 (up from 261 -- 5 new tests: 1 file-mode
test for `log_gm_command`, 2 first-creation directory-mode tests, 2
pre-existing-loose-directory retightening tests; 0 removed, 0 narrowed).
Repo-wide `pytest tests/ --continue-on-collection-errors`: 3717 passed,
212 skipped, 5035 subtests passed, 17 pre-existing `capstone`-import
collection errors only (same baseline every prior round reports), no new
failures. เขียว (local pytest, this session, POSIX sandbox -- the new
tests skip their assertion body on non-POSIX, same pattern as the existing
capture-file-mode test).

## nonclaim

Headless-only round. No frame sent to a real client, no game test run, no
`runtime.py` edit, no `gm_accounts.json` change (still respecting the
standing COO rule to wait for `GT-107-R3` attended-verification -- still
`[PENDING]`, no new result since round `y2nhzz`'s `0326` letter). Pure
security-hardening inside this lane's own write zone; no `gm/` command
behavior changed for any caller, no wire fact, no RE citation involved.

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี — รอบนี้ headless-only ล้วน อุดช่องโหว่สิทธิ์ไฟล์/โฟลเดอร์เท่านั้น ไม่มีผลต่อพฤติกรรมคำสั่ง
GM ใด ๆ ที่ผู้เทสเห็นบนจอ

## Open items / waiting on

- `CORE-REQUEST-011`/`012` -- still blocked on chief, normal backlog.
- `GT-103`, `GT-107-R3`, `GT-110` -- all attended-only, waiting on an
  attended runner.
- Standing COO rule (2026-08-28T02:50+07:00): no account may be added to
  `gm_accounts.json` until `GT-107-R3` attended-verifies. Respected.
- Drive-by doc fix: `docs/GM_LANE.md`'s round `5f9lxw` entry had an unfilled
  `<this-round-timestamp>` placeholder in its own closing link -- filled in
  with the real filename this round, alongside adding this round's own
  entry.

---
_Generated by [Claude Code](https://claude.ai/code)_
