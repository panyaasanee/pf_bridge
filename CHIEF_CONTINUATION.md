# PIRATE FORCE — Chief Architect continuation file



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

(แถวเปิด 011 012 014 015 017 021 026 — สรุปย่อคำต่อคำย้ายไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260829_R229_trim.md` · ถ้อยคำเต็มอยู่ใน `archive/CORE_REQUEST_REGISTRY_ARCHIVE_20260828_R211_rows001-026.md` เหมือนเดิม · เลขจองล่าสุด: 027)







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
