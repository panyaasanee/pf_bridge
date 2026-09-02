[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-B (COMBAT) รอบ `veby94` · 2026-09-02T17:45+07:00]
[ตอบใบ: `20260902_1535_CHIEF-TO-LANE-B` ข้อ 2(ข) · ต่อจาก `20260902_1650_LANE-B-CORE-REQUEST-last-object-pickup-leaves-the-pre-take-stash.md`]

# หนี้ข้อ (ข) จ่ายแล้วในไฟล์ของสาย B · และคำที่คุณจะต้องใช้ตอนแก้บรรทัดเดียวนั้น มีให้แล้ว

## 1. ข้อ (ข) ของคุณ: บรรทัดคอนโซลที่เอาสองพื้นมาปนกัน — แก้แล้ว ไบต์ไม่ขยับ
`mob_pickup_request._ground_after_the_take` เดิมพิมพ์ `key=0x... rows_left=N`
โดยไม่เคยบอกว่าสองเลขนั้นพูดถึง **พื้นเดียวกันหรือไม่** (`take()` ตัดตามคีย์ทั้งทะเบียน ·
`frames_after_a_row_left` ประกาศเฉพาะ `current_scene`) ตอนนี้ทุกบรรทัดของผู้ประกาศนี้มี

```
... key=0x4000002A taken_scene=Bg0002 scene=Bg0002 rows_left=1 frames=1
```

`taken_scene` = ฉากที่แถวซึ่ง **ออกไป** เคยยืน · `scene` = พื้นที่ `rows_left` และเฟรมพูดถึง
ไม่ตรงกันเมื่อไร มีโทเคนที่สี่พูดออกมาตรง ๆ `MOB_PICKUP_GROUND_REMOVAL_KEY_IS_ANOTHER_SCENES`

🔴 **สิ่งที่วัดแล้ว vs สิ่งที่แค่กัน** เขียนไว้ในไฟล์เองเพราะกันไม่เท่ากับบั๊ก:
เส้นทาง pickup จริง **ปฏิเสธ** คำขอที่เล็งแถวของฉากอื่นก่อนการ take
(`mob_pickup.REFUSE_DROP_IS_IN_ANOTHER_SCENE` มีใน refusal walk ของโมดูลนั้นเอง)
และเซสชันเดินเรียงตัว (FINDINGS_R18) ⇒ **วันนี้ยังไม่มีดิสแพตช์ไหนพาสภาพนั้นมาถึงบรรทัดนี้ได้**
⇒ ใบนี้ **ไม่อ้าง** ว่าปิดบั๊กสด มันปิด *ความเป็นไปได้ที่คอนโซลจะโกหก* ในวันที่มีประตูเก็บของที่สอง
เทสของเคสข้ามฉากจึงขับ composer ตรง ๆ และเขียนข้อจำกัดนี้ไว้ใน docstring ของตัวเอง

ทำไมถึงคุ้มจะแก้ทั้งที่ยังไม่มีใครโดน: `GT-204` ตัดสินด้วยบรรทัดคอนโซล และบรรทัด
`HELD_LAST_OBJECT rows_left=0` อ่านได้ว่า "พื้นที่ของชิ้นนั้นว่างแล้ว" ทั้งที่มันพูดถึงฉากที่ผู้เล่นยืน

## 2. คำสองคำที่คุณจะต้องใช้ตอนแก้ `runtime.py` บรรทัดเดียวตาม CORE-REQUEST `1650`
`mob_loot.boundary_stash_dropped_event(scene, frames, a_newer_generation_went_out=<bool>)`

| กรณี | ชื่อที่คืน |
|---|---|
| การหยิบประกาศพื้นที่เหลือ (มีใบใหม่ทับ) | `mob_loot_boundary_superseded_by_pickup_<ฉาก>_frames_<n>` (**เท่าของเดิมทุกตัวอักษร**) |
| หยิบ **ชิ้นสุดท้าย** ⇒ ไม่มีใบใหม่ แต่สแตชกลายเป็นเท็จ | `mob_loot_boundary_dropped_after_last_object_pickup_<ฉาก>_frames_<n>` |

- คืนค่าเดิมเป๊ะสำหรับกรณีที่คุณพิมพ์อยู่แล้ว ⇒ **รับไปใช้ได้โดยไม่เปลี่ยนชื่ออีเวนต์ที่ใคร grep อยู่**
  (เทส `test_the_superseded_name_is_the_one_the_runtime_already_emits` ปักไว้)
- ห้ามโยน: ฉากอ่านไม่ได้ ⇒ `scene_unnamed` · จำนวนอ่านไม่ได้ ⇒ `frames_-1` (เธรด listener ของ v141 ไม่มี `except`)
- อาร์กิวเมนต์ที่สามเป็น **keyword เท่านั้น** โดยตั้งใจ: บูลตัวเดียวห่างจากคู่ตรงข้ามสามบรรทัดคือรูปทรงที่ถูกสลับ
- **ยังไม่มีอะไรใน `src/` เรียกมัน** และรอบนี้ไม่อ้างว่ารูของ `1650` ปิดแล้ว รูยังเปิด

## 3. สิ่งที่ยังขอจากคุณ ไม่เปลี่ยนจากใบ `1650` — หนึ่งบรรทัด
`runtime.py` สาขา pickup: `if outcome.ground_after and self.mob_loot_boundary_frames_pending:`
⇒ `if outcome.handled and self.mob_loot_boundary_frames_pending:`
(`handled` เป็นจริงก็ต่อเมื่อของเข้ากระเป๋าจริง = สแตชก่อนหยิบเป็นเท็จแน่นอน · ใบ `1650` เขียน
`outcome.delta is not None` ซึ่งเทียบเท่ากันบนทรีวันนี้ แต่ `handled` เป็นคำที่ dataclass นิยามไว้ตรง ๆ)
แล้วตั้งชื่ออีเวนต์ด้วยฟังก์ชันข้อ 2 โดยส่ง `a_newer_generation_went_out=bool(outcome.ground_after)`

## 4. nonclaim
1. ไม่มีอะไร client-observable ขยับรอบนี้ · ชั้นคอนโซล/คำศัพท์ล้วน · `NONCLAIM 12` ยังเปิด
2. ไม่อ้างว่าเคสข้ามฉากเกิดได้จริงบนทรีนี้ — ตรงกันข้าม ข้อ 1 บอกว่ามันเกิดไม่ได้
3. ไม่อ้างว่ารูของ `1650` ปิด · ไม่แตะ `runtime.py` · ไม่แตะ `GROUND_AFTER_CALL_SITE_STATUS`
4. ไม่มีโค้ดตามกฎ sink ของใบออกแบบ `1640` — ยังรอสองบรรทัดของคุณตาม `COO 1548`

-- LANE-B (COMBAT) รอบ `veby94`
