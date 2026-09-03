# LANE-A round `t8m3ab` (start 2026-09-04T00:04+07:00)

**NOW.md ขยับข้อไหนรอบนี้: ไม่ขยับข้อไหน.** งานตรงกับสิ่งที่ COO บันทึกไว้แล้วใน
"งานด่วนตอนนี้" (ป้าย `2247`) และยังไม่ถึงเกณฑ์ "รอ Panya ติ๊ก" (โค้ด+เทสเสร็จ แต่ยังไม่มี
รอบ attended ยืนยันผลบนจอ เพราะฟีเจอร์นี้ไม่มีอะไรให้ผู้เล่นเห็นด้วยตัวเอง เป็นสัญญาระหว่างสาย)
รายงานเต็มส่งแยกถึง COO แล้ว: `notes_to_chief/20260904_0040_LANE-A-TO-COO-actor-identities-landed-pr687.md`

## ต้นรอบ

- list PR `[LANE-A]` เปิดทั้งสองรีโป: ไม่มี → ตัดกิ่งใหม่ ไม่ยึดต่อ
- PR `[LANE-A]` รอบก่อน (server `#683`, pf_bridge `#1023`, รอบ `gs8hmn`): ทั้งคู่ `merged=true`
  ตรวจด้วย `pull_request_read` โดยตรง → งานอยู่บน `main` แล้ว ไม่ต้องกู้อะไร
- กล่องจดหมาย: grep `ADDRESSEE: LANE-A` ที่ไม่มี stub เจอ 5 ใบ (`1207`, `1227`, `1249`, `1252`,
  `2247`) — ตรวจแล้วพบว่า 4 ใบแรก **มี stub อยู่จริง** (ชื่อไฟล์ stub ตัด `.md` ออกก่อนต่อ
  `.CONSUMED.txt` ซึ่งการเช็คครั้งแรกของผมเองไม่ได้คิดรูปแบบนี้ไว้ ตรวจซ้ำด้วยชื่อไฟล์ตรงแล้วเจอ
  ครบ) เหลือใบเดียวที่ยังไม่บริโภคจริง: `2247` — คืองานหลักของรอบนี้เอง

## งาน: `SceneCensusResult.actor_identities` (COO-DECISION `20260903_2247`)

LANE-B ต้องการรายชื่อ identity ที่ arrival census ของฉากส่งจริง เพื่อ splice ความเป็นศัตรู
ให้ฉาก 14 โดยไม่ต้องเดา (`notes_to_chief/20260903_2211_LANE-B-STATUS-...`) COO สั่งให้
`SceneCensusResult` พกฟิลด์ใหม่ อ่านผ่าน `field_mobs.roster_for_scene_id` (สาธารณะของสาย B)
ไม่ import ไฟล์ตารางต่อฉากของสาย B ตรง ๆ

- `src/pirateforce_foundation/lane_hooks/__init__.py`: เพิ่ม `actor_identities: tuple[int, ...] = ()`
- `src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py`: `_field_mob_identities(scene_id)`
  ใหม่ + import `field_mobs` + ต่อเข้า `_compose_for_scene`
- `tests/test_lane_a_scene_census.py`: คลาสใหม่ `ActorIdentitiesFromFieldMobRegistryTests`
  (6 เทส หลัง pf-adversary) รวมเทสมิวแทนต์ที่พิสูจน์ว่าฟิลด์ derive จากทะเบียนจริง

## pf-adversary (สั่งต้นรอบ ตามกฎ COO `0903_2345` — ผลกลับมาก่อนจบรอบ ไม่ต้อง `ADVERSARY_PENDING`)

พบ 3 ข้อ, 2 ข้อจริงแก้แล้วในคอมมิตที่สอง, 1 ข้อ informational:
1. **[CONFIRMED, แก้แล้ว]** คอมเมนต์ใน `lane_hooks/__init__.py` เขียนผิดว่าฉาก 2 เดินทาง
   เดียวกันด้วย — จริง ๆ ฉาก 1/2 ไม่เคยถึง `SceneCensusResult` เลย (กันไว้ทั้งใน `runtime.py`
   และ `RESERVED_BY_RUNTIME_BRANCHES`) แก้คอมเมนต์แล้ว
2. **[CONFIRMED, แก้แล้ว]** เคส "อ่านทะเบียนพัง" กับ "ไม่มีอะไรลงทะเบียน" ให้ผล `()` เหมือนกัน
   แยกไม่ออกบนคอนโซล — เพิ่มบรรทัด `WORLD_CENSUS_ACTOR_IDENTITIES_UNREPORTABLE reason=<Type>`
   เฉพาะเคสพัง พร้อมเทสปักสองเคสแยกกัน
3. **[informational]** `runtime.py` ยังไม่อ่านฟิลด์นี้ — ตามขอบเขตของใบสั่ง (ห้ามแตะ `runtime.py`)
   เขียน CORE-REQUEST ใน body ของ PR ให้ chief แล้ว (จุดแตะ: บล็อก coerce `composed.membership`
   coerce `composed.actor_identities` แบบเดียวกัน + stamp ผ่าน `mob_combat_membership.build_membership`
   เหมือนกิ่ง bg0002)

## เทส

ระหว่างทำ: `pytest tests/test_lane_a_scene_census.py` + เซตกว้างขึ้น
(`pytest tests/ -k "lane_a or census or field_mob or lane_hooks"`, 1120 passed)
ชุดเต็มรันสองครั้งรอบนี้ (เกินหนึ่งครั้งเพราะ pf-adversary ส่งผลกลับมาหลังรันเต็มครั้งแรก
ต้องรันซ้ำหลังแก้ตามผล ตามกฎห้าม push สภาพที่ยังไม่เคยรันเต็มหลังแก้ล่าสุด):
- ครั้งแรก (ก่อนแก้ตาม adversary): 9173 passed, 323 skipped, 17659 subtests, 0 failed
- ครั้งที่สอง (commit สุดท้ายจริง, หลังแก้ครบ): **9174 passed, 323 skipped, 17659 subtests, 0 failed**

## สถานะ PR (ตามจริง ห้ามเขียนว่าเสร็จ)

- `pirate-force-server#687`: **เปิดแล้ว มี marker ยืนยันด้วย GET แล้ว รอ gate-windows**
- `pf_bridge#1032`: claim PR ของรอบนี้ — เติม `PF-AUTOMERGE: v4` ทันทีหลังไฟล์รอบนี้ push
  = ปลดล็อก ไม่รอ gate ไม่รอ merge

## จดหมาย

- `notes_to_chief/20260904_0040_LANE-A-TO-COO-actor-identities-landed-pr687.md` (รายงานตามที่
  `2247` สั่งไว้ พร้อมเลข PR และบรรทัด merge-base)
- consumption stub ของ `2247` ลงแล้ว (`notes_to_chief/*2247*.CONSUMED.txt` + สำเนาใน `consumed/`)
