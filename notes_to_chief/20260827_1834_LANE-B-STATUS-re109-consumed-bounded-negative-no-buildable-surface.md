ถึง: chief (cloud) / COO

# LANE-B STATUS — round B_20260827_1834: RE-109 consumed (bounded negative), no new buildable surface this round

เวลา: `2026-08-27T18:34+07:00`

## กล่องจดหมาย (addendum v2 section B)

หาด้วย `grep -rl "ADDRESSEE: LANE-B"` และไล่ใบที่ LANE-B เปิดเองที่ยังไม่มี `.CONSUMED.txt` — เจอหนึ่งใบ:

- **`notes_to_chief/20260827_1815_RE-109-RESULT-ACTOR-NAME-COLOR-DRIVER-BOUNDED.md`**
  (RE-109, เปิดโดย LANE-B รอบ 1734 ต่อยอดจาก PANYA-REFERENCE) → **CLOSED BOUNDED-NEGATIVE/DONE**
  ตัวเรา (`actor_type=3 → CMyActor → NameBoardPlayer`) กับมอน/NPC
  (`actor_type=4 → CNetNPC → NameBoardNPC`) เข้าคนละ board class ตั้งแต่ชั้น allocator —
  ห้ามสรุปว่า "ตัวเราขึ้นส้ม" กับ "มอนยังไม่ aggro ขึ้นส้ม" เป็น field เดียวกันจาก RGB ที่เท่ากัน
  Complete CFG ทั้งสอง body ไม่พบ direct call ไป FONT_COLOR loader/relationship comparator —
  consumer ที่เหลือเป็น virtual/resource state ที่ static resolve ต่อไม่ได้ `gamedata/**` มีตาราง
  `FONT_COLOR`/`FACTION`/`n_SKIN_COLOR` แต่ไม่มี crosswalk ผูกเข้ากับ `LABEL_NAME` — ห้าม join จากเลข ID
  `BUILD_IMPACT: NONE` — ห้าม hard-code สีจาก actor_type/faction/FONT_COLOR ID/n_SKIN_COLOR ในโค้ด lane นี้
  จนกว่าจะมี attended one-field A/B crosswalk (ที่ RE-109 เสนอไว้เป็น method ceiling ถัดไป)

ปิดหัวใบใน `CLIENT_RE_QUEUE.md` แล้ว (result section ต่อท้าย ไม่ลบของเดิม) วาง `.CONSUMED.txt` แล้ว
สำเนาต้นฉบับไป `notes_to_chief/consumed/` แล้ว ไม่มีใบอื่นค้างถึง LANE-B (ใบของ LANE-A/LANE-GM
ปล่อยให้สายนั้นบริโภคเอง)

## ทำไมรอบนี้ไม่มีโค้ดใหม่

ตรวจ `src/pirateforce_foundation/mob_combat.py`, `mob_death.py`, `mob_pickup.py`, `mob_loot.py`,
`mob_aggro.py`, `mob_ai_control.py`, `field_mobs.py` (repo `pirate-force-server`) หา marker
`PROVISIONAL`/`TODO`/`awaiting`/`not wired` — ทุกจุดที่เจอเป็น assumption ที่ติดป้ายรอคำตอบภายนอกอยู่แล้ว
(รอ `RE-110` สำหรับ attack cadence จริง, รอ COO สำหรับ pickup/aggro tuning ที่ confirm ไปแล้วบางจุด) ไม่มี
จุดไหนที่ตัดสินเองต่อได้แล้วยังไม่ทำ `RE-110`/`RE-111` (เปิดโดย LANE-B รอบ 1734 เช่นกัน) ยังไม่มีผลกลับมา

`lane_hooks/` skeleton ลง main แล้ว (R195) แต่ยังไม่เจอ COO-DECISION ที่ประกาศให้สาย A/B เริ่มลงทะเบียน
เอง (มีแค่ acknowledgment รอบ 1241) — ตาม addendum G ("chief ทำใบแรก รอ COO ประกาศ") lane B ยังไม่ย้าย
world-wipe fix (`runtime.py` bar_frames/death_frames) ไป `lane_hooks/lane_b_*.py` รอบนี้ รอสัญญาณนั้นก่อน
ไม่ใช่ตัดสินใจเอง เพราะแตะ `runtime.py` เป็นเขตของ chief

BUILD-004 (มอนสนามจริง, กำหนด 28 ส.ค. 12:00) ยืนยันสดแล้วรอบก่อน (13/13 mobs, 115/115 census) BUILD-005
(ตี/ตาย) มี attack-cadence gate ใหม่รออ chief ต่อสาย `MOB_COMBAT_CADENCE_WIRING` BUILD-006 (เก็บของ) มี
`dispatch_pickup_request()` แล้ว ไม่มี blocker ใหม่จากรอบนี้ที่ต้องรายงาน COO — ทั้งสามยังอยู่ในกำหนดเดิม

## เขตเขียนรอบนี้

`notes_to_chief/`, `CLIENT_RE_QUEUE.md` (เฉพาะหัวใบ RE-109 ที่ตัวเองเปิด), `rounds/` เท่านั้น — ไม่แตะ
`pirate-force-server` รอบนี้ (ไม่มีโค้ดที่ต้องแก้จากผล RE-109)
