# LANE-A round `xlraox`-continuation (`2134`) -- GT-194 pre-written for the UI-B vitalcount fix

## NOW.md (read first, per house rule)

Checked before anything else. `รอ Panya ติ๊ก` empty. `PANYA-ORDER 20260901_0215` still pauses all
numbered milestones (BUILD-001/002 stay parked). Of the current `งานด่วนตอนนี้` list, none is a
LANE-A action item this round: P-1/P-2/P-3 belong to other lanes or Codex/RE; GM-A, GM-B, UI-B (chat
command), UI-B (button), census latch are all either code-done-waiting-on-attended-GT (explicitly
"ไม่ใช่ตัวบล็อกสาย" per the new rule) or owned by GM/DB lanes. The one item that is LANE-A's
(UI-A/UI-B logout dispatch, per `FROM_CHIEF_R278` + the `1930` capture letter's own `ADDRESSEE`)
already has its build done and its CORE-REQUEST sent (round `xlraox`, PR pirate-force-server#505 /
pf_bridge#750, both merged) -- chief has not wired the fix yet (`vital_count == 1` still on `main`
at `logout_hypothesis.py:1457`, confirmed by grep this round). Nothing new addressed to LANE-A in
the mailbox since `xlraox` (checked `notes_to_chief` for unconsumed `ADDRESSEE: LANE-A` letters --
none found; both old outstanding ASK-COO letters from 08-30/08-31 already have `COO-DECISION`
replies and consumed stubs from earlier rounds).

**รอบนี้ขยับ NOW ข้อไหน**: ไม่ได้ขยับข้อไหน (ไม่มีสิทธิ์แก้ `NOW.md`, และไม่มีข้อไหนใน NOW ที่รอ
สายนี้ทำอะไรต่อตอนนี้ -- ตัวเดียวที่เป็นของสายนี้กำลังรอ chief) รอบนี้จึงเป็นรอบ "ไม่มีของใหม่ต้องสร้าง
ในเขตเขียนของตัวเอง" ตัวที่สองติดกันในความหมายที่ ADDENDUM v2 กฎ F พูดถึง (รอบ `xlraox` เองก็ตกอยู่
ในสภาพเดียวกันตอนจบ -- งานส่งไปรอ chief แล้ว "ไม่เร่ง") -- เลือกทำตามกฎ F ข้อ (ค): เขียน/ปรับใบเทสใน
คิว แทนการหยุดรอเฉย ๆ

## Section A -- prior PR fate (ADDENDUM v2 rule A)

Checked via GitHub MCP tools (available this session, unlike the prior 5 rounds' sessions):

    pirate-force-server#505 [LANE-A] ... LogoutVital request classifier ... -- state=closed, merged=true
    pf_bridge#750           [LANE-A] logout vital-count envelope gap ...   -- state=closed, merged=true

Both merged. Nothing to recover. `list_pull_requests(state=open)` on both repos shows zero
`[LANE-A]`-titled PRs open right now, so this round opens a fresh PR pair to claim the round lock
(per the lock rule).

## Mailbox (ADDENDUM v2 rule B)

Zero unconsumed `ADDRESSEE: LANE-A` letters at round start (checked `notes_to_chief/` for `.md`
files lacking a `.CONSUMED.txt` companion that also carry `ADDRESSEE: LANE-A` or `TO_LANE-A` --
none found beyond this lane's own outgoing, unanswered `2007` CORE-REQUEST, which this lane does not
consume itself). `RE-197` (opened by this lane last round, for lane C) has no answer yet -- checked,
not blocking. Nothing to consume this round.

## What this round built

The prior round's CORE-REQUEST is sent and explicitly non-blocking ("ไม่เร่ง"), so per rule 2
("คุณไม่ตอบคำถาม คุณสร้างของ ... ห้ามหยุดรอ") this round pre-wrote the attended-test ticket for the
fix chief hasn't landed yet, following the project's own `BLOCKED-ON-WIRING` pre-write convention
(precedent: `GT-190`, `GT-193` earlier in the same file) so no new ticket has to be opened later and
the tester can move the instant chief's fix lands.

Added **`GT-194 UI-B-LOGOUT-VITALCOUNT-ENVELOPE-FIX-001`** to the end of `GAME_TEST_QUEUE.md`:
objective, two-layer pass criteria (client-observable: real "exit game" click responds with a
pending vital in the session; wire/DB: regression-guard pytest + dispatch no longer returns
`logout_hypothesis_wrong_envelope_no_reply`), nonclaims, RECHECK block, links, numbered `194`
(highest prior `GT` was `193`, highest `RE` `197` -- both reconfirmed by direct grep, not assumed).

### pf-adversary pass (real `Task`/Agent tool available this session)

Ran the `pf-adversary` subagent against the new entry before commit (first real invocation on this
specific ticket -- prior 5 rounds lacked the `Task` tool entirely and had to self-checklist per
`AGENTS.md`'s `COO-DECISION 20260901_1744`; this session has it). Findings:

- Numbering, cited line numbers (`logout_hypothesis.py:1451-1465`, the `vital_count == 1` check at
  exactly `1457`), file/function existence, and the 18/18 + 122-passed/3-skipped test claims all
  independently re-verified clean in a disposable worktree -- no defect.
- **Two real defects found and fixed before commit**:
  1. RECHECK items 1 and 2 assumed two different working directories (parent-dir-relative vs
     repo-root-relative) -- would silently break if run back-to-back from one shell. Fixed: both
     items now self-contain `(cd pirate-force-server && ...)`.
  2. RECHECK item 1's original `grep -n "vital_count == 1"` over the whole file collides with an
     unrelated decoy hit at `logout_hypothesis.py:1560` (`classify_worldinfo_frame`, a different
     function, untouched by this fix) -- the grep would never cleanly report "no more matches" even
     after the real fix lands. Fixed: item 1 now `sed -n '1451,1465p' ... | grep ...` to scope the
     search to `classify_logout_attempt`'s own body only, with an explicit warning to re-locate the
     line range if the function moves.

Re-ran both fixed RECHECK commands by hand after editing: item 1 correctly still finds the
unfixed check right now (proves the gate is honest -- ticket stays `BLOCKED-ON-WIRING`, no false
`READY`), item 2 passes 122/3 skipped clean, no decoy hit anywhere.

## Files touched (pf_bridge only -- no server-repo write zone touched this round)

- `GAME_TEST_QUEUE.md` -- appended `GT-194` (BLOCKED-ON-WIRING), RECHECK fixed post-adversary
- `rounds/A_20260901_2134_gt194_logout_vitalcount_queue_entry.md` -- this file

No `notes_to_chief` letter needed this round -- nothing new to ask chief/COO beyond what `2007`
already covers, and no mailbox item was consumed.

## GitHub MCP tools status

Available and used this round (`mcp__github__*`, `Task`/Agent) -- unlike the prior five LANE-A
rounds flagged in `20260901_1355_KA1A-OBSERVATION-*`. Used them for the PR-fate check (Section A),
the real `pf-adversary` subagent call, and will use `update_pull_request` (not raw REST PATCH, not
GraphQL) for the draft-removal step per this lane's protocol.

## ตัวเลขที่วัดได้

- เทส regression guard: `pytest tests/test_logout_request_envelope.py tests/ -k logout -q` ->
  122 passed, 3 skipped (ยืนยันซ้ำหลังแก้ RECHECK)
- RECHECK item 1 (ก่อนแก้จริง): พบ 1 hit ที่บรรทัด 7 ของช่วง 1451-1465 (คือ `vital_count == 1` เดิม) --
  ถูกต้องตามสถานะ `BLOCKED-ON-WIRING`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลย -- รอบนี้เป็นเอกสารคิวเทสล้วน (ใบเทสที่รอ chief ต่อสายก่อนถึงจะรันได้) ไม่มีโค้ดใหม่ ไม่มี
โมดูลใหม่ การเปลี่ยนแปลงที่ผู้เล่นเห็นจริงยังรอรอบที่ chief แก้ `logout_hypothesis.py` แล้วผู้เทสยืนยัน
ด้วยตาผ่าน `GT-194` นี้
