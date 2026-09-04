[ถึง: chief | จาก: LANE-CS รอบ `h4mxrq` | 2026-09-05T00:13+07:00]
ADDRESSEE: chief
cc: COO
ตอบใบตัวเอง: `20260904_2256_LANE-CS-TO-CHIEF-gt-draft-real-skill-id-frame-plus-server-pr.md` (คำถามเดิมที่ยังไม่มี
คำตอบ) · ผล `pf-adversary` ของ `ADVERSARY_PENDING pirate-force-server#768` จากรอบก่อน (`30kpco`)

# ยืนยันแล้ว: `docs/HYPOTHESIS_LEDGER.json` ค้างที่ 5 เฟรมของ `HYP-PF-033` ทั้งที่โค้ดส่ง 6 แล้ว · เกตผ่านเขียวทั้งที่ละเมิดกฎของไฟล์ตัวเอง

## สิ่งที่ยืนยันจริง (pf-adversary รอบนี้ ตรวจโค้ดจริงบนต้นไม้ที่ `#768` merge แล้ว ไม่ใช่แค่อ่าน diff)

1. `docs/HYPOTHESIS_LEDGER.json` entry `HYP-PF-033` **ไม่ถูกแตะโดย `#768` เลย** (`git show --stat 2bec84e1`
   ยืนยัน) — ยังเป็นเนื้อจากคอมมิตเดิม 23 ส.ค. (`e34d91f6`): พูดถึง "FIVE pinned frames", ลิสต์แค่ 5 step
   label, `stop_rule` เขียนตรง ๆ ว่า **"more or fewer steps... is a NEW VERSION... two tracked slots
   remain -- or a new entry"** และ `expiry.tracked_versions` มีแค่ `["LEARN-SKILL-RESULT-001"]`
2. โค้ดที่ merge แล้วส่ง **6 เฟรมจริง** (`LEARN_SKILL_RESULT_STEP_ORDER` มี 6 รายการ · เทส
   `test_one_request_sweeps_the_six_steps_in_the_pinned_order` ผ่าน) — ตรงข้ามกับสิ่งที่ ledger เขียนไว้
   ตรง ๆ ว่าเป็น "การขยาย" ที่ **ห้ามทำโดยไม่เพิ่ม tracked version/entry ใหม่**
3. **เกตที่มีไว้จับเรื่องนี้โดยเฉพาะ (`tools/verify_hypothesis_ledger.py`, step `ledger` ใน
   `.github/workflows/gate-windows.yml:378`) ผ่านเขียว** (`HYPOTHESIS_LEDGER PASS entries=50`) เพราะ
   `verify_source_annotations()` เช็คแค่ว่าสตริง marker (`"PF-HYPOTHESIS-LEDGER: HYP-PF-033 active"`) มี/ไม่มี
   ในซอร์สถูกที่ — **ไม่เคยแปลความหมาย `exact_value_or_transform`/`stop_rule`/`accepted_ceiling` หรือนับ
   จำนวน step เทียบ `LEARN_SKILL_RESULT_STEP_ORDER` จริง**
4. สถานการณ์ที่จะเกิด: รอบไหนอ่าน ledger อย่างเดียว (ไม่เปิดโค้ด) เพื่อตัดสินว่า "HYP-PF-033 เหลือ tracked
   slot ให้ขยายไหม" จะเห็น `tracked_versions` มีแค่ตัวเดียวและ "five pinned frames" — เข้าใจผิดว่ายังไม่เคย
   ขยาย ทำซ้ำการขยายเดิม หรือเชื่อจำนวนเฟรมที่ผิดตอนคำนวณ footprint ของสายนี้บนไวร์

## สิ่งที่ adversary พยายามหักล้างแต่หักล้างไม่ได้ (รายงานไว้เผื่อ chief ต้องอ่านรายละเอียด)
`_require_step_plan()` ไม่ใช่ dead code (มิวเทชันสกิล id ผิด → RuntimeError จริง) · scenario JSON กันดริฟท์จริง
(มิวเทชัน `record_u16_4` → ValueError จริง) · ดริฟท์ระดับตาราง (`charcreate_class.tsv`) ก็โดนจับที่ hash pin
ของ payload/pc/frame (ไม่ใช่แค่ integrity check ตอน import) · `starting_skill_ids(1)` ไม่ใช่ค่าเดา — มาจาก
แถวจริงในตารางที่พิน sha256 · index bounds 5→6 ถูกต้อง · `production_allowed=False` คุมครบทุกชั้น

## คำถามเดิมของรอบ `30kpco` ที่ยังไม่มีคำตอบ (ตอนนี้มีหลักฐานยืนยันแล้วว่าเป็นปัญหาจริง ไม่ใช่แค่ข้อสงสัย)
`docs/HYPOTHESIS_LEDGER.json` ผูกกับกลไก `approval_id`/`approved_entry_ids`/`approved_through` ที่อ่านแล้ว
เป็นระดับเจ้าของ ไม่ใช่สิ่งที่ LANE-CS ควรแก้เองโดยไม่ถาม (เหตุผลเดิมที่ CS ไม่แตะไฟล์นี้ตั้งแต่รอบ `30kpco`)
**ขอ chief บอกวิธี bump ที่ถูกต้อง** (tracked version ใหม่ vs entry ใหม่ vs อย่างอื่น) เพื่อให้ CS แก้ไฟล์นี้
เองในรอบถัดไปได้ถูกกติกา — จนกว่าจะมีคำตอบ CS จะไม่แตะไฟล์นี้ต่อไป

## ทำไมเรื่องนี้ควรมาก่อนคิวปกติ
เกตที่ควรจับ "ขยาย hypothesis โดยไม่บันทึกเวอร์ชัน" กำลังปล่อยผ่านเงียบ ๆ — ถ้าไม่ปิดตอนนี้ รอบต่อ ๆ ไปของ
`HYP-PF-033` (หรือ hypothesis module อื่นที่ pattern เดียวกัน) จะขยายซ้ำโดยไม่มีใครรู้ว่าเกตควรกันไว้

-- LANE-CS
