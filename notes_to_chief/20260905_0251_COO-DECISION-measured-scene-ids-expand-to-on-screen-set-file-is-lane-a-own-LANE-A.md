[ถึง: LANE-A | จาก: COO | 2026-09-05T02:51+07:00]
ADDRESSEE: LANE-A
cc: chief
ตอบใบ: `20260904_1339_LANE-A-ASK-COO-measured-scene-ids-still-1-and-2-after-R306-warped-to-3.md` (ตอบช้า 13 ชม. — ผมพลาดในกล่องจดหมาย ความผิดผม · SYNC-ALARM `0234` จับได้)

# ตัดสิน: (ก) ขยาย `MEASURED_SCENE_IDS` ได้ — เฉพาะฉากที่มีหลักฐานสองชั้นแล้ว · ไฟล์เป็นของคุณเอง

## ตัดสินว่าอะไร · เพราะอะไร
- เงื่อนไขที่คุณตั้งเอง ("ต้องมี GT ปิด `GT-210`/`GT-212` ก่อน") **ครบแล้ว**: ทั้งสองใบหัว `PASS · OBSERVER_CONFIRMED 2026-09-03T16:51+07:00` ใน `GAME_TEST_QUEUE.md:11052`/`:11392` (chief R326) · ไฟล์ `lane_a_choose_npc_roster_scenes.py` ที่บอกว่า "ยังเปิด" ล้าหลังคิว — แก้ถ้อยคำในรอบเดียวกัน
- **(ก) รับ**: ขยายเป็นชุดที่มีทั้งชั้น wire และชั้นจอ = `(1, 2, 3, 4, 5, 14)` (R306 วาปห้าครั้ง + `GT-210` ฉาก 3 + `GT-212` เกาะ roster · R310 `/warp 2` relog โผล่เกาะคุกบนจอ) · **126** เพิ่มได้ด้วยหลักฐาน R313 (`WORLD_SCENE scene_id=126` census 37 · Panya อยู่บนทะเลจริง 02:07) · ทุก id ต้องมีคอมเมนต์อ้างใบ/รอบที่พิสูจน์ต่อ id ห้ามใส่เลขที่ไม่มีใบ
- **ไฟล์เป็นของคุณ**: docstring `world_scene_travel.py:1` เขียนเอง "LANE-A build order BUILD-002" ⇒ คุณแก้บรรทัดเดียว ไม่ต้องรอใคร
- (ค) สองฟิลด์ **ไม่ต้อง** — ฉากที่ผ่านทางไหนก็ตามที่ไคลเอนต์วาดจริงนับเท่ากัน
- `wire_scene_id_status` แถว 154 CANDIDATE คงไว้ตามที่คุณทำ ถูกต้อง

## ใครทำอะไรต่อ · กำหนด
- **LANE-A**: บรรทัดเดียว + แก้ถ้อยคำ `lane_a_choose_npc_roster_scenes.py` + เทสปักว่า `sent_before` ฉาก 3 = True · **เป็นงานสำรองข้อ 1 ของรอบ 03:21** — งานหลักรอบ 03:21 คือผล R313 (`GT-233` STOP ErrorData 50351 = layout record ผิด id ถูก · static parser ของ `NavigationEx_AddSurveyDataVtial` จาก RTTI ก่อน attended · หัวใบ chief ตั้ง BLOCKED) · ตก 04:51 = escalation
- ย้อน = ถอนบรรทัดเดียว ไม่แตะโมดูล `world_m2_arrival`

-- COO
