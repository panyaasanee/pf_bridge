[ถึง: chief cloud (cc) และ COO และ Panya | จาก: สาย B (COMBAT) · รอบ `B_20260827_1120` · 2026-08-27T11:20+07:00]
[อ้างอิง: `notes_to_chief/20260827_0520_ATTENDED-URGENT-*` (การวินิจฉัยดั้งเดิม), `20260827_0920_CHIEF-URGENT-*`
/ `CORE-REQUEST-008` (ปัญหาข้างเคียงคนละจุด, ยังค้างแยกต่างหาก)]

# LANE-B -- `CORE-REQUEST-009` [เสนอ เลขถัดจาก 008 · รอ chief เขียนแถวทะเบียนจริง] -- ครึ่งผู้เล่นของคู่ hostile pairing ทั่วไป (ไม่ใช่แค่ตัวปักหมุดเดียว) พร้อมโค้ดวางได้เลย

## สรุปสั้น

`GT-084` (บูตไร้แฟล็ก) เห็นมอนสเตอร์เป็น NPC สีเขียวธรรมดา ไม่แดง แม้ census จะประกอบ hostile body
13/13 จริงแล้ว (พิสูจน์แล้วโดย R187) จดหมาย `0520` วินิจฉัยไว้แล้วว่าสาเหตุคือ: ผู้เล่นเองไม่เคยออก
ด้วย `basic_faction=1` บนบูตไร้แฟล็ก เพราะโค้ดที่ทำสิ่งนั้น (`_npc_hostile_start_game_response`,
`runtime.py:3018-3075`) ถูกเรียกเฉพาะเมื่อ `npc_hostile_hypothesis_scenario is not None`
(`runtime.py:4472`) เท่านั้น และฟังก์ชันนั้นเองยังปักหมุดตัวตนเดียว (`NPC_HOSTILE_PLAYER_IDENTITY_LO/
HI`) ไว้ด้วย ⇒ ไม่มีทางที่ตัวละครจริงตัวไหนจะได้ครึ่งนี้บนเส้นทางที่เจ้าของเล่นจริงเลย

รอบนี้สร้างครึ่งที่เป็น pure logic ให้แล้ว: `src/pirateforce_foundation/player_hostile_pairing.py`,
ฟังก์ชัน `compose_start_game_with_player_pairing(projector, selected, backpack, pc, frame)` —
เรียก encoder เดิม (`player_wire.make_actor_attr_with_basic_faction` ผ่าน `projector.start_game`)
ตัวเดียวกับที่ `_npc_hostile_start_game_response` ใช้อยู่แล้ววันนี้ ไม่มีของใหม่ ไม่มีการคลายด่านของ
serializer แม้แต่บิตเดียว แค่เอาหมุดตัวตนที่ไม่จำเป็นออก fail-closed คืนไบต์ production เดิมทุกครั้งที่
serializer ปฏิเสธหรือความยาวไม่ตรง

## ทำไมปลอดภัย (ไม่ใช่การขยายด่าน)

`player_wire.make_actor_attr_with_basic_faction` เดิมรับแค่ `scene_id in (1, 2)`, `scene_seq == 0`,
`basic_faction == 1` เท่านั้น (ไฟล์นั้นสายนี้ไม่แตะ) — `app.py`'s เอง (`default = Position(1, 0,
legacy.V135_PLAYER_X, ...)`, บรรทัด 748) คือ spawn เริ่มต้นของทุกตัวละครวันนี้ และ checkpoint การเดิน
(`runtime.py:3537`) ไม่เคยเปลี่ยน `scene_id`/`scene_seq` เลย ⇒ ตัวละครทุกตัวบนเส้นทางที่ต่อสายอยู่จริง
วันนี้ (scene 278 ปิดโดยเจตนา, `COO-DECISION-BUILD-002-scene278-stays-off`) อยู่ในช่วงที่ serializer
เดิมยอมรับอยู่แล้วเสมอ วันที่ฉากอื่นเปิด ตัวละครที่นั่นจะ fail-closed ทันที (คืนไบต์ production เดิม
+ event ชื่อ) เหมือนพฤติกรรมของ `_npc_hostile_start_game_response` วันนี้ทุกอย่าง

## โค้ดที่ขอให้ต่อ (บรรทัดเดียวจริง ๆ ตามธรรมเนียมของบ้านนี้ CORE-REQUEST-006 -- "ALWAYS ON, no scenario flag")

ที่ `runtime.py` รอบ ๆ บรรทัด 4472-4480 (จุดที่ `pc, frame` เป็นผลจาก inherited dispatch แล้ว และ
ก่อน `self.start_game_reply_sent = True`):

```python
# CORE-REQUEST-009 (LANE-B).  ALWAYS ON, no scenario flag -- same shape as
# CORE-REQUEST-006.  player_hostile_pairing reuses the exact frozen
# serializer _npc_hostile_start_game_response already calls, minus that
# function's extra single-identity pin, and fails closed to the untouched
# production bytes for any character/scene the serializer itself refuses.
pc, frame, _pairing_sent, _pairing_event = (
    player_hostile_pairing.compose_start_game_with_player_pairing(
        self.foundation.projector, self.foundation.selected,
        self.foundation.backpack, pc, frame,
    )
)
print(player_hostile_pairing.describe_pairing_attempt(
    _pairing_sent, _pairing_event,
))
if npc_hostile_hypothesis_scenario is not None:
    pc, frame = self._npc_hostile_start_game_response(pc, frame)
```

(ต้องมี `from . import player_hostile_pairing` หรือเทียบเท่าที่หัวไฟล์ ตามแบบ import อื่น ๆ ของ
`runtime.py` เอง)

**ทางเลือกที่สอง ถ้า chief เห็นเหตุผลอื่น:** ถ้าต้องการให้สาขาแฟล็กเดิมยังทำงานเป็นอิสระ (ไม่ให้
`compose_start_game_with_player_pairing` ที่ส่งไปแล้วมาชนกับ `_npc_hostile_start_game_response` ที่
เรียกซ้อนทับ) ให้ห่อสาขาแฟล็กเดิมด้วย `if not _pairing_sent:` ก่อนเรียก — ทั้งสองแบบไม่มีความเสี่ยง
เพิ่มต่อบูตไร้แฟล็ก (`npc_hostile_hypothesis_scenario` เป็น `None` เสมอบนบูตนั้น) สายนี้ไม่ยืนกราน
แบบไหน chief เลือกได้

## ทดสอบไว้แล้วก่อนขอ (ดูรายละเอียดเต็มใน `rounds/B_20260827_1120_*.md`)

9 เทสใหม่ (`tests/test_player_hostile_pairing.py`) รวม fail-closed สำหรับฉากที่ไม่รับ, `scene_seq`
ที่ไม่ใช่ 0, และ `selected=None` (พบและแก้เองระหว่าง self-review — เดิม crash ด้วย `AttributeError`
ไม่ fail-closed) สวีตเต็ม 3411 ผ่าน 0 regression

## nonclaims

- ไม่ได้อ้างว่าไคลเอนต์จะเรนเดอร์แดงจริง -- นั่นยังเป็นคำถามเปิดของ `GT-084`/`RIDER-084-A` รอบสอง
  (ตามที่จดหมาย `0520` ข้อ ④.3 เสนอไว้แล้ว ใบนี้ไม่เปิดใบใหม่ซ้ำ)
- ไม่ได้อ้างว่านี่คือ "ครึ่งที่ขาดเพียงหนึ่งเดียว" -- อ้างแค่ว่ามันขาดแน่ ๆ วันนี้ (จาก `0520`) และการ
  เติมมันเข้าไปตามที่เสนอไม่มีความเสี่ยงเพิ่มต่อเส้นทางที่ serializer เดิมไม่ยอมรับอยู่แล้ว
- ไม่แตะ `runtime.py`/`app.py`/`player_wire.py`/`legacy_bridge.py` เลยในรอบนี้ -- นอกเขตของสายนี้
  ทั้งหมด
- ไม่เกี่ยวกับ `CORE-REQUEST-008` (compose `bar_frames`/`death_frames` เข้า full census) -- นั่นยัง
  ค้างแยกต่างหาก ตรวจสดยืนยันซ้ำวันนี้ว่ายังไม่ต่อสาย (`hostile_census_frames` ใน `runtime.py` grep
  ยังเป็น 0 hit)

BUILD_IMPACT: ปิดช่องว่างสุดท้ายที่ทำให้ `BUILD-004`'s "หลายตัวชื่อแดง" ยังไม่เป็นจริงบนบูตไร้แฟล็ก
แม้ประชากรจริงจาก MOBS table จะต่อสายและพิสูจน์ census แล้วก็ตาม -- ถ้าไม่ต่อสาย ทุกครั้งที่เจ้าของ
ไปดู Port Royal จะยังเห็น NPC สีเขียวเหมือนเดิมทุกประการ ไม่ต่างจากเมื่อวาน

-- สาย B (COMBAT)

---
_Generated by [Claude Code](https://claude.ai/code)_
