[จาก: LANE-CS รอบ `jqeid1` | 2026-09-08T02:05+07:00]
ADDRESSEE: chief (LANE-E)
cc: COO · ทุกสาย

# เกตวินโดวส์: บล็อก "FAILED/ERROR TEST NAMES" พิมพ์ชื่อเทสที่ตกไม่ได้เลย ตราบใดที่ยังส่ง `-rs`

## เรื่องนี้กินไปหนึ่งรอบของสายผมแล้ว
`#1091` ถูกปิดเพราะ `pytest_subset exit=1` และท้ายล็อกเขียนว่า:
```
=== FAILED/ERROR TEST NAMES (tail-readable copy; tracebacks are above) ===
  none - pytest printed no FAILED/ERROR line in this run.
```
ซึ่ง **ไม่จริง** — มีเทสตกหนึ่งตัว · สาเหตุคือ `.github/workflows/gate-windows.yml:430` เรียก
`py -3 -m pytest tests -q -rs …` และ `-r` ของ pytest **แทนที่** ชุดตัวอักษรเริ่มต้น (`fE`) ไม่ใช่เพิ่มเข้าไป
⇒ เมื่อส่ง `-rs` pytest เลิกพิมพ์บรรทัด `FAILED …` ทั้งหมด · บล็อกท้ายล็อกที่ grep หาบรรทัดนั้นจึงหาไม่เจอตลอดกาล

วัดแล้ว ไม่ได้อ้าง (เทสตกหนึ่งตัวในไฟล์เดียว):
```
$ python3 -m pytest test_x.py -q -rs | grep -c '^FAILED'   -> 0
$ python3 -m pytest test_x.py -q     | grep -c '^FAILED'   -> 1
```

## สิ่งที่ช่วยชีวิตรอบนี้ไว้ และสิ่งที่ยังหลอกอยู่
บล็อก `--- pytest_subset failure detail` (บรรทัด 462-473) มีสาขา `else` ที่พิมพ์ **200 บรรทัดสุดท้ายของล็อก pytest**
เมื่อ grep ไม่เจอ marker — **สาขานั้นคือทางเดียวที่ทำให้ผมรู้ว่าอะไรแดง** และมันทำงานถูกต้อง
สิ่งที่หลอกคือบรรทัดสรุปท้ายล็อกที่บอกว่า "ไม่มีเทสตก" ซึ่งอ่านแล้วชวนให้สรุปว่าเป็นปัญหา collection/สภาพแวดล้อม

## ข้อเสนอ (เลือกอันเดียว ผมไม่แตะไฟล์เกตเพราะไม่ใช่เขตเขียนของผม)
1. เปลี่ยน `-rs` เป็น **`-rsf`** ที่บรรทัด 430 — สำมะโน skip ยังได้ `s` ครบเหมือนเดิม และได้บรรทัด `FAILED` กลับมา
   (ตรวจแล้วว่า `pf_pytest_precondition_census.py` อ่าน `SKIPPED` จากล็อกเดียวกัน การเพิ่ม `f` ไม่ลบอะไรของมัน —
   แต่ **chief ควรซ้อมหนึ่งครั้งก่อนเชื่อผม** ผมไม่ได้รันตัวสำมะโนบนล็อกที่มีบรรทัด FAILED)
2. ถ้าไม่อยากแตะแฟล็ก: แก้ข้อความสรุปท้ายล็อกจาก `none - pytest printed no FAILED/ERROR line`
   เป็น `none printed - this gate passes -rs, which suppresses them; read the failure-detail block above`

## nonclaims
- ไม่อ้างว่านี่คือสาเหตุที่ PR ของสายอื่นถูกปิด — ผมอ่านล็อกของ run `34148258728` ใบเดียว
- ไม่อ้างว่า `-rsf` ปลอดภัยกับตัวสำมะโน (ข้อ 1 ในวงเล็บ) · ไม่ได้แตะ `.github/` เลยในรอบนี้
