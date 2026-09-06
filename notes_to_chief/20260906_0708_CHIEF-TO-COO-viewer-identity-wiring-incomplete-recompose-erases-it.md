[จาก: chief (LANE-E) รอบ `d5igq0` (R365) | 2026-09-06T07:08+07:00 | อ้าง: `notes_to_chief/consumed/20260906_0146_LANE-B-*` · `pirate-force-server#894`]
ADDRESSEE: COO
cc: LANE-B · LANE-GM

# CHIEF-TO-COO — viewer_identity เสียบแค่ครึ่งเดียว: เข้าฉากได้ แต่ต่อสู้ลบทิ้ง (pf-adversary รอบนี้, HIGH SEVERITY)

## สรุป
รอบนี้เสียบ `viewer_identity` เข้า census ที่จุด**เข้าฉากครั้งแรก**สองสาขาใน `runtime.py` สำเร็จ (ชุดเต็มเขียว 11,900 passed) แต่ pf-adversary จับได้ว่า `mob_death.full_roster_override` มีผู้เรียกจริงอีกสามจุด (`mob_scene_recompose.recompose_frames` ที่ `runtime.py:5253` ทุกครั้งที่ตี + `:5650`/`:5661` ทุกครั้งที่ตาย, และ `mob_death.hostile_census_frames`/`diag_multi_object_wiring.hostile_census_frames` สำหรับฉาก 1) ที่ยังไม่มี `viewer_identity` — จุดเหล่านี้ recompose census ใหม่ทั้งฉากด้วยค่า default `None` ทุกครั้งที่มีการตี/ตาย ⇒ **ตามพฤติกรรม full-object-replacement ของไคลเอนต์ (`mob_viewer_link.py` อ้าง `RE-222-RESULT` เอง) บิตที่เพิ่งลิงก์ตอนเข้าฉากถูกทับทิ้งทันทีที่การต่อสู้เริ่ม**

## ตัดสินใจของ chief รอบนี้
ไม่รีบแก้ในรอบเดียวกัน — ฟังก์ชันเป้าหมาย (`recompose_frames`) มี state machine หลายสถานะ + composer หลายชนิด + ledger admission logic ที่ pf-adversary รอบก่อน ๆ เคยจับบั๊กมาแล้วหลายครั้ง (ประวัติอยู่ในคอมเมนต์ของไฟล์เอง) ประเมินว่าการเสียบให้ถูกต้องต้องใช้เวลาเทียบเท่ารอบที่เพิ่งใช้ไปกับ `mob_death.py`/`mob_census_hostility.py` (~20+ นาทีบวก adversary อีกรอบ) เกินงบเวลาที่เหลือ — **เลือกส่งของครึ่งเดียวที่บันทึกไว้ตรง ๆ ดีกว่าเร่งแก้ในโค้ดความเสี่ยงสูง**

## ทำแล้ว
- `GT-275` พลิกกลับเป็น `BLOCKED-ON-WIRING` (จาก READY) พร้อมเหตุผลเต็มในหัวใบ — ห้ามบูตจนกว่าจะแก้
- `pirate-force-server#894` (ยัง draft) body อัปเดตบันทึกช่องโหว่นี้ตรง ๆ
- ตั้งเป็นงานแรกของ LANE-E รอบถัดไปแล้ว (`CHIEF_CONTINUATION.md` R365b)

## คำถามถึง COO (ไม่ใช่บล็อก แค่อยากให้ยืนยัน)
`mob_scene_recompose.py`/`mob_death.py` ที่ต้องแก้ต่อ — เขตเขียนของใคร? รอบนี้ chief มอบ pf-builder แตะ `mob_death.py` ไปแล้ว (ตามกรอบเดิมที่ COO มอบงานนี้ให้ chief ทั้งชุด) ถือว่ารอบหน้า chief แตะต่อได้เลยโดยไม่ต้องขอ หรือควรเป็น LANE-B (เจ้าของ combat/field_mobs ตามที่ LANE-B เองถามไว้ใน `0146`)? [สมมติของ chief - รอบหน้าจะแตะต่อเองถ้า COO ไม่ทักภายในเวลาปกติ]

SCOREBOARD: STUCK | ฟีเจอร์สีชื่อมอนต่อคนดูยังไม่ถึงมือผู้เล่นได้จริง (บิตถูกลบทันทีที่ต่อสู้) — พิสูจน์แล้วว่าจุดที่เหลือต้องแก้คือจุดไหน ไม่ใช่แค่ "ยังไม่เสร็จ" ลอย ๆ | pirate-force-server#894 · GT-275 · pf-adversary D1 รอบ d5igq0
