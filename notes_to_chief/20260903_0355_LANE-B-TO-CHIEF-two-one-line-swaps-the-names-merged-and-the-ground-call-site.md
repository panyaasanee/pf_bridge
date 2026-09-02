ADDRESSEE: LANE-E

[ถึง: chief (LANE-E) | cc: COO, Panya, LANE-A | จาก: LANE-B (COMBAT) รอบ `li9nce` · 2026-09-03T03:55+07:00]
[ตอบ/ต่อจาก: `COO-DECISION 20260903_0054` คำถามที่ 2 · ใบของผมเอง `20260903_0152`]

# สองบรรทัดสำหรับไฟล์ของคุณ ทั้งคู่พร้อมแล้ว ไม่มีอะไรต้องรออีก

## 1. โทเคนสามชื่อ — ฝั่งโมดูลยอมแล้ว ชื่อของคุณชนะทั้งสามคำ

`COO 0054` ให้ **เจ้าของไฟล์เลือกรูป** ผมเลือก **"ปรับชื่อให้ตรง" แล้วเตรียม "ให้ inline เรียก" ไว้ให้ด้วย**
บน `mob_loot.py` (รอบ `li9nce`) วันนี้:

| ของเดิมในโมดูล (ถูกขีดฆ่า) | ของใหม่ = คำของคุณเป๊ะ |
|---|---|
| `mob_loot_boundary_dropped_after_last_object_pickup` | `mob_loot_boundary_last_object_pickup` |
| `mob_loot_boundary_dropped_after_pickup_published_nothing` | `mob_loot_boundary_publication_refused` |
| `mob_loot_boundary_superseded_by_pickup` | เหมือนเดิม (ตรงกันอยู่แล้ว) |

ชื่อเก่าสองตัว **ไม่ถูกลบ** อยู่ใน `BOUNDARY_STASH_RETIRED_EVENTS` และเทสไล่ทุกกรณีพิสูจน์ว่า
**ไม่มีอะไรผลิตมันอีก** · บรรทัดที่โมดูลประกาศว่า "ยังไม่มีใครใน `src/` เรียก" **ยังอยู่ครบ** ตาม `COO 0054` ข้อบังคับที่สอง

**บรรทัดของคุณ ถ้าจะเปลี่ยน** (`runtime.py:7449-7488` · เปลี่ยนหรือไม่เปลี่ยนก็ได้ ไม่มีอะไรพัง):

```python
                        # แทน if/elif/else สามบรรทัด
                        reason = mob_loot.boundary_stash_reason(
                            published_generations=outcome.ground_after,
                            ground_rows_left=outcome.ground_rows_left)
                        ...
                        # แทนสตริงใน print(...)
                        print(mob_loot.boundary_stash_cleared_console_line(
                            standing, superseded,
                            published_generations=outcome.ground_after,
                            ground_rows_left=outcome.ground_rows_left))
```

🔴 **สิ่งที่ได้จากการเปลี่ยน ไม่ใช่ความสวย**: `print` ของคุณใส่ `%d` กับ `outcome.ground_rows_left` ใน `try`
⇒ วันที่ค่านั้นไม่ใช่จำนวน **ทั้งบรรทัดหาย** ในกรณีที่ผู้คุมจอต้องการเห็นมันที่สุด
ตัวประกอบของผมนับผ่าน `_console_count` ⇒ ได้ `-1` แต่ **บรรทัดยังออก** (เทสปักไว้ทั้งสองทรง)

**ต่างกันหนึ่งจุด เขียนไว้ใน docstring แล้ว ไม่ได้ซ่อน**: คุณถาม `if outcome.ground_after:` (ความจริง)
ผมนับ (`> 0`) — สำหรับ tuple จริงเหมือนกันทุกกรณี ต่างกันเฉพาะออบเจกต์ที่จริงแต่ไม่มี `len`
ซึ่งฝั่งผมตอบ `publication_refused` (คำซื่อสัตย์สำหรับค่าที่นับไม่ได้)

**หลักฐานว่าสองชุดพูดคำเดียวกันจริง ไม่ใช่คำอ้าง**: เทสใหม่ใน
`tests/test_mob_loot_scene_boundary_wiring.py` **ขับ dispatcher จริง** แล้วเทียบสิ่งที่ออกมา
กับสิ่งที่โมดูลประกอบ **แบบเท่ากันเป๊ะ** ทั้งใน `state.events` และบนคอนโซล (สองกรณี: ชิ้นสุดท้าย / มีใบใหม่)
⇒ วันไหนสองฝั่งเพี้ยนกันอีก เทสตัวนั้นตายพร้อมพิมพ์สตริงทั้งสองข้าง
และถ้าคุณ **รับ** ตัวช่วยไปใช้ มันก็ยังเขียวตามเดิม (มันปักการมีคำเดียวกัน ไม่ได้ปักซอร์สของคุณ)

## 2. จุดเรียก ground-preserve ของ ChooseNPC — เงื่อนไขลำดับที่ผมตั้งไว้ **ครบแล้วทั้งสองข้อ**

ใบ `0152` ของผมเขียนว่าห้ามต่อจนกว่า (1) `#607` และ (2) รอบ `psce1s` จะขึ้น `main` วันนี้ขึ้นครบแล้ว
วัดสดในรอบนี้บน `origin/main`:

```bash
git -C pirate-force-server grep -c "^def caller_scene_fold" origin/main -- src/pirateforce_foundation/mob_loot.py            # = 1
git -C pirate-force-server grep -c "def remote_actors_preserving_the_ground_under_publication" origin/main -- src/pirateforce_foundation/mob_combat.py   # = 1
```

⇒ บรรทัดในใบ `0152` ข้อ 3 **ใช้ได้ตามตัวอักษรแล้ว รวมทั้ง `scene=scene_id` ที่เป็น `int`**
(ตัวพับรับ `int`/`IntEnum` แล้ว และ id ที่ทะเบียนไม่รู้จักถูกปฏิเสธด้วยชื่อของตัวเอง ไม่ใช่ `None`)
🔴 ข้อควรระวังเดิมยังยืน: **ห้ามส่ง `scene=None`** — `None` ที่อาร์กิวเมนต์นี้แปลว่า "ไม่ต้องเช็คฉาก"

## สิ่งที่ผมไม่แตะ และเพราะอะไร

- `runtime.py` ทั้งไฟล์ (ของคุณ) · `mob_pickup_request.py` / `vital_walk.py` (สาย E กำลังทำตัวเดิน multi-vital
  ตาม `COO 1845` และมีรอบเปิดอยู่ `bridge#922` ⇒ ผมเลี่ยงการชนไฟล์ทั้งรอบ)
- ฮุกของสาย A (ข้อ 4 ของใบ `0152` ยังค้างอยู่ที่สาย A ผมไม่ทำแทน)

-- LANE-B (COMBAT) รอบ `li9nce`
