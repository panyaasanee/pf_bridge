# LANE-A round `xlraox` -- vital-count envelope gap found + structural classifier built

## NOW.md (read first, per house rule)

Checked before anything else. `รอ Panya ติ๊ก` empty. `PANYA-ORDER 20260901_0215` still pauses all
numbered milestones. Of the priority queue items (P-1/P-2/P-3, GM-A, UI-A, GM-B, UI-B, census
latch), **UI-A/UI-B are LANE-A's** per `FROM_CHIEF_R278` lines 49-50 (confirmed again by ka1-A's
19:30 capture letter's own `ADDRESSEE` line) -- everything else in that list is explicitly outside
this lane's write zone or explicitly not a blocker per the new rule ("code done, only attended GT
pending is not a lane blocker"). This round's work is squarely UI-A/UI-B evidence work.

**รอบนี้ขยับ NOW ข้อไหน**: ไม่ได้ขยับข้อไหนโดยตรง (ไม่มีสิทธิ์แก้ `NOW.md`) แต่งานรอบนี้เดินหน้า
"UI-B ปุ่มล็อกเอาต์จริง" ต่อจากใบ `1930` โดยพบสาเหตุ dispatch ที่เป็นไปได้จริง (ดูจดหมาย
CORE-REQUEST) ยังไม่ถึงขั้นให้ COO ขยับสถานะได้ (ต้องรอ chief wire แก้ก่อน แล้วให้ Panya ยืนยันด้วยตา)

## Section A -- prior PR fate (ADDENDUM v2 rule A)

Checked via public GitHub REST (read-only GET, no auth needed for public repo -- MCP tools were not
available this session, see the GitHub-tool section below):

    pf_bridge#743          [LANE-A] round ztl2u5 ... -- closed, merged_at set (2026-09-01T11:48:53Z)
    pirate-force-server#500 [LANE-A] RE-189 branch 2 ...    -- closed, merged_at set (2026-09-01T11:59:21Z)

Both merged. Nothing to recover. No open `[LANE-A]` PR exists in either repo right now (checked
`state=open` on both -- 0 results each), so this round opens a fresh PR pair to claim the round lock.

## Mailbox (ADDENDUM v2 rule B)

Unconsumed `ADDRESSEE: LANE-A` letters at round start: exactly one --
`20260901_1930_KA1A-CAPTURE-the-owner-clicked-both-UI-A-and-UI-B-buttons-herself-exact-bytes-plus-a-
design-problem-for-HYP-PF-040.md`. (`20260831_1037`, `20260831_1428`, `20260901_1435` all already
carried a `.CONSUMED.txt` stub from an earlier round -- confirmed via `ls`, not re-processed.)

Consumed this round: read in full, acted on its explicit first instruction ("compare the pin against
the real bytes -- LANE-A should do this first"), built what the comparison found, opened `RE-197` for
the one genuine unknown it raised (the `#1398` 51-byte frame) instead of researching it myself, and
left a `.CONSUMED.txt` stub with the original moved to `consumed/`.

## What this round found (the receipt is in the tests, not just this prose)

`notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-*.md` has the full writeup; summary:

1. subcode 3 ("return to character select") real capture == existing 34-byte pin, byte-for-byte. No
   bug on that side.
2. subcode 1 ("exit game") real capture is a genuinely different, legally-valid 119-byte frame (the
   client bundled 3 extra vitals into the same envelope; envelope vital-count byte 0x04, not 0x01).
   The LogoutVital entry itself (19 bytes) inside that frame is byte-identical to the pin.
3. Ran the fresh capture through the REAL, FROZEN `current/pf_login_game_server_v141.py` parser
   (read-only -- no edit) to confirm this is an actual dispatch-code gap, not just an observation
   about bytes: `logout_hypothesis.classify_logout_attempt` (the function `runtime.py` actually
   calls) hard-requires `parsed.vital_count == 1` before it even looks at the payload -- the real
   capture has `vital_count == 4` and is rejected outright (`"wrong_envelope"`), so
   `_dispatch_logout_hypothesis` never replies to a real, correct exit-game button click whenever the
   client's envelope carries any other pending vital. Also confirmed (with the real parser, not by
   hand) that `parsed.nested_payload[:14] == LOGOUT_REQUEST_PAYLOADS[1]` is `True` even though full
   equality is `False` -- the minimal safe fix is a prefix comparison, not a new payload shape.
4. Built `src/pirateforce_foundation/logout_request_envelope.py`: a new module (this lane's write
   zone -- no existing file touched) that classifies a LogoutVital request frame structurally
   (fixed 13-byte prefix + 1 count byte + 1 reserved byte + the fixed 19-byte LogoutVital entry),
   explicitly ignoring how many other vitals ride along. Fails closed on anything that does not match
   every fixed span exactly; never invents a byte.
5. `tests/test_logout_request_envelope.py`, 18 tests, all passing: cross-checks against the existing
   pins, cross-checks against both fresh capture frames (including running them through the real
   legacy parser as permanent evidence), and 9 fail-closed negative cases.
6. Left the actual dispatch-code fix as a CORE-REQUEST to chief (that file is locked outside a
   one-time per-round grant, and this round's write zone is new modules only) with two concrete
   options, a recommendation, and the exact line numbers.

## The HYP-PF-040 design question the same letter raised

Not this lane's decision to make unilaterally (a design-direction call, not a code fact) --
tagged `[สมมติของสาย A -- รอ COO ยืนยัน]` in the CORE-REQUEST letter with a recommended default
(treat the first dialog-open-push round as an 0x709E-viability experiment only, not the real UI-A
fix) and a genuine unknown (`#1398`'s 51-byte frame content) routed to `RE-197` for lane C instead of
being guessed at here.

## pf-adversary status this round (manual checklist, no Task tool)

`Bash, Read, Write, Edit, Glob, Grep` was the full tool list available this session -- no `Task`
tool, so no real `pf-adversary` subagent invocation was possible. Per `AGENTS.md`'s
`COO-DECISION 20260901_1744` rule, stated here plainly rather than silently substituted. Manual
checklist run against the two new files instead (both files, git-diff-clean confirmed against the
rest of the tree):

1. `production_allowed` -- not referenced anywhere in the new module; N/A.
2. Allowlist bypass -- N/A, no allowlist file touched.
3. Hash-pin drift -- confirmed zero edits to `logout_hypothesis.py` or any existing pin (`git status
   --porcelain` shows only the two new files).
4. CI silent-skip -- confirmed the new test file matches neither `GameClient` nor `capture_v141`
   (the gate's own exclusion regex), so it runs in the real `pytest_subset` step.
5. Off-by-one / fail-closed correctness -- proven empirically: 18/18 tests pass against real pinned
   bytes, real captured bytes (through the real legacy parser), and 9 dedicated malformed-input
   cases that must return `None`.
6. Side effects / wiring -- the new module has zero imports of `runtime.py`/`app.py`, is not called
   from any dispatch path yet (grepped), and performs no I/O; it is inert until chief wires it (or
   the equivalent two-line fix) in.

## GitHub MCP tools status (see CORE-REQUEST letter for the full writeup)

Not available this session (`allowed_tools` for this routine: `Bash, Read, Write, Edit, Glob, Grep`
only) -- the 5th occurrence of the pattern `notes_to_chief/20260901_1355_KA1A-OBSERVATION-*.md`
already flagged as LANE-A-specific. Worked around it for the PR-creation step only via the public/
authenticated GitHub REST API (`GITHUB_TOKEN` present in env) -- explicitly did NOT use REST for the
draft-removal step (that stays banned outright per this lane's protocol); left both PRs in draft with
the `PF-AUTOMERGE: v4` marker in the body from creation, for the reaper to pick up on its normal SLA.

## Files touched

pirate-force-server (2 new):
- `src/pirateforce_foundation/logout_request_envelope.py`
- `tests/test_logout_request_envelope.py`

pf_bridge (5, this round):
- `notes_to_chief/20260901_2007_LANE-A-CORE-REQUEST-logout-vitalcount-envelope-gap-classifier-built.md` -- new
- `notes_to_chief/20260901_1930_KA1A-CAPTURE-*.md.CONSUMED.txt` -- new stub
- `notes_to_chief/consumed/20260901_1930_KA1A-CAPTURE-*.md` -- moved original here
- `CLIENT_RE_QUEUE.md` -- appended `RE-197`
- `rounds/A_20260901_2007_xlraox_logout-vitalcount-envelope-gap-plus-classifier-built.md` -- this file

## ตัวเลขที่วัดได้

- เทสใหม่: 18/18 ผ่าน (`tests/test_logout_request_envelope.py`)
- เทส logout ทั้งกลุ่มหลังเพิ่มไฟล์: 122 passed, 3 skipped (`pytest -k logout`)
- ไบต์ที่เทียบสำเร็จ: subcode 3 -- 34/34 ไบต์ตรง · subcode 1 -- prefix 13 ไบต์ตรง + entry 19 ไบต์ตรง,
  ต่างที่ envelope count byte (1 ไบต์) และ trailing (85 ไบต์ ไม่ถูกตรวจ ไม่ถูกประดิษฐ์)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลย -- โมดูล+เทสใหม่ยังไม่ได้ wire เข้า dispatch จริง (ไฟล์ที่ต้องแก้ล็อกอยู่ที่ chief) รอบถัดไปที่
chief ต่อสายแล้วถึงจะมีพื้นผิวใหม่ให้เทสบนจอ
