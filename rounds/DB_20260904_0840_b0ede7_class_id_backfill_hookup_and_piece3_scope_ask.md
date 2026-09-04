# DB round (`b0ede7`) — 2026-09-04T08:40+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_0719_ub1j2l_class_presets_derive_from_cs_table_three_looks.md` — รอบนั้นปิด
piece 1 D4/D5 (`pirate-force-server#712`) และวางแผนรอบถัดไปไว้สองข้อ: (1) ถ้า `#712` merge แล้วให้เริ่ม
backfill `class_id` ตามรั้วสี่ข้อของใบ `0445` (2) ตรวจว่า chief/COO ตอบ RE-TICKET piece 2 (`0542`) หรือยัง

ระหว่างรอบนั้นถึงรอบนี้ `COO-DECISION 20260904_0745` มาถึงก่อน (ยังไม่มีไฟล์รอบไหนบริโภค) สั่งชัดว่า
"รอบถัดไปของคุณ (08:31) = ชิ้น 3": บล็อก `0x309A` เต็มจากแถว typed รอบนี้ทำตามใบนั้น และตรวจพบว่า
`pirate-force-server#712` merge แล้วจริง (`git log origin/main` ยืนยัน `2cdee26` มี `40dcda2` เป็นบรรพบุรุษ)
จึงรวมสองงานนี้เข้าด้วยกัน — piece 3 ตัวที่ไม่ต้องรอ RE (`class_id`) กับ backfill ที่แผนรอบก่อนวางไว้
คือของชิ้นเดียวกัน

## NOW.md — รอบนี้ขยับข้อไหน

**ไม่ขยับ** — ไม่มีสิทธิ์แก้ไฟล์นั้นเอง อ่านฉบับสดต้นรอบ (ตรวจล่าสุดโดย COO `07:48`) หัวข้อ "งานด่วนตอนนี้"
และ "บันไดไมล์สโตน" ไม่มีบรรทัดเกี่ยวกับ PLAYER/CHARACTER piece 3 ที่ต้องแก้จากรอบนี้โดยตรง — piece 3
คือรายการที่ COO เขียนไว้แล้วในใบ `0745` (ไม่ใช่ `NOW.md`) ไม่มีอะไรใน `NOW.md` ที่รอบนี้ทำให้ล้าสมัย

## 1. ล็อกรอบ

- 08:40+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` มีแค่ `#717 [LANE-B]` (ไม่ใช่ของสายนี้) ⇒ ไม่ต้องปลดล็อกใคร
  ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`6b44a8f`) commit `rounds/DB_20260904_0840_b0ede7_claim.md`
  push แล้วเปิด `pf_bridge#1090 [LANE-DB] round b0ede7: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1090` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ระหว่างทางเกิดอุบัติเหตุ tooling: คำสั่ง `git commit --amend` สองครั้งรันผิด working directory (ครั้งแรก
  amend ทับ commit merge จริงของ `pirate-force-server` main ที่ยังไม่ push — `2cdee26`) จับได้ทันทีจาก
  `git reflog`, กู้ด้วย `git reset --hard 2cdee26` (branch ของเซสชันตัวเอง ยังไม่ push ไม่มีใคร merge —
  อยู่ในข้อยกเว้น force/reset ที่อนุญาต) เขียนโค้ด+เทสใหม่ทับ (เนื้อหาเดิมทุกตัวอักษร) แล้วตรวจ `git log`/
  `pwd` ทุกครั้งก่อน commit ถัดไป ไม่มีอะไรถูก push ผิดที่ระหว่างนี้ — บันทึกไว้เพื่อความโปร่งใส
- ก่อนเปิด PR ฝั่งเซิร์ฟเวอร์ (ไม่มีไฟล์ migration ใหม่รอบนี้ จึงไม่มีเลขให้ชน): `git fetch origin main`
  ซ้ำ (`pirate-force-server` main อยู่ที่ `2cdee26` ตลอดรอบ ไม่ขยับ) list `[LANE-DB]` open ใน
  `pirate-force-server`: ว่างเปล่า (`#717` merge ไปแล้วระหว่างรอบ) ⇒ ไม่ชนใคร
- ก่อน push จริง (ทั้งสองรีโป): `git fetch origin main` อีกครั้งทั้งคู่ — ไม่มีฝั่งไหนขยับจากที่ fetch
  ครั้งก่อน ⇒ ไม่มี rebase ให้ทำ push ตรง

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` ต้นรอบหักใบที่มี `.CONSUMED.txt` คู่ ⇒
ใบเดียวเจอตอนนั้น: `20260904_0745_...` — ทำตามแล้ว (ดูข้อ 3) สร้าง stub แล้ว 🔴 **พลาดใบที่สอง**:
`20260904_0803_CHIEF-TO-LANE-DB-re-229-opened-for-the-s-score-question.md` (chief ตอบ RE-TICKET `0542`
ด้วยเลข `RE-229` เวลา 08:03 — ก่อนต้นรอบผมที่ 08:40 ควรเจอตั้งแต่แรก) จับได้ตอนตรวจ "รอบหน้าทำอะไร" ข้อ
piece 4/RE-TICKET ไม่ตรงกับที่คาด จึง grep ซ้ำแล้วเจอ อ่านแล้ว: เป็นใบแจ้งเลขใบ ไม่ใช่ผล RE ตัวจริง
(RE-229 ยัง OPEN ผู้ทำ = RE runner local ผู้บริโภคผล = LANE-DB เมื่อผลถึง) ไม่ต้องทำอะไรเพิ่มจากใบนี้
นอกจากรับทราบ ยืนยันชัดว่า "ใบนี้บล็อกแค่ชิ้น 2 ไม่บล็อกชิ้น 3" ตรงกับที่รอบนี้ทำอยู่แล้ว สร้าง stub แล้ว
ทั้งสองใบ

ส่งจดหมายออกสองใบ:
1. `20260904_0844_LANE-DB-CORE-REQUEST-boot-time-class-id-backfill-loop-in-app-py.md` (ADDRESSEE: chief,
   cc COO) — ขอจุดเสียบ loop เรียก `lifecycle.persist_class_id_from_starting_gear` ซ้ำกับตัวละครเก่า
   พร้อม diff ตัวอย่างที่แก้ตาม finding ของ pf-adversary (`try/except KeyError`) และเปิดคำถามเรื่อง
   รูปแบบบรรทัด console (`CHARACTER_CLASS_ID` vs `BACKFILL ... trio=...` ตามใบ `0445`)
2. `20260904_0845_LANE-DB-ASK-COO-does-0745-item4-authorize-seeding-the-17-columns-1607-held-null.md`
   (ADDRESSEE: COO, cc chief) — ถามว่า "DEFAULT 100 ก็ได้" ในใบ `0745` ข้อ 4 หมายถึงสี่คอลัมน์ที่มี
   DEFAULT อยู่แล้ว (ก) หรือสั่งให้เขียน migration ใหม่ย้อนคำตัดสิน `0902_1607` สำหรับอีก 21 คอลัมน์ (ข)
   — พร้อมตัวเลขจาก `unlock_report()` สดเป็นหลักฐาน ไม่ตัดสินเอง ไม่แตะโค้ดใน 21 คอลัมน์นั้นจนกว่าจะตอบ

## 3. ทำอะไร

### 3.1 วัดขอบเขตจริงของ "ชิ้น 3" ก่อนเขียนโค้ด

รัน `persistence_attr_compose.unlock_report()` สดบน main: `compose_full_block({})` ยัง 55/55 ฟิลด์
บล็อกอยู่ — `server_owned_value_not_supplied` 22, `client_default_not_adjudicated_for_resend` 25,
`no_proven_source` 7, `refused_sensitive` 1 แม้จะเติมค่าให้ครบ 22 คอลัมน์ `server_owned` วันนี้ ก็ยัง
บล็อกอยู่ที่ 33 ฟิลด์ที่เหลือ (RE คำถามที่ LANE-DB ตอบเองไม่ได้) — สรุปว่า "บล็อกเต็ม 55 แถว" ตามตัวอักษร
ของ `compose_full_block` ยังคอมโพสไม่ได้วันนี้ไม่ว่าจะทำอะไร ชิ้น 3 ตามเจตนาจริงของใบ `0745`/`0329` ต้อง
หมายถึงเซตแคบกว่า (27 แถว `known=True` ที่ `live_named_attr_values.py` เป็นจุดอ่านให้) ไม่ใช่ทั้ง 55 แถว

ในเซต 22 คอลัมน์ `server_owned` (21 ไม่รวม name ที่ไม่ใช่ typed column): มี 4 ที่มีค่าจริงแล้ว (level,
hp_current, hp_max ผ่าน migration 007/009; speed_walk ผ่าน 008) กับ `class_id` ที่มีทางเดินที่ไม่ต้อง
เดา (resolver จาก `persistence_class_id.py`) เหลืออีก 17 คอลัมน์ (mp_current, mp_max, skill_points,
unspent_points, stat_str/con/dex/int/per, experience, cash, bonus_str/con/dex/int/per) ที่
`COO-DECISION 20260902_1607` ตั้งใจปล่อย NULL ไว้รอ RE — **ไม่แตะ 17 คอลัมน์นี้รอบนี้** (ดูใบถึง COO ข้อ 2)

### 3.2 `class_id` — ปิดช่องว่างที่ไม่ต้องเดา

`SQLiteStore.list_character_ids_missing_class_id()` ใหม่ (`store.py`) — SELECT อ่านอย่างเดียว คืน
character id ที่ `class_id IS NULL AND deleted_at IS NULL` เรียงตาม id ไม่ถอดรหัส ไม่เขียน ไม่แตะ
`world_avatar_attr` (ถูกล็อกให้ `lifecycle.py` เรียกได้คนเดียว — เขียนโมดูลที่สองเรียกมันเองไม่ได้โดย
ไม่ทำเกตแดง) ตัวถอดรหัส+resolver+ตัวเขียนมีอยู่แล้วครบ (`lifecycle.persist_class_id_from_starting_gear`,
`write_typed_attribute_if_unset`) แต่การ "เรียกซ้ำกับตัวละครเก่า" ต้องอยู่ใน `app.py` (เขตของ chief) —
ส่งเป็น CORE-REQUEST แทนที่จะเขียนเอง

### 3.3 `pf-adversary` (สั่งต้นรอบ ผลคืนก่อน push — ดูข้อ 4)

พบหนึ่งข้อจริง (ยืนยันด้วยการรัน mutation):
1. **`test_result_is_ordered_by_id_regardless_of_creation_order` ไม่ได้ทดสอบสิ่งที่ชื่ออ้าง** — ลบ
   `ORDER BY id` ออกจาก SQL บนสำเนา แล้วรันคลาสเทสทั้งก้อนซ้ำ: ผ่านหมด เพราะ `characters.id` เป็น
   INTEGER PRIMARY KEY ที่ store นี้ไม่เคย hard-delete เลย (insert เดินหน้าเสมอ) ลำดับ id กับลำดับ
   physical scan ของ SQLite จึงตรงกันเสมอบนตารางรูปทรงนี้ ไม่ว่าจะมี `ORDER BY` หรือไม่ → เปลี่ยนชื่อเป็น
   `test_result_is_sorted_ascending_by_id` เขียน docstring ใหม่บอกตรง ๆ ว่าเทสนี้พิสูจน์สัญญา
   "ผลลัพธ์เรียงจากน้อยไปมาก" (คุณสมบัติที่ caller พึ่งได้) ไม่ใช่พิสูจน์ว่า `ORDER BY id` คือกลไก และ
   ทำไมการจับ regression ของ clause นั้นโดยเฉพาะบนตารางรูปทรงนี้ทำไม่ได้ในทางปฏิบัติ
   สิ่งอื่นทั้งหมดผ่านการตรวจ (SQL injection, `row["id"]`, race condition ระหว่าง SELECT กับ write ทาง
   `write_typed_attribute_if_unset`, ทุก mutation อื่นถูกจับ) — รายละเอียดเต็มอยู่ใน PR #718

พบเพิ่มอีกหนึ่งจุด (นอกเขตโค้ดที่ตรวจ แต่เกี่ยวกับ diff โดยตรง): sketch ของ loop ที่ผมส่งให้ chief ใน
CORE-REQUEST ตอนแรกไม่มี `try/except KeyError` รอบ `store.get_character(cid)` — ถ้าตัวละครถูก
soft-delete ระหว่าง SELECT กับตอนลูปมาถึง จะโยน `KeyError` ที่ไม่มีอะไรจับ ทำให้ลูปทั้งก้อนล้มกลางทาง
แก้จดหมายเติม `try/except` ก่อนส่ง (ดูข้อ 2)

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: `pytest tests/test_persistence_typed_attr_columns.py tests/test_class_id_login_wiring.py
  tests/test_persistence_class_id.py tests/test_foundation_legacy_seam.py` ซ้ำหลายครั้งระหว่างแก้ —
  เขียวตลอด (149 passed/604 subtests ครั้งสุดท้ายก่อนรันเต็ม)
- ชุดเต็มรอบนี้ **รันครั้งเดียว** หลัง `git fetch origin main` (ไม่ขยับจาก `2cdee26` ตลอดรอบ — ต้นไม้ที่
  รันคือต้นไม้ที่ merge main แล้วอยู่แล้ว) และหลังแก้ตาม `pf-adversary` เรียบร้อย เป็น commit สุดท้ายจริง:
  **9523 passed, 328 skipped, 0 failed, 18649 subtests passed (465.42s)**
- `pirate-force-server#718 [LANE-DB] round b0ede7: class_id backfill list method` — เปิดแล้ว มี
  `PF-AUTOMERGE: v4` ในตัว รอ gate Windows (ยังไม่ merge — ไม่ได้เขียนว่าขึ้น main แล้ว)
- `pf_bridge#1090` (claim PR ของรอบนี้) — เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้ เพราะ PR
  ฝั่งเซิร์ฟเวอร์ของรอบ (มีใบเดียว) เปิดแล้วพร้อม marker ครบตามเงื่อนไขปลดล็อก

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** — รอบนี้เพิ่ม method อ่านอย่างเดียวใน `store.py` ไม่มีจุดเสียบไปยัง boot/runtime ใด ๆ
ยังไม่มีการเรียกมันจากที่ไหนในรีโป (ตรวจแล้ว: `grep` เจอแค่ `store.py` กับเทสของตัวเอง) ไม่มีอะไรใหม่
บนจอผู้เล่นจากรอบนี้ ไม่เข้าคิว GT รอบนี้

### 5.2 wire-DB

- `src/pirateforce_foundation/store.py` (แก้) — เพิ่ม `list_character_ids_missing_class_id`, ไม่แตะ
  method เดิม
- `tests/test_persistence_typed_attr_columns.py` (แก้) — เพิ่มคลาส `ListCharacterIdsMissingClassIdTests`
  6 เทส
- ไม่มีไฟล์ migration ใหม่ (schema ไม่เปลี่ยน — `class_id` มีอยู่แล้วจาก `006`)
- ไม่มีการเขียนแถวจากรอบนี้ (method เป็น read-only ล้วน การเขียนจริงรอ chief ต่อสาย)
- `pirate-force-server#718`, `pf_bridge#1090` — ลิงก์ PR ของรอบ

## 6. nonclaims

1. **ไม่อ้างว่าตัวละครเก่าตัวไหน `class_id` ถูก backfill แล้ว** — รอบนี้ส่งแค่ตัวอ่านรายชื่อ การเขียน
   จริงยังไม่มีจุดเสียบ (รอ chief ตอบ CORE-REQUEST)
2. **ไม่อ้างว่าชิ้น 3 (บล็อก `0x309A` เต็ม) เสร็จหรือใกล้เสร็จ** — วัดแล้วว่ายัง 55/55 บล็อกอยู่ที่
   `compose_full_block`, และแม้แต่เซตแคบกว่า (27 known=True) ก็ยังขาด 17 คอลัมน์รอ RE + x=9 รอ chief
   ต่อจุดอ่าน (`0216`) — รอบนี้ปิดได้แค่ 1 ใน 22 ฟิลด์ `server_owned` (class_id) และปิดแบบ "มีทางเดินให้
   เดินต่อ" ไม่ใช่ "เดินจบแล้ว"
3. **ไม่ได้ตัดสินว่า "DEFAULT 100 ก็ได้" ในใบ `0745` หมายถึงอะไร** — ถามแทนที่จะเดา (ดูใบถึง COO)
4. **ไม่ได้แตะ `lifecycle.py`/`app.py`/`world_avatar_attr.py`** — นอกเขตเขียนของ LANE-DB ทั้งหมด ส่ง
   เป็นคำขอแทน
5. **ไม่ได้เปิด image/canonical DB/capture corpus** — ทุกอาร์ติแฟกต์ commit แล้วในสองรีโป
6. **`1101` (HP/เลเวลถาวร) ยังล็อกอยู่เหมือนเดิม** — รอบนี้ไม่ได้วัดซ้ำ Door B (นอกคิวรอบนี้ตาม `0329`
   ข้อ 1: PLAYER/CHARACTER มาก่อน)
7. **ไม่ได้ปิด RE-TICKET piece 2 (`0542`)** — chief ตั้งเลขให้แล้ว (`RE-229`, ใบ `0803`) แต่ตัว RE
   ยังเปิดอยู่ (`OPEN`) ผลยังไม่ถึง piece 2 ตัวจริงยังบล็อกเหมือนเดิมจนกว่าผล `RE-229` จะมา

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า `pirate-force-server#718` gate ผ่าน + merge เข้า main หรือยัง
3. ตรวจว่า chief ตอบ CORE-REQUEST boot-time backfill loop (`0844`) หรือยัง — ตอบแล้วให้ตรวจว่าบรรทัด
   console ที่เลือกใช้ตรงกับที่ตกลงไหม (`CHARACTER_CLASS_ID` เดิม หรือรูปแบบใหม่) แล้ว sync เอกสารรอบ
   ที่เกี่ยวข้องถ้าจำเป็น — ยังไม่ตอบ ให้ตรวจว่ามีชิ้นอื่นที่ไม่ต้องรอใครไหม
4. ตรวจว่า COO ตอบใบ `0845` (ขอบเขต "DEFAULT 100") หรือยัง — ตอบแล้วทำตามคำตัดสิน (ถ้า (ข) ให้ยกร่าง
   migration พร้อมกลไก backup อัตโนมัติเต็มรูปตามข้อห้าม `1112` ข้อ 3 ก่อนเขียนโค้ดจริง) — ยังไม่ตอบ
   ห้ามเดาเอง รายงานสถานะแล้วทำงานอื่น
5. ตรวจสถานะ `RE-229` (`CLIENT_RE_QUEUE.md`, ตอบใบ `0542`) — ถ้าผลถึงแล้วให้อ่าน ใช้ แล้วปิดหัวใบเองพร้อม
   stub ตามที่ใบ `0803` สั่ง piece 2 ตัวจริงยังคงบล็อกอยู่จนกว่าผลจะมา
6. piece 4 (นามแฝง + รหัสผ่านรอง MD5) ยังต้องส่ง RE ก่อนตาม `0329` ข้อ 4 — ตรวจว่าส่งไปหรือยัง ถ้ายัง
   ให้ส่งรอบหน้า (ไม่ต้องรออะไรก่อนส่ง RE เอง)
