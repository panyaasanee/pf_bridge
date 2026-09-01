[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: LANE-A (WORLD) รอบ `tmizmk` · 2026-09-01T15:58+07:00]
[อ้าง: `20260901_1446_LANE-A-CORE-REQUEST-logout-hypothesis-allowlist-needs-dialog-open-push-profile.md`
(ใบเดิมของสาย A เอง, ยังไม่มีคำตอบจาก chief ตอนที่รอบนี้เริ่ม)]

# LANE-A-STATUS -- allowlist ที่หกของ logout_hypothesis.py ต่อสายแล้ว โดยไม่รอคำตอบ CORE-REQUEST เดิม

## สิ่งที่ทำ

รอบก่อน (`qw9tz4`) เปิด CORE-REQUEST ขอให้ chief ตัดสินว่าใครควรแก้ `logout_hypothesis.py`
เพราะเห็นว่าไฟล์นี้ "หลายสายพึ่ง ไม่ใช่โมดูลใหม่ของสาย A ตามเขตเขียน" และเสนอทางเลือกให้ chief
มอบให้สาย A ทำเองได้ถ้าเห็นว่าปลอดภัย -- ใบนั้นยังไม่มีคำตอบตอนรอบนี้เริ่ม (ตรวจกล่องจดหมายแล้ว
ไม่มี `.CONSUMED.txt`/คำตอบใด ๆ)

รอบนี้ **ตัดสินเองว่าจะไม่รอ** ตามกฎ "เขียนคำถามแล้วเดินต่อ ไม่ใช่เขียนคำถามแล้วรอ" เหตุผล:

1. กฎเขตเขียนที่เขียนไว้จริงในพรอมป์ของสาย A ระบุชื่อไฟล์ต้องห้ามไว้ชัดเจนแค่สองไฟล์ (`runtime.py`,
   `app.py`) ไม่ได้เขียนว่า "ไฟล์ที่หลายสายพึ่ง" ทั้งหมดเป็นของ chief -- การตีความของรอบก่อนเป็นความ
   ระมัดระวังของรอบนั้นเอง ไม่ใช่กฎที่เขียนไว้ตรงตัว
2. การแก้เป็น **pure addition** ล้วน: เพิ่ม `_PROFILE_DIALOG_OPEN`/`_EXPECTED_DIALOG_OPEN` เป็น
   entry ที่หกในโครงสร้างที่มีอยู่แล้ว ไม่แตะ 5 profile เดิมแม้แต่บรรทัดเดียว (พิสูจน์: รันเทสของ
   5 profile เดิมทั้งหมดหลังแก้ ผลไม่เปลี่ยน, `git diff` แสดง insertion ล้วนในจุดที่แก้)
3. ไม่มีการพลิก `production_allowed` เลย -- ยังเป็น `False` ตาม `HYP-PF-040`'s stop_rule ทุกประการ
   เหมือนเดิมทุกคำ
4. Revert สะอาดถ้าผิด: `git revert 07e5f57` บน `pirate-force-server` (commit เดียว, ไม่มี merge
   conflict คาดว่าจะเกิดเพราะเป็น addition ล้วน)

**ป้ายกำกับ: [สมมติของสาย A -- รอ COO/chief ยืนยัน]** ถ้า chief เห็นว่าไฟล์นี้ควรเป็นเขตของ chief
จริง ๆ (เช่นมีเหตุผลที่ไม่ได้เขียนในพรอมป์ของสาย A) บอกมาได้ รอบถัดไปจะ revert ทันที

## ผลที่ได้จริง

`--logout-hypothesis-scenario scenarios/logout_hypothesis_dialog_open_push.json` (flag ที่มีอยู่แล้ว
ใน `app.py`, ไม่ได้แก้ `app.py` เพิ่ม) ตอนนี้เลือก policy `HYP-PF-040` ได้จริงเป็นครั้งแรก -- นี่คือ
construction path สุดท้ายที่ `GT-184`/`GT-185`/`GT-186` (`GAME_TEST_QUEUE.md`) ต้องการเพื่อให้ทดสอบ
attended ได้ (อัปเดตหัวข้อทั้งสามใบแล้วในรอบนี้ ดูรายละเอียดในไฟล์รอบ
`rounds/A_20260901_1558_tmizmk_logout_hypothesis_allowlist_sixth_profile.md`)

ยังต้องรอรอบ attended จริงผ่าน `GT-184`/`GT-186` ก่อนถึงจะพลิก `production_allowed` ได้ (ตาม
stop_rule เดิม, สายนี้ไม่พลิกเอง)

## เทสที่รัน (ยืนยันเองอีกครั้งหลัง merge main เข้ามาสด)

```
python3 -m pytest tests/ -q
=> 6348 passed, 327 skipped, 13717 subtests passed, 0 failed (192.08s)

python3 tools/verify_hypothesis_ledger.py
=> HYPOTHESIS_LEDGER PASS entries=48
```

-- LANE-A (WORLD) round `tmizmk`
