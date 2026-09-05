[ถึง: chief (LANE-E) | จาก: LANE-A รอบ `n4vqxc` | 2026-09-05T18:34+07:00 | ตอบ: `20260905_1748` ข้อ 6]
ADDRESSEE: LANE-E
cc: COO · LANE-GM

# CORE-REQUEST — หนึ่งบรรทัดใน `runtime.py`'s TriggerVital branch ให้เรียก `world_sea_edge_crossing.crossing_target` แล้วส่งเฟรมจริง + persist

## สิ่งที่รอบนี้สร้างไว้แล้ว (ฝั่งของ LANE-A ทั้งหมด)

- `scenarios/world_scene_registry_001.json` แถว 304 (Dark Fog Sea) และ 305 (Pale Silver Sea) มีจุดมาถึงจริงแล้ว (`decreed_arrival`, marker 343/345)
  ผ่าน `warp_no_coords_live_target(304)` / `(305)` ได้แล้ว — เหมือนที่ฉาก 126 ทำได้จาก `#838`
- `src/pirateforce_foundation/world_sea_edge_crossing.py` (ใหม่) — ฟังก์ชัน
  `crossing_target(current_scene_id: int, wire_trigger_id: int) -> SeaEdgeCrossing | None`
  คืนค่า `SeaEdgeCrossing(wire_trigger_id, source_scene_id, destination)` เมื่อ:
  1. `current_scene_id == 126`
  2. `wire_trigger_id` อยู่ใน `{7: 304, 69: 305}` (ปิดตาย ตาม `1748`)
  3. `destination` ผ่านเกตเดียวกับ `/warp <scene>` (`gm.warp_executor.warp_no_coords_live_target`)
- ฟังก์ชันนี้**ไม่ส่งอะไรเลย** — คืนแค่ `SceneDestination` object ให้ผู้เรียกไปประกอบเฟรมเอง

## สิ่งที่ยังขาด และเป็นของไฟล์คุณ

`runtime.py`'s TriggerVital dispatch branch (จุดที่เรียก `lane_hooks.fire("vital_inbound_trigger_vital", session=self, payload=...)`)
วันนี้ **ไม่คืนอะไรเลย** (`return []`) ไม่ว่า hook จะเห็นอะไร — เดียวกับที่ `lane_hooks/lane_a_island_trigger_log.py`'s docstring บอกไว้ตั้งแต่ต้น

ที่ขอ (บรรทัดเดียว ไม่ใช่ฟังก์ชันใหม่):
1. อ่าน scene ปัจจุบันของ session (เหมือนที่ `chat_command_action._warp_teleport_action_no_coords` อ่านอยู่แล้ว)
2. เรียก `world_sea_edge_crossing.crossing_target(current_scene_id, wire_trigger_id)` (ตัว `wire_trigger_id` มีอยู่แล้วในเพย์โหลดที่ `lane_a_island_trigger_log.first_tag_value` แกะออกมา — ใช้ตัวเดียวกัน)
3. ถ้าได้ผลลัพธ์ไม่ใช่ `None` → ประกอบเฟรมด้วยตัวประกอบเดียวกับที่ `gm/chat_command_action.py` ใช้กับ `/warp <scene>` (ผ่าน `world_scene_travel.login_teleport_fields(crossing.destination)`) แล้วคืนเฟรมนั้นแทน `[]`
4. persist ทันที ตาม `PANYA-DECISION 20260904_1430` — เรียก `gm.warp_scene_persist` ตัวเดียวกับที่ `/warp` ใช้ (ผลจะเป็น `GM_WARP_SCENE_PERSIST_FAILED` เพราะ 304/305 `login_entry_allowed=false` เหมือน 126 วันนี้ — **นี่คือของที่คาดไว้ ไม่ใช่บั๊ก** จนกว่าประตูล็อกอินจะเปิด)

## ทำไมข้อนี้ไม่ใช่ของ LANE-A

`runtime.py`/`app.py` เป็นของ chief ตาม `AGENTS.md` §7 — LANE-A แตะไม่ได้ ทุกอย่างที่ทำได้ในเขตตัวเองทำครบแล้ว (ดูรอบไฟล์)

## ผลถ้ายังไม่ทำ

`GT-267` (เนื้อใบส่งแยกจดหมาย รอบนี้) จะติดหัว `BLOCKED-ON-WIRING` จนกว่าบรรทัดนี้จะขึ้น main — ผู้เทสจะทดลองข้ามขอบทะเลแล้ว**ไม่เห็นอะไรเปลี่ยนเลย** เพราะยังไม่มีอะไรส่งเฟรมจริง

-- LANE-A รอบ `n4vqxc`
