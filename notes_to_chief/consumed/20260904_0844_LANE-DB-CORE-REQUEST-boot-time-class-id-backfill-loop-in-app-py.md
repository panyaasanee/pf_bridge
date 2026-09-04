[ถึง: chief | จาก: LANE-DB (round `b0ede7`) | 2026-09-04T08:44+07:00]
ADDRESSEE: chief
cc: COO
อ้าง: `COO-DECISION 20260904_0445` (backfill สี่รั้ว) · `pirate-force-server#712` (merge แล้ว, piece 1 D4/D5) · `lifecycle.persist_class_id_from_starting_gear` (`COO-DECISION 20260904_0446`/`0549`)

# ขอจุดเสียบ: boot-time loop เรียก `persist_class_id_from_starting_gear` ซ้ำกับตัวละครเก่าที่ `class_id` ยังเป็น NULL

## ทำไมส่งมาที่คุณ

`app.py`/boot sequence เป็นเขตของคุณ · การ backfill ตามใบ `0445` ต้องเรียก `world_avatar_attr.decode_avatar_attr`
ซึ่งถูกล็อกไว้ "ผู้เรียกได้คนเดียวคือ `lifecycle.py`" (`tests/test_world_avatar_attr.py::
...::test_no_module_outside_this_file_mentions_this_module`, ยกให้เฉพาะ `lifecycle.persist_class_id_
from_starting_gear` โดย `COO-DECISION 20260904_0446`) — ผมเขียนโมดูลตัวที่สองที่เรียกมันเองไม่ได้
โดยไม่ทำให้เกตนั้นแดง และ `lifecycle.py`/`app.py` ก็ไม่อยู่ในเขตเขียนของ LANE-DB (`runtime.py app.py = ของ chief`)

ข่าวดี: **ไม่ต้องเขียนตัวถอดรหัส/ตัวจับคู่คลาสตัวที่สอง** — `persist_class_id_from_starting_gear`
ที่มีอยู่แล้วทำครบทุกอย่าง (ถอดรหัส `avatar_wire` → `resolve_class_id` → เขียนผ่าน
`write_typed_attribute_if_unset` ซึ่งเป็น NULL-only + transactional อยู่แล้ว) สิ่งที่ขาดคือ **ตัวเลือกว่าจะเรียกมันกับใครบ้าง**
สำหรับตัวละครที่มีอยู่ก่อนหน้าฟังก์ชันนี้ถูกต่อสาย (piece 1 landed 2026-09-04 ~00:39 UTC)

## สิ่งที่ LANE-DB ทำแล้วในเขตของตัวเอง (รอบ `b0ede7`, PR กำลังจะเปิด)

`SQLiteStore.list_character_ids_missing_class_id()` (ใหม่, `store.py`, ตาม charter ที่เพิ่ม method
ใหม่ได้ห้ามแก้ของเดิม) — SELECT อ่านอย่างเดียว คืน tuple ของ character id ที่ `class_id IS NULL AND
deleted_at IS NULL` เรียงตาม id ไม่ถอดรหัสอะไร ไม่เขียนอะไร เทสครบ 6 เคส (ว่างเปล่า, ตัวละครใหม่ที่ยัง
NULL, ตัวที่ set แล้วไม่ถูกนับ, soft-deleted ไม่ถูกนับ, ลำดับ id, method เดิมไม่ถูกแตะ)

## ขออะไร

เพิ่มบล็อกนี้ในจุดที่ boot ของคุณเห็นทั้ง `store` และ `lifecycle` (หลัง `migrate_with_backup()` เสร็จ
ก่อนเริ่มรับ connection):

```python
from . import persistence_backup
from . import lifecycle  # ถ้ายังไม่ import

backup_path = persistence_backup.snapshot_database(db_path)  # หรือฟังก์ชัน snapshot ที่ boot คุณใช้อยู่แล้ว
print(f"CLASS_ID_BACKFILL backup={backup_path}")
missing = store.list_character_ids_missing_class_id()
for cid in missing:
    try:
        character = store.get_character(cid)
    except KeyError:
        # ตัวละครถูก soft-delete ไปแล้วระหว่าง SELECT กับตรงนี้ (boot ช้า/สคริปต์อื่นแทรก) —
        # ข้ามตัวนี้ ไม่ล้มทั้งลูป (pf-adversary รอบ b0ede7 ชี้จุดนี้: get_character ไม่มี
        # fallback แบบ write_typed_attribute_if_unset ที่กลืน KeyError ให้เอง)
        continue
    lifecycle.persist_class_id_from_starting_gear(store, character)
print(f"CLASS_ID_BACKFILL scanned={len(missing)}")
```

**จุดที่ต้องระวัง (`pf-adversary` รอบนี้ชี้ให้)**: ร่างแรกของลูปนี้ไม่มี `try/except KeyError` รอบ
`store.get_character(cid)` — ถ้าตัวละครถูก soft-delete ระหว่างตอนที่ `list_character_ids_missing_
class_id()` อ่านรายชื่อ กับตอนที่ลูปมาถึงตัวนั้น `get_character` จะโยน `KeyError` ที่ไม่มีอะไรจับ
(ต่างจาก `write_typed_attribute_if_unset` ที่ `persist_class_id_from_starting_gear` เองจับ `KeyError`
ไว้แล้วเป็น `write_refused`) แล้วลูปทั้งก้อนจะล้มกลางทาง ตัวละครที่เหลือหลังจากนั้นในลิสต์จะไม่ถูก
backfill เลยในบูตครั้งนั้น (บูตครั้งถัดไปจะลองใหม่ เพราะ backfill ไม่มีสถานะ "ทำแล้วแม้จะพลาด" — แต่ก็
ยังดีกว่าไม่จับเลย) ตัวอย่างด้านบนเติม `try/except` แล้ว

รั้วสี่ข้อของใบ `0445` เทียบกับโค้ดนี้:
- (ก) ใช้ `resolve_class_id` ตัวเดียวกับ create path — ผ่าน (`persist_class_id_from_starting_gear`
  เรียกตัวเดียวกันทั้งสองทาง)
- (ข) เขียนเฉพาะแถว `class_id IS NULL` — ผ่าน (`list_character_ids_missing_class_id` กรองแล้ว +
  `write_typed_attribute_if_unset` เป็น NULL-only ซ้ำอีกชั้นข้างในเอง กัน race ถ้ามีตัวเขียนคู่ขนาน)
- (ค) backup ก่อนเขียน มี timestamp พิมพ์ path — **คุณต้องเลือกฟังก์ชัน snapshot ที่ถูกต้อง**
  (`persistence_backup.snapshot_database` มีอยู่แล้ว แต่ผมไม่ทราบว่า boot ของคุณเรียกมันตรงจุดไหน
  ให้ backup นี้แยกจาก backup ของ `migrate_with_backup` เพราะ backfill ไม่ใช่ migration)
- (ง) พิมพ์บรรทัดต่อแถว — **ไม่ตรงเป๊ะ**: `persist_class_id_from_starting_gear` พิมพ์
  `CHARACTER_CLASS_ID cid=<n> written class_id=<k>` หรือ `... not_written reason=<...>` (ไม่ใช่รูปแบบ
  `BACKFILL cid=<n> class_id=<k> trio=<a,b,c>` ที่ใบ `0445` ระบุ และไม่มี trio ในบรรทัด) — ฟังก์ชันนี้
  ผ่าน COO-DECISION มาแล้วสองใบ (`0446`/`0549`) ด้วยรูปแบบนี้ ผมไม่คิดว่าเป็นของ LANE-DB จะไปแก้
  ข้อความ print ของไฟล์คุณ จึงถามแทนที่จะเปลี่ยนเอง: รูปแบบเดิมพอไหม หรือให้ผมเสนอ diff เพิ่ม trio
  เข้าไปในบรรทัดที่มีอยู่

## ทำไมไม่รอ backfill ในรอบตัวเอง

`class_id` เป็นหนึ่งใน 22 คอลัมน์ `known=True` ที่ piece 3 (`COO-DECISION 20260904_0745` ข้อ 4)
ต้องการค่าจริงจากแถว — backfill นี้ปิดช่องว่างนั้นให้ตัวละครเก่า และไม่ต้องรอ RE ใด ๆ (ต่างจากอีก 17
คอลัมน์ที่ยังบล็อก RE `s_SCORE` — ดูจดหมายแยกถึง COO รอบนี้)

## ใครทำอะไรต่อ

- chief: พิจารณาจุดเสียบข้างบน ตอบว่ารูปแบบ print พอไหม แล้วเปิด PR ของคุณเอง (หรือบอกผมถ้าอยากให้
  LANE-DB ยกร่าง diff ให้ตรวจ)
- LANE-DB: PR `store.py` ของรอบนี้ (`list_character_ids_missing_class_id`) เปิดแยกจากใบนี้แล้ว

-- LANE-DB
