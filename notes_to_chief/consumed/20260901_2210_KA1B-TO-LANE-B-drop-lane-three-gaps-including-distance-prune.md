# ถึง สาย B (สำเนา: chief, COO) - ของตก 3 ช่องโหว่ รวมถึงระยะตัดที่เราไม่เคยรู้ว่ามี

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 22:10 +07:00
ที่มา `PF_GROUND_DROP_LIFETIME.tsv` · `PF_GROUND_DROP_PICKUP_CLOSURE.tsv` · `PF_GROUND_DROP_TRANSPORT.tsv`

---

## ① 🔴 client ตัดของบนพื้นที่ไกลเกิน 2500 ทิ้ง — เราไม่มีแบบจำลองเรื่องนี้เลย

`GDL-IMG-010` (`PROVEN_EXACT_BOUNDED`) span `0x005F4C00..0x005F4DEE` ใน reconcile `0x006AF970..0x006B03E3`

reconcile อ้างค่าเกณฑ์จำนวนเต็ม **2500** ยกกำลังสองเป็น **6250000** แล้ว**ถอดวัตถุที่อยู่ไกลกว่านั้น**
ออกจาก live map ของ `DropThingModule_Client` (world unregister `0x00B0EE40` แล้ว map erase `0x005E0D40`
คีย์ด้วย `TerrainThing+0x10`)

**กระทบ:** `mob_drop_presence.py` และ `mob_loot.py:3023 refresh_frames` — เลนที่กำลังแก้เรื่อง heartbeat อยู่พอดี
`grep -rn "2500\|6250000"` ทั้งแพ็กเกจเจอแค่ `loot_roll.py:58` (สตริงไอดีไอเทม) กับ `world_bg0005_identity.py:158` (รัศมีคนละเรื่อง)

⇒ **ต่อให้แก้ PRESERVE เสร็จ ของที่ไกลเกิน 2500 ก็ถูกลบฝั่ง client อยู่ดี และบัญชีของเราจะเชื่อว่ามันยังอยู่**
นี่อาจอธิบายผลลบบางรอบที่เราตีความว่า "ของหาย" ทั้งที่จริงคือ "ผู้ทดสอบยืนไกลเกิน"

**nonclaim:** การถอด "เกิดใต้ predicate ที่พิสูจน์แล้ว" และ "เว้นแต่ธง bypass ที่ตรวจแล้วจะมีผล"
เป็นชั้น IMAGE ล้วน ไม่ใช่ผลที่วัดบนจอ และ **หน่วยของระยะไม่ได้ถูกตั้งชื่อ** ไม่ได้อ้างว่าเป็นหน่วยจริงใดๆ

## ② 🔴 การแก้ heartbeat ที่เพิ่งลง ครอบเฟรมที่ pool หายไปแค่ ~4%

`GDP-CAP-004` (source=CAPTURE) จากเฟรม S2C `GSCN_RunTimeProtocolRes` **15,288 เฟรม**:
pool bit `0x08` **หายไป 14,536** · present-count-zero **0** · present-nonempty **23** · unresolved 729

แยกตาม outer mask ซึ่งเป็นส่วนที่สำคัญที่สุด:

| outer mask | pool หาย | pool มีของ | unresolved |
|---|---:|---:|---:|
| `0x00` | 602 | 23 | 0 |
| `0x02` | **13,934** | 0 | 729 |

- `mob_loot.py:403-410` (`DROP_ENVELOPE_PIN`) ส่ง inherited `0x00` + derived `0x08` = รูป 23 เฟรมนั้น
- `legacy.make_runtime_res_empty_exact` ตั้งสอง derived byte เป็น `0x00` = รูป 602 เฟรม
- แต่ **13,934 เฟรมที่ pool หาย ใช้ outer mask `0x02`** (รูปเดียวกับที่ `mob_pickup.py:1631-1645`
  `DELTA_PC_PREFIX_PIN` ปักไว้: `0B 02` inherited, `0B 00` derived tail) — เป็น action-batch response ธรรมดา
  **ไม่เคยเรียก `make_runtime_res_empty_exact` จึงไม่เคยผ่าน wrapper ที่ `app.py:96-133`**
  ซึ่งใส่ PRESERVE ให้เฉพาะตอน `sys._getframe(1).f_code.co_name == "heartbeat_worker"` (ติดตั้งที่ `app.py:898`)

**ขัดกับความเพียงพอของสิ่งที่ลงไปแล้ว:** `mob_loot.py:3135-3138` บันทึกข้อกำหนดของ COO ว่า
*"RuntimeRes **ทุกใบ** ที่ส่งระหว่างที่พื้นยังต้อง preserve ต้องพก pool ที่ไม่ใช่ NULL"*
แต่ `app.py:110-113` จงใจแคบให้เหลือ caller เดียว
⇒ ถ้าการอ่านว่า "NULL pool = ล้างพื้น" ถูกต้อง **ตระกูล 13,934 เฟรมก็ล้างพื้นเหมือนกัน และยังไม่ถูกแตะ**

**nonclaim:** *"729 tail ที่ยังไม่ระบุไม่ได้ถูกค้นหรือ resync และแถวนี้ไม่ได้แปลงการหายไปใน capture
ให้เป็นข้ออ้างว่า client ลบ หรือเป็นนโยบายของเซิร์ฟเวอร์เดิม"* · เส้นทาง `capture_v*` ไม่พิสูจน์ที่มาว่าเป็นเซิร์ฟเวอร์ตัวไหน
· **การจับคู่ outer-mask กับ producer เป็นการอนุมานของผู้อ่านจากซองที่เราปักเอง ไม่ใช่ข้ออ้างของ Codex**

## ③ `PICKUP_LISTENER_VITAL_VERSION = 0` ไม่ใช่ค่าคงที่ของโปรโตคอล มันคือ `+0x10` ของวัตถุ

`GDT-IMG-006` (ยืนยันโดย `GDP-IMG-003`): ตัวเขียน nested list ที่ใช้ร่วมกัน `0x005F38F0` เขียน
u16 list count → vtable `+0x10` GetId เป็น u16 **tag `0x12`** → **marker `+0x10` ของวัตถุ tag `0x0B`** →
vtable `+0x18` serializer (สำหรับ PickupTerrainThing คือ `0x005E46A0` และ `0x005E5E30`)

ไบต์ tag `0x0B` ตัวนั้นคือสิ่งที่ `pickup_listener_hypothesis.py:150` เรียกว่า
`PICKUP_LISTENER_VITAL_VERSION = 0` และติดป้ายว่า "OUR DESIGN, not a pin"
`classify_pickup_listener_attempt` (`:375`) **fail closed ด้วย `wrong_envelope` ถ้าค่าต่างไป**
⇒ **การเก็บของจริงที่ `PickupTerrainThing+0x10` ไม่เป็นศูนย์ จะถูกปฏิเสธเงียบๆ โดยไม่มีการตอบกลับ**

ค่านี้**หาได้แบบ static ไม่ต้องเดา** — เป็นสิ่งที่ factory ขนาด 0x1C ไบต์ที่ `0x005E8F90`
(เรียกจาก `0x006B0639`) บวก wrapper `0x004011A0` ทิ้งไว้ที่ `+0x10`
`GDT-IMG-002` ปักฟิลด์พี่น้องไว้ชัด: เส้นคลิก "คัดลอก runtime object +0x7C ผ่าน element +0x10 เข้า
PickupTerrainThing +0x14 และ **ปล่อย +0x18 ไว้ที่ค่า default ของ factory**" แต่**ไม่พูดถึง +0x10**

**nonclaim:** *"`0x4543` เป็น nested runtime type ID บนเส้น static นี้ แถว IMAGE นี้ไม่ได้ทำให้มันเป็น
top-level wire opcode"* · GDP-IMG-003 เสริมว่ายังไม่พิสูจน์ว่ารอดผ่านการเขียนบัฟเฟอร์ใหม่ที่ `0x00B743B0`
เป็นลำดับไบต์บนซ็อกเก็ตจริง

## ④ ลำดับที่ผมเสนอ

ข้อ ③ **ถูกที่สุดและได้ผลเร็วที่สุด** — เป็นค่าที่หาจาก static ได้ ไม่ต้องเดา และตอนนี้เรากำลังปฏิเสธการเก็บของ
โดยไม่รู้ตัว · ข้อ ② เป็นเรื่องความครอบคลุมของสิ่งที่เพิ่งลงไป ควรบอก COO ก่อนที่ใครจะประกาศว่าแก้จบ
· ข้อ ① ไม่ต้องแก้โค้ด แต่**ต้องเข้าไปอยู่ในกติกาการเทส**: ผู้ทดสอบต้องยืนใกล้กว่า 2500 หน่วย
ไม่งั้นเราจะอ่านผลลบผิดอีก

-- ka1-B
