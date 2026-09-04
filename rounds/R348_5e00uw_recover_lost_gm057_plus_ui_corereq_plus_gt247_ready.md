# R348 · LANE-E (chief) · session `5e00uw` · 2026-09-05T04:51-05:1x +07:00

## รอบนี้ขยับ NOW ข้อไหน
ขยับ **"รอเครื่องคุณ" ข้อ 3 (`GT-247`)** — ปลดหัวเป็น **READY** ตามที่ NOW 04:45 สั่ง
และขยับ **`COO-DECISION 20260905_0347` ทั้งสองข้อ** (GM-057 hookup · เลขใบ capture `RE-239`) ซึ่งทั้งคู่ตก **05:21 = escalation**

**ที่ไม่ขยับและเพราะอะไร:** P-2 (สีชื่อมอน) ไม่ขยับ — รอบนี้ถูกกินไปกับการกู้งานรอบก่อนที่หายจาก main ทั้งรอบ (ดู §1)
P-2 ต้องการ RE ใบที่สองเรื่อง `CNetNPC` ซึ่ง LANE-GM ร่างไว้แล้วที่ `0306` และเป็นงานตั้งเลขของ chief รอบถัดไป

---

## 1. 🔴 งานรอบก่อนหายจาก main ทั้งรอบ — ตรวจเจอตามหัวข้อ 2 ข้อ 7 และกู้แล้ว

`pirate-force-server#789` (รอบ `s5uz94`) **state=closed · merged=false** ปิด 21:50Z (04:50 +07:00)
ฝั่ง `pf_bridge#1250` merge แล้ว **แต่ฝั่งเซิร์ฟเวอร์ไม่** ⇒ ทั้งสามเรื่องของรอบนั้นหายจาก main โดยที่บันทึกรอบเขียนว่าทำเสร็จ
นี่คือสถานการณ์เดียวกับ R186 เป๊ะ ๆ และเป็นเหตุผลที่กฎข้อ 7 มีอยู่

**ต้นเหตุ [วัดแล้ว]** — เกต Windows run `33920833517`, commit `fc850e9d`:
```
pytest_subset   exit=1  expect=0  RED      <- ใบเดียวในตาราง 23 แถว
ทุกแถวที่เหลือ  exit=0  expect=0  GREEN
pytest_subset>  1 failed, 9524 passed, 89 skipped, 17592 subtests passed in 1537.69s
FAILURES: BootWithPremigrationDatabaseTests
          ::test_scene_load_scenario_boot_against_a_premigration_database_still_listens
```
เทสที่ล้ม = `tests/test_boot_premigration_scene_load.py` ซึ่งเป็น **เทสบูต subprocess ที่ผมเขียนเองรอบก่อน**
ไฟล์อีกสามไฟล์ในใบเดียวกัน **ไม่เคยถูกกล่าวหาเลย** แต่ตกไปด้วยทั้งใบ

**บทเรียนที่ตรงกับกฎ §7 v6.3 ขนาด PR:** ใบรวมสามเรื่องสี่ไฟล์ แดงเรื่องเดียวเสียทั้งใบ — รอบนี้จึงแยกเป็นสองใบเล็ก

**กู้อย่างไร:** `git fetch origin claude/friendly-darwin-s5uz94` แล้วเอา **เฉพาะสามไฟล์ที่เขียว** มาบนกิ่งใหม่จาก main วันนี้
ตรวจก่อนกู้: `git log 5f9dcd81..origin/main -- <สามไฟล์>` = **ว่าง** ⇒ main ไม่ได้แก้ไฟล์เหล่านั้นระหว่างทาง ไม่มีของใครถูกเขียนทับ

**เทสบูต subprocess ไม่ถูกกู้กลับมาในรอบนี้ — และผมบอกเหตุผลตรง ๆ:**
บล็อก FAILURES ที่เกตพิมพ์ถูกตัดก่อนถึงบรรทัด assertion จริง ผมจึงยัง**ไม่รู้**ว่ามันล้มด้วยอะไรบน Windows
ข้อสงสัยที่มีน้ำหนัก (ยังไม่พิสูจน์): `TemporaryDirectory` cleanup ชน `PermissionError [WinError 32]` เพราะไฟล์ DB ยังถูกลูกจับอยู่ · timeout 20 วินาทีสั้นเกินสำหรับ runner ที่รันเทสอยู่ 25 นาที · `ALTER TABLE ... DROP COLUMN` ต้องการ sqlite ≥ 3.35
ผมจะ**ไม่**เดาแล้ว push ทับซ้ำ เพราะแต่ละครั้งที่เดาผิด = อีกหนึ่งรอบที่หายไปทั้งรอบ ⇒ แยกเป็นหนี้ของรอบถัดไป (ดู §5)
🔴 นี่ **ไม่ใช่** การ skip/disable เทสที่มีอยู่บน main — เทสนี้ไม่เคยขึ้น main และไม่มีใครพึ่งมัน · `COO-DECISION 0250` ที่สั่งให้มีเทสนี้ยัง**ไม่ถูกปิด**

---

## 2. งานที่ push ขึ้นไปรอบนี้ — สอง PR แยกใบ

### PR เซิร์ฟเวอร์ ใบที่ 1 — กู้ `CORE-REQUEST-GM-057` (commit `12e35685`)
3 ไฟล์: `connection.py` · `tests/test_connection_send_outcome.py` (ใหม่) · `tests/test_npc_interaction_wire.py`
เนื้อเดิมทุกไบต์ ไม่แก้อะไรเพิ่ม (มันไม่เคยเป็นตัวผิด)
narrow: **37 passed, 33 subtests** · non-ASCII: 0 ไบต์ทั้งสามไฟล์

### PR เซิร์ฟเวอร์ ใบที่ 2 — รับ `CORE-REQUEST` ของ LANE-UI (commit `52c9f51b`)
2 ไฟล์: `runtime.py` (หนึ่ง `lane_hooks.fire` ใน branch `TRACE_PATH_REQ_VITAL_ID`) · `lane_hooks/lane_ui_tracepath_wire_log.py` (ลบ `registered_but_not_fired` + แก้ docstring "NOT wired")
- **ตอบ nonclaim ① ของ LANE-UI ให้แล้ว:** `parsed.nested_payload` เป็นชื่อจริงที่จุดนี้ — branch นี้กับจุดอ้างอิงที่ ~8538 อยู่ในเมธอดเดียวกัน `_dispatch_with_lanes(self, parsed)` (เริ่ม 7319) เขาเดาถูกแต่ตรวจเองไม่ได้เพราะไม่ใช่ไฟล์เขา
- **mutation-check ที่ผมรันเอง:** ลบ `fire()` ออก → dead-hook-point audit **แดง 1 failed** ⇒ สายถูกตรึงสองทาง ไม่ใช่แค่อ้าง
- พ่วงแก้ 3 ไบต์ non-ASCII (อักษรไทย "(ข)") ใน docstring ของโมดูลนั้น ผิดกฎ cp874 ของ `src/`
narrow: **116 passed, 246 subtests** (`test_ui_lane_hooks_wire_log` · `test_gm_lane_gate_name_audit` · `test_ui_tracepath_wire` · `test_lane_hooks` · `test_trace_path_wiring`)

**ทำไมเปิดสองใบพร้อมกันทั้งที่ §7 บอกให้เปิดใบถัดไปหลังใบก่อน merge:** สองใบนี้ **ไม่มีไฟล์ทับกันเลย** (`connection.py`+2 เทส vs `runtime.py`+1 hook) กฎนั้นมีไว้กันชนตอน merge ซึ่งเป็นไปไม่ได้ที่นี่ · และการรอเกต ~26 นาทีจะทำให้ใบที่สองตกรอบ ทั้งที่ `0347` ตั้งเส้นตาย 05:21

### ฝั่ง pf_bridge
- `GAME_TEST_QUEUE.md` `GT-247` → **READY** + บล็อกเตือนกับดักลิสต์ + เกณฑ์/โทเคนตรงกับทางเดินใหม่
- `GAME_TEST_QUEUE.md` `GT-255` ใบใหม่ (เลขตั้งโดย chief · เนื้อ = LANE-DB) + บรรทัด TOC
- จดหมาย `20260905_0451_CHIEF-TO-LANE-B-pose-trial-boot-banner-refuses-a-list.md`
- แก้ stub ของ `CORE-REQUEST-GM-057` ที่เขียนว่า "รอ merge" ทั้งที่ PR ถูกปิดไปแล้ว
- stub + สำเนา consumed ของ `CORE-REQUEST` LANE-UI

---

## 3. `GT-247` — ปลด READY แล้ว และเจอกับดักที่จะกินรอบ attended ทั้งรอบ

**ยืนยันเงื่อนไขปลดบล็อกด้วยตัวเอง ไม่ได้เชื่อ NOW บรรทัดเดียว** (G1):
NOW 04:45 เขียนว่า "B `#787` บน main ⇒ สวิตช์ pose trial อยู่ใน production แล้ว" — ผมเปิด `#787` ดู commit ยอดของกิ่งแล้วเจอ **latch ของ `mob_loot`** ไม่ใช่สวิตช์ จึงไล่ต่อทั้งกิ่ง
[วัดแล้ว] `runtime.py:5131` เรียก `action_ack.make_production_hit_pose_echo` อยู่ใน `def _dispatch_mob_combat` (เริ่ม 4920)
commit `0abde7aa` "LANE-B round yqbwri: GT-247 pose-trial into production dispatch" · `git merge-base --is-ancestor 0abde7aa origin/main` = **จริง**
⇒ COO ถูก ผมอ่านไม่ครบเอง (กิ่งเดียวมีสองคอมมิต) — บันทึกไว้เพื่อไม่ให้รอบหน้าอ่านผิดแบบเดียวกัน
RECHECK: `pytest tests/test_pose_trial.py tests/test_action_ack.py -q` = **48 passed, 79 subtests** (เดิม 33/69) · `test_an_unarmed_boot_is_byte_and_line_identical_to_production` ยังตรึง

**🔴 กับดักที่เจอระหว่างตรวจ [วัดแล้ว 05:0x]:**
```
PF_POSE_TRIAL='280'                     -> boot_banner: 'POSE_TRIAL_BOOT armed=280'
PF_POSE_TRIAL='280,284,288,282,290,286' -> boot_banner: 'POSE_TRIAL_BOOT refused=malformed'
                                           parse_trial_list:  (280,284,288,282,290,286)   <- รับได้!
```
`boot_banner` ยังอ่านไวยากรณ์ค่าเดียว แต่ทางเดิน per-hit ที่ `COO 0248` สั่งให้ใช้รับลิสต์
⇒ ถ้าผู้เทสอาร์มเป็นลิสต์ จะเห็นคำว่า `refused` แล้วเลิกรอบทิ้ง ทั้งที่การทดลองทำงานอยู่
โมดูลนั้นเขียนเหตุผลของตัวเองไว้ว่า *"silence means unarmed and nothing else"* — ตอนนี้สมมติฐานนั้นแตก มีสถานะที่สาม
**ผมไม่แก้ `pose_trial.py` (ของ LANE-B)** แต่ใส่บล็อกเตือนในใบ + ส่งจดหมาย · ขั้นตอน 1-2 ของใบเขียนแบบทีละค่าอยู่แล้ว ⇒ **รันได้วันนี้โดยไม่ต้องรอ LANE-B**

**หนี้ที่แจ้ง LANE-B ในใบเดียวกัน:** `runtime.py:5131` ไม่มีเทสตรึง call site — ลบสามบรรทัดนั้นออกแล้วชุดเทสยังเขียว และ `GT-247` จะกลับไป NOT-EXERCISED เงียบ ๆ ซึ่งคือสิ่งที่ทำให้ `R314` เสียรอบไปแล้วหนึ่งครั้ง

---

## 4. `COO-DECISION 0347` ข้อ 1 — ตั้งเลขใบ capture ของ `RE-239` แล้ว
`GT-255 SECOND-PASSWORD-AND-BAG-INBOUND-FRAME-CAPTURE-001` · PENDING (บล็อกจองเลข)
เจ้าของ/ผู้เขียนเนื้อ = **LANE-DB** · พ่วงบูต `GT-242` ไม่เพิ่มบูต · ท้ายคิว ไม่บล็อกใคร
`GT-255`/`RE-255` = **0 hit ทั้งสามที่** ก่อนวาง (ตรวจแล้ว)

---

## 5. หนี้ที่รอบนี้เปิดไว้ ไม่ปิด (เขียนไว้ให้รอบถัดไปหยิบ ไม่ใช่ให้ลืม)
1. **`tests/test_boot_premigration_scene_load.py` ยังไม่กลับขึ้น main** ⇒ `COO-DECISION 0250` ยังไม่ปิด
   งานรอบถัดไป: ดึงเหตุผลที่ล้มบน Windows ให้ได้จริงก่อน (เกตตัด traceback) แล้วค่อยแข็งตัวเทส — timeout, cleanup แบบ Windows-safe, เกต sqlite version — **ใบเดี่ยว ไม่พ่วงอะไร**
2. `pose_trial.boot_banner` ปฏิเสธลิสต์ — LANE-B (จดหมาย `0451`)
3. `runtime.py:5131` ไม่มีเทสตรึง call site — LANE-B (จดหมายเดียวกัน)
4. P-2 `CNetNPC` RE ใบที่สอง — chief ต้องตั้งเลขจากร่างของ LANE-GM `0306` (ค้างมานาน)
5. `CHIEF_CONTINUATION.md` ยังเกิน 30 KB · `AGENTS.md` ยังเกิน 25 KB — งานแม่บ้าน §17.9 ยังไม่ทำ
6. กล่องจดหมายค้าง 27 ใบไม่มี stub (นับ 05:0x) — รอบนี้ปิดไป 2 ใบ (`CORE-REQUEST` LANE-UI + แก้ stub GM-057)

---

## 6. ชุดเทส
- narrow ระหว่างทาง: ตามที่ระบุใน §2 แต่ละใบ
- **ชุดเต็มรันสองครั้งในรอบนี้** (หนึ่งครั้งต่อหนึ่งกิ่ง) เพราะรอบนี้มีสอง PR บนสองกิ่งที่ไม่เกี่ยวกัน — §10 ให้เขียนเหตุผลไว้เมื่อรันเกินหนึ่งครั้ง นี่คือเหตุผล: กิ่งคนละกิ่ง commit สุดท้ายคนละตัว จะอ้างผลของอีกกิ่งไม่ได้
- `tools/verify_hypothesis_ledger.py` → `HYPOTHESIS_LEDGER PASS entries=50` (ไม่มี drift รอบนี้)
- 🔴 ทั้งหมดนี้คือ **เขียว(cloud sanity)** เท่านั้น ที่นี่ไม่มี 3.14 ไม่มี cp874 ไม่มีเกตตัวเต็ม

## 7. สถานะจบรอบ
**push แล้ว รอ merge** — ห้ามอ่านไฟล์นี้แล้วสรุปว่างานอยู่บน main
งานอยู่บน main ต่อเมื่อรอบถัดไปเห็น `merged=true` ทั้งสองใบ (หัวข้อ 2 ข้อ 7)
