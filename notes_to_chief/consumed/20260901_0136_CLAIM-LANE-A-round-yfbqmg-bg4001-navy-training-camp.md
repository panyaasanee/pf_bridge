CLAIM
ADDRESSEE: LANE-A
จาก: LANE-A (สาย A · WORLD) รอบ yfbqmg
เวลา: 2026-09-01T01:36+07:00
อายุใบจอง: 90 นาที (หมดอายุ 2026-09-01T03:06+07:00)

หัวข้อที่จอง: การเลือกฉากถัดไปที่จะทำ crosswalk / census -- ฉาก 130 (Bg4001, Navy Training Camp,
42 placements)

เหตุผลที่ต้องจอง: COO-DECISION `20260831_1345_lane-a-scene-claim-extends-claim-before-work.md`
ขยายกฎ claim-before-work ให้ครอบคลุมการเลือกฉากถัดไปของสาย A ทุกรอบ

## เช็คก่อนเริ่ม (ณ 01:36+07:00)

- ไม่มี PR หัวข้อ `[LANE-A]` เปิดค้างใน pirate-force-server หรือ pf_bridge (ตรวจผ่าน
  `mcp__github__search_pull_requests`, `total_count: 0` ทั้งสองรีโป)
- ไม่มี `*CLAIM-LANE-A*` อื่นที่อายุยังไม่เกิน 90 นาทีสำหรับฉากใดๆ ใน `notes_to_chief/` (ไฟล์ CLAIM ล่าสุด
  ก่อนใบนี้คือ `20260831_2327_CLAIM-LANE-A-round-68mm02-bg0011-*` ซึ่ง consumed แล้วและอายุเกิน 90 นาที)
- `git log --all --diff-filter=A -- 'src/pirateforce_foundation/world_bg4001_identity.py'
  'src/pirateforce_foundation/world_population_bg4001.py'` ทั้งสองรีโปว่างเปล่า -- ยังไม่มีใครสร้างไฟล์ชื่อนี้
  บน `main` มาก่อน
- Registry (`scenarios/world_scene_registry_001.json`) บน `main` (หลัง fast-forward merge เข้า
  origin/main ล่าสุด, pirate-force-server HEAD `b2563dc`): เปิดแล้วครบ 3,4,5,6,7,8,9,10,11 (เก้าประตูจาก
  สิบประตูเดิม) -- เหลือปิดฉากเดียวจากสิบประตูเดิม: **130 (Bg4001, Navy Training Camp, 42 placements,
  `login_entry_allowed: false`)** ตามที่รอบ `68mm02` (แผนก่อนหน้า) บันทึกไว้ในใบ
  `20260831_2349_LANE-A-STATUS-bg0011-*.md`

แผน: build (identity + population crosswalk) + wire (registry, census composer, handoff) + open
(`login_entry_allowed: true`) ในรอบเดียวตามรูปแบบเดิมที่ใช้กับเก้าฉากก่อนหน้า ตรวจ
`git log --all` และ registry สดอีกครั้งก่อนสร้างไฟล์ใหม่ทุกไฟล์เพื่อกันชนซ้ำ (บทเรียนจากรอบ `ir0lpw`)

-- LANE-A (WORLD) round `yfbqmg`
