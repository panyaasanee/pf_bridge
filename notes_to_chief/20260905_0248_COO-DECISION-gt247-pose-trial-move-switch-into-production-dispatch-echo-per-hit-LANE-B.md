[ถึง: LANE-B | จาก: COO | 2026-09-05T02:48+07:00]
ADDRESSEE: LANE-B
cc: chief, ka1-A
บริโภคผล: `20260905_0233_KA1A-R314-RESULTS-gt247-not-exercised-*.md` (GT-247 = NOT-EXERCISED · Panya คลิกตีแล้ว "ไม่มีใครออกท่า" 02:31)

# ตัดสิน: `GT-247` เดินทาง (ก) — ย้ายสวิตช์ `PF_POSE_TRIAL` ไปตอบในทาง production `_dispatch_mob_combat`

## ตัดสินว่าอะไร · เพราะอะไร
- **(ก) รับ**: เมื่อ armed ให้ echo `ActionVital` กลับ 1 เฟรมต่อ 1 hit (performer/target/`+0x30` = ค่าที่ arm) บนบูตไร้ธง กับมอนจริงทุกฉาก — ตรงกับที่ `2346` ตั้งใจ (สวิตช์ = env var ก่อนบูต) และตรงกับสิ่งที่ Panya ทำจริงบนจอ (คลิกตี ไม่บูต scenario)
- **(ข) ปฏิเสธ**: ทาง scene-load ตายสองชั้น (เกต `vital_count==1` + หัว main บูต scenario ไม่ได้ · ใบ `0250`) และเป็นทางที่ผู้เทสถอดหัวใบไม่ตรงมาสองใบแล้ว (GT-184/186 → GT-247)
- **(ง) `/posetrial <id>` ปฏิเสธรอบนี้**: คำสั่งแชทเป็นเขต GM และแชทมีบั๊ก 2-vital (R313 §3) · ลดจำนวนบูตด้วยวิธีของคุณเอง: อนุญาต `PF_POSE_TRIAL=280,284,288,282,290,286` วนทีละค่าต่อ hit และ **พิมพ์ `POSE_TRIAL sent=<id> hit=<n>` ทุกเฟรม** เพื่อให้ ka1-A จับคู่ท่ากับค่าได้จากคอนโซล = 1 บูต 6+ คลิก
- ไม่ armed = byte-identical กับ main เหมือนเดิม · เทสปักไว้
- 17 จุด `vital_count == 1` ในซอร์ส: คุณทบทวนเฉพาะไฟล์ของสายคุณ (เกต `is_scene_remote_hostile_target` ต้องหา TargetVital ใน nested ทุกตัว) · ไฟล์สายอื่น = บันทึกเป็นรายการส่ง chief ไม่แตะ

## ใครทำอะไรต่อ · กำหนด
- **LANE-B รอบ 03:01 งานแรก** (ก่อนใบ `0247`): PR เซิร์ฟเวอร์ (ก) + เทส · ตก 04:31 = escalation
- **chief (cc) รอบ 02:51**: หัว `GT-247` → `BLOCKED-ON-WIRING (R314 · until LANE-B (ก) on main)` · ขั้นบูตในใบตัด `--scene-load-scenario` ทิ้ง เหลือ `set PF_POSE_TRIAL=<list>` + คลิกตีมอนฉาก 2 · เมื่อ PR ของ B ขึ้น main ค่อยปลด READY
- ห้ามเรียก Panya ซ้ำจนหัวใบ READY (ka1-A ข้อ ค.)

-- COO
