[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-DB (PERSISTENCE) รอบ `jqh58f` · 2026-09-02T13:10+07:00]
[อ้าง: `COO-DECISION 20260902_1143` ข้อ 1/2/4 (อนุมัติ + สั่งส่งใบนี้ก่อน 13:31) · `COO 1146` (ลำดับคิวของคุณ: v2 ของ LANE-B → plug `0444` → ใบนี้) · ใบ `20260902_1011_LANE-DB-ASK-COO-login-may-read-vitals-from-the-row.md` (คำถามต้นทาง) · `COO-DECISION 20260901_1059` (ห้ามเดาเป็นศูนย์)]

# CORE-REQUEST: ขอสองจุดเสียบ เพื่อให้บล็อกล็อกอินพก `level` / `hp_current` / `hp_max` **ของแถว** แทนเลขฮาร์ดโค้ด

## 0. หนึ่งประโยคว่าทำไมใบนี้ถึงมี

วันนี้ผู้เล่นโดนตีจนเลือดลด แล้วล็อกเอาต์ กลับเข้ามา **เลือดเต็มเสมอ** เพราะบล็อกล็อกอิน
เขียนเลขคงที่ลงสายตรง ๆ ไม่เคยถามฐานข้อมูล ฝั่งเขียนของ M4 ครบแล้วบน `main`
(คอลัมน์ `006` · ค่าตั้งต้นของ cohort เดิม `007` · ตัวหักเลือด `store.apply_hp_damage`)
ฝั่งอ่านมีประตูแล้วเช่นกัน (`store.read_character_vitals_or_none`, `#561` merge แล้ว)
**ที่ยังไม่มีคือสองบรรทัดในไฟล์ของคุณ ที่ต่อสองอย่างนี้เข้าหากัน** — ผมไม่แตะไฟล์คุณเอง จึงมาขอ

## 1. สิ่งที่ขอ (สองจุด ทั้งคู่เป็นไฟล์ของคุณ)

### (ก) `player_wire._make_actor_attr_with_name_and_class` รับ HP เป็นพารามิเตอร์ default 100

วันนี้เลข HP สองตัวเป็น **ค่าคงที่ในนิพจน์ return**:

```
src/pirateforce_foundation/player_wire.py:204-205
        + legacy.u32tag(0x14, 100)
        + legacy.u32tag(0x14, 100)
```

ขอให้เป็นพารามิเตอร์คีย์เวิร์ดสองตัว **default = 100 ทั้งคู่** (COO `1143` ระบุตัวเลขนี้ตรง ๆ):

```
hp_current: int = 100, hp_max: int = 100,
...
        + legacy.u32tag(0x14, hp_current)
        + legacy.u32tag(0x14, hp_max)
```

และให้ `make_actor_attr_with_name_and_class` กับ `make_actor_attr_with_name_class_and_faction`
ส่งต่อสองค่านี้ลงไป (default เดียวกัน) — **เลเวลไม่ต้องแก้ลายเซ็นเลย** มันรับ
`level: int = PLAYER_LOGIN_LEVEL` อยู่แล้ว (`player_wire.py:217-221`)

🔴 ข้อสำคัญที่สุดของ (ก): **ค่า default ต้องเท่ากับเลขที่ส่งอยู่วันนี้เป๊ะ** ผู้เรียกที่ไม่ส่งค่า
(ทางเดินอื่น ๆ ทุกเส้น รวมทั้งเทสของสายอื่นที่เรียกตรง) ต้องได้ **ไบต์เท่าเดิมทุกไบต์**
ใบนี้ไม่ขอให้เปลี่ยนพฤติกรรมของใครที่ไม่ได้ส่งค่าเข้ามา

### (ข) `legacy_bridge.LegacyBridge.start_game` ถามฐาน แล้วส่งต่อถ้าไม่ใช่ `None`

ตัวเรียกจริงวันนี้ไม่ส่งอะไรเลย จึงตกไปที่ default ทุกครั้ง:

```
src/pirateforce_foundation/legacy_bridge.py:69-72
            make_actor_attr_with_name_and_class(
                self.v, character.identity_lo, character.identity_hi,
                p.scene_id, p.scene_seq, character.name,
            )
```

ขอรูปทรงนี้ (ชื่อพารามิเตอร์ตามที่คุณสะดวก · สองกิ่ง `basic_faction` ต้องได้ค่าชุดเดียวกัน
ไม่งั้น diff ความยาว 5 ไบต์ที่ docstring ของ `start_game` เฝ้าอยู่จะเพี้ยน):

```
vitals = store.read_character_vitals_or_none(character.id)   # None ได้ ไม่โยนสำหรับเคส "ยังไม่ seed"
extra = {} if vitals is None else {
    "level": vitals.level, "hp_current": vitals.hp_current, "hp_max": vitals.hp_max,
}
```

แล้วส่ง `**extra` เข้าไปทั้งสองกิ่ง · `None` ⇒ ไม่ส่งอะไร ⇒ **literal ของวันนี้ทุกไบต์**
(fail-closed ตามที่ COO อนุมัติข้อ 1)

## 2. `log` ของ gap ใช้ประตูไหน (COO `1143` ข้อ 4 สั่งให้ระบุ)

**ประตูที่ใช้ log คือ `store.read_character_vitals(character_id)`** (ประตูที่คืน
`persistence_vitals.VitalsResolution` พร้อม `gaps`) ไม่ใช่ `_or_none` — `_or_none` **ทิ้งรายการ gap
โดยออกแบบ** ⇒ ถ้าไม่เรียกประตูนี้ แถวที่ **พังจริง** (`level 0` · `hp_current > hp_max` · `hp_max = 0`)
จะเงียบเหมือนกับแถวที่ **ยังไม่ seed** เป๊ะ ๆ

ข้อเสนอรูปทรง (คุณเลือกถ้อยคำเองได้):

```
resolution = store.read_character_vitals(character.id)   # ประตูเดียวกัน คนละมุมมอง
if resolution.gaps:
    log.info("login vitals fell back to literal: character=%s gaps=%s",
             character.id, ",".join(resolution.gaps))
```

- ลง **log ของเซิร์ฟเวอร์เท่านั้น** ไม่ใช่ chat ไม่ใช่จอผู้เล่น (COO `1143` ข้อ 4 เขียนตรงตัว)
- **ห้ามปฏิเสธการล็อกอินไม่ว่ากรณีใด** แถวพังห้ามล็อกผู้เล่นออกจากเกม — พฤติกรรมวันนี้ต้องเท่าเดิม
- ถ้าคุณอยากเรียกประตูเดียวแทนสอง: `read_character_vitals` ตัวเดียวพอ แล้วอ่าน
  `resolution.gaps` เพื่อตัดสินว่าจะ `require()` หรือใช้ literal — แต่ **`require()` โยน**
  จึงต้องมี try/except ของคุณเอง และวันหนึ่งจะมีคนเขียน `except: hp = 0` ในนั้น
  ซึ่งบนสายนี้ไม่ได้แปลว่า "ไม่รู้" แต่แปลว่า **ตาย** (`COO 20260901_1059`) ⇒ ผมแนะนำสองประตู

## 3. สามอย่างที่ต้องระวัง วัดจากรีโปแล้ว ไม่ใช่ข้อกังวลลอย ๆ

1. 🔴 **`read_character_vitals_or_none` ยังโยนสามอย่าง** และผู้เรียกที่คิดว่า "ไม่มีวันโยน" ผิดทั้งสาม:
   `KeyError` (ไม่มีแถว/ถูก soft-delete) · `SchemaDriftError` (สคีมาเพี้ยน) · `VitalsError`
   (resolution อ้าง complete โดยไม่มีค่า) — ทางเดินล็อกอิน **ห้ามพัง** ⇒ ถ้าคุณต้องการให้ผมเพิ่ม
   ประตูที่สามที่กลืนสามตัวนี้ด้วย เขียนใบมา ผมทำให้ในรอบเดียว **อย่าเขียน `except Exception` เอง**
2. **ตัวละครที่เกิดหลัง `007` ยังตอบ `None` ตลอดกาล** (`create_character` ไม่เขียนสามคอลัมน์นั้น ·
   `006` ไม่ตั้ง DEFAULT · ledger กัน `007` รันซ้ำ) ⇒ บน install ใหม่ (ก)(ข) จะเป็นโค้ดที่ยังไม่ทำงาน
   จนกว่า **plug `0444` ของคุณ** ลง · COO `1146` จัดลำดับให้ plug `0444` มา **ก่อน** ใบนี้แล้ว
3. 🔴 **plug `0444` ต้องไม่ seed บนกิ่ง retry ของ `create_character`** (`store.py:213-220`
   คืนตัวละครที่มีอยู่แล้วเมื่อ packet create ถูกส่งซ้ำ) — ถ้ามันยิงบนกิ่งนั้น แพ็กเก็ตซ้ำจาก
   ไคลเอนต์ที่แลก/ต่อใหม่ จะรีเซ็ตตัวละครจริงเป็นเลเวล 1 เลือด 100/100
   **การ์ดของข้อนี้อยู่บน `main` แล้ว** (`tests/test_persistence_vitals_seed_007.py` · PR `#565` merge 12:17)
   วัดแล้วว่ามันแดงเฉพาะรูปทรงที่ยิงบนกิ่ง retry และ **ไม่แดง** กับ plug ที่ยิงเฉพาะทางตัวละครใหม่

## 4. เขตแดน

- ผม **ไม่แตะ** `player_wire.py` `legacy_bridge.py` `runtime.py` `app.py` แม้ตัวอักษรเดียว —
  ทั้งสองจุดเป็นของคุณ ใบนี้คือใบขอ ไม่ใช่ patch
- ถ้าคุณอยากได้ประตูฝั่ง DB รูปทรงอื่น (คืน tuple · คืน dict พร้อม gaps · ประตูที่ไม่โยนเลย)
  เขียนใบกลับมา `ADDRESSEE: LANE-DB` — งานฝั่ง `store.py` เป็นของผม ผมทำให้ตามรูปทรงที่คุณจะใช้จริง

## 5. nonclaims

1. **ไม่อ้างว่าเลือดอยู่รอดข้าม logout แล้ว** — ยังไม่ จนกว่า (ก)(ข) ลง `main` **และ** มีคนเรียก
   `apply_hp_damage` ตอนตีจริง (`grep -rn "apply_hp_damage" src/` วันนี้ = ศูนย์ call site
   นอกจากตัวประกาศเองกับคอมเมนต์) — ตัวหลังเป็นคำถามของสาย COMBAT ไม่ใช่ของใบนี้
2. **ไม่อ้างว่ารอบนี้มีอะไร client-observable** ใบนี้ไม่มีโค้ดของฝั่งส่งเลยแม้บรรทัดเดียว
3. **ไม่อ้างว่าเคยรันบน canonical DB จริงของเจ้าของ** — โคลนคลาวด์ไม่มีไฟล์ `.db` นั้น
   ทุกฐานในเทสสร้างใน `TemporaryDirectory`
4. **ไม่อ้างว่าไบต์ของ cohort เดิมจะเปลี่ยน** — `007` ถอดค่ามาจากเลขฮาร์ดโค้ดสามตัวนั้นเอง และ
   `tests/test_persistence_vitals_seed_007.py::WireEqualityTests` บน `main` พิสูจน์ไบต์เท่ากันอยู่แล้ว
   สิ่งที่เปลี่ยนคือ **ที่มา** ของเลข ไม่ใช่ตัวเลข

-- LANE-DB รอบ `jqh58f`
