[ถึง: chief cloud · cc COO, Panya | จาก: สาย B (COMBAT), รอบ `B_20260827_1637` · 2026-08-27 ~16:46 (+07:00)]

# LANE-B STATUS -- บริโภคผล GT-084-R2 แล้ว, อัปเดตหัวใบ GT-084/GT-084-R2, เปิด RE-107/RE-108,
บันทึกผลวัด (body-dependent ไม่ใช่ class-dependent) ลง `mob_death.py` -- ไม่แก้พฤติกรรม

## สรุปสั้น

จดหมาย `20260827_1620_GT084R2-RESULT-...md` (attended, Panya ขับเอง, OBSERVER_CONFIRMED
15:52-15:55) เป็นผลของใบที่สาย B เป็นเจ้าของ (`GT-084`/`GT-084-R2`) -- บริโภคแล้วรอบนี้
ตามกติกา "ใครเปิดใบ คนนั้นบริโภคผล" ผลคือ: wire/DB ครบ (hit x5, HP to 0, kill, dying/
dead frame, loot x2, census 115/115 คงที่) แต่ client-observable FAIL 2 จุด: ศพแข็งลอย
ไม่ล้ม (ต่างจาก GT-022/GT-025) และ single-click ไม่มีแผงเป้า (ต่างจาก GT-045 v3)

## แก้อะไรบ้าง

**`GAME_TEST_QUEUE.md`** (สิทธิ์แก้เฉพาะบรรทัดหัวใบของใบที่สาย B เป็นเจ้าของ, ไม่แตะ
เนื้อใบ):
- `GT-084` หัวใบ: `[READY -- merged, ...]` -> RESULT อ้างผลต่อของ GT-084-R2, ระบุ
  wire PASS / client-observable FAIL 2 จุด, ห้ามอ่านเป็น PASS/DONE
- `GT-084-R2` หัวใบ: `[PENDING]` -> RESULT, claim หลัก (hostile ที่ตาเห็น) PASS ด้วย
  หลักฐานพฤติกรรม แต่ไม่ตรงเกณฑ์สี/แผงตามใบเป๊ะ, สถานะสุดท้าย (PASS/MIXED) ทิ้งให้
  chief ตั้งตามกฎ 🔴 chief เป็นคนตั้งสถานะสุดท้ายเสมอ -- สายนี้แค่กรอกผล

**`CLIENT_RE_QUEUE.md`** -- เปิด `RE-107`/`RE-108` (grep ยืนยัน 0 hit ก่อนจอง, เลข
สูงสุดก่อนหน้าคือ `106`):
- `RE-107` MOB-DEATH-DYING-DEAD-ANIMATION-DRIVER-001 [STATIC-ON-BRIDGE] -- field/frame
  อะไรคุม fall-vs-freeze ของ body ชื่อ+hostile actor_type 4 (predicate `0x43BDA0`/
  `0x43BD70` ที่ `mob_death.py` pin ไว้แล้วเป็นจุดเริ่มให้ RE)
- `RE-108` SELECT-TARGET-UI-PANEL-REQUIRED-FRAME-001 [STATIC-ON-BRIDGE] -- field/frame
  อะไรที่ client ต้องการถึงจะเปิดแผงเป้า (ต่างจาก GT-045 v3 ที่เปิดได้)

ทั้งสองใบไม่ตอบคำถามเอง (ตามกฎเลนนี้ "คุณไม่ตอบคำถาม คุณสร้างของ") -- แค่เปิดให้ RE
runner ขุด static เอง

**`mob_death.py`** (repo `pirate-force-server`) -- เอกสารล้วน ตามธรรมเนียม
`[UPDATE, round <id>, <date>]` ของไฟล์เอง (strike ด้วย `~~text~~` ไม่ลบ):
- module docstring: เพิ่ม bullet ใหม่ใต้ "WHAT IS CLIENT-OBSERVABLE..." บันทึกว่า
  named+hostile body ถูกส่ง+สังเกตครั้งแรกแล้ว (GT-084-R2) และผลไม่ล้ม -- สรุปว่า
  two-frame chain's effect **BODY-DEPENDENT ยืนยันแล้ว** ไม่ใช่คำถามเปิดของ actor_type
  อย่างเดียวอีกต่อไป
- ย่อหน้า `[PROPOSED, not measured]` เดิม -- เติม update ว่าตอนนี้ MEASURED แล้ว, ผล
  mixed ("stays there" จริง แต่ "falls flat" ผิด)
- `MOB_DEATH_NONCLAIMS` -- ต่อท้าย 2 รายการเดิม (เรื่อง "named and hostile...never
  observed") ด้วย `[STALE as of GT-084-R2] [MEASURED, by <จดหมาย>]:` -- ไม่ลบคำเดิม
- `production_allowed`, `DEATH_TASK_HOLD_MS`, `DYING_TIMER_SECONDS` -- **ไม่แตะ**
  (ยืนยันด้วย git diff, ดูรอบไฟล์ด้านล่าง)

`scenarios/combat_death_001.json` -- regenerate จาก `pin_document()` (เปลี่ยนแค่ 2
บรรทัดตรงกับ nonclaims 2 รายการที่แก้ -- ไม่มีตัวเลข/VA/timer ไหนขยับ)

`tests/test_mob_death.py` -- เติมคอมเมนต์อธิบาย (ไม่ใช่ assertion ใหม่) ตามที่คำสั่งรอบนี้
อนุญาตเฉพาะคอมเมนต์ ไม่ปั้นข้อเท็จจริงที่ยังไม่วัด

## สวีตเต็ม

`tests.test_mob_death`: 70/70 passed (รวมเทสที่เทียบ pin document กับ nonclaims
ตรงๆ -- จับได้จริงตอนลืม regenerate JSON รอบแรก แก้แล้วรันซ้ำเขียว) ·
`tests.test_mob_combat` + `tests.test_field_mobs`: 64/64 passed · cp874-encodable
ตรวจแล้วทั้งสามไฟล์ที่แก้ (`src/ tests/ scenarios/` อยู่ในสโคปที่ gate บังคับ)

## กล่องจดหมาย

บริโภคจดหมาย `20260827_1620_GT084R2-RESULT-...md` แล้ว -- สร้าง `.CONSUMED.txt` +
คัดลอกต้นฉบับเข้า `notes_to_chief/consumed/` (สร้างโฟลเดอร์ใหม่ ยังไม่เคยมี) ไม่ลบ
ต้นฉบับ

## CORE-REQUEST / boundaries

**none** -- ไม่มีอะไรในรอบนี้ต้องแก้ `runtime.py`/`app.py`
`current/pf_login_game_server_v141.py` ไม่ถูกแตะ (ทดสอบอ่านอย่างเดียวผ่าน `load_legacy()`
ที่มีอยู่แล้วก่อนรอบนี้) `scenarios/world_*.json` ไม่ถูกแตะ (คนละไฟล์กับ
`combat_death_001.json` ซึ่งเป็น pin ของ `mob_death.py` เอง ไม่ใช่ world scenario ของสาย A)

## ยังไม่ได้พิสูจน์

- `RE-107`/`RE-108` ยังเปิดอยู่ -- คำตอบจริงว่าฟิลด์ไหนคุม fall/แผงเป้ายังไม่มี
- สถานะสุดท้าย (PASS/MIXED) ของ `GT-084`/`GT-084-R2` รอ chief ตั้ง
- Loot บนพื้นที่เซิร์ฟเวอร์ส่งจริง (2 ใบ) ยังไม่มีใครยืนยันว่าเห็น/ไม่เห็นบนจอ

## ไม่ push, ไม่เปิด PR (ตามคำสั่งรอบนี้)

`pirate-force-server` branch `claude/admiring-galileo-9rvtdp` (3 ไฟล์แก้, ยังไม่
commit) · `pf_bridge` branch `claude/friendly-ride-9rvtdp` (5 ไฟล์ใหม่/แก้ + จดหมายนี้,
ยังไม่ commit) -- ปล่อยให้ chief ตรวจแล้ว commit/เปิด PR เอง ไม่มี `[LANE-B]` PR เปิดค้าง
ที่ต้องกังวลเรื่อง round lock

รายละเอียดเต็ม: `rounds/B_20260827_1637_gt084r2_consumed_re107_re108_opened.md`

-- สาย B · COMBAT
