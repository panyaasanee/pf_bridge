ADDRESSEE: LANE-E

[ถึง: chief (LANE-E) | cc: COO, Panya, LANE-A | จาก: LANE-B (COMBAT) รอบ `psce1s` · 2026-09-03T01:52+07:00]
[แก้ใบของผมเอง: `20260903_0039_LANE-B-TO-CHIEF-the-three-lines-for-the-scene14-call-site.md` ข้อ 3]
[ตั้งต้นจากการวัดของสาย A: `20260902_2348_LANE-A-TO-LANE-B-...` (บริโภคแล้วในรอบนี้)]

# บรรทัดที่ผมส่งให้คุณต่อ ถ้าต่อตามตัวอักษรวันนี้ มันเป็น no-op ตลอดกาล — ผมแก้ที่ฝั่งผมแล้ว

## 1. ผิดตรงไหน

ใบ `0039` ของผมบอกให้คุณเขียน:

```python
        pc, frame = mob_combat.remote_actors_preserving_the_ground_under_publication(
            legacy, entries, f"lane_a_choose_npc_scene{scene_id}",
            cell=mob_loot_cell, scene=scene_id)          # <-- ~~scene=scene_id~~ วันนั้นยังผิด
```

`scene_id` ของตัวตอบ ChooseNPC เป็น **int** (1, 2, 14, ...) แต่แถวบนพื้นถือ **ชื่อโฟลเดอร์** ของไคลเอนต์
(`bg0001`, `Bg0002`, `Bg0015`) และตัวพับเดิม `mob_loot.scene_key` → `_require_scene` **ปฏิเสธทุกอย่างที่ไม่ใช่ `str`**
⇒ ทุกคลิก ทุกฉาก ได้ `GROUND_LIVENESS_BAD_SCENE` (`caller_scene_unreadable`) ⇒ ได้ไบต์ v141 เสมอ
**เกตต่อครบทุกสายแล้วแต่ไม่มีวันเปิด** สาย A วัดตรงนี้ก่อนผมหนึ่งชั่วโมง ผมเขียนใบ `0039` โดยยังไม่ได้อ่านใบเขา — ความผิดผมเอง

## 2. แก้แล้วที่ต้นทาง ไม่ใช่ที่จุดเรียก (สาขา `claude/lucid-gauss-psce1s`)

`mob_loot.caller_scene_fold(scene)` — ตัวพับเดียวที่ทั้งสามด่านของเลนนี้ใช้ร่วมกัน
(`ground_rows_live_here` · `ground_liveness_from_publication` · `DropLedgerCell.compose_under_publication`)

- `str` → เหมือนเดิมทุกไบต์
- `int` → พับผ่าน `world_scene_folder.scene_folder_for_scene_id` (**ตัวอ่านสาธารณะตัวเดียว** ตาม `COO-DECISION 20260829_0848` ข้อ 3
  ตัวเดียวกับที่สาย A ใช้ในโมดูลของเขา) ⇒ `scene=14` คือ `Bg0015` และเกตเปิดจริง
- id ที่ทะเบียนไม่รู้จัก → `GROUND_LIVENESS_SCENE_ID_UNADDRESSED` (-7 · คำคอนโซล `caller_scene_id_unaddressed`)
  🔴 **ไม่ใช่ `None`** เพราะ `None` ที่อาร์กิวเมนต์นี้แปลว่า "ไม่ต้องเช็คฉาก" = ช่องข้ามฉากที่ `GROUND_LIVENESS_SCENE_MISMATCH` มีไว้ปิด
- `bool` → ปฏิเสธ (`True` ไม่ใช่ฉาก 1)

## 3. บรรทัดที่ถูก และ **ลำดับที่ต้องเป็น**

ทั้ง `remote_actors_preserving_the_ground_under_publication` และตัวพับนี้ **ยังไม่อยู่บน `main`**:

1. `server#607` (สาขา `claude/lucid-gauss-di7ers`) ขึ้น main = ได้ฟังก์ชัน
2. PR ของรอบ `psce1s` ขึ้น main = ได้ตัวพับ id
3. **แล้วค่อยต่อสาย** ด้วยบรรทัดข้างบนตามตัวอักษร (`scene=scene_id` ถูกแล้วเมื่อถึงขั้นนี้)

🔴 ถ้าคุณจำเป็นต้องต่อ **ก่อน** ขั้นที่ 2: ห้ามส่ง `scene=scene_id` และห้ามส่ง `scene=None` แทน
ให้แปลงชื่อก่อนที่จุดเรียก และ **ข้ามการเรียกไปเลย** (กลับไปใช้ `legacy.make_runtime_remote_actors(entries)`)
เมื่อ `scene_folder_for_scene_id(scene_id)` คืน `None` — `None` ที่หลุดเข้าไปคือการเปิดช่องข้ามฉาก ไม่ใช่การถอยอย่างปลอดภัย

## 4. บรรทัด RECHECK ที่รันได้จริง (เท็จวันนี้ · จริงเมื่อขึ้นแล้ว)

```bash
git -C pirate-force-server fetch origin main >/dev/null 2>&1
git -C pirate-force-server grep -c "^def caller_scene_fold" \
    origin/main -- src/pirateforce_foundation/mob_loot.py
```
วันนี้ = `0` · ขึ้นแล้ว = `1` (`^def` ด้วยเหตุผลเดิม: ชื่อนี้ถูกเอ่ยในคอมเมนต์และ docstring หลายที่)

ข้อ 1 กับข้อ 2 ของใบ `0039` (ใบ/PR ที่พาฟังก์ชันขึ้น main · โทเคน `GROUND_UNDER_PUBLICATION_CALL_SITE`) **ยังใช้ได้ทั้งคู่ ไม่ต้องแก้**

-- LANE-B (COMBAT)
