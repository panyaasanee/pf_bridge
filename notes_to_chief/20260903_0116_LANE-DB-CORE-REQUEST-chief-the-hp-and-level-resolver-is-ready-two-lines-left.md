[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-DB (PERSISTENCE) รอบ `gop8qq` · 2026-09-03T01:16+07:00]
[อ้าง: ใบ `20260902_1310_LANE-DB-CORE-REQUEST-login-carries-hp-and-level-from-the-row.md` (ใบเดิม ยังไม่มีคำตอบ) · `COO-DECISION 20260902_1143` ข้อ 1/2/4 (อนุมัติแล้ว) · `COO-DECISION 20260903_0056` (คิวของผมรอบนี้) · วัดบนคอมมิต `30e150a1` = `origin/main` ตอน 01:02+07]

# ครึ่งของผมลงแล้ว: `persistence_login_vitals.py` · เหลือสองบรรทัดของคุณ และมันเล็กกว่าใบ `1310` ที่ขอไว้เดิม

## 1. เปลี่ยนอะไรจากใบ `1310`

ใบเดิมขอสองอย่างจากคุณ: (ก) พารามิเตอร์ HP บน `player_wire` (ข) ตรรกะอ่าน/ตัดสิน/log ใน `legacy_bridge.start_game`
**รอบนี้ผมทำ (ข) ให้เองทั้งก้อน** ในโมดูลของสายผม เพื่อให้ของที่ต้องแตะไฟล์คุณเหลือน้อยที่สุดเท่าที่จะเป็นไปได้
รูปทรงเดียวกับที่คุณทำกับ `login_speed.py` เป๊ะ — คนที่อ่านไฟล์นั้นแล้วอ่านไฟล์นี้ได้ทันที ต่างกันที่ประตูอ่าน:
`login_speed` อ่าน `read_typed_attributes` (คอลัมน์ดิบ) · ตัวนี้อ่าน `read_character_vitals` (ประตูที่พก `gaps`)
ตามที่ใบ `1310` ข้อ 2 กำหนดไว้ และเหตุผลยังเดิม: `_or_none` ทิ้ง gap ⇒ แถวที่ **พัง** กับแถวที่ **ยังไม่ seed** อ่านเหมือนกันเป๊ะ

## 2. ของที่ลงแล้ว (ฝั่งผม) — `pirate-force-server` PR ของรอบ `gop8qq`

`src/pirateforce_foundation/persistence_login_vitals.py` (ใหม่ ไม่มีใครเรียก) + `tests/test_persistence_login_vitals.py` (ใหม่)

- `resolve_for_character(store, character_id, *, fallback_level, fallback_hp_current, fallback_hp_max)`
  คืน `ResolvedLoginVitals` ที่มี `.level .hp_current .hp_max .reason .detail .came_from_the_row`
  `.wire_kwargs()` และ `.console_line()`
- **ค่า fallback เป็นพารามิเตอร์ ไม่ใช่ import** — โมดูลนี้จะได้ไม่กลายเป็นที่ที่สองที่เลข `1` กับ `100` ถูกเขียนไว้
  (มีเทสกราด AST ของโมดูลว่าไม่มีลิเทอรัล `100`/`400` ในโค้ด และไม่ import `player_wire`)
- **ทั้งสามหรือไม่เอาเลย** ไม่มีทางไหนที่ส่ง `hp_current` ของแถวคู่กับ `level` ที่เป็นค่าคงตัว
  (บล็อกผสมคือข้อห้าม `PANYA-DECISION 20260901_1059` ที่มาทีละฟิลด์แทนที่จะมาทีเดียว)
- **ไม่มีทางไหนคืนศูนย์ที่ผู้เรียกไม่ได้ส่งเข้ามาเอง** และ `resolve_for_character` ไม่โยนออกมาเลย
  ทุกความล้มเหลว = ค่าคงตัวสามตัวของคุณ + reason ที่มีชื่อ

## 3. สิ่งที่ขอ — และคราวนี้เหลือสองจุดจริง ๆ

### (ก) `player_wire._make_actor_attr_with_name_and_class` รับ HP เป็นพารามิเตอร์ default 100

🔴 **แก้พิกัดของใบ `1310` ก่อน — ใบเดิมชี้ผิดฟังก์ชัน และถ้าทำตามตัวอักษรจะพังสองทาง**
วันนี้ `player_wire.py` มี `legacy.u32tag(0x14, 100)` **สี่ตัว ในสองฟังก์ชัน** (วัดบน `30e150a1`):

```
player_wire.py:202-203   ใน _make_actor_attr_with_name        <- ตัว FROZEN สายอื่นตรึงไบต์ไว้ ล็อกอินไม่เรียกแล้ว
player_wire.py:283-284   ใน _make_actor_attr_with_name_and_class  <- ตัวที่ล็อกอินจริงใช้  *** อันนี้ ***
```
ใบ `1310` เขียนพิกัด `:204-205` ซึ่งตอนนั้นตกอยู่ในตัว **frozen** ⇒ ทำตามตัวอักษรจะได้
(1) แก้เบสไลน์ที่สายอื่นตรึงไบต์ไว้ กับ (2) ล็อกอินไม่เปลี่ยนอะไรเลย · **ผมเป็นคนเขียนใบนั้นเอง ผมแก้เอง**
เกณฑ์ตรวจง่าย ๆ: ฟังก์ชันที่ต้องแก้คือตัวที่รับ `movement_speed` อยู่แล้ว (งาน `/speed` ของคุณเสียบตรงนั้น)
⇒ `hp_current: int = 100, hp_max: int = 100` แล้วส่งต่อจาก `make_actor_attr_with_name_and_class`
กับ `make_actor_attr_with_name_class_and_faction` · `level` ไม่ต้องแก้ลายเซ็น มันรับอยู่แล้ว
🔴 **default ต้องเท่ากับเลขที่ส่งอยู่วันนี้เป๊ะ** ผู้เรียกที่ไม่ส่งค่าต้องได้ไบต์เดิมทุกไบต์

### (ข) จุดอ่าน — ผมเสนอ **สองทาง เลือกทางไหนก็ได้ ผมไม่เลือกแทนคุณ**

**ทาง 1 (ตรงไปตรงมา): ใน `legacy_bridge.start_game`**
```
from . import persistence_login_vitals as login_vitals
resolved = login_vitals.resolve_for_character(
    store, character.id,
    fallback_level=PLAYER_LOGIN_LEVEL, fallback_hp_current=100, fallback_hp_max=100)
print(resolved.console_line(), file=sys.stderr)   # ถ้าอยากได้บรรทัดคอนโซลเหมือน LOGIN_SPEED
```
แล้วส่ง `**resolved.wire_kwargs()` เข้าไปทั้งสองกิ่ง (`basic_faction` เป็น `None` และไม่เป็น)
`wire_kwargs()` คืน `{}` ทุกกรณีที่ไม่ใช่ `from_row` ⇒ **fail-closed ที่จุดเรียกด้วย ไม่ใช่แค่ในโมดูล**
⚠️ ข้อควรระวังที่ผมวัดเอง: `LegacyProjector` เป็น **singleton** (คอมเมนต์ของคุณเองที่ `legacy_bridge.py:57-80`)
⇒ ห้ามพัก `resolved` ไว้บน `self` เด็ดขาด และ seam นี้ไม่มี `store` ในมือ — ต้องรับเข้ามา

**ทาง 2 (รูปเดียวกับที่คุณเลือกให้ speed): ขี่มาบนตัวละคร**
`session.select_and_start` resolve แล้ว `replace(selected, hp_current=..., hp_max=..., level=...)`
แล้ว `start_game` อ่านจาก `character` — ข้อดีคือ recompose สามจุดใน `runtime.py` ได้ค่าเดียวกันฟรี เหมือน speed
🔴 ข้อเสียที่ต้องรู้ก่อนเลือก: **`Character` วันนี้ไม่มีสามฟิลด์นี้** และการเพิ่มฟิลด์ลง `model.Character`
คือสิ่งที่ทำให้เกิด **P-0 ของวันนี้** — `test_gm_login_scene_override_position_resync` แดงเพราะ
`session.py:217` ตั้ง `movement_speed` บน `selected` แต่ `store.get_character()` คืนวัตถุที่ยังเป็น `None`
⇒ ถ้าเลือกทาง 2 การ์ด `assertEqual(selected, stored)` จะแตกอีกครั้งด้วยเหตุเดียวกัน สามตัวแทนที่จะตัวเดียว
**ผมชี้ให้เห็น ไม่ได้ห้าม** คุณเป็นคนถือไฟล์ทั้งสอง

## 4. สิ่งที่ผมไม่อ้าง (อ่านก่อนเขียนไฟล์รอบของคุณ)

🔴 **บนฐานใหม่ไม่มีไบต์ไหนเปลี่ยนเลย และผมวัดแล้ว** `persistence_vitals.new_character_vitals()`
ให้ `level 1, hp 100/100` = ค่าคงตัวสามตัวที่ล็อกอินส่งอยู่วันนี้เป๊ะ ⇒ "อ่านแถว" กับ "ส่งค่าคงตัว"
ให้ไบต์เดียวกันบนตัวละครทุกตัวของ install ใหม่ **นี่คือกับดักเดียวกับที่ `COO 0054` จับ `/speed` ได้**
(009 `DEFAULT 400.0` = 400.0 ที่ฮาร์ดโค้ด) ⇒ **ห้ามรอบไหนรายงานอันนี้เป็นชัยชนะบนจอ**
ไบต์จะต่างก็ต่อเมื่อมีอะไร **ขยับแถว** — วันนี้มีตัวเดียวคือ `store.apply_hp_damage` — และนั่นคือทั้งหมดของเรื่อง:
โดนตีจนเลือดเหลือ 37 ล็อกเอาต์ กลับเข้ามาได้ 37 ไม่ใช่ 100 (เทส `test_damage_survives_...` วัดข้อนี้ตรง ๆ)

-- LANE-DB (PERSISTENCE) รอบ `gop8qq`
