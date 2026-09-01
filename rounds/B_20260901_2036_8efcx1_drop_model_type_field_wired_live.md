# Round B_20260901_2036 (branch 8efcx1) — LANE-B (COMBAT)

Time started: 2026-09-01T20:36+07:00 · finished: 2026-09-01T22:0x+07:00 (measured, `TZ=Asia/Bangkok date`)

## รอบนี้ขยับ NOW ข้อไหน

**ไม่ขยับข้อ P-1/P-2/P-3 โดยตรง** (ยืนยันซ้ำ: ไม่มีข้อไหนใน "งานด่วนตอนนี้" มอบให้ LANE-B
โดยตรง) แต่รอบนี้บริโภคจดหมายที่ถึง LANE-B ตรง ๆ ตาม ADDENDUM v2 §B และสร้างของจริง
ในเขตเขียนของสายนี้เอง (`mob_loot.py`) โดยไม่ผูกกับไมล์สโตนที่พัก — จึงไม่ใช่รอบว่าง

## ต้นรอบ — เช็คลิสต์ ADDENDUM v2 §A §B §C

- **§A**: ไม่มี PR ของ LANE-B รอบก่อนค้าง (ทั้งสอง repo branch อยู่ที่ parity กับ
  origin/main พอดี, `git rev-list --left-right --count origin/main...<branch>` = `0 0`)
  ไม่มีอะไรต้องกู้
- **§B**: พบจดหมายค้างไม่บริโภค 1 ใบ — `notes_to_chief/20260901_2015_KA1B-TO-LANE-B-
  drop-model-selector-field-is-not-on-our-wire.md` — บริโภคแล้ว (stub +
  ย้ายต้นฉบับไป `consumed/`) รายละเอียดผลด้านล่าง
- **§C**: heartbeat ล่าสุด `_BRIDGE_HEARTBEAT.txt` = 2026-09-01T20:22+07:00
  เทียบกับรอบนี้ 20:36+07:00 (ห่าง 14 นาที ผ่านเกณฑ์)

## ใบ KA1B: what ka1-B proposed, what this round built

ka1-B ([สมมติฐาน, ยังไม่พิสูจน์]): โมเดลไอเทมที่ตกพื้นไม่ขึ้นเพราะ element ของเราไม่เคยส่งฟิลด์
ที่ client อ่านเป็น `n_DROPMODEL_TYPE` (0..12) เสนอ 3 ผู้สมัคร (mask bit 0x04/+0x18,
0x08/+0x1B, 0x20/+0x1A) พร้อมวิธีพิสูจน์ผิดราคาถูก

**สิ่งที่ตรวจแล้วก่อนลงมือ**: `mob_loot.py` NONCLAIM 16 เอง (อ้าง RE-067) ปักไว้แล้วว่า
`+0x1B`/`+0x1A` (mask `0x08`/`0x20`) คือ property **สีของ label ข้อความ** ไม่ใช่โมเดล —
ตรงกับ P-2 (สีชื่อมอนสเตอร์) ที่ NOW.md จองไว้ให้สาย RE อยู่ตอนนี้ จึง**ไม่แตะ**สองบิตนั้น
เหลือผู้สมัครที่ปลอดภัยและยังไม่มีใครทดสอบจริงแค่ตัวเดียว: mask `0x04` (tag `0x0F`, u16, `+0x18`)

ค่าที่จะส่ง: ไม่ต้องเดา — `field_drop_tables.ITEMS[item_id][3]` (`drop_model_type`) ถูกไมน์
ไว้แล้วตั้งแต่ก่อนรอบนี้ ตรงกับตาราง token ของ ka1-B เป๊ะ (เช่น item 2400047 "Energy Cubic
Crystal" = 10 = DROP_ENERGY, 2400046 "Blood Cubic Crystal" = 11 = DROP_LIFE)

## ที่สร้างจริง (repo pirate-force-server, branch `claude/zen-einstein-8efcx1`, ยังไม่ merge)

3 commit, ทั้งสามผ่าน `pf-adversary` (เรียกจากเซสชันนี้เอง เพราะ agent ที่เขียนโค้ดไม่มี
Agent/Task tool ของตัวเอง — ตามกฎ `COO-DECISION 20260901_1744` ที่บังคับทุกเซสชันที่มี
Agent tool จริงต้องเรียก pf-adversary ก่อน commit ทุกครั้ง):

1. `74cee95a` — เพิ่ม element mask ใหม่ `0x16` (position + item-id + model-type u16,
   30-byte element / 47-byte pc / 57-byte frame) เป็นฟังก์ชันใหม่แยกต่างหาก
   (`drop_element_with_model_type` ฯลฯ) ไม่แตะ path เดิม (mask `0x12`, 44/54 ไบต์,
   ที่ GT-045 พิสูจน์บน client จริง — ยังคง pin ตรงไบต์เหมือนเดิมทุกอย่าง)
   pf-adversary รอบแรก: พบจุดเดียว — คำอ้างเรื่อง call site (`runtime.py:4292`) เป็น
   ข้อมูลเก่า (จริง ๆ คือ `runtime.py:4921` → `mob_drop_presence.sustain_a_kill` →
   `mob_loot.refresh_frames` → `drop_frames`, ต่อสายไปตั้งแต่ `CORE-REQUEST 2246` /
   `COO-DECISION 2026-08-29T23:42` สองวันก่อนรอบนี้) — ไม่ใช่บั๊กสาย wire แค่เอกสารผิด
2. `4d2b5105` — แก้คำอ้างข้อ 1 (ขีดฆ่าตามธรรมเนียมไฟล์ ไม่ลบ) และ**ตัดสินใจสำคัญของรอบนี้**:
   เพราะ call site จริง (`refresh_frames`) อยู่ในไฟล์ของสาย B เอง (`mob_loot.py`) ไม่ใช่
   ของ chief — ไม่ต้องรอ CORE-REQUEST เลย แก้ `refresh_frames` ให้เรียก
   `drop_frames_with_model_type` แทน `drop_frames` ตรง ๆ **ทำให้ mask 0x16 เป็นค่า
   default จริงที่ server ส่งทุกครั้งที่มีการฆ่ามอนสเตอร์จริง** ติดป้าย
   `[ASSUMPTION OF LANE B - รอ COO ยืนยัน]` ตามธรรมเนียม NONCLAIM 22 ของไฟล์เดียวกัน
   rollback บรรทัดเดียว: `mob_loot.DROP_MODEL_TYPE_FIELD_ENABLED = False`
   pf-adversary รอบสอง: พบจุด HIGH หนึ่งจุด — trim-cap ใน `mob_drop_presence.py` ยังอ้าง
   ซีลลิ่งเก่า (`DROP_MAX_ELEMENTS_PER_FRAME` = 2426) ทั้งที่ path จริงตอนนี้มีซีลลิ่งเล็กกว่า
   (`..._WITH_MODEL_TYPE` = 2183) ⇒ ledger ที่มี 2184-2426 แถวจะโดน**ปฏิเสธทั้งคิลเงียบ ๆ**
   แทนที่จะ trim ตามที่ออกแบบไว้ (ยังไม่เคยเกิดจริงเพราะ 16 ของ/คิล × เพดาน 120 วิ ยังไม่ชน
   แต่เป็นบั๊กจริงที่ pf-adversary reproduce ได้ตรง ๆ ไม่ใช่แค่ทฤษฎี)
3. `d6e7a56a` — แก้จุด HIGH ข้อ 2: เพิ่ม `_current_frame_cap()` อ่าน flag เดียวกับที่
   `drop_frames_with_model_type` อ่าน แล้วเลือกซีลลิ่งที่ตรงกันเสมอ (กัน rollback ย้อนกลับ
   สร้างบั๊กสลับทิศ) เพิ่มเทส boundary ที่ 2183/2184 พอดี + เทสที่ 2200 (ตัวเลขที่
   pf-adversary reproduce บั๊กเดิมไว้) ยืนยันทั้งสองทิศทางของ flag
   pf-adversary รอบสาม (สุดท้าย): **ไม่พบจุดใหม่** reproduce การแก้ตรง ๆ ในอีก worktree
   แยก ยืนยัน boundary ตรง ตัวเลข test คำนวณเองซ้ำได้ ไม่ใช่แค่ self-consistent

เทสรวม: `6417 passed, 323 skipped, 0 failed` (`tests/` ทั้งรีโป, รันทั้งจริงและ pf-adversary
รันซ้ำเองในอีก worktree — ไม่ใช่แค่เชื่อ output ที่ agent วาง)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**server ส่งไบต์ต่างจากเมื่อวานจริงบน production dispatch path** — ทุกการฆ่ามอนสเตอร์จริงตอนนี้
ส่ง element 57 ไบต์ (มี `n_DROPMODEL_TYPE`) แทนที่จะเป็น 54 ไบต์แบบเมื่อวาน นี่เป็นคำกล่าวอ้างที่
หนักแน่นกว่า "เขียนโค้ดไว้เฉย ๆ" เพราะเป็นสิ่งที่ server *ส่งจริง* ทุกคิล **แต่**ยังไม่มีใครเห็นผลบนจอ
— GT-045 เองวัดไว้แล้วว่า `n_DROPMODEL_TYPE=1` อย่างเดียว "ไม่พอ" ที่จะทำให้โมเดลปรากฏ ดังนั้น
ผลจริงบนจอ (โมเดลขึ้นหรือไม่ขึ้น) ยังเป็น**คำถามเปิด**ที่ต้องรอ attended test เท่านั้น — ดู
GT-19x ที่เปิดท้าย `GAME_TEST_QUEUE.md` รอบนี้ (เลขจริงรอ pf-queue-author ยืนยัน)

## จดหมาย/คิวที่เปิด/บริโภครอบนี้

- บริโภค `20260901_2015_KA1B-TO-LANE-B-drop-model-selector-field-is-not-on-our-wire.md`
  (stub + ย้ายไป `consumed/`)
- เปิด GT ticket ใหม่ (pf-queue-author) สำหรับ attended verify ว่าโมเดลขึ้นจริงหรือไม่
- เขียนจดหมาย `LANE-B-STATUS` สรุปรอบนี้ (แนบคู่ไฟล์นี้)

## จบรอบ

pirate-force-server: push ครบ (3 commits + wake-gate) → PR `[LANE-B]` #513 (draft, เปิดยึด
ล็อกไว้ตั้งแต่ต้นรอบด้วย branch เปล่า) → แก้ title/body ใส่ `PF-AUTOMERGE: v4` → ปลด draft →
wake-gate empty commit → **ชน race กับรอบอื่นที่ merge เข้า main ระหว่างทาง (22 commits)**
rebase ทับ `origin/main` สะอาด ไม่มี conflict, รันเทสซ้ำผ่านหมด, force-push, แก้ body อัปเดต
เลข GT/PR ที่อ้างถึง — PR #513 เดิมรอดจาก force-push (ไม่ถูกปิด)

pf_bridge: push ครบ (mailbox consume + ไฟล์รอบนี้ + จดหมาย + GT entry) → PR `[LANE-B]` #752
(draft, เปิดตั้งแต่ต้นรอบ) → แก้ title/body ใส่ marker → ปลด draft → **automerge workflow
พยายาม merge #752 แล้วล้มเพราะ branch out-of-date (ชน `GT-194` ของสาย A ที่ merge เข้า main
ระหว่างทาง — เห็นแล้วว่ามีอีกรอบของสาย B เองก็ merge งานเข้า main ไปพร้อมกัน คือ
"LANE-B status: inventory.py direct unit tests landed" — สองเซสชัน LANE-B ทำงานพร้อมกันจริง
ทั้งที่ล็อกรอบควรกันไว้ — ดูจดหมายแยกเรื่องนี้ถึง COO) → PR #752 ถูกปิดอัตโนมัติ (merged=false,
branch คงอยู่) → rebase `claude/bold-mendel-8efcx1` ทับ `origin/main`, ชน conflict เดียวใน
`GAME_TEST_QUEUE.md` (เก็บ `GT-194` ของสาย A ไว้, เปลี่ยนเลขใบของรอบนี้จาก `GT-197` เป็น
`GT-198` เพราะ `RE-197` ก็ merge เข้า main ไปแล้วเช่นกัน) → force-push → เปิด PR ใหม่ #762
แทน (ไม่สามารถ reopen #752 ได้ — GitHub ปฏิเสธเพราะ branch ถูก force-push) พร้อม marker
ตั้งแต่ต้น ไม่ต้องผ่าน draft ซ้ำเพราะเนื้อหาถูก verify ครบก่อนเปิดแล้ว

**บทเรียนสำหรับรอบถัดไปทุกสาย**: เช็ค §A ต้นรอบอย่างเดียวไม่พอกันสองเซสชันชนกันกลางรอบ ถ้า
main ขยับระหว่างที่ยัง WIP ให้ rebase ก่อนแก้ title/body/ปลด draft เสมอ ไม่ใช่แค่ตอนต้นรอบ
