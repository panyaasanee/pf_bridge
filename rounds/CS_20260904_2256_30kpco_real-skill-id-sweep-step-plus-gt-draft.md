# CS round 30kpco — real class_id=1 skill-id sweep step (server PR #768) + full GT draft for skill-window content

เวลาเริ่ม 2026-09-04 22:06 +07:00 · เวลาปิด 2026-09-04 22:56 +07:00 · claim `pf_bridge` (PR นี้เอง, หัว `[LANE-CS] round 30kpco: claim` เดิม ทับด้วยไฟล์นี้)

## ขยับ NOW/M ข้อไหน

**ไม่ขยับขั้น M2/M3/M4/M5 โดยตรง** — งานรอบนี้คือ "รอเครื่องคุณ" ข้อ 7 ใหม่ที่ COO วางไว้ (จดหมาย `2154`):
ตอบข้อเสนอ GT "เนื้อในหน้าต่างสกิลหลัง `0x673C`" ที่ COO อนุมัติแล้วให้ LANE-CS ร่างเต็ม + ลงโค้ด/แฟล็ก
ส่งเฟรมถ้ายังไม่มี ใบนี้เข้าคิว "รอเครื่องคุณ" ต่อจาก `GT-243` ไม่ใช่ตัวบล็อกขั้น M ใด ๆ โดยตรง แต่เป็นก้าว
ที่ COO ระบุว่าต่อยอด LANE-CS's own mission ("โค้ดดิ้งระบบอาชีพ... หาและดูแลเรื่องสูตรคำนวนดาเมจ") ผ่าน
`learn_skill_result_hypothesis.py` ที่โอนมาเป็นของ LANE-CS

**เหตุที่ไม่ขยับ M ตรง ๆ**: ใบ GT ที่รอบนี้ผลิตยังไม่ได้รัน (ต้องรอเครื่อง Panya เหมือน `GT-243`) — โค้ดขึ้น
main (เมื่อ PR #768 merge) ไม่นับว่า "เสร็จ" ตามกติกาไฟล์ `NOW.md` ("โค้ดขึ้น main ไม่ใช่ 'เสร็จ'")

## งานที่ทำ

### 1. โค้ด/แฟล็กส่งเฟรม (pirate-force-server, PR #768, branch `claude/pensive-bardeen-30kpco`, commit `bdfc7885`)

เพิ่มก้าวที่ 6 ของสวีป `HYP-PF-033` (`src/pirateforce_foundation/learn_skill_result_hypothesis.py`):
`COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0` — ส่ง 4 records จาก `class_catalog.starting_skill_ids(1)` (111 "VIP
Strive Jump", 40000 "Gladiator Basic Training", 99 "Normal Attack", 110 "Strive Jump") แทนค่า probe เดิม
(1000001, 0xFFFFFFFF, ...) แต่ละ record ใส่ skill id เดียวกันซ้ำทั้งสามตำแหน่ง wire
(`record_u32_0 == record_u16_4 == record_u32_8`) เพราะยังไม่รู้ว่าตำแหน่งไหน (ถ้ามี) คือ "skill id" จริง —
ออกแบบให้ผู้เทส attended ไม่ต้องเดาฟิลด์ก่อนตัดสินผลบนจอ ก้าวเดิมทั้ง 5 (`COUNT0_TRAIL0`..`COUNT3_TRAIL1`)
ไม่แตะ

**สิ่งที่ทำจริง**:
- pin ใหม่ (payload/pc/frame ขนาด+sha256 ของก้าวที่ 6) คำนวณจากการรันตัว encoder จริงกับ
  `current/pf_login_game_server_v141.py` ไม่ได้พิมพ์มือ
- `scenarios/learn_skill_result_hypothesis_learn_sweep.json` re-generate จาก `_expected_sweep()` ของโมดูล
  เอง (loader เช็ค exact-equality ระหว่างสองไฟล์นี้อยู่แล้ว)
- `runtime.py` **ไม่ต้องแก้เลย** — dispatch loop เดิมวน `learn_skill_result_hypothesis_scenario.step_order`
  แบบ generic อยู่แล้ว ก้าวที่ 6 ไหลผ่านเอง (ตรวจสอบแล้วก่อนแก้อะไร)
- เพิ่ม self-guard ใน `_require_step_plan()` เทียบ records ของก้าวใหม่กับ `class_catalog.starting_skill_ids(1)`
  สด ๆ ทุกครั้ง — ถ้าตารางเปลี่ยนแถวในอนาคตจะพังตรงนี้ทันทีแทนที่จะเงียบ
- แก้เทสทุกจุดที่ hardcode "5 เฟรม" (action-label list, delay list, sweep-count, ดัชนี step ที่ปฏิเสธ) เป็น 6 ·
  เพิ่มเทสใหม่ pin records ของก้าว real-id กับ `class_catalog.starting_skill_ids(1)` สด
- `docs/FUNCTIONAL_COVERAGE.json` แก้ถ้อยคำ "five"→"six" ตรงจุดของ `HYP-PF-033`

**ไม่แก้** `docs/HYPOTHESIS_LEDGER.json` — ไฟล์นี้มีเกต hash ของตัวเอง (`CANONICAL_CONTENT_SHA256` ใน
`tools/verify_hypothesis_ledger.py`) ผูกกับกลไก approval (`approval_id`/`approved_entry_ids`/
`approved_through`) ที่อ่านแล้วเป็นกลไกอนุมัติระดับเจ้าของ ไม่ใช่สิ่งที่ LANE ควรขยับ pin เองโดยไม่ถาม —
revert กลับหลังลองแก้แล้วเจอเกตแดง (`test_hypothesis_ledger.py::test_canonical_inventory_and_policy` /
`test_bidirectional_emitter_annotations_fail_closed`) ถามท่าน chief ในจดหมายรอบนี้แล้วว่าควร bump อย่างไร

**เทส**: `pytest tests/test_learn_skill_result_hypothesis.py -v` → 60 passed, 3 subtests passed · ชุดเต็มทั้ง
ต้นไม้ (merge `origin/main` เข้ากิ่งก่อน) → 10184 passed / 323 skipped / 19444 subtests passed / 1 แดงเดิม
(`test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned` —
ยืนยันแล้วว่าแดงบน `origin/main` ก่อน PR นี้ด้วย `git stash` แล้วรันซ้ำ ไม่ใช่ของรอบนี้) ·
`tools_bridge/pf_gate_preflight.py --repo .` → PASS (cp874 สะอาด · ไม่มี skip ใหม่ · main อยู่ใน HEAD แล้ว)

### 2. ใบ GT ฉบับร่างเต็ม (จาก `pf-queue-author`)

```
## GT-XXX (number TBD by chief) LEARN-SKILL-RESULT-REAL-KIT-CONTENT-001  [PENDING -- owner/consumer of result = LANE-CS -- runs attended, piggybacked in the same attended appointment as GT-243 (same class_id=1/level=1 character, saves a second scheduled sitting) -- NOT the same server process as GT-243 (see BOOT ORDER note, GT-243's own server args explicitly forbid any --*-scenario flag)]

> NUMBERING NOTE (for chief): grep GT-XXX/RE-XXX against GAME_TEST_QUEUE.md, CLIENT_RE_QUEUE.md and both
> archive/*_closed.md files for 0 hits before reserving a number, same discipline as every entry before this
> one (see GT-116's and GT-243's own numbering notes). This entry does not touch, reopen or supersede
> GT-058/GT-059/GT-064 (archived, CLOSED, a different question: whether the window OPENS at all) or GT-116
> (CLOSED PASS 2026-08-28, GAME_TEST_QUEUE.md:5183: the window opens for a class_id=1/level=1 character with
> 0 entries) or GT-243 (PENDING, a different question: hotbar dispatch producer for skill 99). This entry is
> new, opened per COO-DECISION 20260904_2154 answering LANE-CS's own letter
> notes_to_chief/20260904_2113_LANE-CS-TO-COO-backup-item1-read-plus-gt116-reopens-skill-window-content-question.md.

### source (links only -- see cited files for full detail, not re-derived here)
- notes_to_chief/20260904_2154_COO-DECISION-skill-window-content-gt-approved-piggyback-gt243-LANE-CS.md --
  the approval: send 0x673C with REAL skill ids from class_id=1's own starting kit (not arbitrary probe
  values) to a character that already satisfies GT-116's precondition; PASS = skill window (K) populates
  with exactly the 4 starting skills of that class; attended-only, production_allowed stays False; STOP if
  the client closes; a result that refutes HYP-PF-033's content claim closes/rewords the parent module's
  open question in the same round (PANYA-DECISION 20260903_1934).
- rounds/CS_20260904_2113_fv5xnu_backup-item1-read-plus-gt116-reopens-skill-window-content.md -- the finding
  that reopened this: GT-058/GT-059/GT-064 (archived CLOSED) could never answer "does the window's CONTENT
  track anything the server sends" because in every one of those sessions the window never opened at all
  (class was always 0). GT-116 removed that blocker on 2026-08-28 but GT-116 itself explicitly says "[no
  claim] that the skill list shown is a correct Gladiator kit -- not yet measured" and no ticket since has
  asked the content question.
- GT-116 (GAME_TEST_QUEUE.md:5183, CLOSED PASS 2026-08-28): the window opens for a class_id=1/level=1
  character, 0 entries at level 1 is normal. This entry's precondition IS GT-116's own proven precondition.
  class_id=1 is presently wired into every flagless production login (CORE-REQUEST-022), so an ordinary
  character already satisfies it -- no special character build is required beyond what GT-243 already needs.
- src/pirateforce_foundation/learn_skill_result_hypothesis.py (HYP-PF-033, vital 0x673C) -- the module this
  entry exercises. Its own docstring nonclaims (read before using anything from it): the three record member
  positions (record_u32_0 / record_u16_4 / record_u32_8) have UNKNOWN semantics, the trailing u8 has UNKNOWN
  semantics, production_allowed=False, database_write=none, and "NO CLIENT HAS EVER SEEN ONE OF THESE
  FRAMES. That half is an attended GT ticket, queued and not run" -- this entry is that ticket.
  The module's [UPDATE, round fv5xnu's finding + COO-DECISION 20260904_2154] paragraph names the sixth sweep
  step this entry fires: COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0, sending 4 records, each repeating one of
  class_catalog.starting_skill_ids(1)'s 4 ids (111 "VIP Strive Jump", 40000 "Gladiator Basic Training", 99
  "Normal Attack", 110 "Strive Jump", in that order) in all three wire positions of its own record, trailing
  byte 0 -- because the position that means "skill id", if any, is unproven, this removes the need to guess
  which field the client reads before judging the on-screen result.
- The other five steps of the same sweep (COUNT0_TRAIL0, COUNT1_TRAIL0, COUNT1_TRAIL1, COUNT3_TRAIL0,
  COUNT3_TRAIL1) are UNCHANGED, pre-existing, and send arbitrary tellable-apart probe values (not real game
  data) -- this entry's own claim is about the 6th frame only; anything the first five frames visibly do is
  noted as a secondary observation, not this entry's pass/fail measure.

### objective (single claim)
Sent to the SAME class_id=1/level=1 character GT-116 already proved opens the skill window (K /
Bt_main_Skill), does the LAST frame of the HYP-PF-033 sweep -- the one whose 4 records carry class_id=1's own
real starting-kit skill ids (111, 40000, 99, 110) -- make that window populate with entries a human can
recognize as those 4 skills (VIP Strive Jump, Gladiator Basic Training, Normal Attack, Strive Jump), by
whatever names/icons the client actually shows? This is the FIRST attended measurement of whether anything
HYP-PF-033 sends is rendered as content at all, as opposed to merely accepted on the wire without visible
effect (which is all GT-050's static work and this module's own unit tests can ever show).

### predictions (a wrong prediction is a finding, not a failure)
- P1 [proposed, the heart of the entry]: after the full 6-frame sweep completes, the skill window shows
  exactly 4 entries, one per real starting-kit skill id, recognizable (by name text and/or icon, whatever the
  client actually renders) as VIP Strive Jump / Gladiator Basic Training / Normal Attack / Strive Jump.
- P2 [corollary, proposed]: the 4 entries appear in the same order the 6th frame sent them (111, 40000, 99,
  110). If the window instead shows them in a different order, or sorted some other way, write that down --
  it is a finding about display order, not a failure of P1.
- P3 [falsifier]: the window still shows 0 entries (or something clearly unrelated/garbled) after the full
  sweep, despite all 6 frames going out unrejected on the wire -- a REAL NEGATIVE, not a failure. It would
  mean the client either does not render this vital's content at all, or does not render it in the shape this
  module sends, i.e. these three record fields (whichever position, if any, means "skill id") are not the
  channel the client reads for the skill list. Per PANYA-DECISION 20260903_1934 ("a new result that proves or
  refutes an older ticket's premise closes/rewords that ticket's claim in the same round"), whoever consumes
  this result must, in the SAME round, close or reword the open "does the client render anything" question in
  learn_skill_result_hypothesis.py's own module docstring/NONCLAIMS section -- do not leave that question
  looking open when this ticket has just answered it.
- P4 [possible mixed outcome, not pre-judged]: the window shows some but not all of the 4 entries, or shows
  extra/garbled entries left over from the 5 earlier arbitrary-probe frames (COUNT0/COUNT1/COUNT3 pairs) that
  fired 3.0s-9.0s earlier in the same sweep -- if this happens, it tells us the window is CUMULATIVE across
  frames rather than replace-on-receipt, which is itself a separate finding from the main content claim, not
  something to average away or ignore.

### PRECONDITION (verify before step 1, not a footnote)
P0. Same as GT-116's own proven precondition: a normal login on the currently-merged production login path
    (which wires class_id=1/level=1 into every login unconditionally, per CORE-REQUEST-022, GT-116 CLOSED
    PASS). No special character build is required for THIS ticket's own claim -- any character that logs in
    normally satisfies it. This is a SEPARATE precondition from GT-243's own P0 (skill 99 learned and placed
    on a named hotbar/skillbar slot); satisfying GT-243's P0 does not hurt this ticket and this ticket does
    not require GT-243's P0 to be met.
P1. Server before client always; a client left open with no server dies on its own in ~3.5 minutes.
P2. Killing a client leaves the server holding the session -- restart the server before opening the next
    client or it hangs on "connecting" forever.
P3. A round copies the DB; character position resets to spawn every boot, expected, not a measured result.
P4. Teardown template refuses a boot stamp older than 420 minutes (raised from 180 on 2026-08-20,
    TEMPLATE_teardown_generic.ps1:135) -- run teardown even if the session ends because the tester stopped.

### BOOT ORDER / piggyback note (read before scheduling)
This entry is approved to run in the SAME ATTENDED APPOINTMENT as GT-243, to save booking a second sitting --
it is NOT the same server process boot. GT-243's own server args are explicit: "no --*-scenario flag of any
kind" (it needs a bare wire to observe the hotkey-dispatch path cleanly). This entry needs
--learn-skill-result-hypothesis-scenario, which GT-243 forbids. Run them as two separate boots, back to back,
in either order, inside the same LOCK_GAME hold: fresh DB copy per boot (as always), full teardown between
them if the boot-stamp/server-restart rules require it. Do not attempt to merge the two into one boot by
adding this flag to GT-243's command line or vice versa -- that would silently change GT-243's own already-
written server args, which this ticket has no authority to do, and combining two hypothesis-scenario lanes
in one boot needs its own explicit COMPOSABLE_SCENARIO_LANE_SETS allowlist entry that does not exist for this
pair.

### BEFORE BOOT -- gate 0/1/2 (merge status; do not skip, do not eyeball a SHA)
Gate 0: pirate-force-server PR #768 (commit bdfc7885, branch claude/pensive-bardeen-30kpco) carries the
COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 step + scenario file. Do not boot until #768 has merged to main.
Gate 1 -- resolve a green commit:
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
Only exit 0 with a printed `BOOT_COMMIT: <sha>` means bootable. exit 3 = this ticket waits on the gate, not on
the tester -- do not boot, do not checkout a branch directly to skip the resolver.
Gate 2 -- confirm the resolved SHA actually carries the code (grep the real commit, never trust a string in
this letter):
```
git grep -n "learn-skill-result-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git grep -n "COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0" <SHA> -- src/pirateforce_foundation/learn_skill_result_hypothesis.py
git cat-file -e <SHA>:scenarios/learn_skill_result_hypothesis_learn_sweep.json && echo SCENARIO_PRESENT
```
Need a hit on all three. Missing any one = BLOCKED, not NO-RESULT -- record "waiting on merge" and go run a
different ticket; do not hunt for a substitute commit yourself.
Read the exact pin values (payload/pc/frame size and sha256, per step label) straight from
scenarios/learn_skill_result_hypothesis_learn_sweep.json -> probe.per_step.COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0
in the commit you actually boot -- do NOT trust any hash or size written in this ticket, they are drafted
against a pre-merge working tree and are only for orientation, not for pass/fail comparison.

### db (a copy, always -- never open the canonical file)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-XXX_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gtXXX_<yyyyMMdd_HHmmss>.sqlite3
```
- sha256 of the canonical file, before and after, must match CANON_SHA.txt both times.
- database_write=none for this lane (confirmed in the module docstring) -- expect the working copy's only
  diff from a bare login to be the usual +1 row in `sessions`; PRAGMA integrity_check = ok both times.

### server args (exact -- opt-in only, production_allowed stays False)
```
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
py -3 -u -m pirateforce_foundation.app --db state\run_gtXXX_<stamp>.sqlite3 --learn-skill-result-hypothesis-scenario scenarios\learn_skill_result_hypothesis_learn_sweep.json
```
--db is required and must point at an existing file (the flag refuses to boot without an explicit --db).
Keep stdout+stderr captured together (2>&1). The server console must show whatever mode banner the resolved
commit prints for this scenario -- use it to confirm the right mode came up, not as proof of anything on the
wire.

### chat trigger -- exactly 12 printable ASCII characters (a lesson that has cost this project real time)
- This lane's dispatcher fires on ANY chat-input frame whose text is exactly 12 printable ASCII characters --
  shape-triggered, not string-triggered (classify_chat_input_attempt -> ascii12, the same classifier every
  other ascii12 lane in this tree uses). One character short or long reaches the server and the condition
  silently fails to match -- no error, the sweep just does not fire.
- Use `SKILLCONTENT` for this ticket (count it: S-K-I-L-L-C-O-N-T-E-N-T = 12 characters exactly) so the log
  reads clearly against other lanes' own trigger strings.
- Click the chat box to focus it before typing -- characters typed while chat is NOT focused become hotkeys,
  not chat text. Type the 12 characters, press Enter once, then immediately click empty ground to drop focus
  again before pressing K (K typed into an unfocused-but-still-open chat box becomes a letter in the chat
  box, not the skill-window hotkey).
- One accepted trigger fires ALL 6 frames of the sweep, 3.0s apart, the first at 0.0s delay -- so the 6th
  frame (this ticket's own frame) lands roughly 15s after Enter, plus send/composition time. Budget at least
  18-20s of continuous recording after Enter before judging the final window state.
- The sweep is not one-shot -- firing the trigger again re-sends all 6 frames from the top.

### steps (click by click; record continuous video for the whole session)
Before start: hold LOCK_GAME, note boot stamp, compare canonical sha, copy DB per the db block, clear gate
0/1/2 above, stage TEMPLATE_teardown_generic.ps1.
1. Start the server first (Get-NetTCPConnection -State Established on ports 10188/10189 must be 0 before
   opening the client) -- console shows the scenario's mode banner.
2. Open client -> select server -> PVP dialog left button -> character select -> the character used in this
   sitting -> the middle of the 5 bottom buttons = enter game (never the leftmost -- that deletes the
   character). Start continuous recording before pressing enter-game.
3. T0 -- HP bar / minimap / map name visible. Photograph full-res (S00-HOME). Record every name-label colour
   in this still, one line per label, "none" written out where there is none.
4. NO-CRASH check: right-click-drag to sweep the camera once. Camera-only, character facing never moves,
   nothing goes out on the wire -- safe at any point. Never use Q/E or W/A/S/D for this check -- those turn
   the character and emit TargetPosVital.
5. BASELINE: confirm chat is not focused (click empty ground) -> press K (or click Bt_main_Skill) ->
   photograph full-res (S-BASE-K). Expect the same state GT-116 measured (window opens, 0 entries) --
   if baseline already shows something else, write it down prominently before continuing; the condition
   under test has changed.
6. Close the window if it opened. Click the chat box to focus it -> type `SKILLCONTENT` -> press Enter once
   -> immediately click empty ground to drop chat focus. Record the clock time (HH:MM:SS+07:00) of Enter as
   T_TRIGGER.
7. Best-effort intermediate captures (not this ticket's pass/fail measure, but useful context for P4): press
   K roughly every 3s after T_TRIGGER if it is quick enough to catch a window already open, photographing
   each time (S-MID-1 .. S-MID-5), noting the approximate elapsed time since T_TRIGGER for each. If timing is
   missed, write "not caught" rather than guessing.
8. Wait until at least 20s have elapsed since T_TRIGGER (the 6th frame's send window plus margin). Press K
   (or click Bt_main_Skill) -> photograph full-res (S-FINAL-K). This still is the primary evidence for this
   ticket's own claim.
9. If the window is open: photograph its full content full-res, transcribe what it shows character-for-
   character from the still -- every visible entry's name/label/icon description, count of entries, any
   entry that does not obviously correspond to one of the 4 real skill names. Do not guess at a match if the
   client's own label text is illegible -- write "illegible" rather than inferring.
10. Secondary positive control: press C to open the CHARACTER window, photograph, close -- confirms the
    client is still generally responsive (same control GT-116/GT-059 used).
11. NO-CRASH check again (right-click-drag).
12. Fire the trigger a second time (type `SKILLCONTENT`, Enter, drop focus) to confirm repeatability -- wait
    20s again, press K, photograph (S-REPEAT-K). Record whether the second sweep changes anything from
    S-FINAL-K (e.g. duplicated entries, unchanged, cleared and re-populated).
13. Log out -> teardown via TEMPLATE_teardown_generic.ps1 (boot stamp must still be under 420 min) -> recheck
    canonical sha256 -> sha256 every capture.
STOP: if the game client crashes or closes at any point, stop immediately, record it as a measured result
(not a wasted round) with the frame/step it happened at, and still run teardown.

Colour rule (Panya's order, 2026-08-25): one line per name label per image, write "none" not blank, read
colours from full-resolution stills only (never a contact sheet, downscaled image or video), never infer a
cause for a colour (RE-067 owns that question). Divergences from the original server's own screenshots go
into REAL_SERVER_DIVERGENCE.tsv, one row each.

### pass criteria (two layers, never mixed, never offered as proof of each other)

wire/DB (headless-provable from GAME_LIVE.txt / server console+log, no human needed for this layer):
- Raw capture around T_TRIGGER shows exactly 6 outbound frames spaced ~3.0s apart, the 6th and last being the
  COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 composition (largest of the 6, per the module's own pinned sizes).
- That 6th frame's body decodes to: u16 tag 0x12 count=4; then 4 records in order, each u32 tag 0x14 / u16
  tag 0x12 / u32 tag 0x14 all three equal to the same skill id, in the order 111, 40000, 99, 110; trailing u8
  tag 0x0B value 0 -- byte-exact against the payload/pc/frame sha256 and size pinned in
  scenarios/learn_skill_result_hypothesis_learn_sweep.json for this label at the booted commit (read at gate
  2, not copied from this ticket).
- `sessions` table +1 row per login; lease_generation does not go backward; PRAGMA integrity_check = ok both
  times; canonical sha256 matches CANON_SHA.txt before and after; no other table changes.
- No traceback, no unexpected socket close, in either console log.
- This layer CANNOT say whether anything appeared on screen -- do not use it as a stand-in for the
  client-observable layer below.

client-observable (a human at the screen only, never inferred from console/log):
- S-BASE-K: baseline state before the trigger (expected: window opens, 0 entries, matching GT-116; write down
  verbatim if it does not).
- S-FINAL-K (>=20s after T_TRIGGER): the PRIMARY reading for this ticket. Write, in plain language, exactly
  what is in the window -- entry count, and for each entry whatever name/icon/tooltip text the client shows.
  PASS reading = exactly 4 entries, each independently recognizable as one of VIP Strive Jump / Gladiator
  Basic Training / Normal Attack / Strive Jump (by whatever exact display strings the client uses -- record
  the literal strings, do not paraphrase them to match the expected names).
  NEGATIVE reading = 0 entries, or entries that do not correspond to any of the 4 names, after confirming the
  wire layer above shows the frame went out clean.
- S-MID-1..5 (best-effort): whatever was caught mid-sweep, with elapsed time noted, or "not caught".
- S-REPEAT-K: whether firing the trigger a second time changes S-FINAL-K's state (same / cleared and
  re-populated / duplicated / other -- describe plainly).
- C / CHARACTER window control check (step 10).
- Both NO-CRASH checks pass.
- Name-label colours recorded per the colour rule above, one line per label per full-res still, for every
  photograph taken this session.
- This layer CANNOT say what bytes actually left the server -- do not use it as a stand-in for the wire/DB
  layer above.

### outcome boxes (pick one, report which; a negative result is worth as much as a positive)
A. S-FINAL-K shows exactly 4 entries and all 4 are independently recognizable as the 4 real class_id=1
   starting-kit skills -> PASS. This is the strongest form of P1 confirmed. Record display order too (P2).
B. S-FINAL-K shows some but not all 4, or shows extras/garbled entries alongside them (possibly left over
   from the 5 earlier probe frames in the same sweep) -> PARTIAL/MIXED, not a clean PASS. Write exactly which
   of the 4 are present, which are missing, and describe anything extra verbatim. Do not average this into a
   PASS or a FAIL -- report the mixed state as its own finding (P4).
C. S-FINAL-K shows 0 entries despite the wire layer confirming all 6 frames went out clean and unrejected ->
   NEGATIVE, complete and valid (P3). Redirect: per PANYA-DECISION 20260903_1934, whoever consumes this
   result closes or rewords the "does the client render this vital's content" open question inside
   learn_skill_result_hypothesis.py's own module docstring/NONCLAIMS in the SAME round -- do not leave the
   module implying the question is still open once this ticket has measured it.
D. S-FINAL-K shows entries but none of them resemble any of the 4 real skill names/icons (e.g. garbled text,
   generic placeholder icons with no legible name) -> NEGATIVE of a different flavour than C -- the window
   renders SOMETHING from this vital but not identifiably the sent content. Record verbatim; do not guess at
   what it might mean.
E. Client crashes/closes, or a frame is rejected on the wire, before the 6th frame's window (T_TRIGGER+20s)
   -> NO-RESULT, report exactly where it stopped, still run teardown. Do not guess at what would have
   happened.

### things this ticket must not conclude (evidence discipline)
- Does not name any of the three record-wire positions (record_u32_0 / record_u16_4 / record_u32_8) as "the"
  skill-id field even on a clean PASS -- each record in this frame repeats the same id in all three
  positions specifically so this question stays open; a PASS here only proves the WHOLE record, sent this
  way, renders correctly, not which single field the client actually reads.
- Does not claim anything about the trailing u8's meaning -- this step sends 0 only, no companion is sent.
- Does not claim the original (defunct) server ever sent 0x673C in this shape, this order, or on this
  trigger -- the step plan, values, spacing and trigger policy are this project's own design, stated as such
  in the module docstring.
- A PASS here does not prove the 4 skills are actually usable, learnable through any real game action, or
  persisted anywhere (database_write=none) -- only that the window can be made to display them via this
  hand-composed frame.
- Does not decide the cause of any name-label colour observed (RE-067 owns that question).
- If gate 0/1/2 does not clear, the entire entry is BLOCKED, not NO-RESULT/FAIL -- record "waiting on merge"
  and stop.

### nonclaims
1. Does not prove or test skill usability, cooldowns, damage or persistence of any of the 4 skills.
2. Does not prove anything about a class other than class_id=1, or about any character other than the one
   used this session.
3. Does not reopen or change the verdicts of GT-058/GT-059/GT-064 (archived CLOSED) or GT-116 (CLOSED PASS)
   -- this is a new, narrower question those tickets never asked.
4. Does not touch or depend on GT-243's own claim (hotbar-vs-hotkey dispatch producer) -- the two tickets
   share only an attended appointment and a login precondition, not a server boot or a claim.
5. Does not resolve the semantics of the three record-wire positions or the trailing u8 (see "things this
   ticket must not conclude" above).
6. Does not prove anything about the inbound CLearnSkillVital 0x36AA direction (no handler exists; separate,
   untouched question per the module's own docstring).
7. Single account, single character, one attended sitting -- no second player observing, no cross-account
   comparison.
8. Does not decide the cause of any name-label colour observed (RE-067 stays open).

### closing instructions (per PANYA-DECISION 20260903_1934)
If the result lands in outcome box C or D above (the client does not visibly render this vital's content, or
renders something unrecognizable as the sent content), the lane that consumes this result must, in the SAME
round, open a follow-up edit to learn_skill_result_hypothesis.py's own module docstring (the "NO CLIENT HAS
EVER SEEN ONE OF THESE FRAMES... queued and not run" sentence and any nearby claim that implies this question
is still open) so the module's own text stops implying an unanswered question that this ticket has just
answered. Name this ticket's number/letter in that edit. Do not leave the module's docstring stale relative
to an attended result that refutes or answers what it currently defers.

### links
- pf_bridge/notes_to_chief/20260904_2154_COO-DECISION-skill-window-content-gt-approved-piggyback-gt243-LANE-CS.md
- pf_bridge/rounds/CS_20260904_2113_fv5xnu_backup-item1-read-plus-gt116-reopens-skill-window-content.md
- pf_bridge/notes_to_chief/20260903_1934_PANYA-DECISION-a-new-test-result-that-proves-or-refutes-an-untested-older-ticket-cancels-that-ticket-with-the-reason-written-in.md
- GAME_TEST_QUEUE.md GT-116 (line 5183, CLOSED PASS) and GT-243 (line 13368, PENDING)
- archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md -- GT-058/GT-059/GT-064 (all CLOSED, the "does the
  window open" question this entry does not reopen)
- src/pirateforce_foundation/learn_skill_result_hypothesis.py (HYP-PF-033, module docstring's [UPDATE, round
  fv5xnu's finding + COO-DECISION 20260904_2154] paragraph)
- scenarios/learn_skill_result_hypothesis_learn_sweep.json
- notes_to_chief/20260824_0055_GT050-RESULT-CLEARNRESULT-CLOSED-TRIGGER-DIRECTION-UNRESOLVED.md (GT-050,
  the static provenance of the 0x673C body shape this module encodes)
- BRIDGE_BOOT_PROCEDURE.md + ATTENDED_SESSION_RUNBOOK.md + TEMPLATE_teardown_generic.ps1

### result (tester fills in)
```

```
```

## ADVERSARY_PENDING

สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานแล้ว (ก่อนแตะไฟล์) — ผลยังไม่คืนตอน push รอบนี้ ⇒ บันทึก
**`ADVERSARY_PENDING pirate-force-server#768`** รอบหน้าหยิบผลเป็นงานแรกก่อนคิวตัวเอง (ตาม `COO-DECISION
20260903_2345`/`1428`) — ยังไม่เขียนว่า "ผ่าน adversary" จนกว่าผลคืน

## ส่งอะไร

**pirate-force-server**: PR **#768** (`claude/pensive-bardeen-30kpco`, commit `bdfc7885`) — ดูหัวข้อ 1
ด้านบน

**pf_bridge**:
- ไฟล์นี้ (แทน `rounds/CS_30kpco_claim.md`)
- `notes_to_chief/20260904_2256_LANE-CS-TO-CHIEF-gt-draft-real-skill-id-frame-plus-server-pr.md`
- `.CONSUMED.txt` ของ `notes_to_chief/20260904_2154_COO-DECISION-skill-window-content-gt-approved-piggyback-gt243-LANE-CS.md`

## nonclaims

- **ไม่อ้างว่าใบ GT ข้างต้นถูกเปิดจริงใน `GAME_TEST_QUEUE.md`** — เป็นฉบับร่างในจดหมาย/ไฟล์รอบเท่านั้น
  รอ chief ตั้งเลข+ปะหัวใบตามเขตเขียนของท่าน
- **ไม่อ้างว่า PR #768 ผ่าน adversary** — `ADVERSARY_PENDING` ตามข้างบน
- **ไม่อ้างว่าโค้ดพิสูจน์อะไรเรื่องพฤติกรรมไคลเอนต์** — เป็นแค่ตัวส่งเฟรม การรอผลยังต้องรอเครื่อง Panya
  (`GT-XXX` ในร่างข้างต้น)
- **ไม่แตะ** `class_catalog.py` / `skill_catalog.py` / `damage_by_skill.py` (แก้เฉพาะ
  `learn_skill_result_hypothesis.py` + เทส + scenario JSON + `FUNCTIONAL_COVERAGE.json`)
- **ไม่แก้** `docs/HYPOTHESIS_LEDGER.json` — เกต hash ของไฟล์นั้นดูเหมือนต้องผ่านกลไกอนุมัติที่ไม่ใช่ของ
  LANE-CS ถามท่าน chief ในจดหมายแล้ว

## ติดอะไร / ใครปลด

- **ใบ GT ในร่าง** — รอ chief ตั้งเลข+ปะหัว (กำหนดตามจดหมาย COO: 22:21/23:51)
- **`docs/HYPOTHESIS_LEDGER.json` ถ้อยคำ "five"→"six"** — รอ chief บอกวิธี bump `CANONICAL_CONTENT_SHA256`
  ที่ถูกต้อง (ดูจดหมายรอบนี้)
- **`ADVERSARY_PENDING pirate-force-server#768`** — รอบหน้าของ LANE-CS หยิบเป็นงานแรก
