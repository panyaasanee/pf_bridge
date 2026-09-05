[ถึง: chief | จาก: LANE-GM (รอบ `f5htuc`) | 2026-09-05T15:34+07:00]
ADDRESSEE: chief
cc: COO

# `tools/pf_equip_attack_behavior_extract.py` ไม่เคย commit -- `.gitignore` กันไว้ -- เทสหนึ่งตัวแดงถาวรบน fresh clone

พบระหว่างรันชุดเต็มบังคับของรอบนี้ ไม่ใช่งานของสายนี้ (`test_combat_pose.py` / `tools/` เป็นของ LANE-B)
เขียนใบนี้เพราะเป็นเกตของทุกสาย ไม่ใช่แค่ของ LANE-B

## ค้นแล้ว: เจอ
- ชุดเต็มบน `origin/main` (สอง commit ล่าสุด `fff3969`) แดง 1 ตัวเสมอ:
  `tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_the_shipped_tables_when_it_can_run`
  `FileNotFoundError: tools/pf_equip_attack_behavior_extract.py` -- ไฟล์ไม่มีอยู่จริงในเช็คเอาต์
- `.gitignore` บรรทัด 118-119: `!/tools/` แล้ว `/tools/*` (deny-by-default, ต้อง allowlist ทีละไฟล์)
  `grep -n "pf_equip_attack_behavior_extract" .gitignore` = **0 hit** -- ไม่มีบรรทัด
  `!/tools/pf_equip_attack_behavior_extract.py` ที่ไหนเลย ต่างจากไฟล์ `pf_*.py` อื่นในโฟลเดอร์เดียวกัน
  ที่ทุกตัวมี allowlist ของตัวเอง (`pf_class_skill_starting_kit_extract.py`,
  `pf_scene_cast_sources_extract.py`, ...)
- `git log --all -- tools/pf_equip_attack_behavior_extract.py` = **0 commit ในประวัติทั้งรีโป**
  -- ไม่ใช่ไฟล์ที่เคยอยู่แล้วถูกลบ เป็นไฟล์ที่ไม่เคย commit เลยตั้งแต่ต้น
- ไฟล์ถูกอ้างชื่อจริงใน 4 จุด (`combat_pose.py:42,128`, `pose_trial.py:104`,
  `test_combat_pose.py:214`) -- โค้ด production คาดว่ามันมีอยู่ แค่ไม่เคยถูกปล่อยให้ผ่าน `.gitignore`
- decorator `@BRIDGE_GAMEDATA.skip_unless_present()` เช็คแค่ว่า `pf_bridge/gamedata` มีอยู่ไหม
  (sibling repo) ไม่ได้เช็คว่าตัวสคริปต์เองมีอยู่ในเช็คเอาต์นี้ไหม -- เพราะงั้นในสภาพแวดล้อมไหนก็ตามที่มี
  `pf_bridge` (ทั้งคลาวด์แบบนี้และเครื่อง Panya) เทสนี้จะพยายามรันเสมอ และแดงเสมอ

## ผลกระทบที่วัดได้
เทสนี้แดงถาวรบน `origin/main` ปัจจุบัน โดยไม่เกี่ยวกับ diff ของรอบไหนเลย -- ทุกรอบที่รันชุดเต็มจะเจอ
1 failed ตัวนี้ และต้องเสียเวลาแยกแยะทุกครั้งว่าเป็นของตัวเองหรือไม่ (รอบนี้เสียไปเพราะไม่มีมาก่อน)
ไม่แน่ใจว่าเกต Windows บนเครื่อง Panya เขียวเพราะมีสำเนาไฟล์นี้อยู่นอก git จริง หรือแดงเหมือนกันแต่
ไม่มีใครสังเกต -- ไม่มีอำนาจแตะ `tools/`/`.gitignore` เพื่อตรวจเอง

## ไม่ใช่ของสายนี้ ไม่ได้แก้
`tools/`, `.gitignore`, `combat_pose.py`, `test_combat_pose.py` อยู่นอกเขตเขียนของ LANE-GM ทั้งหมด
(เขตนี้ = `gm/`, `scenarios/gm_*.json`, `tests/test_gm_*.py`, `docs/GM_LANE.md`) -- ส่งเป็นใบพบ ไม่ใช่ PR แก้

## เสนอ (ไม่ใช่คำสั่ง)
ถ้าไฟล์นี้ยังอยู่บนเครื่อง Panya นอก git ให้ commit เข้าไปพร้อม `!/tools/pf_equip_attack_behavior_extract.py`
ในบรรทัด allowlist -- หรือถ้าตัวสร้างตารางถูก retire ไปแล้วจริง ให้ตัดสินใจว่าจะลบเทสนี้หรือเปลี่ยนเป็น skip
เมื่อไม่มีสคริปต์ (ไม่ใช่แค่เมื่อไม่มี `pf_bridge`)

## nonclaim
ไม่อ้างว่า `EQUIP_VALUE_SHA256`/`CREATION_GEAR_SHA256` (เทสอีกตัวในไฟล์เดียวกัน) ผิด -- ตัวนั้นผ่าน
ไม่อ้างว่ากระทบเกต Windows จริง (ไม่มีเครื่องนั้นให้ตรวจ) · ไม่แตะไฟล์ใดในใบนี้เลย
