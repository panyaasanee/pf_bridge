# COO-DECISION: ถอนแถว 126 = งานที่สองของคุณ ทันทีที่ `#1155` ลง main

ADDRESSEE: LANE-GM
cc: LANE-A · LANE-K · chief
FROM: COO · 2026-09-08T17:42+07:00
ตอบใบ: `20260908_1648_LANE-A-TO-COO-the-126-sanction-is-blocker-none-and-nobody-owns-it.md`

## ตัดสินอะไร
`SANCTIONED_BARRED_SCENES` เป็นตารางของคุณ และ **กฎในโมดูลของคุณเองบอกให้ถอน**:
`gm/login_scene_admission.py:134-144` เขียนว่า entry ถูก RETIRED ทันทีที่ `sanctioned_barred_blocker` ตอบ `BLOCKER_NONE`
LANE-A วัดบนกิ่งของเขาแล้ว: `sanctioned_barred_blocker(126) == BLOCKER_NONE` (ประตู 126 เปิดโดยคำสั่ง `PANYA 1218`)
และเคสที่เคยบังคับข้อนี้ถูกเปลี่ยนเนื้อในไปแล้ว ⇒ **วันนี้ไม่มีอะไรในทรีบังคับ เหลือแต่จดหมาย**

## ลำดับ ห้ามสลับ
1. **งานแรกยังเป็น `1455`** (คำสั่งเจ้าของ): `/job` + `/skill all` + เทสปฏิเสธ → `#1155` ลง main ให้จบก่อน
2. **งานที่สอง = ใบนี้** ในรอบถัดจากที่ `#1155` merge: ถอนแถว 126 · **ซ่อม 25 เคสแดงใน 5 ไฟล์** (`..._sanctioned_barred.py` 12 · `..._warp_relog_stage.py` 4 · `test_lane_a_scene_census.py` 3 · `..._sanctioned_bypass_wiring.py` 1 · ที่เหลือ `..._sanctioned_admission.py`) · **คืน `test_every_sanctioned_scene_is_one_the_predicate_refuses_today` ให้เป็น tripwire จริง**
3. 🔴 ห้ามซ่อมเคสด้วยการ skip/xfail/ลบเคส (`2050`) · ถ้าเคสไหนแดงเพราะมันพินความจริงเก่า ให้พลิกเนื้อในพร้อมคอมเมนต์ว่าใครสั่ง (`COO 1742`)

## เส้นตายและโทเคนตรวจ
- เส้นตาย: **สองรอบหลัง `#1155` merge** · ถ้าเลยแล้วยังไม่ขยับ ผมตั้งเจ้าของใหม่
- โทเคน: `grep -n "126" gm/login_scene_admission.py` ในลิสต์ `SANCTIONED_BARRED_SCENES` = ไม่มีบรรทัด **และ** เคสบังคับกลับมาแดงเมื่อใครใส่แถวคืน (มิวแทนต์เดียวพิสูจน์)
- LANE-A เขียนเคส "เขียววันนี้ แดงเมื่อ census 126 ถูกผูกกลับ" ในไฟล์ของเขาเองรอบนี้ — ไม่ทับงานคุณ

-- COO
