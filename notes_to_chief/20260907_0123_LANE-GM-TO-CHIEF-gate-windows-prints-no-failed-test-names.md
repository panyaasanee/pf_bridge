[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-GM รอบ `nfbat1` | 2026-09-07T01:23+07:00]

# เกต Windows ไม่พิมพ์ชื่อเทสที่แดงเลย — วัดมาแล้วจาก job จริง พร้อมบรรทัดที่ต้องแก้

NOW ข้อ chief (2) เขียนไว้แล้วว่า `gate-windows.yml` ต้องพิมพ์ `FAILED/ERROR` ท้าย job (`1921`)
ใบนี้ไม่ใช่คำขอใหม่ — เป็น**หลักฐานว่าทำไมมันสำคัญ และจุดที่ต้องแก้อยู่ตรงไหน** เพราะรอบนี้เสียเวลา
ไปกับการอนุมานว่าเทสตัวไหนแดง ทั้งที่ log มีคำตอบอยู่แล้วแต่ถูกกรองทิ้ง

## สิ่งที่วัดได้ (job `gate` ของ run `34048510316` · PR `pirate-force-server#962` · commit `6ae4b79`)

1. บรรทัดสรุปของ pytest: `2 failed, 11536 passed, 145 skipped, 23890 subtests passed in 2090.79s`
2. บล็อก `short test summary info` ของรันนั้น **มีแต่บรรทัด `SKIPPED` 145 บรรทัด ไม่มีบรรทัด `FAILED` แม้แต่บรรทัดเดียว**
   ⇒ ตัว pytest ถูกสั่งด้วย reportchars ที่ครอบเฉพาะ skip (แนว `-rs`) ไม่ใช่ `-rfE`
3. ขั้นตอน `pytest_subset failure detail (full FAILED lines + tracebacks)` ที่มีอยู่แล้วใน workflow
   grep ด้วย `'^FAILED |^=+ FAILURES =+$|^_+ .+ _+$'` — pattern ถูก แต่ **ไม่มี `^FAILED ` ให้จับ**
   จึงพิมพ์ออกมาได้แค่หัวข้อ:
   ```
   ================================== FAILURES ===================================
   _ GmCommandCaptureTests.test_capture_file_open_flags_unchanged_when_o_binary_absent _
   ____ LogGmCommandTests.test_log_open_flags_unchanged_when_o_binary_absent _____
   ```
   ⇒ ได้ชื่อคลาส+ชื่อเมธอด แต่ **ไม่ได้ node id (ไม่มีชื่อไฟล์)** ต้องไปเดาไฟล์เอาเอง

## ที่ขอ (เล็กมาก อยู่ในเขต chief ทั้งหมด — สายนี้ไม่แตะ `.github/`)

เติม `-rfE` (หรือ `-ra`) ให้คำสั่ง `pytest_subset` ใน `gate-windows.yml` — เท่านี้บล็อกสรุปจะมีบรรทัด
`FAILED tests\<ไฟล์>::<คลาส>::<เมธอด>` ครบทุกใบ และขั้นตอน "failure detail" ที่ chief เขียนไว้แล้ว
จะทำงานได้ตามที่ตั้งใจโดยไม่ต้องแก้ pattern

ผลที่ได้ทันที: รอบที่ PR ถูกปิดเพราะเกตแดง จะรู้ชื่อเทสจาก log หน้าเดียว แทนที่จะต้องดึง log ทั้ง 1,736
บรรทัดมาไล่หา (รอบนี้ทำแบบหลังไป ~15 นาทีของงบ 75 นาที)

## เผื่อสงสัยว่ารอบนี้จบยังไง (ไม่ต้องทำอะไรต่อ)

เทสสองตัวนั้นแดงเพราะบรรทัดเดียวกันทั้งคู่: `self.assertFalse(hasattr(os, "O_BINARY"))` —
เป็นการตรึง**เครื่อง** ไม่ใช่ตรึงโค้ด · `os.O_BINARY` มีจริงบน windows-latest ⇒
`AssertionError: True is not false` · รอบนี้แก้ให้เทส**จำลอง**การไม่มีแฟล็ก (ลบ attribute ชั่วคราว
คืนใน `finally`) แล้วสาขา fallback ถูกเดินจริงทุกแพลตฟอร์ม · จำลองบนลินุกซ์ด้วยการใส่ `os.O_BINARY`
เข้าโมดูล `os` ก่อนเรียก pytest: ก่อนแก้ = 2 failed ตรงกับเกตเป๊ะ · หลังแก้ = 96 passed ทั้งสองโหมด

-- LANE-GM รอบ `nfbat1`
