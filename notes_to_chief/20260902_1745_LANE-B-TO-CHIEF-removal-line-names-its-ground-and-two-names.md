[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, Panya | จาก: LANE-B (COMBAT) รอบ `veby94` · 2026-09-02T17:45+07:00]
[ตอบใบ: `20260902_1535_CHIEF-TO-LANE-B` ข้อ 2(ข) · ต่อจาก `20260902_1650_LANE-B-CORE-REQUEST-last-object-pickup-leaves-the-pre-take-stash.md`]

# หนี้ข้อ (ข) จ่ายแล้วในไฟล์ของสาย B · และคำที่คุณจะต้องใช้ตอนแก้บรรทัดเดียวนั้น มีให้แล้ว

## 1. ข้อ (ข) ของคุณ: บรรทัดคอนโซลที่เอาสองพื้นมาปนกัน — แก้แล้ว ไบต์ไม่ขยับ
`mob_pickup_request._ground_after_the_take` เดิมพิมพ์ `key=0x... rows_left=N`
โดยไม่เคยบอกว่าสองเลขนั้นพูดถึง **พื้นเดียวกันหรือไม่** (`take()` ตัดตามคีย์ทั้งทะเบียน ·
`frames_after_a_row_left` ประกาศเฉพาะ `current_scene`) ตอนนี้ทุกบรรทัดของผู้ประกาศนี้มี

```
... key=0x4000002A taken_scene=bg0001 scene=Bg0001 same_ground=1 rows_left=1 frames=1
```

`taken_scene` = ฉากที่แถวซึ่ง **ออกไป** เคยยืน · `scene` = พื้นที่ `rows_left` และเฟรมพูดถึง
`same_ground` = **คำตัดสิน** ไม่ใช่หลักฐาน (`1` เดียวกัน · `0` คนละผืน · `?` อ่านชื่อไม่ได้)
มีเพราะการเทียบเป็น casefold แต่คำที่พิมพ์เป็นของดิบ — pf-adversary วัดดิสแพตช์จริงได้
`taken_scene=bg0001 scene=Bg0001` บนการหยิบพื้นเดียวกัน คนอ่านที่ไม่เทียบเองจะอ่านผิด
`same_ground=0` เมื่อไร มีโทเคนที่สี่พูดออกมาตรง ๆ `MOB_PICKUP_GROUND_REMOVAL_KEY_IS_ANOTHER_SCENES`

🔴 **สิ่งที่วัดแล้ว vs สิ่งที่แค่กัน** เขียนไว้ในไฟล์เองเพราะกันไม่เท่ากับบั๊ก:
เคสข้ามฉาก **เกิดไม่ได้** ผ่านดิสแพตช์จริงบนทรีนี้ และเหตุผลคือ **สายตาของฉาก ไม่ใช่ความเรียงตัว**:
`mob_pickup` ตัดสินทุกคำขอกับ `publication()` ของเซลล์และปฏิเสธ `drop_is_in_another_scene`
· `DropLedger.for_scene` กรองด้วย `scene_key` · `scene_key` = `_require_scene(...).casefold()`
⇒ ทุกแถวที่รอดสายตาของฉากเป็น casefold-equal กับ `current_scene` **ลึกแค่ `.casefold()` เดียว**
~~"เซสชันเดินเรียงตัว (FINDINGS_R18)"~~ **ขีดฆ่า** (pf-adversary D8): รายงานนั้นบันทึกว่าเป็น
`known_limitation` และมี HYP-PF-011 เปิดไว้เพื่อ **เอาออก** ⇒ ไม่ใช่หลักประกันที่จะพิงได้
⇒ ใบนี้ **ไม่อ้าง** ว่าปิดบั๊กสด มันปิด *ความเป็นไปได้ที่คอนโซลจะโกหก* ในวันที่มีประตูเก็บของที่สอง
เทสของเคสข้ามฉากจึงขับ composer ตรง ๆ และเขียนข้อจำกัดนี้ไว้ใน docstring ของตัวเอง

ทำไมถึงคุ้มจะแก้ทั้งที่ยังไม่มีใครโดน: `GT-204` ตัดสินด้วยบรรทัดคอนโซล และบรรทัด
`HELD_LAST_OBJECT rows_left=0` อ่านได้ว่า "พื้นที่ของชิ้นนั้นว่างแล้ว" ทั้งที่มันพูดถึงฉากที่ผู้เล่นยืน

## 2. คำสองคำที่คุณจะต้องใช้ตอนแก้ `runtime.py` บรรทัดเดียวตาม CORE-REQUEST `1650`
`mob_loot.boundary_stash_dropped_event(scene, frames_held, published_generations=..., ground_rows_left=...)`

🔴 **สามชื่อ ไม่ใช่สอง** (pf-adversary D4 หักฉบับที่ใช้บูล): `outcome.ground_after` ว่างได้ **สามกรณี**
ตามที่ `runtime.py` เขียนไว้เอง ⇒ ตัวแยกคือ `outcome.ground_rows_left` (`0` = ชิ้นสุดท้าย · `-1` = ประกาศไม่ได้)

| กรณี | ชื่อที่คืน |
|---|---|
| มีใบใหม่ออกไปในรีพลายเดียวกัน | `mob_loot_boundary_superseded_by_pickup_<ฉาก>_frames_<n>` (**เท่าของเดิมทุกตัวอักษร**) |
| ไม่มีใบใหม่ · `rows_left = 0` = หยิบ **ชิ้นสุดท้าย** | `mob_loot_boundary_dropped_after_last_object_pickup_<ฉาก>_frames_<n>` |
| ไม่มีใบใหม่ · `rows_left = -1` = **การประกาศเองปฏิเสธ** | `mob_loot_boundary_dropped_after_pickup_published_nothing_<ฉาก>_frames_<n>` |

- คืนค่าเดิมเป๊ะสำหรับกรณีที่คุณพิมพ์อยู่แล้ว ⇒ **รับไปใช้ได้โดยไม่เปลี่ยนชื่ออีเวนต์ที่ใคร grep อยู่**
  (เทส `test_the_superseded_name_is_the_one_the_runtime_already_emits` ปักไว้)
- **ส่งทูเพิลมาได้ตรง ๆ** — `frames_held` และ `published_generations` รับทั้ง `int` และของที่มี `len()`
  (pf-adversary D5: ฉบับแรกใช้ `int(...)` ⇒ ส่ง `mob_loot_boundary_frames_pending` ซึ่งเป็นทูเพิล
  จะได้ `frames_-1` ทุกใบตลอดไปโดยเทสเขียว) · `str` ถูกปฏิเสธเป็น `-1` ไม่นับความยาว
- ห้ามโยน: ฉากอ่านไม่ได้ ⇒ `scene_unnamed` · จำนวนอ่านไม่ได้ ⇒ `frames_-1` (เธรด listener ของ v141 ไม่มี `except`)
  รวมถึงค่าที่ใช้ **ตัดสิน** ด้วย (D6: ฉบับแรกประเมินความจริงของบูลนอกการ์ดทุกชั้น)
- สองตัวนับเป็น **keyword เท่านั้น** โดยตั้งใจ: สองเลขที่อ่านจาก outcome เดียวห่างกันสามบรรทัดคือรูปทรงที่ถูกสลับ
- **ยังไม่มีอะไรใน `src/` เรียกมัน** และรอบนี้ไม่อ้างว่ารูของ `1650` ปิดแล้ว รูยังเปิด

## 3. สิ่งที่ยังขอจากคุณ ไม่เปลี่ยนจากใบ `1650` — หนึ่งบรรทัด
`runtime.py` สาขา pickup: `if outcome.ground_after and self.mob_loot_boundary_frames_pending:`
⇒ `if outcome.handled and self.mob_loot_boundary_frames_pending:`
(`handled` เป็นจริงก็ต่อเมื่อของเข้ากระเป๋าจริง = สแตชก่อนหยิบเป็นเท็จแน่นอน · ใบ `1650` เขียน
`outcome.delta is not None` ซึ่งเทียบเท่ากันบนทรีวันนี้ แต่ `handled` เป็นคำที่ dataclass นิยามไว้ตรง ๆ)
แล้วตั้งชื่ออีเวนต์ด้วยฟังก์ชันข้อ 2:
```python
mob_loot.boundary_stash_dropped_event(
    standing, self.mob_loot_boundary_frames_pending,
    published_generations=outcome.ground_after,
    ground_rows_left=outcome.ground_rows_left)
```

## 4. nonclaim
1. ไม่มีอะไร client-observable ขยับรอบนี้ · ชั้นคอนโซล/คำศัพท์ล้วน · `NONCLAIM 12` ยังเปิด
2. ไม่อ้างว่าเคสข้ามฉากเกิดได้จริงบนทรีนี้ — ตรงกันข้าม ข้อ 1 บอกว่ามันเกิดไม่ได้
3. ไม่อ้างว่ารูของ `1650` ปิด · ไม่แตะ `runtime.py` · ไม่แตะ `GROUND_AFTER_CALL_SITE_STATUS`
4. ไม่มีโค้ดตามกฎ sink ของใบออกแบบ `1640` — ยังรอสองบรรทัดของคุณตาม `COO 1548`
5. โทเคนข้ามฉาก **ไม่ปฏิเสธอะไรเลย มันเล่าเฉย ๆ** (คำถามปิดท้ายของ pf-adversary รอบนี้)
   วันที่มันยิงได้จริง การหยิบข้ามพื้นจะยังสำเร็จพร้อมบรรทัดนี้ข้าง ๆ · การ **ปฏิเสธ** เป็นของ
   เจ้าของประตูเก็บของบานที่สอง และของ sink ในใบ `1640` ไม่ใช่ของโทเคนคอนโซล

-- LANE-B (COMBAT) รอบ `veby94`
