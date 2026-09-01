# PIRATE FORCE — Chief Architect continuation file

## 🔴 ลำดับงานปัจจุบัน — ไมล์สโตน M1-M6 พักไว้ (คำสั่งตรงเจ้าของ 2026-09-01T02:15 ผ่านกะ1-A)

อ่านหัวข้อนี้ก่อนมอบหมายงานใดๆ ทุกรอบ — อย่ามอบงาน milestone (M1-M6/CHARTER-02) ใหม่จนกว่าเจ้าของจะสั่งกลับมา
(พัก ไม่ใช่ยกเลิก) ใบเต็ม: `notes_to_chief/consumed/20260901_0215_PANYA-ORDER-*.md` · มอบหมายสาย:
`notes_to_chief/consumed/20260901_0302_FROM_CHIEF_R278_*.md`

- **P-1** ของดรอปต้องอยู่บนพื้นนานพอให้เดินไปเก็บทัน → **LANE-B**
- **P-2** สีชื่อมอนต้องถูกสถานะ: ปกติ=ส้ม / สู้=แดง / ตาย=เทา (ห้ามชมพู) → **LANE-GM**
- **P-3** เปิดปุ่ม GM ให้ได้ → **LANE-GM** (Codex ป้อนข้อมูลเรื่อยๆ ใบที่แตะ P-3 หยิบใช้ทันที ไม่เข้าคิวรอ)
- งานสร้างใหม่คู่ขนาน: GM-A `/warp` ไม่ใส่พิกัด (LANE-GM, GT-182 **PASS** รอบ 8zf80f) · GM-B `/speed` (LANE-GM) ·
  UI-A/UI-B ปุ่มกลับหน้าเลือกตัวละคร/logout (LANE-A)
- `GT-146`/ใบตีมอนทั้งหมด **ห้ามเข้าคิว attended** จนกว่า P-1 และ P-2 จะเสร็จ

🔴 KA1A-FINDING 20260901_1110 (`notes_to_chief/consumed/`): บล็อกนี้อยู่ใน **จดหมาย/ไฟล์นี้เท่านั้น** —
prompt ของแต่ละสาย (scheduled routine) ยังพูดถึงแต่ milestone เดิม เพราะ**เจ้าของเท่านั้นที่แก้ prompt ได้จริง**
(chief แก้แทนไม่ได้ ห้ามลองด้วย) จนกว่าเธอจะทำ ให้ chief ทุกรอบอ่านบล็อกนี้ก่อนมอบงานใหม่ แทนการพึ่ง prompt สาย

## ดัชนีรอบเก่า (รอบ 44-178) — ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_INDEX.md` แล้วทั้งบล็อก ไม่มีการลบเนื้อหา

## 0. โครงสร้างทีมคืนนี้ + เช็คก่อนเริ่มทุกครั้ง

### 0.1 ใครทำอะไร (ผู้ใช้สั่ง 04:40 แก้ 04:45)

- **`pirate-force-chief-continue`** (คุณ, ตื่นนาทีที่ 0,10,20,…):
  งานโค้ด / เอกสาร / ledger / verifier / commit
  🚫 **ห้ามเทสในเกม** — ถึงจุดที่ต้องเทส ให้เขียนรายการ PENDING ลง
  `pf_bridge\GAME_TEST_QUEUE.md` แล้วจบรอบ
- **ผู้เทสในเกม = เซสชันหลัก** (Claude ตัวที่คุยกับผู้ใช้ ถือสิทธิ์ computer use อยู่แล้ว)
  task `pirate-force-game-tester` ถูกปิดชั่วคราวคืนนี้
- **กลไกปลุก:** chief-continue จบรอบ → notification ปลุกเซสชันหลักอัตโนมัติ
  → ผู้เทสอ่านคิว ถ้ามี PENDING ก็เทสแล้วกรอกผลกลับ
  **แค่จบรอบให้เรียบร้อย = ปลุกผู้เทสแล้ว ไม่ต้องทำอะไรเพิ่ม**
- ทั้งคู่ใช้ `LOCK.txt` เดียวกัน

### 0.2 เช็คตามลำดับ

1. **`pf_bridge\LOCK.txt`**
   - ขึ้นต้น `RELEASED` = ว่าง ทำงานได้เลย
   - ขึ้นต้น `HELD` และ timestamp อายุ **< 20 นาที** = มีคนทำอยู่ → **หยุดทันที**
     ห้ามเขียน `inbox\` ห้ามแตะ repo
   - `HELD` แต่ timestamp **นิ่ง** เกิน 20 นาที = หมดอายุ เขียนทับเป็นของตัวเองได้
   - timestamp **ขยับ** = เจ้าของยังมีชีวิต ห้ามแย่ง
2. **`pf_bridge\inbox\`** — ถ้ามี `.ps1` ค้าง แปลว่างานก่อนหน้ายังรันไม่จบ → หยุด
3. **`pf_bridge\outbox\`** — อ่านไฟล์ล่าสุด ถ้ามีผลที่ยังไม่วิเคราะห์ ให้อ่านก่อน
4. **`pf_bridge\GAME_TEST_QUEUE.md`** — ถ้ามีรายการที่ผู้เทสกรอก `result` กลับมาแล้ว
   ให้เอามาประมวล/commit ต่อ

---

## CORE-REQUEST registry — ตัวนับเดียวทุกสาย (COO-DECISION 20260826_0656 · ตารางนี้สร้างโดย chief R174 · ตัด+สรุปเหลือเฉพาะแถวเปิด R211 28jd9c)

กติกา: chief เท่านั้นเขียนแถวนี้ · สายเสนอเลขถัดไปในจดหมายตัวเองกำกับ `[เสนอ · รอ chief]` · `ต่อแล้ว` เขียนได้ก็ต่อเมื่อโค้ดอยู่บน `main` แล้วจริง (`COO-DECISION 0401 §③`)

🔴 R211+R229 housekeeping: full table rows 001-026 -> `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` · row 027 (closed, wired R210, merge verified) + R211 preamble + stale WIRED-count note -> `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ตารางข้างล่าง = เฉพาะแถวที่ยังเปิด

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 028)

- 028 CORE-REQUEST-GM-047 (สาย GM รอบ `bxkxfc` · P0 · `COO-DECISION 20260901_0741`) — cross-scene GM warp label ไม่เคยเรียก resync ตำแหน่ง (`runtime.py:5304` เดิมเช็คเฉพาะ `WARP_ACTION_LABEL`) เสี่ยง DB position เพี้ยนถ้ารัน `GT-182` ก่อนแก้ · แก้รอบ `ts0deo`: เช็คสมาชิกสามป้าย (`WARP_ACTION_LABEL`/`WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`/`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`) ที่ `runtime.py:5304` + เทสถดถอยใหม่ที่พิสูจน์ผ่าน dispatch จริง (ยืนยันเทสล้มบนโค้ดเดิม 1!=2, ผ่านบนโค้ดใหม่) · **ต่อแล้ว (wired) — ยืนยันรอบ `69r41m` (R283)**: `pf_bridge#680` merged `2026-09-01T01:19:23Z`, `pirate-force-server#452` merged `01:27:10Z`, ทั้งคู่ยืนยันด้วย `pull_request_read get` (ไม่ใช่ `list_pull_requests`'s `merged` field ซึ่งอ่านผิดเป็น false — tool quirk เดิม) + อ่านโค้ดตรงจาก `origin/main:runtime.py:5304` เห็น `_GM_WARP_LABELS` สามป้ายจริง · ปลด `GT-182` จาก `BLOCKED-PENDING-GM047-FIX` เป็น `BLOCKED-ON-ATTENDED [NEEDS-ATTENDED-CAPTURE]` แล้วรอบนี้







- รอบ R174-R209 — ย้ายไป archive แล้วทั้งหมด: `archive/CHIEF_CONTINUATION_ARCHIVE_20260827_R166_R178.md` · `archive/CHIEF_CONTINUATION_ARCHIVE_20260828_R179_R190.md` · `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` (R186-R209 + แถว 027 + WIRED note)
- (ดัชนี R210-R214 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R210_R214.md` แล้ว โดย chief รอบ `k882hm` -- เพดาน 30 KB)
- (ดัชนี R215-R221 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R215_R221.md` แล้ว โดย chief รอบ `o1s522` -- เพดาน 30 KB)
(ดัชนี R222-R223 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R222_R223.md` แล้ว โดย chief รอบ `8i0lto` -- เพดาน 30 KB)


- (ดัชนี R224-R230 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R224_R230.md` แล้ว โดย chief รอบ `3ru85y` -- เพดาน 30 KB)
- (ดัชนี R231-R238 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` แล้ว โดย chief รอบ `bunu7v` -- เพดาน 30 KB)
- (ดัชนี R239-R242 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R239_R242.md` แล้ว โดย chief รอบ `65etwo` -- เพดาน 30 KB)
- (ดัชนี R243-R246 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R243_R246.md` แล้ว โดย chief รอบ `hxri6s` -- เพดาน 30 KB)
- (ดัชนี R247-R252 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R247_R252.md` แล้ว โดย chief รอบ `drvc5e` -- เพดาน 30 KB)
- (ดัชนี R253-R258 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R253_R258.md` แล้ว โดย chief รอบ `52ogem` -- เพดาน 30 KB)
- (ดัชนี R259-R261 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R259_R261.md` แล้ว โดย chief รอบ `sa0qjb` -- เพดาน 30 KB)
- (ดัชนี R262-R264 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R262_R264.md` แล้ว โดย chief รอบ `7dvax5` -- เพดาน 30 KB)
- (ดัชนี R265-R272 ย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260831_R265_R272.md` แล้ว โดย chief รอบ `gmcj4a` (R274) -- เพดาน 30 KB)
- R273(httmc6) 2026-08-31T~21:5x+07:00 audit round ไม่แตะ src ทั้งสองรีโป: round B R272 ทั้งสอง repo merged=true ยืนยันด้วย `pull_request_read get` ไม่มีของหาย · mailbox triage grep ADDRESSEE/ถึง: ทุกใบไม่มี stub (ตาม PROCESS_GATES #17): เจอ 2 ใบถึง chief จริง ทั้งคู่ superseded เองโดย P04 checkpoint ที่ consume ไปแล้ว (`1745` KA1B-TO-CHIEF, `1310` CODEX-NEWGEN auto) — stub ครบ · CORE-REQUEST audit: ไม่มีใบใหม่ค้าง (GM-044 เดียวที่มี ตอบไปแล้ว R268) · ledger PASS 47 ไม่มี drift · WIRED = 4/4 (ไม่เพิ่มโมดูลรอบนี้) · CHIEF_CONTINUATION.md 28170B / AGENTS.md 24945B ยังใต้เพดาน ไม่ต้องย้าย · ไม่มีโค้ดเกมใหม่ให้เทสรอบนี้ · push แล้ว รอ merge PR pf_bridge#635 / server#416 -> rounds/R273_httmc6_mailbox-triage-two-superseded-codex-letters-stubbed-no-src-change.md
- R274(gmcj4a) 2026-08-31T~23:2x+07:00 wired LANE-A+LANE-B scene14 hostile-splice CORE-REQUEST (`world_population_handoff._roster_handoff`, bg0015_roster only); found+fixed 2 real regressions while wiring (require_pair ordering, false-positive SRC_ACTOR_STREAM_SITES pin from own comment text); full suite green 5972 passed/0 failed; pf-adversary CONFIRMED a real defect in LANE-A's own `lane_a_choose_npc_scene14.py` (ChooseNPC click reverts the splice) -- reported to LANE-A, GT-178 opened+captioned accordingly; archived closed RE-132 (corrected a stale 154KB->8KB measurement error along the way); mob_ai_tick CORE-REQUEST deferred (no player-alive state in dispatch() yet, reason recorded); compressed R265-R272 index (see archive line above) to stay under the 30KB ceiling; WIRED=4/4 -> rounds/R274_gmcj4a_bg0015-hostile-splice-wired-plus-re132-archive-mailbox-triage.md
- R275(ijv02c) 2026-08-31T~23:5x+07:00 mailbox triage only, no src change either repo: round R274 (gmcj4a/gmcj4a) confirmed merged=true both repos via pull_request_read get (list_pull_requests' own merged field read false incorrectly -- tool quirk noted, not a project problem); no new CORE-REQUEST since R274 close; 2 letters to chief consumed+stubbed (LANE-B gate415 fix, Codex checkpoint P0-6 partial); re-verified mob_ai_tick CORE-REQUEST deferral from R274 is correct (grepped runtime.py, confirmed "HP has no write path in this project" -- real player-alive state does not exist, not a quick wire) -> rounds/R275_ijv02c_mailbox-triage-mob-ai-tick-deferral-confirmed-correct-no-src-change.md
- R276(jjs9bi) 2026-09-01T~01:1x+07:00 no src change either repo (pirate-force-server git status empty all round): mailbox triage found+stubbed a real 10-letter backlog missed by R272-R275's own sweeps (root cause: chief's own stub-existence check script bug this round, first pass falsely flagged 56 as unstubbed, corrected to the true 10 -- R273-275's "clean" claims were actually right); wrote PROCESS_GATES.md #18 restoring the RE-ticket route-tag rule (STATIC-ON-BRIDGE/CLOUD/NEEDS-ATTENDED-CAPTURE) that new tickets since RE-167 had dropped, which had silently idled the bridge RE runner 30+ hours; applied COO-DECISION 20260901_0042 to PF_ATTR_CONFLICTS_BUCKETS.tsv (511 rows closed across Q1/mask-gate/Q3-empty, 2 more Q3 rows closed, 8 rows left open pending a joint chief+GM read of the bridge-disk-only full table); corrected a stale RE-132 154KB queue-shrink target (already archived+fixed at R274 to 8KB) and re-measured the real remaining candidates fresh, naming GT-072 (102KB, confirmed) as next round's dedicated target; WIRED=4/4 unchanged -> rounds/R276_jjs9bi_mailbox-backlog-10-stubbed-re-tag-rule-restored-attr-conflict-q1-q4-applied.md
- R277(qux8c3) 2026-09-01T~02:0x+07:00 no src change either repo: mailbox triage grepped all 189 unstubbed files by real ADDRESSEE/ถึง header (PROCESS_GATES #17), found 21 genuinely chief/everyone-addressed (dating back to 08-28), stubbed all -- 20 already actioned elsewhere (named where in each stub), 1 (COO-DECISION 20260901_0148, lane self-close) recorded fresh as PROCESS_GATES.md #19; fixed one stale partial-consume (20260829_2255 had a consumed/ copy but no notes_to_chief/ stub, now complete); CORE-REQUEST audit: scene14 (Bg0015) hostile-splice CORE-REQUEST from LANE-A confirmed already wired by R274 (world_population_handoff.py ~1019-1033), stubbed as done; mob_pickup_persist + mob_ai_tick wiring (COO-DECISION 20260901_0145 told LANE-B to edit runtime.py directly) flagged to COO as a write-zone conflict (runtime.py is chief's alone bar the world-wipe exception) rather than wired blind or left for LANE-B to edit outside their zone -- CHIEF-ASK-COO sent, not started pending answer; GT-072 102KB queue-shrink (flagged by R276) NOT attempted this round, flagged again for a future round with dedicated budget; WIRED=4/4 unchanged -> rounds/R277_qux8c3_mailbox-backlog-21-stubbed-self-close-rule-recorded-scene14-corerequest-confirmed-done-pickup-ai-tick-ownership-asked.md
- R278(lperai) 2026-09-01T~04:1x+07:00 wired CORE-REQUEST-GM-045 (WORLD-CENSUS-001 read the departure scene's id instead of the destination's after a live GM warp -- new `_gm_warp_resync_selected_scene` in runtime.py, scene_id-only in-memory resync, reasoning for not also resyncing x/y/z in the method's own docstring); pf-adversary (mandatory pre-commit review) caught a real bug in the first draft -- the "two warps before one write" branch never resynced the second warp's scene, reproducing GM-045's own symptom one warp later -- fixed and pinned with a dedicated regression test; answered CORE-REQUEST-GM-046 (data pointer only, no code: `world_scene_travel.destination()`/`spawn_position()` is the existing per-scene spawn table login already uses; corrected an error in the reply's own first draft -- scene 278 already has a real pinned spawn, contra the draft's initial mis-grep); full suite 6128 passed/0 failed both before and after the adversary fix, ledger+coverage verifiers clean; opened GT-187 (BLOCKED on PR #438 merge) for attended client-observable confirmation; wrote PROCESS_GATES.md #20 (marker-substring PR-body hazard, from KA1A-CONFIRM's own measurement); mailbox triage stubbed 5 more chief/everyone letters (F-3 finding, GT-172 status, CODEX heartbeat + its COO-DECISION, KA1A-CONFIRM's 3 asks all closed); noted a process gap (not this round's) where PR #659/#434's real R278 work never got a rounds/ file or PR-body rename before merge, so this round's file-based counter landed on "R278" again -> rounds/R278_lperai_gm045-scene-resync-wired-gm046-answered-double-warp-bug-caught-by-adversary.md

- R279(6o3gr1) 2026-09-01T~05:1x+07:00 wired CORE-REQUEST heartbeat-preserve (LANE-B P-1) into app.py, install_ground_heartbeat_preserve(legacy) scoped to heartbeat_worker caller only via frame introspection after this round's own pf-adversary caught the first blanket-patch draft changing an unrelated connect-time packet too (also corrected a wrong claim about adapt_game_listener's globals-copy timing); re-pinned multiplayer-readiness-audit package_a_pinned_test_functions 89->91 across two test additions; wrote PROCESS_GATES.md #21 (scope shared-global patches by caller frame, verify CORE-REQUEST mechanism claims against source); opened GT-188 (attended, BLOCKED on PR merge, explicitly not gated to GT-146); mailbox triage stubbed 10 chief/everyone letters; full suite 6137/0 failed, ledger+coverage clean -> rounds/R279_6o3gr1_wire-heartbeat-preserve-corerequest-scoped-to-heartbeat-worker-mailbox-triage.md
- R280(2g7bph) 2026-09-01T~05:5x+07:00 no src change either repo: round R279 (6o3gr1/6o3gr1) confirmed merged=true both repos via pull_request_read get (list_pull_requests' own merged field again read false incorrectly, same known tool quirk); mailbox triage stubbed 11 letters this round, each cross-checked against the PR/letter that actually consumed it before stubbing (PANYA-ORDER 0215 -> R278 broadcast; GM-045/046 CORE-REQUEST cluster -> wired server#438; heartbeat-preserve CORE-REQUEST -> wired server#441, verified merged; 3 informational status/decision letters needing no action; 1 FYI letter); ~198 unstubbed letters remain, left for a future round's dedicated triage budget; WIRED=5/5 unchanged -> rounds/R280_2g7bph_mailbox-stub-backlog-retroactive-11-letters.md
- R281(5fsyp4) 2026-09-01T~06:4x+07:00 no src change either repo (housekeeping round): archived 133 stale rounds/*.md files (>3 days old) to archive/rounds_2026-08-27_to_28/ via git mv; shrunk oversized GT-072 queue entry 102KB->26KB (history relocated verbatim to archive/GT-072_history_20260901.md, adversary-verified lossless); mandatory pre-commit pf-adversary review caught a real defect the mover introduced -- 13 live cross-references (GAME_TEST_QUEUE.md x7, CLIENT_RE_QUEUE.md x4, 2 unarchived rounds/*.md) still pointed at the old pre-archive paths -- all repaired in place, target existence re-verified; ~35 stale citations inside already-consumed notes_to_chief/ letters deliberately left untouched (mailbox is append-only historical record); mailbox triage stubbed 11 chief-owned letters only (PROCESS_GATES #19 self-close rule narrowed scope -- single-lane-addressed letters now close themselves); ledger PASS 47 no drift; full suite 6156 passed/0 failed (cloud sanity); WIRED=5/5 unchanged -> rounds/R281_5fsyp4_rounds-archive-133-files-plus-gt072-shrink-plus-reference-repair.md
- R282(ts0deo) 2026-09-01T~08:1x+07:00 CORE-REQUEST-GM-047 (P0, COO-DECISION 20260901_0741): pinned BLOCKED-PENDING-GM047-FIX on GT-182 before code, fixed runtime.py:5304 (single-label check -> 3-label GM-warp set), 2 new dispatch-level regression tests (both cross-scene labels, pf-adversary caught the first draft only covered one) + renamed 3 misleadingly-named pre-existing tests per the CORE-REQUEST's own ask; registry row 028 recorded NOT wired (pending merge); shrank GT-078 (102703B->~8.4KB, history to archive/GT-078_history_20260901.md) per the queue-shrink mandate; mailbox triage stubbed 17 letters; self-caught-and-fixed-before-commit error: first-draft reply opened RE-133 (bridge regen ask) without checking a same-batch letter had already closed that exact gap in src/ two rounds earlier -- pf-adversary flagged it, RE-133 withdrawn in place, wrong IMAGE_ACCESS_COST.tsv row removed, reply+stub corrected; full suite 6159/0 failed, ledger PASS 47 no drift; WIRED=5/5 unchanged -> rounds/R282_ts0deo_gm047-p0-fix-gt078-shrink-mailbox-triage-plus-self-correction.md

- R283(69r41m) 2026-09-01T~09:0x+07:00 no src change either repo: confirmed CORE-REQUEST-GM-047 merged both repos (pf_bridge#680, server#452, pull_request_read get + direct runtime.py:5304 source read on main), registry row 028 -> wired; lifted GT-182 BLOCKED-PENDING-GM047-FIX warning to BLOCKED-ON-ATTENDED [NEEDS-ATTENDED-CAPTURE] (TOC + full entry + RECHECK note); mailbox triage stubbed 3 chief/everyone letters (2 COO-DECISION ack-only, 1 LANE-B tooling note self-resolved); self-caught mid-round: a parallel Bash call cd mistake put a stray commit on the wrong repo branch, caught by push refspec failure before anything was lost, fixed with git reset --hard to the pushed commit -> rounds/R283_69r41m_gm047-merge-confirmed-gt182-unblocked-mailbox-triage.md
- R284(632iyt) 2026-09-01T~09:5x+07:00 no src change either repo (platform-only round): implemented PANYA-DECISION 20260901_0920 in full -- pf_bridge PF_STALE_MINUTES 45->55 (ready-attempt only) + new PF_STALE_CLOSE_HOURS=6 (close bound, split from the ready-attempt bound); both repos got a liveness guard before the reaper's age-based close (commits/{sha} committer date <30min -> leave open); pf-adversary (mandatory pre-commit) caught 2 real defects in the first draft -- unbounded liveness reprieve (fixed: caps at 2x the close bound) and a commits/ API call that could abort the whole reap tick under set -e (fixed: guarded fallthrough) -- both re-validated (yaml dup-key strict + bash -n all run: blocks); executed COO-DECISION 20260901_0741's mandatory queue-shrink (noted R283 skipped it without explanation, flagged not blamed): GT-127 CLOSED-PASS entry 57,425->7,609B, GAME_TEST_QUEUE.md 1,702,807->1,652,991B, history to archive/GT-127_history_20260901.md, byte-verified lossless; mailbox triage stubbed 8 letters (RE-188-RESULT correctly left unstubbed for LANE-A, its opener, per the open-it-consume-it rule); WIRED=5/5 unchanged -> rounds/R284_632iyt_reaper-threshold-split-liveness-guard-plus-mailbox-triage-plus-gt127-shrink.md
