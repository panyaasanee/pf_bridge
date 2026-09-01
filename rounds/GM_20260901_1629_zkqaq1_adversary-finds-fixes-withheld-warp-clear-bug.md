# LANE-GM round zkqaq1 (scheduled, no attended watching) -- 2026-09-01T16:29+07:00

## NOW.md check (บังคับก่อนทุกอย่าง)

อ่าน `NOW.md` แล้ว (ตรวจล่าสุดโดย COO 14:47+07:00, 3 ข้อด่วน P-1/P-2/P-3 + คิวต่อท้าย)
รอบนี้ขยับ NOW ข้อไหน: **ไม่มีข้อไหนขยับสถานะ** เหตุผลแยกตามข้อ:

- **P-1**: ไม่ใช่ของสาย GM
- **P-2**: ยังรอ `RE-195` (เปิดโดย chief 16:05 ตอบ `CORE-REQUEST-GM-048`) -- chief ตัดสินแล้วว่า
  P-2 ผูกกับ FontStyleID selector ไม่ใช่ faction comparator (บริโภครอบนี้) แต่ยังเขียนโค้ดสีไม่ได้
  จนกว่า RE-195 จะตอบว่ากลไกไหนมี server-controllable input จริง -- ตรวจ `CLIENT_RE_QUEUE.md` แล้ว
  ใบยังเปิดอยู่ ไม่มี RESULT ใหม่รอบนี้
- **P-3**: นอกเขต repo ทั้งสอง (native DLL) -- RE-164 ข้อ 1/3 ยังต้องการ disassembly ที่ไม่มีใน
  clone นี้ (ยืนยันซ้ำจากรอบ `vsopwk`/`0626`) รอ RE runner ผ่าน chief เหมือนเดิม ไม่มีอะไรใหม่ให้ขยับ
- **GM-A**: ไม่ใช่ตัวบล็อกสายตามกฎใหม่ (โค้ดเสร็จ รอ Panya รัน `GT-192`)
- **GM-B**: LANE-DB ถือเต็ม
- **UI-A/UI-B**: ของ LANE-A

## ก่อนเริ่ม: ยืนยันไฟล์อ้างอิง

`../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (`ls -la` รอบนี้)

## Part A -- ชะตา PR รอบก่อน (r2jfjm)

`pull_request_read(method=get)` ตรง ๆ ทั้งสองใบ (ไม่เชื่อ `list` เฉย ๆ): `pf_bridge#723`
`merged:true` (2026-09-01T08:24:23Z) · `pirate-force-server#483` `merged:true`
(2026-09-01T08:32:53Z) -- งานรอบก่อนอยู่บน `main` แล้ว ไม่ต้อง cherry-pick

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo ก่อนแตะไฟล์ใด ๆ: ไม่มี `[LANE-GM]` ค้าง (server repo
มี `[LANE-E] #487` และ `[LANE-A] #484` ของสายอื่น ไม่แตะ) เปิด draft PR ยึดล็อกก่อนทำงาน:
`pf_bridge#729`, `pirate-force-server#488` (commit เปล่า "round claim: zkqaq1" ทั้งสอง repo ก่อน)

## Part B -- กล่องจดหมาย

ใบ `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` (ตรวจ header บรรทัดแรกจริง ไม่ใช่แค่ grep คำใน
เนื้อความ -- รอบก่อน ๆ เคยมี false positive จากใบที่แค่พูดถึง "LANE-GM" ในเนื้อหา): มีหนึ่งใบ

`notes_to_chief/20260901_1605_CHIEF-REPLY-gm048-target-fontstyleid-not-faction-re195-opened.md`
-- บริโภคแล้ว (สตับ + สำเนาไป `consumed/`) เนื้อหา: chief ตัดสิน P-2 ผูกกับ FontStyleID selector,
ยืนยันไม่มีวิถี wire ส่ง FontStyleID วันนี้ (ตรงกับที่ใบ `1519` ของสายนี้เองวัดไว้แล้ว), เปิด
`RE-195` ให้ตอบว่า `0x0043C380` กับ `0x4A1D50` เป็นฟังก์ชันเดียวกันหรือไม่ -- สายนี้เป็นผู้บริโภคผล
ตามสัญญาของใบ ยังไม่มีผลรอบนี้

## สิ่งที่ทำรอบนี้: pf-adversary เจาะ warp wire ที่ merge แล้ว เจอบั๊กจริงในเขตเขียนของสายนี้เอง

Agent tool (`subagent_type: pf-adversary`) ใช้ได้จริงรอบนี้ (เหมือนรอบ `bxkxfc`) -- ให้ตรวจ
`gm/warp_executor.py` และ `gm/teleport_wire.py` ย้อนหลัง (ไฟล์ wire ที่ blast radius สูงสุดที่เพิ่ง
ผ่าน live cross-scene warp จริง `GT-172` PASS) เทียบกับเทสของทั้งสองไฟล์ว่าเทสไล่ผ่าน dispatch จริง
หรือแค่เรียกฟังก์ชันแยกส่วน

**พบข้อบกพร่องจริง 1 ข้อ (ตรวจซ้ำด้วยตัวเองจาก source ตรง ๆ ก่อนเชื่อ):**
`src/pirateforce_foundation/gm/chat_command_action.py:1256-1259` -- tuple ที่เช็คว่า action label
ไหน "ต้อง clear parked warp target เมื่อ audit-log เขียนไม่สำเร็จ" มีแค่สอง label
(`WARP_ACTION_LABEL`, `WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`) แต่ตอนนี้มีสาม label จริง (GM-A เพิ่ม
`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL` เข้ามาโดยไม่แก้ tuple นี้ -- ยืนยันจาก git log
commit `cdf5d7b`) ผลคือ `/warp <เลขแมพ>` แบบไม่มีพิกัดที่ audit-log ล้ม (`OSError`) จะทิ้ง
`gm_last_warp_target` ค้างไว้ทั้งที่ไม่มี byte ไหนออกไปจริง ขัดกับ invariant "ไม่มี byte ออก = ไม่มี
target ค้าง" ที่ comment ของโค้ดจุดเดียวกันเขียนไว้เอง (ยังไม่เคยเป็น false-positive จริงบนจอ เพราะ
`runtime.py`'s confirm-token gate อ่านแค่ label ที่อยู่ใน `actions` ที่ dispatch คืนจริง ไม่ใช่ target
ที่ parked ไว้เฉย ๆ -- แต่เป็น landmine รอโค้ดจุดอื่นในอนาคตที่อ่าน `gm_last_warp_target` นอก gate นี้)

**สาเหตุที่เทสเดิมไม่จับ:** `tests/test_gm_command_audit_outcome.py`'s
`test_the_withheld_warp_leaves_no_parked_target_behind` ทดสอบแค่ label เดียว (`/warp 2 100 200`,
ForcePos) ไม่มีเทสไหนไล่ label ที่สามผ่าน dispatch จริงภายใต้ audit failure -- ซ้ำแพทเทิร์นเดียวกับ
บั๊ก `runtime.py:5304` ของรอบ `bxkxfc` (self-review "ฟังก์ชันมีอยู่และ logic ดูถูก" แต่ไม่ไล่ label
จริงที่ caller ใช้) เพียงแต่รอบนี้บั๊กอยู่ในเขตเขียนของสายนี้เอง (`gm/`) ไม่ใช่ของ chief -- แก้เองได้
ทันที ไม่ต้องเปิด CORE-REQUEST

## แก้แล้วรอบนี้

`src/pirateforce_foundation/gm/chat_command_action.py:1256-1261`: เพิ่ม
`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL` เข้า tuple + แก้ comment เดิม ("BOTH WARP LABELS"
ที่ล้าสมัยตั้งแต่มี label ที่สาม) เป็น "ALL THREE" พร้อมบันทึกว่า tuple นี้เคย drift มาแล้วครั้งหนึ่ง
ไม่ใช่ single source of truth

เพิ่มเทสสองตัวใน `tests/test_gm_command_audit_outcome.py`
(`AuditFailureIsFailClosedTests.test_the_withheld_cross_scene_warp_leaves_no_parked_target_behind`,
`.test_the_withheld_no_coords_cross_scene_warp_leaves_no_parked_target`) ครอบทั้งสอง label ที่ขาด
เดิม -- **มิวเทชันเทสจริง**: revert fix ชั่วคราวแล้วรัน สอง เทสใหม่ -- ตัวที่คุมเลเบล no-coords ล้ม
ตามคาด (`AssertionError: WarpTargetRecord(...) is not None`) เอา fix กลับมา รันซ้ำผ่านหมด ยืนยันว่า
เทสจับบั๊กได้จริงไม่ใช่ green ปลอม

## เทสที่พิสูจน์

`python3 -m pytest tests/ -q` = **6350 passed, 327 skipped, 13717 subtests passed, 0 failed**
เขียว(cloud sanity) (baseline รอบก่อน 6156 passed -- ส่วนต่างมาจากงานสายอื่นที่ merge เข้า main
ระหว่างนี้ ไม่ใช่ของรอบนี้ทั้งหมด; ของรอบนี้เองคือ +2 เทสใหม่)
`tools/verify_hypothesis_ledger.py` PASS entries=48 (ไม่ขยับจากรอบก่อน)
`tools/verify_functional_coverage.py` PASS domains=8 (ไม่ขยับจากรอบก่อน)

## pf-adversary

รันจริงผ่าน Agent tool รอบนี้ (ไม่ใช่ self-review) -- รายงานเต็มอยู่ในบทสรุปของ subagent ระบุ 1 บั๊ก
จริง (แก้แล้วข้างบน) และตรวจ 6 หัวข้ออื่น (auth gate, scene validation, kill-switch regression test,
`warp_executor.*`'s hardening, `teleport_wire.py`'s wire codec round-trip, `FORCE_POS_VITAL_
VERSION_CONFIRMED` release) ไม่พบปัญหา -- บันทึกไว้กันขุดซ้ำ

## ที่ไม่ทำในรอบนี้ (เจตนา)

- ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
  `scenarios/combat_*.json` -- นอกเขตเขียนทั้งหมด
- ไม่เขียนโค้ดสีมอนสเตอร์ใด ๆ -- ยังรอ `RE-195`
- ไม่รวม shared `GM_WARP_LABELS` frozenset ที่ pf-adversary เสนอไว้เป็นคำถามปิดท้าย -- มีจุดใช้เดียว
  ใน `chat_command_action.py` วันนี้ (tuple ที่แก้ไปแล้ว) การเพิ่ม abstraction ตอนนี้จะเกินสิ่งที่ต้อง
  ใช้จริง เก็บไว้เป็นข้อสังเกตถ้ามีจุดที่สามที่ต้องรู้ label ครบสามตัวในอนาคต

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี (บนจอ)** -- นี่คือการปิด invariant ที่ไม่เคยแสดงผลผิดบนจอจริง (landmine ที่ปิดก่อนมีคนสะดุด
ไม่ใช่บั๊กที่ attended tester เคยเจอ) ไม่มี wire ใหม่ ไม่มี chat command ใหม่ให้ลอง

nonclaim ตาม §3 ของหลักการสาย GM: การแก้นี้ปิด landmine ที่ pf-adversary เจอ ไม่ใช่หลักฐานว่า P-2/P-3
ขยับ และไม่ได้ boot เกม/เซิร์ฟเวอร์ใด ๆ รอบนี้ -- ไม่มี GM ข้ามขั้นในรอบนี้เลย

## nonclaims

1. ไม่อ้างว่าบั๊กนี้เคยแสดงผลเป็น false-positive จริงบนจอ -- ตรวจแล้วว่า confirm-token gate ยังไม่
   อ่านจุดนี้วันนี้ เป็น landmine ไม่ใช่ observed defect
2. ไม่อ้างว่า RE-195 ตอบแล้ว -- ยังเปิดอยู่ ตรวจ `CLIENT_RE_QUEUE.md` ตรง ๆ รอบนี้
3. ไม่แตะ `npc_hostile_hypothesis.py`/`runtime.py`/`app.py`/`pf_login_game_server_v141.py`/
   canonical DB/`scenarios/world_*.json`/`scenarios/combat_*.json`
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
5. ไม่ลบประวัติ/จดหมายเดิม -- สตับใหม่เท่านั้น ต้นฉบับสำเนาไว้ที่ `consumed/` ครบ

## PR

`pf_bridge#729` / `pirate-force-server#488`

Companion: `pirate-force-server` (branch `claude/upbeat-fermi-zkqaq1`, src fix + 2 tests)

PF-AUTOMERGE: v4

— สาย GM รอบ `zkqaq1`
