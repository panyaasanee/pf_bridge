# PF input inventory

สำรวจและคำนวณ SHA-256 แบบอ่านอย่างเดียว; ไม่รันหรือแก้ input และไม่ส่งออก raw dump/capture bytes

## Executable identity

- `GameClient.bin`: size 14759424, SHA-256 `c528bf43070e2789170f41b6e3e28ccec6b57bdc594ee73dfa061188a5d1e4bd`
- `GameClient.local.bin`: size 14759424, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- ผล: ขนาดเท่ากันแต่ SHA-256 ต่างกัน จึงเป็นคนละ `IMAGE` source และ A1-A4 ยังคงผูกกับ `GameClient.local.bin` เท่านั้น

## Census

- capture directories: 242
- IMAGE: 2 file(s), 29518848 byte(s)
- DUMP: 2 file(s), 26524651 byte(s)
- CAPTURE: 1772 file(s), 595134426 byte(s)
- DATA: 290 file(s), 93867 byte(s)

DATA census รอบนี้ครอบเฉพาะ XML 290 ไฟล์ที่อนุมัติเป็นหลักฐานนำเข้า; ไฟล์ Data ชนิดอื่นจะต้องเพิ่ม manifest ก่อนใช้อ้างข้อเท็จจริง
