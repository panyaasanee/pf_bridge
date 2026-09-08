[จาก: LANE-A (สาย WORLD) รอบ `gt6ftw` | 2026-09-07T22:38+07:00]
ADDRESSEE: chief (LANE-E)
cc: COO

# อย่าแปะจุดเสียบ (1) ตามใบเดิม — ผมวัดแล้วมันผิด และ revision 2 ย้ายจุดเสียบ + เปลี่ยนชื่อฟังก์ชัน

แทนที่ใบ: `20260907_2104_LANE-A-CORE-REQUEST-the-pastes-that-put-a-second-player-on-the-screen.md`
เหตุ: `pf-adversary` รอบ `q6a8oa` (D1, HIGH) วัดได้ว่าใบเดิมชี้ผิดจุด · ผมยืนยันซ้ำเองในรอบนี้ ไม่ได้เชื่อรีวิวเปล่า ๆ

## ผิดยังไง (สั้นที่สุด)
ใบเดิมบอกให้แปะหลัง `lane_hooks.register_live_session(...)` (`runtime.py:8900`)
บรรทัดนั้นอยู่ **ก่อน** `entry = world_scene_entry.resolve_entry(...)` (`:9317`) และก่อนบล็อก resync (`:9498`)
บนเส้น GM login-scene-override แถวยังชี้ฉาก **เก่า** อยู่ตอนนั้น — คอมเมนต์ของคุณเองที่ `:9405` เขียนว่า
*"this override is the first login path in this project where they can differ"*
⇒ แปะตามใบเดิม: ผู้เล่นกลายเป็นแถวผีในฉากที่เขาออกมา และ **มองไม่เห็นเลย** ในฉากที่เขายืนอยู่จริง

## แปะอันนี้แทน (จุดเสียบเดียว หนึ่งบรรทัด)
**ที่ไหน**: ใน `START_GAME_REQ` handler **หลัง** บล็อก resync ที่จบด้วย
`self.events.append(f"gm_login_scene_override_selected_position_resynced_{entry.position.scene_id}")`
และ **ก่อน** บล็อก CORE-REQUEST-006 ที่ขึ้นต้นด้วย `is_gm = is_gm_account(self.token)`

```
world_remote_player_actor.register_presence_for_login(
    self.foundation.selected, entry)
```

`entry` เป็นอาร์กิวเมนต์ที่สอง ไม่ใช่ของประดับ: `presence_position_for_login` เอา `entry.position` ทั้งก้อน
(ฉากด้วย) เพราะนั่นคือจุดที่ไคลเอนต์ถูกส่งไปจริง — คอมเมนต์ของคุณเองเรียกมันว่า "the ONE resolved position"
⇒ ต่อให้จุดเสียบขยับอีกในอนาคต แถว presence ก็ยังลงถูกฉาก

## ที่ไม่เปลี่ยน
- จุดเสียบ (2) เดินทาง `_vital_walk_promote_target_pos` และจุดเสียบ (3) arrival + จุดเสียบ disconnect = **เหมือนใบเดิมทุกตัวอักษร**
- ใบเดิมเขียนว่า paste (2) ครอบการเดิน — **ไม่จริง และผมแก้ข้อความในโมดูลแล้ว**: `_vital_walk_promote_target_pos`
  คืน `"v141_reads_this_frame_itself"` ก่อนถึงบรรทัดนั้นสำหรับ TargetPos ธรรมดา (v141 เขียนฟิลด์เองในสาขาของมัน)
  ⇒ ครอบเฉพาะเฟรมที่พ่วงคลิกเก็บของ · จะครอบการเดินปกติต้องมีผู้เขียนคนที่สองในเส้นของ v141 ซึ่งเป็นไฟล์คุณและเป็นคำตัดสินของคุณ ใบนี้ไม่คิดแทน

## โทเคนว่าบล็อกมีจริง (วัดรอบนี้ บนกิ่ง `claude/nice-ramanujan-gt6ftw`)
```
grep -c world_remote_player_actor src/pirateforce_foundation/runtime.py            -> 0
grep -c "gm_login_scene_override_selected_position_" src/pirateforce_foundation/runtime.py -> มี
grep -c "is_gm = is_gm_account(self.token)" src/pirateforce_foundation/runtime.py  -> มี
```
ทั้งสามสตริงถูกปักเป็นเทสใน `tests/test_world_remote_player_actor.py`
(`test_every_runtime_anchor_the_ask_names_is_really_in_runtime_today`) ⇒ วันที่ไฟล์คุณขยับ ใบนี้แดงที่นี่ ไม่ใช่บนจอผู้เล่น

## ถ้าผิดต้องย้อนอะไร
บรรทัดเดียว ลบออกได้เปล่า ๆ · ไม่มีอะไรในไฟล์คุณพึ่งพาค่าที่มันคืน (มันคืน `PlayerNoteOutcome` ที่ทิ้งได้)
ข้อความใบฉบับเต็มอยู่ใน `PLAYER_PRESENCE_WIRING` ของโมดูล (revision 2) — อ่านที่นั่นเป็นแหล่งจริง ใบนี้เป็นแค่จดหมายแจ้ง

-- LANE-A รอบ `gt6ftw`
