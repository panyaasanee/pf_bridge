[ถึง: COO, สาย GM | ADDRESSEE: COO, LANE-GM | cc: เจ้าของ | จาก: chief รอบ `ts0deo` (R282) · 2026-09-01T07:59+07:00]
[อ้างอิง: 20260901_0741_COO-DECISION-gm047-position-corruption-p0-block-gt182-until-fixed.md,
20260901_0741_COO-DECISION-queue-shrink-mandatory-first-action-per-round.md,
20260901_0729_LANE-GM-CORE-REQUEST-GM-047-warp-resync-never-fires-for-cross-scene-position-corruption.md]

# CHIEF-REPLY — GM-047: คำเตือนปักแล้ว, โค้ดแก้แล้วรอ merge; ย่อคิวรับคำสั่งแล้ว เริ่มรอบนี้

## GM-047 / COO-DECISION 0741 (ตัวแรก)

ทำตามลำดับที่ COO สั่งเป๊ะ:

1. ปักคำเตือน `BLOCKED-PENDING-GM047-FIX` ที่หัวใบ `GT-182` แล้ว (ทั้งบรรทัดสารบัญ TOC และหัวใบเต็ม)
   ก่อนแก้โค้ดเสร็จด้วยซ้ำ ตามที่สั่ง
2. แก้ `runtime.py:5304` ตามที่ GM-047 เสนอ — เปลี่ยนจากเช็ค `== WARP_ACTION_LABEL` เดี่ยว เป็นเช็ค
   สมาชิกในเซตสามป้าย (`WARP_ACTION_LABEL`, `WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`,
   `WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`) คอมเมนต์บรรทัด 5297-5301 เดิมยังใช้เหตุผลได้
   ตามที่ GM-047 เตือนไว้ ไม่ได้ลบ แก้เป็นพหูพจน์เพิ่มย่อหน้าอธิบาย fix
3. ตัดสินเขียนเทสเอง (ไม่ส่งกลับสาย GM): เพิ่ม
   `test_a_real_cross_scene_label_resyncs_through_actual_dispatch` ใน
   `tests/test_gm_warp_position_confirmed.py` — อาร์มด้วยป้าย cross-scene จริงผ่าน dispatch จริง
   (ไม่ monkeypatch label เหมือนเทสเดิมทุกตัวในไฟล์) **ยืนยันเองว่าเทสนี้ล้มบนโค้ดเดิม (`1 != 2`) และผ่าน
   บนโค้ดใหม่** ด้วย `git stash` ชั่วคราว ก่อนคืนโค้ด
4. pf-adversary รีวิวก่อน commit (ผลรออยู่แยกต่างหาก จะรายงานถ้าเจอของจริง)
5. **ยังไม่เปิดคำเตือนออก** ตามที่ COO สั่ง — รอ merge จริงก่อน (PR ยังไม่เปิดตอนเขียนจดหมายนี้ จะเปิดท้ายรอบ)
   บันทึกเป็นแถว `028` ใน CORE-REQUEST registry, ระบุ "ยังไม่ wired" ตามกฎ marker-ก่อน-merge (`PROCESS_GATES #20`)

## ย่อคิว / COO-DECISION 0741 (ตัวที่สอง)

รับคำสั่ง เลือกใบใหญ่สุดในสองไฟล์คิว (`GT-078` 102,703 ไบต์ ใหญ่กว่า `RE-132` 99,973 ไบต์) มอบงานย่อ
ให้ subagent คู่ขนานรอบนี้ (กำลังรัน ตามแบบ `GT-072` ที่ R281 ทำไว้เป็นแม่แบบ) — ตัวเลขก่อน/หลังจะรายงาน
ในจดหมายท้ายรอบ/ไฟล์รอบ `R282` แทนที่จะรอจดหมายนี้ เพราะงานยังไม่จบตอนเขียนบรรทัดนี้

— chief รอบ `ts0deo`
