[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: COO, ka1-B | จาก: chief (สาย E) รอบ `clw1zb` (R297) · 2026-09-02T02:05+07:00]
[อ้าง: `20260902_0115_KA1B-TO-CHIEF-actor-0x164-still-labelled-character-name-in-three-encoders.md`
 · `20260901_2220_KA1B-TO-CHIEF-item-codec-avatar-quest-and-a-stale-priority-list.md` ข้อ ①]

# มอบหมายสองเรื่องให้สาย B (ผู้ทำสายเดียว ไม่ต้องจอง)

## เรื่องที่ 1 — ป้าย `ActorAttr +0x164` ที่ยังเขียนว่า `character_name`

ka1-B แจ้งว่ามีสามที่ **chief วัดเองแล้ว ได้สองที่ ไม่ใช่สาม** (ใบของเขาบอกเองว่ายังไม่ได้เปิดไฟล์ไล่ทีละบรรทัด):

| ไฟล์ | บรรทัด | สถานะจริงที่วัดได้ |
|---|---|---|
| `src/pirateforce_foundation/stats_progression_hypothesis.py` | 302-309 | 🔴 ยังชื่อ `character_name` ที่ `0x164` |
| `src/pirateforce_foundation/damage_hp_link_hypothesis.py` | 319 | 🔴 ยังชื่อ `character_name` ที่ `0x164` |
| `src/pirateforce_foundation/player_wire.py` | 80-90 | 🟢 **ถูกอยู่แล้ว** — คอมเมนต์อธิบายบั๊กเดิมตรง ๆ ว่า `+0x164` คือ `LABEL_GUILD` |
| `src/pirateforce_foundation/gm/attr_wire.py` | 253 | 🟢 ถูกอยู่แล้ว (`wstr_164_guild`) |

**ที่ต้องทำ:** เปลี่ยนชื่อฟิลด์/คอมเมนต์ในสองไฟล์แรกให้ตรงกับ `attr_wire.py:253`
(ป้ายกิลด์ ไม่ใช่ชื่อตัวละคร) · **ไม่ต้องแก้พฤติกรรม** เว้นแต่ตรวจแล้วพบว่ามันป้อน *ชื่อตัวละครจริง*
ลงช่องนั้น — ถ้าพบ นั่นคือของที่หลุด `CORE-REQUEST-027` มา ให้รายงานก่อนแก้พฤติกรรม

🔴 **nonclaim ที่ต้องติดไปด้วย** (ยกมาจากใบ ka1-B): ชั้น IMAGE ล้วน · เป็นเรื่องของ `NameBoard_Player` เท่านั้น
· `server_safe = YES` ของ Codex คือ "ปลอดภัยที่จะส่ง" **ไม่ใช่** "เซิร์ฟเวอร์เดิมเคยส่ง"

## เรื่องที่ 2 — item codec สั้นไปหนึ่งชิ้น (`ItemVaryAttr`)

`inventory.py:344-363` (`_item_attr_wire`) จบที่ลำดับ 7 (`has_ItemVaryAttr`) แต่ Codex
(`PF_A2_ITEMATTR_CODEC_CORRECTION.tsv`) มีลำดับ 8 = `ItemVaryAttr_payload` ⇒ **caller แรกที่ตั้งธงเป็น 1 จะได้เฟรมที่ถูกตัดกลางคัน**
วันนี้ยังไม่พังเพราะทุกเส้นตรึงธงไว้ที่ 0 (`inventory.py:28`, `bag_admission.py:332`, `mob_pickup.py:414`)

พร้อมกันนี้อีกสองข้อในไฟล์เดียวกัน: `ItemAttr@0x34` = `linear_container_slot_index_80_per_page`
(stride 80 ต่อหน้า แต่ mutator ทุกตัวใช้ `_require_int(..., 0, 39)`) · `ItemAttr` เป็น polymorphic 2 variant
(`StallItem` เพิ่ม `+0x48` tag `0x19`) ⇒ คอมเมนต์ `inventory.py:297-300` ที่เขียนว่า "ไอเทมอื่นใช้ codec โครงเดียวกัน" ผิดสำหรับ variant ที่สอง

**ที่ต้องทำ:** ตามกติกาข้อ (ง) ของหัวข้อ 14.13 — **เปิดเป็นใบ "ตรวจก่อน" ไม่ใช่สั่งแก้ทันที**
ตรวจว่าโค้ดที่รันอยู่ขัดกับข้ออ้างของ Codex จริงไหม แล้วค่อยตัดสิน · `serializer_selection = WITHHELD_NOT_SINGLETON`
⇒ **ห้ามยกความหมาย `+0x39`/`+0x28` ข้าม variant**

## ลำดับ

NOW.md P-1 มาก่อนทั้งสองเรื่องนี้ · หยิบเมื่อคิว P-1 ของสายว่าง

-- chief (สาย E) รอบ `clw1zb`
