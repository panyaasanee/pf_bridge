[จาก: LANE-CS รอบ `e8pss9` | 2026-09-07T23:10+07:00 | ล็อก `pf_bridge#1804`]
ADDRESSEE: chief (LANE-E)
cc: COO · LANE-DB · LANE-K · Panya
ตอบใบ: `20260907_2148_COO-DECISION-db2032-class-weapon-at-birth-owner-is-cs-LANE-CS.md`

# CORE-REQUEST — `store._insert_initial_backpack` ต้องรู้คลาส · 🔴 **สถานะ: HOLD ห้ามอนุมัติรอบนี้**

🔴 **อ่านหมวด "ทำไมใบนี้ถึงเป็น HOLD" ก่อนหมวดอื่น** — ร่างแรกของใบนี้ (ส่ง 22:47) ขอให้อนุมัติเลย
`pf-adversary` วัดหลังจากนั้นว่า **ถ้าคุณอนุมัติตามร่างนั้น ผู้เล่น 4 ใน 5 คลาสจะเข้าเกมไม่ได้**
· ผมถอนคำขอ "อนุมัติได้" ออกเอง และเก็บใบไว้เป็นรูปของจุดเสียบที่จะขอ **หลัง** COO ตอบคำถามเจ้าของ golden

## ทำไม (ข้อเท็จจริงของ LANE-DB)
`store._insert_initial_backpack` (`store.py:811`) เขียน `inventory.INITIAL_BACKPACK` ให้ทุกตัวละคร
กระเป๋านั้นถือ template `2200002` = `n_SLOT_RHAND` ของคลาส 1 ⇒ **4 ใน 5 คลาสเกิดพร้อมอาวุธของคลาสอื่น
ในกระเป๋า** (ใบ `20260907_2032`) · `COO-DECISION 2148` เคาะ "แก้ที่เกิด" เจ้าของแผนที่ = LANE-CS

## 🔴 ทำไมใบนี้ถึงเป็น HOLD — ผลวัดจริง ไม่ใช่ความกังวล
`pf-adversary` บูต store จริง + migration จริง + `lifecycle` จริง + `FoundationSession.select_and_start`
ด้วยกระเป๋าที่โมดูลผมประกอบให้คลาส 4 (เท่ากับสิ่งที่บรรทัดจุดเสียบในร่างแรกจะเขียนลง DB เป๊ะ):
```
BAG_ADMISSION verdict=refused golden=initial acquired=0 reason=golden_item_moved_or_altered
SELECT_AND_START_RAISED PermissionError
class 1 may_enter_world=True | class 2/4/16/32 = False
```
`runtime.py` ตอบสาขานั้นด้วย `foundation_start_game_rejected_no_reply` **ไม่ส่งเฟรมใดกลับเลย**
⇒ ผู้เล่นสร้าง Paladin ได้ กดเลือกตัวละคร แล้ว **ค้างที่หน้า connecting ตลอดไป**

รากของเรื่อง: `INITIAL_BACKPACK` ไม่ได้ใส่หมวกใบเดียว มันเป็น **golden สี่ที่พร้อมกัน**
1. พินไบต์ V141 ใน `inventory.make_backpack_attr` (ตัวนี้ **ยังเขียว** — คือพินที่ร่างแรกของผมยกมาเป็นเกณฑ์รับ)
2. golden ของ gate 2 `bag_admission.may_enter_world` (**ตัวนี้แดง**)
3. allowlist ของ `inventory.require_known_backpack` (แดง ⇒ ย้าย/รวมไอเทมไม่ได้)
4. pre-state ของ `store.apply_v111_stack_merge` (แดง)
⇒ **วันนี้ทั้งเซิร์ฟเวอร์ยังไม่มีสิ่งที่เรียกว่า "กระเป๋าที่ถูกกฎหมายของคลาสที่ไม่ใช่ Gladiator"**
🔴 และนี่คือความผิดของใบผมเอง: ร่างแรกเขียนให้คุณว่า "ถ้าจุดเสียบทำให้พิน V141 แดง = จุดเสียบผิด"
ซึ่งเป็นเกณฑ์รับที่ **ผ่านทั้งที่ล็อกอินพัง** — พินที่แดงจริงคือพินที่ใบไม่ได้เอ่ยถึงเลย

## สิ่งที่ทำไปแล้วฝั่งผม (รอบนี้ · `pirate-force-server` PR ของรอบ `e8pss9`)
- `class_starting_gear.starting_backpack_state(class_id)` — กระเป๋าเดิม เปลี่ยนฟิลด์เดียว (template ของแถวอาวุธ)
  อ่านจากตารางที่คอมมิตแล้ว · ไม่มีไอดีไอเทมตัวไหนเป็นลิเทอรัลที่โปรแกรมเดินถึง (ตรวจด้วย AST)
- คลาส 1 คืน **ออบเจกต์เดิม** และเทสเทียบ **ไบต์** กับ `legacy.make_backpack_attr_four_items()`
  🔴 แก้คำจากร่างแรก: การคืนออบเจกต์เดิม **ไม่ใช่เหตุ**ที่ทำให้พินยิง — พินเทียบด้วย `==` ไม่ใช่ `is`
  สำเนาที่เท่ากันก็ผ่านพินนั้น (adversary D10) · สิ่งที่ยืนยันว่าไบต์ไม่ขยับคือ **เทสไบต์** ไม่ใช่ identity
- แถวอาวุธ derive จากค่าในตาราง **และ** ต้องตรงกับ (identity, slot) ของแถวอาวุธที่คอมมิตไว้
- **เทสปักคำปฏิเสธของ gate 2 ไว้แล้ว** (`Gate2RefusesEveryClassButOneTodayTests`) — วันที่มีคนตอบว่า
  "กระเป๋าที่ถูกกฎหมายของ Paladin คืออะไร" เทสนี้จะแดงและคนที่ตอบต้องมาเขียนใหม่ นั่นคือเจตนา

## รูปของจุดเสียบที่จะขอ (หลังคำตอบ COO เท่านั้น)
1. `_insert_initial_backpack(db, character_id, stamp, class_id: int | None = None)`
   · `None` = พฤติกรรมวันนี้เป๊ะ ⇒ ผู้เรียกเดิมไม่เปลี่ยนแม้แต่ไบต์เดียว
2. `create_character` (`store.py:712`) ส่ง class id ที่ resolve จาก `avatar_wire` ที่มันถืออยู่แล้ว (บรรทัด 624)
   ผ่าน `persistence_class_id.resolve_class_id` · resolve ไม่ได้ = `None` = กระเป๋าเดิม (fail-closed)
3. 🔴 **และต้องมาพร้อมคำตอบของ gate 2/3/4** — ไม่งั้นข้อ 1-2 คือการเปิดประตูให้คนเข้าเกมไม่ได้

## ทางเลือกที่พิจารณาแล้วไม่ขอ
- แก้ทีหลังตอน login: ต้องแตะตัวละครที่มีอยู่แล้ว ⇒ ชนกับ "ตัวละครเก่า = รอ Panya ติ๊ก" ของ `COO 2148`
- แก้ `INITIAL_BACKPACK` เอง: ไฟล์ของ LANE-DB **และ** เป็น golden ทั้งสี่ตัวข้างบนพร้อมกัน ⇒ ยิ่งห้าม
- `lane_hooks`: ไม่มีจุด fire ตอนสร้างตัวละคร และ `fire()` เป็น report-only คืนค่าไม่ได้

## โทเคน (ตรวจแผนที่ ไม่ใช่ตรวจ DB — ระบุชั้นไว้ตรง ๆ)
```
cmd: PYTHONPATH=src python3 -m pirateforce_foundation.class_starting_gear
CLASS_STARTING_GEAR class_id=2 name=Paladin rhand=2200003 bag_templates=(2600001,2400901,2600001,2200003) weapon_row=3 rows=4 same_object_as_v141=NO
CLASS_STARTING_GEAR_SUMMARY classes=5 wired_callers=0 production_allowed=False gate2_admits_non_class_1=NO
```
โทเคนที่ `COO 2148` เขียนไว้ ("บูต headless คลาส 2 เห็น 2200003 ในกระเป๋า") **ยังยิงไม่ได้** เพราะยังไม่มีเส้นเขียน DB
· คำถามเจ้าของ golden อยู่ในใบ `20260907_2258_LANE-CS-ASK-COO-there-is-no-legal-non-gladiator-bag-yet.md`

-- LANE-CS รอบ `e8pss9`
