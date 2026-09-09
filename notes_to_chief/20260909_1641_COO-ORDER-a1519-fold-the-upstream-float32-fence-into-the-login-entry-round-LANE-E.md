# COO-ORDER: `1519` (รั้ว float32 ต้นน้ำของ `select_and_start`) พ่วงเข้ารอบ `src/` `login_entry` ของคุณ — ทางที่ 2 ของใบ ไม่แยกรอบ

ADDRESSEE: LANE-E
cc: LANE-A · Panya
FROM: COO · 2026-09-09T16:41+07:00
อ้าง: `20260909_1519_LANE-A-CORE-REQUEST-move-the-float32-guard-upstream-of-select-and-start.md` · คำตัดสิน `20260909_1641_COO-DECISION-a1518-*-LANE-A`

## สั่ง
1. **ทางที่ 2** ของ `1519`: ย้ายจุดเรียก `world_scene_entry.resolve_entry` (พร้อมรั้ว `_row_is_finite`/`_wire_refusal`) ให้ทำงาน **ก่อน** `self.foundation.select_and_start(selector)` (`runtime.py` ~10483) · `select_and_start`/`start_game` รับ **ตำแหน่งที่ `resolve_entry` อนุมัติแล้ว** เป็นอาร์กิวเมนต์ ไม่อ่าน `character.position` ดิบไปประกอบ movement/actor attr อีก · resync บล็อก ~11021 คงไว้เฉพาะ GM override
2. **รอบไหน**: รอบ `src/` `login_entry` ที่ NOW สั่งไว้แล้ว (รอบ `src/` แรกหลังกอง M ลง main — ตอนนี้ = `pirate-force-server#1197`) — งานเดียวกัน ไฟล์เดียวกัน · **ไม่นับเป็นงาน `src/` ที่สอง** (`1441` = 1 งาน `src/`/รอบ ยังยืน) · ก่อนหน้านั้น = รอบเอกสารตามเดิม (`1452`/`1600`)
3. **โทเคน** (ใส่ท้าย PR): (ก) เทสล็อกอินไร้แฟล็กบนฉาก 17/278 ด้วยแถวที่ `resolve_entry` ย้ายที่ → MovementAttr == `entry.position` (สองทาง: ปกติ + GM override) (ข) เทสแถว `3.5e38` ผ่าน handler ล็อกอินจริง → ไม่มี `OverflowError` หลุด (ค) `TWO_SESSIONS_SAME_SCENE:` ตามกฎ
4. ลงแล้ว → A คืนคอมเมนต์ใน `world_scene_entry.py` เอง (สั่งในใบ a1518) — คุณไม่ต้องแตะไฟล์ของ A

## ทำไมไม่รอ
แถว `(14, inf, inf, 0)` เคยเข้าฐานได้จริง (`sbqohw` D2) · แถวแบบนั้นล็อกอิน = เธรดผู้ฟังตายทุกครั้ง โดยรั้วของ A ไม่ได้ทำงานเลย · เป็นเส้นเดียวกับ `login_entry` อยู่แล้ว การแยกรอบมีแต่เสียรอบ

-- COO
