# GT-116 + GT-121 + GT-120 RESULT 2026-08-28 09:25 +07:00 — **ทั้งสามใบ PASS ในบูตเดียว**: หน้าต่างสกิลเปิดได้ (มีอาชีพแล้ว) · สำมะโนเกาะคุกมาตอน arrival ไม่ต้องกดปุ่มเดิน · ปุ่ม GO! ไม่ค้างอีกแล้ว

ถึง: chief (GT-116/GT-120 เจ้าของ · ADDRESSEE: chief) · สาย A (GT-121 · ADDRESSEE: LANE-A) · สาย GM/B · RE runner · cc COO, กะ1-B
จาก: attended session "กะ1-A" (Panya ขับ UI เอง; brief → "ทราบ" → บูต; รวม 3 ใบใน 1 บูตตามคำสั่งเจ้าของ) · OBSERVER_CONFIRMED: 2026-08-28T09:2x+07:00 (คำเจ้าของ + ภาพ + วิดีโอ)

## บูต (jobs 1319 hold+resolve · 1320 boot_video · 1321 teardown กดโดยเจ้าของ 09:21 · release 1322)
- BOOT_COMMIT **98307ae** = main HEAD (เขียวของตัวเอง run 33134254855) ไร้แฟล็ก · ด่าน: grep 4/4 (class/level attr · tracepath handler · bg0002 arrival census · census composer) + pytest test_bg0002_census_wiring 12 passed · seed run DB Arena01 → scene_id=2 (26905,21185,1680) SEED_OK · canonical ไม่เปลี่ยน · teardown PASS
- วิดีโอ evidence_video\1320_g116_FULLROUND_20260828_091744.mkv · ภาพ evidence_screens\GT116_121_120_* · คอนโซล GameClient\capture_g116_20260828_091740\server_console_live.out.txt

## GT-121 (arrival census, สาย A) = PASS
- wire: `WORLD_CENSUS assembled=97/97 source=bg0002_full_roster` พิมพ์ที่ **HB#5** (ตอน arrival) · first `TargetPosVital` ที่ **HB#15** (10 heartbeat ต่อมา) ⇒ สำมะโนมาก่อนผู้เล่นขยับจริง (รอบ M1-P เดิม census มาหลัง TargetPos ใบแรก — แก้แล้ว) · anchor=(26905,21185,1680)=spawn (ผู้เล่นไม่ได้ขยับ)
- จอ (เจ้าของ): "เข้าแมพมา NPC ทุกตัวเกิดมารออยู่แล้ว **ผ่าน**" — ช่องว่างข้อ 1 ของ M1-P ปิด

## GT-116 (class/level → หน้าต่างสกิล, chief) = PASS (claim เดียว: หน้าต่างเปิดได้)
- จอ (เจ้าของ): "**หน้าต่างสกิลเปิดได้** แต่ยังไม่มีรายการใด ๆ" — ตรงเกณฑ์ P1/P2 ของใบเป๊ะ (level 1 มี 0 สกิลเป็นเรื่องปกติ ขอแค่หน้าต่างเปิด ซึ่งเดิมเปิดไม่ได้เพราะ class=0) ⇒ **คอขวด learn-skill ที่ค้างมาหลายใบ (GT-058/059/064) ปิดได้ที่ต้นเหตุ = ส่ง class+level** — ยืนยันสมมติฐาน "Attr ไม่ครบ = คอขวด" ของเจ้าของ
- nonclaim: ยังไม่วัดเนื้อในหน้าต่าง (รายการสกิลของ Gladiator) — ต้องมีตาราง skill ของ class 1 (คนละเรื่อง)

## GT-120 (map GO! ไม่ค้าง, chief) = PASS (claim เดียว: ข้อความไม่ค้างตลอดไป)
- wire: client ส่ง `0x4391` (CTracePathReqVital) → เซิร์ฟเวอร์ตอบ `[G>] TRACE_PATH_EMPTY_VECTOR_REPLY (35 bytes)` ทันที (late 0.4ms)
- จอ (เจ้าของ): กด GO! ที่ Warden Sebastian → "กำลังค้นหาเป้าหมาย.." ขึ้นแล้ว**หายใน 1 วินาที** (เดิมค้างตลอดไป) จากนั้นแชทขึ้น "เป้าหมายปัจจุบันไม่มีอยู่ หรือปัจจุบันไปยังตำแหน่งนั้นไม่ได้!" ⇒ ตรงเกณฑ์ P1 (ข้อความไม่ค้าง) + พฤติกรรม empty-vector fallback ตามที่ CORE-REQUEST-025 ตั้งใจ (ยังไม่มี waypoint/auto-walk — เป็นงานถัดไปถ้าต้องการให้ GO! เดินจริง)

## nonclaims รวม
- [ไม่อ้าง] ว่า GO! พาเดินไปหา NPC ได้ (ยังไม่ทำ auto-walk — ต้องส่ง path จริงจาก roster ตำแหน่ง) · [ไม่อ้าง] ว่าหน้าต่างสกิลแสดงสกิลถูกของ Gladiator · ทั้งสามวัดเฉพาะ claim เดียวของใบตัวเอง

## ต่อไป (เสนอ)
1. chief/สาย A ปิดหัวใบ GT-116/120/121 เป็น PASS · M1-P2 เหลือช่องว่าง 3/4/6 (สีชื่อ NPC เหลือง/มอน ส้ม-แดง-เทา · ความหนาแน่น+scale มอน · Pike ท่านอน/idle-walk) + ไอคอนเควส !/? เหนือหัว — ทั้งหมดเข้าแกน Attr completeness
2. GO! เดินจริง: สาย A ต่อ CTracePath ให้ตอบ path จริงจากตำแหน่ง roster (ตอนนี้ตอบ empty ⇒ client บอก "ไปไม่ได้") — ทำเมื่อว่างจาก identity
3. GT-114 DIAG (Mountain Deer สี/ศพ/แผงเป้า) ยังรอ chief wiring · RE-122 (ตัวเลข MP/stat จริงของ class 1 level 1) กำลังขุด

## หลักฐาน
คอนโซล L163/211-212 (census arrival), L2582 (TargetPos ทีหลัง), L2751-2752 (0x4391 → TRACE_PATH_EMPTY_VECTOR_REPLY) · outbox\1319 (pytest 12 passed, SEED_OK) · outbox\1321 (PASS) · ภาพ GT116_121_120_prison_exile_map_GO_sebastian_092033.png
