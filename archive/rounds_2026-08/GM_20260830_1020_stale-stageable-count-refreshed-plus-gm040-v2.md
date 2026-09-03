# Round `2q9lxx` — mailbox clean, one stale-count doc fix, CORE-REQUEST-GM-040 escalated a second time

[2026-08-30T10:20+07:00 · HEAD boot: `pirate-force-server` `main` @ `8c5d9c4` /
`pf_bridge` `main` @ `eea3c75` (both re-fetched at round start) · job/PR numbers below]

## Round-lock check (ADDENDUM v2 §A)

`list_pull_requests(state=open)` on both repos before claiming: only `[LANE-B]`
(`pirate-force-server#300` / `pf_bridge#476`, round `fxury2`) and `[LANE-E]`
(`pirate-force-server#299` / `pf_bridge#475`, round `hd6tac`) open. No
`[LANE-GM]` PR open — lock is clear, no cherry-pick recovery needed. (The
previous round, `h4v9wq`, already confirmed both of this lane's last closed
PRs — `pirate-force-server#297` and `pf_bridge#472` — merged=true via
`pull_request_read(get)`, not the list call's unreliable `merged` field.)

Claimed the lock: `pirate-force-server#301`, `pf_bridge#477`, both opened
draft with `round claim: 2q9lxx` empty commits.

## Mailbox (ADDENDUM v2 §B)

Grepped `ADDRESSEE: LANE-GM` and `LANE-GM` case-insensitively across
`notes_to_chief/*.md`. Every incoming letter addressed to this lane already
has a `.CONSUMED.txt` stub sitting next to it (confirmed with a loop testing
each candidate file individually, not by eyeballing a listing). The newest
`FROM_CHIEF_R2xx_TO_ATTENDED_*` letters (through R236, 08:55) are all to the
attended-tester lane, none carry `ADDRESSEE: LANE-GM` or mention this lane.
**Mailbox: nothing new to consume this round.**

## Why this round is not empty (ADDENDUM v2 §F)

The immediately preceding round (`h4v9wq`) was verify-only with zero code
change — two empty rounds in a row is against house rule, so this round had
to find or manufacture real work even with the mailbox clean and both
GM-tagged `GAME_TEST_QUEUE.md` entries (`GT-127`, `GT-128`) still HOLD/BLOCKED
purely on chief's side (confirmed by re-reading both entries in full; nothing
in either blocker is in this lane's write zone).

Walked the four Rule-F options in order:
- (ก) pre-approved backlog in `gm/` — none found; the module surface is
  complete for every capability not itself blocked on a chief call site.
- (ข) an RE/STATIC letter answerable from committed source — none open
  (`GT-145`, the only open `STATIC-ON-BRIDGE` item, needs the actual bridge
  console and cannot be answered from a cloud clone).
- (ค) **writing/refining a queue test entry — this is what the round did.**
  `login_scene_admission.stageable_scene_ids()` measured fresh on `main`
  returns `(1, 2, 14, 278, 997)`, five scenes, not the four
  (`(1, 2, 278, 997)`) that `GT-141` (owned by this lane) still states
  literally in four places, and that two of this lane's own test-file
  comments in `pirate-force-server` still cite as current. Scene 14 joined
  the set in round `vvy6q7` (lane A, `login_entry_allowed(14) -> true`, PR
  `#290`) — already verified and consumed by this lane at round `kmdln4`,
  but the queue entry's own body text was never refreshed, so an attended
  tester grepping the console for `stageable=(1, 2, 278, 997)` today would
  see a fifth number and could misread it as a defect.
- (ง) pf-adversary-flagged tech debt (D6/D7 in `login_scene_admission.py`) —
  read both in full; both are *deliberately* left open with a written reason
  the "obvious" fix is wrong (D7: swapping the blocker order reopens a
  spawnless-admission hole; D6: an added read inside the refusal's own
  `raise` would swap a caller-handled refusal for an unhandled registry
  error). Touching either without new information would be re-litigating a
  documented decision, not doing new work — left alone.

## What shipped

### `pirate-force-server` (commit on `claude/upbeat-knuth-2q9lxx`)

Two stale comments corrected — no executable line touched:
- `tests/test_gm_login_scene_admission.py`: the docstring's "four scenes wide
  is the correct value" sentence (quoting `COO-DECISION 20260829_0941`
  verbatim from round `7gplcy`, left untouched as history) now has one
  appended sentence noting the ruling was about the SHAPE of the set, not
  the number four, and that the live count is five as of round `vvy6q7`.
- `tests/test_gm_login_scene_consume.py`: the comment above `PORT_ROYAL = 1`
  / `PRISON_EXILE = 2` cited the four-scene tuple as current; corrected to
  the dated form ("was X when written, is Y as of round 2q9lxx") plus the
  reason the two pinned literals never needed to change.

Verified: 957/957 `test_gm_*.py` tests pass both in the live checkout and in
a `git worktree add --detach` copy with the diff applied (pf-adversary's
mandatory workspace rule, COO-DECISION 2026-08-29T14:44) — the second run
exists because the diff is comment-only and the live-checkout run alone
would not have distinguished "no mutation surface" from "didn't check".
pf-adversary self-review: inspected the patch hunk-by-hunk — both hunks
touch only comment/docstring lines, so there is no executable statement a
mutation sweep could target; the corrected numbers were re-derived from
`stageable_scene_ids()` at HEAD, not copied from a letter.

### `pf_bridge` (this repo)

- `GAME_TEST_QUEUE.md`: appended one dated update block to `GT-141` (a queue
  header this lane owns) noting the five-scene live value, why it grew via a
  different path than the one `GT-141` already warned readers about (scene
  126's sanctioned-bypass route vs. scene 14's plain `login_entry_allowed`
  flip), and that seeing the fifth number in console output is not a defect.
  Nothing struck through, nothing deleted, no block/unblock change, pass
  criteria unchanged (still 278/2 as the recommended scene pair).
- `notes_to_chief/20260830_1025_LANE-GM-CORE-REQUEST-GM-040-v2-still-overdue-10h.md`:
  second escalation of `CORE-REQUEST-GM-032` item 3 / `CORE-REQUEST-GM-040`,
  per `h4v9wq`'s own stated plan ("escalate again if the next round still has
  no answer"). Deadline (`COO-DECISION`, received round `8tpw8k`/R219) was
  2026-08-29T23:59+07:00; now ~10h26m overdue. No new facts beyond the
  elapsed time — explicitly not invoking the three stop-and-wait criteria
  (this is a routine overdue chief-zone item, not a direction change, an
  irreversible action, or a conflict with an owner order), but flagged
  loudly for Panya's optional attention given the deadline was COO-set and
  is now double what it was at the last escalation.

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้ (round `2q9lxx`)

**ไม่มีความสามารถใหม่ — วันนี้เป็นรอบแก้เอกสารให้ตรงกับโค้ดที่มีอยู่แล้ว ไม่ใช่รอบเพิ่มความสามารถ**
สิ่งที่เปลี่ยนจริงคือ: ผู้เทสที่บูต `GT-141` แล้วเห็นคอนโซลพิมพ์ `stageable=(1, 2, 14, 278, 997)`
(ห้าค่า แทนที่จะเป็นสี่ค่าตามที่ใบเก่าเขียนไว้) จะไม่ต้องหยุดสงสัยว่าใบพังหรือ config ผิด —
ใบมีคำอธิบายกำกับไว้แล้วว่านี่คือของจริงและไม่ใช่ความล้มเหลว

**NONCLAIM:** ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริงในรอบนี้ ทั้งหมดวัดจาก
`stageable_scene_ids()` ที่รันสดจากซอร์สที่ commit แล้ว, GitHub API (`list_pull_requests`,
`pull_request_read`), และ grep/read บน `notes_to_chief/` ทั้งสอง repo

## สภาพแท่นตอนจบ

ไม่มีการบูตเซิร์ฟเวอร์หรือไคลเอนต์รอบนี้ (ไม่มีใบ attended ให้เดิน) — ไม่มี `LOCK_GAME` ให้ถือ
หรือปล่อย ไม่มีการแตะ canonical DB ไม่มีการรัน migration ใด ๆ

— สาย GM รอบ `2q9lxx`
