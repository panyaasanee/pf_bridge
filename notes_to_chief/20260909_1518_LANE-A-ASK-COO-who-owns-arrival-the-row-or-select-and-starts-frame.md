# ASK-COO — ใครเป็นเจ้าของ "การมาถึง" บนล็อกอินไร้แฟล็ก: แถวถาวร หรือเฟรมที่ select_and_start ประกอบไปแล้ว

ADDRESSEE: COO
cc: chief · Panya
FROM: LANE-A รอบ `ynfhoc` · 2026-09-09T15:18+07:00
อ้าง: `rounds/A_20260909_1326_949y62_ADDENDUM_adversary_not_clean.md` ข้อ A1 (D4) และ D (คำถามเดียวที่ pf-adversary บอกว่าดีไซน์นี้ยังไม่ตอบ)

## ติดอะไร (ยืนยันเองรอบนี้ ไม่ก๊อปเลขบรรทัดจากใบรอบที่แล้ว)

`grep -n "resolve_entry(" src/pirateforce_foundation/runtime.py` และอ่านโค้ดจริงยืนยันว่า:

```
runtime.py ~10483  self.foundation.select_and_start(selector)   <-- ประกอบเฟรมจริงจาก character.position ตรง ๆ
runtime.py ~10846  world_scene_entry.resolve_entry(...)          <-- probe ของ GM override (emit=lambda _line: None)
runtime.py ~10929  world_scene_entry.resolve_entry(...)          <-- เรียกจริง
```

`select_and_start` → `session.py` → `legacy_bridge.LegacyProjector.start_game`/`movement_attr` เรียก `f32tag`/`struct.pack("<f", ...)`
บน `character.position` **โดยตรง ไม่ผ่าน `resolve_entry` เลย** และรันเป็นบรรทัดแรกของ handler ก่อน `resolve_entry`
ทั้งสองครั้งจะได้รันด้วยซ้ำ — คอมเมนต์ของ runtime.py เองที่บล็อก resync (~11021) ยืนยันเรื่องนี้ด้วยคำพูดตรง ๆ ว่า
"pc/frame were already composed above by select_and_start() ... FROM THE CHARACTER'S REAL STORED ROW -- entirely
before this override was even computed"

**ผลคือ**: `resolve_entry` (ที่อยู่ในเขตของสายผม) เป็นผู้ตอบว่า "แถวนี้ควรลงที่ไหน" แต่เฟรมที่ไคลเอนต์ได้รับจริงบนบูตไร้แฟล็ก
(ActorAttr/MovementAttr) ถูกประกอบจาก `character.position` **ดิบ ๆ** ไปแล้วก่อนที่ `resolve_entry` จะได้ตอบคำถามนั้นด้วยซ้ำ
และจะถูกประกอบใหม่จาก `entry.position` (คำตอบของ `resolve_entry`) **เฉพาะกรณีมี GM login-scene override เท่านั้น**
(`if login_scene_override is not None:` ที่ runtime.py ~11021) — ล็อกอินปกติไม่มี resync นี้เลย

⇒ บนล็อกอินไร้แฟล็กธรรมดา: `pc`/`frame` (ActorAttr/MovementAttr) กับ `entry.teleport_fields` **ถือคนละจุดกันได้จริง**
ทุกครั้งที่ `resolve_entry` ตัดสินใจ **ย้ายที่** จากแถวดิบ (relocate ไปที่ pinned spawn เพราะ ground evidence ไม่ยืนยัน,
หรือ relocate เพราะแถวไม่ใช่ตัวเลขที่เข้ารหัส float32 ได้) — วัดได้ว่าเกิดขึ้นจริงที่ฉาก **17 และ 278**
(สองฉากเดียวที่มี ground box วัดแล้วในทะเบียน ณ commit นี้ — `grep -n '"ground": {' scenarios/world_scene_registry_001.json`
คืนสองแถว) เพราะสองฉากนี้มีทั้งแถวจริงที่อาจอยู่นอกกรอบ **และ** กลไก relocate ที่ resolve_entry เดียวเท่านั้นที่รู้จัก

รั้ว `_wire_refusal` (D5/D6 ของรอบ `sbqohw`) ที่ผมเพิ่งแก้คอมเมนต์ให้ตรงความจริงในรอบนี้ ก็เป็นเหยื่อของช่องว่างเดียวกัน:
มันอยู่ใน `resolve_entry` เท่านั้น จึงมาไม่ทันตัวเข้ารหัสตัวแรก (`select_and_start`) ที่รันไปก่อนแล้วบนล็อกอินปกติ —
รายละเอียดอยู่ใน CORE-REQUEST คนละใบ (ใบเดียวกับที่แนบมาพร้อมกัน) แต่รากของทั้งสองปัญหาคือคำถามเดียวกัน

## คำถามที่ต้องมีคนตอบ

**การมาถึงของตัวละครบนล็อกอินไร้แฟล็ก ถูกกำหนดโดยฝั่งไหนของ `select_and_start`?**
- ฝั่ง "แถว" (`character.position` ดิบ ๆ ที่ `select_and_start` ประกอบเฟรมจากมันไปแล้ว)
- หรือฝั่ง "คำตอบของ `resolve_entry`" (`entry.position` ที่ `world_scene_entry` เป็นเจ้าของตรรกะทั้งหมด)

ตราบใดที่ยังไม่มีคำตอบ: รั้วทุกตัวที่สายผมเติมให้ `resolve_entry` ปกป้อง **ไม่ได้จริง** สำหรับล็อกอินไร้แฟล็กธรรมดา
(กันได้แค่ค่าที่ resolve_entry ตอบ ไม่ใช่ค่าที่ `select_and_start` ส่งออกไปแล้ว) และทุกครั้งที่มันย้ายที่ คือความเห็นที่สอง
ที่ฝั่งเฟรมจริงไม่เคยได้ยิน — ไคลเอนต์อาจเห็นตัวละครยืนอยู่ที่หนึ่ง (จาก MovementAttr) ขณะที่ teleport พาไปอีกที่

## ผมเลือกอะไรไปแล้ว (ไม่ block งาน รอคำตอบ)

ตามกติกาโปรเจกต์ "ไม่สมมติ ให้ถาม" ผมไม่เดาคำตอบและไม่แก้ `runtime.py`/`session.py` เอง (เขตของ chief)
งาน 6 ข้ออื่นของรอบนี้เดินต่อตามปกติโดยไม่รอใบนี้ — สิ่งที่ผมทำได้ในเขตของตัวเองคือแก้คอมเมนต์ที่เคย
อ้างว่ารั้วนี้ปกป้องล็อกอินปกติได้ ให้พูดความจริงแทน (ดู `src/pirateforce_foundation/world_scene_entry.py`
คอมเมนต์เหนือ `RELOCATED_ROW_OUTSIDE_FLOAT32`) และส่ง CORE-REQUEST แยกอีกหนึ่งใบขอให้ chief ย้ายรั้วขึ้นต้นน้ำ
(รายละเอียดเชิงกลไกอยู่ในใบนั้น)

## ถ้าคำตอบคือ "แถวเป็นเจ้าของ"

`select_and_start`/`start_game` ต้องเรียก `resolve_entry` (หรือรั้วของมัน) **ก่อน** ประกอบเฟรมแรก ไม่ใช่หลัง — งานนี้อยู่ในไฟล์ของ chief

## ถ้าคำตอบคือ "เฟรมของ select_and_start เป็นเจ้าของ"

`resolve_entry`/`_wire_refusal` กลายเป็นรั้วที่มีประโยชน์เฉพาะทาง non-login (Columbus, M2 arrival, GM override resync)
เท่านั้น และเอกสารของโมดูลต้องพูดแบบนั้นตรง ๆ แทนที่จะบอกว่ามันปกป้องล็อกอิน — ผมแก้คอมเมนต์รอบนี้ไปในทิศทางนี้แล้ว
เผื่อคำตอบออกมาทางนี้ แต่ยินดีแก้กลับถ้า COO เลือกทางแรก

-- LANE-A
