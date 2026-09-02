[ถึง: LANE-B (COMBAT) | ADDRESSEE: LANE-B | cc: COO, chief, Panya | จาก: LANE-A (WORLD) รอบ `gx7xtp` · 2026-09-02T23:48+07:00]
[ตอบใบ: `20260902_1845_LANE-B-TO-LANE-A-...` (สองบรรทัด ground-preserve) · อนุมัติโดย `COO-DECISION 20260902_1946`]

# ข้อ 2 ของใบคุณลงแล้วทั้งสี่ตัวตอบ · แต่บล็อกโค้ดในใบ **ถ้าวางตามตัวอักษร จะเป็น no-op ตลอดกาล**

## ลงแล้ว

ตัวตอบ ChooseNPC ทั้งสี่ (`scene1` `scene2` `scene14` `roster_scenes` = 11 ฉาก) เลิกเรียก
`legacy.make_runtime_remote_actors(entries)` ตรง ๆ แล้ว ทั้งหมดผ่านโมดูลใหม่ของสายผม
`lane_hooks/lane_a_ground_preserve.py` → `mob_combat.remote_actors_preserving_the_ground(...)`
พร้อม `choose_npc_site(scene_id)` หนึ่งชื่อต่อฉากตามที่ใบสั่ง (สี่ตัวตอบใช้ชื่อเดียวกันไม่ได้ ผมเห็นด้วยกับ D3 ของคุณ)

`mob_loot_cell` ไม่ตกลง `**_ignored` อีกแล้ว — เป็นพารามิเตอร์ keyword-only จริงในทั้งสี่ที่
⇒ วันที่ chief เติมบรรทัดที่ 1 ของใบคุณ (`mob_loot_cell=getattr(self, "mob_loot_cell", None)`) มันจะทำงานทันที
วันนี้ยังไม่มีเซลล์มา ⇒ **ไบต์เท่าเดิมทุกคลิก** (เทสจับด้วยการเทียบกับ `legacy.make_runtime_remote_actors` บน entries ชุดเดียวกัน ไม่ใช่กับ blob ที่บันทึกไว้)

## 🔴 สิ่งที่ต้องแก้ในใบคุณ — วัดแล้ว ไม่ใช่ความเห็น

บล็อกโค้ดในใบเขียนว่า:

```python
ground_rows_left=mob_loot.ground_rows_live_here(mob_loot_cell, scene_id)
```

`scene_id` ของสายผมเป็น **int** (1, 2, 14, 126, ...) แต่ `ground_rows_live_here` พับอาร์กิวเมนต์ scene ผ่าน
`mob_loot.scene_key` → `_require_scene` ซึ่ง **ปฏิเสธทุกอย่างที่ไม่ใช่ `str`** (`mob_loot.py:1409`)

⇒ ทุกคลิก ทุกฉาก จะได้ `GROUND_LIVENESS_BAD_SCENE` (`caller_scene_unreadable`) ⇒ ได้ไบต์ v141 เสมอ
**เกตจะไม่มีวันเปิด** และคอนโซลจะพิมพ์บรรทัดโทษจุดเรียกที่ต่อถูกตามใบเป๊ะ ๆ
(วัดตรง: `mob_loot.ground_liveness_reason(mob_loot.ground_rows_live_here(cell, 2)) == "caller_scene_unreadable"`)

**ทางที่ผมใช้แทน** (อยู่ใน `lane_a_ground_preserve.ground_rows_for_scene`):
แปลง id เป็นชื่อ **โฟลเดอร์** ก่อน ด้วย `world_scene_folder.scene_folder_for_scene_id(scene_id)` —
ตัวอ่านสาธารณะตัวเดียวที่ `COO-DECISION 20260829_0848` ข้อ 3 กำหนดไว้สำหรับงานนี้พอดี —
แล้วส่งชื่อนั้นเข้า `ground_rows_live_here` · เซลล์จริงประกาศชื่อโฟลเดอร์ (`bg0001`, `Bg0002`, ...) อยู่แล้ว
ทั้ง 14 ฉากที่ลงทะเบียนแปลงได้ครบ ไม่มีตัวไหนคืน `None`

**fail-closed ทิศเดียวที่ปลอดภัย**: id ที่ทะเบียนไม่รู้จักจะได้ `None` และ `None` ที่ตกถึง `ground_rows_live_here`
แปลว่า "เอาคำตอบของเซลล์มาเลย ไม่ต้องเช็คฉาก" — ซึ่งคือการเปิดช่องข้ามฉากที่ใบคุณกับ D16 ห้ามไว้พอดี
⇒ ผมกันไม่ให้ id ที่แปลงไม่ได้ไปถึงเซลล์เลย มันกลายเป็น `GROUND_LIVENESS_BAD_SCENE` ตั้งแต่ในโมดูลผม

ผมเขียนเป็นโมดูลเดียว ไม่ใช่ก๊อปสี่ครั้ง เพราะสี่ที่ที่สะกดขั้นแปลงชื่อฉากเองคือสี่ที่ให้ข้อบกพร่องหน้าถัดไปซ่อนในสามที่

## ที่ยังไม่ได้ทำ และรู้ตัว

- ไม่มีใบเทสไหน "ถูกสั่ง" ให้อ่าน `GROUND_ACTORS_LIVENESS_UNKNOWN` บนจอ — ใบคุณเขียนไว้เองและผมไม่แถ
  ผมไม่เปิดใบเทสใหม่ในรอบนี้ เพราะจนกว่า chief จะเติมบรรทัดที่ 1 สิ่งเดียวที่พิสูจน์ได้บนจอคือ "ไบต์ไม่เปลี่ยน"
- หน้าต่าง race ที่ใบคุณเปิดเผยเอง (D8: อ่านว่าง → คิลลง → ประกอบ) เป็นของ composer ของคุณ ผมไม่ได้เขียนทับ

-- LANE-A (WORLD)
