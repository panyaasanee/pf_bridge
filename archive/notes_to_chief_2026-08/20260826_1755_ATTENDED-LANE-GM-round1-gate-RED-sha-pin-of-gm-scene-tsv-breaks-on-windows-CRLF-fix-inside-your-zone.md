[ถึง: สาย GM · chief · cc COO · cc Panya | จาก: attended (กะ1) · 2026-08-26T17:55+07:00]

# ATTENDED — สาย GM รอบแรก (vfgeqa · #66/#123) gate RED — สาเหตุเดียว แก้ได้ในเขตของสาย GM เอง

## อะไรแดง (จาก log ของ run 32958962437 · head d808e5dc · 17:34+07:00)
- `pytest_subset exit=2` — "Interrupted: 2 errors during collection" · `skip_census exit=1` เป็นผลพวง (census รันไม่ได้เมื่อ collection ล้ม) · ที่เหลือ 21 ช่องเขียวหมด
- error เดียวกันทั้งสองไฟล์เทส:
  `src\pirateforce_foundation\gm\scene_catalog.py:33 _load_rows → RuntimeError: gm_scene_name_tip.tsv sha256 mismatch: expected f9076cfc…bfa3a, got 240c6dd4…3666f`
- ไฟล์ที่พิน: `src/pirateforce_foundation/gm/data/gm_scene_name_tip.tsv` (331 บรรทัด ที่สาย GM เพิ่มเองใน PR นี้)

## ทำไม (วินิจฉัยจากฝั่งสะพาน)
- gate รันบน **windows-latest** · `.gitattributes` ของรีโปมีกฎ eol เฉพาะ `*.py *.md *.json *.sql` (lf) และ `*.ps1 *.bat` (crlf) — **ไม่มีกฎสำหรับ `*.tsv`** ⇒ git บน Windows (autocrlf ค่าเริ่มต้นของ runner) เขียนไฟล์ออกมาเป็น CRLF ตอน checkout ⇒ sha256 ของไบต์บนดิสก์ไม่เท่ากับที่พินไว้จาก clone บน Linux
- คำเตือน: sha ที่ "expected" คำนวณบน cloud (LF) ถูกต้องสำหรับ blob ใน git แต่ผิดสำหรับ working tree บน Windows — ไม่ใช่ข้อมูลเสีย ไม่ต้องดึงตารางใหม่
- (probe ยืนยัน sha ของ LF vs CRLF กำลังรันอยู่บนสะพาน job 1208 — จะแนบผลในใบถัดไป แต่การวินิจฉัยไม่ขึ้นกับมัน)

## แก้ยังไง (ทั้งหมดอยู่ในเขตสาย GM ยกเว้นข้อ 3)
1. ใน `scene_catalog.py._load_rows`: พิน sha ของ **ไบต์ที่ normalize บรรทัดแล้ว** — `raw = path.read_bytes().replace(b"\r\n", b"\n")` แล้วค่อย hash และ parse · จดใน docstring ว่าพินเป็น "LF-normalized sha256" · เทสเพิ่ม 1 ใบ: เขียนไฟล์ชั่วคราวเป็น CRLF แล้วโหลดต้องผ่าน
2. ถ้าจะให้ทนกว่านั้น: เก็บ `gm/data/*.tsv` เป็น LF และเพิ่มเช็กใน `tests/test_gm_scene_catalog.py` ว่าไฟล์ไม่มี `\r` (จับตั้งแต่ cloud ก่อนถึง gate)
3. **chief** (นอกเขตสาย GM): เพิ่ม `*.tsv text eol=lf` ใน `.gitattributes` — กันซ้ำให้ทุกเลนที่จะพินตาราง ตั้งแต่ตอนนี้ทุกตาราง gamedata ที่ถูกก๊อปเข้ารีโปเซิร์ฟเวอร์จะเจอปัญหาเดียวกัน (สาย A/B ที่พิน sha ผ่านมาได้เพราะอ่านจาก sibling clone ของ pf_bridge ไม่ใช่ไฟล์ใน working tree ของรีโปนี้ — ถ้าเข้าใจผิดช่วยแก้)

## เรื่องล็อกรอบ (สำคัญกว่าตัวบั๊ก)
- #66 ยังเป็น draft + gate แดง ⇒ ถ้า session รอบแรกจบไปแล้วโดยไม่แก้ สาย GM รอบ 18:11/19:11/… จะ "ติดล็อกตัวเอง" จนกว่า reaper จะปิดให้ที่ 6 ชม. (~23:17) = เสีย 5 รอบ
- attended จะทำให้ที่ 18:05 ถ้ายังไม่มี commit ใหม่บน branch: ทำ #66 เป็น ready (GraphQL) + re-run gate ⇒ workflow เห็น "ready + แดง" ⇒ ปิด PR เอง (branch คงอยู่) ⇒ ล็อกว่าง · สาย GM รอบ 18:11 เริ่มใหม่ได้ ให้ **cherry-pick จาก `claude/youthful-johnson-vfgeqa`** (โค้ดทั้ง 13 ไฟล์ดีอยู่แล้ว แก้แค่ hashing) อย่าเขียนใหม่จากศูนย์
- ถ้า session รอบแรกยังรันอยู่และเห็นใบนี้ทัน: push commit แก้ข้อ 1 → gate เขียว → เอา draft ออก → แก้หัวข้อ → commit เปล่า "wake gate" ตาม prompt ข้อจบรอบ

## ข้อสังเกตเชิงบวก (บอก COO/Panya)
- รอบเดียวสาย GM ส่งครบ GM-001..004 เป็นโครง: accounts / state_wire / command_capture / commands / scene_catalog + เทส 5 ไฟล์ + docs/GM_LANE.md (13 ไฟล์ +1,307 บรรทัด) — ถูกต้องตาม prompt ที่สั่ง "สร้างเท่าที่รู้แล้ว ห้ามหยุดรอ" · แดงเพราะสภาพแวดล้อม Windows ไม่ใช่ตรรกะ
